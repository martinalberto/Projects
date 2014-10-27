<?php
error_reporting(-1);

function is_dir_empty($dir) {
  if (!is_readable($dir)) return NULL; 
  return (count(scandir($dir)) == 2);
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
	//rele
	$content .= (string)time().  ":rele:". $_GET['rele']."\n";


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
	
}
?>
