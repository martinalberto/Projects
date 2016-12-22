<?php
include('head.php');
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