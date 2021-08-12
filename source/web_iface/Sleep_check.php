<!DOCTYPE html>
<html>
<head>
<title>Config XXX Submitted</title>

<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
        background-color:green;
    }
</style>
</head>
<body>

<br>
<h1>Minion XXX launch prep</h1>
<br>
<br>
<h3>Step 1: Reset sample counter and archive previous data.</h3>
<form method='post' action=''>
<input type='submit' name='new_mission' value='Archive data and begin mission' />
</form>
<br>
<h3>Step 2: Turn Minion off before deployment.</h3>
<form method='post' action=''>
<input type='submit' name='shutdown' value='Set Minion XXX to Sleep' />
</form>
<br>
<h3>Step 3: After 30 seconds, attach the magent to keep the Minion off.</h3>
<br>
<form action="/index.php" method="post">
<input type="submit" value="Return">
</form>
<br>
<br>
</body>
</html>


<?php
if(isset($_POST['new_mission'])){

$command = escapeshellcmd('sudo python /var/www/html/new_mission.py');
$output = shell_exec($command);
echo $output;
echo '<br>Ready to begin Mission!<br>';
}
?>

<?php
if(isset($_POST['shutdown'])){

$command = escapeshellcmd('sudo python /var/www/html/Minion_sleep.py');
$output = shell_exec($command);
echo "Minion returned to sleep cycle!\n";
echo "Goodbye!";
}
?>
