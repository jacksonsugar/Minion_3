<html>
<head>
    <title>Close Me</title>
</head>

<body>

<h1>Data files are compressed!</h1>

<br>
<br>

<?php

echo $_GET['dataname'];

echo exec('sudo python /var/www/html/ziparchives.py ' . $_GET['dataname']);

echo "<script>window.close();</script>";

?>

<form action="/index.php" method="post">
<input type="submit" value="Return">
</form>


</body>
</html>
