<!DOCTYPE html>
<html>
<head>
<title>Minion Testing</title>

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

<h1> Take a test image! </h1>
<br>
<br>
<form method='post' action=''>
<input type='submit' name='capture' value='Capture!' />
<input type='submit' name='download' value='Capture & Download!' />
</form>
<br>
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
