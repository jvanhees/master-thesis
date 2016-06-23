<?php
function next_button($url, $text){
	return '<button type="submit" class="blue waves-effect waves-light btn-large right"><i class="material-icons right">forward</i>'.$text.'</a>';
}

function Redirect($url, $permanent = false){
    header('Location: ' . $url, true, $permanent ? 301 : 302);
    exit();
}



?>