<?php
/**
 * Custom fields for taxonomies
 **/
class wpl_galaxy_wp_admin_taxonomy_controller extends wpl_galaxy_wp_admin_controller {
	
	function __construct() {
		
		if( is_admin() ) {
			// Add custom fields to taxonomies
			add_action( 'wproto_catalog_category_add_form_fields', array( $this, 'add_taxonomy_form_fields' ), 10, 2 );
			add_action( 'wproto_catalog_category_edit_form_fields', array( $this, 'edit_taxonomy_form_fields' ), 10, 2 );
			add_action( 'edited_wproto_catalog_category', array( $this, 'save_custom_taxonomy_meta' ), 10, 2 );  
			add_action( 'create_wproto_catalog_category', array( $this, 'save_custom_taxonomy_meta' ), 10, 2 );
			
			add_action( 'wproto_portfolio_category_add_form_fields', array( $this, 'add_taxonomy_form_fields' ), 10, 2 );
			add_action( 'wproto_portfolio_category_edit_form_fields', array( $this, 'edit_taxonomy_form_fields' ), 10, 2 );
			add_action( 'edited_wproto_portfolio_category', array( $this, 'save_custom_taxonomy_meta' ), 10, 2 );  
			add_action( 'create_wproto_portfolio_category', array( $this, 'save_custom_taxonomy_meta' ), 10, 2 );
			
			add_action( 'wproto_photoalbums_category_add_form_fields', array( $this, 'add_taxonomy_form_fields' ), 10, 2 );
			add_action( 'wproto_photoalbums_category_edit_form_fields', array( $this, 'edit_taxonomy_form_fields' ), 10, 2 );
			add_action( 'edited_wproto_photoalbums_category', array( $this, 'save_custom_taxonomy_meta' ), 10, 2 );  
			add_action( 'create_wproto_photoalbums_category', array( $this, 'save_custom_taxonomy_meta' ), 10, 2 );
			
			add_action( 'wproto_video_category_add_form_fields', array( $this, 'add_taxonomy_form_fields' ), 10, 2 );
			add_action( 'wproto_video_category_edit_form_fields', array( $this, 'edit_taxonomy_form_fields' ), 10, 2 );
			add_action( 'edited_wproto_video_category', array( $this, 'save_custom_taxonomy_meta' ), 10, 2 );  
			add_action( 'create_wproto_video_category', array( $this, 'save_custom_taxonomy_meta' ), 10, 2 );
			
			add_action( 'category_add_form_fields', array( $this, 'add_taxonomy_form_fields' ), 10, 2 );
			add_action( 'category_edit_form_fields', array( $this, 'edit_taxonomy_form_fields' ), 10, 2 );
			add_action( 'edited_category', array( $this, 'save_custom_taxonomy_meta' ), 10, 2 );  
			add_action( 'create_category', array( $this, 'save_custom_taxonomy_meta' ), 10, 2 );
			
			add_action( 'product_cat_add_form_fields', array( $this, 'add_taxonomy_form_fields' ), 10, 2 );
			add_action( 'product_cat_edit_form_fields', array( $this, 'edit_taxonomy_form_fields' ), 10, 2 );
			add_action( 'edited_product_cat', array( $this, 'save_custom_taxonomy_meta' ), 10, 2 );  
			add_action( 'create_product_cat', array( $this, 'save_custom_taxonomy_meta' ), 10, 2 );
			
			// Custom taxonomy columns
			add_filter( 'manage_edit-wproto_catalog_category_columns', array( $this, 'manage_admin_taxonomy_columns' ), 10, 1);
			add_filter( 'manage_wproto_catalog_category_custom_column', array( $this, 'get_admin_taxonomy_columns' ), 10, 3 );
			
			add_filter( 'manage_edit-wproto_portfolio_category_columns', array( $this, 'manage_admin_taxonomy_columns' ), 10, 1);
			add_filter( 'manage_wproto_portfolio_category_custom_column', array( $this, 'get_admin_taxonomy_columns' ), 10, 3 );
			
			add_filter( 'manage_edit-wproto_photoalbums_category_columns', array( $this, 'manage_admin_taxonomy_columns' ), 10, 1);
			add_filter( 'manage_wproto_photoalbums_category_custom_column', array( $this, 'get_admin_taxonomy_columns' ), 10, 3 );
			
			add_filter( 'manage_edit-wproto_video_category_columns', array( $this, 'manage_admin_taxonomy_columns' ), 10, 1);
			add_filter( 'manage_wproto_video_category_custom_column', array( $this, 'get_admin_taxonomy_columns' ), 10, 3 );
			
			add_filter( 'manage_edit-category_columns', array( $this, 'manage_admin_taxonomy_columns' ), 10, 1);
			add_filter( 'manage_category_custom_column', array( $this, 'get_admin_taxonomy_columns' ), 10, 3 );
			
			add_filter( 'manage_edit-product_cat_columns', array( $this, 'manage_admin_woo_taxonomy_columns' ), 10, 1);
			add_filter( 'manage_product_cat_custom_column', array( $this, 'get_admin_taxonomy_columns' ), 10, 3 );
			
			// Add JS & CSS
			add_action( 'admin_head', array( $this, 'add_taxonomy_scripts' ) );
		}
		
	}
	
	/**
	 * Add form fields to taxonomy
	 **/
	function add_taxonomy_form_fields() {
		global $taxonomy;
		
		$data = array();
		
		if( $taxonomy != 'product_cat' ) {
			$this->view->load_partial( 'custom_fields/category_image_add', $data );
		}
		
		$this->view->load_partial( 'custom_fields/category_featured_add', $data );
		$this->view->load_partial( 'custom_fields/category_new_add', $data );
	}
	
	/**
	 * Edit taxonomy screen fields
	 **/
	function edit_taxonomy_form_fields( $term ) {
		global $taxonomy;
		
		$data = array();
		$term_id = $term->term_id;
		$data['meta'] = get_option( "taxonomy_$term_id" );		
		$data['category_image_id'] = isset( $data['meta']['category_image_id'] ) ? $data['meta']['category_image_id'] : '';
		$data['category_featured'] = isset( $data['meta']['category_featured'] ) ? $data['meta']['category_featured'] : '';
		$data['category_new'] = isset( $data['meta']['category_new'] ) ? $data['meta']['category_new'] : '';
		
		if( $taxonomy != 'product_cat' ) {
			$this->view->load_partial( 'custom_fields/category_image_edit', $data );
		}
		$this->view->load_partial( 'custom_fields/category_featured_edit', $data );
		$this->view->load_partial( 'custom_fields/category_new_edit', $data );
	}
	
	/**
	 * Save custom taxonomy meta
	 **/
	function save_custom_taxonomy_meta( $term_id ) {
		if ( isset( $_POST['term_meta'] ) ) {
			$term_meta = get_option( "taxonomy_$term_id" );
			$cat_keys = array_keys( $_POST['term_meta'] );
			foreach ( $cat_keys as $key ) {
				if ( isset ( $_POST['term_meta'][$key] ) ) {
					$term_meta[$key] = $_POST['term_meta'][$key];
				}
			}
			// Save the option array.
			update_option( "taxonomy_$term_id", $term_meta );
		}
	}
	
	/**
	 * Add taxonomy columns
	 **/
	function manage_admin_taxonomy_columns( $columns ) {
		$columns_local = array();
    if ( isset( $columns['cb'])) {
			$columns_local['cb'] = $columns['cb'];
			unset( $columns['cb'] );
    }
    if ( isset( $columns['name'])) {
			$columns_local['name'] = $columns['name'];
			unset( $columns['name'] );
    }
    
    $columns_local['category_image'] = __( 'Image', 'wproto' );
    $columns_local['category_featured'] = __( 'Featured', 'wproto' );
    $columns_local['category_new'] = __( 'New', 'wproto' );
    
    return array_merge( $columns_local, $columns);
	}
	
	function manage_admin_woo_taxonomy_columns( $columns ) {		
    $columns['category_featured'] = __( 'Featured', 'wproto' );
    $columns['category_new'] = __( 'New', 'wproto' );
    return $columns;
	}
	
	/**
	 * Add taxonomy clolumns values
	 **/
	function get_admin_taxonomy_columns( $row_content, $column_name, $term_id ) {
		
		$data['meta'] = get_option( "taxonomy_$term_id" );
		
		if( $column_name == 'category_image' ) {
			
			$image_id = $data['meta']['category_image_id'];
			
			if( $image_id == 0 ) {
				$image_preview = wpl_galaxy_wp_utils::is_retina() ? WPROTO_THEME_URL . '/images/admin/category-no-image@2x.jpg' : WPROTO_THEME_URL . '/images/admin/category-no-image.jpg';
			} else {
				$thumb_name = wpl_galaxy_wp_utils::is_retina() ? 'wproto-admin-category-thumb-2x' : 'wproto-admin-category-thumb';
				$image_preview = wp_get_attachment_image_src( $image_id, $thumb_name );
				$image_preview = @$image_preview[0];
			}
			
			echo '<img src="' . $image_preview . '" width="100" class="wproto-cat-column-image" height="75" alt="" />';
			
		}
		
		if( $column_name == 'category_featured' ) {
			echo $data['meta']['category_featured'] == 'yes' ? __('Yes', 'wproto') : __('No', 'wproto');
		}
		
		if( $column_name == 'category_new' ) {
			echo $data['meta']['category_new'] == 'yes' ? __('Yes', 'wproto') : __('No', 'wproto');
		}
		
		if( wpl_galaxy_wp_utils::isset_woocommerce() ) {
			global $woocommerce;
		
			if ( $column_name == 'thumb' ) {

				$image = '';
				$thumbnail_id = get_woocommerce_term_meta( $term_id, 'thumbnail_id', true );
				if( $thumbnail_id ) {
					$image = wp_get_attachment_url( $thumbnail_id );
				} else {
					$image = woocommerce_placeholder_img_src();
				}
				echo '<img src="' . $image . '" alt="Thumbnail" class="wp-post-image" height="48" width="48" />';
			}

		}
		
	}
	
	/**
	 * Add JS Scripts
	 **/
	function add_taxonomy_scripts() {
		
		$tax = isset( $_GET['taxonomy'] ) ? $_GET['taxonomy'] : '';
		
		if( in_array( $tax, array( 'wproto_catalog_category', 'category', 'wproto_video_category', 'wproto_photoalbums_category', 'wproto_catalog_category', 'wproto_portfolio_category' ) ) ) {
			wp_register_script( 'wproto-catalog-category', WPROTO_THEME_URL . '/js/admin/screen-taxonomy.js?' . $this->settings['res_cache_time'] );
			wp_enqueue_script( 'wproto-catalog-category', array( 'jquery' ) );
		}
		
	}
	
	
}