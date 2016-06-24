<?php
session_unset();
if(rand(1, 2) == 1){
	$_SESSION['imagetype'] = 'static';
} else {
	$_SESSION['imagetype'] = 'video';
}
?>


<h4>Introductie</h4>
<p>In deze gebruikerstest word er onderzoek gedaan naar previews van videos bij nieuwsartikelen. De test bestaat uit drie artikelen, met elk twee verschillende voorbeelden. Hierbij wordt uw mening gevraagd door middel van een aantal statements, waarbij u kan aangeven of u het hier (deels) eens of (deels) oneens mee bent. Deze test duurt in totaal ongeveer 3 minuten.</p>
<p>De resultaten van deze enquête worden anoniem opgeslagen. Door op "Start" te klikken, gaat u ermee akkoord dat de verzamelde gegevens worden gebruikt voor het gebruik in een onderzoek naar previews van nieuwsartikelen. Meer informatie over het doel van dit onderzoek is beschikbaar aan het einde van deze enquête.</p>

<p>
	<a href="/1/" class="blue waves-effect waves-light btn-large right"><i class="material-icons right">forward</i>Start</a>
</p>
