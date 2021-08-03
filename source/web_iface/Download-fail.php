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

$datadir = '/home/pi/Desktop/minion_data';
$imagedir = '/home/pi/Desktop/minion_pics';
$configfile = '/home/pi/Desktop/Minion_config.ini';
$zip_file = 'MinionXXX.zip';

$rootPath = realpath('/home/pi/Desktop');

// Get real path for our folder
$rootdataPath = realpath($datadir);
$rootimagePath = realpath($imagedir);

// Initialize archive object
$zip = new ZipArchive();
$zip->open($zip_file, ZipArchive::CREATE | ZipArchive::OVERWRITE);

// Create recursive directory iterator
// @var SplFileInfo[] $files
$datafiles = new RecursiveIteratorIterator(
    new RecursiveDirectoryIterator($rootdataPath),
    RecursiveIteratorIterator::LEAVES_ONLY
);

$imagefiles = new RecursiveIteratorIterator(
    new RecursiveDirectoryIterator($rootimagePath),
    RecursiveIteratorIterator::LEAVES_ONLY
);

$files = new AppendIterator();
$files->append($datafiles);
$files->append($imagefiles);

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

// Add Minion Config file
$zip->addFile($configfile, 'Minion_config.ini');

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
