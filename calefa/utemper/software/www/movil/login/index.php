<?php
session_start();



function encrypt_($string) {
$key="miauei";
   $result = '';
   for($i=0; $i<strlen($string); $i++) {
      $char = substr($string, $i, 1);
      $keychar = substr($key, ($i % strlen($key))-1, 1);
      $char = chr(ord($char)+ord($keychar));
      $result.=$char;
   }
   return base64_encode($result);
}


function decrypt_($string) {
$key="miauei";
   $result = '';
   $string = base64_decode($string);
   for($i=0; $i<strlen($string); $i++) {
      $char = substr($string, $i, 1);
      $keychar = substr($key, ($i % strlen($key))-1, 1);
      $char = chr(ord($char)-ord($keychar));
      $result.=$char;
   }
   return $result;
}



$valido=true;


	 if((!isset($_GET['borra_session']))&&(isset($_COOKIE['id_usuario_dw']))){
         /*Entra solo si se presiona el boton entrar*/
        
		$db = new SQLite3('../text/user');
		$nombre=$_COOKIE['id_usuario_dw'];
         $contrasena=decrypt_($_COOKIE['marca_aleatoria_usuario_dw']);
		
         //$consulta="SELECT id, nombre,contrasena FROM user where nombre='$nombre' AND contrasena='$contrasena'";
		$data= $db->querySingle("SELECT email FROM user where nombre='$nombre' AND contrasena='$contrasena' limit 1");
		
		if (intval($data)<1){
             $valido=false;
         }else{
             $valido=true;
             //guardamos en sesion el nombre del usuario 
			   if ($_POST["guardar_clave"]=="1"){
				  //3) ahora meto una cookie en el ordenador del usuario con el identificador del usuario y la cookie aleatoria
				  setcookie("id_usuario_dw", $nombre , time()+(60*60*24*365));
				  setcookie("marca_aleatoria_usuario_dw", encrypt_($contrasena), time()+(60*60*24*365));
			   }
             $_SESSION["usuario"]=$data;
			 $_SESSION["equipo"]= $data;
             header("location:../index.php?login=true&".time());
         }               
      }


      if(strlen($_POST['name'])>0){
         /*Entra solo si se presiona el boton entrar*/
        
		$db = new SQLite3('../text/user');
		$nombre=$_POST['name'];
         $contrasena=$_POST['pass'];
		
         //$consulta="SELECT id, nombre,contrasena FROM user where nombre='$nombre' AND contrasena='$contrasena'";
		$data= $db->querySingle("SELECT email FROM user where nombre='$nombre' AND contrasena='$contrasena' limit 1");
		
		if (intval($data)<1){
             $valido=false;
         }else{
             $valido=true;
             //guardamos en sesion el nombre del usuario 
			   if ($_POST["guardar_clave"]=="1"){
				  //3) ahora meto una cookie en el ordenador del usuario con el identificador del usuario y la cookie aleatoria
				  setcookie("id_usuario_dw", $nombre , time()+(60*60*24*365));
				  setcookie("marca_aleatoria_usuario_dw", encrypt_($contrasena), time()+(60*60*24*365));
			   }
             $_SESSION["usuario"]=$data;
			 $_SESSION["equipo"]= $data;
             header("location:../index.php?login=true&".time());
         }               
      }
?>
<!DOCTYPE html> 
<html> 
<head> 
	<meta charset="UTF-8">
	<title>Utemper Login</title> 
	<meta name="viewport" content="width=device-width, initial-scale=1"> 
	<link rel="stylesheet" href="../css/jquery.mobile.structure-1.0.1.css" />
	<link rel="apple-touch-icon" href="../images/launch_icon_57.png" />
	<link rel="apple-touch-icon" sizes="72x72" href="../images/launch_icon_72.png" />
	<link rel="apple-touch-icon" sizes="114x114" href="../images/launch_icon_114.png" />
	<link rel="stylesheet" href="../css/jquery.mobile-1.0.1.css" />
	<link rel="stylesheet" href="../css/custom.css" />
	<script src="../js/jquery-1.7.1.min.js"></script>
	<script src="../js/jquery.mobile-1.0.1.min.js"></script>
</head> 
<body> 
<div id="choisir_restau" data-role="page" data-add-back-btn="true">
	
		<div data-role="header"> 
		<h1> Login</h1>
	</div> 

	<div data-role="content">
	
	<?php
	 if(isset($_GET['borra_session'])){
	 if (isset($_SERVER['HTTP_COOKIE'])) {
		$cookies = explode(';', $_SERVER['HTTP_COOKIE']);
		foreach($cookies as $cookie) {
			$parts = explode('=', $cookie);
			$name = trim($parts[0]);
			setcookie($name, '', time()-1000);
			setcookie($name, '', time()-1000, '/');
		}
	}
	?>
		<div data-theme="a" data-form="ui-body-a" class="ui-body ui-body-a ui-corner-all"><p><i>
		<IMG SRC="../img/icon_info.png"> </i>
			Borradas todas las sesiones</p>
		</div>
		<?php
		}
		?>
	

		<form id="formulario" action="index.php?<?=time()?>"  method="POST" data-ajax="false">
<label> Usuario </label>
<input type="text" id="name" name="name">
<label> Password </label>
<input type="password" id="pass" name="pass" >

		<input type="checkbox" checked name="guardar_clave" id="guardar_clave" value="1" />
		<label for="guardar_clave">Guardar sesión </label>
<br>
<input type="submit" value="Login" id="botonLogin" />
<?php /* <table width="100%"><tr><td><input type="button" class="ui-btn ui-btn-corner-all ui-shadow" onClick="location.href='index.php?use_session=<?=time()?>'"  value="Usar sesión" />
 <td><input type="button"  class="ui-btn ui-btn-corner-all ui-shadow" data-theme="c" onClick="location.href='index.php?borra_session=<?=time()?>'"  value="Borrar sesión" /></td>
 </table>
 */ ?>
<input type="button" class="ui-btn ui-btn-corner-all ui-shadow" data-theme="c" onClick="location.href='registro.php?<?=time()?>'" data-transition="slidedown" value="Registro" />
</form>	
	</div>

</div><!-- /page -->
</body>
</html>
