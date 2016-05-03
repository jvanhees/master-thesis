<?php
$file = file_get_contents('clips.json');
$clips = json_decode($file,true);

$file = file_get_contents('thumbnails.json');
$thumbnails = json_decode($file,true);


$newData = [];

$i = 0;
foreach($clips['items'] as $clipKey => $clip){
	foreach($thumbnails as $thumbkey => $thumbnail){
		if($clip['id'] == $thumbnail['id']){
			$i++;
			$clips['items'][$clipKey]['thumbnail'] = $thumbnail;
			echo $i . ': ' . $clip['id'] . '<br />';
			unset($thumbnails[$thumbkey]);
		}
	}
}

$fp = fopen('results.json', 'w');
fwrite($fp, json_encode($clips));
fclose($fp);


?>
<pre>
<?php
	print_r($thumbnails);
?>
<?php
	print_r($clips);
?>
</pre>