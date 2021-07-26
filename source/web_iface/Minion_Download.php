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

<h1>Download Minion XXX Data</h1>

<br>
<br>

<h2>Please be patient as files are zipped together</h2>
<form method='post' action=''>
<input type='submit' name='download' value='Download Data' />
</form>
<br>
<br>
<form action="/View_Data.php" method="post">
<input type="submit" value="Return">
</form>
<br>
<br>
<br>

<?php
if(isset($_POST['download'])){

echo "This is a test";

flush();


$dir = '/home/pi/Desktop/';
$zip_file = 'Minion52.zip';

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
header('Content-Length: ' . filesize($zip_file));

readfile($zip_file);
}
?>

</body>
