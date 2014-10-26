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
            <h2> Selecion red Wifi</h2>
               <p> La red Selecionada es:  <strong><?echo $_GET['red']; ?></strong></p>
            <table border="0" cellpadding="0" cellspacing="0">
               <tr>
                  <td>IP Address:</td>
                  <td><input type='number' name='ethIpAddress' onChange='setDhcpAddresses(this.value)'></td>
               </tr>
               <tr>
                  <td>Gateway:</td>
                  <td><input type='number' name='gateway'></td>
               </tr>
                 <tr>
                     <td>Subnet Mask:</td>
                     <td><input type='number' name='dhcpSubnetMask' onChange='manualModDhcp()'></td>
                  </tr>                    
                  <tr>
                     <td>Primary DNS:</td>
                     <td><input type='number' name='dhcpPrimaryDns'></td>
                  </tr>
				  <tr>
                     <td>Secondary DNS:</td>
                     <td><input type='number' name='dhcpSecondaryDns'></td>
                  </tr>
            </table>
            <br>

          

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
