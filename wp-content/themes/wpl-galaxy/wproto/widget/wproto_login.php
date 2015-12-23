<?php

	add_action( 'widgets_init', 'register_wpl_galaxy_wp_login_widget' );
	
	function register_wpl_galaxy_wp_login_widget() {
		register_widget( 'wpl_galaxy_wp_login_widget' );
	}
	
	class wpl_galaxy_wp_login_widget extends WP_Widget {
		
		function __construct() {
			$widget_ops = array( 'classname' => 'wproto-login-widget', 'description' => __('A widget that displays the social signin / sugnup form. ', 'wproto') );
		
			$control_ops = array( 'width' => 300, 'height' => 350, 'id_base' => 'wproto-login-widget' );
		
			$this->WP_Widget( 'wproto-login-widget', __( '&laquo;Galaxy&raquo; Register / Login', 'wproto' ), $widget_ops, $control_ops );
		}
		
		function widget( $args, $instance ) {
			global $wpl_galaxy_wp;
			
			$data = array();
			
			$data['instance'] = $instance;
			$data['args'] = $args;
			
			$title = is_user_logged_in() ? $instance['title_logged'] : $instance['title'];
			
			$data['title'] = apply_filters( 'widget_title', $title );

			if( is_user_logged_in() && $instance['hide_from_logged'] == 1 ) {
				
			} else {
				$wpl_galaxy_wp->view->load_partial( 'widgets/login', $data );
			}

		}
		
		function update( $new_instance, $old_instance ) {
			$instance = $old_instance;

			//Strip tags from title and name to remove HTML 
			$instance['title'] = isset( $new_instance['title'] ) ? strip_tags( $new_instance['title'] ) : '';
			$instance['title_logged'] = isset( $new_instance['title_logged'] ) ? strip_tags( $new_instance['title_logged'] ) : '';
			$instance['hide_from_logged'] = isset( $new_instance['hide_from_logged'] ) ? absint( $new_instance['hide_from_logged'] ) : 0;
			
			return $instance;
		}
		
		function form( $instance ) {

			$defaults = array(
				'title' => __( 'Sign In / Sign Up', 'wproto' ),
				'title_logged' => '',
				'hide_from_logged' => 0
			);
			
			$instance = wp_parse_args( (array) $instance, $defaults );

			?>
			<p>
				<label for="<?php echo $this->get_field_id( 'title' ); ?>"><?php _e('Widget title for unregistered users:', 'wproto'); ?></label>
				<input class="widefat" type="text" id="<?php echo $this->get_field_id( 'title' ); ?>" name="<?php echo $this->get_field_name( 'title' ); ?>" value="<?php echo $instance['title']; ?>" />
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'hide_from_logged' ); ?>"><?php _e('Hide widget from authorized users:', 'wproto'); ?></label>
				<input type="checkbox" <?php checked( $instance['hide_from_logged'], 1 ); ?> name="<?php echo $this->get_field_name( 'hide_from_logged' ); ?>" value="1" id="<?php echo $this->get_field_id( 'hide_from_logged' ); ?>" />
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'title_logged' ); ?>"><?php _e('Widget title for authorized users (optional):', 'wproto'); ?></label>
				<input class="widefat" type="text" id="<?php echo $this->get_field_id( 'title_logged' ); ?>" name="<?php echo $this->get_field_name( 'title_logged' ); ?>" value="<?php echo $instance['title_logged']; ?>" />
			</p>
			<p class="wproto-edit-toggles-widget-p">
				<a href="<?php echo admin_url('admin.php?page=wproto_theme_settings#api'); ?>" class="button button-primary"><?php _e( 'Go to theme\'s API options', 'wproto' ); ?></a>
			</p>
			<?php
		}
		
	}