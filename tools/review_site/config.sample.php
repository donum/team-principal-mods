<?php
// Copy this file to config.php on the server and change what you need.
return [
    // Shown in the browser tab and the page header.
    'title' => 'Team Principal Translation Review',

    // Where the database and the uploaded data files live. The default is the
    // data/ folder next to this file, which its .htaccess locks. A folder
    // outside the web space is even safer, for example '/is/htdocs/wpXXXX/review-data'.
    // 'data_dir' => __DIR__ . '/data',

    // Leave empty for SQLite (one file in data_dir, nothing to set up).
    // For MySQL: 'mysql:host=localhost;dbname=db123;charset=utf8mb4'
    'db_dsn' => '',
    'db_user' => null,
    'db_pass' => null,
];
