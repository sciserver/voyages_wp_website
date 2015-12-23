<?php
/**
 * Team custom post type controller
 **/
class wpl_galaxy_wp_team_controller extends wpl_galaxy_wp_base_controller {

	function __construct() {
		// Security: Admin only
		if ( is_admin() ) {
			add_action( 'admin_menu', array( $this, 'remove_meta_box' ) );
			add_filter( 'manage_edit-wproto_team_columns', array( $this, 'manage_admin_columns' ) );
			add_action( 'manage_wproto_team_posts_custom_column', array( $this, 'get_admin_columns' ), 10, 2);
			// add info box
			add_action( 'admin_footer', array( $this, 'add_info_box'));
			
			// Filter by category
			add_action( 'restrict_manage_posts', array( $this, 'add_flter_posts_by_category' ) );
			add_filter( 'parse_query', array( $this, 'add_posts_query_filter' ) );
			
			// Add custom meta boxes
			add_action( 'add_meta_boxes', array( $this, 'add_edit_metaboxes' ) );
			
			// Save custom data
			add_action( 'save_post', array( $this, 'save_custom_meta' ) );
		}
	}
	
	/**
	 * Save custom fields
	 **/
	function save_custom_meta( $post_id ) {
		
		$post_type = get_post_type( $post_id );
		
		if( $post_type == 'wproto_team' ) {
			
			// Stop WP from clearing custom fields on autosave
			if ( defined( 'DOING_AUTOSAVE') && DOING_AUTOSAVE )
				return;

			// Prevent quick edit from clearing custom fields
			if ( defined( 'DOING_AJAX') && DOING_AJAX )
				return;

			if( empty( $_POST) )
				return;
			
			$allowed_tags = wp_kses_allowed_html( 'post' );
			
			update_post_meta( $post_id, "age", isset( $_POST["age"] ) ? wp_kses( $_POST["age"], $allowed_tags ) : '' );
			update_post_meta( $post_id, "position", isset( $_POST["position"] ) ? wp_kses( $_POST["position"], $allowed_tags ) : '' );
			update_post_meta( $post_id, "experience", isset( $_POST["experience"] ) ? wp_kses( $_POST["experience"], $allowed_tags ) : '' );
			update_post_meta( $post_id, "twitter_url", isset( $_POST["twitter_url"] ) ? wp_kses( $_POST["twitter_url"], $allowed_tags ) : '' );
			update_post_meta( $post_id, "facebook_url", isset( $_POST["facebook_url"] ) ? wp_kses( $_POST["facebook_url"], $allowed_tags ) : '' );
			update_post_meta( $post_id, "linkedin_url", isset( $_POST["linkedin_url"] ) ? wp_kses( $_POST["linkedin_url"], $allowed_tags ) : '' );
			
		}
		
	}
	
	/**
	 * Add custom metaboxes
	 **/
	function add_edit_metaboxes() {
		
		add_meta_box(
			'wproto_meta_featured'
			,__( 'Public information', 'wproto' )
			,array( $this, 'render_meta_box_public_info' )
			,'wproto_team'
			,'side'
			,'default'
		);
		
	}
	
	function render_meta_box_public_info() {
		global $post;
		$data = array();
		$data['age'] = get_post_meta( $post->ID, 'age', true );
		$data['position'] = get_post_meta( $post->ID, 'position', true );
		$data['experience'] = get_post_meta( $post->ID, 'experience', true );
		$data['twitter_url'] = get_post_meta( $post->ID, 'twitter_url', true );
		$data['facebook_url'] = get_post_meta( $post->ID, 'facebook_url', true );
		$data['linkedin_url'] = get_post_meta( $post->ID, 'linkedin_url', true );
		
		$this->view->load_partial( 'metaboxes/team_member', $data );
	}
	
	/**
	 * Manage admin columns
	 **/
	function manage_admin_columns( $columns ) {
		$new_columns['cb'] = '<input type="checkbox" />';
		$new_columns['image'] = __( 'Photo', 'wproto');
		$new_columns['title'] = __( 'Name', 'wproto' );
		$new_columns['text'] = __( 'Text', 'wproto' );
		$new_columns['category'] = __( 'Categories', 'wproto');
		
		$new_columns['date'] = __( 'Date', 'wproto' );
		
		return $new_columns;
	}
	
	/**
	 * Remove unused metaboxes
	 **/
	function remove_meta_box() {
		remove_meta_box( 'postcustom', 'wproto_team', 'normal');
		remove_meta_box( 'slugdiv', 'wproto_team', 'normal');
	}
	
	/**
	 * Get the data for admin columns
	 **/
	function get_admin_columns( $column_name, $id ) {
		
		switch ( $column_name ) {
			case 'image':
				echo '<a href="' . admin_url( 'post.php?post=' . $id . '&action=edit' ) . '">';
				echo '<div class="wproto-admin-thumb">';
				if ( has_post_thumbnail() ):
				
					$thumb = wpl_galaxy_wp_utils::is_retina() ? 'wproto-admin-thumb-2x' : 'wproto-admin-thumb';
					$url_arr = wp_get_attachment_image_src( get_post_thumbnail_id( $id ), $thumb );
					
					echo '<img width="100" height="75" src="' . $url_arr[0] . '" alt="" />';
				else: 
					$img = wpl_galaxy_wp_utils::is_retina() ? 'noimage-2x.gif' : 'noimage.gif';
					echo '<img width="100" height="75" src="' . WPROTO_THEME_URL . '/images/admin/' . $img . '" alt="" />';
				endif;
				echo '</div>';
				echo '</a>';
			break;
			case 'text':
				the_excerpt();
			break;
			case 'category':
				$terms = get_the_terms( $id, 'wproto_team_category' );
				$this->view->load_partial( 'admin_filters/list_categories', array( 'terms' => $terms ) );
			break;
		}
	}
	
	/**
	 * Add info box
	 **/
	function add_info_box() {
		$screen = get_current_screen();
		$hide_infobox = $this->get_option( 'hide_infobox', 'general' );
		// Add - edit sidebars screen
		if( $hide_infobox != 'yes' && ( isset( $screen->base ) && $screen->base == 'edit' ) && $_GET['post_type'] == 'wproto_team' ):
			$this->view->load_partial( 'infobox/infobox', array('title' => __( 'Team Members', 'wproto'), 'content' => '<p>' . __( 'Team - it\'s a not public post type. Use this post type to manage your staff.', 'wproto') . '</p>' . '<p>' . __( sprintf( '<a href="%s">Use categories</a> to split these records by profession / occupation etc.', admin_url('edit-tags.php?taxonomy=wproto_team_category&post_type=wproto_team')), 'wproto') . '</p>') );
		endif; 
	}
	
	/**
	 * Filter query by category at admin screen
	 **/
	function add_flter_posts_by_category() {
		global $post, $wp_query, $wpdb;
		if ( get_post_type( $post ) == 'wproto_team' ) {
			$data = array();
			$data['wp_query'] = $wp_query;
			$data['taxonomy'] = 'wproto_team_category';
			$this->view->load_partial( 'admin_filters/category_filter', $data );
		}
	}
	
	/**
	 * Query filter by category at admin screen
	 **/
	function add_posts_query_filter( $query ) {
		
		global $post;
			
		if ( get_post_type( $post ) == 'wproto_team' ) {
				
			if( isset( $_GET['filter_by_category'] ) && $_GET['filter_by_category'] > 0 ) {
				$query->set( 'tax_query', array(
					array(
						'taxonomy' => 'wproto_team_category',
						'terms' => $_GET['filter_by_category'] 
					)
				));
			}
				
		}
		
	}

}