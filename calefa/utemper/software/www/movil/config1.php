<?php
session_start();
//manejamos en sesion el nombre del usuario que se ha logeado
if (!isset($_SESSION["usuario"])){
   // header("location:login/index.php?nologin=false");
    
}
$_SESSION["usuario"];
?>
<!DOCTYPE html> 
<html> 
<head> 
	<meta charset="UTF-8">
	<title>Restaurant Picker</title> 
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
		<h1>Utemper Configuración.</h1>
	</div> 

	<div data-role="content">
	<h1>Men&uacute;	de Configuraci&oacute;n.</h1>
	<div class="choice_list"> 
	<ul data-role="listview" data-inset="true" >
			<li><a href="wifi_redes.php"  data-transition="slidedown"><i><IMG SRC="img/icon_wifi.png"> </i> <br> <h3> Configurar Wifi. </h3></a></li>
			<li><a href="estado.php"  data-transition="slidedown"><i><IMG SRC="img/icon_status.png"> </i> <br> <h3> Estado del sistema. </h3></a></li>
	</ul>	
	</div>
	
	</div>
	</div><!-- /page -->

</body>
</html>
