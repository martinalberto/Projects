<?php
error_reporting(-1);

if(isset($_POST['id'])) {
	$fl='/tmp/utemper/config/'.$_POST["id"].'.conf'; 
	if ($_POST['operacion']=="2utemper")
	{	
    /*read operation ->*/
		$tmp = fopen($fl, "r");
		if ($tmp != FALSE )
		{
			$data =fread($tmp,filesize($fl));
			echo $data;
			fclose($tmp);
			echo (string)unlink($fl);
		}
		else
			mkdir ( "/tmp/utemper/config/", 0777 ,True); 
			//http_response_code(600);
	}
}
else
{
echo "ERROR";
}
?>