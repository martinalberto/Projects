<?php

    // If the values are posted, insert them into the database.
    if (isset($_POST['name']) && isset($_POST['pass'])){
	//Open the database mydb

		$db = new SQLite3('../text/user');
//Create a basic table
//var_dump( $db->exec('CREATE TABLE IF NOT EXISTS user (id numeric PRIMARY KEY ,nombre text, contrasena text, email varchar (255))'));

        $username = $_POST['name'];
		$email = $_POST['email'];
        $password = $_POST['pass'];
		$time=time();
		$msg="";
		echo "INSERT INTO user (id, nombre, contrasena, email) VALUES ('$time','$username', '$password', '$email')";
		var_dump($db->exec( "INSERT INTO user (id, nombre, contrasena, email) VALUES ('$time','$username', '$password', '$email')"));
        if($db->exec( "INSERT INTO user (id, nombre, contrasena, email) VALUES ('$time','$username', '$password', '$email')")){
            $msg = "<script>alert('Usuario creado correctamente.');location.href='../index.php?login=true&".time()."'</script>   <a href='../index.php?login=true&".time()."' data-transition='slidedown'  data-ajax='false'>Acceso</a>";
			
        }
		exit;
    }
    ?>
<!DOCTYPE html> 
<html> 
<head> 
	<meta charset="UTF-8">
	<title>Utemper registro</title> 
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

<?php

if ( strlen($msg)>0){
	echo $msg;
	exit;
}
?>
<div id="choisir_restau" data-role="page" data-add-back-btn="true">
	
	<div data-role="header"> 
		<h1> Login</h1>
	</div> 

	<div data-role="content">
		<form id="formulario" action="registro.php?<?=time()?>" method="POST"  data-ajax="false">
<label> Usuario </label>
<input type="text" id="name" name="name">
<label> Password </label>
<input type="password" id="pass" name="pass" >
 <label> Password </label>
<input type="password" id="pass1" name="pass1" >
 <label> Co'digo Utemper </label>
<input type="text" id="email" name="email" >

<input type="submit" value="Registro" id="botonLogin">
<a class="ui-btn ui-btn-corner-all ui-shadow" data-theme="c" href="index.php" data-transition="slidedown"> Volver a login </a>
</form>	
	</div>

</div><!-- /page -->
</body>
</html>
