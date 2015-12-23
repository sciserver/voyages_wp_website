<?php
	$wproto_tpl_contact_email_to = isset( $data['wproto_tpl_contact_email_to'] ) ? $data['wproto_tpl_contact_email_to'] : get_bloginfo('admin_email');
	$wproto_tpl_contact_success_text = isset( $data['wproto_tpl_contact_success_text'] ) ? $data['wproto_tpl_contact_success_text'] : __('Message was sent! Thank you!', 'wproto');
	$wproto_tpl_contact_address = isset( $data['wproto_tpl_contact_address'] ) ? $data['wproto_tpl_contact_address'] : '';
	$wproto_tpl_contact_phone = isset( $data['wproto_tpl_contact_phone'] ) ? $data['wproto_tpl_contact_phone'] : '';
	$wproto_tpl_contact_fax = isset( $data['wproto_tpl_contact_fax'] ) ? $data['wproto_tpl_contact_fax'] : '';
	$wproto_tpl_contact_display_captcha = isset( $data['wproto_tpl_contact_display_captcha'] ) ? $data['wproto_tpl_contact_display_captcha'] : 'yes';
	$wproto_tpl_contact_display_social = isset( $data['wproto_tpl_contact_display_social'] ) ? $data['wproto_tpl_contact_display_social'] : 'yes';
	
	$wproto_tpl_contact_google_img = isset( $data['wproto_tpl_contact_google_img'] ) ? $data['wproto_tpl_contact_google_img'] : '';
	//$wproto_tpl_contact_google_img_2x = isset( $data['wproto_tpl_contact_google_img_2x'] ) ? $data['wproto_tpl_contact_google_img_2x'] : '';
	
	$wproto_tpl_contact_google_pointer_img = isset( $data['wproto_tpl_contact_google_pointer_img'] ) ? $data['wproto_tpl_contact_google_pointer_img'] : '';
	//$wproto_tpl_contact_google_pointer_img_2x = isset( $data['wproto_tpl_contact_google_pointer_img_2x'] ) ? $data['wproto_tpl_contact_google_pointer_img_2x'] : '';
	
	$wproto_tpl_contact_display_map_zoom = isset( $data['wproto_tpl_contact_display_map_zoom'] ) ? $data['wproto_tpl_contact_display_map_zoom'] : 10;
	$wproto_tpl_contact_display_map_draggable = isset( $data['wproto_tpl_contact_display_map_draggable'] ) ? $data['wproto_tpl_contact_display_map_draggable'] : 'yes';
	$wproto_tpl_contact_display_map_zoom_control = isset( $data['wproto_tpl_contact_display_map_zoom_control'] ) ? $data['wproto_tpl_contact_display_map_zoom_control'] : 'no';
?>

<table class="form-table wproto-form-table">
	<tr>
		<th><label for="wproto_tpl_contact_email_to"><?php _e( 'Your E-mail (to:)', 'wproto' ); ?>:</label></th>
		<td>
		
			<input type="email" class="text" id="wproto_tpl_contact_email_to" value="<?php echo $wproto_tpl_contact_email_to; ?>" name="wproto_settings[wproto_tpl_contact_email_to]" />
		
		</td>
	</tr>
	<tr>
		<th><label><?php _e( 'Success text message', 'wproto' ); ?>:</label></th>
		<td>
		
			<?php
				wp_editor(
					$wproto_tpl_contact_success_text,
					'wproto-maintenance-page-text-editor',
					array(
						'media_buttons' => false,
						'textarea_name' => 'wproto_settings[wproto_tpl_contact_success_text]',
						'textarea_rows' => 8,
						'tabindex' => 4,
						'teeny' => true,
						'quicktags' => false,
						'tinymce' => array(
							'theme_advanced_buttons1' => 'bold, italic',
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
		<th><label for="wproto_tpl_contact_address"><?php _e( 'Address', 'wproto' ); ?>:</label></th>
		<td>
		
			<textarea class="textarea" rows="4" id="wproto_tpl_contact_address" name="wproto_settings[wproto_tpl_contact_address]"><?php echo esc_textarea( $wproto_tpl_contact_address ); ?></textarea>
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto_tpl_contact_phone"><?php _e( 'Phone', 'wproto' ); ?>:</label></th>
		<td>
		
			<input class="text" type="text" id="wproto_tpl_contact_phone" value="<?php echo $wproto_tpl_contact_phone; ?>" name="wproto_settings[wproto_tpl_contact_phone]" />
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto_tpl_contact_fax"><?php _e( 'Fax', 'wproto' ); ?>:</label></th>
		<td>
		
			<input class="text" type="text" id="wproto_tpl_contact_fax" value="<?php echo $wproto_tpl_contact_fax; ?>" name="wproto_settings[wproto_tpl_contact_fax]" />
		
		</td>
	</tr>
	<tr>
		<th style="vertical-align: middle"><label><?php _e( 'Display captcha', 'wproto' ); ?>:</label></th>
		<td>
		
			<div class="field switch">
				<label class="cb-enable <?php echo $wproto_tpl_contact_display_captcha == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
				<label class="cb-disable <?php echo $wproto_tpl_contact_display_captcha == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
				<input name="wproto_settings[wproto_tpl_contact_display_captcha]" type="hidden" value="<?php echo $wproto_tpl_contact_display_captcha; ?>" />
				<div class="clear"></div>
			</div>
		
		</td>
	</tr>
	<tr>
		<th style="vertical-align: middle"><label><?php _e( 'Display social icons', 'wproto' ); ?>:</label></th>
		<td>
		
			<div class="field switch">
				<label class="cb-enable <?php echo $wproto_tpl_contact_display_social == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
				<label class="cb-disable <?php echo $wproto_tpl_contact_display_social == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
				<input name="wproto_settings[wproto_tpl_contact_display_social]" type="hidden" value="<?php echo $wproto_tpl_contact_display_social; ?>" />
				<div class="clear"></div>
			</div>
		
		</td>
	</tr>
	<tr>
		<th><label><?php _e( 'Custom google map logo', 'wproto' ); ?>:</label></th>
		<td>
		
			<p>
				<label><?php _e('Choose an image:', 'wproto'); ?><br />
				<input type="text" id="wproto_tpl_contact_google_img" class="text" name="wproto_settings[wproto_tpl_contact_google_img]" value="<?php echo $wproto_tpl_contact_google_img; ?>" /> <a href="javascript:;" class="button wproto-image-selector" data-url-input="#wproto_tpl_contact_google_img"><?php _e( 'Upload', 'wproto' ); ?></a> 
				<a href="javascript:;" data-url-input="#wproto_tpl_contact_google_img" class="button wproto-image-remover"><?php _e( 'Remove', 'wproto' ); ?></a></label>
			</p>
		
		</td>
	</tr>
	<tr>
		<th><label><?php _e( 'Custom google map pointer', 'wproto' ); ?>:</label></th>
		<td>
		
			<p>
				<label><?php _e('Choose an image:', 'wproto'); ?><br />
				<input type="text" id="wproto_tpl_contact_google_pointer_img" class="text" name="wproto_settings[wproto_tpl_contact_google_pointer_img]" value="<?php echo $wproto_tpl_contact_google_pointer_img; ?>" /> <a href="javascript:;" class="button wproto-image-selector" data-url-input="#wproto_tpl_contact_google_pointer_img"><?php _e( 'Upload', 'wproto' ); ?></a> 
				<a href="javascript:;" data-url-input="#wproto_tpl_contact_google_pointer_img" class="button wproto-image-remover"><?php _e( 'Remove', 'wproto' ); ?></a></label>
			</p>
		
		</td>
	</tr>
	<tr>
		<th><label><?php _e( 'Map zoom', 'wproto' ); ?>:</label></th>
		<td>
		
			<input type="number" name="wproto_settings[wproto_tpl_contact_display_map_zoom]" value="<?php echo $wproto_tpl_contact_display_map_zoom; ?>" />
		
		</td>
	</tr>
	<tr>
		<th><label><?php _e( 'Map draggable', 'wproto' ); ?>:</label></th>
		<td>
		
			<div class="field switch">
				<label class="cb-enable <?php echo $wproto_tpl_contact_display_map_draggable == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
				<label class="cb-disable <?php echo $wproto_tpl_contact_display_map_draggable == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
				<input name="wproto_settings[wproto_tpl_contact_display_map_draggable]" type="hidden" value="<?php echo $wproto_tpl_contact_display_map_draggable; ?>" />
				<div class="clear"></div>
			</div>
		
		</td>
	</tr>
	<tr>
		<th><label><?php _e( 'Map Zoom Control', 'wproto' ); ?>:</label></th>
		<td>
		
			<div class="field switch">
				<label class="cb-enable <?php echo $wproto_tpl_contact_display_map_zoom_control == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
				<label class="cb-disable <?php echo $wproto_tpl_contact_display_map_zoom_control == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
				<input name="wproto_settings[wproto_tpl_contact_display_map_zoom_control]" type="hidden" value="<?php echo $wproto_tpl_contact_display_map_zoom_control; ?>" />
				<div class="clear"></div>
			</div>
		
		</td>
	</tr>
</table>