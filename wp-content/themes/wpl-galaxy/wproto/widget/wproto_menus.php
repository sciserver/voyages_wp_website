<?php

	add_action( 'widgets_init', 'register_wpl_galaxy_wp_menus_widget' );
	
	function register_wpl_galaxy_wp_menus_widget() {
		register_widget( 'wpl_galaxy_wp_menus_widget' );
	}
	
	class wpl_galaxy_wp_menus_widget extends WP_Widget {
		
		function __construct() {
			$widget_ops = array( 'classname' => 'wproto-menus-widget', 'description' => __('A widget that displays menus.', 'wproto') );
		
			$control_ops = array( 'width' => 300, 'height' => 350, 'id_base' => 'wproto-menus-widget' );
		
			$this->WP_Widget( 'wproto-menus-widget', __( '&laquo;Galaxy&raquo; Menus', 'wproto' ), $widget_ops, $control_ops );
		}
		
		function widget( $args, $instance ) {
			global $wpl_galaxy_wp;
			
			$data = array();
			$data['title'] = apply_filters( 'widget_title', $instance['title'] );
			
			$data['instance'] = $instance;
			$data['args'] = $args;

			$wpl_galaxy_wp->view->load_partial( 'widgets/menus', $data );

		}
		
		function update( $new_instance, $old_instance ) {
			$instance = $old_instance;

			//Strip tags from title and name to remove HTML 
			$instance['title'] = strip_tags( str_replace( '\'', "&#39;", $new_instance['title'] ) );
			$instance['menu'] = isset( $new_instance['menu'] ) ? $new_instance['menu'] : '';
			$instance['display_icons'] = isset( $new_instance['display_icons'] ) ? absint( $new_instance['display_icons'] ) : 0;
			$instance['display_description'] = isset( $new_instance['display_description'] ) ? absint( $new_instance['display_description'] ) : 0;

			return $instance;
		}
		
		function form( $instance ) {
			
			//Set up some default widget settings.
			$defaults = array(
				'title' => __( 'Menus', 'wproto' ),
				'menu' => '',
				'display_icons' => 1
			);
			
			$instance = wp_parse_args( (array) $instance, $defaults );
			
			global $wp_roles;
			$roles = $wp_roles->get_names();
			
			$menus = get_terms( 'nav_menu', array( 'hide_empty' => true ) );
			?>
			<p>
				<label for="<?php echo $this->get_field_id( 'title' ); ?>"><?php _e('Widget title:', 'wproto'); ?></label>
				<input class="widefat" type="text" id="<?php echo $this->get_field_id( 'title' ); ?>" name="<?php echo $this->get_field_name( 'title' ); ?>" value="<?php echo $instance['title']; ?>" />
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'menu' ); ?>"><?php _e('Choose a menu:', 'wproto'); ?></label>
				<select class="widefat" id="<?php echo $this->get_field_id( 'menu' ); ?>" name="<?php echo $this->get_field_name( 'menu' ); ?>">
					<?php
						if( count( $menus ) > 0 ):
						foreach ( $menus as $menu ):
					?>
					<option <?php echo $instance['menu'] == $menu->slug ? 'selected="selected"' : ''; ?> value="<?php echo $menu->slug; ?>"><?php echo $menu->name; ?></option>
					<?php endforeach; endif; ?>
					
				</select>
			</p>
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['display_icons'] ); ?> id="<?php echo $this->get_field_id( 'display_icons' ); ?>" name="<?php echo $this->get_field_name( 'display_icons' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'display_icons' ); ?>"><?php _e('Display icons', 'wproto'); ?></label>  
			</p>
			<?php
		}
		
	}