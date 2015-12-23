<?php
/**
 * Pricing tables custom post type controller
 **/
class wpl_galaxy_wp_pricing_tables_controller extends wpl_galaxy_wp_base_controller {

	function __construct() {
		// Security: Admin only
		if ( is_admin() ) {
			// add info box
			add_action( 'admin_footer', array( $this, 'add_info_box'));
			add_action( 'admin_enqueue_scripts', array( $this, 'add_scripts' ) );
			// Add custom meta boxes
			add_action( 'add_meta_boxes', array( $this, 'add_edit_metaboxes' ) );
			// Save custom data
			add_action( 'save_post', array( $this, 'save_custom_meta' ) );

		}
	}
	
	/**
	 * Add info box
	 **/
	function add_info_box() {
		
		$screen = get_current_screen();
		
		$hide_infobox = $this->get_option( 'hide_infobox', 'general' );
		// Add - edit sidebars screen
		if( $hide_infobox != 'yes' && (isset( $screen->base ) && $screen->base == 'edit') && $_GET['post_type'] == 'wproto_pricing_table' && $_GET['page'] != 'wproto-catalog-layout-editor' ):
			$this->view->load_partial( 'infobox/infobox', array('title' => __( 'Pricing Tables', 'wproto'), 'content' => '<p>' . __( 'Create unlimited number of pricing tables with amazing visual editor. You can use paste these tables at any post or page simply by clicking on editor button.', 'wproto') . '</p>') );
		endif; 
	}
	
	/**
	 * Add admin scripts
	 **/
	function add_scripts() {
		global $post;
		
		$post_type = get_post_type( $post );
		
		if( $post_type == 'wproto_pricing_table' ) {
			wp_register_script( 'wproto-pricing-tables-screen', WPROTO_THEME_URL . '/js/admin/screen-pricing-tables.js?' . $this->settings['res_cache_time'] );
			wp_enqueue_script( 'wproto-pricing-tables-screen', array( 'jquery' ) );
		}
	}
	
	/**
	 * Add custom metaboxes
	 **/
	function add_edit_metaboxes() {
		
		add_meta_box(
			'wproto_pricing_table_subtitle'
			,__( 'Table Description (text after table title)', 'wproto' )
			,array( $this, 'render_meta_box_table_subtitle' )
			,'wproto_pricing_table'
			,'normal'
			,'high'
		);
		
		add_meta_box(
			'wproto_pricing_table_editor'
			,__( 'Pricing Table Editor', 'wproto' )
			,array( $this, 'render_meta_box_table_editor' )
			,'wproto_pricing_table'
			,'normal'
			,'high'
		);
		
		add_meta_box(
			'wproto_pricing_table_editor_style'
			,__( 'Style', 'wproto' )
			,array( $this, 'render_meta_box_table_editor_style' )
			,'wproto_pricing_table'
			,'side'
			,'core'
		);
		
		add_meta_box(
			'wproto_pricing_table_editor_legend'
			,__( 'Tip', 'wproto' )
			,array( $this, 'render_meta_box_table_editor_tip' )
			,'wproto_pricing_table'
			,'side'
			,'core'
		);
		
	}
	
	/**
	 * Table subtitle metabox
	 **/
	function render_meta_box_table_subtitle() {
		global $post;
		$data = array();
		$data['subtitle'] = get_post_meta( $post->ID, 'subtitle', true );
		
		$this->view->load_partial( 'metaboxes/pricing_table_subtitle', $data );
	}
	
	/**
	 * Render "Featured" metabox
	 **/
	function render_meta_box_table_editor() {
		global $post;
		$data = array();
		$data['pricing_table'] = get_post_meta( $post->ID, 'pricing_table', true );
		
		$this->view->load_partial( 'metaboxes/pricing_table_editor', $data );
	}
	
	/**
	 * Save custom fields
	 **/
	function save_custom_meta( $post_id ) {
		
		$post_type = get_post_type( $post_id );
		
		if( $post_type == 'wproto_pricing_table' ) {
			
			// Stop WP from clearing custom fields on autosave
			if ( defined( 'DOING_AUTOSAVE') && DOING_AUTOSAVE )
				return;

			// Prevent quick edit from clearing custom fields
			if ( defined( 'DOING_AJAX') && DOING_AJAX )
				return;

			if( empty( $_POST) )
				return;
			
			update_post_meta( $post_id, "pricing_table", isset( $_POST["pt"] ) ? $_POST["pt"] : '' );
			update_post_meta( $post_id, "table_style", isset( $_POST["table_style"] ) ? strip_tags( $_POST["table_style"] ) : 'style_1' );
			update_post_meta( $post_id, "subtitle", isset( $_POST["subtitle"] ) ? strip_tags( $_POST["subtitle"] ) : '' );
			
		}
		
	}
	
	/**
	 * Render Tip metabox
	 **/
	function render_meta_box_table_editor_tip() {
		$this->view->load_partial( 'metaboxes/pricing_table_editor_tip' );
	}
	
	/**
	 * Render table style metabox
	 **/
	function render_meta_box_table_editor_style() {
		global $post;
		
		$data = array();
		$data['table_style'] = get_post_meta( $post->ID, 'table_style', true );
		$this->view->load_partial( 'metaboxes/pricing_table_editor_style', $data );
	}
	
	/**
	 * Check string for image shortcode
	 **/
	public static function check_shortcode( $text ) {
		
		$retina_img = wpl_galaxy_wp_utils::is_retina() ? '@2x' : '';
		
		$text = str_replace( '[y]', '<img src="' . WPROTO_THEME_URL .  '/images/shortcodes/y' . $retina_img . '.png" alt="" width="16" height="16" />', $text );
		$text = str_replace( '[n]', '<img src="' . WPROTO_THEME_URL .  '/images/shortcodes/n' . $retina_img . '.png" alt="" width="16" height="16" />', $text );
		$text = str_replace( '[na]', '<img src="' . WPROTO_THEME_URL .  '/images/shortcodes/na' . $retina_img . '.png" alt="" width="16" height="16" />', $text );
		$text = str_replace( '[star0]', '<img src="' . WPROTO_THEME_URL .  '/images/shortcodes/star0' . $retina_img . '.png" alt="" width="16" height="16" />', $text );
		$text = str_replace( '[star50]', '<img src="' . WPROTO_THEME_URL .  '/images/shortcodes/star50' . $retina_img . '.png" alt="" width="16" height="16" />', $text );
		$text = str_replace( '[star100]', '<img src="' . WPROTO_THEME_URL .  '/images/shortcodes/star100' . $retina_img . '.png" alt="" width="16" height="16" />', $text );
		$text = str_replace( '[cool]', '<img src="' . WPROTO_THEME_URL .  '/images/shortcodes/cool' . $retina_img . '.png" alt="" width="16" height="16" />', $text );
		return $text;
	}
	
}