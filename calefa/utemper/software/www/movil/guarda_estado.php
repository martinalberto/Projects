<?php
session_start();
//manejamos en sesion el nombre del usuario que se ha logeado
if (!isset($_SESSION["usuario"])){
   // header("location:login/index.php?nologin=false");
    
}
$_SESSION["usuario"];
?>
<!DOCTYPE html> 
<html> 
	<head>
	</head> 

<body> 
<?php

if ( !file_exists("text") )
    mkdir("text");
$file = fopen("text/estado.txt", "r") or exit("Unable to open file!");
$escribe="";
$data_to_write=intval($_GET['estado']);
while(!feof($file)){
$linea= fgets($file);
	if((stripos($linea,"estado")!== false )&&($data_to_write>0) && ($data_to_write<3)){
		$escribe.="estado:".$data_to_write;
	}else
		$escribe.=$linea;
}
fclose($file);
file_put_contents("text/estado.txt", $escribe);




echo '<meta http-equiv="refresh" content="0; url=index.php?response=ok&nocache='.time().'">';
?>
</body>
</html>