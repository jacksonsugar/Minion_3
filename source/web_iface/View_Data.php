<!DOCTYPE html>
<html>
<head>
<title>View Data XXX</title>
<style>
    h1 {text-align: center;}
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
        /*background-color:lightskyblue;*/
    }
.testDiv {
    border: 5px outset red;
}
</style>
</head>
<body>
<h1> MINION XXX DATA </h1>

<fieldset>
<h2> minion_data/ </h2>

<?php

$output = null;
exec('ls /home/pi/Desktop/minion_data/', $output);
echo '<pre>';
foreach($output as $line)
    echo $line . "\n";
echo '</pre>';

?>
</fieldset>
<br><br>
<fieldset>
<h3>minion_data/INI/</h3>

<?php

$output = null;
exec('ls /home/pi/Desktop/minion_data/INI/', $output);
echo '<pre>';
foreach($output as $line)
    echo $line . "\n";
echo '</pre>';

?>
</fieldset>
<br><br>
<fieldset>
<h3>minion_data/FIN/</h3>

<?php

$output = null;
exec('ls /home/pi/Desktop/minion_data/FIN/', $output);
echo '<pre>';
foreach($output as $line)
    echo $line . "\n";
echo '</pre>';

?>
</fieldset>
<br><br>
<fieldset>
<h2> minion_pics/ </h2>

<?php

$output = null;
exec('ls /home/pi/Desktop/minion_pics/', $output);
echo '<pre>';
foreach($output as $line)
    echo $line . "\n";
echo '</pre>';

?>
</fieldset>
<br>
<br>
<?php

$command = escapeshellcmd('sudo python /var/www/html/get_telemetry.py');
$output = shell_exec($command);
echo $output;

?>
<br>
<br>
<form action="/Minion_Download.php" method='post'>
<input type='submit' value='Download Data' />
</form>

<br>
<br>

<form method='post' action=''>
<input type='submit' name='new_mission' value='Archive Data' />
</form>

<br>
<br>

<form action="/clear.php" method="post">
<input type="submit" value="Clear Data">
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
<br>
<br>
<br>
<br>
<br>

<?php
if(isset($_POST['new_mission'])){

$command = escapeshellcmd('sudo python /var/www/html/new_mission.py');
$output = shell_exec($command);
header("Refresh:0");
}
?>


