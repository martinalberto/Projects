<!DOCTYPE html> 
<html> 
	<head>
	</head> 

<body> 
<?php
$array_min=array("00","15","30","45");

$data_to_write="";
for($i=0;$i<25;$i++){
for($a=0;$a<4;$a++){
if(($_POST[$i.($array_min[$a])]!="0")&&($_POST[$i.($array_min[$a])]!="1")){
$data_to_write.="0;";
}else{
$data_to_write.=$_POST[$i.($array_min[$a])].";";
}
}
}

if( strlen($data_to_write)>30){
$file_path = "text/".$_POST['dia'].".txt";

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