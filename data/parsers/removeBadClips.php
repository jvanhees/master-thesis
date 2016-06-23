<?php
$file = file_get_contents('../interface/data.json');
$data = json_decode($file);

foreach($data as $clip => $idx){
	print_r($clip);
}






?>