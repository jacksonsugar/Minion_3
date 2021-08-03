<!DOCTYPE html>
<html>
<head>
<title>Clear Minion XXX Data</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
        background-color:red;
    }
</style>
</head>
<body>

<h1>Clear Minion XXX Data!</h1>

<form method='post' action=''>
<input type='submit' name='clear' value='Clear Data' />
</form>
<br>
<br>
<form action="/View_Data.php" method="post">
<input type="submit" value="Return">
</form>
<br>
<br>
</body>
</html>
<br>
<br>

<?php
if(isset($_POST['clear'])){

$command = escapeshellcmd('sudo python /var/www/html/clear_minion_data.py');
$output = shell_exec($command);
echo $output;

}
?>
