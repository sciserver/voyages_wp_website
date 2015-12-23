<p>
	<label><?php _e('Custom link', 'wproto'); ?></label>
	<input type="text" name="wproto_benefit_link" value="<?php echo $data['link']; ?>" />
</p>
<p>
	<label><?php _e('Animation settings', 'wproto'); ?></label>
	<select name="wproto_benefit_animation">
		<option value=""><?php _e('Default', 'wproto'); ?></option>
		<option <?php echo $data['animation'] == 'bounceIn' ? 'selected="selected"' : ''; ?> value="bounceIn">bounceIn</option>
		<option <?php echo $data['animation'] == 'fadeIn' ? 'selected="selected"' : ''; ?> value="fadeIn">fadeIn</option>
		<option <?php echo $data['animation'] == 'fadeInUp' ? 'selected="selected"' : ''; ?> value="fadeInUp">fadeInUp</option>
		<option <?php echo $data['animation'] == 'fadeInDown' ? 'selected="selected"' : ''; ?> value="fadeInDown">fadeInDown</option>
		<option <?php echo $data['animation'] == 'fadeInLeft' ? 'selected="selected"' : ''; ?> value="fadeInLeft">fadeInLeft</option>
		<option <?php echo $data['animation'] == 'fadeInRight' ? 'selected="selected"' : ''; ?> value="fadeInRight">fadeInRight</option>
		<option <?php echo $data['animation'] == 'fadeInUpBig' ? 'selected="selected"' : ''; ?> value="fadeInUpBig">fadeInUpBig</option>
		<option <?php echo $data['animation'] == 'fadeInDownBig' ? 'selected="selected"' : ''; ?> value="fadeInDownBig">fadeInDownBig</option>
		<option <?php echo $data['animation'] == 'fadeInLeftBig' ? 'selected="selected"' : ''; ?> value="fadeInLeftBig">fadeInLeftBig</option>
		<option <?php echo $data['animation'] == 'fadeInRightBig' ? 'selected="selected"' : ''; ?> value="fadeInRightBig">fadeInRightBig</option>
		<option <?php echo $data['animation'] == 'rotateIn' ? 'selected="selected"' : ''; ?> value="rotateIn">rotateIn</option>
		<option <?php echo $data['animation'] == 'rotateInUpLeft' ? 'selected="selected"' : ''; ?> value="rotateInUpLeft">rotateInUpLeft</option>
		<option <?php echo $data['animation'] == 'rotateInDownLeft' ? 'selected="selected"' : ''; ?> value="rotateInDownLeft">rotateInDownLeft</option>
		<option <?php echo $data['animation'] == 'rotateInUpRight' ? 'selected="selected"' : ''; ?> value="rotateInUpRight">rotateInUpRight</option>
		<option <?php echo $data['animation'] == 'rotateInDownRight' ? 'selected="selected"' : ''; ?> value="rotateInDownRight">rotateInDownRight</option>
		<option <?php echo $data['animation'] == 'flash' ? 'selected="selected"' : ''; ?> value="flash">flash</option>
	</select>
</p>
<p>
	<label style="display: block"><?php _e('Animation delay in seconds', 'wproto'); ?></label>
	<input type="text" name="wproto_benefit_animation_delay" value="<?php echo $data['animation_delay'] == '' ? '0.0' : $data['animation_delay']; ?>" />
	<div class="description"><?php _e('(for example: 0.3)', 'wproto'); ?></div>
</p>
<p>
	<label><input type="radio" class="wproto-benefit-style-chooser" <?php echo $data['style'] == '' || $data['style'] == 'image' ? 'checked="checked"' : ''; ?> name="wproto_benefit_style" value="image" /> <?php _e( 'Use Featured Image as benefit icon', 'wproto' ); ?></label>
</p>
<p>
	<label><input type="radio" class="wproto-benefit-style-chooser" <?php echo $data['style'] == 'icon' ? 'checked="checked"' : ''; ?> name="wproto_benefit_style" value="icon" /> <?php _e( 'Select an icon from the library', 'wproto' ); ?></label>
</p>
<p id="wproto-benefit-icon-chooser" <?php echo $data['style'] == '' || $data['style'] == 'image' ? ' style="display: none;"' : ''; ?>>
	<?php echo $data['icon'] <> '' ? '<i data-name="' . $data['icon'] . '" class="wproto-icon-holder ' . $data['icon'] . ' fa-4x"></i> <a href="javascript:;" class="wproto-icon-chooser">' . __( 'Change', 'wproto') . '</a>' : '<i data-name="" class="wproto-icon-holder icon-2x"></i> <a href="javascript:;" class="wproto-icon-chooser">' . __( 'Select icon', 'wproto') . '</a>'; ?>
	<input type="hidden" value="<?php echo $data['icon']; ?>" name="wproto_benefit_icon_name" class="wproto-icon-holder-input" />
</p>