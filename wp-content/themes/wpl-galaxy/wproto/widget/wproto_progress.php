<?php

	add_action( 'widgets_init', 'register_wpl_galaxy_wp_progress_widget' );
	
	function register_wpl_galaxy_wp_progress_widget() {
		register_widget( 'wpl_galaxy_wp_progress_widget' );
	}
	
	class wpl_galaxy_wp_progress_widget extends WP_Widget {
		
		function __construct() {
			$widget_ops = array( 'classname' => 'wproto-progress-widget', 'description' => __('A widget that displays the progress bars. ', 'wproto') );
		
			$control_ops = array( 'width' => 300, 'height' => 350, 'id_base' => 'wproto-progress-widget' );
		
			$this->WP_Widget( 'wproto-progress-widget', __( '&laquo;Galaxy&raquo; Progress Bars', 'wproto' ), $widget_ops, $control_ops );
		}
		
		function widget( $args, $instance ) {
			global $wpl_galaxy_wp;
			
			$data = array();
			$data['title'] = apply_filters( 'widget_title', $instance['title'] );
			
			$data['instance'] = $instance;
			$data['args'] = $args;

			$wpl_galaxy_wp->view->load_partial( 'widgets/progress', $data );

		}
		
		function update( $new_instance, $old_instance ) {
			$instance = $old_instance;

			//Strip tags from title and name to remove HTML 
			
			$instance['title'] = strip_tags( str_replace( '\'', "&#39;", $new_instance['title'] ) );
			$instance['progress_content'] = $new_instance['progress_content'];

			return $instance;
		}
		
		function form( $instance ) {
			
			//Set up some default widget settings.
			$defaults = array(
				'title' => __( 'Our Skills', 'wproto' ),
				'progress_content' => ''
			);
			
			$instance = wp_parse_args( (array) $instance, $defaults );
			
			?>
			<p>
				<label for="<?php echo $this->get_field_id( 'title' ); ?>"><?php _e('Widget title:', 'wproto'); ?></label>
				<input class="widefat" type="text" id="<?php echo $this->get_field_id( 'title' ); ?>" name="<?php echo $this->get_field_name( 'title' ); ?>" value="<?php echo $instance['title']; ?>" />
			</p>
			<p class="wproto-edit-progress-widget-p">
				<textarea style="display: none" name="<?php echo $this->get_field_name( 'progress_content' ); ?>" id="<?php echo $this->get_field_id( 'progress_content' ); ?>"><?php echo esc_textarea( $instance['progress_content'] ); ?></textarea>
				<a href="javascript:;" data-content-id="#<?php echo $this->get_field_id( 'progress_content' ); ?>" id="wproto-edit-progress-widget" class="button button-primary"><?php _e( 'Click here to edit progress bars', 'wproto' ); ?></a>
			</p>
			<?php
		}
		
	}