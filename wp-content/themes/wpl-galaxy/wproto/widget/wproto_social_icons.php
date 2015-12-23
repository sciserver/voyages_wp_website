<?php

	add_action( 'widgets_init', 'register_wpl_galaxy_wp_social_icons_widget' );
	
	function register_wpl_galaxy_wp_social_icons_widget() {
		register_widget( 'wpl_galaxy_wp_social_icons_widget' );
	}
	
	class wpl_galaxy_wp_social_icons_widget extends WP_Widget {
		
		function __construct() {
			$widget_ops = array( 'classname' => 'wproto-social-icons-widget', 'description' => __('A widget that displays your social icons. ', 'wproto') );
		
			$control_ops = array( 'width' => 300, 'height' => 350, 'id_base' => 'wproto-social-icons-widget' );
		
			$this->WP_Widget( 'wproto-social-icons-widget', __( '&laquo;Galaxy&raquo; Social Icons', 'wproto' ), $widget_ops, $control_ops );
		}
		
		function widget( $args, $instance ) {
			global $wpl_galaxy_wp;
			
			$data = array();
			$data['title'] = apply_filters( 'widget_title', $instance['title'] );
			
			$data['instance'] = $instance;
			$data['args'] = $args;

			$wpl_galaxy_wp->view->load_partial( 'widgets/social_icons', $data );

		}
		
		function update( $new_instance, $old_instance ) {
			$instance = $old_instance;

			//Strip tags from title and name to remove HTML 
			$instance['title'] = strip_tags( $new_instance['title'] );

			return $instance;
		}
		
		function form( $instance ) {
			
			//Set up some default widget settings.
			$defaults = array(
				'title' => '',
			);
			
			$instance = wp_parse_args( (array) $instance, $defaults );
			
			?>
			<p>
				<label for="<?php echo $this->get_field_id( 'title' ); ?>"><?php _e('Widget title:', 'wproto'); ?></label>
				<input class="widefat" type="text" id="<?php echo $this->get_field_id( 'title' ); ?>" name="<?php echo $this->get_field_name( 'title' ); ?>" value="<?php echo $instance['title']; ?>" />
			</p>
			<?php
		}
		
	}