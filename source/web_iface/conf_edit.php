<!DOCTYPE html>
<html>
<head>
<title>Edit XXX Config</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    	/*background-color:lightskyblue;*/
    }
</style>
</head>
<body>
<h1>MINION XXX Config!</h1>

<p>This tool is designed to prepare MINIONs for deployment</p>

<?php

$cfg_file = parse_ini_file("/home/pi/Desktop/Minion_config.ini", true);

if ($cfg_file['Sampling_scripts']['Image'] == 1) { $Image = "checked";} else { $Image = "";}
if ($cfg_file['Sampling_scripts']['30Ba-Pres'] == 1) { $BA30 = "checked";} else { $BA30 = "";}
if ($cfg_file['Sampling_scripts']['100Ba-Pres'] == 1) { $BA100 = "checked";} else { $BA100 = "";}
if ($cfg_file['Sampling_scripts']['Temperature'] == 1) { $Temp = "checked";} else { $Temp = "";}
if ($cfg_file['Sampling_scripts']['Oxybase'] == 1) { $OXY = "checked";} else { $OXY = "";}
if ($cfg_file['Sampling_scripts']['ACC_100Hz'] == 1) { $ACC = "checked";} else { $ACC = "";}

echo '<form action="/action_page.php" method="post">
  <label for="DMAX">Maximum Depth (meters):</label>
  <input type="text" id="DMAX" name="DMAX" value="'.$cfg_file['Mission']['Max_Depth'].'"><br><br>
  <fieldset>
  <legend>Initial Samples:</legend>
  <label for="IHours">Initial Sample Time (hours):</label><br>
  <input type="text" id="IHours" name="IHours" value="'.$cfg_file['Initial_Samples']['hours'].'"><br>
  <label for="ICamFS">Camera Sample Rate (minutes):</label><br>
  <input type="text" id="ICamFS" name="ICamFS" value="'.$cfg_file['Initial_Samples']['Camera_sample_rate'].'"><br>
  <label for="ITPFS">Temperatrue and Pressure Sample Rate (Hz):</label><br>
  <input type="text" id="ITPFS" name="ITPFS" value="'.$cfg_file['Initial_Samples']['TempPres_sample_rate'].'"><br>
  <label for="IOXYFS">Dissolved Oxygen Sample Rate (Hz):</label><br>
  <input type="text" id="IOXYFS" name="IOXYFS" value="'.$cfg_file['Initial_Samples']['Oxygen_sample_rate'].'"><br>
  </fieldset>
  <fieldset>
  <legend>Final Samples:</legend>
  <label for="FHours">Final Sample Time (hours):</label><br>
  <input type="text" id="FHours" name="FHours" value="'.$cfg_file['Final_Samples']['hours'].'"><br>
  <label for="FCamFS">Camera Sample Rate (minutes):</label><br>
  <input type="text" id="FCamFS" name="FCamFS" value="'.$cfg_file['Final_Samples']['Camera_sample_rate'].'"><br>
  <label for="FTPFS">Temperatrue and Pressure Sample Rate (Hz):</label><br>
  <input type="text" id="FTPFS" name="FTPFS" value="'.$cfg_file['Final_Samples']['TempPres_sample_rate'].'"><br>
  <label for="FOXYFS">Dissolved Oxygen Sample Rate (Hz):</label><br>
  <input type="text" id="FOXYFS" name="FOXYFS" value="'.$cfg_file['Final_Samples']['Oxygen_sample_rate'].'"><br>
  </fieldset>
  <fieldset>
  <legend>Deplpyment Time:</legend>
  <label for="TDays">Days:</label><br>
  <input type="text" id="TDays" name="TDays" value="'.$cfg_file['Deployment_Time']['days'].'"><br>
  <label for="THours">Hours:</label><br>
  <input type="text" id="THours" name="THours" value="'.$cfg_file['Deployment_Time']['hours'].'"><br>
  </fieldset>
  <fieldset>
  <legend>Sleep Cycle:</legend>
  <label for="SCycle">Sleep Cycle programmed on micro controller in hours:</label><br>
  <input type="text" id="SCycle" name="SCycle" value="'.$cfg_file['Sleep_cycle']['Minion_sleep_cycle'].'"><br>
  </fieldset>
  <fieldset>
  <legend>Data Sample</legend>
  <label for="DS_Time">Data Sample Time (min):</label><br>
  <input type="text" id="DS_Time" name="DS_Time" value="'.$cfg_file['Data_Sample']['Minion_sample_time'].'"><br>
  <label for="SensorFS">Sensor Sample Rate (Hz):</label><br>
  <input type="text" id="SensorFS" name="SensorFS" value="'.$cfg_file['Data_Sample']['Minion_sample_rate'].'"><br>
  <label for="OxygenFS">Oxybase Sample Rate (Hz):</label><br>
  <input type="text" id="OxygenFS" name="OxygenFS" value="'.$cfg_file['Data_Sample']['Oxygen_sample_rate'].'"><br>
  </fieldset>
  <fieldset>
  <legend>Sampling Methods</legend>
  <input '.$Image.' type="checkbox" id="Image" name="Image" value="Image">
  <label for="Image"> Image</label><br>
  <input '.$BA30.' type="checkbox" id="30Bar_Pres" name="30Bar_Pres" value="30Bar_Pres">
  <label for="30Bar_Pres"> BR 30 Bar Pressure Sensor</label><br>
  <input '.$BA100.' type="checkbox" id="100Bar_Pres" name="100Bar_Pres" value="100Bar_Pres">
  <label for="100Bar_Pres"> BR 100 Bar Pressure Sensor</label><br>
  <input '.$Temp.' type="checkbox" id="Temp" name="Temp" value="Temp">
  <label for="Temp"> BR Temperature Sensor</label><br>
  <input '.$OXY.' type="checkbox" id="OXY" name="OXY" value="OXY">
  <label for="OXY"> Oxybase O2 Sensor</label><br>
  <input '.$ACC.' type="checkbox" id="ACC" name="ACC" value="ACC">
  <label for="ACC"> ADXL345 Accelerometer </label><br>
  </fieldset>
  <fieldset>
  <legend>Ignore WIFI Signal:</legend>
  <br>
  <label for="IG_WIFI-days">Days:</label>
  <input type="text" id="IG_WIFI-days" name="IG_WIFI-days" value="'.$cfg_file['Mission']['Ignore_WIFI-days'].'"><br><br>
  <label for="IG_WIFI-hours">Hours:</label>
  <input type="text" id="IG_WIFI-hours" name="IG_WIFI-hours" value="'.$cfg_file['Mission']['Ignore_WIFI-hours'].'"><br>
  </fieldset>
  </fieldset>
  <br>
  <fieldset>
  <legend>Confirm Minion Number:</legend>
  <input type="text" id="MNumber" name="MNumber" value="'.$cfg_file['MINION']['Number'].'"  required/>
  </fieldset>
  <br>
  <input type="submit" value="Review">
  <input type="reset">
</form>';

?>

<br>
<form action="/index.php" method="post">
<input type="submit" value="Return">
</form>

</body>
</html>

<br>
<br>
<br>
<br>
<br>
<br>
