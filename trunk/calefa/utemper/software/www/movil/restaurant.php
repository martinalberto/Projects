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
	
	<link rel="stylesheet"  href="js/jquery.ui.datepicker.mobile.css" /> 
	<script src="js/jquery-1.7.1.min.js"></script>
	<script src="js/jquery.mobile-1.0.1.min.js"></script>
		<script src="js/jQuery.ui.datepicker.js"></script>
	<script src="js/jquery.ui.datepicker.mobile.js"></script>
	<script>
	function cargar_pagina(asdas,obj){
		alert(obj.style.background);
		if(obj.style.background=="#0072C6"){
			obj.style.background="#F2F2F2";
			obj.style.color="#333";
		}else{
			obj.style.background="#0072C6";
			obj.style.color="#BBB";
		}
		}
	
	</script>
</head> 
<body> 
<div id="restau" data-role="page" data-add-back-btn="true">
	
	<div data-role="header"> 
		<h1> Encendido</h1>
	</div> 


<center>
		<a href="tel:0388161072"  id="botton_fecha" data-role="button" data-icon="arrow-d"> Día : <i id="a_i_fecha"><?= date("j - n - Y")?></i>¿ Cambiar día ? </a>	
<input type="date" name="date" id="date" value="dd/mm/YYYY"  />		
<span style="    line-height: 1.8em;
    margin: 0 2.3em;
    text-align: center;"> Select Horas de encendido </span>

<?php for($i=0;$i<24;$i++){ ?> 
<table>
<tbody><tr style="cursor:pointer">
<td><?=($i<10?'0':'')?><b><?=$i?></b> h</td>
<td onclick="cargar_pagina('haz.php?h=0','td_0')" style="border: 1px;
	padding: 7px;
	border-style: solid;
	border-color: black; background-color: #F2F2F2;  " id="td_0"><?=($i<10?'0':'')?><?=$i?>:00</td>
<td onclick="cargar_pagina('haz.php?h=1',this)" style="border: 1px;
	padding: 7px;
	border-style: solid;
	border-color: black; background-color: #F2F2F2;  " id="td_1"><?=($i<10?'0':'')?><?=$i?>:15</td>
<td onclick="cargar_pagina('haz.php?h=2',this)" style="border: 1px;
	padding: 7px;
	border-style: solid;
	border-color: black; background-color: #F2F2F2;  " id="td_2"><?=($i<10?'0':'')?><?=$i?>:30</td>
<td onclick="cargar_pagina('haz.php?h=3',this)" style="border: 1px;
	padding: 7px;
	border-style: solid;
	border-color: black; background-color: #F2F2F2;  " id="td_3"><?=($i<10?'0':'')?><?=$i?>:45</td>

</tr></tbody></table>
<?php } ?>
</center>
		<a href="tel:0388161072"  data-role="button" data-icon="checkbox-on"> Salvar </a>	

	<hr/>
	




	</div>


</div><!-- /page -->
</body>

</html>
