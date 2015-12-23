<?php

	add_action( 'widgets_init', 'register_wpl_galaxy_wp_photoalbums_widget' );
	
	function register_wpl_galaxy_wp_photoalbums_widget() {
		register_widget( 'wpl_galaxy_wp_photoalbums_widget' );
	}
	
	class wpl_galaxy_wp_photoalbums_widget extends WP_Widget {
		
		function __construct() {
			$widget_ops = array( 'classname' => 'wproto-photoalbums-widget', 'description' => __('A widget that displays the photoalbums. ', 'wproto') );
		
			$control_ops = array( 'width' => 300, 'height' => 350, 'id_base' => 'wproto-photoalbums-widget' );
		
			$this->WP_Widget( 'wproto-photoalbums-widget', __( '&laquo;Galaxy&raquo; Photoalbums', 'wproto' ), $widget_ops, $control_ops );
		}
		
		function widget( $args, $instance ) {
			global $wpl_galaxy_wp;
			
			$data = array();
			$data['title'] = apply_filters( 'widget_title', $instance['title'] );
			
			$data['instance'] = $instance;
			$data['args'] = $args;

			$wpl_galaxy_wp->view->load_partial( 'widgets/photoalbums', $data );
		}
		
		function update( $new_instance, $old_instance ) {
			$instance = $old_instance;

			//Strip tags from title and name to remove HTML 
			$instance['title'] = strip_tags( str_replace( '\'', "&#39;", $new_instance['title'] ) );

			$instance['posts_count'] = isset( $new_instance['posts_count'] ) ? absint( $new_instance['posts_count'] ) : 1;
			$instance['album'] = isset( $new_instance['album'] ) ? absint( $new_instance['album'] ) : 0;
			$instance['link_to'] = isset( $new_instance['link_to'] ) ? strip_tags( $new_instance['link_to'] ) : 'file';

			return $instance;
		}
		
		function form( $instance ) {
			
			//Set up some default widget settings.

			$defaults = array(
				'title' => __( 'Photoalbums', 'wproto' ),
				'posts_count' => 5,
				'album' => '',
				'link_to' => 'file'
			);
			
			$instance = wp_parse_args( (array) $instance, $defaults );
			
			?>
			<p>
				<label for="<?php echo $this->get_field_id( 'title' ); ?>"><?php _e('Widget title:', 'wproto'); ?></label>
				<input class="widefat" type="text" id="<?php echo $this->get_field_id( 'title' ); ?>" name="<?php echo $this->get_field_name( 'title' ); ?>" value="<?php echo $instance['title']; ?>" />
			</p>
			<p>
				<strong><?php _e('Displaying', 'wproto'); ?>:</strong>
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'posts_count' ); ?>"><?php _e('Number of photos to display:', 'wproto'); ?></label>
				<input class="widefat" type="number" min="1" name="<?php echo $this->get_field_name( 'posts_count' ); ?>" id="<?php echo $this->get_field_id( 'posts_count' ); ?>" value="<?php echo $instance['posts_count']; ?>" />
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'album' ); ?>"><?php _e('Select photoalbum:', 'wproto'); ?></label>
				<select class="widefat" id="<?php echo $this->get_field_id( 'album' ); ?>" name="<?php echo $this->get_field_name( 'album' ); ?>">
					<?php
						global $wpl_galaxy_wp;
						$photoalbums = $wpl_galaxy_wp->model->post->get( '', -1, 0, 'date', 'DESC', 'wproto_photoalbums', 'wproto_photoalbums_category' );
						while( $photoalbums->have_posts() ): $photoalbums->the_post();
					?>
					<option <?php echo get_the_ID() == $instance['album'] ? 'selected="selected"' : ''; ?> value="<?php the_ID(); ?>"><?php the_title(); ?></option>
					<?php
						endwhile;
					?>
				</select>
			</p>
			<p>
				<label for="<?php echo $this->get_field_id( 'link_to' ); ?>"><?php _e('Link to:', 'wproto'); ?></label>
				<select class="widefat" id="<?php echo $this->get_field_id( 'link_to' ); ?>" name="<?php echo $this->get_field_name( 'link_to' ); ?>">
					<option <?php echo $instance['link_to'] == 'file' ? 'selected="selected"' : ''; ?> value="file"><?php _e( 'File (will be opened at LightBox)', 'wproto' ); ?></option>
					<option <?php echo $instance['link_to'] == 'post' ? 'selected="selected"' : ''; ?> value="post"><?php _e( 'Photo Album', 'wproto' ); ?></option>
				</select>
			</p>
			<?php
		}
		
	}