<?php

	add_action( 'widgets_init', 'register_wpl_galaxy_wp_toggles_widget' );
	
	function register_wpl_galaxy_wp_toggles_widget() {
		register_widget( 'wpl_galaxy_wp_toggles_widget' );
	}
	
	class wpl_galaxy_wp_toggles_widget extends WP_Widget {
		
		function __construct() {
			$widget_ops = array( 'classname' => 'wproto-toggles-widget', 'description' => __('A widget that displays the toggles. ', 'wproto') );
		
			$control_ops = array( 'width' => 300, 'height' => 350, 'id_base' => 'wproto-toggles-widget' );
		
			$this->WP_Widget( 'wproto-toggles-widget', __( '&laquo;Galaxy&raquo; Toggles', 'wproto' ), $widget_ops, $control_ops );
		}
		
		function widget( $args, $instance ) {
			global $wpl_galaxy_wp;
			
			$data = array();
			$data['title'] = apply_filters( 'widget_title', $instance['title'] );
			
			$data['instance'] = $instance;
			$data['args'] = $args;

			$wpl_galaxy_wp->view->load_partial( 'widgets/toggles', $data );

		}
		
		function update( $new_instance, $old_instance ) {
			$instance = $old_instance;

			//Strip tags from title and name to remove HTML 
			
			$instance['title'] = strip_tags( str_replace( '\'', "&#39;", $new_instance['title'] ) );
			$instance['toggles_content'] = str_replace( '\'', "&#39;", $new_instance['toggles_content'] );

			return $instance;
		}
		
		function form( $instance ) {
			
			//Set up some default widget settings.
			$defaults = array(
				'title' => __( 'Toggles Widget', 'wproto' ),
				'toggles_content' => ''
			);
			
			$instance = wp_parse_args( (array) $instance, $defaults );
			
			?>
			<p>
				<label for="<?php echo $this->get_field_id( 'title' ); ?>"><?php _e('Widget title:', 'wproto'); ?></label>
				<input class="widefat" type="text" id="<?php echo $this->get_field_id( 'title' ); ?>" name="<?php echo $this->get_field_name( 'title' ); ?>" value="<?php echo $instance['title']; ?>" />
			</p>
			<p class="wproto-edit-toggles-widget-p">
				<textarea style="width: 100%; height: 130px;" name="<?php echo $this->get_field_name( 'toggles_content' ); ?>" id="<?php echo $this->get_field_id( 'toggles_content' ); ?>"><?php echo esc_textarea( $instance['toggles_content'] ); ?></textarea>
				<a href="javascript:;" data-content-id="<?php echo $this->get_field_id( 'toggles_content' ); ?>" class="button button-primary"><?php _e( 'Click here to add toggles', 'wproto' ); ?></a>
			</p>
			<?php
		}
		
	}