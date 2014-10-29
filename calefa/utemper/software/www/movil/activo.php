<?php
include('head.php');
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

<div id="choisir_restau" data-role="page" data-add-back-btn="true">
	
	<div data-role="header"> 
		<h1> Encedemos</h1>
	</div> 

	<div data-role="content">
	
	<div class="choice_list"> 
	 <form method="POST" action="guarda.php" data-ajax="false" >
	 	<input type="hidden" name="dia" value="<?=$_GET['dia']?>">
	<h1> Horas de encendido en el <b>día <?php
	$dias = array("Lunes","Martes","Mi&eacute;rcoles","Jueves","Viernes","S&aacute;bado","Domingo");
	echo $dias[intval($_GET['dia']-1)];
	?></b></h1><br>

<?php 

if (($gestor = fopen('text/'.$_SESSION["equipo"]."/".$_GET['dia'].".txt", "r")) !== FALSE) {
$data=fgetcsv (  $gestor ,  1000 , ';');

for($i=0;$i<24;$i++){ ?> 
<table>
<tbody><tr style="cursor:pointer">
<td><?=($i<10?'0':'')?><b><?=$i?></b> h</td>
<td onclick="cargar_pagina('haz.php?d=<?=$_GET['dia']?>&h=<?=$i?>00',this)" style="border: 1px;
	padding: 7px;
	border-style: solid;
	 color: <?=($data[$a]<1?"#333":"#BBB")?>; 
	border-color: black; background-color: <?=($data[$a]<1?"#F2F2F2":"#0072C6")?>;  " ><input type="hidden" name="<?=$i?>00" value="<?=($data[$a]<1?"0":"1")?>"><?=($i<10?'0':'')?><?=$i?>:00</td>
<td onclick="cargar_pagina('haz.php?d=<?=$_GET['dia']?>&h=<?=$i?>15',this)" style="border: 1px;
	padding: 7px;
	border-style: solid;
	color: <?=($data[$a+1]<1?"#333":"#BBB")?>; 
	border-color: black; background-color: <?=($data[$a+1]<1?"#F2F2F2":"#0072C6")?>;  "><input type="hidden" name="<?=$i?>15" value="<?=($data[$a+1]<1?"0":"1")?>"><?=($i<10?'0':'')?><?=$i?>:15</td>
<td onclick="cargar_pagina('haz.php?d=<?=$_GET['dia']?>&h=<?=$i?>30',this)"  style="border: 1px;
	padding: 7px;
	border-style: solid;
	color: <?=($data[$a+2]<1?"#333":"#BBB")?>; 
	border-color: black; background-color: <?=($data[$a+2]<1?"#F2F2F2":"#0072C6")?>;  " ><input type="hidden" name="<?=$i?>30" value="<?=($data[$a+2]<1?"0":"1")?>"><?=($i<10?'0':'')?><?=$i?>:30</td>
<td onclick="cargar_pagina('haz.php?d=<?=$_GET['dia']?>&h=<?=$i?>45',this)" style="border: 1px;
	padding: 7px;
	border-style: solid;
	color: <?=($data[$a+3]<1?"#333":"#BBB")?>; 
	border-color: black; background-color: <?=($data[$a+3]<1?"#F2F2F2":"#0072C6")?>;  " ><input type="hidden" name="<?=$i?>45" value="<?=($data[$a+3]<1?"0":"1")?>"><?=($i<10?'0':'')?><?=$i?>:45</td>

</tr></tbody></table>
<?php
$a=$a+4;
}
 }else{

for($i=0;$i<24;$i++){ ?> 
<table>
<tbody><tr style="cursor:pointer">
<td><?=($i<10?'0':'')?><b><?=$i?></b> h</td>
<td onclick="cargar_pagina('haz.php?d=<?=$_GET['dia']?>&h=<?=$i?>00',this)" style="border: 1px;
	padding: 7px;
	border-style: solid;
	border-color: black; background-color: #F2F2F2;  " ><input type="hidden" name="<?=$i?>00" value="0"><?=($i<10?'0':'')?><?=$i?>:00</td>
<td onclick="cargar_pagina('haz.php?d=<?=$_GET['dia']?>&h=<?=$i?>15',this)" style="border: 1px;
	padding: 7px;
	border-style: solid;
	border-color: black; background-color: #F2F2F2;  "><input type="hidden" name="<?=$i?>15" value="0"><?=($i<10?'0':'')?><?=$i?>:15</td>
<td onclick="cargar_pagina('haz.php?d=<?=$_GET['dia']?>&h=<?=$i?>30',this)"  style="border: 1px;
	padding: 7px;
	border-style: solid;
	border-color: black; background-color: #F2F2F2;  " ><input type="hidden" name="<?=$i?>30" value="0"><?=($i<10?'0':'')?><?=$i?>:30</td>
<td onclick="cargar_pagina('haz.php?d=<?=$_GET['dia']?>&h=<?=$i?>45',this)" style="border: 1px;
	padding: 7px;
	border-style: solid;
	border-color: black; background-color: #F2F2F2;  " ><input type="hidden" name="<?=$i?>45" value="0"><?=($i<10?'0':'')?><?=$i?>:45</td>

</tr></tbody></table>
<?php }
} ?>


		<input type="submit" data-role="button" data-icon="checkbox-on" value="Guardar" />	

	<hr/>
	


</form>

	</div>


</div><!-- /page -->

</body>

</html>
