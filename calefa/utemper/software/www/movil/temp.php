<?php
include('head.php');
?>

<?php
if (!isset($_SESSION["usuario"])){
 //   header("location:login/index.php?nologin=false");
    $_estoy_logeado='<a href="login/index.php?nologin=false"  data-transition="slidedown"  data-ajax="false">Login</a><script languaje="javascript">location.href="login/index.php?nologin=false&rand='.time().'"</script></body></html>';
}
?>

<!DOCTYPE html> 
<html > 

<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width initial-scale=1.0 maximum-scale=1.0 user-scalable=0"> 
	<title>Select Temp.</title> 
	<meta name="viewport" content="width=device-width, initial-scale=1"> 
	<link rel="stylesheet" href="css/jquery.mobile.structure-1.0.1.css" />
	<link rel="apple-touch-icon" href="images/launch_icon_57.png" />
	<link rel="apple-touch-icon" sizes="72x72" href="images/launch_icon_72.png" />
	<link rel="apple-touch-icon" sizes="114x114" href="images/launch_icon_114.png" />
		<link rel="stylesheet" href="css/jquery.mobile-1.0.1.css" />
	<link rel="stylesheet" href="css/custom.css" />

	<link rel="stylesheet" href="css/vertical_silder.css" />
	
	<script src="js/jquery-1.7.1.min.js"></script>
	<script src="js/jquery.mobile-1.0.1.min.js"></script>

	
	<style>
  #ex1_container { text-align:center }
</style>

</head> 

	
<body> 
<?php

if ( strlen($_estoy_logeado)>0){
 //   header("location:login/index.php?nologin=false");
    echo $_estoy_logeado;
	exit;
}

$dir = 'text/'.$_SESSION["equipo"];
$temperatura= (float)leeConf($dir, "temperatura");
?>

<!-- Start of first page: #one -->

<div id="choisir_ville" data-role="page" data-add-back-btn="true">
	
	<div data-role="header"> 
		<h1> Utemper.</h1>
	</div> 
	
	<div data-role="content"style="text-align:center;" >	
<h3>Temperatura:</h3>	
<form method="POST" action="guarda_temp.php" data-ajax="false" >
<table width="95%"><tr><td>
<input type="number" name="slider" id="slider-0" value="<?php echo $temperatura;?>"  onchange="(this.value=this.value.replace(/,/g, '.'));this.value=Math.round(this.value * 100)/100" step="0.01" />

			               <p align="center">
		<input type="submit" data-role="button" data-icon="checkbox-on" data-ajax="false" value="Guardar" />	
                  </p>
</td><td width="100px"><img src="images/temperature_3925.png" style="margin:10px;width:96px !important"></td></tr></table>		
	</div><!-- /content -->
</form>
</div><!-- /page one -->

</body>
</html>
