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


$data_to_write=intval($_POST['slider']);

if( strlen($data_to_write)>0){
$file_path = "text/temp.txt";

if ( !file_exists("text") )
    mkdir("text");

$file_handle = fopen($file_path, 'w');

fwrite($file_handle, $data_to_write);
fclose($file_handle);
}


echo '<meta http-equiv="refresh" content="0; url=index.php?response=ok">';
?>
</body>
</html>