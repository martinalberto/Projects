<!DOCTYPE html> 
<html> 
	<head>
  <meta charset="UTF-8">	
	<title>Utemper Control</title> 
	
	<meta name="viewport" content="width=device-width, initial-scale=1"> 
	<link rel="stylesheet" href="jquery.mobile.structure-1.0.1.css" />
	<link rel="stylesheet" href="css/font-awesome.min.css" />
	<link rel="apple-touch-icon" href="images/launch_icon_57.png" />
	<link rel="apple-touch-icon" sizes="72x72" href="images/launch_icon_72.png" />
	<link rel="apple-touch-icon" sizes="114x114" href="images/launch_icon_114.png" />
	<link rel="stylesheet" href="jquery.mobile-1.0.1.css" />
	<link rel="stylesheet" href="custom.css" />
	<script src="js/jquery-1.7.1.min.js"></script>
	<script src="js/jquery.mobile-1.0.1.min.js"></script>
</head> 

<body> 
<div data-role="page" id="home" data-theme="c">

	<div data-role="content">
	
	<div id="branding">
		<h1>Utemper Control </h1>
	</div>
	<form method="POST" action="index.html" data-ajax="false" >
	<div class="choice_list"> 
	<!-- <h1> What would you'd like to eat? </h1> -->
	<?php if($_GET['response']=='ok'){?>
	<br>
	<div data-theme="a" data-form="ui-body-a" class="ui-body ui-body-a ui-corner-all">
			<p>Los cambios se han guardado correctamente. Puede verificarlos accediendo donde se han editado</p>

		</div>
		<?php } ?>
<input type="submit" data-role="button" data-icon="checkbox-on" value="Ir a página principal" />	
	</form >
	</div>
	</div>



</div><!-- /page -->
</body>
</html>
