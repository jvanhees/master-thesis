<?php
if($item == 1){
	$videoId = '2651860';
	$title = 'Sea Princess';
	$text = 'Visitors from Australia and New Zealand arrive in Cobh on board the cruise liner Sea Princess on their world tour from Sydney.
	Video Eddie O\'Hare Evening Echo';
} elseif($item == 2){
	
} elseif($item == 3){
	
}

if($page == 'without'){
	?>
	<article class="article-preview card">
		<div class="card-content">
			<span class="card-title">Sea Princess</span>
			<p>Visitors from Australia and New Zealand arrive in Cobh on board the cruise liner Sea Princess on their world tour from Sydney.
	Video Eddie O'Hare Evening Echo</p>
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

