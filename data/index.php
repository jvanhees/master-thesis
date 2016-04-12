<?php
$file = file_get_contents('data.json');
$data = json_decode($file);

$hasTitle = 0;
$hasDescription = 0;
$hasTags = 0;

foreach($data->items as $clip){
	if(isset($clip->title)){
		$hasTitle++;
	}
	if(isset($clip->description)){
		$hasDescription++;
	}
	if(isset($clip->cat)){
		$hasTags++;
	}
}
?>
<!doctype HTML>
<html>
<head>
<title>Data</title>
<link rel="stylesheet" href="style.css" type="text/css" media="screen">
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
<script type="text/javascript" src="main.js"></script>
</script>
</head>
<body>
<a href="browse.php">Browse clips</a>
<pre>
<?php
print_r(json_decode($data->items[0]->assets));
?>
</pre>
<h1>Stats</h1>
<table>
	<tr>
		<td>Total clips</td>
		<td><?=$data->numfound?></td>
	</tr>
	<tr>
		<td>With title</td>
		<td><?=$hasTitle?></td>
	</tr>
	<tr>
		<td>With description</td>
		<td><?=$hasDescription?></td>
	</tr>
	<tr>
		<td>With tags</td>
		<td><?=$hasTags?></td>
	</tr>
</table>
<h2>Longest clips</h2>

<hr />
<div id="tag-dist"></div>
<hr />
<div id="length-dist"></div>
<hr />
<div id="most-used"></div>
</html>
</body>