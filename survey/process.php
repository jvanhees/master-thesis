<?php
session_start();
include('inc/functions.php');

print_r($_POST);


$_SESSION['thumbnail'] = 'video';

if($_POST['formtype'] == 'without'){
	$_SESSION['page'] = 2;
} elseif($_POST['formtype'] == 'with'){
	$_SESSION['page'] = 3;
} else {
	$_SESSION['page'] = 0;
}

print $_SESSION['page'];

Redirect("/");
die();

?>