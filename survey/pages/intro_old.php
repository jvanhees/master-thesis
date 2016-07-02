<?php
session_unset();
include('../connect.php');

$sql = "SELECT imagetype AS id, COUNT(imagetype) AS count FROM sessions GROUP BY imagetype ORDER BY count DESC LIMIT 1";

if(!$result = $db->query($sql)){
	// Error
	if(rand(1, 2) == 1){
		$_SESSION['imagetype'] = 'static';
	} else {
		$_SESSION['imagetype'] = 'video';
	}
} else {
	$data = $result->fetch_assoc();
	if($data['id'] == 'static'){
		$_SESSION['imagetype'] = 'video';
	} else {
		$_SESSION['imagetype'] = 'static';
	}
}
echo $_SESSION['imagetype'];
?>

<h4>Introductie</h4>
<p>In deze gebruikerstest wordt er onderzoek gedaan naar previews van videos bij nieuwsartikelen. De test bestaat uit drie previews van videos, met elk twee verschillende voorbeelden. Hierbij wordt uw mening gevraagd door middel van een aantal statements, waarbij u kan aangeven of u het hier (deels) eens of (deels) oneens mee bent. Deze test duurt in totaal ongeveer 3 minuten.</p>
<p>De resultaten van deze enquête worden anoniem opgeslagen. Door op "Start" te klikken, gaat u ermee akkoord dat de verzamelde gegevens worden gebruikt voor het gebruik in een onderzoek naar previews van nieuwsartikelen. Meer informatie over het doel van dit onderzoek is beschikbaar aan het einde van deze enquête.</p>
<p class="small">Vanwege technische redenen wordt de enquête niet helemaal correct op smartphones weergegeven, sommige dingen kunnen daarom wat vreemd ogen.</p>
<p>
	<a href="/1/" class="blue waves-effect waves-light btn-large right"><i class="material-icons right">forward</i>Start</a>
</p>
