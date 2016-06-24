<?php
include('inc/functions.php');
session_start();

if(isset($_GET['page'])){
	$p = $_GET['page'];
} else {
	$p = 0;
	$_SESSION['page'] = 0;
}

if($_SESSION['page'] != $p && $p != 1){
	Redirect('/');
	die();
}

if($p == 1 || $p == 2){
	$item = 1;
} elseif($p == 3 || $p == 4) {
	$item = 2;
} elseif($p == 5 || $p == 6) {
	$item = 3;
}

$totalPages = 7;

switch($p){
	case 0:
		$page = 'intro';
		break;
	case 1:
	case 3:
	case 5:
		$page = 'without';
		break;
	case 2:
	case 4:
	case 6:
		$page = 'with';
		break;
	case 7:
		$page = 'outro';
		break;
}

include('inc/header.php');

include('pages/'.$page.'.php');

include('inc/footer.php');
?>