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
        /*background-color:lightskyblue;*/
    }
.testDiv {
    border: 5px outset red;
}
</style>
    <meta charset="UTF-8">
    <script type="text/javascript" src="autoUpdate.js"></script>
</head>

<body>

<?php
$message = "<h1>Download archive:  " . $_POST['download'] . $_GET['zipready'] . "</h1>";

echo $message;

?>


<br>
<br>
<p1>First Zip data to file:</p1>
<br>
<br>
<button type="button" onclick="window.open('Archive_Download.php?zipready=<?php echo $_POST['download'];?>','_blank');
window.open('ziparchives.php?dataname=<?php echo $_POST['download'];?>','_self');">
<?php echo "ZIP: " . $_POST['download'];?></button>
<br>
<br>
<p1>Second Download data:</p1>
<br>
<br>
<form method='post' action=''>
<input type='submit' name='senddata' value='Download:<?php echo $_GET['zipready'];?> ' />
</form>
<br>

<?php
if(isset($_POST['senddata'])){

$zip = "MXXX-" . $_GET['zipready'] . ".zip";

$zippath = "/var/www/html/" . $zip;

header('Content-Description: File Transfer');
header('Content-Type: application/octet-stream');
header('Content-Disposition: attachment; filename='.basename($zippath));
header('Content-Transfer-Encoding: binary');
header('Expires: 0');
header('Cache-Control: must-revalidate');
header('Pragma: public');
header('Content-Length: ' . filesize($zippath));
ob_end_clean();
ob_clean();
flush();
readfile($zippath);

}
?>

<div id="liveData">
    <p>Loading Data...</p>
</div>

<form action="/Minion_archive.php" method="post">
<input type="submit" value="Return">
</form>

</body>
</html>
