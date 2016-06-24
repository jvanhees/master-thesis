<?php
if($item == 1){
	$clip = '2485205';
	$videoId = '2651860';
	$title = 'Sea Princess';
	$text = 'Visitors from Australia and New Zealand arrive in Cobh on board the cruise liner Sea Princess on their world tour from Sydney.';
} elseif($item == 2){
	$clip = '2452879';
	$videoId = '2652964';
	$title = 'Motors and Me Patrick O\'Sullivan';
	$text = 'Patrick O\'Sullivan from Clonakilty with his 1968 Daimler 420 Sovereign.';
} elseif($item == 3){
	$clip = '2489018';
	$videoId = '2652966';
	$title = 'Roller Derby double header hosted at Little Island Sports Complex';
	$text = 'Mars Grand Dam O\'Reilly, Co Captain of Cork City Firebirds at the Roller Derbydouble header hosted at Little Island Sports Complex.';
}

if($page == 'without'){
	?>
	<article class="article-preview card">
		<div class="card-content">
			<span class="card-title"><?=$title?></span>
			<p><?=$text?></p>
		</div>
	</article>
	<?php
} elseif($page == 'with'){
	?>
	<article class="article-preview card">
		<div class="card-image">
			<div>
				<?php if($_SESSION['thumbnail'] == 'static'){ ?>
				<img src="/resources/img/<?=$clip?>.jpeg">
				<?php } else { ?>
				<script type="text/javascript" src="//jorick.bbvms.com/p/survey_thumbnail/c/<?=$videoId?>.js"></script>
				<?php } ?>
				<span class="card-title"><?=$title?></span>
			</div>
		</div>
		<div class="card-content">
			<p><?=$text?></p>
		</div>
	</article>
	<?php
}

?>

