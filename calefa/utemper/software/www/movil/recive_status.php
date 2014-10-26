<?php
error_reporting(-1);

if(isset($_GET['id'])) {

	$content ="";
	$fl='/tmp/utemper/estado/'.$_GET["id"].'.php'; 
	
	if (!file_exists($fl)) {
		mkdir ( "/tmp/utemper/estado/", 0777, True); 
	}
	
    /*read operation ->*/ 
	//echo $fl;
	//$tmp = fopen($fl, "r");
	//if ($tmp != FALSE )
	//	$content=fread($tmp,filesize($fl));
	//fclose($tmp);

	//date
	$content =(string)time(). ":last_update=". (string)time(). "\n";
	//temp
	$content .= (string)time().  ":temp=". $_GET['temp']."\n";
	//rele
	$content .= (string)time().  ":rele=". $_GET['rele']."\n";

	
    /*write operation ->*/
	$tmp =fopen($fl, "w");
	fwrite($tmp, $content);
	fclose($tmp);
	//echo "READ";
}
?>
