
<h2><?php _e('Products section', 'wproto'); ?></h2>

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
		<th><label for="wproto_section_data-section_style"><?php _e( 'Section style', 'wproto' ); ?>:</label></th>
		
		<td>
		
			<?php
				$section_style = isset( $data['wproto_section_data']['section_style'] ) ? $data['wproto_section_data']['section_style'] : 'style_1';
			?>
		
			<p>
				<label><input type="radio" <?php echo $section_style == 'style_1' ? 'checked="checked"' : ''; ?> name="wproto_section_data[section_style]" value="style_1" /> <?php _e( 'Display "Best ratings", "Reviews on our blog" and "Best sellers"', 'wproto' ); ?></label> <br />
				<label><input type="radio" <?php echo $section_style == 'style_2' ? 'checked="checked"' : ''; ?> name="wproto_section_data[section_style]" value="style_2" /> <?php _e( 'Display "New arrivals"', 'wproto' ); ?></label> <br />
				<label><input type="radio" <?php echo $section_style == 'style_3' ? 'checked="checked"' : ''; ?> name="wproto_section_data[section_style]" value="style_3" /> <?php _e( 'Display "Best sellers"', 'wproto' ); ?></label> <br />
			</p>
		
		</td>
		
	</tr>
	<tr>
		<th><label for="wproto_section_data-menu_title"><?php _e( 'Menu title (fot one-page template)', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_data-menu_title" name="wproto_section_data[menu_title]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_data']['menu_title'] ) ? $data['wproto_section_data']['menu_title'] : ''; ?>" />
		
		</td>
	</tr>
</table>