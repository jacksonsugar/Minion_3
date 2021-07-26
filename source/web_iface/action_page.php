<!DOCTYPE html>
<html>
<head>
<title>Submit 52 Config</title>

<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
        background-color:lightskyblue;
    }
</style>
</head>
<body>
<h1>Minion <?php echo $_POST["MNumber"]; ?>!</h1>
<fieldset>
MAX Depth: <?php echo $_POST["DMAX"]; ?><br>
Ignore_WIFI-days: <?php echo $_POST["IG_WIFI-days"]; ?><br>
Ignore_WIFI-hours: <?php echo $_POST["IG_WIFI-hours"]; ?><br>
</fieldset>
<fieldset>
<legend>Initial Samples:</legend>
Initial Sample Time (hours): <?php echo $_POST["IHours"]; ?><br>
Camera Sample Rate (minutes): <?php echo $_POST["ICamFS"]; ?><br>
Temperatrue and Pressure Sample Rate (Hz): <?php echo $_POST["ITPFS"]; ?><br>
Dissolved Oxygen Sample Rate (Hz): <?php echo $_POST["IOXYFS"]; ?><br>
</fieldset>

<fieldset>
<legend>Final Samples:</legend>
Final Sample Time (hours): <?php echo $_POST["FHours"]; ?><br>
Camera Sample Rate (minutes): <?php echo $_POST["FCamFS"]; ?><br>
Temperatrue and Pressure Sample Rate (Hz): <?php echo $_POST["FTPFS"]; ?><br>
Dissolved Oxygen Sample Rate (Hz): <?php echo $_POST["FOXYFS"]; ?><br>
</fieldset>

<fieldset>
<legend>Deployment Time:</legend>
Days: <?php echo $_POST["TDays"]; ?><br>
Hours: <?php echo $_POST["THours"]; ?><br>
</fieldset>

<fieldset>
<legend>Sleep Cycle:</legend>
<?php echo $_POST["SCycle"]; ?><br>
</fieldset>

<fieldset>
<legend>Data Sample:</legend>
Data Sample Time (min): <?php echo $_POST["DS_Time"]; ?><br>
Sensor Sample Rate (Hz): <?php echo $_POST["SensorFS"]; ?><br>
Oxybase Sample Rate (Hz): <?php echo $_POST["OxygenFS"]; ?><br>
</fieldset>

<fieldset>
<legend>Sampling Methods:</legend>
Image: <?php if ($_POST["Image"]=="Image"){echo "True";}else{echo "False";} ?><br>
BR 30 Bar Pressure Sensor: <?php if ($_POST["30Bar_Pres"]=="30Bar_Pres"){echo "True";}else{echo "False";} ?><br>
BR 100 Bar Pressure Sensor: <?php if ($_POST["100Bar_Pres"]=="100Bar_Pres"){echo "True";}else{echo "False";} ?><br>
BR Temperature Sensor: <?php if ($_POST["Temp"]=="Temp"){echo "True";}else{echo "False";} ?><br>
Oxybase O2 Sensor: <?php if ($_POST["OXY"]=="OXY"){echo "True";}else{echo "False";} ?><br>
ADXL345 Accelerometer: <?php if ($_POST["ACC"]=="ACC"){echo "True";}else{echo "False";} ?><br>
</fieldset>

<?php
$myfile = fopen("newconfig.txt", "w") or die("Unable to open file!");

$header = "#This is the Minion config file.\n\n";
fwrite($myfile, $header);

$Minion = "[MINION]\n"
  ."Number = ".$_POST["MNumber"]."\n\n";

fwrite($myfile, $Minion);

$Mission = "[Mission]\n"
  ."Abort = 0"."\n"
  ."Max_Depth = ".$_POST["DMAX"]."\n"
  ."Ignore_WIFI-days = ".$_POST["IG_WIFI-days"]."\n"
  ."Ignore_WIFI-hours = ".$_POST["IG_WIFI-hours"]."\n\n";
fwrite($myfile, $Mission);

$Initial_Samples = "[Initial_Samples]\n"
  ."hours = ".$_POST["IHours"]."\n"
  ."Camera_sample_rate = ".$_POST["ICamFS"]."\n"
  ."TempPres_sample_rate = ".$_POST["ITPFS"]."\n"
  ."Oxygen_sample_rate = ".$_POST["IOXYFS"]."\n\n";

fwrite($myfile, $Initial_Samples);

$Final_Samples = "[Final_Samples]\n"
  ."hours = ".$_POST["FHours"]."\n"
  ."Camera_sample_rate = ".$_POST["FCamFS"]."\n"
  ."TempPres_sample_rate = ".$_POST["FTPFS"]."\n"
  ."Oxygen_sample_rate = ".$_POST["FOXYFS"]."\n\n";

fwrite($myfile, $Final_Samples);

$Deployment_Time = "[Deployment_Time]\n"
  ."days = ".$_POST["TDays"]."\n"
  ."hours = ".$_POST["THours"]."\n\n";

fwrite($myfile, $Deployment_Time);

$Sleep_cycle = "[Sleep_cycle]\n"
  ."Minion_sleep_cycle = ".$_POST["SCycle"]."\n\n";

fwrite($myfile, $Sleep_cycle);

$Data_Sample = "[Data_Sample]\n"
  ."Minion_sample_time = ".$_POST["DS_Time"]."\n"
  ."Minion_sample_rate = ".$_POST["SensorFS"]."\n"
  ."Oxygen_sample_rate = ".$_POST["OxygenFS"]."\n\n";

fwrite($myfile, $Data_Sample);

if ($_POST["Image"]=="Image"){$bImage = "True";}else{$bImage = "False";}
if ($_POST["30Bar_Pres"]=="30Bar_Pres"){$b30bar = "True";}else{$b30bar = "False";}
if ($_POST["100Bar_Pres"]=="100Bar_Pres"){$b100bar = "True";}else{$b100bar = "False";}
if ($_POST["Temp"]=="Temp"){$btemp = "True";}else{$btemp = "False";}
if ($_POST["OXY"]=="OXY"){$boxy = "True";}else{$boxy = "False";}
if ($_POST["ACC"]=="ACC"){$bacc = "True";}else{$bacc = "False";}

$Sampling_scripts = "[Sampling_scripts]\n"
  ."Image = ".$bImage."\n"
  ."30Ba-Pres = ".$b30bar."\n"
  ."100Ba-Pres = ".$b100bar."\n"
  ."Temperature = ".$btemp."\n"
  ."Oxybase = ".$boxy."\n"
  ."ACC_100Hz = ".$bacc."\n\n";

fwrite($myfile, $Sampling_scripts);

fclose($myfile);
?>

<h2>Config 52 saved!</h2>

<form action="/form_submitted.php" method="post">
<input type="submit" value="Write Minion Config!">
</form>

<br>
<form action="/index.php" method="post">
<input type="submit" value="Return">
</form>

</body>
</html>

