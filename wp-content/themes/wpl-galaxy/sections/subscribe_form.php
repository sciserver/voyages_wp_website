<?php
	global $wproto_section, $wpl_galaxy_wp;
	$section_data = isset( $wproto_section->data ) ? unserialize( $wproto_section->data ) : array();
	
	$form_action = isset( $section_data['form_action'] ) ? $section_data['form_action'] : '';
	$user_id = isset( $section_data['user_id'] ) ? $section_data['user_id'] : '';
	$list_id = isset( $section_data['list_id'] ) ? $section_data['list_id'] : '';
	$name_id = isset( $section_data['name_id'] ) ? $section_data['name_id'] : '';
	$phone_id = isset( $section_data['phone_id'] ) ? $section_data['phone_id'] : '';
	$email_id = isset( $section_data['email_id'] ) ? $section_data['email_id'] : '';

?>
<!--
	SUBSCRIBE FORM
-->
<section id="section-id-<?php echo $wproto_section->ID; ?>">
<form class="wrapper subscribe-form" action="<?php echo $form_action; ?>" method="post" data-appear-animation="fadeIn">
		
	<fieldset>
			
		<?php if( $wproto_section->title <> '' ): ?>
		<header class="hgroup">
			<h2><?php echo $wproto_section->title; ?></h2>
			<?php if( $wproto_section->subtitle <> '' ): ?>
			<h5><?php echo $wproto_section->subtitle; ?></h5>
			<?php endif; ?>
		</header>
		<?php endif; ?>
				
		<p>
		
			<input type="hidden" name="u" value="<?php echo $user_id; ?>" />
			<input type="hidden" name="id" value="<?php echo $list_id; ?>" />
		
			<input type="text" name="<?php echo $name_id; ?>" placeholder="<?php _e('Your name', 'wproto'); ?>" />
			
			<input type="text" name="<?php echo $phone_id; ?>" placeholder="<?php _e('Your phone number (optional)', 'wproto'); ?>" />
					
			<input type="email" name="<?php echo $email_id; ?>" placeholder="<?php _e('Your email', 'wproto'); ?>" />
					
			<input type="submit" value="<?php _e('Subscribe', 'wproto'); ?>" />
				
		</p>
			
	</fieldset>
		
</form>
</section>