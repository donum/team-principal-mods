<?php
// Shared code of the team review site: config, database, sessions, accounts.
declare(strict_types=1);

if (!is_file(__DIR__ . '/config.php')) {
    http_response_code(500);
    exit('Copy config.sample.php to config.php and fill it in.');
}
$CONFIG = require __DIR__ . '/config.php';

const ROLES = ['admin', 'lead', 'reviewer'];

function cfg(string $k, $default = null) {
    global $CONFIG;
    return $CONFIG[$k] ?? $default;
}

function data_dir(): string {
    $d = cfg('data_dir', __DIR__ . '/data');
    if (!is_dir($d)) mkdir($d, 0770, true);
    return rtrim($d, '/\\');
}

function now(): string { return gmdate('Y-m-d\TH:i:s\Z'); }

// --- database ---------------------------------------------------------------

function db(): PDO {
    static $pdo = null;
    if ($pdo) return $pdo;
    $dsn = cfg('db_dsn') ?: 'sqlite:' . data_dir() . '/review.sqlite';
    $pdo = new PDO($dsn, cfg('db_user'), cfg('db_pass'), [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ]);
    if (is_sqlite()) {
        $pdo->exec('PRAGMA foreign_keys = ON');
        $pdo->exec('PRAGMA journal_mode = WAL');
        $pdo->exec('PRAGMA busy_timeout = 5000');
    } else {
        $pdo->exec("SET NAMES utf8mb4");
    }
    migrate($pdo);
    return $pdo;
}

function is_sqlite(): bool {
    return str_starts_with((string)(cfg('db_dsn') ?: 'sqlite:'), 'sqlite:');
}

function migrate(PDO $pdo): void {
    $sqlite = is_sqlite();
    $id = $sqlite ? 'INTEGER PRIMARY KEY AUTOINCREMENT' : 'INT AUTO_INCREMENT PRIMARY KEY';
    $key = $sqlite ? 'TEXT' : 'VARCHAR(255)';
    $txt = $sqlite ? 'TEXT' : 'MEDIUMTEXT';
    $end = $sqlite ? '' : ' ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin';
    // Every review table carries `lang`: one site serves all the game's languages.
    // base_de / base_en: the translated and the English text when the row was written.
    $short = $sqlite ? 'TEXT' : 'VARCHAR(16)';
    $tables = [
        "users (id $id, name $key NOT NULL UNIQUE, pass_hash $txt, role $key NOT NULL, langs $key,
            invite_token $key, invite_expires $key, created $key, last_seen $key)",
        "releases (id $id, release_id $key NOT NULL UNIQUE, file $key, game_build $key, lang $short NOT NULL,
            imported_at $key, imported_by INT, is_current INT NOT NULL DEFAULT 0, messages INT)",
        "reviews (id $id, lang $short NOT NULL, msg_key $key NOT NULL, user_id INT NOT NULL, verdict $key NOT NULL,
            text $txt, reason $txt, base_de $txt, base_en $txt, updated $key, UNIQUE (lang, msg_key, user_id))",
        "votes (review_id INT NOT NULL, user_id INT NOT NULL, PRIMARY KEY (review_id, user_id))",
        "comments (id $id, lang $short NOT NULL, msg_key $key NOT NULL, user_id INT NOT NULL, body $txt, created $key)",
        "decisions (lang $short NOT NULL, msg_key $key NOT NULL, status $key NOT NULL, text $txt, review_id INT,
            note $txt, base_de $txt, base_en $txt, decided_by INT, updated $key, batch_id INT, PRIMARY KEY (lang, msg_key))",
        "batches (id $id, lang $short NOT NULL, name $key, created $key, created_by INT, item_count INT)",
        "batch_items (batch_id INT NOT NULL, msg_key $key NOT NULL, text $txt, base_de $txt, base_en $txt,
            PRIMARY KEY (batch_id, msg_key))",
        "claims (lang $short NOT NULL, area $key NOT NULL, user_id INT NOT NULL, claimed_at $key, PRIMARY KEY (lang, area))",
        "glossary (id $id, lang $short NOT NULL, en_term $key NOT NULL, de_term $key, note $txt, status $key NOT NULL,
            user_id INT, updated $key)",
        // Screenshots: one image of a screen, in one language, linked to many messages,
        // each with the rectangle (fractions of the image, 0..1) where that message shows.
        "shots (id $id, lang $short NOT NULL, file $key NOT NULL, width INT, height INT, area $key, screen $key,
            caption $txt, user_id INT, created $key)",
        "shot_links (shot_id INT NOT NULL, msg_key $key NOT NULL, x REAL, y REAL, w REAL, h REAL, user_id INT,
            PRIMARY KEY (shot_id, msg_key))",
        "login_attempts (ip $key NOT NULL, at INT NOT NULL)",
    ];
    foreach ($tables as $t) $pdo->exec("CREATE TABLE IF NOT EXISTS $t$end");
    // Columns added after the first version: a package is sent when a lead says so.
    add_column($pdo, 'batches', 'sent_at', $key);
    add_column($pdo, 'batches', 'sent_by', 'INT');
    add_column($pdo, 'batches', 'sent_note', $txt);
}

function add_column(PDO $pdo, string $table, string $col, string $type): void {
    $cols = is_sqlite()
        ? array_column($pdo->query("PRAGMA table_info($table)")->fetchAll(), 'name')
        : $pdo->query("SHOW COLUMNS FROM $table")->fetchAll(PDO::FETCH_COLUMN);
    if (!in_array($col, $cols, true)) $pdo->exec("ALTER TABLE $table ADD COLUMN $col $type");
}

function q(string $sql, array $args = []): PDOStatement {
    $st = db()->prepare($sql);
    $st->execute($args);
    return $st;
}

// --- sessions and accounts ----------------------------------------------------

function start_session(): void {
    if (session_status() === PHP_SESSION_ACTIVE) return;
    $https = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
        || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https');
    session_name('tpreview');
    session_set_cookie_params(['lifetime' => 60 * 60 * 24 * 30, 'path' => '/', 'secure' => $https,
        'httponly' => true, 'samesite' => 'Lax']);
    ini_set('session.gc_maxlifetime', (string)(60 * 60 * 24 * 30));
    session_start();
    if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(16));
}

function csrf(): string { start_session(); return $_SESSION['csrf']; }

function current_user(): ?array {
    start_session();
    $id = $_SESSION['uid'] ?? null;
    if (!$id) return null;
    $u = q('SELECT id, name, role, langs FROM users WHERE id = ? AND pass_hash IS NOT NULL', [$id])->fetch();
    if (!$u) { unset($_SESSION['uid']); return null; }
    if (($_SESSION['seen'] ?? 0) < time() - 300) {
        q('UPDATE users SET last_seen = ? WHERE id = ?', [now(), $id]);
        $_SESSION['seen'] = time();
    }
    $u['id'] = (int)$u['id'];
    return $u;
}

/** A lead decides for the languages in users.langs (comma list, empty = all). */
function is_lead(?array $u, ?string $lang = null): bool {
    if (!$u) return false;
    if ($u['role'] === 'admin') return true;
    if ($u['role'] !== 'lead') return false;
    $langs = array_filter(array_map('trim', explode(',', (string)($u['langs'] ?? ''))));
    return !$langs || $lang === null || in_array($lang, $langs, true);
}

const LANG_NAMES = ['de' => 'German', 'fr' => 'French', 'es' => 'Spanish', 'it' => 'Italian',
    'pt-BR' => 'Portuguese (Brazil)', 'ru' => 'Russian'];

function valid_lang(string $l): bool { return (bool)preg_match('/^[a-z]{2}(-[A-Z]{2})?$/', $l); }
function is_admin(?array $u): bool { return $u && $u['role'] === 'admin'; }

function user_count(): int { return (int)q('SELECT COUNT(*) FROM users')->fetchColumn(); }

function client_ip(): string { return $_SERVER['REMOTE_ADDR'] ?? 'unknown'; }

function too_many_attempts(): bool {
    q('DELETE FROM login_attempts WHERE at < ?', [time() - 900]);
    return (int)q('SELECT COUNT(*) FROM login_attempts WHERE ip = ?', [client_ip()])->fetchColumn() >= 10;
}

function log_in(int $uid): void {
    start_session();
    session_regenerate_id(true);
    $_SESSION['uid'] = $uid;
    q('UPDATE users SET last_seen = ? WHERE id = ?', [now(), $uid]);
}

function new_token(): string { return rtrim(strtr(base64_encode(random_bytes(18)), '+/', '-_'), '='); }

// --- releases (the data files from tools/locale_review.py) ---------------------

function current_release(string $lang): ?array {
    return q('SELECT * FROM releases WHERE is_current = 1 AND lang = ? ORDER BY id DESC LIMIT 1', [$lang])->fetch() ?: null;
}

/** Languages with a loaded game file, in the order of LANG_NAMES. */
function loaded_langs(): array {
    $l = q('SELECT DISTINCT lang FROM releases WHERE is_current = 1')->fetchAll(PDO::FETCH_COLUMN);
    $rank = function ($x) { $i = array_search($x, array_keys(LANG_NAMES), true); return $i === false ? 99 : $i; };
    usort($l, fn($a, $b) => $rank($a) <=> $rank($b));
    return $l;
}

function release_path(string $release_id): string {
    return data_dir() . '/releases/' . preg_replace('/[^A-Za-z0-9_.-]/', '_', $release_id) . '.json';
}

/** key => [english, translation] of the language's current release, cached for the request. */
function current_texts(string $lang): array {
    static $maps = [];
    if (isset($maps[$lang])) return $maps[$lang];
    $map = [];
    $rel = current_release($lang);
    if ($rel) {
        $data = json_decode((string)file_get_contents(release_path($rel['release_id'])), true);
        foreach ($data['rows'] ?? [] as $r) $map[$r[0]] = [$r[1], $r[2]];
    }
    return $maps[$lang] = $map;
}

function placeholders(string $s): array {
    preg_match_all('/\{[^{}\n]*\}|<[^>\n]+>|\[[A-Z_\/]+\]|%[sd]/', $s, $m);
    $p = $m[0];
    sort($p);
    return $p;
}
