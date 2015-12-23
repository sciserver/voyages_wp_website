<?php

	add_action( 'widgets_init', 'register_wpl_galaxy_wp_author_info_widget' );
	
	function register_wpl_galaxy_wp_author_info_widget() {
		register_widget( 'wpl_galaxy_wp_author_info_widget' );
	}
	
	class wpl_galaxy_wp_author_info_widget extends WP_Widget {
		
		function __construct() {
			$widget_ops = array( 'classname' => 'wproto-authors-info-widget', 'description' => __('A widget that displays the information about registered WordPress user. ', 'wproto') );
		
			$control_ops = array( 'width' => 300, 'height' => 350, 'id_base' => 'wproto-authors-info-widget' );
		
			$this->WP_Widget( 'wproto-authors-info-widget', __( '&laquo;Galaxy&raquo; Author\'s Info', 'wproto' ), $widget_ops, $control_ops );
		}
		
		function widget( $args, $instance ) {
			global $wpl_galaxy_wp;
			
			$data = array();
			$data['title'] = apply_filters( 'widget_title', $instance['title'] );
			
			$data['instance'] = $instance;
			$data['args'] = $args;

			$wpl_galaxy_wp->view->load_partial( 'widgets/authors_info', $data );

		}
		
		function update( $new_instance, $old_instance ) {
			$instance = $old_instance;

			//Strip tags from title and name to remove HTML 
			$instance['title'] = isset( $new_instance['title'] ) ? strip_tags( str_replace( '\'', "&#39;", $new_instance['title'] ) ) : '';
			$instance['user_id'] = isset( $new_instance['user_id'] ) ? absint( $new_instance['user_id'] ) : 0;
			$instance['show_avatar'] = isset( $new_instance['show_avatar'] ) ? absint( $new_instance['show_avatar'] ) : 0;
			$instance['show_website'] = isset( $new_instance['show_website'] ) ? absint( $new_instance['show_website'] ) : 0;
			$instance['show_email'] = isset( $new_instance['show_email'] ) ? absint( $new_instance['show_email'] ) : 0;

			return $instance;
		}
		
		function form( $instance ) {
			
			//Set up some default widget settings.
			$defaults = array(
				'title' => __( 'Author\'s info', 'wproto' ),
				'user_id' => '',
				'show_avatar' => 1,
				'show_website' => 1,
				'show_email' => 1
			);
			
			$instance = wp_parse_args( (array) $instance, $defaults );
			
			global $wp_roles;
			$roles = $wp_roles->get_names();
			?>
			<p>
				<label for="<?php echo $this->get_field_id( 'title' ); ?>"><?php _e('Widget title:', 'wproto'); ?></label>
				<input class="widefat" type="text" id="<?php echo $this->get_field_id( 'title' ); ?>" name="<?php echo $this->get_field_name( 'title' ); ?>" value="<?php echo $instance['title']; ?>" />
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'user_id' ); ?>"><?php _e('Choose an user:', 'wproto'); ?></label>
				<select class="widefat" id="<?php echo $this->get_field_id( 'user_id' ); ?>" name="<?php echo $this->get_field_name( 'user_id' ); ?>">
					<?php foreach( $roles as $k=>$v ): ?>
					<?php if( $k == 'subscriber' || $k == 'contributor' ) continue; ?>
					<optgroup label="<?php echo $v; ?>">
						<?php $users = get_users( 'orderby=nicename&role=' . $k ); ?>
						<?php foreach( $users as $user ): ?>
						<option <?php echo $instance['user_id'] == $user->ID ? 'selected="selected"' : ''; ?> value="<?php echo $user->ID; ?>"><?php echo $user->display_name; ?></option>
						<?php endforeach; ?>
					</optgroup>
					<?php endforeach; ?>
				</select>
			</p>
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['show_avatar'] ); ?> id="<?php echo $this->get_field_id( 'show_avatar' ); ?>" name="<?php echo $this->get_field_name( 'show_avatar' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'show_avatar' ); ?>"><?php _e('Show avatar', 'wproto'); ?></label>  
			</p>
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['show_website'] ); ?> id="<?php echo $this->get_field_id( 'show_website' ); ?>" name="<?php echo $this->get_field_name( 'show_website' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'show_website' ); ?>"><?php _e('Display social profiles', 'wproto'); ?></label>  
			</p>
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['show_email'] ); ?> id="<?php echo $this->get_field_id( 'show_email' ); ?>" name="<?php echo $this->get_field_name( 'show_email' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'show_email' ); ?>"><?php _e('Display email', 'wproto'); ?></label>  
			</p>
			<?php
		}
		
	}