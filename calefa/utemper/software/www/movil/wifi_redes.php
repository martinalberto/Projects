<?php
session_start();
//manejamos en sesion el nombre del usuario que se ha logeado
if (!isset($_SESSION["usuario"])){
  //  header("location:login/index.php?nologin=false");
    
}
$_SESSION["usuario"];
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
		<h1> Utemper Control</h1>
	</div> 

	<div data-role="content">
	
	<div class="choice_list"> 
	<h1> Selecciona de la red Wifi para conctarse. </h1>
	
	<ul data-role="listview" data-inset="true" data-filter="true"  >
		
<?php
$handle = @fopen("/tmp/redes_wifi.txt", "r");
if ($handle) {
    while (($buffer = fgets($handle, 4096)) !== false) {
	$buffer = trim($buffer);
        list($senal, $ssid, $encriptado) = split (';', $buffer);
        $text = '	<li><a href="wifi_selecion.php?red=' . $ssid ;
	$text .= '&cript=' . $encriptado;
        $text .= '"  data-transition="slidedown"> ' . $ssid ;
        if ($encriptado =="1") { 
			$text .= '<span class="ui-li-count" >Cript</span>';
			}
        $text .='</a> </li> 
';
	if ($senal!="0"){
		echo $text;
	}
}
    if (!feof($handle)) {
        echo "Error: unexpected fgets() fail\n";
    }
    fclose($handle);
}
else
{
	echo "Error: El Sistema no encontro redes WIFI.\n";
}
?>
	</ul>
	</div>
	
	</div>

</div><!-- /page -->
</body>
</html>
