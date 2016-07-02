<?php
if($item == 1){
	$clip = '2551267';
	$videoId = '2653758';
	$title = 'A Plane aborts landing at Cork Airport';
	$text = 'Strong, gusty crosswinds were causing problems on  November 18  at Cork Airport. The pilot of the CityJet flight from London City Airport was forced to abort landing after touchdown and perform a \'go around\' procedure. The plane landed safely a few minutes later.';
} elseif($item == 2){
	$clip = '2526352';
	$videoId = '2653759';
	$title = 'Roy Keane does the Crossbar Challenge';
	$text = 'Roy Keane nails the Crossbar Challenge here at the National Sports Campus.';
} elseif($item == 3){
	$clip = '2553815';
	$videoId = '2653760';
	$title = 'RTE Lotto Champagne Fail';
	$text = 'RTE News captures a syndicate celebrating their lotto win.';
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
				<?php if($_SESSION['imagetype'] == 'static'){ ?>
				<img src="/resources/img/<?=$clip?>.jpg">
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

