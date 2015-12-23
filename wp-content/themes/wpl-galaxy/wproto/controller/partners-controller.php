<?php
/**
 * Partners / Clients custom post controller
 **/
class wpl_galaxy_wp_partners_controller extends wpl_galaxy_wp_base_controller {

	function __construct() {
		// Security: Admin only
		if ( is_admin() ) {
			add_action( 'admin_menu', array( $this, 'remove_meta_box' ) );
			add_filter( 'manage_edit-wproto_partners_columns', array( $this, 'manage_admin_columns' ) );
			add_action( 'manage_wproto_partners_posts_custom_column', array( $this, 'get_admin_columns' ), 10, 2);
			// add info box
			add_action( 'admin_footer', array( $this, 'add_info_box'));
			
			// Filter by category
			add_action( 'restrict_manage_posts', array( $this, 'add_flter_posts_by_category' ) );
			add_filter( 'parse_query', array( $this, 'add_posts_query_filter' ) );
		}
	}
	
	/**
	 * Manage admin columns
	 **/
	function manage_admin_columns( $columns ) {
		$new_columns['cb'] = '<input type="checkbox" />';
		$new_columns['image'] = __( 'Image', 'wproto');
		$new_columns['title'] = __( 'Title', 'wproto' );
		$new_columns['category'] = __( 'Categories', 'wproto');
		
		$new_columns['date'] = __( 'Date', 'wproto' );
		
		return $new_columns;
	}
	
	/**
	 * Remove unused metaboxes
	 **/
	function remove_meta_box() {
		remove_meta_box( 'postcustom', 'wproto_partners', 'normal');
		remove_meta_box( 'slugdiv', 'wproto_partners', 'normal');
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
			case 'category':
				$terms = get_the_terms( $id, 'wproto_partners_category' );
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
		if( $hide_infobox != 'yes' && ( isset( $screen->base ) && $screen->base == 'edit' ) && $_GET['post_type'] == 'wproto_partners' ):
			$this->view->load_partial( 'infobox/infobox', array('title' => __( 'Partners / Clients', 'wproto'), 'content' => '<p>' . __( 'It\'s a not public post type. Use this post type to manage your partners, clients etc.', 'wproto') . '</p>' . '<p>' . __( sprintf( '<a href="%s">Use categories</a> to split these records by type.', admin_url('edit-tags.php?taxonomy=wproto_partners_category&post_type=wproto_partners')), 'wproto') . '</p>') );
		endif; 
	}
	
	/**
	 * Filter query by category at admin screen
	 **/
	function add_flter_posts_by_category() {
		global $post, $wp_query;
		if ( get_post_type( $post ) == 'wproto_partners' ) {
			$data = array();
			$data['wp_query'] = $wp_query;
			$data['taxonomy'] = 'wproto_partners_category';
			$this->view->load_partial( 'admin_filters/category_filter', $data );
		}
	}
	
	/**
	 * Query filter by category at admin screen
	 **/
	function add_posts_query_filter( $query ) {
		
		global $post;
			
		if ( get_post_type( $post ) == 'wproto_partners' ) {
				
			if( isset( $_GET['filter_by_category'] ) && $_GET['filter_by_category'] > 0 ) {
				$query->set( 'tax_query', array(
					array(
						'taxonomy' => 'wproto_partners_category',
						'terms' => $_GET['filter_by_category'] 
					)
				));
			}
				
		}
		
	}

}