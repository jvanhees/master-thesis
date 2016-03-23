<?php
include 'header.php';

$output = [
	//['Clip title', 'Clips']
];

foreach($data->items as $clip){
	if(isset($clip->cat)){
		array_push($output, [$clip->title, count($clip->cat)]);
	} else {
		array_push($output, [$clip->title, 0]);
	}
}

echo json_encode($output);
?>