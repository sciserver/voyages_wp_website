<?php
/**
 *	Add / Remove / Edit widget areas
 **/
class wpl_galaxy_wp_admin_sidebars_controller extends wpl_galaxy_wp_admin_controller {
	
	function __construct() {
		
		if( is_admin() ) {
			add_filter( 'manage_edit-wproto_sidebars_columns', array( $this, 'modify_sidebars_columns' ) );
			add_action( 'admin_footer', array( $this, 'add_info_box'));
			add_action( 'admin_enqueue_scripts', array( $this, 'add_scripts' ) );
			add_action( 'admin_enqueue_scripts', array( $this, 'add_styles' ) );
		}
		
	}
	
	/**
	 * Sidebars columns
	 **/
	function modify_sidebars_columns( $theme_columns ) {
		$columns = array(
        'cb' => '<input type="checkbox" />',
        'name' => __( 'Sidebar name', 'wproto' ),
				'description' => __('Description', 'wproto'),
        );
    return $columns;
	}
	
	/**
	 * Add info box to sidebars screen
	 **/
	function add_info_box() {
		$hide_infobox = $this->get_option( 'hide_infobox', 'general' );
		// Add - edit sidebars screen
		if( $hide_infobox != 'yes' && isset( $_GET['taxonomy'] ) && $_GET['taxonomy'] == 'wproto_sidebars' ):
			$this->view->load_partial( 'infobox/infobox', array('title' => __( 'Widget Areas', 'wproto'), 'content' => '<p>' . __( 'Create an unlimited number of sidebars, and use them at your website.', 'wproto') . '</p>') );
		endif; 
		
	}
	
	/**
	 * Add JS Scripts
	 **/
	function add_scripts() {
		if( isset( $_GET['taxonomy'] ) && $_GET['taxonomy'] == 'wproto_sidebars' ) {
			wp_register_script( 'wproto-sidebars', WPROTO_THEME_URL . '/js/admin/screen-sidebars.js?' . $this->settings['res_cache_time'] );
			wp_enqueue_script( 'wproto-sidebars', array( 'jquery' ) );
		}
		
	}
	
	/**
	 * Add CSS Styles
	 **/
	function add_styles() {
		if( isset( $_GET['taxonomy'] ) && $_GET['taxonomy'] == 'wproto_sidebars' ) {
			wp_enqueue_style( 'wproto-sidebars', WPROTO_THEME_URL . '/css/admin/sidebars.css?' . $this->settings['res_cache_time'] );
		}
	}
	
}