<!DOCTYPE html>
<html>
<head>
<title>View Data</title>
<style>
    h1 {text-align: center;}
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
        /*background-color:lightskyblue;*/
    }
</style>
</head>
<body>
<h1> MINION DATA </h1>

<fieldset>
<h2> minion_data/ </h2>

<?php

$command = escapeshellcmd('ls /home/pi/Desktop/minion_data/');
$output = shell_exec($command);
echo $output;

?>
</fieldset>
<br><br>
<fieldset>
<h3>minion_data/INI/</h3>

<?php

$command = escapeshellcmd('ls /home/pi/Desktop/minion_data/INI/');
$output = shell_exec($command);
echo $output;

?>
</fieldset>
<br><br>
<fieldset>
<h3>minion_data/FIN/</h3>

<?php

$command = escapeshellcmd('ls /home/pi/Desktop/minion_data/FIN/');
$output = shell_exec($command);
echo $output;

?>
</fieldset>
<br><br>
<fieldset>
<h2> minion_pics/ </h2>

<?php

$command = escapeshellcmd('ls /home/pi/Desktop/minion_pics/');
$output = shell_exec($command);
echo $output;

?>
</fieldset>
<br>
<br>

<h2>Download MINION Data</h2>
<form method='post' action=''>
<input type='submit' name='download' value='Download Data' />
</form>

<br>
<br>

<form action="/clear.php" method="post">
<input type="submit" value="Clear Data">
</form>


<br>
<br>

<form action="/index.php" method="post">
<input type="submit" value="Return">
</form>

</body>
</html>

<?php
if(isset($_POST['download'])){
$dir = '/home/pi/Desktop/';
$zip_file = 'MinionData.zip';

// Get real path for our folder
$rootPath = realpath($dir);

// Initialize archive object
$zip = new ZipArchive();
$zip->open($zip_file, ZipArchive::CREATE | ZipArchive::OVERWRITE);

// Create recursive directory iterator
/** @var SplFileInfo[] $files */
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
ob_clean();
flush();
readfile($zip_file);
}
?>

