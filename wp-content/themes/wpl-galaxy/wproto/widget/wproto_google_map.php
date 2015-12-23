<?php

	add_action( 'widgets_init', 'register_wpl_galaxy_wp_google_map_widget' );
	
	function register_wpl_galaxy_wp_google_map_widget() {
		register_widget( 'wpl_galaxy_wp_google_map_widget' );
	}
	
	class wpl_galaxy_wp_google_map_widget extends WP_Widget {
		
		function __construct() {
			$widget_ops = array( 'classname' => 'wproto-google-map-widget', 'description' => __('A widget that displays the google map. ', 'wproto') );
		
			$control_ops = array( 'width' => 300, 'height' => 350, 'id_base' => 'wproto-google-map-widget' );
		
			$this->WP_Widget( 'wproto-google-map-widget', __( '&laquo;Galaxy&raquo; Google Map', 'wproto' ), $widget_ops, $control_ops );
		}
		
		function widget( $args, $instance ) {
			global $wpl_galaxy_wp;
			
			$data = array();
			$data['title'] = apply_filters( 'widget_title', $instance['title'] );
			
			$data['instance'] = $instance;
			$data['args'] = $args;

			$wpl_galaxy_wp->view->load_partial( 'widgets/google_map', $data );

		}
		
		function update( $new_instance, $old_instance ) {
			$instance = $old_instance;

			$allowed_tags = wp_kses_allowed_html( 'post' );

			//Strip tags from title and name to remove HTML 
			$instance['title'] = strip_tags( str_replace( '\'', "&#39;", $new_instance['title'] ) );
			$instance['before_text'] = isset( $new_instance['before_text'] ) ? wp_kses( $new_instance['before_text'], $allowed_tags ) : '';
			$instance['address'] = isset( $new_instance['address'] ) ? strip_tags( str_replace( '\'', "&#39;", $new_instance['address'] ) ) : '';
			$instance['after_text'] = isset( $new_instance['after_text'] ) ? wp_kses( $new_instance['after_text'], $allowed_tags ) : '';

			return $instance;
		}
		
		function form( $instance ) {
			
			//Set up some default widget settings.
			$defaults = array(
				'title' => __( 'Google Map', 'wproto' ),
				'before_text' => '',
				'address' => '',
				'after_text' => ''
			);
			
			$instance = wp_parse_args( (array) $instance, $defaults );
			
			?>
			<p>
				<label for="<?php echo $this->get_field_id( 'title' ); ?>"><?php _e('Widget title:', 'wproto'); ?></label>
				<input class="widefat" type="text" id="<?php echo $this->get_field_id( 'title' ); ?>" name="<?php echo $this->get_field_name( 'title' ); ?>" value="<?php echo $instance['title']; ?>" />
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'before_text' ); ?>"><?php _e('Text before map (optional):', 'wproto'); ?></label>
				<textarea class="widefat" name="<?php echo $this->get_field_name( 'before_text' ); ?>" id="<?php echo $this->get_field_id( 'before_text' ); ?>"><?php echo $instance['before_text']; ?></textarea>
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'address' ); ?>"><?php _e('Address:', 'wproto'); ?></label>
				<input class="widefat" type="text" name="<?php echo $this->get_field_name( 'address' ); ?>" id="<?php echo $this->get_field_id( 'address' ); ?>" value="<?php echo $instance['address']; ?>" />
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'after_text' ); ?>"><?php _e('Text after map (optional):', 'wproto'); ?></label>
				<textarea class="widefat" name="<?php echo $this->get_field_name( 'after_text' ); ?>" id="<?php echo $this->get_field_id( 'after_text' ); ?>"><?php echo $instance['after_text']; ?></textarea>
			</p>
			<?php
		}
		
	}