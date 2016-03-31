<?php
$file = file_get_contents('../tags.json');
$data = json_decode($file);

$output = [
	['(other)', 0]
];
$type = 'tag';
foreach($data->facets->catSort as $key => $value){
	if($type == 'tag'){
		if($data->facets->catSort[$key+1] != 1){
			array_push($output, [$value, $data->facets->catSort[$key+1]]);
		} else {
			$output[0][1]++;
		}
		$type = 'count';
	} else {
		$type = 'tag';
	}	
}

usort($output, "cmp");

echo json_encode($output);


function cmp($a, $b) {
    return $a[1] < $b[1];
}
?>