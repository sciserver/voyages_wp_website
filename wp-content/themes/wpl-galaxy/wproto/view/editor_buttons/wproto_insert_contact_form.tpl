<input type="hidden" id="wproto-insert-contact-form-formid" value="<?php echo uniqid(); ?>" />
<p>
	<label for="wproto-insert-contact-recipient-email"><?php _e( 'Recipient email', 'wproto' ); ?>: </label> <br />
	<input value="<?php echo @$data['settings']['to'] == '' ? get_option('admin_email') : @$data['settings']['to']; ?>" class="full-width-input" type="email" id="wproto-insert-contact-recipient-email" />
</p>
<p>
	<label for="wproto-insert-contact-form-subject"><?php _e( 'Email subject', 'wproto' ); ?>: </label> <br />
	<input value="<?php echo @$data['settings']['subject'] == '' ? __( 'Feedback from website', 'wproto') : @$data['settings']['subject']; ?>" class="full-width-input" type="text" id="wproto-insert-contact-form-subject" />
</p>
<p>
	<label for="wproto-insert-contact-form-title"><?php _e( 'Title', 'wproto' ); ?>: </label> <br />
	<input value="<?php echo @$data['settings']['title']; ?>" class="full-width-input" type="text" id="wproto-insert-contact-form-title" />
</p>
<p>
	<label for="wproto-insert-contact-form-text"><?php _e( 'Text', 'wproto' ); ?>: </label> 
	<textarea class="full-width-textarea" style="height: 100px" id="wproto-insert-contact-form-text"><?php echo @$data['settings']['text']; ?></textarea>
</p>
<p>
	<label><input type="checkbox" value="yes" id="wproto-insert-contact-form-captcha" <?php echo @$data['settings']['captcha'] == 'yes' ? 'checked="checked"' : ''; ?> /> <?php _e( 'Enable captcha', 'wproto' ); ?></label>
</p>