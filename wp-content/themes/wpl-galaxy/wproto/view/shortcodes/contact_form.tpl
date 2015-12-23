<?php global $wpl_galaxy_wp; $id = uniqid(); ?>
<?php if( isset( $data['title'] ) && $data['title'] <> '' ): ?>
	<h4><?php echo $data['title']; ?></h4>
<?php endif; ?>
<?php if( isset( $data['text'] ) && $data['text'] <> '' ): ?>
	<p><?php echo $data['text']; ?></p>
<?php endif; ?>
<form class="wproto-contact-form" id="wproto-contact-form-<?php echo $id; ?>" action="javascript:;" method="post">
	<fieldset>
		<input type="hidden" name="to" value="<?php echo ( isset( $data['to'] ) ? $data['to'] : get_option('admin_email') ); ?>" />
		<input type="hidden" name="subject" value="<?php echo ( isset( $data['subject'] ) ? $data['subject'] : __('Feedback from website', 'wproto') ); ?>" />
		<input type="hidden" name="wproto_form_id" value="<?php echo $data['form_id']; ?>" />
		<p>
			<!--<label for="wptoto-contact-form-input-name-<?php echo $id; ?>"><?php _e( 'Name', 'wproto'); ?></label>-->
			<input placeholder="<?php _e( 'Your name', 'wproto'); ?>" id="wptoto-contact-form-input-name-<?php echo $id; ?>" type="text" name="name" value="" class="wproto-contact-form-name-input" />
		</p>
		<p>
			<!--<label for="wptoto-contact-form-input-email-<?php echo $id; ?>"><?php _e( 'E-mail', 'wproto'); ?></label>-->
			<input placeholder="<?php _e( 'Email address', 'wproto'); ?>" id="wptoto-contact-form-input-email-<?php echo $id; ?>" name="email" type="email" value="" class="wproto-contact-form-email-input" />
		</p>
		<p>
			<!--<label for="wptoto-contact-form-input-message-<?php echo $id; ?>"><?php _e( 'Message', 'wproto'); ?></label>-->
			<textarea placeholder="<?php _e( 'Message', 'wproto'); ?>" id="wptoto-contact-form-input-message-<?php echo $id; ?>" class="wproto-contact-form-message-input" name="message"></textarea>
		</p>
		<p>
			<span class="captcha">
			<?php if( isset( $data['captcha'] ) && $data['captcha'] == 'yes' ): ?>
				<?php $wpl_galaxy_wp->controller->captcha->generate_captcha_phrase(); ?>
			<?php endif; ?>
			</span>
			<input type="submit" value="<?php _e( 'Submit', 'wproto'); ?>" />
		</p>
	</fieldset>
</form>
