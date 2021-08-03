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
</head>

<body>

<h1>Minion XXX Data Archive</h1>

<br>
<br>

<h3>Download archived Minion data:</h3>
<fieldset>
<br>
<?php

$path = '/home/pi/Desktop/minion_memory';

$dir = new DirectoryIterator($path);

foreach ($dir as $fileinfo) {

  if ($fileinfo->isDir() && !$fileinfo->isDot()) {

    echo "<fieldset>
        <form method='post' action='Archive_Download.php'>
        <p1>".$fileinfo->getFilename()."</p1><br>
        <input type='submit' name='download' value='Download' />
        <input type='hidden' name='download' value='".$fileinfo->getFilename()."' />
        </form>
        <form method='post' action='/Delete_Archive.php'>
        <input type='submit' name='remove' value='Delete' />
        <input type='hidden' name='remove' value='".$fileinfo->getFilename()."' />
        </form></fieldset><br><br>";

}

}
?>
</fieldset>
<br>
<br>
<form action="/index.php" method="post">
<input type="submit" value="Return">
</form>
<br>
<br>
<br>

<?php
if(isset($_POST['downloaderr'])){

$dir = "/home/pi/Desktop/minion_memory/".$_POST['download']."/";

$zip_file = "XXX-".$_POST['download'].".zip";

// Get real path for our folder
$rootPath = realpath($dir);

// Initialize archive object
$zip = new ZipArchive();
$zip->open($zip_file, ZipArchive::CREATE | ZipArchive::OVERWRITE);

// Create recursive directory iterator
// @var SplFileInfo[] $files
$files = new RecursiveIteratorIterator(
    new RecursiveDirectoryIterator($rootPath),
    RecursiveIteratorIterator::LEAVES_ONLY
);

foreach ($files as $name => $file)
{
    // Skip directories (they would be added automatically)
    if (!$file->isDir())
    {
        // Get real and relative path for current file
        $filePath = $file->getRealPath();
        $relativePath = substr($filePath, strlen($rootPath) + 1);
        // Add current file to archive
        $zip->addFile($filePath, $relativePath);
    }
}

// Zip archive will be created only after closing object
$zip->close();

header('Content-Description: File Transfer');
header('Content-Type: application/octet-stream');
header('Content-Disposition: attachment; filename='.basename($zip_file));
header('Content-Transfer-Encoding: binary');
header('Expires: 0');
header('Cache-Control: must-revalidate');
header('Pragma: public');
header('Content-Length: ' . filesize("/var/www/html/".$zip_file));
ob_end_clean();
ob_clean();
flush();
readfile($zip_file);
}
?>

</body>
