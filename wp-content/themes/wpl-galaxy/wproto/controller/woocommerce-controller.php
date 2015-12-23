<?php
/**
 * Woo Commerce support
 **/
class wpl_galaxy_wp_woocommerce_controller extends wpl_galaxy_wp_base_controller {
	
	function __construct() {
		remove_action( 'woocommerce_before_main_content', 'woocommerce_output_content_wrapper', 10 );
		remove_action( 'woocommerce_after_main_content', 'woocommerce_output_content_wrapper_end', 10 );
		if( is_admin()) {
			// Add custom meta boxes
			add_action( 'add_meta_boxes', array( $this, 'add_edit_metaboxes' ) );
			// Save custom data
			add_action( 'save_post', array( $this, 'save_custom_meta' ) );
		}		
		add_filter( 'woocommerce_enqueue_styles', '__return_false' );
		add_action( 'widgets_init', array( $this, 'override_woocommerce_widgets' ), 15 );
		// change breadcrumbs style
		add_filter( 'woocommerce_breadcrumb_defaults', array( $this, 'override_breadcrumbs_style' ) );
		
		add_filter( 'loop_shop_per_page', create_function( '$cols', 'return 12;' ), 20 );
		
		// AJAX cart header
		add_action( 'wp_ajax_wproto_header_ajax_cart', array( $this, 'ajax_header_cart' ) );
		add_action( 'wp_ajax_nopriv_wproto_header_ajax_cart', array( $this, 'ajax_header_cart' ) );
	}
	
	/**
	 * Add custom metaboxes
	 **/
	function add_edit_metaboxes() {
		
		add_meta_box(
			'wproto_meta_product'
			,__( 'Displaying options', 'wproto' )
			,array( $this, 'render_meta_box_display' )
			,'product'
			,'side'
			,'high'
		);
		
		add_meta_box(
			'wproto_meta_likes'
			,__( 'Product Item Rating', 'wproto' )
			,array( $this, 'render_meta_box_likes' )
			,'product'
			,'side'
			,'high'
		);
		
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
	 * Displaying options metabox
	 **/
	function render_meta_box_display() {
		global $post;
		$data = array();
		$data['badge'] = get_post_meta( $post->ID, 'badge', true );
		
		$this->view->load_partial( 'metaboxes/product_badges', $data );
	}
	
	/**
	 * Save custom fields
	 **/
	function save_custom_meta( $post_id ) {
		
		$post_type = get_post_type( $post_id );
		
		if( $post_type == 'product' ) {
			
			// Stop WP from clearing custom fields on autosave
			if ( defined( 'DOING_AUTOSAVE') && DOING_AUTOSAVE )
				return;

			// Prevent quick edit from clearing custom fields
			if ( defined( 'DOING_AJAX') && DOING_AJAX )
				return;

			if( empty( $_POST) )
				return;
			
			$allowed_tags = wp_kses_allowed_html( 'post' );

			update_post_meta( $post_id, "wproto_likes", isset( $_POST["wproto_likes"] ) ? absint( $_POST["wproto_likes"] ) : 0 );
			update_post_meta( $post_id, "wproto_views", isset( $_POST["wproto_views"] ) ? absint( $_POST["wproto_views"] ) : 0 );
			update_post_meta( $post_id, "badge", isset( $_POST["badge"] ) ? wp_kses( $_POST["badge"], $allowed_tags ) : '' );
			
		}
		
	}
	
	/**
	 * Override wooCommerce widgets output
	 **/
	function override_woocommerce_widgets() {
		
		$woo_widgets = array(
			//'WC_Widget_Layered_Nav',
			//'WC_Widget_Layered_Nav_Filters',
			'WC_Widget_Product_Categories',
			'WC_Widget_Products',
			'WC_Widget_Product_Search',
			'WC_Widget_Recently_Viewed',
			'WC_Widget_Recent_Reviews',
			'WC_Widget_Top_Rated_Products'
		);
		
		foreach( $woo_widgets as $widget ) {
			 if ( class_exists( $widget ) ) {
			 	unregister_widget( $widget );
		 	}
		}
		
		// load our new widgets
		$directory = WPROTO_ENGINE_DIR . '/widget/woocommerce/';
		$handle = opendir( $directory );
		
		while (false !== ($file = readdir($handle))) {
			if (is_file($directory . $file)) {
				require_once $directory . $file;
			}
		}
		
	}
	
	/**
	 * Change breadcrumbs style
	 **/
	function override_breadcrumbs_style( $defaults ) {
		
		$defaults['wrap_before'] = '<div class="breadcrumbs" id="crumbs">';
		$defaults['wrap_after'] = '</div>';
		$defaults['delimiter'] = '<i class="delimeter"></i> ';
		return $defaults;
	}
	
	/**
	 * Display AJAX cart
	 **/
	function ajax_header_cart() {
		global $woocommerce;
		
		$data = array();
		$data['cart'] = $woocommerce->cart->get_cart();
		$data['totals'] = $woocommerce->cart->get_cart_total();
		
		$this->view->load_partial( 'front/cart', $data );
		
		die;
	}
	
}
