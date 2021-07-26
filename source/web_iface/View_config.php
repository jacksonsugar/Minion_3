<!DOCTYPE html>
<html>
<head>
<title>View XXX Config</title>

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

<h2>Minion XXX Config File</h2>

<?php

if ($file = fopen("/home/pi/Desktop/Minion_config.ini", "r")) {
    while(!feof($file)) {
        $line = fgets($file);
        echo $line;
        echo nl2br("\n");
    }
    fclose($file);
}

?>

<br>
<form action="/index.php" method="post">
<input type="submit" value="Return">
</form>
</body>
</html>
<br>
<br>
<br>
<br>
<br>
