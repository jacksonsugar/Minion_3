<html>
<head>
    <title>Close Me</title>
</head>

<body>

<h1>Data files are being compressed</h1>

<br>
<br>

<?php

echo exec('sudo python /var/www/html/zipfiles.py');

echo "<script>window.close();</script>";

?>

<form action="/index.php" method="post">
<input type="submit" value="Return">
</form>


</body>
</html>
