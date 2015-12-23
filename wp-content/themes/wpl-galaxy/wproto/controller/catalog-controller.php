<?php
/**
 * Catalog custom post type controller
 **/
class wpl_galaxy_wp_catalog_controller extends wpl_galaxy_wp_base_controller {

	function __construct() {
		// Security: Admin only
		if ( is_admin() ) {
			// Add custom meta boxes
			add_action( 'add_meta_boxes', array( $this, 'add_edit_metaboxes' ) );
			
			add_action( 'admin_footer', array( $this, 'add_info_box'));
			// Save custom data
			add_action( 'save_post', array( $this, 'save_custom_meta' ) );
			// Admin screen filters
			add_filter( 'manage_edit-wproto_catalog_columns', array( $this, 'manage_admin_columns' ) );
			add_action( 'manage_wproto_catalog_posts_custom_column', array( $this, 'get_admin_columns' ), 10, 2);
			add_filter( 'manage_edit-wproto_catalog_sortable_columns', array( $this, 'manage_sortable_columns' ));
			add_filter( 'request', array( $this, 'make_sortable_request' ) );
			
			// Post filters
			add_action( 'restrict_manage_posts', array( $this, 'add_posts_admin_filters' ) );
			add_filter( 'parse_query', array( $this, 'add_posts_admin_query_filters' ) );

		}
	}
	
	/**
	 * Add info box
	 **/
	function add_info_box() {
		$screen = get_current_screen();
		$hide_infobox = $this->get_option( 'hide_infobox', 'general' );
		// Add - edit sidebars screen
		if( $hide_infobox != 'yes' && ( isset( $screen->base ) && $screen->base == 'edit' ) && $_GET['post_type'] == 'wproto_catalog' && $_GET['page'] != 'wproto-catalog-layout-editor' ):
			$this->view->load_partial( 'infobox/infobox', array('title' => __( 'Catalog', 'wproto'), 'content' => '<p>' . __( 'Use these posts to store your products at website. Plase this as part of website, part of the content or as a widget.', 'wproto') . '</p>') );
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
			,'wproto_catalog'
			,'side'
			,'high'
		);
		
		add_meta_box(
			'wproto_meta_likes'
			,__( 'Catalog Item Rating', 'wproto' )
			,array( $this, 'render_meta_box_likes' )
			,'wproto_catalog'
			,'side'
			,'high'
		);
		
		add_meta_box(
			'wproto_meta_catalog_overview'
			,__( 'Overview', 'wproto' )
			,array( $this, 'render_meta_box_overview' )
			,'wproto_catalog'
			,'normal'
			,'high'
		);
		
		add_meta_box(
			'wproto_meta_catalog'
			,__( 'Catalog item options', 'wproto' )
			,array( $this, 'render_meta_box_catalog' )
			,'wproto_catalog'
			,'normal'
			,'default'
		);
		
		add_meta_box(
			'wproto_meta_attached_images'
			,__( 'Attached Images', 'wproto' )
			,array( $this, 'render_meta_box_attached_images' )
			,'wproto_catalog'
			,'normal'
			,'default'
		);
		
		remove_meta_box( 'postcustom', 'wproto_catalog', 'normal');
		remove_meta_box( 'slugdiv', 'wproto_catalog', 'normal');
		
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
	 * Render "Overview" metabox
	 **/
	function render_meta_box_overview() {
		global $post;
		$data = array();
		$data['overview_text'] = get_post_meta( $post->ID, 'overview_text', true );
		$this->view->load_partial( 'metaboxes/catalog_overview', $data );
	}
	
	/**
	 * Render "Catalog" options metabox
	 **/
	function render_meta_box_catalog() {
		global $post;
		$data = array();
		$data['price'] = get_post_meta( $post->ID, 'price', true );
		$data['old_price'] = get_post_meta( $post->ID, 'old_price', true );
		$data['sku'] = get_post_meta( $post->ID, 'sku', true );
		$data['link_to_buy'] = get_post_meta( $post->ID, 'link_to_buy', true );
		$data['badge'] = get_post_meta( $post->ID, 'badge', true );
		
		$this->view->load_partial( 'metaboxes/catalog', $data );
	}
	
	/**
	 * Render "Attached images" meta box
	 **/
	function render_meta_box_attached_images() {
		global $post;
		$data = array();
		$data['images'] = get_post_meta( $post->ID, 'wproto_attached_images', true );
		$this->view->load_partial( 'metaboxes/attached_images', $data );
	}
	
	/**
	 * Save custom fields
	 **/
	function save_custom_meta( $post_id ) {
		
		$post_type = get_post_type( $post_id );
		
		if( $post_type == 'wproto_catalog' ) {
			
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
			update_post_meta( $post_id, "price", isset( $_POST["price"] ) ? wp_kses( $_POST["price"], $allowed_tags ) : 0 );
			update_post_meta( $post_id, "link_to_buy", isset( $_POST["link_to_buy"] ) ? wp_kses( $_POST["link_to_buy"], $allowed_tags ) : '' );
			update_post_meta( $post_id, "wproto_likes", isset( $_POST["wproto_likes"] ) ? absint( $_POST["wproto_likes"] ) : 0 );
			update_post_meta( $post_id, "wproto_views", isset( $_POST["wproto_views"] ) ? absint( $_POST["wproto_views"] ) : 0 );
			
			update_post_meta( $post_id, "sku", isset( $_POST["sku"] ) ? wp_kses( $_POST["sku"], $allowed_tags ) : '' );
			update_post_meta( $post_id, "badge", isset( $_POST["badge"] ) ? wp_kses( $_POST["badge"], $allowed_tags ) : '' );
			update_post_meta( $post_id, "old_price", isset( $_POST["old_price"] ) ? wp_kses( $_POST["old_price"], $allowed_tags ) : '' );
			
			update_post_meta( $post_id, "overview_text", isset( $_POST["overview_text"] ) ? wp_kses( $_POST["overview_text"], $allowed_tags ) : '' );
			
		}
		
	}
	
	/**
	 * Manage admin columns
	 **/
	function manage_admin_columns( $columns ) {
	
		$likes_on_posts = $this->get_option( 'likes_on_posts', 'general' );
	
		$new_columns['cb'] = '<input type="checkbox" />';
		$new_columns['image'] = __( 'Image', 'wproto');
		$new_columns['title'] = __( 'Title', 'wproto' );
		$new_columns['price'] = __( 'Price', 'wproto' );
		if( $likes_on_posts == 'yes' ) $new_columns['rating'] = __( 'Likes', 'wproto');
		$new_columns['views'] = __( 'Views', 'wproto');
		$new_columns['is_featured'] = __( 'Featured', 'wproto');
		$new_columns['category'] = __( 'Categories', 'wproto');
		$new_columns['tag'] = __( 'Tags', 'wproto');
		$new_columns['date'] = __( 'Date', 'wproto' );
		
		return $new_columns;
	}
	
	/**
	 * Get the data for admin columns
	 **/
	function get_admin_columns( $column_name, $id ) {
		global $wpl_galaxy_wp;
		
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
				$terms = get_the_terms( $id, 'wproto_catalog_category' );
				$this->view->load_partial( 'admin_filters/list_categories', array( 'terms' => $terms ) );
			break;
			case 'tag':
				$terms = get_the_terms( $id, 'wproto_catalog_tag' );
				$this->view->load_partial( 'admin_filters/list_categories', array( 'terms' => $terms ) );
			break;
			case 'price':
				$price = get_post_meta( $id, 'price', true );
				
				$catalog_currency = $wpl_galaxy_wp->get_option( 'catalog_currency', 'general' );
				$catalog_currency = $catalog_currency != NULL ? $catalog_currency : '$';
				
				$catalog_currency_display = $wpl_galaxy_wp->get_option( 'catalog_currency_display', 'general' );
				$catalog_currency_display = $catalog_currency_display != NULL ? $catalog_currency_display : 'before';
				
				if( $price <> '') {
					
					echo $catalog_currency_display == 'before' ? $catalog_currency . ' ' . $price : $price . ' ' . $catalog_currency;
					
				}

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
		$columns['price'] = 'price';
		$columns['rating'] = 'rating';
		$columns['views'] = 'views';
  	return $columns;
	}
	
	/**
	 * Sortable by custom column, change request
	 **/
	function make_sortable_request( $vars ) {
		if ( isset( $vars['orderby'] ) && 'price' == $vars['orderby'] ) {
			$vars = array_merge( $vars, array(
				'meta_key' => 'price',
				'orderby' => 'meta_value_num'
			));
		}
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
		$type = get_post_type( $post );
		if ( $type == 'wproto_catalog' ) {
			$data = array( 'typenow' => $type );
			$data['wp_query'] = $wp_query;
			$data['taxonomy'] = 'wproto_catalog_category';
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
			
		if ( get_post_type( $post ) == 'wproto_catalog' ) {
			
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
						'taxonomy' => 'wproto_catalog_category',
						'terms' => $_GET['filter_by_category'] 
					)
				));
			}
				
		}
		
	}
	
}