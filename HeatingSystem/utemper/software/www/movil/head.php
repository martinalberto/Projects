<?php
#ini_set ('session.save_path', '/tmp/');
session_start();
//manejamos en sesion el nombre del usuario que se ha logeado

function guardaConf($dir, $param, $valueNew )
{
	$source=$dir."/utemper.conf";
	$temp  =$dir."/utemper.conf.tmp";
	$sendFile = $dir."/send/utemper.conf";
	$update = false;
	
	if (!file_exists($source)) {
		mkdir ($dir."/send/", 0777, True); 
		file_put_contents($source, "estado_caldera:0");
	}
	
	// copy operation
	$origen =fopen($source, 'r');
	$destino =fopen($temp, 'w');

	if (($origen) && ($destino)){
	   
		while (($line = fgets($origen, 4096)) !== false) {
			$line = trim($line);
			if(count(split (':', $line))== 3)
			{
				 list($seg, $nombre, $valor) = split (':', $line);
				 if($nombre == $param)
				 {
					$line = (string)time().":".$param.":".$valueNew;
					$update = true;
				 }
			}
			fwrite($destino, $line."\n");
		}
		if (!feof($origen)) {
			echo "guardaConf: Error: unexpected fgets() fail\n";
			fclose($origen);
			fclose($destino);
			exit();
		}
	}
	else
	{
	echo "guardaConf error, imposible leer:" .$dir."\n" ;
	echo "guardaConf error, imposible scribir:" .$temp."\n" ;
	fclose($origen);
	fclose($destino);
	exit();
	}
	
	if (!$update)
	{
		$line = (string)time().":".$param.":".$valueNew;
		fwrite($destino, $line."\n");
	}
	
	fclose($origen);
	fclose($destino);

	// delete old source file
	unlink($source);
	// rename target file to source file
	rename($temp, $source);
	copy($source, $sendFile);
	sleep(0.5);
}

function leeConf($dir, $param )
{
	$source=$dir."/utemper.conf";
	
	if (!file_exists($source)) {
		mkdir(  $dir."/send/", 0777, True); 
		file_put_contents($source, (string)time().":estado_caldera:0");
	}

	$origen =fopen($source, 'r');

	if ($origen){
		while (($line = fgets($origen, 4096)) !== false) {
			$line = trim($line);
			if(count(split (':', $line))== 3)
			{
				 list($seg, $nombre, $valor) = split (':', $line);				 
				 if($nombre == $param)
				 {
				 	fclose($origen);
					return $valor;
				 }
			}
		}
		if (!feof($origen)) {
			echo "Error: unexpected fgets() fail\n";
			fclose($origen);
			exit();
		}
	}
	else
	{
	echo "leeConf error, imposible leer:" .$dir."\n" ;
	exit();
	}
	fclose($origen);
	return "";
}


if (!isset($_SESSION["usuario"]) ){
        header("location:login/index.php?nologin=false");
        exit;
}

// ultimo acceso a la web.
if (isset($_SESSION["equipo"]) ){
        $path_ultimo_Acceso = 'text/'.$_SESSION["equipo"]."/ultimoAcceso.txt";
        $origen =fopen($path_ultimo_Acceso, 'w');
        if ($origen){
                fwrite($origen, (string)time()."\n");
        }
        else
        {
                echo "leeConf error, imposible escribir en:" .$path_ultimo_Acceso."\n" ;
                exit();
        }
        fclose($origen);
}
?>
