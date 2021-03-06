<!DOCTYPE HTML>
<!-- Website template by freewebsitetemplates.com -->
<html>
<head>
	<meta charset="UTF-8">
	<title>Sensor measurement</title>
	<link rel="stylesheet" href="css/style.css" type="text/css">
</head>
<body>

	<?php
		// define variables and set to empty values
		$run = 0;
		$time = 0;
		$data_array = array();
		$number_of_sensor = 0;

		if ($_SERVER["REQUEST_METHOD"] == "POST") {
			if (isset($_POST['start'])) {
				
				$time = intval(test_input($_POST["time"]));
				$cmd = 'echo '.$time.' > data/test';
				system($cmd);
				// echo 'start time is '.$time;
				$run = 1;

			} elseif (isset($_POST['stop'])) {
				$cmd = 'echo stop > data/test';
				system($cmd);
				sleep(2);
				// echo "stop";
				$run = 0;
			}

		}
		function test_input($data) {
			$data = trim($data);
			$data = stripslashes($data);
			$data = htmlspecialchars($data);
			return $data;
		}
	?>



	<div id="header">
		<div>
			<div class="logo">
				<a href="index.php">Zero Type</a>
			</div>
			<ul id="navigation">
				<li class="active">
					<a href="index.php">Home</a>
				</li>
				<li class="active">
					<a href="about.html">About</a>
				</li>
			</ul>
		
				

		</div>
	</div>
	<div id="contents">
		<div id="tagline" class="clearfix">
			<h1>Result</h1>
			<div>
			
				<?php
					function read_number_of_sensor() {
						$myfile = fopen("data/number_of_sensor", "r") or die("Unable to open file!");
						$number_of_sensor = intval(fread($myfile,filesize("data/number_of_sensor")));
						fclose($myfile);
						return $number_of_sensor;
					}

					function read_data_from_file($number_of_sensor){
						global $data_array;

						echo "Number of sensors is $number_of_sensor<br>";
						echo "<br>";

						echo "<table border=\"1\" style=\"width:100%\">";
						echo "<tr>";
						echo "<td><strong>t(ms)</strong></td>";
						for ($i = 1; $i <= $number_of_sensor; $i++){
							echo "<td><strong>Sensor[$i]</strong></td>";
						}
						echo "</tr>";

						$xml=simplexml_load_file("data/data.xml");
						if ($xml ===FALSE)
						{
							echo "Could not load data";
						}
						else
						{
							foreach($xml->children() as $items)
							{
								echo "<tr>";
								$temp_arr = array($items->t);

								echo "<td>$items->t</td>";
								$s = $items->sensor;
								for ($i = 0; $i < $number_of_sensor; $i++){
									$x = $s[$i];
									array_push($temp_arr, $x);
									echo "<td>$x</td>";
								}
								echo "</tr>";
								array_push($data_array, $temp_arr);
								// echo 'Size of = '.sizeof($data_array).' <br>';
								// echo 'Size of = '.sizeof($temp_arr).' <br>';
							} 
						}
						echo "</table>";
					}

					# get number of sensors
					$number_of_sensor = read_number_of_sensor();
					read_data_from_file($number_of_sensor);
				?>
				  
			</div>

			<div>
				<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>"> 
					Interval time: <input type="number" name="time"> milisecond <br>
					<input type="submit" name="start" value="Start">
					<input type="submit" name="stop" value="Stop"> 
				</form>
				<form>
					<label id="time_cout">0</label> Samples <br>
					<script>
						var sample = 0;
						
						function myTimer() {
						    sample  = sample + 1;
						    document.getElementById("time_cout").innerHTML = "" + sample;
						}
						
						<?php
							if ($run == 1)
							{
								echo 'var myVar=setInterval(function () {myTimer()}, '.$time.');';
							}
						?>
						
					</script> 
				</form>


				<?php
					function draw_plot($id)
					{
						require_once 'phplot/phplot.php';
						global $data_array; 
						global $number_of_sensor;
						$plot = new PHPlot();
						echo '<br><strong> Plot for sensor '.$id.'</strong><br>';

						$example_data = array();

						foreach ($data_array as $items) {
							// $test = $test + 1.5;
							$test = floatval($items[$id])*100;
							array_push($example_data, array($items[0] / 1000.0, $test));
						}
						$plot->SetTitle('Sensor '.$id);
						$plot->SetDataValues($example_data);
						$plot->SetXTickLabelPos('plotdown');
						$plot->SetXTickPos('none');
						$plot->SetPrintImage(False);
						$x = $plot->DrawGraph();
						echo "<img src=\"" . $plot->EncodeImage() . "\">\n";
					}
					for ($i = 1; $i < $number_of_sensor; $i++)
					{
						draw_plot($i);
					}
				?>

			</div>

		</div>
	</div>
	<div id="footer">
		<div class="clearfix">
			<div id="connect">
				<a href="http://freewebsitetemplates.com/go/facebook/" target="_blank" class="facebook"></a><a href="http://freewebsitetemplates.com/go/googleplus/" target="_blank" class="googleplus"></a><a href="http://freewebsitetemplates.com/go/twitter/" target="_blank" class="twitter"></a><a href="http://www.freewebsitetemplates.com/misc/contact/" target="_blank" class="tumbler"></a>
			</div>
			<p>
				© 2015 Designed by Phuc Le (tanphuc.le@gmail.com)
			</p>
		</div>
	</div>
</body>
</html>
