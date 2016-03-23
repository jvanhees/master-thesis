<?php
include('header.php');

usort($data->items, function($a, $b) {
	if(!isset($a->length_int)){
		return -1;
	} else if(!isset($b->length_int)){
		return 1;
	}
    return $a->length_int - $b->length_int;
});
$results = array_reverse($data->items);


for($i = 0; $i < 10; $i++){
	$c = $results[$i];
	echo $c->length_int . ' ' . $c->title . '<br />';
}
?>