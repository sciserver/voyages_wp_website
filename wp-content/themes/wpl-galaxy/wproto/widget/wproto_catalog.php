<?php

	add_action( 'widgets_init', 'register_wpl_galaxy_wp_catalog_widget' );
	
	function register_wpl_galaxy_wp_catalog_widget() {
		register_widget( 'wpl_galaxy_wp_catalog_widget' );
	}
	
	class wpl_galaxy_wp_catalog_widget extends WP_Widget {
		
		function __construct() {
			$widget_ops = array( 'classname' => 'wproto-catalog-widget', 'description' => __('A widget that displays the catalog items. ', 'wproto') );
		
			$control_ops = array( 'width' => 300, 'height' => 350, 'id_base' => 'wproto-catalog-widget' );
		
			$this->WP_Widget( 'wproto-catalog-widget', __( '&laquo;Galaxy&raquo; Catalog', 'wproto' ), $widget_ops, $control_ops );
		}
		
		function widget( $args, $instance ) {
			global $wpl_galaxy_wp;
			
			$data = array();
			$data['title'] = apply_filters( 'widget_title', $instance['title'] );
			
			$data['instance'] = $instance;
			$data['args'] = $args;

			$wpl_galaxy_wp->view->load_partial( 'widgets/catalog', $data );
		}
		
		function update( $new_instance, $old_instance ) {
			$instance = $old_instance;

			//Strip tags from title and name to remove HTML 
			$instance['title'] = isset( $new_instance['title'] ) ? strip_tags( str_replace( '\'', "&#39;", $new_instance['title'] ) ) : 0;
			$instance['featured_only'] = isset( $new_instance['featured_only'] ) ? absint( $new_instance['featured_only'] ) : 0;
			$instance['sticky_only'] = isset( $new_instance['sticky_only'] ) ? absint( $new_instance['sticky_only'] ) : 0;
			
			$instance['display_thumb'] = isset( $new_instance['display_thumb'] ) ? absint( $new_instance['display_thumb'] ) : 0;
			$instance['display_price'] = isset( $new_instance['display_price'] ) ? absint( $new_instance['display_price'] ) : 0;
			$instance['display_excerpt'] = isset( $new_instance['display_excerpt'] ) ? absint( $new_instance['display_excerpt'] ) : 0;
			$instance['display_likes'] = isset( $new_instance['display_likes'] ) ? absint( $new_instance['display_likes'] ) : 0;
			$instance['display_views'] = isset( $new_instance['display_views'] ) ? absint( $new_instance['display_views'] ) : 0;
			$instance['display_comments_count'] = isset( $new_instance['display_comments_count'] ) ? absint( $new_instance['display_comments_count'] ) : 0;
			
			$instance['posts_count'] = isset( $new_instance['posts_count'] ) ? absint( $new_instance['posts_count'] ) : 0;
			$instance['display_categories'] = isset( $new_instance['display_categories'] ) ? strip_tags( $new_instance['display_categories'] ) : 'all';
			$instance['order_by'] = isset( $new_instance['order_by'] ) ? strip_tags( $new_instance['order_by'] ) : 'id';
			$instance['sort'] = isset( $new_instance['sort'] ) ? strip_tags( $new_instance['sort'] ) : 'DESC';
			$instance['link_to'] = isset( $new_instance['link_to'] ) && $new_instance['link_to'] == 'post' ? 'post' : 'custom_url';

			return $instance;
		}
		
		function form( $instance ) {
			
			//Set up some default widget settings.
			$defaults = array(
				'title' => __( 'Catalog', 'wproto' ),
				'featured_only' => 0,
				'sticky_only' => 0,
				'display_thumb' => 1,
				'display_price' => 1,
				'display_excerpt' => 1,
				'display_likes' => 1,
				'display_views' => 1,
				'display_comments_count' => 1,
				'posts_count' => 5,
				'display_categories' => 'all',
				'order_by' => 'date',
				'sort' => 'DESC',
				'link_to' => 'post'
			);
			
			$instance = wp_parse_args( (array) $instance, $defaults );
			
			?>
			<p>
				<label for="<?php echo $this->get_field_id( 'title' ); ?>"><?php _e('Widget title:', 'wproto'); ?></label>
				<input class="widefat" type="text" id="<?php echo $this->get_field_id( 'title' ); ?>" name="<?php echo $this->get_field_name( 'title' ); ?>" value="<?php echo $instance['title']; ?>" />
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'link_to' ); ?>"><?php _e('Link to:', 'wproto'); ?></label>
				<select class="widefat" id="<?php echo $this->get_field_id( 'link_to' ); ?>" name="<?php echo $this->get_field_name( 'link_to' ); ?>">
					<option <?php echo $instance['link_to'] == 'post' ? 'selected="selected"' : ''; ?> value="post"><?php _e( 'Catalog post', 'wproto' ); ?></option>
					<option <?php echo $instance['link_to'] == 'custom_url' ? 'selected="selected"' : ''; ?> value="custom_url"><?php _e( 'Custom buy URL', 'wproto' ); ?></option>
				</select>
			</p>
			<p>
				<strong><?php _e('Status', 'wproto'); ?>:</strong>
			</p>
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['featured_only'] ); ?> id="<?php echo $this->get_field_id( 'featured_only' ); ?>" name="<?php echo $this->get_field_name( 'featured_only' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'featured_only' ); ?>"><?php _e('Featured only', 'wproto'); ?></label>  
			</p>
			<p>
				<strong><?php _e('Displaying', 'wproto'); ?>:</strong>
			</p>
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['display_thumb'] ); ?> id="<?php echo $this->get_field_id( 'display_thumb' ); ?>" name="<?php echo $this->get_field_name( 'display_thumb' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'display_thumb' ); ?>"><?php _e('Display thumbnails', 'wproto'); ?></label>  
			</p>
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['display_price'] ); ?> id="<?php echo $this->get_field_id( 'display_price' ); ?>" name="<?php echo $this->get_field_name( 'display_price' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'display_price' ); ?>"><?php _e('Display price', 'wproto'); ?></label>  
			</p>
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['display_excerpt'] ); ?> id="<?php echo $this->get_field_id( 'display_excerpt' ); ?>" name="<?php echo $this->get_field_name( 'display_excerpt' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'display_excerpt' ); ?>"><?php _e('Display excerpt', 'wproto'); ?></label>  
			</p>
			<!--
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['display_likes'] ); ?> id="<?php echo $this->get_field_id( 'display_likes' ); ?>" name="<?php echo $this->get_field_name( 'display_likes' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'display_likes' ); ?>"><?php _e('Display likes', 'wproto'); ?></label>  
			</p>
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['display_views'] ); ?> id="<?php echo $this->get_field_id( 'display_views' ); ?>" name="<?php echo $this->get_field_name( 'display_views' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'display_views' ); ?>"><?php _e('Display views', 'wproto'); ?></label>  
			</p>
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['display_comments_count'] ); ?> id="<?php echo $this->get_field_id( 'display_comments_count' ); ?>" name="<?php echo $this->get_field_name( 'display_comments_count' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'display_comments_count' ); ?>"><?php _e('Display comments count', 'wproto'); ?></label>  
			</p>
			-->
			<p>
				<label for="<?php echo $this->get_field_id( 'posts_count' ); ?>"><?php _e('Number of items to display:', 'wproto'); ?></label>
				<input class="widefat" type="number" min="1" name="<?php echo $this->get_field_name( 'posts_count' ); ?>" id="<?php echo $this->get_field_id( 'posts_count' ); ?>" value="<?php echo $instance['posts_count']; ?>" />
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'display_categories' ); ?>"><?php _e('Display from categories:', 'wproto'); ?></label>
				<select class="widefat" id="<?php echo $this->get_field_id( 'display_categories' ); ?>" name="<?php echo $this->get_field_name( 'display_categories' ); ?>">
					<option <?php echo $instance['display_categories'] == 'all' ? 'selected="selected"' : ''; ?> value="all"><?php _e( 'All categories', 'wproto'); ?></option>
					<?php
						$categories = get_terms( 'wproto_catalog_category', array(
							'hide_empty' => 0
						));
						if( is_array( $categories ) && count( $categories ) > 0 ):
						foreach( $categories as $cat ):
					?>
					<option <?php echo $instance['display_categories'] == $cat->term_id ? 'selected="selected"' : ''; ?> value="<?php echo $cat->term_id; ?>"><?php echo $cat->name; ?></option>
					<?php
						endforeach;
						endif;
					?>
				</select>
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'order_by' ); ?>"><?php _e('Order items by:', 'wproto'); ?></label>
				<select class="widefat" id="<?php echo $this->get_field_id( 'order_by' ); ?>" name="<?php echo $this->get_field_name( 'order_by' ); ?>">
					<option <?php echo $instance['order_by'] == 'id' ? 'selected="selected"' : ''; ?> value="id"><?php _e( 'ID', 'wproto' ); ?></option>
					<option <?php echo $instance['order_by'] == 'date' ? 'selected="selected"' : ''; ?> value="date"><?php _e( 'Date', 'wproto' ); ?></option>
					<option <?php echo $instance['order_by'] == 'modified' ? 'selected="selected"' : ''; ?> value="modified"><?php _e( 'Modified', 'wproto' ); ?></option>
					<option <?php echo $instance['order_by'] == 'title' ? 'selected="selected"' : ''; ?> value="title"><?php _e( 'Title', 'wproto' ); ?></option>
					<option <?php echo $instance['order_by'] == 'rand' ? 'selected="selected"' : ''; ?> value="rand"><?php _e( 'Random', 'wproto' ); ?></option>
					<option <?php echo $instance['order_by'] == 'menu' ? 'selected="selected"' : ''; ?> value="menu"><?php _e( 'Menu order', 'wproto' ); ?></option>
				</select>
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'sort' ); ?>"><?php _e('Sort:', 'wproto'); ?></label>
				<select class="widefat" id="<?php echo $this->get_field_id( 'sort' ); ?>" name="<?php echo $this->get_field_name( 'sort' ); ?>">
					<option <?php echo $instance['sort'] == 'ASC' ? 'selected="selected"' : ''; ?> value="ASC"><?php _e( 'Ascending', 'wproto' ); ?></option>
					<option <?php echo $instance['sort'] == 'DESC' ? 'selected="selected"' : ''; ?> value="DESC"><?php _e( 'Descending', 'wproto' ); ?></option>
				</select>
			</p>
			<?php
		}
		
	}