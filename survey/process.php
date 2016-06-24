<?php
session_start();
include('inc/functions.php');
include('connect.php');

if(!isset($_SESSION['id'])){
	$ip = $db->escape_string($_SERVER['REMOTE_ADDR']);
	$imagetype = $_SESSION['imagetype'];

	$sql = 'INSERT INTO `sessions` (`ip`, `imagetype`) VALUES ("'.$ip.'", "'.$imagetype.'")';

	if(!$result = $db->query($sql)){
		// Error
		Redirect('/');
		die();
	} else {
		$_SESSION['id'] = $db->insert_id;
	}
}

$formtype = $db->escape_string($_POST['formtype']);
$item = $db->escape_string($_POST['item']);
$engagement = $db->escape_string($_POST['engagement']);
$information = $db->escape_string($_POST['information']);

// If without image, create a new entry
if($formtype == 'without'){
	$sql = 'INSERT INTO `results` (`session_id`, `item`, `engagement_without`, `information_without`) VALUES ("'.$_SESSION['id'].'", "'.$item.'", "'.$engagement.'", "'.$information.'")';
	if(!$result = $db->query($sql)){
		// Error
		Redirect('/');
		die();
	}
} else {
	// Else modify the entry with the same session id and item
	$sql = 'SELECT `id` FROM `results` WHERE `session_id` = "'.$_SESSION['id'].'" AND `item` = "'.$item.'"';
	$result = $db->query($sql);
	if($result->num_rows > 0) {
		// output data of each row
	    $data = $result->fetch_assoc();
	} else {
		// Error
		Redirect('/');
		die();
	}
	
	$sql = 'UPDATE `results` set `engagement_with`="'.$engagement.'", `information_with`="'.$information.'" WHERE `id` = "'.$data['id'].'"';
	if(!$result = $db->query($sql)){
		// Error
		Redirect('/');
		die();
	}
}

if($formtype == 'without'){
	$pagemodifier = 0;
} else {
	$pagemodifier = 1;
}

$_SESSION['page'] = $pagemodifier + ($item * 2);

Redirect('/'.$_SESSION['page']);
die();

?>