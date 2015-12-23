<?php

	add_action( 'widgets_init', 'register_wpl_galaxy_wp_categories_widget' );
	
	function register_wpl_galaxy_wp_categories_widget() {
		register_widget( 'wpl_galaxy_wp_categories_widget' );
	}
	
	class wpl_galaxy_wp_categories_widget extends WP_Widget {
		
		function __construct() {
			$widget_ops = array( 'classname' => 'wproto-categories-widget', 'description' => __('A widget that displays taxonomies.', 'wproto') );
		
			$control_ops = array( 'width' => 300, 'height' => 350, 'id_base' => 'wproto-categories-widget' );
		
			$this->WP_Widget( 'wproto-categories-widget', __( '&laquo;Galaxy&raquo; Categories', 'wproto' ), $widget_ops, $control_ops );
		}
		
		function widget( $args, $instance ) {
			global $wpl_galaxy_wp;
			
			$data = array();
			$data['title'] = apply_filters( 'widget_title', $instance['title'] );
			
			$data['instance'] = $instance;
			$data['args'] = $args;

			$wpl_galaxy_wp->view->load_partial( 'widgets/categories', $data );

		}
		
		function update( $new_instance, $old_instance ) {
			$instance = $old_instance;

			//Strip tags from title and name to remove HTML 
			$instance['title'] = isset( $new_instance['title'] ) ? strip_tags( str_replace( '\'', "&#39;", $new_instance['title'] ) ) : '';
			$instance['tax_name'] = isset( $new_instance['tax_name'] ) ? $new_instance['tax_name'] : '';
			$instance['display_new'] = isset( $new_instance['display_new'] ) ? absint( $new_instance['display_new'] ) : 0;
			$instance['display_featured'] = isset( $new_instance['display_featured'] ) ? absint( $new_instance['display_featured'] ) : 0;
			$instance['display_image'] = isset( $new_instance['display_image'] ) ? absint( $new_instance['display_image'] ) : 0;
			$instance['display_description'] = isset( $new_instance['display_description'] ) ? absint( $new_instance['display_description'] ) : 0;
			$instance['do_not_display_empty'] = isset( $new_instance['do_not_display_empty'] ) ? absint( $new_instance['do_not_display_empty'] ) : 0;
			$instance['display'] = isset( $new_instance['display'] ) ? strip_tags( $new_instance['display'] ) : 'all';
			$instance['style'] = isset( $new_instance['style'] ) ? strip_tags( $new_instance['style'] ) : 'flat';
			$instance['show_count'] = isset( $new_instance['show_count'] ) ? absint( $new_instance['show_count'] ) : 0;

			return $instance;
		}
		
		function form( $instance ) {
			
			//Set up some default widget settings.
			$defaults = array(
				'title' => __( 'Categories', 'wproto' ),
				'tax_name' => '',
				'display_new' => 1,
				'display_featured' => 1,
				'display_image' => 1,
				'display_description' => 1,
				'do_not_display_empty' => 1,
				'show_count' => 1,
				'display' => 'all',
				'style' => 'flat'
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
				<label for="<?php echo $this->get_field_id( 'tax_name' ); ?>"><?php _e('Choose a taxonomy:', 'wproto'); ?></label>
				<select class="widefat" id="<?php echo $this->get_field_id( 'tax_name' ); ?>" name="<?php echo $this->get_field_name( 'tax_name' ); ?>">
					<option <?php echo $instance['tax_name'] == 'category' ? 'selected="selected"' : ''; ?> value="category"><?php _e( 'Blog category', 'wproto' ); ?></option>
					<option <?php echo $instance['tax_name'] == 'wproto_video_category' ? 'selected="selected"' : ''; ?> value="wproto_video_category"><?php _e( 'Video categories', 'wproto' ); ?></option>
					<option <?php echo $instance['tax_name'] == 'wproto_photoalbums_category' ? 'selected="selected"' : ''; ?> value="wproto_photoalbums_category"><?php _e( 'Photoalbum categories', 'wproto' ); ?></option>
					<option <?php echo $instance['tax_name'] == 'wproto_catalog_category' ? 'selected="selected"' : ''; ?> value="wproto_catalog_category"><?php _e( 'Catalog categories', 'wproto' ); ?></option>
					<option <?php echo $instance['tax_name'] == 'wproto_portfolio_category' ? 'selected="selected"' : ''; ?> value="wproto_portfolio_category"><?php _e( 'Portfolio categories', 'wproto' ); ?></option>
				</select>
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'display' ); ?>"><?php _e('Display:', 'wproto'); ?></label>
				<select class="widefat" id="<?php echo $this->get_field_id( 'display' ); ?>" name="<?php echo $this->get_field_name( 'display' ); ?>">
					<option <?php echo $instance['display'] == 'all' ? 'selected="selected"' : ''; ?> value="all"><?php _e( 'All categories', 'wproto' ); ?></option>
					<option <?php echo $instance['display'] == 'only_featured' ? 'selected="selected"' : ''; ?> value="only_featured"><?php _e( 'Featured only', 'wproto' ); ?></option>
					<option <?php echo $instance['display'] == 'only_new' ? 'selected="selected"' : ''; ?> value="only_new"><?php _e( 'New only', 'wproto' ); ?></option>
					<option <?php echo $instance['display'] == 'only_new_and_featured' ? 'selected="selected"' : ''; ?> value="only_new_and_featured"><?php _e( 'New and Featured only', 'wproto' ); ?></option>
				</select>
			</p>
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['display_new'] ); ?> id="<?php echo $this->get_field_id( 'display_new' ); ?>" name="<?php echo $this->get_field_name( 'display_new' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'display_new' ); ?>"><?php _e('Display "new" sticker', 'wproto'); ?></label>  
			</p>
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['display_featured'] ); ?> id="<?php echo $this->get_field_id( 'display_featured' ); ?>" name="<?php echo $this->get_field_name( 'display_featured' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'display_featured' ); ?>"><?php _e('Display "featured" sticker', 'wproto'); ?></label>  
			</p>
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['display_image'] ); ?> id="<?php echo $this->get_field_id( 'display_image' ); ?>" name="<?php echo $this->get_field_name( 'display_image' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'display_image' ); ?>"><?php _e('Display category image', 'wproto'); ?></label>  
			</p>
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['display_description'] ); ?> id="<?php echo $this->get_field_id( 'display_description' ); ?>" name="<?php echo $this->get_field_name( 'display_description' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'display_description' ); ?>"><?php _e('Display category description', 'wproto'); ?></label>  
			</p>
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['do_not_display_empty'] ); ?> id="<?php echo $this->get_field_id( 'do_not_display_empty' ); ?>" name="<?php echo $this->get_field_name( 'do_not_display_empty' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'do_not_display_empty' ); ?>"><?php _e('Do not display empty categories', 'wproto'); ?></label>  
			</p>
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['show_count'] ); ?> id="<?php echo $this->get_field_id( 'show_count' ); ?>" name="<?php echo $this->get_field_name( 'show_count' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'show_count' ); ?>"><?php _e('Show count of posts', 'wproto'); ?></label>  
			</p>
			<?php
		}
		
	}