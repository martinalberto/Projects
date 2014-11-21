<?php
include('head.php');
?>

<?php
function readestado($string)
{
   $dir = 'text/'.$_SESSION["equipo"];
   $source=$dir."/status.txt";
           
   if (!file_exists($source)) {
		   mkdir( $dir, 0777, True); 
		   $content =(string)time(). ":last_update:". (string)time(). "\n";
		   $content .= (string)time().  ":temp:". $_GET['temp']."\n";
		   $content .= (string)time().  ":rele:". $_GET['rele']."\n";
		   file_put_contents($source, $content);
   }

   $origen =fopen($source, 'r');
   if ($origen){              
		   while (($line = fgets($origen, 4096)) !== false) {
				   $line = trim($line);

			   if(count(split (':', $line))== 3)
			   {
					list($seg, $nombre, $valor) = split (':', $line);
					if($nombre == $string)
					{
						   fclose($origen);
						   return $valor;
					}
			   }
		   }
		   if (!feof($origen)) {
			   echo "Error: unexpected fgets() fail\n";
			   fclose($origen);
			   exit();
		   }
   }
   else
   {
	   echo "leeConf error, imposible leer:" .$source."\n" ;
	   exit();
   }
   fclose($origen);
   return "0";
}
?>

<!DOCTYPE html> 
<html> 
<head> 
	<meta charset="UTF-8">
	<title>Utemper Control</title> 
	<meta name="viewport" content="width=device-width, initial-scale=1"> 
	<link rel="stylesheet" href="css/jquery.mobile.structure-1.0.1.css" />
	<link rel="apple-touch-icon" href="images/launch_icon_57.png" />
	<link rel="apple-touch-icon" sizes="72x72" href="images/launch_icon_72.png" />
	<link rel="apple-touch-icon" sizes="114x114" href="images/launch_icon_114.png" />
	<link rel="stylesheet" href="css/jquery.mobile-1.0.1.css" />
	<link rel="stylesheet" href="css/custom.css" />
	<script src="js/jquery-1.7.1.min.js"></script>
	<script src="js/jquery.mobile-1.0.1.min.js"></script>
</head> 
<body> 
<div id="choisir_ville" data-role="page" data-add-back-btn="true">
	
	<div data-role="header"> 
		<h1>Utemper Estado</h1>
	</div> 

	<div data-role="content">

	<b>Estado de tu Utemper:</b><br>
	   <hr>

		   <p> <b>Numero de serie:   <?php
			echo $_SESSION["equipo"];
			?> </b> </p>
				
		<table border="1" cellpadding="0" cellspacing="0">
		   <tr>
			  <td>Utemper:</td>
			  <td>
			  <?php
				if (time() - (readestado("last_update") + 0) < 300)
					{
					echo '<img SRC="img/estado_on.png"><br> Encendido ';
					}
				else
					{
					echo '<img SRC="img/estado_off.png"><br> Error de comunicacion. ';
					date_default_timezone_set("Europe/Madrid"); 
					echo '<p> ultima comunicacion:'.date("Y-m-d H:i:s",readestado("last_update")).' </p>';
					}
			  ?>
			  </td>
		   </tr>
			 <tr>
				 <td>Caldera:</td>
			     <td>  <?php
				if (readestado("rele")==1)
					{
					echo '<img SRC="img/estado_caldera_on.png"><br> Encendida ';
					}
				else
					{
					echo '<img SRC="img/estado_caldera_off.png"><br>  Apagada. ';
					}
				?> </td>
			  </tr>
		</table>
		<hr>
		<table border="0" cellpadding="0" cellspacing="0">
		   <tr>
			  <td>Temperatura dentro:</td>
			  <td>
			   <?php
				echo readestado("temp");
				?> &deg;C
			  </td>
		   </tr>
		   <tr>
			  <td>Temperatura fuera:</td>
			  <td>
			   <?php
				echo readestado("temp");
				?> &deg;C
			  </td>
		   </tr>
		</table>
		<br>

	
	</div>

</div><!-- /page -->
</body>
</html>