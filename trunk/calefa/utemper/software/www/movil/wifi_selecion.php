<?php
session_start();
//manejamos en sesion el nombre del usuario que se ha logeado
if (!isset($_SESSION["usuario"])){
 //   header("location:login/index.php?nologin=false");
    
}
$_SESSION["usuario"];
?>
<!DOCTYPE html> 
<html> 
<head> 
	<meta charset="UTF-8">
	<title>Utemper Control</title> 
	<meta name="viewport" content="width=device-width, initial-scale=1"> 
	<link rel="stylesheet" href="css/jquery.mobile.structure-1.0.1.css" />
	<link rel="apple-touch-icon" href="images/launch_icon_57.png" />
	<link rel="apple-touch-icon" sizes="72x72" href="images/launch_icon_72.png" />
	<link rel="apple-touch-icon" sizes="114x114" href="images/launch_icon_114.png" />
	<link rel="stylesheet" href="css/jquery.mobile-1.0.1.css" />
	<link rel="stylesheet" href="css/custom.css" />
	<script src="js/jquery-1.7.1.min.js"></script>
	<script src="js/jquery.mobile-1.0.1.min.js"></script>
</head> 
<body> 
<div id="choisir_ville" data-role="page" data-add-back-btn="true">
	
	<div data-role="header"> 
		<h1>Utemper Control</h1>
	</div> 

	<div data-role="content">
	
	<div class="choice_list"> 

         <form>
            <b>Setup Wifi:</b><br>
	       <hr>
            <h2> Seleci&oacute;n red Wifi</h2>
               <p> La red Selecionada es:  <strong><?echo $_GET['red']; ?></strong></p>
			   <?php
			   if ($_GET['cript']==1 ){
					echo "<p> La red esta protegida por contrase&ntilde;a. <br> Es necesario introducir la contrase&ntilde;a para poder terminar la configuraci&oacute;n </p>";
					
            echo '<table border="0" cellpadding="0" cellspacing="0">';
               echo '<tr>';
                echo '  <td>Password:</td>';
                echo '  <td><input type="password" name="pass"></td>';
              echo '</tr>';
            echo '</table>';
            echo '<br>';
				}
			else
			{
			echo "<p> ¿Desea guardar y acceder a esta red Wifi.? </p>";
			}
				?>				
            <center>
               <p align="center">
                  <input type='button' onClick='btnSave(0)' value='Guardar'> 
            </center>
         </form>

	</div>
	
	</div>

</div><!-- /page -->
</body>
</html>
