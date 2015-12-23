<p>
	<label for="wproto-add-amination-select"><?php _e( 'Choose animation that will be applied to the selected image', 'wproto' ); ?>: </label>
	<br />	
	<?php 
		$current_anim = isset( $_POST['current_animation'] ) ? strip_tags( $_POST['current_animation'] ) : '';
	?>
	<select style="width: 100%" id="wproto-add-amination-select">
		<option value=""><?php _e('No animation', 'wproto'); ?></option>
		<option <?php echo $current_anim == 'fadeIn' ? 'selected="selected"' : ''; ?> value="fadeIn">fadeIn</option>
		<option <?php echo $current_anim == 'fadeInUp' ? 'selected="selected"' : ''; ?> value="fadeInUp">fadeInUp</option>
		<option <?php echo $current_anim == 'fadeInDown' ? 'selected="selected"' : ''; ?> value="fadeInDown">fadeInDown</option>
		<option <?php echo $current_anim == 'fadeInLeft' ? 'selected="selected"' : ''; ?> value="fadeInLeft">fadeInLeft</option>
		<option <?php echo $current_anim == 'fadeInRight' ? 'selected="selected"' : ''; ?> value="fadeInRight">fadeInRight</option>
		<option <?php echo $current_anim == 'fadeInUpBig' ? 'selected="selected"' : ''; ?> value="fadeInUpBig">fadeInUpBig</option>
		<option <?php echo $current_anim == 'fadeInDownBig' ? 'selected="selected"' : ''; ?> value="fadeInDownBig">fadeInDownBig</option>
		<option <?php echo $current_anim == 'fadeInLeftBig' ? 'selected="selected"' : ''; ?> value="fadeInLeftBig">fadeInLeftBig</option>
		<option <?php echo $current_anim == 'fadeInRightBig' ? 'selected="selected"' : ''; ?> value="fadeInRightBig">fadeInRightBig</option>
		<option <?php echo $current_anim == 'rotateIn' ? 'selected="selected"' : ''; ?> value="rotateIn">rotateIn</option>
		<option <?php echo $current_anim == 'rotateInUpLeft' ? 'selected="selected"' : ''; ?> value="rotateInUpLeft">rotateInUpLeft</option>
		<option <?php echo $current_anim == 'rotateInDownLeft' ? 'selected="selected"' : ''; ?> value="rotateInDownLeft">rotateInDownLeft</option>
		<option <?php echo $current_anim == 'rotateInUpRight' ? 'selected="selected"' : ''; ?> value="rotateInUpRight">rotateInUpRight</option>
		<option <?php echo $current_anim == 'rotateInDownRight' ? 'selected="selected"' : ''; ?> value="rotateInDownRight">rotateInDownRight</option>
		<option <?php echo $current_anim == 'flash' ? 'selected="selected"' : ''; ?> value="flash">flash</option>
	</select>
</p>

<div id="wproto-temporary-div"></div>