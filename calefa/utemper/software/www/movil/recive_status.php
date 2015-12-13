<?php
error_reporting(-1);

function is_dir_empty($dir) {
  if (!is_readable($dir)) return NULL; 
  return (count(scandir($dir)) == 2);
}

function get_client_ip() {
    $ipaddress = '';
    if (getenv('HTTP_CLIENT_IP'))
        $ipaddress = getenv('HTTP_CLIENT_IP');
    else if(getenv('HTTP_X_FORWARDED_FOR'))
        $ipaddress = getenv('HTTP_X_FORWARDED_FOR');
    else if(getenv('HTTP_X_FORWARDED'))
        $ipaddress = getenv('HTTP_X_FORWARDED');
    else if(getenv('HTTP_FORWARDED_FOR'))
        $ipaddress = getenv('HTTP_FORWARDED_FOR');
    else if(getenv('HTTP_FORWARDED'))
       $ipaddress = getenv('HTTP_FORWARDED');
    else if(getenv('REMOTE_ADDR'))
        $ipaddress = getenv('REMOTE_ADDR');
    else
        $ipaddress = 'UNKNOWN';
    return $ipaddress;
}

if(isset($_GET['id'])) {

	$content ="";
	$fl='text/'.$_GET["id"].'/status.txt'; 
	$dirSend = 'text/'.$_GET["id"]."/send/";

	if (!file_exists($fl)) {
		mkdir ( $dirSend, 0777, True); 
	}

	//date
	$content =(string)time(). ":last_update:". (string)time(). "\n";
	//temp
	$content .= (string)time().  ":temp:". $_GET['temp']."\n";
	//temp_ext
	$content .= (string)time().  ":temp_ext:". $_GET['temp_ext']."\n";
	//rele
	$content .= (string)time().  ":rele:". $_GET['rele']."\n";
	$content .= (string)time().  ":ip:".get_client_ip();


    /*write operation ->*/
	$tmp =fopen($fl, "w");
	if ($tmp != FALSE )
	{
		fwrite($tmp, $content);
	}
	fclose($tmp);

	
	if(is_dir_empty($dirSend))
	{
		echo "update:none\n";
	}
	else
	{
	echo "update:read\n";
	}
	
	
	// ultima conexion:
	$path_ultimo_Acceso = 'text/'.$_GET['id']."/ultimoAcceso.txt";
	$origen =fopen($path_ultimo_Acceso, 'r');
	if ($origen){
		if (($timepo = fgets($origen, 4096)) !== false) {
			$timepo = trim($timepo);
			$lastTime= $timepo + 0;
			if(time()- $lastTime>600)
			{
			echo "segsendstatus:600\n";
			}
			else if (time()- $lastTime>60)
			{
			echo "segsendstatus:60\n";
			}
			else
			{
			echo "segsendstatus:5\n";
			}
		}
	}
	else
	{
		echo "leeConf error, imposible leer en:" .$path_ultimo_Acceso."\n" ;
		exit();
	}
}
?>
