
<h2><?php _e('Text section', 'wproto'); ?></h2>

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
		<th><label for="wproto-section-editor-before-text"><?php _e( 'Section text', 'wproto' ); ?>:</label></th>
		<td>
		
		<?php
			$content = isset( $data['wproto_section_content']['before_text'] ) ? $data['wproto_section_content']['before_text'] : '';
			wp_editor(
				stripslashes( str_replace( '\'', "&#39;", $content ) ),
				'wproto-section-editor-before-text',
				array(
					'media_buttons' => true,
					'textarea_name' => 'wproto_section_content[before_text]',
					'textarea_rows' => 20,
					'quicktags' => true
				)
			);
		?>
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto_section_data-menu_title"><?php _e( 'Menu title (fot one-page template)', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_data-menu_title" name="wproto_section_data[menu_title]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_data']['menu_title'] ) ? $data['wproto_section_data']['menu_title'] : ''; ?>" />
		
		</td>
	</tr>
</table>