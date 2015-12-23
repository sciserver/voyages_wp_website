<?php
/**
 *	Theme settings controller
 **/
class wpl_galaxy_wp_settings_controller extends wpl_galaxy_wp_admin_controller {
	
	function __construct() {
		
		if( is_admin() ) {
			// add info box
			add_action( 'admin_footer', array( $this, 'add_info_box'));
			add_action( 'admin_enqueue_scripts', array( $this, 'add_scripts' ) );

			// check for maintenance mode
			add_action( 'admin_notices', array( $this, 'is_maintenance_mode' ) );
			// rebuild thumbnail
			add_action( 'wp_ajax_wproto_rebuild_thumbnails', array( $this, 'ajax_rebuild_thumbnails' ) );
			add_action( 'wp_ajax_wproto_flush_rewrite_rules', array( $this, 'flush_rewrite_rules' ) );
			
			// grab google fonts
			add_action( 'wp_ajax_wproto_grab_google_fonts_list', array( $this, 'ajax_grab_google_fonts_list' ) );
		}
		
		// filter wp_head with settings
		add_action( 'init', array( $this, 'setup_wp' ) );
		// print tracking code
		add_action( 'wp_footer', array( $this, 'print_tracking_code' ));
		
	}
	
	/**
	 * Add JS Scripts
	 **/
	function add_scripts() {
		
		$page = isset( $_GET['page'] ) ? $_GET['page'] : '';
		
		if( $page == 'wproto_theme_settings' ) {
			wp_register_script( 'wproto-settings-screen', WPROTO_THEME_URL . '/js/admin/screen-settings.js?' . $this->settings['res_cache_time'] );
			wp_enqueue_script( 'wproto-settings-screen', array( 'wproto-engine-functions' ) );	
		}
		
	}
	
	/**
	 * Add info box
	 **/
	function add_info_box() {
		// Add - edit sidebars screen
		$page = isset( $_GET['page'] ) ? $_GET['page'] : '';
		$hide_infobox = $this->get_option( 'hide_infobox', 'general' );
		
		if( $hide_infobox != 'yes' ):
		
			if( $page == 'wproto_theme_settings' ):
				$this->view->load_partial( 'infobox/infobox', array('title' => wp_get_theme(), 'content' => '<p>' . __( 'Thank you for purchasing this theme. We hope that you will appreciate our work and you will like it.', 'wproto') . '</p>' . '<p>' . __( sprintf( 'We support all of our customers, so if you faced a problem - feel free to <a href="%s" target="_blank">contact to our support</a>.', 'http://themeforest.net/user/wplab?ref=wplab' ), 'wproto') . '</p>') );
			endif;
			
		endif;
		 
	}
	
	/**
	 * Display "settings" settings screen
	 **/
	function display_settings_screen() {
		$data = array();
		
		$this->view->load_partial( 'settings/settings', $data );
	}

	
	/**
	 * Save customize settings
	 **/
	function save() {

		$_POST = wp_unslash( $_POST );
		
		$allowed_tags = wp_kses_allowed_html( 'post' );
		
		if( $_POST['wproto_setting_action'] == 'settings' ) {
			
			delete_transient('wproto_font_icons');
			
			$_POST['general']['icomoon_enabled'] = isset( $_POST['general']['icomoon_enabled'] ) ? $_POST['general']['icomoon_enabled'] : 'no';
			
			$_POST['general']['likes_on_posts'] = isset( $_POST['general']['likes_on_posts'] ) ? $_POST['general']['likes_on_posts'] : 'no';
			$_POST['general']['likes_on_comments'] = isset( $_POST['general']['likes_on_comments'] ) ? $_POST['general']['likes_on_comments'] : 'no';
			
			update_option( 'blogname', isset( $_POST['general']['site_title'] ) ? wp_kses( $_POST['general']['site_title'], $allowed_tags ) : '' );
			update_option( 'blogdescription', isset( $_POST['general']['site_tagline'] ) ? wp_kses( $_POST['general']['site_tagline'], $allowed_tags ) : '' );
			
			if( (isset( $_POST['api']['enable_google_oauth'] ) && $_POST['api']['enable_google_oauth'] == 'yes') || (isset( $_POST['api']['enable_facebook_oauth'] ) && $_POST['api']['enable_facebook_oauth'] == 'yes') ) {
				update_option( 'users_can_register', true );
			}
			
			$_POST['general']['captcha_difficult'] = isset( $_POST['general']['captcha_difficult'] ) && is_array( $_POST['general']['captcha_difficult'] ) ? $_POST['general']['captcha_difficult'] : array( 'minus' );

		}
		
		if( is_array( $_POST ) && count( $_POST ) > 0 ) {
			foreach( $_POST as $env=>$v ) {
				
				if( is_array( $v ) && count( $v ) > 0 ) {
					foreach( $v as $option_name=>$option_value ) {
						$this->set_option( $option_name, $option_value, $env );
					}
					
				}
				
			}
			
			$this->write_all_settings();
			
			$tab = isset( $_POST['wproto_tab'] ) ? $_POST['wproto_tab'] : '';
			
			header( 'Location: ' . add_query_arg( array( 'wproto_tab' => $tab, 'updated' => 'true', 'display' => '#' . $tab ) ) );
			exit;
			
		}
		
		
	}
	
	/**
	 * Check if maintenance mode is enabled
	 **/
	function is_maintenance_mode() {
		
		if( $this->get_option('maintenance_enabled', 'general') == 'yes' ) {
			printf( '<div class="updated notify-maintenance"><p>%s <a href="%s">%s</a></p></div>', __( 'Maintenance mode is enabled. All pages of your website will be not availabled to visitors (<strong>users, with Administrator permissions are excluded</strong>) and search engines while maintenance mode is enabled.', 'wproto' ), admin_url('admin.php?page=wproto_theme_settings#custom-modes'), __( 'Settings page', 'wproto' ) );
		}
		
	}
	
	
	/**
	 * Rebuild thumbnails
	 **/
	function ajax_rebuild_thumbnails() {
		global $wpdb;

		if( is_admin() && $_SERVER[ 'REQUEST_METHOD'] == 'POST' && current_user_can( 'administrator')) {

			if ( $_POST['subaction'] == "getlist") {

				$res = array();

				$attachments =& get_children( array(
					'post_type' => 'attachment',
					'post_mime_type' => 'image',
					'numberposts' => -1,
					'post_status' => null,
					'post_parent' => null, // any parent
					'output' => 'object',
				));
                    
				foreach ( $attachments as $attachment) {
					$res[] = array('id' => $attachment->ID);
				}
                    
				die( json_encode( $res));
                    
			}
                
			if ( $_POST['subaction'] == "regen") {
                    
				$id = (int)$_POST[ "id"];

				$fullsizepath = get_attached_file( $id);

				if ( FALSE !== $fullsizepath && @file_exists( $fullsizepath) ) {
					@set_time_limit( 30);
					wp_update_attachment_metadata( $id, wp_generate_attachment_metadata( $id, $fullsizepath));
				}

				die;
                    
			}
                
		} else {
			die( __( 'Access denied', 'wproto'));
		}
	}
	
	/**
	 * Flush rewrite rules
	 **/
	function flush_rewrite_rules() {
		update_option( 'rewrite_rules', '' );
		flush_rewrite_rules( true );
		die;
	}
	
	/**
	 * Grab google fonts list
	 **/
	function ajax_grab_google_fonts_list() {
		
		$fonts = wpl_galaxy_wp_utils::grab_google_fonts( true );
		
		if( count( @$fonts->items ) > 0 ) echo 'ok';
		
		die;
	}
	
	/**
	 * Setup WP with settings
	 **/
	function setup_wp() {
		$rss_enabled = $this->get_option( 'rss_enabled', 'general' );
		
		if( $rss_enabled == 'no' ):
			remove_action( 'wp_head', 'feed_links_extra', 3 ); // Display the links to the extra feeds such as category feeds
			remove_action( 'wp_head', 'feed_links', 2 ); // Display the links to the general feeds: Post and Comment Feed
			remove_action( 'wp_head', 'rsd_link' ); // Display the link to the Really Simple Discovery service endpoint, EditURI link
			
			add_action( 'do_feed', array( $this, 'disable_rss_feed' ), 1);
			add_action( 'do_feed_rdf', array( $this, 'disable_rss_feed' ), 1);
			add_action( 'do_feed_rss', array( $this, 'disable_rss_feed' ), 1);
			add_action( 'do_feed_rss2', array( $this, 'disable_rss_feed' ), 1);
			add_action( 'do_feed_atom', array( $this, 'disable_rss_feed' ), 1);
			add_action( 'do_feed_rss2_comments', array( $this, 'disable_rss_feed' ), 1);
			add_action( 'do_feed_atom_comments', array( $this, 'disable_rss_feed' ), 1);

			
		endif;
		
	}
	
	/**
	 * Disable RSS feed
	 **/
	function disable_rss_feed() {
		wp_die( __( 'Feed was disabled by administrator', 'wproto' ) );
	}
	
	/**
	 * Print tracking code at footer
	 **/
	function print_tracking_code() {
		$tracking_code = $this->get_option( 'tracking_code', 'general' );
		echo @$tracking_code;
	}	
	
}