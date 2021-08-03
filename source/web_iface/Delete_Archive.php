<!DOCTYPE html>
<html>
<head>
<title>Download Data XXX</title>
<style>
    h1 {text-align: center;}
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
        background-color:red;
    }
.testDiv {
    border: 5px outset red;
}
</style>
</head>

<body>

<h1>Delete Minion XXX Data Archive?</h1>

<br>
<br>

<?php

$message = "<h3>Delete archive ".$_POST['remove']."?</h3>";

echo $message;

echo "<form method='post' action=''>
    <input type='submit' name='delete' value='Delete' />
    <input type='hidden' name='delete' value='".$_POST['remove']."' />
    </form><br><br>";

?>

<form action="/Minion_archive.php" method="post">
<input type="submit" value="Return">
</form>
<br>
<br>


<?php
if(isset($_POST['delete'])){

$path = '/home/pi/Desktop/minion_memory/'.$_POST['delete'];

$com = 'sudo rm -r '.$path;

$command = escapeshellcmd($com);
$output = shell_exec($command);

echo "Archive Deleted";

}
?>

</body>
</html>
