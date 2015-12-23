<?php echo $data['args']['before_widget']; ?>

<!-- widget title -->
<?php if ( isset( $data['title'] ) ) : ?>

	<?php echo $data['args']['before_title']; ?>
	
		<?php echo $data['title']; ?>
		
	<?php echo $data['args']['after_title']; ?>
	
<?php endif; ?>

<!-- widget content -->

<?php if( isset( $data['instance']['text'] ) && $data['instance']['text'] <> '' ): ?>
	<p><?php echo $data['instance']['text']; ?></p>
<?php endif; ?>

<?php global $wpl_galaxy_wp; $id = uniqid(); ?>
<form class="wproto-contact-form" id="wproto-contact-form-<?php echo $id; ?>" action="javascript:;" method="post">
	<fieldset>
		<input type="hidden" name="to" value="<?php echo ( isset( $data['instance']['recipient_email'] ) ? $data['instance']['recipient_email'] : get_option('admin_email') ); ?>" />
		<input type="hidden" name="subject" value="<?php echo ( isset( $data['instance']['email_subject'] ) ? $data['instance']['email_subject'] : __('Feedback from website', 'wproto') ); ?>" />
		<input type="hidden" name="wproto_form_id" value="<?php echo $data['instance']['wproto_form_id']; ?>" />
		<input type="hidden" name="from_widget" value="<?php echo $data['args']['widget_id']; ?>" />
		<p>
			<!--<label for="wptoto-contact-form-input-name-<?php echo $id; ?>"></label>-->
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
			<?php if( isset( $data['instance']['enable_captcha'] ) && $data['instance']['enable_captcha'] == 'yes' ): ?>
				<?php $wpl_galaxy_wp->controller->captcha->generate_captcha_phrase(); ?>
			<?php endif; ?>
			<input type="submit" value="<?php _e( 'Submit', 'wproto'); ?>" />
		</p>
	</fieldset>
</form>

<?php echo $data['args']['after_widget'];