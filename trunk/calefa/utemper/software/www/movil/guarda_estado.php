<?php
session_start();
//manejamos en sesion el nombre del usuario que se ha logeado
if (!isset($_SESSION["usuario"])){
   // header("location:login/index.php?nologin=false");
    
}
$_SESSION["usuario"];
?>

<?php
function guardaConf( $param, $valueNew )
{
	$source="utemper.conf";
	$temp = $source + ".tmp";
	$sendFile = "send/utemper.conf";

	// copy operation
	$origen =@fopen($source, 'r');
	$destino =@fopen($temp, 'w');

	if (($origen) && ($destino)){
	   
		while (($line = fgets($origen, 4096)) !== false) {
			$line = trim($line);
			if(count(split (':', $line))== 3)
			{
				 list($seg, $nombre, $valor) = split (':', $line);
				 if($nombre == $param)
				 {
					$line = (string)time().":".$param.":".$valueNew;
					echo "Update";
				 }
			}
			fwrite($destino, $line);
			fwrite($destino, "\n");
		}
		if (!feof($origen)) {
			echo "Error: unexpected fgets() fail\n";
		}
	}
	fclose($origen);
	fclose($destino);

	// delete old source file
	unlink($source);
	// rename target file to source file
	rename($temp, $source);
	copy($source, $sendFile);
}
?>

<!DOCTYPE html> 
<html> 
	<head>
	</head> 

<body> 

<?php


guardaConf("temperatura",$_GET['estado'] ); 

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