<?php
/**
 *
 **/
class wpl_galaxy_wp_post_controller extends wpl_galaxy_wp_base_controller {

	function __construct() {
		// Security: Admin only
		if ( is_admin() ) {

			// Add custom meta boxes
			add_action( 'add_meta_boxes', array( $this, 'add_metaboxes' ) );
			// Save custom data
			add_action( 'save_post', array( $this, 'save_custom_meta' ) );
			
			// Admin screen filters
			add_filter( 'manage_edit-post_columns', array( $this, 'manage_admin_columns' ) );
			add_action( 'manage_post_posts_custom_column', array( $this, 'get_admin_columns' ), 10, 2);
			
			// Add sortable columns
			add_filter( 'manage_edit-post_sortable_columns', array( $this, 'manage_sortable_columns' ));
			add_filter( 'request', array( $this, 'make_sortable_request' ) );
			
			// Post filters
			add_action( 'restrict_manage_posts', array( $this, 'add_posts_admin_filters' ) );
			add_filter( 'parse_query', array( $this, 'add_posts_admin_query_filters' ) );
			
			// Pages admin filters
			add_action( 'restrict_manage_posts', array( $this, 'add_pages_admin_filters' ) );
			add_filter( 'parse_query', array( $this, 'add_pages_admin_query_filters' ) );
			add_filter( 'manage_edit-page_columns', array( $this, 'manage_pages_admin_columns' ) );
			add_action( 'manage_page_posts_custom_column', array( $this, 'get_pages_admin_columns' ), 10, 2);

		}
		
		add_action( 'wp_ajax_wproto_ajax_filter_hexagon_posts', array( $this, 'ajax_filter_hexagon_posts' ) );
		add_action( 'wp_ajax_nopriv_wproto_ajax_filter_hexagon_posts', array( $this, 'ajax_filter_hexagon_posts' ) );

	}
	
	/**
	 * Add custom metaboxes
	 **/
	function add_metaboxes() {
		
		if ( current_user_can( 'edit_pages' ) ):
		
		add_meta_box(
			'wproto_meta_featured'
			,__( 'Featured post', 'wproto' )
			,array( $this, 'render_meta_box_featured' )
			,'post'
			,'side'
			,'high'
		);
		
		add_meta_box(
			'wproto_meta_likes'
			,__( 'Post Rating', 'wproto' )
			,array( $this, 'render_meta_box_likes' )
			,'post'
			,'side'
			,'high'
		);
		
		endif;
		
	}
	
	/**
	 * Render "Featured" metabox
	 **/
	function render_meta_box_featured() {
		global $post;
		$data = array();
		$data['featured'] = get_post_meta( $post->ID, 'featured', true );
		
		$this->view->load_partial( 'metaboxes/post_featured', $data );
	}
	
	/**
	 * Render "Likes" metabox
	 **/
	function render_meta_box_likes() {
		global $post;
		$data = array();
		$data['likes'] = get_post_meta( $post->ID, 'wproto_likes', true );
		$data['views'] = get_post_meta( $post->ID, 'wproto_views', true );
		
		$likes_enabled = $this->get_option( 'likes_on_posts', 'general' );
		if( $likes_enabled == 'no' ) {
			$data['hide_likes'] = true;
		}
		
		$this->view->load_partial( 'metaboxes/post_likes', $data );
	}
	
	/**
	 * Save custom fields
	 **/
	function save_custom_meta( $post_id ) {
		
		$post_type = get_post_type( $post_id );
		
		if( $post_type == 'post' ) {
			
			// Stop WP from clearing custom fields on autosave
			if ( defined( 'DOING_AUTOSAVE') && DOING_AUTOSAVE )
				return;

			// Prevent quick edit from clearing custom fields
			if ( defined( 'DOING_AJAX') && DOING_AJAX )
				return;

			if( empty( $_POST) )
				return;
				
			if ( current_user_can( 'edit_pages' ) ):
				
				update_post_meta( $post_id, "featured", isset( $_POST["featured"] ) ? $_POST["featured"] : 'no' );
				update_post_meta( $post_id, "wproto_likes", isset( $_POST["wproto_likes"] ) ? absint( $_POST["wproto_likes"] ) : 0 );
				update_post_meta( $post_id, "wproto_views", isset( $_POST["wproto_views"] ) ? absint( $_POST["wproto_views"] ) : 0 );
				
			endif;
			
		}
		
	}
	
	/**
	 * Manage admin columns
	 **/
	function manage_admin_columns( $columns ) {
	
		$likes_on_posts = $this->get_option( 'likes_on_posts', 'general' );;
	
		$new_columns['cb'] = '<input type="checkbox" />';
		$new_columns['image'] = __( 'Photo', 'wproto');
		$new_columns['title'] = __( 'Name', 'wproto' );
		$new_columns['comments'] = '<span class="vers"><div class="comment-grey-bubble"></div></span>';
		
		if( $likes_on_posts != 'no' ) $new_columns['rating'] = __( 'Likes', 'wproto');
		
		$new_columns['views'] = __( 'Views', 'wproto');
		
		if ( current_user_can( 'edit_pages' ) ):
		
			$new_columns['is_sticky'] = __( 'Sticky', 'wproto');
			$new_columns['is_featured'] = __( 'Featured', 'wproto');
			
		endif;
			
		$new_columns['tags'] = __( 'Tags', 'wproto');
		$new_columns['categories'] = __( 'Categories', 'wproto');
		$new_columns['author'] = __( 'Author', 'wproto' );
		$new_columns['date'] = __( 'Date', 'wproto' );
		
		return $new_columns;
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
			case 'is_sticky': 
				$this->view->load_partial( 'admin_filters/is_sticky', array( 'post_id' => $id ) );
			break;
			case 'is_featured': 
				$this->view->load_partial( 'admin_filters/is_featured', array( 'post_id' => $id, 'is_featured' => get_post_meta( $id, 'featured', true ) ) );
			break;
			case 'rating':
			
				$likes = get_post_meta( $id, 'wproto_likes', true );
				$like_img = wpl_galaxy_wp_utils::is_retina() ? 'like@2x.png' : 'like.png';
				echo absint( $likes ) . ' <img width="16" height="16" src="' . WPROTO_THEME_URL . '/images/admin/' . $like_img . '" alt="" />';
			
			break;
			case 'views':
				$views = get_post_meta( $id, 'wproto_views', true );
				$view_img = wpl_galaxy_wp_utils::is_retina() ? 'views@2x.png' : 'views.png';
				echo absint( $views ) . ' <img width="16" height="16" src="' . WPROTO_THEME_URL . '/images/admin/' . $view_img . '" alt="" />';
			break;
		}
	}
	
	/**
	 * Setup sortable columns
	 **/
	function manage_sortable_columns( $columns ) {
		$columns['rating'] = 'rating';
		$columns['views'] = 'views';
  	return $columns;
	}
	
	/**
	 * Sortable by custom column, change request
	 **/
	function make_sortable_request( $vars ) {
		if ( isset( $vars['orderby'] ) && 'rating' == $vars['orderby'] ) {
			$vars = array_merge( $vars, array(
				'meta_key' => 'wproto_likes',
				'orderby' => 'meta_value_num'
			));
		}
		if ( isset( $vars['orderby'] ) && 'views' == $vars['orderby'] ) {
			$vars = array_merge( $vars, array(
				'meta_key' => 'wproto_views',
				'orderby' => 'meta_value_num'
			));
		}
    return $vars;
	}
	
	/**
	 * Filter query by category at admin screen
	 **/
	function add_posts_admin_filters() {
		global $post, $wp_query;
		if ( get_post_type( $post ) == 'post' ) {
			$data = array( 'typenow' => 'post' );
			$this->view->load_partial( 'admin_filters/posts_filter', $data );
			$this->view->load_partial( 'admin_filters/ajax_loader' );
		}
	}
	
	
	/**
	 * Query filter by category at admin screen
	 **/
	function add_posts_admin_query_filters( $query ) {
			
		if( isset( $_GET['featured'] ) && $_GET['featured'] == 'yes' ) {
			$query->set( 'meta_query', array(
				array(
					'key' => 'featured',
					'value' => 'yes'
				)
			));
		}
			
		if( isset( $_GET['post_format'] ) && $_GET['post_format'] <> '' ) {
			$query->set( 'tax_query', array(
				array(
					'taxonomy' => 'post_format',
					'field' => 'slug',
					'terms' => array( $_GET['post_format'] )
				)
			));
		}
		
	}
	
	/**
	 * Filter query by category at admin screen
	 **/
	function add_pages_admin_filters() {
		global $typenow;
		if ( $typenow == 'page' ) {
			$tpls = get_page_templates();
			ksort( $tpls );
			$data['templates'] = $tpls;
			$this->view->load_partial( 'admin_filters/pages_filter', $data );
		}
	}
	
	/**
	 * Query filter by category at admin screen
	 **/
	function add_pages_admin_query_filters( $query ) {
		
		global $typenow;
			
		if ( $typenow == 'page' ) {
				
			if( isset( $_GET['page_template'] ) && trim( $_GET['page_template'] ) != '' ) {
				$query->set( 'meta_query', array(
					array(
						'key' => '_wp_page_template',
						'value' => $_GET['page_template']
					)
				));
			}
			
			if( isset( $_GET['page_redirect'] ) && trim( $_GET['page_redirect'] ) != '' ) {
				$query->set( 'meta_query', array(
					array(
						'key' => 'wproto_redirect_enabled',
						'value' => 'yes'
					)
				));
			}

				
		}
		
	}
	
	/**
	 * Manage admin columns
	 **/
	function manage_pages_admin_columns( $columns ) {
	
		$new_columns['cb'] = '<input type="checkbox" />';
		$new_columns['title'] = __( 'Title', 'wproto' );
		$new_columns['page_template'] = __( 'Page template', 'wproto');
		$new_columns['author'] = __( 'Author', 'wproto');
		$new_columns['date'] = __( 'Date', 'wproto' );
		
		return $new_columns;
	}
	
	/**
	 * Get the data for admin columns
	 **/
	function get_pages_admin_columns( $column_name, $id ) {
		switch ( $column_name ) {
			case 'page_template':
				echo ucwords( str_replace( '_', ' ', str_replace( '-', ' ', str_replace( 'page-tpl', '',  str_replace( '.php', '', basename( get_page_template() ) ) ) ) ) );
			break;
		}
	}
	
	/**
	 * Filter hexagon posts via AJAX
	 **/
	function ajax_filter_hexagon_posts() {
		
		$term_id = isset( $_POST['term_id'] ) ? absint( $_POST['term_id'] ) : 0;
		$post_type = isset( $_POST['post_type'] ) ? strip_tags( $_POST['post_type'] ) : '';
		$posts_per_page = isset( $_POST['posts_per_page'] ) ? absint( $_POST['posts_per_page'] ) : get_option('posts_per_page');
		$tax_name = isset( $_POST['taxonomy_name'] ) ? strip_tags( $_POST['taxonomy_name'] ) : '';
		
		$response = array();
		
		$args = array(
			'post_type' => $post_type,
			'posts_per_page' => $posts_per_page,
			'post_status' => 'publish'
		);
		
		if( $term_id > 0 ) {
			$args['tax_query'] = array( array(
				'taxonomy' => $tax_name,
				'field' => 'id', 
				'terms' => $term_id
			));
		}
		
		global $wpl_galaxy_wp_ajax_pagination, $wp_query;
		$wpl_galaxy_wp_ajax_pagination = true;
		
		$wp_query = new WP_Query( $args );
		
		ob_start();
		get_template_part( 'layouts/hexagon' );
			
		$response['html'] = ob_get_clean();
		$response['max_pages'] = $wp_query->max_num_pages;
		
		if( $wp_query->max_num_pages <= 1 ) {
			$response['hide_link'] = 'yes';
		}
		
		die( json_encode( $response ) );
		
	}
	
}