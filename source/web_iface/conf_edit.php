<!DOCTYPE html>
<html>
<head>
<title>Edit 49 Config</title>
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
<h1>MINION 49 Config!</h1>

<p>This tool is designed to prepare MINIONs for deployment</p>

<form action="/action_page.php" method="post">
  <label for="DMAX">Maximum Depth (meters):</label>
  <input type="text" id="DMAX" name="DMAX" value="300"><br><br>
  <fieldset>
  <legend>Initial Samples:</legend>
  <label for="IHours">Initial Sample Time (hours):</label><br>
  <input type="text" id="IHours" name="IHours" value="2"><br>
  <label for="ICamFS">Camera Sample Rate (minutes):</label><br>
  <input type="text" id="ICamFS" name="ICamFS" value="10"><br>
  <label for="ITPFS">Temperatrue and Pressure Sample Rate (Hz):</label><br>
  <input type="text" id="ITPFS" name="ITPFS" value="5"><br>
  <label for="IOXYFS">Dissolved Oxygen Sample Rate (Hz):</label><br>
  <input type="text" id="IOXYFS" name="IOXYFS" value="1"><br>
  </fieldset>
  <fieldset>
  <legend>Final Samples:</legend>
  <label for="FHours">Final Sample Time (hours):</label><br>
  <input type="text" id="FHours" name="FHours" value="1"><br>
  <label for="FCamFS">Camera Sample Rate (minutes):</label><br>
  <input type="text" id="FCamFS" name="FCamFS" value="10"><br>
  <label for="FTPFS">Temperatrue and Pressure Sample Rate (Hz):</label><br>
  <input type="text" id="FTPFS" name="FTPFS" value="5"><br>
  <label for="FOXYFS">Dissolved Oxygen Sample Rate (Hz):</label><br>
  <input type="text" id="FOXYFS" name="FOXYFS" value="1"><br>
  </fieldset>
  <fieldset>
  <legend>Deplpyment Time:</legend>
  <label for="TDays">Days:</label><br>
  <input type="text" id="TDays" name="TDays" value="2"><br>
  <label for="THours">Hours:</label><br>
  <input type="text" id="THours" name="THours" value="12"><br>
  </fieldset>
  <fieldset>
  <legend>Sleep Cycle:</legend>
  <label for="SCycle">Sleep Cycle programmed on micro controller in hours:</label><br>
  <input type="text" id="SCycle" name="SCycle" value=".25"><br>
  </fieldset>
  <fieldset>
  <legend>Data Sample</legend>
  <label for="DS_Time">Data Sample Time (min):</label><br>
  <input type="text" id="DS_Time" name="DS_Time" value="Camera"><br>
  <label for="SensorFS">Sensor Sample Rate (Hz):</label><br>
  <input type="text" id="SensorFS" name="SensorFS" value="5"><br>
  <label for="OxygenFS">Oxybase Sample Rate (Hz):</label><br>
  <input type="text" id="OxygenFS" name="OxygenFS" value="1"><br>
  </fieldset>
  <fieldset>
  <legend>Sampling Methods</legend>
  <input checked type="checkbox" id="Image" name="Image" value="Image">
  <label for="Image"> Image</label><br>
  <input type="checkbox" id="30Bar_Pres" name="30Bar_Pres" value="30Bar_Pres">
  <label for="30Bar_Pres"> BR 30 Bar Pressure Sensor</label><br>
  <input type="checkbox" id="100Bar_Pres" name="100Bar_Pres" value="100Bar_Pres">
  <label for="100Bar_Pres"> BR 100 Bar Pressure Sensor</label><br>
  <input type="checkbox" id="Temp" name="Temp" value="Temp">
  <label for="Temp"> BR Temperature Sensor</label><br>
  <input type="checkbox" id="OXY" name="OXY" value="OXY">
  <label for="OXY"> Oxybase O2 Sensor</label><br>
  <input type="checkbox" id="ACC" name="ACC" value="ACC">
  <label for="ACC"> ADXL345 Accelerometer </label><br>
  </fieldset>
  <br>
  <fieldset>
  <legend>Confirm Minion Number:</legend>
  <input type="text" id="MNumber" name="MNumber" value="" required/>
  </fieldset>
  <br>
  <input type="submit" value="Review">
  <input type="reset">
</form>

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
