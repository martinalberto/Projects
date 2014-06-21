<!DOCTYPE html> 
<html> 
<head> 
	 <meta charset="UTF-8">
	<title>Restaurant Picker</title> 
	<meta name="viewport" content="width=device-width, initial-scale=1"> 
	<link rel="stylesheet" href="jquery.mobile.structure-1.0.1.css" />
	<link rel="apple-touch-icon" href="images/launch_icon_57.png" />
	<link rel="apple-touch-icon" sizes="72x72" href="images/launch_icon_72.png" />
	<link rel="apple-touch-icon" sizes="114x114" href="images/launch_icon_114.png" />
	<link rel="stylesheet" href="jquery.mobile-1.0.1.css" />
	<link rel="stylesheet" href="custom.css" />
	<script src="js/jquery-1.7.1.min.js"></script>
	<script src="js/jquery.mobile-1.0.1.min.js"></script>
</head> 
<body> 
<div id="choisir_ville" data-role="page" data-add-back-btn="true">
	
	<div data-role="header"> 
		<h1> Selección del día de la semana a programar</h1>
	</div> 

	<div data-role="content">
	
	<div class="choice_list"> 
	<h1> Selección del día de la semana a programar </h1>
	
	<ul data-role="listview" data-inset="true" data-filter="true"  >
	<li><a href="activo.php?dia=1"  data-transition="slidedown"> Lunes <span class="ui-li-count" > L </span></a> </li>
	<li><a href="activo.php?dia=2"  data-transition="slidedown"> Martes <span class="ui-li-count" > M </span></a> </li>
	<li><a href="activo.php?dia=3" data-transition="slidedown">  Miércoles <span class="ui-li-count" > X </span></a> </li>
	<li><a href="activo.php?dia=4" data-transition="slidedown"> Jueves <span class="ui-li-count" > J </span></a> </li>
	<li><a href="activo.php?dia=5" data-transition="slidedown">Viernes <span class="ui-li-count" > V</span></a> </li>	
	<li><a href="activo.php?dia=6" data-transition="slidedown"> Sábado <span class="ui-li-count" > S </span></a> </li>
	<li><a href="activo.php?dia=7" data-transition="slidedown"> Domingo <span class="ui-li-count" > D </span></a> </li>	
	</ul>
	</div>
	
	</div>

</div><!-- /page -->
</body>
</html>
