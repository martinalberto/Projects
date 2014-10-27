<?php
include('head.php');
?>

<?php
session_start();
//manejamos en sesion el nombre del usuario que se ha logeado
if (!isset($_SESSION["usuario"])){
   // header("location:login/index.php?nologin=false");
    
}
$_SESSION["usuario"];
$_SESSION["equipo"]= "137291051180603";
?>
<!DOCTYPE html> 
<html> 
	<head>
	</head> 

<body> 
<?php
if (!is_numeric($_POST['slider']))
{
	echo "Error temperatura no es un numero. \n";
	exit();
}

$dir = 'text/'.$_SESSION["equipo"];
guardaConf($dir, "temperatura",$_POST['slider']);




echo '<meta http-equiv="refresh" content="0; url=index.php?response=ok">';
?>
</body>
</html>