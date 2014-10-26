<?php
session_start();
$valido=true;
      if(isset($_POST['name'])){
         /*Entra solo si se presiona el boton entrar*/
        
		$db = new SQLite3('../text/user');
var_dump($db);
		$nombre=$_POST['name'];
         $contrasena=$_POST['pass'];
		echo "SELECT id FROM user where nombre='$nombre' AND contrasena='$contrasena'";
		
         //$consulta="SELECT id, nombre,contrasena FROM user where nombre='$nombre' AND contrasena='$contrasena'";
		$data= $db->querySingle("SELECT id, nombre,contrasena FROM user where nombre='$nombre' AND contrasena='$contrasena' limit 1");
		
		if (intval($data)<1){
             $valido=false;
         }else{
			
             $valido=true;
             //guardamos en sesion el nombre del usuario 
             $_SESSION["usuario"]=$data;
             header("location:../index.php?login=true&".time());
         }               
      }
?>
<!DOCTYPE html> 
<html> 
<head> 
	<meta charset="UTF-8">
	<title>Restaurant Picker</title> 
	<meta name="viewport" content="width=device-width, initial-scale=1"> 
	<link rel="stylesheet" href="jquery.mobile.structure-1.0.1.css" />
	<link rel="apple-touch-icon" href="../images/launch_icon_57.png" />
	<link rel="apple-touch-icon" sizes="72x72" href="../images/launch_icon_72.png" />
	<link rel="apple-touch-icon" sizes="114x114" href="../images/launch_icon_114.png" />
	<link rel="stylesheet" href="../jquery.mobile-1.0.1.css" />
	<link rel="stylesheet" href="../custom.css" />
	<script src="../js/jquery-1.7.1.min.js"></script>
	<script src="../js/jquery.mobile-1.0.1.min.js"></script>
</head> 
<body> 
<div id="choisir_restau" data-role="page" data-add-back-btn="true">
	
	<div data-role="header"> 
		<h1> Login</h1>
	</div> 

	<div data-role="content">
		<form id="formulario" action="index.php?<?=time()?>"  method="POST" data-ajax="false">
<label> Usuario </label>
<input type="text" id="name" name="name">
<label> Password </label>
<input type="password" id="pass" name="pass" >
 
<input type="submit" value="Login" id="botonLogin">
<a class="ui-btn ui-btn-corner-all ui-shadow" data-theme="c" href="registro.php" data-transition="slidedown"> Registro </a>
</form>	
	</div>

</div><!-- /page -->
</body>
</html>
