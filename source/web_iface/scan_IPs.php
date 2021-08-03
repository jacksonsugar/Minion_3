<!DOCTYPE html>
<html>
<head>
<title>View Minion IPs</title>

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

<h1>Scan network for connected devices!</h1>

<fieldset>
<br>
<form method='post' action=''>
<input type='submit' name='IPs' value='Scan now!' />
</form>
<br>
<?php
if(isset($_POST['IPs'])){

$command = escapeshellcmd('sudo python /var/www/html/scan_network.py');
$output_IPs = shell_exec($command);
echo nl2br($output_IPs);

}
?>
<br>
</fieldset>

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

