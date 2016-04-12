<?php
if(isset($_GET['c'])){ $count = $_GET['c']; } else { $count = 200; }
if(isset($_GET['p'])){ $page = $_GET['p']; } else { $page = 0; }
$GLOBALS['defaultMediaAssetPath'] = 'https://d2vt09yn8fcn7w.cloudfront.net';
$file = file_get_contents('data.json');
$data = json_decode($file);
$i = $page * $count;
function format($c, $key){
	if(isset($c->{$key})){
		return $c->{$key};
	} else {
		return '';
	}
}
function format_length($seconds){
	$minutes = floor($seconds % 3600 / 60);
	$seconds = $seconds % 60;

	return sprintf("%02d:%02d", $minutes, $seconds);
}
function format_date($zdate){
	$date = new DateTime($zdate, new DateTimeZone('UCT'));
	return $date->format('d-m-Y');
}
function format_tags($c){
	if(isset($c->cat)){
		return implode($c->cat, ', ');
	} else {
		return '';
	}
}
function format_preview($c){
	if(isset($c->assets)){
		$assets = json_decode($c->assets);
		foreach($assets as $asset){
			if($asset->mediatype == 'MP4_MAIN'){
				return '<a href="#" onclick="openVideo(\''.$GLOBALS['defaultMediaAssetPath'].$asset->src.'\')" href="#">'.$asset->mediatype.'</a>';
			}
		}
		return $assets[0]->mediatype;
	} else {
		return '';
	}
}

$clips = array_slice($data->items, $page * $count, ($page * $count) + $count);

?>
<!doctype HTML>
<html>
<head>
<title>Data</title>
<link rel="stylesheet" href="style.css" type="text/css" media="screen">
</head>
<body>
Page <?=$page?> (<?=$page * $count?> - <?=($page * $count) + $count?>)
<div class="pager">
	<a href="?p=<?=$page-1 ?>">Prev</a> - <a href="?p=<?=$page+1 ?>">Next</a>
</div>
<script type="text/javascript">
function openVideo(url){
	window.open(url, 'Preview', 'width=480, height=360'); return false;
}
</script>
<table>
	<thead>
		<tr>
			<td>#</td>
			<td>ID</td>
			<td>Title</td>
			<td>Description</td>
			<td>Length</td>
			<td>Published date</td>
			<td>Tags</td>
			<td>Preview</td>
		</tr>
	</thead>
	<tbody>
		<?php foreach($clips as $c){ ?>
		<?php
		$i++;
		if($i % 2 == 0) { $parity = 'odd'; } else { $parity = 'even'; }
		?>
		<tr class="<?=$parity?>">
			<td><?=$i?></td>
			<td><?=$c->id?></td>
			<td class="title"><?=format($c, 'title')?></td>
			<td class="description"><?=format($c, 'description')?></td>
			<td><?=format_length($c->length_int)?></td>
			<td><?=format_date($c->published_date)?></td>
			<td><?=format_tags($c)?></td>
			<td><?=format_preview($c)?></td>
		</tr>
		<?php } ?>
	</tbody>
</table>
<div class="pager">
	<a href="?p=<?=$page-1 ?>">Prev</a> - <a href="?p=<?=$page+1 ?>">Next</a>
</div>
</body>
</html>