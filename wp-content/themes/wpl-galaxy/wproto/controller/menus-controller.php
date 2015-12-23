<?php
/**
 *	Theme menus controller
 **/
class wpl_galaxy_wp_menus_controller extends wpl_galaxy_wp_admin_controller {
	
	function __construct() {
		
		// add custom menu fields to menu
		add_filter( 'wp_setup_nav_menu_item', array( $this, 'add_menu_custom_fields' ) );
		
		if( is_admin() ) {
			// save menu custom fields
			add_action( 'wp_update_nav_menu_item', array( $this, 'update_menu_custom_fields'), 10, 3 );
			// edit menu walker
			add_filter( 'wp_edit_nav_menu_walker', array( $this, 'edit_menu_walker'), 10, 2 );
			// add info box
			add_action( 'admin_footer', array( $this, 'add_info_box'));
			
			add_action( 'admin_enqueue_scripts', array( $this, 'add_styles' ) );
			
			//add_action( 'admin_init', array( $this, 'add_metaboxes' ) );

		}
		
		add_filter( 'nav_menu_css_class', array( $this, 'fix_front_menu_class' ), 10, 2);
		
	}
	
	/**
	 * Add custom fields values
	 **/
	function add_menu_custom_fields( $menu_item ) {
		$menu_item->menu_icon = get_post_meta( $menu_item->ID, '_menu_item_icon', true );
		
		$menu_item->dont_display_as_link = get_post_meta( $menu_item->ID, '_menu_item_dont_display_as_link', true );
		$menu_item->mega_menu = get_post_meta( $menu_item->ID, '_menu_item_mega_menu', true );
		$menu_item->hide_large_desktop = get_post_meta( $menu_item->ID, '_menu_item_hide_large_desktop', true );
		$menu_item->hide_small_desktop = get_post_meta( $menu_item->ID, '_menu_item_hide_small_desktop', true );
		$menu_item->hide_tablet = get_post_meta( $menu_item->ID, '_menu_item_hide_tablet', true );
		$menu_item->hide_phone = get_post_meta( $menu_item->ID, '_menu_item_hide_phone', true );
		return $menu_item;
	}
	
	/**
	 * Update menu custom fields
	 **/
	function update_menu_custom_fields( $menu_id, $menu_item_db_id, $args ) {
		
		$allowed_tags = wp_kses_allowed_html( 'post' );
		
		// Check if element is properly sent
		if ( isset( $_REQUEST['menu_item_icon'] ) && is_array( $_REQUEST['menu_item_icon']) ) {
			$item_value = $_REQUEST['menu_item_icon'][$menu_item_db_id];
			update_post_meta( $menu_item_db_id, '_menu_item_icon', wp_kses( $item_value, $allowed_tags ) );
		}
		
		$item_value = isset( $_REQUEST['menu_item_dont_display_as_link'][$menu_item_db_id] ) ? $_REQUEST['menu_item_dont_display_as_link'][$menu_item_db_id] : 'no';	
		update_post_meta( $menu_item_db_id, '_menu_item_dont_display_as_link', wp_kses( $item_value, $allowed_tags ) );
		
		$item_value = isset( $_REQUEST['menu_item_mega_menu'][$menu_item_db_id] ) ? $_REQUEST['menu_item_mega_menu'][$menu_item_db_id] : 'no';	
		update_post_meta( $menu_item_db_id, '_menu_item_mega_menu', wp_kses( $item_value, $allowed_tags ) );

		$item_value = isset( $_REQUEST['menu_item_hide_large_desktop'][$menu_item_db_id] ) ? $_REQUEST['menu_item_hide_large_desktop'][$menu_item_db_id] : 'no';
		update_post_meta( $menu_item_db_id, '_menu_item_hide_large_desktop', wp_kses( $item_value, $allowed_tags ) );

		$item_value = isset( $_REQUEST['menu_item_hide_small_desktop'][$menu_item_db_id] ) ? $_REQUEST['menu_item_hide_small_desktop'][$menu_item_db_id] : 'no';
		update_post_meta( $menu_item_db_id, '_menu_item_hide_small_desktop', wp_kses( $item_value, $allowed_tags ) );

		$item_value = isset( $_REQUEST['menu_item_hide_tablet'][$menu_item_db_id] ) ? $_REQUEST['menu_item_hide_tablet'][$menu_item_db_id] : 'no';
		update_post_meta( $menu_item_db_id, '_menu_item_hide_tablet', wp_kses( $item_value, $allowed_tags ) );

		$item_value = isset( $_REQUEST['menu_item_hide_phone'][$menu_item_db_id] ) ? $_REQUEST['menu_item_hide_phone'][$menu_item_db_id] : 'no';
		update_post_meta( $menu_item_db_id, '_menu_item_hide_phone', wp_kses( $item_value, $allowed_tags ) );

	}
	
	/**
	 * Edit menu
	 **/
	function edit_menu_walker( $walker, $menu_id ) {
		return 'wpl_galaxy_wp_admin_nav_menu_walker';
	}
	
	/**
	 * Add info box
	 **/
	function add_info_box() {
		
		$screen = get_current_screen();
		
		$hide_infobox = $this->get_option( 'hide_infobox', 'general' );
		// Add - edit sidebars screen
		if( $hide_infobox != 'yes' && (isset( $screen->base ) && $screen->base == 'nav-menus') ):
			$this->view->load_partial( 'infobox/infobox', array('title' => __( 'Custom Navigation Menus', 'wproto'), 'content' => '<p>' . __( 'Customize your menus - setup mega menu or add icons for any menu item.', 'wproto') . '</p>') );
		endif; 
	}
	
	/**
	 * Add CSS Styles
	 **/
	function add_styles() {
		
		$screen = get_current_screen();
		
		if( isset( $screen->base ) && $screen->base == 'nav-menus' ) {
			wp_enqueue_style( 'wproto-menus', WPROTO_THEME_URL . '/css/admin/menus.css?' . $this->settings['res_cache_time'] );
		}
	}
	
	/**
	 * Add metabox for quick menu items access
	 **/
	function add_metaboxes() {
		
		add_meta_box(
			'wproto_quick_access_menu'
			,__( 'Site Sections', 'wproto' )
			,array( $this, 'render_meta_box_quick_access' )
			,'nav-menus'
			,'side'
			,'high'
		);

		
	}
	
	/**
	 * Quick access metabox
	 **/
	function render_meta_box_quick_access() {
		$this->view->load_partial( 'metaboxes/menu_archives' );
	}
	
	/**
	 * Fix taxonomy highlight at front
	 **/
	function fix_front_menu_class( $classes, $item ) {
		global $wp_query;
		
		$tax = isset( $wp_query->query_vars['taxonomy'] ) ? $wp_query->query_vars['taxonomy'] : NULL;
		
		if( $tax != NULL ) {

  		if ( $item->object_id == get_option('page_for_posts') ) {
    		$key = array_search( 'current_page_parent', $classes );
      		if ( false !== $key )
        		unset( $classes[ $key ] );
     	}
		}
		
		return $classes;
		
	}
	
}