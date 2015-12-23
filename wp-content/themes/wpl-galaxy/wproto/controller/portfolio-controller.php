<?php
/**
 * Portfolio custom post controller
 **/
class wpl_galaxy_wp_portfolio_controller extends wpl_galaxy_wp_base_controller {

	function __construct() {
		// Security: Admin only
		if ( is_admin() ) {
			// add info box
			add_action( 'admin_footer', array( $this, 'add_info_box'));
			// Add custom meta boxes
			add_action( 'add_meta_boxes', array( $this, 'add_edit_metaboxes' ) );
			// Save custom data
			add_action( 'save_post', array( $this, 'save_custom_meta' ) );
			// Admin screen filters
			add_filter( 'manage_edit-wproto_portfolio_columns', array( $this, 'manage_admin_columns' ) );
			add_action( 'manage_wproto_portfolio_posts_custom_column', array( $this, 'get_admin_columns' ), 10, 2);
			
			// Post filters
			add_action( 'restrict_manage_posts', array( $this, 'add_posts_admin_filters' ) );
			add_filter( 'parse_query', array( $this, 'add_posts_admin_query_filters' ) );
			
			// Add sortable columns
			add_filter( 'manage_edit-wproto_portfolio_sortable_columns', array( $this, 'manage_sortable_columns' ));
			add_filter( 'request', array( $this, 'make_sortable_request' ) );
		}
		
		// load more link at home
		add_action( 'wp_ajax_wproto_home_load_portfolio_posts', array( $this, 'ajax_load_more_posts' ) );
		add_action( 'wp_ajax_nopriv_wproto_home_load_portfolio_posts', array( $this, 'ajax_load_more_posts' ) );
		
		// home portfolio filter
		add_action( 'wp_ajax_wproto_home_filter_portfolio_posts', array( $this, 'ajax_filter_home_posts' ) );
		add_action( 'wp_ajax_nopriv_wproto_home_filter_portfolio_posts', array( $this, 'ajax_filter_home_posts' ) );
		
	}
	
	/**
	 * Add info box
	 **/
	function add_info_box() {
		$screen = get_current_screen();
		$hide_infobox = $this->get_option( 'hide_infobox', 'general' );
		// Add - edit sidebars screen
		if( $hide_infobox != 'yes' && ( isset( $screen->base ) && $screen->base == 'edit' ) && $_GET['post_type'] == 'wproto_portfolio' && $_GET['page'] != 'wproto-portfolio-layout-editor' ):
			$this->view->load_partial( 'infobox/infobox', array('title' => __( 'Portfolio', 'wproto'), 'content' => '<p>' . __( 'Place here your works that you want to show to your website visitors.', 'wproto') . '</p>') );
		endif; 
	}
	
	/**
	 * Add custom metaboxes
	 **/
	function add_edit_metaboxes() {
		
		add_meta_box(
			'wproto_meta_featured'
			,__( 'Featured post', 'wproto' )
			,array( $this, 'render_meta_box_featured' )
			,'wproto_portfolio'
			,'side'
			,'high'
		);
		
		add_meta_box(
			'wproto_meta_attached_images'
			,__( 'Portfolio Images', 'wproto' )
			,array( $this, 'render_meta_box_attached_images' )
			,'wproto_portfolio'
			,'normal'
			,'default'
		);
		
		add_meta_box(
			'wproto_meta_likes'
			,__( 'Post Rating', 'wproto' )
			,array( $this, 'render_meta_box_likes' )
			,'wproto_portfolio'
			,'side'
			,'high'
		);
		
		add_meta_box(
			'wproto_meta_portfolio'
			,__( 'Portfolio link', 'wproto' )
			,array( $this, 'render_meta_box_portfolio' )
			,'wproto_portfolio'
			,'side'
			,'high'
		);
		
		remove_meta_box( 'postcustom', 'wproto_portfolio', 'normal');
		remove_meta_box( 'slugdiv', 'wproto_portfolio', 'normal');
		
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
	 * Render "Attached images" metabox
	 **/
	function render_meta_box_attached_images() {
		global $post;
		$data = array();
		$data['images'] = get_post_meta( $post->ID, 'wproto_attached_images', true );
		$this->view->load_partial( 'metaboxes/attached_images', $data );
	}
	
	/**
	 * Render "Likes" metabox
	 **/
	function render_meta_box_likes() {
		global $post;
		$data = array();
		$data['hide_likes'] = true;
		$data['views'] = get_post_meta( $post->ID, 'wproto_views', true );
		
		$this->view->load_partial( 'metaboxes/post_likes', $data );
	}
	
	/**
	 * Render options metabox
	 **/
	function render_meta_box_portfolio() {
		global $post;
		$data = array();
		$data['link'] = get_post_meta( $post->ID, 'link', true );
		
		$this->view->load_partial( 'metaboxes/portfolio', $data );
	} 
	
	/**
	 * Save custom fields
	 **/
	function save_custom_meta( $post_id ) {
		
		$post_type = get_post_type( $post_id );
		
		if( $post_type == 'wproto_portfolio' ) {
			
			// Stop WP from clearing custom fields on autosave
			if ( defined( 'DOING_AUTOSAVE') && DOING_AUTOSAVE )
				return;

			// Prevent quick edit from clearing custom fields
			if ( defined( 'DOING_AJAX') && DOING_AJAX )
				return;

			if( empty( $_POST) )
				return;
			
			$allowed_tags = wp_kses_allowed_html( 'post' );
			
			update_post_meta( $post_id, "featured", isset( $_POST["featured"] ) ? wp_kses( $_POST["featured"], $allowed_tags ) : 'no' );
			update_post_meta( $post_id, "wproto_views", isset( $_POST["wproto_views"] ) ? absint( $_POST["wproto_views"] ) : 0 );
			update_post_meta( $post_id, "link", isset( $_POST["link"] ) ? wp_kses( $_POST["link"], $allowed_tags ) : '' );
			
		}
		
	}
	
	/**
	 * Manage admin columns
	 **/
	function manage_admin_columns( $columns ) {
	
		$new_columns['cb'] = '<input type="checkbox" />';
		$new_columns['image'] = __( 'Image', 'wproto');
		$new_columns['title'] = __( 'Title', 'wproto' );
		$new_columns['views'] = __( 'Views', 'wproto');
		$new_columns['is_featured'] = __( 'Featured', 'wproto');
		$new_columns['category'] = __( 'Categories', 'wproto');
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
			case 'is_featured': 
				$this->view->load_partial( 'admin_filters/is_featured', array( 'post_id' => $id, 'is_featured' => get_post_meta( $id, 'featured', true ) ) );
			break;
			case 'category':
				$terms = get_the_terms( $id, 'wproto_portfolio_category' );
				$this->view->load_partial( 'admin_filters/list_categories', array( 'terms' => $terms ) );
			break;
			case 'views':
				$views = get_post_meta( $id, 'wproto_views', true );
				$view_img = wpl_galaxy_wp_utils::is_retina() ? 'views@2x.png' : 'views.png';
				echo absint( $views ) . ' <img width="16" height="16" src="' . WPROTO_THEME_URL . '/images/admin/' . $view_img . '" alt="" />';
			break;
		}
	}
	
	/**
	 * Filter query by category at admin screen
	 **/
	function add_posts_admin_filters() {
		global $post, $wp_query;
		if ( get_post_type( $post ) == 'wproto_portfolio' ) {
			$data = array( 'typenow' => 'wproto_portfolio' );
			$data['wp_query'] = $wp_query;
			$data['taxonomy'] = 'wproto_portfolio_category';
			$this->view->load_partial( 'admin_filters/category_filter', $data );
			$this->view->load_partial( 'admin_filters/posts_filter', $data );
			$this->view->load_partial( 'admin_filters/ajax_loader' );
		}
	}
	
	/**
	 * Query filter by category at admin screen
	 **/
	function add_posts_admin_query_filters( $query ) {
		
		global $post;
			
		if ( get_post_type( $post ) == 'wproto_portfolio' ) {
			
			if( isset( $_GET['featured'] ) && $_GET['featured'] == 'yes' ) {
				$query->set( 'meta_query', array(
					array(
						'key' => 'featured',
						'value' => 'yes'
					)
				));
			}
			
			if( isset( $_GET['filter_by_category'] ) && $_GET['filter_by_category'] > 0 ) {
				$query->set( 'tax_query', array(
					array(
						'taxonomy' => 'wproto_portfolio_category',
						'terms' => $_GET['filter_by_category'] 
					)
				));
			}
				
		}
		
	}
	
	/**
	 * Setup sortable columns
	 **/
	function manage_sortable_columns( $columns ) {
		$columns['views'] = 'views';
  	return $columns;
	}
	
	/**
	 * Sortable by custom column, change request
	 **/
	function make_sortable_request( $vars ) {
		if ( isset( $vars['orderby'] ) && 'views' == $vars['orderby'] ) {
			$vars = array_merge( $vars, array(
				'meta_key' => 'wproto_views',
				'orderby' => 'meta_value_num'
			));
		}
    return $vars;
	}
	
	/**
	 * Load more posts at homepage
	 **/
	function ajax_load_more_posts() {
		
		$max_pages = isset( $_POST['max_pages'] ) ? absint( $_POST['max_pages'] ) : 0;
		$current_page = isset( $_POST['current_page'] ) ? absint( $_POST['current_page'] ) : 1;
		$current_page = $current_page == 0 ? 1 : $current_page;
		$terms = isset( $_POST['terms'] ) ? strip_tags( $_POST['terms'] ) : '';
		
		$taxonomy_terms = explode( ',', $terms );
		$next_page = $current_page + 1;
		
		$response = array();
		
		$args = array(
			'post_type' => 'wproto_portfolio',
			'posts_per_page' => 9,
			'paged' => $next_page,
			'post_status' => 'publish'
		);
		
		if( trim( $terms ) <> '' ) {
			$args['tax_query'] = array( array(
				'taxonomy' => 'wproto_portfolio_category',
				'field' => 'id', 
				'terms' => $taxonomy_terms
			));
		}
		
		global $wpl_galaxy_wp_home_portfolio_items, $wpl_galaxy_wp_home_portfolio_pagination;
		$wpl_galaxy_wp_home_portfolio_items = new WP_Query( $args );
		$wpl_galaxy_wp_home_portfolio_pagination = true;
		
		ob_start();
		get_template_part('part-home-portfolio');
			
		$response['html'] = ob_get_clean();

		$response['current_page'] = $next_page;
			
		if( $next_page + 1 > $max_pages ) {
			$response['hide_link'] = 'yes';
		}
		
		die( json_encode( $response ) );
		
	}
	
	/**
	 * Filter home posts
	 **/
	function ajax_filter_home_posts() {
		
		$term_id = isset( $_POST['term_id'] ) ? absint( $_POST['term_id'] ) : 0;
		
		$response = array();
		
		$args = array(
			'post_type' => 'wproto_portfolio',
			'posts_per_page' => 9,
			'post_status' => 'publish'
		);
		
		if( $term_id > 0 ) {
			$args['tax_query'] = array( array(
				'taxonomy' => 'wproto_portfolio_category',
				'field' => 'id', 
				'terms' => $term_id
			));
		}
		
		global $wpl_galaxy_wp_home_portfolio_items, $wpl_galaxy_wp_home_portfolio_count;		
		$wpl_galaxy_wp_home_portfolio_items = new WP_Query( $args );
		$wpl_galaxy_wp_home_portfolio_count = array( 'publish' => $wpl_galaxy_wp_home_portfolio_items->found_posts );
		$wpl_galaxy_wp_home_portfolio_count = (object)$wpl_galaxy_wp_home_portfolio_count;
		
		ob_start();
		get_template_part('part-home-portfolio');
			
		$response['html'] = ob_get_clean();
		
		die( json_encode( $response ) );
		
	}

}