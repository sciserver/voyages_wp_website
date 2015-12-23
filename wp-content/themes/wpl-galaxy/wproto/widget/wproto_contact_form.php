<?php

	add_action( 'widgets_init', 'register_wpl_galaxy_wp_contact_form_widget' );
	
	function register_wpl_galaxy_wp_contact_form_widget() {
		register_widget( 'wpl_galaxy_wp_contact_form_widget' );
	}
	
	class wpl_galaxy_wp_contact_form_widget extends WP_Widget {
		
		function __construct() {
			$widget_ops = array( 'classname' => 'wproto-contact-form-widget', 'description' => __('A widget that displays the contact form. ', 'wproto') );
		
			$control_ops = array( 'width' => 300, 'height' => 350, 'id_base' => 'wproto-contact-form-widget' );
		
			$this->WP_Widget( 'wproto-contact-form-widget', __( '&laquo;Galaxy&raquo; Contact Form', 'wproto' ), $widget_ops, $control_ops );
		}
		
		function widget( $args, $instance ) {
			global $wpl_galaxy_wp;
			
			$data = array();
			$data['title'] = apply_filters( 'widget_title', $instance['title'] );
			
			$data['instance'] = $instance;
			$data['args'] = $args;
			
			if( $_SERVER['REQUEST_METHOD'] == 'POST' && get_transient( 'wprcf_' . md5( $instance['wproto_form_id'] ) ) == 'ok' ) {
				delete_transient( 'wprcf_' . md5( $instance['wproto_form_id'] ) );
				$data['sent'] = 'ok';
			}
			
			$wpl_galaxy_wp->view->load_partial( 'widgets/contact_form', $data );

		}
		
		function update( $new_instance, $old_instance ) {
			$instance = $old_instance;

			$allowed_tags = wp_kses_allowed_html( 'post' );

			//Strip tags from title and name to remove HTML 
			$instance['title'] = strip_tags( str_replace( '\'', "&#39;", $new_instance['title'] ) );
			$instance['recipient_email'] = isset( $new_instance['recipient_email'] ) ? strip_tags( $new_instance['recipient_email'] ) : '';
			$instance['email_subject'] =  wp_kses( $new_instance['email_subject'], $allowed_tags );
			$instance['text'] = wp_kses( str_replace( '\'', "&#39;", $new_instance['text'] ), $allowed_tags );
			$instance['wproto_form_id'] = isset( $new_instance['wproto_form_id'] ) ? strip_tags( $new_instance['wproto_form_id'] ) : '';
			$instance['enable_captcha'] = isset( $new_instance['enable_captcha'] ) ? 'yes' : 'no';

			return $instance;
		}
		
		function form( $instance ) {
			
			//Set up some default widget settings.
			$defaults = array(
				'title' => __( 'Contact Us', 'wproto' ),
				'recipient_email' => '',
				'email_subject' => '',
				'text' => '',
				'enable_captcha' => 'yes',
				'wproto_form_id' => $this->id
			);
			
			$instance = wp_parse_args( (array) $instance, $defaults );
			
			?>
			<input type="hidden" id="<?php echo $this->get_field_id( 'wproto_form_id' ); ?>" name="<?php echo $this->get_field_name( 'wproto_form_id' ); ?>" value="<?php echo $instance['wproto_form_id']; ?>" />
			<p>
				<label for="<?php echo $this->get_field_id( 'title' ); ?>"><?php _e('Widget title:', 'wproto'); ?></label>
				<input class="widefat" type="text" id="<?php echo $this->get_field_id( 'title' ); ?>" name="<?php echo $this->get_field_name( 'title' ); ?>" value="<?php echo $instance['title']; ?>" />
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'recipient_email' ); ?>"><?php _e('Recipient Email:', 'wproto'); ?></label>
				<input class="widefat" type="text" name="<?php echo $this->get_field_name( 'recipient_email' ); ?>" id="<?php echo $this->get_field_id( 'recipient_email' ); ?>" value="<?php echo $instance['recipient_email']; ?>" />
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'email_subject' ); ?>"><?php _e('Email Subject:', 'wproto'); ?></label>
				<input class="widefat" type="text" name="<?php echo $this->get_field_name( 'email_subject' ); ?>" id="<?php echo $this->get_field_id( 'email_subject' ); ?>" value="<?php echo $instance['email_subject']; ?>" />
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'text' ); ?>"><?php _e('Text (optional):', 'wproto'); ?></label>
				<textarea class="widefat" name="<?php echo $this->get_field_name( 'text' ); ?>" id="<?php echo $this->get_field_id( 'text' ); ?>"><?php echo $instance['text']; ?></textarea>
			</p>
			<p>
				<input class="checkbox" value="yes" type="checkbox" <?php echo $instance['enable_captcha'] == 'yes' ? 'checked="checked"' : ''; ?> id="<?php echo $this->get_field_id( 'enable_captcha' ); ?>" name="<?php echo $this->get_field_name( 'enable_captcha' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'enable_captcha' ); ?>"><?php _e('Enable captcha', 'wproto'); ?></label>  
			</p>
			<?php
		}
		
	}