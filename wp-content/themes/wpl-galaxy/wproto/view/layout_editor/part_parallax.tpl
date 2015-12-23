
<h2><?php _e('Parallax section', 'wproto'); ?></h2>

<table class="form-table wproto-form-table">
	<tr>
		<th>
			<label for="wproto_section_data-background"><?php _e( 'Section background', 'wproto' ); ?>:</label>
		</th>
		<td>
					
			<p>
				<label><?php _e('Background image:', 'wproto'); ?><br />
				<input type="text" id="wproto_section_data-background" class="text" name="wproto_section_data[background]" value="<?php echo isset( $data['wproto_section_data']['background'] ) ? $data['wproto_section_data']['background'] : ''; ?>" /> <a href="javascript:;" class="button wproto-image-selector" data-url-input="#wproto_section_data-background"><?php _e( 'Upload', 'wproto' ); ?></a> 
				<a href="javascript:;" data-url-input="#wproto_section_data-background" class="button wproto-image-remover"><?php _e( 'Remove', 'wproto' ); ?></a></label>
			</p>
						
			<p>
			
				<?php
					$background_repeat = isset( $data['wproto_section_data']['background_repeat'] ) ? $data['wproto_section_data']['background_repeat'] : '';
				?>
			
				<label>
					<?php _e('Background repeat:', 'wproto'); ?><br />
					<select name="wproto_section_data[background_repeat]">
						<option value="repeat"><?php _e('Repeat horizontal and vertical','wproto'); ?></option>
						<option <?php echo $background_repeat == 'repeat-x' ? 'selected="selected"' : ''; ?> value="repeat-x"><?php _e('Horizontal repeat','wproto'); ?></option>
						<option <?php echo $background_repeat == 'repeat-y' ? 'selected="selected"' : ''; ?> value="repeat-y"><?php _e('Vertical repeat','wproto'); ?></option>
						<option <?php echo $background_repeat == 'no-repeat' ? 'selected="selected"' : ''; ?> value="no-repeat"><?php _e('No repeat','wproto'); ?></option>
					</select>
				</label>
			</p>
						
			<p>
			
				<?php
					$background_h_pos = isset( $data['wproto_section_data']['background_h_pos'] ) ? $data['wproto_section_data']['background_h_pos'] : '';
				?>
			
				<label>
					<?php _e('Horizontal background position:', 'wproto'); ?><br />
					<select name="wproto_section_data[background_h_pos]">
						<option value="center"><?php _e('Center','wproto'); ?></option>
						<option <?php echo $background_h_pos == 'left' ? 'selected="selected"' : ''; ?> value="left"><?php _e('Left','wproto'); ?></option>
						<option <?php echo $background_h_pos == 'right' ? 'selected="selected"' : ''; ?> value="right"><?php _e('Right','wproto'); ?></option>
					</select>
				</label>
			</p>
						
			<p>
			
				<?php
					$background_v_pos = isset( $data['wproto_section_data']['background_v_pos'] ) ? $data['wproto_section_data']['background_v_pos'] : '';
				?>
			
				<label>
					<?php _e('Vertical background position:', 'wproto'); ?><br />
					<select name="wproto_section_data[background_v_pos]">
						<option value="center"><?php _e('Center','wproto'); ?></option>
						<option <?php echo $background_v_pos == 'top' ? 'selected="selected"' : ''; ?> value="top"><?php _e('Top','wproto'); ?></option>
						<option <?php echo $background_v_pos == 'bottom' ? 'selected="selected"' : ''; ?> value="bottom"><?php _e('Bottom','wproto'); ?></option>
					</select>
				</label>
			</p>						
						
		</td>
	</tr>
	<tr>
		<th><label for="wproto_section_data-parallax_speed"><?php _e( 'Parallax speed', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_data-parallax_speed" name="wproto_section_data[parallax_speed]" type="number" min="1" max="100" value="<?php echo isset( $data['wproto_section_data']['parallax_speed'] ) ? $data['wproto_section_data']['parallax_speed'] : 20; ?>" />
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto_section_content-title"><?php _e( 'Section title (optional)', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_content-title" name="wproto_section_content[title]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_content']['title'] ) ? $data['wproto_section_content']['title'] : ''; ?>" />
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto-section-editor-before-text"><?php _e( 'Section text (optional)', 'wproto' ); ?>:</label></th>
		<td>
		
		<?php
			$content = isset( $data['wproto_section_content']['before_text'] ) ? $data['wproto_section_content']['before_text'] : '';
			wp_editor(
				stripslashes( str_replace( '\'', "&#39;", $content ) ),
				'wproto-section-editor-before-text',
				array(
					'media_buttons' => false,
					'textarea_name' => 'wproto_section_content[before_text]',
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
	<tr>
		<th><label><?php _e( 'Display call to action button after text?', 'wproto' ); ?>:</label></th>
		<td>
		
			<?php
				$display_button = isset( $data['wproto_section_data']['display_call_to_action_button'] ) ? $data['wproto_section_data']['display_call_to_action_button'] : 'no';
			?>
		
			<div class="field switch">
				<label class="cb-enable <?php echo $display_button == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
				<label class="cb-disable <?php echo $display_button == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
				<input data-toggle-element="tr.wproto-button-controls" name="wproto_section_data[display_call_to_action_button]" type="hidden" value="<?php echo $display_button; ?>" />
				<div class="clear"></div>
			</div>
		
		</td>
	</tr>
	<tr class="wproto-button-controls" style="<?php echo $display_button != 'yes' ? 'display: none' : ''; ?>">
		<th><label for="wproto_section_data-button-title"><?php _e( 'Button text', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_data-button-title" name="wproto_section_data[button_text]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_data']['button_text'] ) ? $data['wproto_section_data']['button_text'] : __('Take a tour', 'wproto'); ?>" />
		
		</td>
	</tr>
	<tr class="wproto-button-controls" style="<?php echo $display_button != 'yes' ? 'display: none' : ''; ?>">
		<th><label for="wproto_section_data-button_link"><?php _e( 'Button link', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_data-button_link" name="wproto_section_data[button_link]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_data']['button_link'] ) ? $data['wproto_section_data']['button_link'] : ''; ?>" />
		
		</td>
	</tr>
	<tr>
		<th><label><?php _e( 'Display subscribe form?', 'wproto' ); ?>:</label></th>
		<td>
		
			<?php
				$display_subscribe_form = isset( $data['wproto_section_data']['display_subscribe_form'] ) ? $data['wproto_section_data']['display_subscribe_form'] : 'no';
			?>
		
			<div class="field switch">
				<label class="cb-enable <?php echo $display_subscribe_form == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
				<label class="cb-disable <?php echo $display_subscribe_form == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
				<input data-toggle-element="#parallax-mailchimp-form" name="wproto_section_data[display_subscribe_form]" type="hidden" value="<?php echo $display_subscribe_form; ?>" />
				<div class="clear"></div>
			</div>
			
			<div id="parallax-mailchimp-form" style="<?php echo $display_subscribe_form == 'no' ? 'display: none;' : ''; ?>">
						
				<p>
					<label><?php _e('Form action', 'wproto'); ?>:<br />
					<input class="text" placeholder="<?php _e('Enter MailChimp form action', 'wproto'); ?>" type="text" name="wproto_section_data[sf_action]" value="<?php echo isset( $data['wproto_section_data']['sf_action'] ) ? $data['wproto_section_data']['sf_action'] : ''; ?>" /></label>
				</p>
							
				<p>
					<label><?php _e('User ID', 'wproto'); ?>:<br />
					<input class="text" placeholder="<?php _e('Enter MailChimp user ID', 'wproto'); ?>" type="text" name="wproto_section_data[sf_user_id]" value="<?php echo isset( $data['wproto_section_data']['sf_user_id'] ) ? $data['wproto_section_data']['sf_user_id'] : ''; ?>" /></label>
				</p>
							
				<p>
					<label><?php _e('List ID', 'wproto'); ?>:<br />
					<input class="text" placeholder="<?php _e('Enter MailChimp list ID', 'wproto'); ?>" type="text" name="wproto_section_data[sf_list_id]" value="<?php echo isset( $data['wproto_section_data']['sf_list_id'] ) ? $data['wproto_section_data']['sf_list_id'] : ''; ?>" /></label>
				</p>
							
				<p>
					<label><?php _e('"Your name" Input name', 'wproto'); ?>:<br />
					<input class="text" placeholder="<?php _e('Enter MailChimp \'Your name\' input name', 'wproto'); ?>" type="text" name="wproto_section_data[sf_name_id]" value="<?php echo isset( $data['wproto_section_data']['sf_name_id'] ) ? $data['wproto_section_data']['sf_name_id'] : ''; ?>" /></label>
				</p>
				
				<p>
					<label><?php _e('"Your phone" Input name', 'wproto'); ?>:<br />
					<input class="text" placeholder="<?php _e('Enter MailChimp \'Your phone\' input name', 'wproto'); ?>" type="text" name="wproto_section_data[sf_phone_id]" value="<?php echo isset( $data['wproto_section_data']['sf_phone_id'] ) ? $data['wproto_section_data']['sf_phone_id'] : ''; ?>" /></label>
				</p>
				
				<p>
					<label><?php _e('"Your email" Input name', 'wproto'); ?>:<br />
					<input class="text" placeholder="<?php _e('Enter MailChimp \'Your email\' input name', 'wproto'); ?>" type="text" name="wproto_section_data[sf_email_id]" value="<?php echo isset( $data['wproto_section_data']['sf_email_id'] ) ? $data['wproto_section_data']['sf_email_id'] : ''; ?>" /></label>
				</p>
						
			</div>
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto-tabbed"><?php _e( 'Custom CSS for parallax section', 'wproto' ); ?>:</label></th>
		<td>
		
			<textarea style="width: 100%" rows="4" id="wproto-tabbed" name="wproto_section_data[custom_css]"><?php echo isset( $data['wproto_section_data']['custom_css'] ) ? stripslashes($data['wproto_section_data']['custom_css']) : ''; ?></textarea>
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto_section_data-menu_title"><?php _e( 'Menu title (fot one-page template)', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_data-menu_title" name="wproto_section_data[menu_title]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_data']['menu_title'] ) ? $data['wproto_section_data']['menu_title'] : ''; ?>" />
		
		</td>
	</tr>
</table>