<?php
	$wproto_slider_show = isset( $data['wproto_slider_show'] ) ? $data['wproto_slider_show'] : 'no';
	$wproto_slider_position = isset( $data['wproto_slider_position'] ) ? $data['wproto_slider_position'] : 'page_header';
	$wproto_slider_type = isset( $data['wproto_slider_type'] ) ? $data['wproto_slider_type'] : 'full_width';
	$wproto_slider_id = isset( $data['wproto_slider_id'] ) ? $data['wproto_slider_id'] : '';
	
	$wproto_display_text_after_slider = isset( $data['wproto_display_text_after_slider'] ) ? $data['wproto_display_text_after_slider'] : 'no';
	$wproto_display_button_after_slider = isset( $data['wproto_display_button_after_slider'] ) ? $data['wproto_display_button_after_slider'] : 'no';
	$wproto_display_button_after_slider_at_new = isset( $data['wproto_display_button_after_slider_at_new'] ) ? $data['wproto_display_button_after_slider_at_new'] : 'no';
	$wproto_display_button_after_slider_text = isset( $data['wproto_display_button_after_slider_text'] ) ? $data['wproto_display_button_after_slider_text'] : '';
	$wproto_display_button_after_slider_link = isset( $data['wproto_display_button_after_slider_link'] ) ? $data['wproto_display_button_after_slider_link'] : '';
	$wproto_subheader_after_slider = isset( $data['wproto_subheader_after_slider'] ) ? $data['wproto_subheader_after_slider'] : '';
	$wproto_header_after_slider = isset( $data['wproto_header_after_slider'] ) ? $data['wproto_header_after_slider'] : '';
	
?>
<table class="form-table wproto-form-table">
	<tr>
		<th><label for="wproto_slider_show"><?php _e( 'Show slider', 'wproto' ); ?>:</label><br />
		<span class="description"><?php _e( sprintf( 'You can manage slides and slider settings at <a href="%s" target="_blank">this page</a>.', admin_url('admin.php?page=layerslider') ), 'wproto'); ?></span></th>
		<td>
		
			<div class="field switch">
				<label class="cb-enable <?php echo $wproto_slider_show == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
				<label class="cb-disable <?php echo $wproto_slider_show == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
				<input data-toggle-element="tr.wproto-slider-options" name="wproto_settings[wproto_slider_show]" type="hidden" value="<?php echo $wproto_slider_show; ?>" />
				<div class="clear"></div>
			</div>
		
		</td>
	</tr>
	<tr class="wproto-slider-options" <?php echo $wproto_slider_show != 'yes' ? 'style="display: none"' : ''; ?>>
		<th><label for="wproto_slider_position"><?php _e( 'Position', 'wproto' ); ?>:</label></th>
		<td>
		
			<select id="wproto_slider_position" class="select" name="wproto_settings[wproto_slider_position]">
				<option value="page_header"><?php _e( 'At page header', 'wproto' ); ?></option>
				<option <?php echo $wproto_slider_position == 'post_header' ? 'selected="selected"' : ''; ?> value="post_header"><?php _e( 'Below post header', 'wproto' ); ?></option>
			</select>
		
		</td>
	</tr>
	<tr class="wproto-slider-options" <?php echo $wproto_slider_show != 'yes' ? 'style="display: none"' : ''; ?>>
		<th><label for="wproto_slider_id"><?php _e( 'Choose slideshow', 'wproto' ); ?>:</label></th>
		<td>
		
			<select name="wproto_settings[wproto_slider_id]" class="select">
				<option value=""><?php _e('Select...', 'wproto'); ?></option>
				<?php if( gettype( $data['layerslider_items'] ) == 'array' && count( $data['layerslider_items'] ) > 0 ): ?>
					<?php foreach( $data['layerslider_items'] as $ls_item ): ?>
						<option <?php echo $wproto_slider_id == $ls_item->id ? 'selected="selected"' : ''; ?> value="<?php echo $ls_item->id; ?>"><?php echo $ls_item->name; ?></option>
					<?php endforeach; ?>
				<?php endif; ?>
			</select>
		
		</td>
	</tr>
	<tr>
		<th><label><?php _e( 'Display text section after slider', 'wproto' ); ?>:</label><br />
		<span class="description"><?php _e( 'This setting can be applied only for &laquo;page header&raquo; slider', 'wproto' ); ?></span></th>
		<td>
		
			<div class="field switch">
				<label class="cb-enable <?php echo $wproto_display_text_after_slider == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
				<label class="cb-disable <?php echo $wproto_display_text_after_slider == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
				<input data-toggle-element="tr.wproto-after-slider-text-options" name="wproto_settings[wproto_display_text_after_slider]" type="hidden" value="<?php echo $wproto_display_text_after_slider; ?>" />
				<div class="clear"></div>
			</div>
		
		</td>
	</tr>
	<tr class="wproto-after-slider-text-options" <?php echo $wproto_display_text_after_slider != 'yes' ? 'style="display: none"' : ''; ?>>
		<th><label for="wproto_slider_position"><?php _e( 'Header text', 'wproto' ); ?>:</label></th>
		<td>
		
			<input type="text" class="text" name="wproto_settings[wproto_header_after_slider]" value="<?php echo $wproto_header_after_slider; ?>" />
		
		</td>
	</tr>
	<tr class="wproto-after-slider-text-options" <?php echo $wproto_display_text_after_slider != 'yes' ? 'style="display: none"' : ''; ?>>
		<th><label for="wproto_slider_position"><?php _e( 'Subheader text', 'wproto' ); ?>:</label></th>
		<td>
		
			<input type="text" class="text" name="wproto_settings[wproto_subheader_after_slider]" value="<?php echo $wproto_subheader_after_slider; ?>" />
		
		</td>
	</tr>
	<tr class="wproto-after-slider-text-options" <?php echo $wproto_display_text_after_slider != 'yes' ? 'style="display: none"' : ''; ?>>
		<th><label for="wproto_slider_position"><?php _e( 'Display action button', 'wproto' ); ?>:</label></th>
		<td>
		
			<div class="field switch">
				<label class="cb-enable <?php echo $wproto_display_button_after_slider == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
				<label class="cb-disable <?php echo $wproto_display_button_after_slider == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
				<input data-toggle-element="tr.wproto-after-slider-text-options" name="wproto_settings[wproto_display_button_after_slider]" type="hidden" value="<?php echo $wproto_display_button_after_slider; ?>" />
				<div class="clear"></div>
			</div>
		
		</td>
	</tr>
	<tr class="wproto-after-slider-text-options" <?php echo $wproto_display_text_after_slider != 'yes' ? 'style="display: none"' : ''; ?>>
		<th><label for="wproto_slider_position"><?php _e( 'Open button link at new window', 'wproto' ); ?>:</label></th>
		<td>
		
			<div class="field switch">
				<label class="cb-enable <?php echo $wproto_display_button_after_slider_at_new == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
				<label class="cb-disable <?php echo $wproto_display_button_after_slider_at_new == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
				<input data-toggle-element="tr.wproto-after-slider-text-options" name="wproto_settings[wproto_display_button_after_slider_at_new]" type="hidden" value="<?php echo $wproto_display_button_after_slider_at_new; ?>" />
				<div class="clear"></div>
			</div>
		
		</td>
	</tr>
	<tr class="wproto-after-slider-text-options" <?php echo $wproto_display_text_after_slider != 'yes' ? 'style="display: none"' : ''; ?>>
		<th><label for="wproto_slider_position"><?php _e( 'Button link', 'wproto' ); ?>:</label></th>
		<td>
		
			<input type="text" class="text" name="wproto_settings[wproto_display_button_after_slider_link]" value="<?php echo $wproto_display_button_after_slider_link; ?>" />
		
		</td>
	</tr>
	<tr class="wproto-after-slider-text-options" <?php echo $wproto_display_text_after_slider != 'yes' ? 'style="display: none"' : ''; ?>>
		<th><label for="wproto_slider_position"><?php _e( 'Button text', 'wproto' ); ?>:</label></th>
		<td>
		
			<input type="text" class="text" name="wproto_settings[wproto_display_button_after_slider_text]" value="<?php echo $wproto_display_button_after_slider_text; ?>" />
		
		</td>
	</tr>
</table>