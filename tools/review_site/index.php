<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';

header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');
header('Referrer-Policy: no-referrer');
header("Content-Security-Policy: default-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data: blob:; script-src 'self'; frame-ancestors 'none'");

$me = current_user();
$mode = user_count() === 0 ? 'setup' : ($me ? 'app' : (isset($_GET['invite']) ? 'invite' : 'login'));
$boot = [
    'mode' => $mode,
    'csrf' => csrf(),
    'invite' => $mode === 'invite' ? (string)$_GET['invite'] : null,
    'title' => cfg('title', 'Team Principal Translation Review'),
];
$v = (string)filemtime(__DIR__ . '/app.js') . filemtime(__DIR__ . '/app.css') . filemtime(__DIR__ . '/shots.js');
?><!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title><?= htmlspecialchars($boot['title']) ?></title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="app.css?v=<?= $v ?>">
</head>
<body>
<div id="app" class="wrap"><p class="sub">Loading…</p></div>
<script id="boot" type="application/json"><?= json_encode($boot, JSON_HEX_TAG | JSON_HEX_AMP | JSON_UNESCAPED_UNICODE) ?></script>
<script src="shots.js?v=<?= $v ?>"></script>
<script src="app.js?v=<?= $v ?>"></script>
</body>
</html>
