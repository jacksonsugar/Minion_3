<!DOCTYPE html>
<html>
<head>
<title>Config Submitted Submitted</title>

<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
        background-color:lightskyblue;
    }
</style>
</head>
<body>

<?php

$command = escapeshellcmd('sudo python /var/www/html/writeconfig.py');
$output = shell_exec($command);
echo $output;

?>

<h>  Config written!</h>

<br>
<form action="/index.php" method="post">
<input type="submit" value="Return">
</form>
</body>
</html>
