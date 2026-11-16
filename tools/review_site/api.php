<?php
// JSON API of the team review site. GET reads, POST writes (with the X-CSRF header).
declare(strict_types=1);
require __DIR__ . '/lib.php';

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');

function out($data, int $code = 200) {
    http_response_code($code);
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}
function fail(string $msg, int $code = 400) { out(['error' => $msg], $code); }

set_exception_handler(function (Throwable $e) {
    error_log('review api: ' . $e);
    out(['error' => 'The server hit an error. Try again, or tell the admin.'], 500);
});

$a = $_GET['a'] ?? '';
$post = $_SERVER['REQUEST_METHOD'] === 'POST';
$in = [];
if ($post) {
    start_session();
    if (!hash_equals($_SESSION['csrf'] ?? '', $_SERVER['HTTP_X_CSRF'] ?? '')) fail('Your session expired. Reload the page.', 403);
    if (str_starts_with($_SERVER['CONTENT_TYPE'] ?? '', 'application/json')) {
        $in = json_decode((string)file_get_contents('php://input'), true) ?: [];
    } else {
        $in = $_POST;
    }
}
$s = fn(string $k, int $max = 20000) => mb_substr(trim((string)($in[$k] ?? '')), 0, $max);

// --- no login needed ------------------------------------------------------------

if ($post && $a === 'setup') {
    if (user_count() > 0) fail('The site is already set up.', 403);
    $name = $s('name', 40); $pw = (string)($in['password'] ?? '');
    if ($name === '' || mb_strlen($pw) < 10) fail('Choose a name and a password of at least 10 characters.');
    q('INSERT INTO users (name, pass_hash, role, created) VALUES (?, ?, ?, ?)',
        [$name, password_hash($pw, PASSWORD_DEFAULT), 'admin', now()]);
    log_in((int)db()->lastInsertId());
    out(['ok' => true]);
}
if ($post && $a === 'login') {
    if (too_many_attempts()) fail('Too many tries. Wait 15 minutes.', 429);
    $u = q('SELECT id, pass_hash FROM users WHERE name = ?', [$s('name', 40)])->fetch();
    if (!$u || !$u['pass_hash'] || !password_verify((string)($in['password'] ?? ''), $u['pass_hash'])) {
        q('INSERT INTO login_attempts (ip, at) VALUES (?, ?)', [client_ip(), time()]);
        fail('Name or password is wrong.', 401);
    }
    if (password_needs_rehash($u['pass_hash'], PASSWORD_DEFAULT))
        q('UPDATE users SET pass_hash = ? WHERE id = ?', [password_hash((string)$in['password'], PASSWORD_DEFAULT), $u['id']]);
    log_in((int)$u['id']);
    out(['ok' => true]);
}
if ($post && $a === 'accept_invite') {
    if (too_many_attempts()) fail('Too many tries. Wait 15 minutes.', 429);
    $u = q('SELECT id, invite_expires FROM users WHERE invite_token = ?', [$s('token', 100)])->fetch();
    if (!$u || $u['invite_expires'] < now()) {
        q('INSERT INTO login_attempts (ip, at) VALUES (?, ?)', [client_ip(), time()]);
        fail('This invite link is not valid any more. Ask the admin for a new one.', 403);
    }
    $pw = (string)($in['password'] ?? '');
    if (mb_strlen($pw) < 10) fail('The password needs at least 10 characters.');
    q('UPDATE users SET pass_hash = ?, invite_token = NULL, invite_expires = NULL WHERE id = ?',
        [password_hash($pw, PASSWORD_DEFAULT), $u['id']]);
    log_in((int)$u['id']);
    out(['ok' => true]);
}
if ($post && $a === 'logout') {
    start_session();
    $_SESSION = [];
    session_destroy();
    out(['ok' => true]);
}

// --- logged in ------------------------------------------------------------------

$me = current_user();
if (!$me) fail('Please log in.', 401);

// The language every read and write works on: ?l=de (or "lang" in the body).
$L = (string)($_GET['l'] ?? $in['lang'] ?? '');
if ($L === '' || !valid_lang($L)) $L = loaded_langs()[0] ?? 'de';
$lead = is_lead($me, $L);

if ($a === 'data') {
    $rel = current_release($L);
    if (!$rel) out(['empty' => true, 'lang' => $L]);
    $etag = '"' . $rel['release_id'] . '"';
    header('ETag: ' . $etag);
    header('Cache-Control: private, max-age=0, must-revalidate');
    if (($_SERVER['HTTP_IF_NONE_MATCH'] ?? '') === $etag) { http_response_code(304); exit; }
    if (!ini_get('zlib.output_compression') && extension_loaded('zlib')) ob_start('ob_gzhandler');
    readfile(release_path($rel['release_id']));
    exit;
}

if ($a === 'shot') {
    $sh = q('SELECT file FROM shots WHERE id = ?', [(int)($_GET['id'] ?? 0)])->fetch();
    $path = $sh ? data_dir() . '/shots/' . basename($sh['file']) : '';
    if (!$sh || !is_file($path)) fail('No such screenshot.', 404);
    $types = ['png' => 'image/png', 'jpg' => 'image/jpeg', 'webp' => 'image/webp', 'gif' => 'image/gif'];
    header('Content-Type: ' . ($types[pathinfo($path, PATHINFO_EXTENSION)] ?? 'application/octet-stream'));
    header('Cache-Control: private, max-age=31536000, immutable');
    header('Content-Length: ' . filesize($path));
    readfile($path);
    exit;
}

$ints = function (array $rows, array $cols) {
    foreach ($rows as &$r) foreach ($cols as $c) if (isset($r[$c])) $r[$c] = (int)$r[$c];
    return $rows;
};

if ($a === 'state') {
    $users = q('SELECT id, name, role, langs, last_seen, CASE WHEN pass_hash IS NULL THEN 1 ELSE 0 END AS invited FROM users ORDER BY name')->fetchAll();
    $reviews = q('SELECT id, msg_key, user_id, verdict, text, reason, updated FROM reviews WHERE lang = ?', [$L])->fetchAll();
    $votes = q('SELECT v.review_id, v.user_id FROM votes v JOIN reviews r ON r.id = v.review_id WHERE r.lang = ?', [$L])->fetchAll();
    $comments = q('SELECT id, msg_key, user_id, body, created FROM comments WHERE lang = ? ORDER BY id', [$L])->fetchAll();
    $decisions = q('SELECT msg_key, status, text, review_id, note, base_de, base_en, decided_by, updated, batch_id FROM decisions WHERE lang = ?', [$L])->fetchAll();
    $batches = q('SELECT id, name, created, created_by, item_count, sent_at, sent_by, sent_note FROM batches WHERE lang = ? ORDER BY id DESC', [$L])->fetchAll();
    $claims = q('SELECT area, user_id, claimed_at FROM claims WHERE lang = ?', [$L])->fetchAll();
    $glossary = q('SELECT id, en_term, de_term, note, status, user_id, updated FROM glossary WHERE lang = ? ORDER BY en_term', [$L])->fetchAll();
    // Screenshots of every language: a screen looks the same in all of them, so another
    // language's picture still shows where a text sits.
    $shots = q('SELECT id, lang, width, height, area, screen, caption, user_id, created FROM shots ORDER BY id')->fetchAll();
    $links = q('SELECT shot_id, msg_key, x, y, w, h, user_id FROM shot_links')->fetchAll();
    foreach ($links as &$k) foreach (['x', 'y', 'w', 'h'] as $c) $k[$c] = (float)$k[$c];
    unset($k);
    $rel = current_release($L);
    $releases = is_admin($me) ? q('SELECT release_id, lang, file, game_build, imported_at, is_current, messages FROM releases ORDER BY id DESC')->fetchAll() : [];
    out([
        'me' => $me + ['lead' => $lead],
        'lang' => $L,
        'langs' => loaded_langs(),
        'lang_names' => LANG_NAMES,
        'release' => $rel ? $rel['release_id'] : null,
        'users' => $ints($users, ['id', 'invited']),
        'reviews' => $ints($reviews, ['id', 'user_id']),
        'votes' => $ints($votes, ['review_id', 'user_id']),
        'comments' => $ints($comments, ['id', 'user_id']),
        'decisions' => $ints($decisions, ['review_id', 'decided_by', 'batch_id']),
        'batches' => $ints($batches, ['id', 'created_by', 'item_count', 'sent_by']),
        'claims' => $ints($claims, ['user_id']),
        'glossary' => $ints($glossary, ['id', 'user_id']),
        'shots' => $ints($shots, ['id', 'width', 'height', 'user_id']),
        'shot_links' => $ints($links, ['shot_id', 'user_id']),
        'releases' => $ints($releases, ['is_current', 'messages']),
        'csrf' => csrf(),
    ]);
}

if (!$post && $a === 'batch_export') {
    $b = q('SELECT * FROM batches WHERE id = ?', [(int)($_GET['id'] ?? 0)])->fetch();
    if (!$b) fail('No such batch.', 404);
    $items = q('SELECT msg_key, text, base_de, base_en FROM batch_items WHERE batch_id = ? ORDER BY msg_key', [$b['id']])->fetchAll();
    $slug = preg_replace('/[^A-Za-z0-9_-]+/', '-', $b['name']) ?: 'batch';
    $fname = "{$b['lang']}-batch-{$b['id']}-$slug";
    if (($_GET['fmt'] ?? 'json') === 'tsv') {
        $notes = [];
        foreach (q('SELECT msg_key, note FROM decisions WHERE lang = ?', [$b['lang']])->fetchAll() as $d) $notes[$d['msg_key']] = $d['note'];
        header('Content-Type: text/tab-separated-values; charset=utf-8');
        header("Content-Disposition: attachment; filename=\"$fname.tsv\"");
        $clean = fn($v) => preg_replace('/[\t\r\n]+/', ' ', (string)$v);
        echo "\u{FEFF}key\tenglish\t{$b['lang']} before\t{$b['lang']} new\treason\n";
        foreach ($items as $i)
            echo implode("\t", array_map($clean, [$i['msg_key'], $i['base_en'], $i['base_de'], $i['text'], $notes[$i['msg_key']] ?? ''])) . "\n";
        exit;
    }
    $o = [];
    foreach ($items as $i) $o[$i['msg_key']] = $i['text'];
    header('Content-Type: application/json; charset=utf-8');
    header("Content-Disposition: attachment; filename=\"$fname.json\"");
    echo json_encode($o, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT);
    exit;
}

if (!$post && $a === 'followup') {
    // What became of every sent change, judged against the language's current game file.
    $texts = current_texts($L);
    $rows = q('SELECT bi.batch_id, bi.msg_key, bi.text, bi.base_de, bi.base_en, b.name
               FROM batch_items bi JOIN batches b ON b.id = bi.batch_id
               WHERE b.lang = ? AND b.sent_at IS NOT NULL ORDER BY bi.batch_id', [$L])->fetchAll();
    $latest = [];
    foreach ($rows as $r) $latest[$r['msg_key']] = $r;   // later batches win
    $res = [];
    foreach ($latest as $k => $r) {
        $cur = $texts[$k] ?? null;
        if ($cur === null || $cur[0] !== $r['base_en']) $state = 'english_changed';
        elseif ($cur[1] === $r['text']) $state = 'taken';
        elseif ($cur[1] === $r['base_de']) $state = 'still_old';
        else $state = 'changed_differently';
        $res[] = ['key' => $k, 'state' => $state, 'batch_id' => (int)$r['batch_id'], 'batch' => $r['name'],
            'sent' => $r['text'], 'before' => $r['base_de'], 'en_then' => $r['base_en'],
            'en_now' => $cur[0] ?? null, 'de_now' => $cur[1] ?? null];
    }
    out(['items' => $res, 'release' => current_release($L)['release_id'] ?? null]);
}

if (!$post) fail('Unknown request.', 404);

// --- writes -----------------------------------------------------------------------

$msg = function (string $key) use ($L): array {
    $texts = current_texts($L);
    if (!isset($texts[$key])) fail('This message is not in the current game file.');
    return $texts[$key];
};
$need_lead = function () use ($lead) { if (!$lead) fail('Only a lead of this language can do this.', 403); };
$need_admin = function () use ($me) { if (!is_admin($me)) fail('Only the admin can do this.', 403); };
/** Take a message out of its package if that package is not sent yet. False if it was sent. */
$unpack = function (string $key) use ($L): bool {
    $d = q('SELECT batch_id FROM decisions WHERE lang = ? AND msg_key = ?', [$L, $key])->fetch();
    if (!$d || !$d['batch_id']) return true;
    $b = q('SELECT sent_at FROM batches WHERE id = ?', [$d['batch_id']])->fetch();
    if ($b && $b['sent_at']) return false;
    q('DELETE FROM batch_items WHERE batch_id = ? AND msg_key = ?', [$d['batch_id'], $key]);
    $n = (int)q('SELECT COUNT(*) FROM batch_items WHERE batch_id = ?', [$d['batch_id']])->fetchColumn();
    if ($n) q('UPDATE batches SET item_count = ? WHERE id = ?', [$n, $d['batch_id']]);
    else q('DELETE FROM batches WHERE id = ?', [$d['batch_id']]);
    q('UPDATE decisions SET batch_id = NULL WHERE lang = ? AND msg_key = ?', [$L, $key]);
    return true;
};
$rect = function () use ($in): array {
    $v = [];
    foreach (['x', 'y', 'w', 'h'] as $c) $v[$c] = max(0.0, min(1.0, (float)($in[$c] ?? 0)));
    if ($v['w'] < 0.003 || $v['h'] < 0.003) fail('Draw a box around the text on the screenshot first.');
    $v['w'] = min($v['w'], 1 - $v['x']); $v['h'] = min($v['h'], 1 - $v['y']);
    return $v;
};

switch ($a) {
    case 'review': {
        $key = $s('key', 255); [$en, $de] = $msg($key);
        $verdict = $in['verdict'] ?? '';
        if (!in_array($verdict, ['ok', 'fix'], true)) fail('Unknown verdict.');
        $text = $verdict === 'fix' ? $s('text') : null;
        if ($verdict === 'fix') {
            if ($text === '') fail('Write the text you suggest.');
            if (placeholders($text) !== placeholders($en)) fail('Keep the placeholders of the English text, like {driver}, exactly as they are.');
        }
        $reason = $s('reason', 2000);
        $old = q('SELECT id FROM reviews WHERE lang = ? AND msg_key = ? AND user_id = ?', [$L, $key, $me['id']])->fetch();
        if ($old) {
            q('UPDATE reviews SET verdict = ?, text = ?, reason = ?, base_de = ?, base_en = ?, updated = ? WHERE id = ?',
                [$verdict, $text, $reason, $de, $en, now(), $old['id']]);
            if ($verdict === 'ok') q('DELETE FROM votes WHERE review_id = ?', [$old['id']]);
        } else {
            q('INSERT INTO reviews (lang, msg_key, user_id, verdict, text, reason, base_de, base_en, updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                [$L, $key, $me['id'], $verdict, $text, $reason, $de, $en, now()]);
        }
        out(['ok' => true]);
    }
    case 'unreview': {
        $r = q('SELECT id FROM reviews WHERE lang = ? AND msg_key = ? AND user_id = ?', [$L, $s('key', 255), $me['id']])->fetch();
        if ($r) { q('DELETE FROM votes WHERE review_id = ?', [$r['id']]); q('DELETE FROM reviews WHERE id = ?', [$r['id']]); }
        out(['ok' => true]);
    }
    case 'vote': {
        $rid = (int)($in['review_id'] ?? 0);
        $r = q('SELECT user_id, verdict FROM reviews WHERE id = ?', [$rid])->fetch();
        if (!$r || $r['verdict'] !== 'fix') fail('That suggestion is gone.');
        if ((int)$r['user_id'] === $me['id']) fail('You can not agree with your own suggestion.');
        q('DELETE FROM votes WHERE review_id = ? AND user_id = ?', [$rid, $me['id']]);
        if (!empty($in['on'])) q('INSERT INTO votes (review_id, user_id) VALUES (?, ?)', [$rid, $me['id']]);
        out(['ok' => true]);
    }
    case 'comment': {
        $key = $s('key', 255); $msg($key);
        $body = $s('body', 4000);
        if ($body === '') fail('Write something first.');
        q('INSERT INTO comments (lang, msg_key, user_id, body, created) VALUES (?, ?, ?, ?, ?)', [$L, $key, $me['id'], $body, now()]);
        out(['ok' => true]);
    }
    case 'uncomment': {
        $c = q('SELECT user_id FROM comments WHERE id = ?', [(int)($in['id'] ?? 0)])->fetch();
        if ($c && ((int)$c['user_id'] === $me['id'] || $lead)) q('DELETE FROM comments WHERE id = ?', [(int)$in['id']]);
        out(['ok' => true]);
    }
    case 'claim': {
        $area = $s('area', 255);
        if ($area === '') fail('Pick an area.');
        $c = q('SELECT user_id FROM claims WHERE lang = ? AND area = ?', [$L, $area])->fetch();
        if ($c && (int)$c['user_id'] !== $me['id'] && !$lead) fail('Someone else has this area. Ask them or a lead.');
        q('DELETE FROM claims WHERE lang = ? AND area = ?', [$L, $area]);
        if (empty($in['release'])) q('INSERT INTO claims (lang, area, user_id, claimed_at) VALUES (?, ?, ?, ?)', [$L, $area, $me['id'], now()]);
        out(['ok' => true]);
    }
    case 'glossary': {
        $id = (int)($in['id'] ?? 0);
        $en = $s('en_term', 200); $de = $s('de_term', 200); $note = $s('note', 2000);
        $status = ($in['status'] ?? 'proposed') === 'agreed' ? 'agreed' : 'proposed';
        if ($status === 'agreed') $need_lead();
        if ($en === '') fail('Write the English term.');
        if ($id) {
            $g = q('SELECT user_id, status FROM glossary WHERE id = ? AND lang = ?', [$id, $L])->fetch();
            if (!$g) fail('That entry is gone.');
            if (!$lead && ((int)$g['user_id'] !== $me['id'] || $g['status'] === 'agreed')) fail('Only a lead can change this entry.', 403);
            q('UPDATE glossary SET en_term = ?, de_term = ?, note = ?, status = ?, updated = ? WHERE id = ?', [$en, $de, $note, $status, now(), $id]);
        } else {
            q('INSERT INTO glossary (lang, en_term, de_term, note, status, user_id, updated) VALUES (?, ?, ?, ?, ?, ?, ?)', [$L, $en, $de, $note, $status, $me['id'], now()]);
        }
        out(['ok' => true]);
    }
    case 'unglossary': {
        $g = q('SELECT user_id, status FROM glossary WHERE id = ?', [(int)($in['id'] ?? 0)])->fetch();
        if ($g && ($lead || ((int)$g['user_id'] === $me['id'] && $g['status'] !== 'agreed'))) q('DELETE FROM glossary WHERE id = ?', [(int)$in['id']]);
        out(['ok' => true]);
    }
    case 'decide': {
        $need_lead();
        $key = $s('key', 255); [$en, $de] = $msg($key);
        $status = $in['status'] ?? '';
        if (!in_array($status, ['approved', 'rejected', 'discuss'], true)) fail('Unknown decision.');
        $text = $status === 'approved' ? $s('text') : null;
        if ($status === 'approved') {
            if ($text === '' || $text === $de) fail('An approved change needs a text that differs from the current one.');
            if (placeholders($text) !== placeholders($en)) fail('The placeholders must match the English text.');
        }
        // A change in a package that is not sent yet leaves that package; a sent one stays
        // in its package, and the new decision goes out with the next one.
        $was_sent = !$unpack($key);
        q('DELETE FROM decisions WHERE lang = ? AND msg_key = ?', [$L, $key]);
        q('INSERT INTO decisions (lang, msg_key, status, text, review_id, note, base_de, base_en, decided_by, updated, batch_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)',
            [$L, $key, $status, $text, (int)($in['review_id'] ?? 0) ?: null, $s('note', 2000), $de, $en, $me['id'], now()]);
        out(['ok' => true, 'was_sent' => $was_sent]);
    }
    case 'undecide': {
        $need_lead();
        $key = $s('key', 255);
        if (!$unpack($key)) fail('This change was sent to the developers already. Decide again instead.');
        q('DELETE FROM decisions WHERE lang = ? AND msg_key = ?', [$L, $key]);
        out(['ok' => true]);
    }
    case 'batch_delete': {
        // Only a package that was not sent: its changes go back to "approved".
        $need_lead();
        $b = q('SELECT sent_at FROM batches WHERE id = ? AND lang = ?', [(int)($in['id'] ?? 0), $L])->fetch();
        if (!$b) fail('That package is gone.');
        if ($b['sent_at']) fail('This package was sent. Mark it as not sent first if that was a mistake.');
        $pdo = db();
        $pdo->beginTransaction();
        q('UPDATE decisions SET batch_id = NULL WHERE batch_id = ?', [(int)$in['id']]);
        q('DELETE FROM batch_items WHERE batch_id = ?', [(int)$in['id']]);
        q('DELETE FROM batches WHERE id = ?', [(int)$in['id']]);
        $pdo->commit();
        out(['ok' => true]);
    }
    case 'batch_sent': {
        $need_lead();
        $id = (int)($in['id'] ?? 0);
        if (!q('SELECT 1 FROM batches WHERE id = ? AND lang = ?', [$id, $L])->fetch()) fail('That package is gone.');
        if (!empty($in['sent'])) q('UPDATE batches SET sent_at = ?, sent_by = ?, sent_note = ? WHERE id = ?', [now(), $me['id'], $s('note', 500), $id]);
        else q('UPDATE batches SET sent_at = NULL, sent_by = NULL, sent_note = NULL WHERE id = ?', [$id]);
        out(['ok' => true]);
    }
    case 'batch_create': {
        $need_lead();
        $name = $s('name', 80) ?: ('Package ' . gmdate('Y-m-d'));
        $pdo = db();
        $pdo->beginTransaction();
        $items = q("SELECT msg_key, text, base_de, base_en FROM decisions WHERE lang = ? AND status = 'approved' AND batch_id IS NULL", [$L])->fetchAll();
        if (!$items) { $pdo->rollBack(); fail('No approved changes are waiting for a package.'); }
        q('INSERT INTO batches (lang, name, created, created_by, item_count) VALUES (?, ?, ?, ?, ?)', [$L, $name, now(), $me['id'], count($items)]);
        $bid = (int)$pdo->lastInsertId();
        foreach ($items as $i) {
            q('INSERT INTO batch_items (batch_id, msg_key, text, base_de, base_en) VALUES (?, ?, ?, ?, ?)',
                [$bid, $i['msg_key'], $i['text'], $i['base_de'], $i['base_en']]);
            q('UPDATE decisions SET batch_id = ? WHERE lang = ? AND msg_key = ?', [$bid, $L, $i['msg_key']]);
        }
        $pdo->commit();
        out(['ok' => true, 'id' => $bid, 'count' => count($items)]);
    }

    // --- screenshots ---
    case 'shot_upload': {
        $f = $_FILES['file'] ?? null;
        if (!$f || $f['error'] !== UPLOAD_ERR_OK) fail('The upload failed. Images up to ' . ini_get('upload_max_filesize') . ' work.');
        if ($f['size'] > 12 * 1024 * 1024) fail('The image is larger than 12 MB.');
        $info = @getimagesize($f['tmp_name']);
        $types = [IMAGETYPE_PNG => 'png', IMAGETYPE_JPEG => 'jpg', IMAGETYPE_GIF => 'gif'];
        if (defined('IMAGETYPE_WEBP')) $types[IMAGETYPE_WEBP] = 'webp';
        $ext = $info ? ($types[$info[2]] ?? null) : null;
        if (!$ext) fail('Upload a PNG, JPEG or WebP image.');
        $sl = (string)($in['shot_lang'] ?? '');
        $shotLang = ($sl === 'en' || valid_lang($sl)) ? $sl : $L;
        if (!is_dir(data_dir() . '/shots')) mkdir(data_dir() . '/shots', 0770, true);
        $file = bin2hex(random_bytes(12)) . '.' . $ext;
        if (!move_uploaded_file($f['tmp_name'], data_dir() . '/shots/' . $file)) fail('The server could not store the image.');
        q('INSERT INTO shots (lang, file, width, height, area, screen, caption, user_id, created) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            [$shotLang, $file, $info[0], $info[1], $s('area', 255), $s('screen', 255), $s('caption', 500), $me['id'], now()]);
        out(['ok' => true, 'id' => (int)db()->lastInsertId()]);
    }
    case 'shot_link': {
        $sid = (int)($in['shot_id'] ?? 0);
        if (!q('SELECT 1 FROM shots WHERE id = ?', [$sid])->fetch()) fail('That screenshot is gone.');
        $key = $s('key', 255); $msg($key);
        $r = $rect();
        q('DELETE FROM shot_links WHERE shot_id = ? AND msg_key = ?', [$sid, $key]);
        q('INSERT INTO shot_links (shot_id, msg_key, x, y, w, h, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)', [$sid, $key, $r['x'], $r['y'], $r['w'], $r['h'], $me['id']]);
        out(['ok' => true]);
    }
    case 'shot_unlink': {
        $l = q('SELECT user_id FROM shot_links WHERE shot_id = ? AND msg_key = ?', [(int)($in['shot_id'] ?? 0), $s('key', 255)])->fetch();
        if ($l && ((int)$l['user_id'] === $me['id'] || $lead)) q('DELETE FROM shot_links WHERE shot_id = ? AND msg_key = ?', [(int)$in['shot_id'], $s('key', 255)]);
        out(['ok' => true]);
    }
    case 'shot_delete': {
        $sh = q('SELECT file, user_id FROM shots WHERE id = ?', [(int)($in['id'] ?? 0)])->fetch();
        if (!$sh) out(['ok' => true]);
        if ((int)$sh['user_id'] !== $me['id'] && !is_lead($me)) fail('Only the uploader or a lead can delete a screenshot.', 403);
        q('DELETE FROM shot_links WHERE shot_id = ?', [(int)$in['id']]);
        q('DELETE FROM shots WHERE id = ?', [(int)$in['id']]);
        @unlink(data_dir() . '/shots/' . basename($sh['file']));
        out(['ok' => true]);
    }

    // --- accounts ---
    case 'user_create': {
        $need_admin();
        $name = $s('name', 40);
        $role = in_array($in['role'] ?? '', ROLES, true) ? $in['role'] : 'reviewer';
        if ($name === '') fail('Write a name.');
        if (q('SELECT 1 FROM users WHERE name = ?', [$name])->fetch()) fail('That name is taken.');
        $langs = implode(',', array_filter(array_map('trim', explode(',', $s('langs', 100))), 'valid_lang'));
        $tok = new_token();
        q('INSERT INTO users (name, role, langs, invite_token, invite_expires, created) VALUES (?, ?, ?, ?, ?, ?)',
            [$name, $role, $langs, $tok, gmdate('Y-m-d\TH:i:s\Z', time() + 14 * 86400), now()]);
        out(['ok' => true, 'token' => $tok]);
    }
    case 'user_reinvite': {
        $need_admin();
        $uid = (int)($in['id'] ?? 0);
        if ($uid === $me['id']) fail('You can not reset your own account here.');
        $tok = new_token();
        q('UPDATE users SET pass_hash = NULL, invite_token = ?, invite_expires = ? WHERE id = ?',
            [$tok, gmdate('Y-m-d\TH:i:s\Z', time() + 14 * 86400), $uid]);
        out(['ok' => true, 'token' => $tok]);
    }
    case 'user_role': {
        $need_admin();
        $uid = (int)($in['id'] ?? 0);
        if ($uid === $me['id']) fail('You can not change your own role.');
        if (!in_array($in['role'] ?? '', ROLES, true)) fail('Unknown role.');
        $langs = implode(',', array_filter(array_map('trim', explode(',', $s('langs', 100))), 'valid_lang'));
        q('UPDATE users SET role = ?, langs = ? WHERE id = ?', [$in['role'], $langs, $uid]);
        out(['ok' => true]);
    }
    case 'user_remove': {
        // Keeps the person's reviews and comments (shown as "former member"); stops the login.
        $need_admin();
        $uid = (int)($in['id'] ?? 0);
        if ($uid === $me['id']) fail('You can not remove yourself.');
        q('UPDATE users SET pass_hash = NULL, invite_token = NULL, role = ? WHERE id = ?', ['removed', $uid]);
        q('DELETE FROM claims WHERE user_id = ?', [$uid]);
        out(['ok' => true]);
    }
    case 'password': {
        $u = q('SELECT pass_hash FROM users WHERE id = ?', [$me['id']])->fetch();
        if (!password_verify((string)($in['old'] ?? ''), $u['pass_hash'])) fail('The current password is wrong.');
        if (mb_strlen((string)($in['new'] ?? '')) < 10) fail('The new password needs at least 10 characters.');
        q('UPDATE users SET pass_hash = ? WHERE id = ?', [password_hash((string)$in['new'], PASSWORD_DEFAULT), $me['id']]);
        out(['ok' => true]);
    }
    case 'import': {
        $need_admin();
        $f = $_FILES['file'] ?? null;
        if (!$f || $f['error'] !== UPLOAD_ERR_OK) fail('The upload failed. Is the file larger than the server allows (' . ini_get('upload_max_filesize') . ')?');
        $raw = (string)file_get_contents($f['tmp_name']);
        $data = json_decode($raw, true);
        if (!is_array($data) || empty($data['release']) || !is_array($data['rows'] ?? null) || !is_array($data['places'] ?? null))
            fail('This is not a data file from tools/locale_review.py.');
        $lang = (string)($data['lang'] ?? '');
        if (!valid_lang($lang)) fail('The data file names no language.');
        $rid = (string)$data['release'];
        if (!is_dir(data_dir() . '/releases')) mkdir(data_dir() . '/releases', 0770, true);
        file_put_contents(release_path($rid), $raw);
        $pdo = db();
        $pdo->beginTransaction();
        q('UPDATE releases SET is_current = 0 WHERE lang = ?', [$lang]);
        if (q('SELECT 1 FROM releases WHERE release_id = ?', [$rid])->fetch()) {
            q('UPDATE releases SET is_current = 1, imported_at = ?, imported_by = ? WHERE release_id = ?', [now(), $me['id'], $rid]);
        } else {
            q('INSERT INTO releases (release_id, file, game_build, lang, imported_at, imported_by, is_current, messages) VALUES (?, ?, ?, ?, ?, ?, 1, ?)',
                [$rid, (string)($data['file'] ?? ''), (string)($data['game_build'] ?? ''), $lang, now(), $me['id'], count($data['rows'])]);
        }
        $pdo->commit();
        out(['ok' => true, 'release' => $rid, 'lang' => $lang, 'messages' => count($data['rows'])]);
    }
}
fail('Unknown request.', 404);
