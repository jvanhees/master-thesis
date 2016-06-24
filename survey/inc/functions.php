<?php
function next_button(){
	return '<button type="submit" class="blue waves-effect waves-light btn-large right"><i class="material-icons right">forward</i>Volgende</a>';
}

function Redirect($url, $permanent = false){
    header('Location: ' . $url, true, $permanent ? 301 : 302);
    exit();
}



?>