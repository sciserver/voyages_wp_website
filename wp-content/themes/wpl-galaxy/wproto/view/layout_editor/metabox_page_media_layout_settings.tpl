<?php
	$wproto_media_tpl_display_type = isset( $data['wproto_media_tpl_display_type'] ) ? $data['wproto_media_tpl_display_type'] : 'wproto_portfolio';
	$wproto_media_tpl_post_title = isset( $data['wproto_media_tpl_post_title'] ) ? $data['wproto_media_tpl_post_title'] : '';
	$wproto_media_tpl_post_id = isset( $data['wproto_media_tpl_post_id'] ) ? absint( $data['wproto_media_tpl_post_id'] ) : 0;
?>
<table class="form-table wproto-form-table">
	<tr>
		<th><label for="wproto_media_tpl_display_type"><?php _e( 'Content to display', 'wproto' ); ?>:</label></th>
		<td>
		
			<select class="select" name="wproto_settings[wproto_media_tpl_display_type]" id="wproto_media_tpl_display_type">
				<option value="wproto_portfolio"><?php _e('Portfolio', 'wproto'); ?></option>
				<option <?php echo $wproto_media_tpl_display_type == 'wproto_photoalbums' ? 'selected="selected"' : ''; ?> value="wproto_photoalbums"><?php _e('Photo album', 'wproto'); ?></option>
			</select>
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto_media_tpl_post_title"><?php _e( 'Select a post to display images from', 'wproto' ); ?>:</label></th>
		<td>
		
			<input type="text" name="wproto_settings[wproto_media_tpl_post_title]" class="text" value="<?php echo $wproto_media_tpl_post_title; ?>" id="wproto_media_tpl_post_title" />
		
			<input type="hidden" value="<?php echo $wproto_media_tpl_post_id; ?>" id="wproto_media_tpl_post_id" name="wproto_settings[wproto_media_tpl_post_id]" />
		
			<p class="description"><?php _e( 'Start typing to search the posts', 'wproto' ); ?></p>
		
		</td>
	</tr>
	<?php
		$display_images_data = isset( $data['display_images_data'] ) ? $data['display_images_data'] : 'no';
		$display_call_to_action = isset( $data['display_call_to_action'] ) ? $data['display_call_to_action'] : 'no';
		$call_to_action_text = isset( $data['call_to_action_text'] ) ? $data['call_to_action_text'] : '';
		$call_to_action_button_text = isset( $data['call_to_action_button_text'] ) ? $data['call_to_action_button_text'] : '';
		$call_to_action_button_link = isset( $data['call_to_action_button_link'] ) ? $data['call_to_action_button_link'] : '';
	?>
	<tr>
	
		<th><label><?php _e( 'Display image title and date', 'wproto' ); ?>:</label></th>
		<td>
		
			<div class="field switch">
				<label class="cb-enable <?php echo $display_images_data == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
				<label class="cb-disable <?php echo $display_images_data == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
				<input name="wproto_settings[display_images_data]" type="hidden" value="<?php echo $display_images_data; ?>" />
				<div class="clear"></div>
			</div>
		
		</td>
	
	</tr>
	<tr>
	
		<th><label><?php _e( 'Show call to action block after slider', 'wproto' ); ?>:</label></th>
		<td>
		
			<div class="field switch">
				<label class="cb-enable <?php echo $display_call_to_action == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
				<label class="cb-disable <?php echo $display_call_to_action == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
				<input data-toggle-element="tr.wproto-call-to-action-options" name="wproto_settings[display_call_to_action]" type="hidden" value="<?php echo $display_call_to_action; ?>" />
				<div class="clear"></div>
			</div>
		
		</td>
	
	</tr>
	<tr class="wproto-call-to-action-options" style="<?php echo $display_call_to_action != 'yes' ? 'display: none' : ''; ?>">
		<th><label><?php _e( 'Call to action text', 'wproto' ); ?>:</label></th>
		<td>
		
		<?php
			wp_editor(
				stripslashes( str_replace( '\'', "&#39;", $call_to_action_text ) ),
				'wproto-call-to-action-text',
				array(
					'media_buttons' => false,
					'textarea_name' => 'wproto_settings[call_to_action_text]',
					'textarea_rows' => 8,
					'teeny' => true,
					'quicktags' => true,
					'tinymce' => array(
						'theme_advanced_buttons2' => '',
						'theme_advanced_buttons3' => '',
						'theme_advanced_buttons4' => ''
					)	
				)
			);
		?>
		
		</td>
	</tr>
	<tr class="wproto-call-to-action-options" style="<?php echo $display_call_to_action != 'yes' ? 'display: none' : ''; ?>">
		<th><label for="wproto_section_data-button-title"><?php _e( 'Button text', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_data-button-title" name="wproto_settings[call_to_action_button_text]" class="text" type="text" maxlength="255" value="<?php echo $call_to_action_button_text; ?>" />
		
		</td>
	</tr>
	<tr class="wproto-call-to-action-options" style="<?php echo $display_call_to_action != 'yes' ? 'display: none' : ''; ?>">
		<th><label for="wproto_section_data-button_link"><?php _e( 'Button link', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_data-button_link" name="wproto_settings[call_to_action_button_link]" class="text" type="text" maxlength="255" value="<?php echo $call_to_action_button_link; ?>" />
		
		</td>
	</tr>
</table>