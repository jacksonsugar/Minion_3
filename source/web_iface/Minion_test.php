<!DOCTYPE html>
<html>
<head>
<title>Minion XXX Testing</title>

<style>
    h1 {text-align: center;}
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
        background-color:lightskyblue;
    }
</style>
</head>
<body>

<h1> Test sampling functions on Minion XXX! </h1>
<br>
<fieldset>
<h3> Take a test image:</h3>
<br>
<form method='post' action=''>
<input type='submit' name='capture' value='Capture!' />
<input type='submit' name='download' value='Capture & Download!' />
</form>
</fieldset>
<fieldset>
<br>
<form method='post' action=''>
<input type='submit' name='pressure' value='Test connected pressure sensor' />
</form>
<br>

<?php
if(isset($_POST['pressure'])){

$command = escapeshellcmd('sudo python3 /home/pi/Documents/Minion_scripts/Pressure_test.py');
$output_pres = shell_exec($command);
echo "Pressure reading: " . $output_pres . " dbar";

}
?>
<br>
</fieldset>
<fieldset>
<br>
<form method='post' action=''>
<input type='submit' name='temperature' value='Test connected temperature sensor' />
</form>
<br>
<?php
if(isset($_POST['temperature'])){

$command = escapeshellcmd('sudo python3 /home/pi/Documents/Minion_scripts/Temperature_test.py');
$output_temp = shell_exec($command);
echo "Temperature reading: " . $output_temp . " C";

}
?>
<br>
</fieldset>
<fieldset>
<br>
<form method='post' action=''>
<input type='submit' name='GPS' value='Test connected Iridium GPS modem' />
</form>
<br>
<?php
if(isset($_POST['GPS'])){

$command = escapeshellcmd('sudo python /home/pi/Documents/Minion_scripts/Iridium_test.py');
$output_GPS = shell_exec($command);
echo $output_GPS;

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
<?php
if(isset($_POST['download'])){

$command = escapeshellcmd('sudo python /var/www/html/Image_test.py');
$output = shell_exec($command);

$file = '/home/pi/testimage.jpg';
$type = 'image/jpeg';
header('Content-Disposition: attachment; filename='.basename($file));
header('Content-Description: File Transfer');
header('Content-Type:'.$type);
header('Content-Transfer-Encoding: binary');
header('Expires: 0');
header('Cache-Control: must-revalidate');
header('Pragma: public');
header('Content-Length: ' . filesize($file));
ob_clean();
flush();
readfile($file);



}
?>

<?php
if(isset($_POST['capture'])){

$command = escapeshellcmd('sudo python /var/www/html/Image_test.py');
$output = shell_exec($command);
echo $output;

$file = '/home/pi/testimage.jpg';
$type = 'image/jpeg';
header('Content-Type:'.$type);
header('Content-Length: ' . filesize($file));
ob_clean();
flush();
readfile($file);

}
?>

