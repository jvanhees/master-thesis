<?php
function likert($group){
	return '
	<div class="likert">
		<p>
			<input name="'.$group.'" type="radio" value="-2" id="'.$group.'-2" />
			<label for="'.$group.'-2">Zeer mee oneens</label>
		</p>
		<p>
			<input name="'.$group.'" type="radio" value="-1" id="'.$group.'-1" />
			<label for="'.$group.'-1">Oneens</label>
		</p>
		<p>
			<input name="'.$group.'" type="radio" value="0" id="'.$group.'0" />
			<label for="'.$group.'0">Noch eens, noch oneens</label>
		</p>
		<p>
			<input name="'.$group.'" type="radio" value="1" id="'.$group.'1" />
			<label for="'.$group.'1">Eens</label>
		</p>
		<p>
			<input name="'.$group.'" type="radio" value="2" id="'.$group.'2" />
			<label for="'.$group.'2">Zeer mee eens</label>
		</p>
	</div>';
}
	
	
?>


<form action="process.php" method="post">
	<input style="display: none;" name="formtype" value="<?php echo $formType; ?>">
	<input style="display: none;" name="item" value="<?php echo $item; ?>">
	<p><strong>Door bovenstaande preview ben ik geïnteresseerd in het bekijken van het nieuwsartikel.</strong></p>
	
	<?=likert('interest')?>
	
	<p><strong>Door bovenstaande preview krijg ik een duidelijk beeld van wat ik van het nieuwsartikel kan verwachten.</strong></p>
	
	<?=likert('expectation')?>
	
	<p>
		<?php echo next_button('?p=2', 'Volgende'); ?>
	</p>
</form>

