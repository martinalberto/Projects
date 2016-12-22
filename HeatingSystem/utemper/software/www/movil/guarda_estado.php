<?php
include('head.php');
?>

<!DOCTYPE html> 
<html> 
	<head>
	</head> 

<body> 
<?php
if (!is_numeric($_GET['estado']))
{
echo "Error estado no es un numero. \n";
exit();
}

$dir = 'text/'.$_SESSION["equipo"];
guardaConf($dir, "estado_caldera",$_GET['estado']);


echo '<meta http-equiv="refresh" content="0; url=index.php?response=ok&nocache='.time().'">';
?>
</body>
</html>