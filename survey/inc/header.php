<!doctype html>
<html>
<head>
	<title>News article user survey</title>
	
	<meta charset="UTF-8">
	
	<!--Import Google Icon Font-->
	<link href="http://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
	
	<link rel="stylesheet" href="/css/materialize.css" type="text/css" media="screen">
	<link rel="stylesheet" href="/css/main.css" type="text/css" media="screen">
	
	<!--Let browser know website is optimized for mobile-->
	<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>
<body>
	<!--Import jQuery before materialize.js-->
	<script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
	<script type="text/javascript" src="js/materialize.min.js"></script>
	<nav class="white-text blue-grey">
		<div class="nav-wrapper container">
			<a href="/" class="title">Onderzoek naar previews van nieuwsartikelen</a>
			
			<ul id="nav-mobile" class="right">
				<li><a href="#!" class="link">Over</a></li>
			</ul>
		</div>
	</nav>
	<div class="progress blue-grey lighten-4">
		<div class="determinate blue-grey darken-2" style="width: <?=$p * (100 / $totalPages) ?>%"></div>
	</div>
	<div class="container main">
		<span class="badge"><?php echo $p; ?> / <?php echo $totalPages; ?></span>