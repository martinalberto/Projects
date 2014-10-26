<?php
session_start();
//manejamos en sesion el nombre del usuario que se ha logeado
if (!isset($_SESSION["usuario"])){
 //   header("location:login/index.php?nologin=false");
    
}
if ( !file_exists("text") )
    mkdir("text");
if ( !file_exists("text/estado.txt") )
	file_put_contents("text/estado.txt", "sdads\nestado:0");
//busca en fichero
$file = fopen("text/estado.txt", "r") or exit("Unable to open file!");
$encendido=0;
while(!feof($file)){
$linea= fgets($file);

	if(stripos($linea,"estado")!== false ){
		$array_encendido=preg_split('/[:]/',$linea);
		$encendido=intval($array_encendido[1]);

	}

}

fclose($file);
sleep(1);
?>
<!DOCTYPE html> 
<html> 
	<head>
  <meta charset="UTF-8">	
	<title>Utemper Control</title> 
	
	<meta name="viewport" content="width=device-width, initial-scale=1"> 
	<link rel="stylesheet" href="css/jquery.mobile.structure-1.0.1.css" />
	<link rel="stylesheet" href="css/font-awesome.min.css" />
	<link rel="apple-touch-icon" href="images/launch_icon_57.png" />
	<link rel="apple-touch-icon" sizes="72x72" href="images/launch_icon_72.png" />
	<link rel="apple-touch-icon" sizes="114x114" href="images/launch_icon_114.png" />
	<link rel="stylesheet" href="css/jquery.mobile-1.0.1.css" />
	<link rel="stylesheet" href="css/custom.css" />
	<script src="js/jquery-1.7.1.min.js"></script>
	<script src="js/jquery.mobile-1.0.1.min.js"></script>
</head> 

<body> 
<div data-role="page" id="home" data-theme="c">

	<div data-role="content">
	
	<div id="branding">
		<h1>Utemper Control </h1>
	</div>
	<form method="POST" data-ajax="false" action="index.php?menu=1&nocache=<?php echo time();?>" >
	<div class="choice_list"> 
	<!-- <h1> What would you'd like to eat? </h1> -->
	<?php 
	if ((intval($_GET['menu'])!=1) || (strlen($_SESSION["usuario"])<1)){
	if($_GET['response']=='ok'){?>
	<br>
	<div data-theme="a" data-form="ui-body-a" class="ui-body ui-body-a ui-corner-all">
			<p>Los cambios se han guardado correctamente. Puede verificarlos accediendo donde se han editado</p>

		</div>
		<?php }
		if (strlen($_SESSION["usuario"])<1){ ?>
			<a data-role="button"  href="login/index.php?nocache=<?=time();?>" > Ir a login</a>	
			
		<?php
		}else{
		?>
			<input type="submit" data-role="button" data-icon="checkbox-on" value="Ir a página principal" />	
	<?php } ?>
	</form >
	
		
	
	</div>
	</div>



</div><!-- /page -->
</body>
</html>

<?php 
}else{
if(strlen($_SESSION["usuario"])<1){
echo '<a href="login/index.php?nologin=false"  data-transition="slidedown"  data-ajax="false">Login</a><script languaje="javascript">location.href="login/index.php?nologin=false&rand='.time().'"</script></body></html>';
exit;
}
?>
	<ul data-role="listview" data-inset="true" >
<li><i class="fa fa-home"></i> <h3> Caldera: </h3>
		<select  data-native-menu="false" data-theme="c"  onchange='window.location.href="guarda_estado.php?estado="+this.selectedIndex+"&nocache=<?=time()?>"' >
		   <option value="on" class="on" data-transition="slidedown"  data-ajax="false" <?=($encendido==0?"selected":"")?> > Encendido </option>
		   <option value="off" class="off" data-transition="slidedown"  data-ajax="false" <?=($encendido==1?"selected":"")?> >Apagado </option>
		   <option value="prog" class="prog" data-transition="slidedown"  data-ajax="false" <?=($encendido==2?"selected":"")?> >Programado </option>
		</select>	
	</form>
	</li>
	
	<li><a href="temp.php"  data-transition="slidedown"  data-ajax="false"><i><IMG SRC="img/icon_temp.png"> </i>  <h3> temperatura. </h3></a></li>
	<li><a href="dias.php?nocache=<?=time()?>"  data-transition="slidedown"><i class="fa fa-calendar-o"></i><h3> Programacion</h3></a></li>
	<li><a href="config1.php"  data-transition="slidedown"><i class="fa fa-cogs fa-fw"></i> <h3> Configuracion.</h3></a></li>	
	</ul>	
	
	</div>
	</div>
	
	
	<script type="text/javascript">
	<!-- para el estado de la calefa  -->
	
	$( '#restau' ).live( 'pageinit',function(event){
		var SelectedOptionClass = $('option:selected').attr('class');
		$('div.ui-select').addClass(SelectedOptionClass);
		
		$('#note_utilisateur').live('change', function(){	 
			$('div.ui-select').removeClass(SelectedOptionClass);
			
			SelectedOptionClass = $('option:selected').attr('class');
			$('div.ui-select').addClass(SelectedOptionClass);		
			
		 });
		
	  
	});

	</script>


</div><!-- /page -->
</body>
</html>
<?php
}
?>