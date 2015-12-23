<?php
	global $wproto_section, $wpl_galaxy_wp;
	$section_data = isset( $wproto_section->data ) ? unserialize( $wproto_section->data ) : array();
	
	$background = isset( $section_data['background'] ) ? $section_data['background'] : '';
	$background_repeat = isset( $section_data['background_repeat'] ) ? $section_data['background_repeat'] : '';
	$background_h_pos = isset( $section_data['background_h_pos'] ) ? $section_data['background_h_pos'] : '';
	$background_v_pos = isset( $section_data['background_v_pos'] ) ? $section_data['background_v_pos'] : '';
	$parallax_speed = isset( $section_data['parallax_speed'] ) ? absint( $section_data['parallax_speed'] ) : 20;
	$parallax_speed = $parallax_speed == 0 ? 20 : $parallax_speed;
	
	$call_to_action = isset( $section_data['display_call_to_action_button'] ) ? $section_data['display_call_to_action_button'] : 'no';
	
	$section_id = uniqid();
	
?>
<!--
					
	PARALLAX
						
-->
<section id="section-id-<?php echo $wproto_section->ID; ?>" class="parallax" data-parallax-speed="<?php echo $parallax_speed; ?>"></section>
<section class="parallax-content">
	<div class="wrapper">
		<?php if( $wproto_section->title <> '' ): ?>
		<div>
			<h1><?php echo $wproto_section->title; ?></h1>
		</div>
		<?php endif; ?>
		
		<?php echo apply_filters( 'the_content', $wproto_section->before_text ); ?>
		
		<?php if( $call_to_action == 'yes' ): ?>
		<div>
			<a href="<?php echo isset( $section_data['button_link'] ) ? $section_data['button_link'] : ''; ?>" class="call-to-action-btn button"><?php echo isset( $section_data['button_text'] ) ? $section_data['button_text'] : ''; ?></a>
		</div>
		<?php endif; ?>
		
		<?php if( isset( $section_data['display_subscribe_form'] ) && $section_data['display_subscribe_form'] == 'yes' ): ?>
		
		<?php
			$action = isset( $section_data['sf_action'] ) ? $section_data['sf_action'] : '';
			$user_id = isset( $section_data['sf_user_id'] ) ? $section_data['sf_user_id'] : '';
			$list_id = isset( $section_data['sf_list_id'] ) ? $section_data['sf_list_id'] : '';
			$i_name = isset( $section_data['sf_name_id'] ) ? $section_data['sf_name_id'] : '';
			$i_phone = isset( $section_data['sf_phone_id'] ) ? $section_data['sf_phone_id'] : '';
			$i_email = isset( $section_data['sf_email_id'] ) ? $section_data['sf_email_id'] : '';
		?>
		
		<form class="inputs" action="<?php echo $action; ?>" method="post">
					
			<input type="hidden" name="u" value="<?php echo $user_id; ?>" />
			<input type="hidden" name="id" value="<?php echo $list_id; ?>" />
					
			<input type="text" name="<?php echo $i_name; ?>" placeholder="<?php _e('Your name', 'wproto'); ?>" value="" />
						
			<input type="text" name="<?php echo $i_phone; ?>" placeholder="<?php _e('Your phone number (optional)', 'wproto'); ?>" />
					
			<input type="email" name="<?php echo $i_email; ?>" placeholder="<?php _e('Your email', 'wproto'); ?>" />
						
			<input type="submit" value="<?php _e('Subscribe', 'wproto'); ?>" />
					
		</form>
		<?php endif; ?>
		
		<style type="text/css">
		
		#section-id-<?php echo $wproto_section->ID; ?> {
			background: url(<?php echo $background; ?>) <?php echo $background_h_pos; ?> <?php echo $background_v_pos; ?> <?php echo $background_repeat; ?> fixed;
		}
		
		<?php echo stripslashes($section_data['custom_css']); ?>
		</style>
	</div>
</section>