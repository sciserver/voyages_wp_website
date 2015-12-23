<?php

	add_action( 'widgets_init', 'register_wpl_galaxy_wp_random_posts_widget' );
	
	function register_wpl_galaxy_wp_random_posts_widget() {
		register_widget( 'wpl_galaxy_wp_random_posts_widget' );
	}
	
	class wpl_galaxy_wp_random_posts_widget extends WP_Widget {
		
		function __construct() {
			$widget_ops = array( 'classname' => 'wproto-random-posts-widget', 'description' => __('A widget that displays the random posts. ', 'wproto') );
		
			$control_ops = array( 'width' => 300, 'height' => 350, 'id_base' => 'wproto-random-posts-widget' );
		
			$this->WP_Widget( 'wproto-random-posts-widget', __( '&laquo;Galaxy&raquo; Random Posts', 'wproto' ), $widget_ops, $control_ops );
		}
		
		function widget( $args, $instance ) {
			global $wpl_galaxy_wp;
			
			$data = array();
			$data['title'] = apply_filters( 'widget_title', $instance['title'] );
			
			$data['posts'] = $wpl_galaxy_wp->model->post->get_random_posts( $instance['post_type'], $instance['count'] );
			
			$data['instance'] = $instance;
			$data['args'] = $args;

			$wpl_galaxy_wp->view->load_partial( 'widgets/random_posts', $data );
		}
		
		function update( $new_instance, $old_instance ) {
			$instance = $old_instance;

			//Strip tags from title and name to remove HTML 
			$instance['title'] = strip_tags( str_replace( '\'', "&#39;", $new_instance['title'] ) );
			$instance['post_type'] = isset( $new_instance['post_type'] ) ? strip_tags( $new_instance['post_type'] ) : 'post';
			$instance['count'] = isset( $new_instance['count'] ) ? absint( $new_instance['count'] ) : 0;
			$instance['display_thumbnails'] = isset( $new_instance['display_thumbnails'] ) ? absint($new_instance['display_thumbnails']) : 0;
			$instance['display_excerpt'] = isset( $new_instance['display_excerpt'] ) ? absint($new_instance['display_excerpt']) : 0;
			$instance['display_likes'] = isset( $new_instance['display_likes'] ) ? absint($new_instance['display_likes']) : 0;
			$instance['display_views'] = isset( $new_instance['display_views'] ) ? absint($new_instance['display_views']) : 0;
			$instance['display_comments_count'] = isset( $new_instance['display_comments_count'] ) ? absint($new_instance['display_comments_count']) : 0;

			return $instance;
		}
		
		function form( $instance ) {
			
			//Set up some default widget settings.
			$defaults = array(
				'title' => __( 'Random posts', 'wproto' ),
				'post_type' => 'post',
				'display_thumbnails' => 1,
				'display_excerpt' => 1,
				'display_likes' => 1,
				'display_views' => 1,
				'display_comments_count' => 1,
				'count' => 3
			);
			
			$instance = wp_parse_args( (array) $instance, $defaults );
			
			?>
			<p>
				<label for="<?php echo $this->get_field_id( 'title' ); ?>"><?php _e('Widget title:', 'wproto'); ?></label>
				<input style="width: 97%;" id="<?php echo $this->get_field_id( 'title' ); ?>" name="<?php echo $this->get_field_name( 'title' ); ?>" value="<?php echo $instance['title']; ?>" />
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'post_type' ); ?>"><?php _e('Post type:', 'wproto'); ?></label>
				<select name="<?php echo $this->get_field_name( 'post_type' ); ?>" id="<?php echo $this->get_field_id( 'post_type' ); ?>" class="widefat">
					<option <?php echo $instance['post_type'] == 'post' ? 'selected="selected"' : ''; ?> value="post"><?php _e('Blog posts', 'wproto'); ?></option>
					<option <?php echo $instance['post_type'] == 'wproto_video' ? 'selected="selected"' : ''; ?> value="wproto_video"><?php _e('Videos', 'wproto'); ?></option>
					<option <?php echo $instance['post_type'] == 'wproto_photoalbums' ? 'selected="selected"' : ''; ?> value="wproto_photoalbums"><?php _e('Photo Albums', 'wproto'); ?></option>
					<option <?php echo $instance['post_type'] == 'wproto_catalog' ? 'selected="selected"' : ''; ?> value="wproto_catalog"><?php _e('Catalog', 'wproto'); ?></option>
				</select>
			</p>
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['display_thumbnails'] ); ?> id="<?php echo $this->get_field_id( 'display_thumbnails' ); ?>" name="<?php echo $this->get_field_name( 'display_thumbnails' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'display_thumbnails' ); ?>"><?php _e('Display post thumbnails', 'wproto'); ?></label>  
			</p>
			<!--
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['display_excerpt'] ); ?> id="<?php echo $this->get_field_id( 'display_excerpt' ); ?>" name="<?php echo $this->get_field_name( 'display_excerpt' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'display_excerpt' ); ?>"><?php _e('Display post excerpt', 'wproto'); ?></label>  
			</p>
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['display_likes'] ); ?> id="<?php echo $this->get_field_id( 'display_likes' ); ?>" name="<?php echo $this->get_field_name( 'display_likes' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'display_likes' ); ?>"><?php _e('Display post likes', 'wproto'); ?></label>  
			</p>
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['display_views'] ); ?> id="<?php echo $this->get_field_id( 'display_views' ); ?>" name="<?php echo $this->get_field_name( 'display_views' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'display_views' ); ?>"><?php _e('Display post views', 'wproto'); ?></label>  
			</p>
			-->
			<p>
				<input class="checkbox" value="1" type="checkbox" <?php checked( $instance['display_comments_count'] ); ?> id="<?php echo $this->get_field_id( 'display_comments_count' ); ?>" name="<?php echo $this->get_field_name( 'display_comments_count' ); ?>" />
				<label for="<?php echo $this->get_field_id( 'display_comments_count' ); ?>"><?php _e('Display comments count', 'wproto'); ?></label>  
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'count' ); ?>"><?php _e('Posts count:', 'wproto'); ?></label>
				<select name="<?php echo $this->get_field_name( 'count' ); ?>" id="<?php echo $this->get_field_id( 'count' ); ?>" class="widefat">
					<?php for( $i=1; $i<11; $i++ ): ?>
					<option <?php echo $instance['count'] == $i ? 'selected="selected"' : ''; ?> value="<?php echo $i; ?>"><?php echo $i; ?></option>
					<?php endfor; ?>
				</select>
			</p>
			<?php
		}
		
	}