
<h2><?php _e('Contact form &amp; Map', 'wproto'); ?></h2>

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
		<th><label for="wproto_section_data-menu_title"><?php _e( 'Menu title (fot one-page template)', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_data-menu_title" name="wproto_section_data[menu_title]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_data']['menu_title'] ) ? $data['wproto_section_data']['menu_title'] : ''; ?>" />
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto_section_data-address"><?php _e( 'Address', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_data-address" name="wproto_section_data[address]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_data']['address'] ) ? $data['wproto_section_data']['address'] : ''; ?>" />
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto_section_data-phone"><?php _e( 'Phone', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_data-phone" name="wproto_section_data[phone]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_data']['phone'] ) ? $data['wproto_section_data']['phone'] : ''; ?>" />
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto_section_data-email"><?php _e( 'E-mail', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_data-email" name="wproto_section_data[email]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_data']['email'] ) ? $data['wproto_section_data']['email'] : ''; ?>" />
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto_section_data-working_hours"><?php _e( 'Working Hours', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_data-working_hours" name="wproto_section_data[working_hours]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_data']['working_hours'] ) ? $data['wproto_section_data']['working_hours'] : ''; ?>" />
		
		</td>
	</tr>
</table>