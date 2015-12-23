<?php

	add_action( 'widgets_init', 'register_wpl_galaxy_wp_site_description_widget' );
	
	function register_wpl_galaxy_wp_site_description_widget() {
		register_widget( 'wpl_galaxy_wp_site_description_widget' );
	}
	
	class wpl_galaxy_wp_site_description_widget extends WP_Widget {
		
		function __construct() {
			$widget_ops = array( 'classname' => 'wproto-site-description-widget', 'description' => __('A widget that displays your logo and short site description. ', 'wproto') );
		
			$control_ops = array( 'width' => 300, 'height' => 350, 'id_base' => 'wproto-site-description-widget' );
		
			$this->WP_Widget( 'wproto-site-description-widget', __( '&laquo;Galaxy&raquo; Site Description', 'wproto' ), $widget_ops, $control_ops );
		}
		
		function widget( $args, $instance ) {
			global $wpl_galaxy_wp;
			
			$data = array();
			
			$data['instance'] = $instance;
			$data['args'] = $args;

			$wpl_galaxy_wp->view->load_partial( 'widgets/site_description', $data );

		}
		
		function update( $new_instance, $old_instance ) {
			$instance = $old_instance;
			$instance['logo'] = isset( $new_instance['logo'] ) ? strip_tags( $new_instance['logo'] ) : '';
			$instance['logo_2x'] = isset( $new_instance['logo_2x'] ) ? strip_tags( $new_instance['logo_2x'] ) : '';
			$instance['logo_width'] = isset( $new_instance['logo_width'] ) ? strip_tags( $new_instance['logo_width'] ) : '';
			$instance['description'] = isset( $new_instance['description'] ) ? str_replace( '\'', "&#39;", $new_instance['description'] ) : '';

			return $instance;
		}
		
		function form( $instance ) {
			
			$defaults = array(
				'logo' => '',
				'logo_2x' => '',
				'logo_width' => '100%',
				'description' => ''
			);
			
			$instance = wp_parse_args( (array) $instance, $defaults );
			?>
			<p>
				<label style="display: block;" for="<?php echo $this->get_field_id( 'logo' ); ?>"><?php _e('Logo:', 'wproto'); ?></label>
				<input class="widefat" style="width: 50%" type="text" id="<?php echo $this->get_field_id( 'logo' ); ?>" name="<?php echo $this->get_field_name( 'logo' ); ?>" value="<?php echo $instance['logo']; ?>" /> 
				<a href="javascript:;" data-url-input="#<?php echo $this->get_field_id( 'logo' ); ?>" class="button wproto-image-selector"><?php _e( 'Upload', 'wproto' ); ?></a>
			</p>
			<?php if( wpl_galaxy_wp_utils::is_retina_enabled() ): ?>
			<p>
				<label style="display: block;" for="<?php echo $this->get_field_id( 'logo_2x' ); ?>"><?php _e('Logo in twice size for retina displays:', 'wproto'); ?></label>
				<input class="widefat" style="width: 50%" type="text" id="<?php echo $this->get_field_id( 'logo_2x' ); ?>" name="<?php echo $this->get_field_name( 'logo_2x' ); ?>" value="<?php echo $instance['logo_2x']; ?>" /> 
				<a href="javascript:;" data-url-input="#<?php echo $this->get_field_id( 'logo_2x' ); ?>" class="button wproto-image-selector"><?php _e( 'Upload', 'wproto' ); ?></a>
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'logo_width' ); ?>"><?php _e('Original logo width:', 'wproto'); ?></label>
				<input class="widefat" style="width: 50px" type="text" id="<?php echo $this->get_field_id( 'logo_width' ); ?>" name="<?php echo $this->get_field_name( 'logo_width' ); ?>" value="<?php echo $instance['logo_width']; ?>" />
			</p>
			<?php endif; ?>
			<p>
				<label for="<?php echo $this->get_field_id( 'description' ); ?>"><?php _e('Description after logo (optional):', 'wproto'); ?></label>
				<textarea class="widefat" rows="7" name="<?php echo $this->get_field_name( 'description' ); ?>" id="<?php echo $this->get_field_id( 'description' ); ?>"><?php echo $instance['description']; ?></textarea>
			</p>
			<?php
		}
		
	}