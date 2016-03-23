<?php
include 'header.php';

$output = [
	//['Clip title', 'Length']
];

foreach($data->items as $clip){
	if(isset($clip->length_int)){
		array_push($output, [$clip->title, $clip->length_int]);
	}
}

echo json_encode($output);
?>