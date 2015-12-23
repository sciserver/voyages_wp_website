
<h2><?php _e('Subscribe form section', 'wproto'); ?></h2>

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
		<th>
			<label for="wproto_section_data-form_action"><?php _e( 'Form action', 'wproto' ); ?>:</label>
			<p class="description"><?php _e( sprintf( 'Read more about <a target="_blank" href="%s">MailChimp forms</a>', 'http://kb.mailchimp.com/article/can-i-host-my-own-sign-up-forms/' ), 'wproto' ); ?></p>
		</th>
		<td>
		
			<input type="text" value="<?php echo isset( $data['wproto_section_data']['form_action'] ) ? $data['wproto_section_data']['form_action'] : ''; ?>" class="text" id="wproto_section_data-form_action" name="wproto_section_data[form_action]" placeholder="<?php _e('Enter MailChimp form action', 'wproto'); ?>" />
		
		</td>
	</tr>
	<tr>
		<th>
			<label for="wproto_section_data-user_id"><?php _e( 'Mail Chimp User ID', 'wproto' ); ?>:</label>
		</th>
		<td>
		
			<input type="text" value="<?php echo isset( $data['wproto_section_data']['user_id'] ) ? $data['wproto_section_data']['user_id'] : ''; ?>" class="text" id="wproto_section_data-user_id" name="wproto_section_data[user_id]" placeholder="<?php _e('Enter MailChimp User ID', 'wproto'); ?>" />
		
		</td>
	</tr>
	<tr>
		<th>
			<label for="wproto_section_data-list_id"><?php _e( 'Mail Chimp List ID', 'wproto' ); ?>:</label>
		</th>
		<td>
		
			<input type="text" value="<?php echo isset( $data['wproto_section_data']['list_id'] ) ? $data['wproto_section_data']['list_id'] : ''; ?>" class="text" id="wproto_section_data-list_id" name="wproto_section_data[list_id]" placeholder="<?php _e('Enter MailChimp List ID', 'wproto'); ?>" />
		
		</td>
	</tr>
	<tr>
		<th>
			<label for="wproto_section_data-name_id"><?php _e( '"Your name" input name', 'wproto' ); ?>:</label>
		</th>
		<td>
		
			<input type="text" value="<?php echo isset( $data['wproto_section_data']['name_id'] ) ? $data['wproto_section_data']['name_id'] : ''; ?>" class="text" id="wproto_section_data-name_id" name="wproto_section_data[name_id]" placeholder="<?php _e('Enter \'Your name\' input name', 'wproto'); ?>" />
		
		</td>
	</tr>
	<tr>
		<th>
			<label for="wproto_section_data-phone_id"><?php _e( '"Your phone" input name', 'wproto' ); ?>:</label>
		</th>
		<td>
		
			<input type="text" value="<?php echo isset( $data['wproto_section_data']['phone_id'] ) ? $data['wproto_section_data']['phone_id'] : ''; ?>" class="text" id="wproto_section_data-phone_id" name="wproto_section_data[phone_id]" placeholder="<?php _e('Enter \'Your phone\' input name', 'wproto'); ?>" />
		
		</td>
	</tr>
	<tr>
		<th>
			<label for="wproto_section_data-email_id"><?php _e( '"Your email" input name', 'wproto' ); ?>:</label>
		</th>
		<td>
		
			<input type="text" value="<?php echo isset( $data['wproto_section_data']['email_id'] ) ? $data['wproto_section_data']['email_id'] : ''; ?>" class="text" id="wproto_section_data-email_id" name="wproto_section_data[email_id]" placeholder="<?php _e('Enter \'Your email\' input name', 'wproto'); ?>" />
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto_section_data-menu_title"><?php _e( 'Menu title (fot one-page template)', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_data-menu_title" name="wproto_section_data[menu_title]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_data']['menu_title'] ) ? $data['wproto_section_data']['menu_title'] : ''; ?>" />
		
		</td>
	</tr>
</table>