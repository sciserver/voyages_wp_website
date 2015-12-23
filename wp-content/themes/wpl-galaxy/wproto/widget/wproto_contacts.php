<?php

	add_action( 'widgets_init', 'register_wpl_galaxy_wp_contacts_widget' );
	
	function register_wpl_galaxy_wp_contacts_widget() {
		register_widget( 'wpl_galaxy_wp_contacts_widget' );
	}
	
	class wpl_galaxy_wp_contacts_widget extends WP_Widget {
		
		function __construct() {
			$widget_ops = array( 'classname' => 'wproto-contacts-widget', 'description' => __('A widget that displays your contacts (address, phone, etc.). ', 'wproto') );
		
			$control_ops = array( 'width' => 300, 'height' => 350, 'id_base' => 'wproto-contacts-widget' );
		
			$this->WP_Widget( 'wproto-contacts-widget', __( '&laquo;Galaxy&raquo; Contact Information', 'wproto' ), $widget_ops, $control_ops );
		}
		
		function widget( $args, $instance ) {
			global $wpl_galaxy_wp;
			
			$data = array();
			$data['title'] = apply_filters( 'widget_title', $instance['title'] );
			
			$data['instance'] = $instance;
			$data['args'] = $args;

			$wpl_galaxy_wp->view->load_partial( 'widgets/contacts', $data );

		}
		
		function update( $new_instance, $old_instance ) {
			$instance = $old_instance;

			//Strip tags from title and name to remove HTML 
			$instance['title'] = strip_tags( str_replace( '\'', "&#39;", $new_instance['title'] ) );
			$instance['free_text'] = $new_instance['free_text'];
			$instance['address'] = strip_tags( $new_instance['address'] );
			$instance['phone'] = strip_tags( $new_instance['phone'] );
			$instance['email'] = strip_tags( $new_instance['email'] );

			return $instance;
		}
		
		function form( $instance ) {
			
			//Set up some default widget settings.
			$defaults = array(
				'title' => __( 'Contacts', 'wproto' ),
				'free_text' => '',
				'address' => '',
				'phone' => '',
				'email' => ''
			);
			
			$instance = wp_parse_args( (array) $instance, $defaults );
			
			?>
			<p>
				<label for="<?php echo $this->get_field_id( 'title' ); ?>"><?php _e('Widget title:', 'wproto'); ?></label>
				<input class="widefat" type="text" id="<?php echo $this->get_field_id( 'title' ); ?>" name="<?php echo $this->get_field_name( 'title' ); ?>" value="<?php echo $instance['title']; ?>" />
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'free_text' ); ?>"><?php _e('Free text:', 'wproto'); ?></label>
				<textarea class="widefat" name="<?php echo $this->get_field_name( 'free_text' ); ?>" id="<?php echo $this->get_field_id( 'free_text' ); ?>"><?php echo $instance['free_text']; ?></textarea>
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'address' ); ?>"><?php _e('Address:', 'wproto'); ?></label>
				<textarea class="widefat" name="<?php echo $this->get_field_name( 'address' ); ?>" id="<?php echo $this->get_field_id( 'address' ); ?>"><?php echo $instance['address']; ?></textarea>
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'phone' ); ?>"><?php _e('Phone number:', 'wproto'); ?></label>
				<input class="widefat" type="text" name="<?php echo $this->get_field_name( 'phone' ); ?>" id="<?php echo $this->get_field_id( 'phone' ); ?>" value="<?php echo $instance['phone']; ?>" />
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'email' ); ?>"><?php _e('Email:', 'wproto'); ?></label>
				<input class="widefat" type="text" name="<?php echo $this->get_field_name( 'email' ); ?>" id="<?php echo $this->get_field_id( 'email' ); ?>" value="<?php echo $instance['email']; ?>" />
			</p>
			<?php
		}
		
	}