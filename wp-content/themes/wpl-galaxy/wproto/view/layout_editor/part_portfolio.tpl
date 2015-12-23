
<h2><?php _e('Portfolio section', 'wproto'); ?></h2>

<table class="form-table wproto-form-table">
	<tr>
		<th><label for="wproto_section_content-title"><?php _e( 'Section title (optional)', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_content-title" name="wproto_section_content[title]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_content']['title'] ) ? $data['wproto_section_content']['title'] : ''; ?>" />
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto_section_content-subtitle"><?php _e( 'Section subtitle (optional)', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_content-subtitle" name="wproto_section_content[subtitle]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_content']['subtitle'] ) ? $data['wproto_section_content']['subtitle'] : ''; ?>" />
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto-section-editor-before-text"><?php _e( 'Text after subtitle (optional)', 'wproto' ); ?>:</label></th>
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
		<th><label for="wproto-section-editor-after-text"><?php _e( 'Text after portfolio filter (optional)', 'wproto' ); ?>:</label></th>
		<td>
		
		<?php
			$content = isset( $data['wproto_section_content']['after_text'] ) ? $data['wproto_section_content']['after_text'] : '';
			wp_editor(
				stripslashes( str_replace( '\'', "&#39;", $content ) ),
				'wproto-section-editor-after-text',
				array(
					'media_buttons' => false,
					'textarea_name' => 'wproto_section_content[after_text]',
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
		<th><label for="wproto_section_data-menu_title"><?php _e( 'Menu title (fot one-page template)', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_data-menu_title" name="wproto_section_data[menu_title]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_data']['menu_title'] ) ? $data['wproto_section_data']['menu_title'] : ''; ?>" />
		
		</td>
	</tr>
</table>