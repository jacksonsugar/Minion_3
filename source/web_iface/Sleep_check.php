<!DOCTYPE html>
<html>
<head>
<title>Config 52 Submitted</title>

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
<h1>  Are you sure you want to put Minion 52 to sleep?</h1>
<br>
<br>
<form method='post' action=''>
<input type='submit' name='shutdown' value='Set Minion 52 to Sleep' />
</form>

<br>
<form action="/index.php" method="post">
<input type="submit" value="Return">
</form>
<br>
<br>
</body>
</html>


<?php
if(isset($_POST['shutdown'])){

$command = escapeshellcmd('sudo python /var/www/html/Minion_sleep.py');
$output = shell_exec($command);
echo "Minion returned to sleep cycle!\n";
echo "Goodbye!";
}
?>
