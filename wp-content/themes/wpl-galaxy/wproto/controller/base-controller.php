<?php
/**
 * Do stuff common to ALL controllers
 **/
class wpl_galaxy_wp_base_controller {
	/**
	 * Class vars. Make controllers public, so
	 * that they can be called from templates too.
	 **/
	public $model = null;
	public $view = null;
	public $controller = null;
	public $settings = array();
	
	/**
	 * Below ALL add_action() and add_filter() hooks that
	 * get served by the methods of this controller
	 * @param array
	 **/
	function __construct( $settings = array() ) {
	
		// Load libraries
		if( is_admin() ) {
			require_once WPROTO_THEME_DIR . '/library/visual-shortcodes/visual-shortcodes.php';
			require_once WPROTO_THEME_DIR . '/library/googl/Googl.class.php';
			require_once WPROTO_THEME_DIR . '/library/tgm-plugin-activation/class-tgm-plugin-activation.php';	
		}
	
		// Translation support
		load_theme_textdomain( 'wproto', WPROTO_THEME_DIR . '/languages' );
	
		// Use sessions
		if( ! session_id() ) {
			@session_start();
		}
		
		// Load settings
		$this->settings = $settings;
		$this->load_settings();
		
		// activate plugins
		add_action( 'tgmpa_register', array( $this, 'register_plugins') );
		
		// Route $_GET/$_POST['wproto_action'] custom requests
		add_action( 'parse_request', array( $this, 'delegate_to_controller_action' ), 1 );
		add_action( 'admin_init', array( $this, 'delegate_to_controller_action' ), 1 );
		
		// Register custom post types and taxonomies
		add_action( 'init', array( $this, 'register_custom_post_types'));
		add_action( 'init', array( $this, 'register_taxonomies'));
		
		// Add theme support
		add_action( 'init', array( $this, 'add_theme_support'));
		
		// Define image sizes
		add_action( 'init', array( $this, 'register_image_sizes'));
		add_filter( 'image_size_names_choose', array( $this, 'register_image_names'));
		
		add_filter( 'use_default_gallery_style', '__return_false' );
		
		register_nav_menus( array(
			'header_menu' => __('Header Menu', 'wproto')
		) );
		
		// Register sidebars
		add_action( 'init', array( $this, 'register_sidebars'));
		
	}
	
	/**
	 * Load settings
	 **/
	function load_settings() {		
		$settings['date_format'] = get_option('date_format');
		$settings['general'] = get_option('wproto_settings_general');
		
		$this->settings = $settings + $this->settings;
		
	}
	
	/**
	 * Get settings value
	 * @param option name string
	 * @param environment string
	 * @param post_id int (optional)
	 **/
	function get_option( $option_name, $env = 'general', $post_id = 0 ) {
		
		$settings_env = isset( $this->settings[ $env ] ) ? $this->settings[ $env ] : array();
		
		$storage = $post_id > 0 ? get_post_meta( $post_id, 'wproto_settings', true ) : $settings_env;
		
		return isset( $storage[ $option_name ] ) ? $storage[ $option_name ] : NULL;
		
	}
	
	/**
	 * Set a new option value and refresh the settings
	 * @param option name string
	 * @param environment string
	 * @param post_id int (optional)
	 **/
	function write_option( $option_name, $option_value, $env ) {
		
		$storage = get_option( 'wproto_settings_' . $env );
		$storage[ $option_name ] = $option_value;

		update_option( 'wproto_settings_' . $env, $storage );
		
		// Refresh settings
		$this->load_settings();
	}
	
	/**
	 * Set option into loaded config
	 **/
	function set_option( $option_name, $option_value, $env ) {
		$this->settings[ $env ][ $option_name ] = $option_value;
	}
	
	/**
	 * Write loaded settings intoDB
	 **/
	function write_all_settings() {
		
		update_option('wproto_settings_general', $this->settings['general']);
		
	}
	
	/**
	 * Parse custom request using our own routing,
	 * i.e. $_GET['wproto_action'] or $_POST['wproto_action'],
	 * and then delegate to appropriate controller
	 * action.
	 *
	 * Example 1: '/?wproto_action=front_controller-view'
	 * Example 2: '/wp-admin/index.php?wproto_action=admin_settings-save'
	 **/
	function delegate_to_controller_action() {
		if ( isset( $_POST['wproto_action'] ) ) {
			$action = $_POST['wproto_action'];
		} elseif ( isset( $_GET['wproto_action'] ) ) {
			$action = $_GET['wproto_action'];
		}

		if ( isset( $action ) ) {
			$controller_and_action = explode( '-', $action );

			if ( count( $controller_and_action ) == 2 ) {
				//! TODO: Learn from popular frameworks how they secure this bit here!
				$controller = 'wpl_galaxy_wp_' . $controller_and_action[0] . '_controller';
				$short_controller = $controller_and_action[0];
				$action = $controller_and_action[1];

				if ( class_exists( $controller ) && method_exists( $controller , $action ) ) {
					call_user_func( array( $this->controller->$short_controller, $action ) );
				} else {
					//throw new Exception( 'This custom request was not well-formed.' );
				}
			}
		}
	}
	
	/**
	 * Autoload and instantiate all application
	 * classes neccessary for this plugin
	 **/
	function dispatch() {
		$this->model =		  new stdClass();
		$this->view =				new stdClass();
		$this->controller =	new stdClass();

		// Manually load dependency classes first
		require_once WPROTO_ENGINE_DIR . '/model/database.php';
		require_once WPROTO_ENGINE_DIR . '/view/view.php';
								
		require_once WPROTO_ENGINE_DIR . '/controller/front-controller.php';
		require_once WPROTO_ENGINE_DIR . '/controller/admin-controller.php';

		// Manually instantiate dependency classes first
		$this->model->database = new wpl_galaxy_wp_database();
		$this->view = new wpl_galaxy_wp_view();
		$this->controller->base = $this;
		$this->controller->front = new wpl_galaxy_wp_front_controller();
		$this->controller->admin = new wpl_galaxy_wp_admin_controller();

		// Autoload all others
		$this->autoload_directory_classes('model');
		$this->autoload_directory_classes('controller');
		$this->autoload_directory_classes('helper');
		$this->autoload_directory_classes('widget');

		// Inject models, view and controllers from this base
		// controller into all OTHER controllers & models
		foreach ($this->controller as $controller) {
			$controller->inject_application_classes($this->model, $this->view, $this->controller, $this->settings);
		}
		foreach ($this->model as $model) {
			$model->inject_application_classes($this->model);
		}
	}
	
	/**
	 * Autoload all classes in a directory
	 **/
	function autoload_directory_classes( $layer, $load_class = true ) {

		$directory = WPROTO_ENGINE_DIR . '/' . $layer . '/';
		$handle = opendir($directory);

		while (false !== ($file = readdir($handle))) {
			
			if( $file == '.htaccess' ) continue;
			
			if (is_file($directory . $file)) {
				// Figure out class name from file name
				$class = str_replace('.php', '', $file);
				
				$class = 'wpl_galaxy_wp_' . str_replace('-', '_', $class) . '';
				$shortClass = str_replace('wpl_galaxy_wp_', '', $class);
				$shortClass = str_replace('_' . $layer, '', $shortClass);

				if( $load_class ) {
					// Avoid recursion
					if ($class != get_class($this) && $class != 'wpl_galaxy_wp_front_controller' && $class != 'wpl_galaxy_wp_admin_controller') {
						// Include and instantiate class
						require_once $directory . $file;
						if( $layer != 'helper' && $layer != 'widget' ) {
							$this->$layer->$shortClass = new $class();
						}
					}
				} else {
					require_once $directory . $file;
				}

			}
		}
	}
	
	/**
	 * Inject models, view and controllers
	 * into all other controllers to make
	 * them callable from there
	 **/
	function inject_application_classes($model, $view, $controller, $settings) {
		$this->model = $model;
		$this->view = $view;
		$this->controller = $controller;
		$this->settings = $settings;
	}
	
	/**
	 * Register plugins
	 **/
	function register_plugins() {
		
		$plugins = array(
			array(
				'name' 		=> 'WooCommerce',
				'slug' 		=> 'woocommerce',
				'required' 	=> false,
				'force_activation' => false
			),
			array(
				'name' => 'Recent Tweets Widget',
				'slug' => 'recent-tweets-widget',
				'required' 	=> false,
				'force_activation' => false
			),
			array(
				'name'     						=> 'LayerSlider WP', 	// The plugin name
				'slug'     						=> 'LayerSlider', 		// The plugin slug (typically the folder name)
				'source'   						=> WPROTO_THEME_DIR . '/library/tgm-plugin-activation/plugins/layersliderwp.zip', // The plugin source
				'required' 						=> false, 						// If false, the plugin is only 'recommended' instead of required
				'version' 						=> '', 								// E.g. 1.0.0. If set, the active plugin must be this version or higher, otherwise a notice is presented
				'force_activation' 		=> false, 							// If true, plugin is activated upon theme activation and cannot be deactivated until theme switch
				'force_deactivation' 	=> true, 							// If true, plugin is deactivated upon theme switch, useful for theme-specific plugins
				'external_url' 				=> 'http://codecanyon.net/item/layerslider-responsive-wordpress-slider-plugin-/1362246' // If set, overrides default API URL and points to an external URL
			),
			/* TODO: Add Visual Composer
			array(
				'name'     						=> 'JS Composer',
				'slug'     						=> 'js_composer',
				'source'   						=> WPROTO_THEME_DIR . '/library/tgm-plugin-activation/plugins/js_composer.zip',
				'required' 						=> false,
				'version' 						=> '',
				'force_activation' 		=> false,
				'force_deactivation' 	=> true,
				'external_url' 				=> 'http://codecanyon.net/item/visual-composer-for-wordpress/242431'
			)*/
		);
		
		$config = array(
			'domain'       			=> 'wproto',         						// Text domain - likely want to be the same as your theme.
			'default_path' 			=> '',                					// Default absolute path to pre-packaged plugins
			'parent_menu_slug' 	=> 'themes.php', 								// Default parent menu slug
			'parent_url_slug' 	=> 'themes.php', 								// Default parent URL slug
			'menu'         			=> 'install-required-plugins', 	// Menu slug
			'has_notices'      	=> true,                      	// Show admin notices or not
			'is_automatic'    	=> false,					   						// Automatically activate plugins after installation or not
			'message' 					=> '',													// Message to output right before the plugins table
			'strings'      			=> array(
				'page_title'                       			=> __( 'Install Required Plugins', 'wproto' ),
				'menu_title'                       			=> __( 'Install Plugins', 'wproto' ),
				'installing'                       			=> __( 'Installing Plugin: %s', 'wproto' ), // %1$s = plugin name
				'oops'                             			=> __( 'Something went wrong with the plugin API.', 'wproto' ),
				'notice_can_install_required'     			=> _n_noop( 'This theme requires the following plugin: %1$s.', 'This theme requires the following plugins: %1$s.' ), // %1$s = plugin name(s)
				'notice_can_install_recommended'				=> _n_noop( 'This theme recommends the following plugin: %1$s.', 'This theme recommends the following plugins: %1$s.' ), // %1$s = plugin name(s)
				'notice_cannot_install'  								=> _n_noop( 'Sorry, but you do not have the correct permissions to install the %s plugin. Contact the administrator of this site for help on getting the plugin installed.', 'Sorry, but you do not have the correct permissions to install the %s plugins. Contact the administrator of this site for help on getting the plugins installed.' ), // %1$s = plugin name(s)
				'notice_can_activate_required'    			=> _n_noop( 'The following required plugin is currently inactive: %1$s.', 'The following required plugins are currently inactive: %1$s.' ), // %1$s = plugin name(s)
				'notice_can_activate_recommended'				=> _n_noop( 'The following recommended plugin is currently inactive: %1$s.', 'The following recommended plugins are currently inactive: %1$s.' ), // %1$s = plugin name(s)
				'notice_cannot_activate' 								=> _n_noop( 'Sorry, but you do not have the correct permissions to activate the %s plugin. Contact the administrator of this site for help on getting the plugin activated.', 'Sorry, but you do not have the correct permissions to activate the %s plugins. Contact the administrator of this site for help on getting the plugins activated.' ), // %1$s = plugin name(s)
				'notice_ask_to_update' 									=> _n_noop( 'The following plugin needs to be updated to its latest version to ensure maximum compatibility with this theme: %1$s.', 'The following plugins need to be updated to their latest version to ensure maximum compatibility with this theme: %1$s.' ), // %1$s = plugin name(s)
				'notice_cannot_update' 									=> _n_noop( 'Sorry, but you do not have the correct permissions to update the %s plugin. Contact the administrator of this site for help on getting the plugin updated.', 'Sorry, but you do not have the correct permissions to update the %s plugins. Contact the administrator of this site for help on getting the plugins updated.' ), // %1$s = plugin name(s)
				'install_link' 					  							=> _n_noop( 'Begin installing plugin', 'Begin installing plugins' ),
				'activate_link' 				  							=> _n_noop( 'Activate installed plugin', 'Activate installed plugins' ),
				'return'                           			=> __( 'Return to Required Plugins Installer', 'wproto' ),
				'plugin_activated'                 			=> __( 'Plugin activated successfully.', 'wproto' ),
				'complete' 															=> __( 'All plugins installed and activated successfully. %s', 'wproto' ), // %1$s = dashboard link
				'nag_type'															=> 'updated' // Determines admin notice type - can only be 'updated' or 'error'
			)
		);

		tgmpa( $plugins, $config );
		
	}
	
	/**
	 * Add theme support
	 **/
	function add_theme_support() {
		add_theme_support( 'automatic-feed-links' );
		add_theme_support( 'woocommerce' );
		add_theme_support( 'html5', array( 'search-form', 'comment-form', 'comment-list' ) );		
		add_theme_support( 'menus' );
		add_theme_support( 'post-formats', array( 'aside', 'gallery', 'link', 'image', 'quote', 'status', 'video', 'audio', 'chat' ) );
		add_theme_support( 'post-thumbnails', array( 'post', 'wproto_slides', 'wproto_partners', 'wproto_catalog', 'wproto_portfolio', 'wproto_team', 'wproto_benefits', 'wproto_testimonials', 'wproto_video', 'wproto_photoalbums', 'product' ) );
	}
	
	/**
	 * Register custom image sizes
	 **/
	function register_image_sizes() {
		
		// Admin-side image sizes
		add_image_size( 'wproto-admin-thumb', 100, 75, true );
		add_image_size( 'wproto-admin-thumb-medium', 150, 150, true );
		add_image_size( 'wproto-admin-category-thumb', 270, 170, true );
		
		// RSS images
		add_image_size( 'wproto-rss-image', 540, 340, true );
		
		// Front image sizes
		add_image_size( 'wproto-mega-menu-thumb', 290, 80, true );
		add_image_size( 'benefits-icon', 97, 97, true );
		add_image_size( 'partners-clients-logo', 170, 155, true );
		add_image_size( 'portfolio-square-big', 336, 336, true );
		add_image_size( 'portfolio-square-medium', 165, 165, true );
		add_image_size( 'photo-small', 85, 85, true );
		add_image_size( 'shop-product-preview', 180, 180, true );
		add_image_size( 'shop-product-preview-small', 67, 68, true );
		add_image_size( 'shop-product-small', 87, 87, true );
		add_image_size( 'shop-product-thumb', 264, 271, true );
		add_image_size( 'shop-product-thumb-medium', 194, 199, true );
		add_image_size( 'shop-product-big', 360, 369, true );
		add_image_size( 'shop-buy-together', 134, 136, true );
		add_image_size( 'shop-related', 180, 182, true );
		add_image_size( 'shop-cart', 63, 63, true );
		add_image_size( 'author-thumb', 267, 198, true );
		add_image_size( 'new-scroll-thumb', 280, 211, true );
		add_image_size( 'portfolio-scroll-thumb', 170, 108, true );
		add_image_size( 'portfolio-hexagon-thumb', 310, 310, true );
		add_image_size( 'header-menu-cat-thumb', 290, 180, true );
		add_image_size( 'post-thumb-full', 1067, 533, true );
		add_image_size( 'category-thumb-full', 1067, 230, true );
		add_image_size( 'post-thumb-big', 520, 365, true );
		add_image_size( 'post-thumb-big-vertical', 546, 770, true );
		add_image_size( 'post-thumb-medium', 364, 274, true );
		add_image_size( 'post-related-medium', 195, 144, true );
		add_image_size( 'post-related-big', 195, 275, true );
		add_image_size( 'widget-recent-posts', 270, 105, true );
		add_image_size( 'widget-post', 270, 200, true );
		add_image_size( 'widget-product', 270, 270, true );
		
		
		// Retina images
		$retina_support_enabled = $this->get_option( 'retina_support', 'general' );
		
		if( $retina_support_enabled == 'yes' ) {
			add_image_size( 'thumbnail-2x', 300, 300, true );
			add_image_size( 'medium-2x', 600, 600, true );
			add_image_size( 'full-2x', 1000, 1000, true );
			
			add_image_size( 'wproto-admin-thumb-2x', 200, 150, true );
			add_image_size( 'wproto-admin-thumb-medium-2x', 300, 300, true );
			add_image_size( 'wproto-admin-category-thumb-2x', 540, 340, true );
			 
			add_image_size( 'wproto-rss-image-2x', 1080, 680, true );
			
			// Front images @2x
			add_image_size( 'wproto-mega-menu-thumb-2x', 540, 160, true );
			add_image_size( 'benefits-icon-2x', 194, 194, true );
			add_image_size( 'partners-clients-logo-2x', 340, 310, true );
			add_image_size( 'portfolio-square-big-2x', 672, 672, true );
			add_image_size( 'portfolio-square-medium-2x', 330, 330, true );
			add_image_size( 'photo-small-2x', 170, 170, true );
			add_image_size( 'shop-product-preview-2x', 360, 360, true );
			add_image_size( 'shop-product-preview-small-2x', 134, 136, true );
			add_image_size( 'shop-product-small-2x', 174, 174, true );			
			add_image_size( 'shop-product-thumb-2x', 528, 542, true );
			add_image_size( 'shop-product-thumb-medium-2x', 388, 398, true );
			add_image_size( 'shop-product-big-2x', 720, 738, true );
			add_image_size( 'shop-buy-together-2x', 268, 272, true );
			add_image_size( 'shop-related-2x', 360, 364, true );
			add_image_size( 'shop-cart-2x', 126, 126, true );
			add_image_size( 'author-thumb-2x', 534, 396, true );
			add_image_size( 'new-scroll-thumb-2x', 560, 422, true );
			add_image_size( 'portfolio-scroll-thumb-2x', 340, 216, true );
			add_image_size( 'portfolio-hexagon-thumb-2x', 620, 620, true );
			add_image_size( 'header-menu-cat-thumb-2x', 580, 360, true );
			add_image_size( 'post-thumb-full-2x', 2134, 1066, true );
			add_image_size( 'category-thumb-full-2x', 2134, 460, true );
			add_image_size( 'post-thumb-big-2x', 1040, 730, true );
			add_image_size( 'post-thumb-big-vertical-2x', 1092, 1540, true );
			add_image_size( 'post-thumb-medium-2x', 728, 548, true );
			add_image_size( 'post-related-medium-2x', 360, 288, true );
			add_image_size( 'post-related-big-2x', 540, 1100, true );
			add_image_size( 'widget-recent-posts-2x', 540, 210, true );
			add_image_size( 'widget-post-2x', 540, 400, true );
			add_image_size( 'widget-product-2x', 540, 540, true );
		}
		
	}
	
	/**
	 * Register image names
	 **/
	function register_image_names( $sizes ) {
		//$sizes[ 'wproto-clients-logo' ] = __( 'Clients logo image', 'wproto' );
		return $sizes;
	}
	
	
	/**
	 * Register custom post types
	 **/
	function register_custom_post_types() {
		
		register_post_type( 'wproto_pricing_table',
			array(
				'label' 					=> __( 'Pricing Tables', 'wproto'),
				'description' 		=> '',
				'public' 					=> FALSE,
				'show_ui' 				=> TRUE,
				'show_in_menu' 		=> TRUE,
				'show_in_nav_menus' => FALSE,
				//'menu_position' 	=> 26,
				//'menu_icon' 			=> WPROTO_THEME_URL . '/images/admin/pricing_tables.png',
				'capability_type' => 'post',
				'hierarchical' 		=> FALSE,
				'supports' 				=> array( 'title', 'custom-fields' ),
				'rewrite' 				=> FALSE,
				'has_archive' 		=> FALSE,
				'query_var' 			=> TRUE,
				'capabilities' => array(
        	'publish_posts' => 'edit_pages',
        	'edit_posts' => 'edit_pages',
        	'edit_others_posts' => 'edit_pages',
        	'delete_posts' => 'edit_pages',
        	'delete_others_posts' => 'edit_pages',
        	'read_private_posts' => 'edit_pages',
        	'edit_post' => 'edit_pages',
        	'delete_post' => 'edit_pages',
        	'read_post' => 'edit_pages',
    		),
				'labels'					=> array(
					'name' 									=> __( 'Pricing Tables', 'wproto'),
					'singular_name' 				=> __( 'Pricing Table', 'wproto'),
					'menu_name' 						=> __( 'Pricing Tables', 'wproto'),
					'add_new' 							=> __( 'Add Pricing Table', 'wproto'),
					'add_new_item' 					=> __( 'Add New Pricing Table', 'wproto'),
					'all_items' 						=> __( 'All Pricing Tables', 'wproto'),
					'edit_item' 						=> __( 'Edit Pricing Table', 'wproto'),
					'new_item' 							=> __( 'New Pricing Table', 'wproto'),
					'view_item' 						=> __( 'View Pricing Table', 'wproto'),
					'search_items' 					=> __( 'Search Pricing Tables', 'wproto'),
					'not_found' 						=> __( 'No Pricing Tables Found', 'wproto'),
					'not_found_in_trash'		=> __( 'No Pricing Tables Found in Trash', 'wproto'),
					'parent_item_colon' 		=> __( 'Parent Pricing Table:', 'wproto') )
			)
		);
		
		register_post_type( 'wproto_partners',
			array(
				'label' 					=> __( 'Partners / Clients', 'wproto'),
				'description' 		=> '',
				'public' 					=> FALSE,
				'show_ui' 				=> TRUE,
				'show_in_menu' 		=> TRUE,
				'show_in_nav_menus' => FALSE,
				'exclude_from_search' => TRUE,
				//'menu_position' 	=> 26,
				//'menu_icon' 			=> WPROTO_THEME_URL . '/images/admin/partner.png',
				'capability_type' => 'post',
				'hierarchical' 		=> FALSE,
				'supports' 				=> array( 'title', 'custom-fields', 'thumbnail', 'editor', 'excerpt' ),
				'rewrite' 				=> FALSE,
				'has_archive' 		=> FALSE,
				'query_var' 			=> FALSE,
				'capabilities' => array(
        	'publish_posts' => 'edit_pages',
        	'edit_posts' => 'edit_pages',
        	'edit_others_posts' => 'edit_pages',
        	'delete_posts' => 'edit_pages',
        	'delete_others_posts' => 'edit_pages',
        	'read_private_posts' => 'edit_pages',
        	'edit_post' => 'edit_pages',
        	'delete_post' => 'edit_pages',
        	'read_post' => 'edit_pages',
    		),
				'labels' 					=> array(
					'name' 									=> __( 'Partners / Clients', 'wproto'),
					'singular_name' 				=> __( 'Partner / Client', 'wproto'),
					'menu_name' 						=> __( 'Partners / Clients', 'wproto'),
					'add_new' 							=> __( 'Add Partner / Client', 'wproto'),
					'add_new_item' 					=> __( 'Add New Partner / Client', 'wproto'),
					'all_items' 						=> __( 'All Partners / Clients', 'wproto'),
					'edit_item' 						=> __( 'Edit Partner / Client', 'wproto'),
					'new_item' 							=> __( 'New Partner / Client', 'wproto'),
					'view_item' 						=> __( 'View Partner / Client', 'wproto'),
					'search_items' 					=> __( 'Search Partners / Clients', 'wproto'),
					'not_found' 						=> __( 'No Partners / Clients Found', 'wproto'),
					'not_found_in_trash' 		=> __( 'No Partners / Clients Found in Trash', 'wproto'),
					'parent_item_colon' 		=> __( 'Parent Partner / Client:', 'wproto') )
			)
		);
		
		if( $this->get_option( 'disable_catalog', 'general' ) != 'yes' ):
		
		register_post_type( 'wproto_catalog',
			array(
				'label' 					=> __( 'Catalog', 'wproto'),
				'description' 		=> '',
				'public' 					=> TRUE,
				'show_ui' 				=> TRUE,
				'show_in_nav_menus' => TRUE,
				'show_in_menu' 		=> TRUE,
				//'menu_position' 	=> 20,
				//'menu_icon' 			=> WPROTO_THEME_URL . '/images/admin/catalog.png',
				'capability_type' => 'post',
				'hierarchical' 		=> FALSE,
				'supports' 				=> array( 'title', 'custom-fields', 'thumbnail', 'editor', 'excerpt', 'comments' ),
				'rewrite' 				=> array( 'slug' => 'catalog' ),
				'has_archive' 		=> FALSE,
				'query_var' 			=> TRUE,
				'capabilities' => array(
        	'publish_posts' => 'edit_pages',
        	'edit_posts' => 'edit_pages',
        	'edit_others_posts' => 'edit_pages',
        	'delete_posts' => 'edit_pages',
        	'delete_others_posts' => 'edit_pages',
        	'read_private_posts' => 'edit_pages',
        	'edit_post' => 'edit_pages',
        	'delete_post' => 'edit_pages',
        	'read_post' => 'edit_pages',
    		),
				'labels' 					=> array(
					'name' 									=> __( 'Catalog', 'wproto'),
					'singular_name' 				=> __( 'Catalog item', 'wproto'),
					'menu_name' 						=> __( 'Catalog', 'wproto'),
					'add_new' 							=> __( 'Add Catalog item', 'wproto'),
					'add_new_item'					=> __( 'Add New Catalog item', 'wproto'),
					'all_items' 						=> __( 'All Catalog items', 'wproto'),
					'edit_item' 						=> __( 'Edit Catalog item', 'wproto'),
					'new_item' 							=> __( 'New Catalog item', 'wproto'),
					'view_item' 						=> __( 'View Catalog item', 'wproto'),
					'search_items' 					=> __( 'Search Catalog items', 'wproto'),
					'not_found' 						=> __( 'No Catalog items Found', 'wproto'),
					'not_found_in_trash' 		=> __( 'No Catalog items Found in Trash', 'wproto'),
					'parent_item_colon' 		=> __( 'Parent Catalog item:', 'wproto') )
			)
		);
		
		endif;
		
		if( $this->get_option( 'disable_portfolio', 'general' ) != 'yes' ):
		
		register_post_type( 'wproto_portfolio',
			array(
				'label' 					=> __( 'Portfolio', 'wproto'),
				'description'			=> '',
				'public' 					=> TRUE,
				'show_ui' 				=> TRUE,
				'show_in_menu'		=> TRUE,
				'show_in_nav_menus' => TRUE,
				//'menu_position' 	=> 20,
				//'menu_icon' 			=> WPROTO_THEME_URL . '/images/admin/portfolio.png',
				'capability_type' => 'post',
				'hierarchical' 		=> FALSE,
				'supports' 				=> array( 'title', 'custom-fields', 'thumbnail', 'editor', 'excerpt', 'comments' ),
				'rewrite' 				=> array( 'slug' => 'portfolio' ),
				'has_archive' 		=> FALSE,
				'query_var' 			=> TRUE,
				'capabilities' => array(
        	'publish_posts' => 'edit_pages',
        	'edit_posts' => 'edit_pages',
        	'edit_others_posts' => 'edit_pages',
        	'delete_posts' => 'edit_pages',
        	'delete_others_posts' => 'edit_pages',
        	'read_private_posts' => 'edit_pages',
        	'edit_post' => 'edit_pages',
        	'delete_post' => 'edit_pages',
        	'read_post' => 'edit_pages',
    		),
				'labels' 					=> array(
					'name' 									=> __( 'Portfolio', 'wproto'),
					'singular_name' 				=> __( 'Portfolio item', 'wproto'),
					'menu_name' 						=> __( 'Portfolio', 'wproto'),
					'add_new' 							=> __( 'Add Portfolio item', 'wproto'),
					'add_new_item' 					=> __( 'Add New Portfolio item', 'wproto'),
					'all_items' 						=> __( 'All Portfolio items', 'wproto'),
					'edit_item' 						=> __( 'Edit Portfolio item', 'wproto'),
					'new_item' 							=> __( 'New Portfolio item', 'wproto'),
					'view_item' 						=> __( 'View Portfolio item', 'wproto'),
					'search_items'					=> __( 'Search Portfolio items', 'wproto'),
					'not_found' 						=> __( 'No Portfolio items Found', 'wproto'),
					'not_found_in_trash' 		=> __( 'No Portfolio items Found in Trash', 'wproto'),
					'parent_item_colon' 		=> __( 'Parent Portfolio item:', 'wproto') )
			)
		);
		
		endif;
		
		register_post_type( 'wproto_team',
			array(
				'label' 					=> __( 'Team', 'wproto'),
				'description' 		=> '',
				'public' 					=> FALSE,
				'show_ui' 				=> TRUE,
				'show_in_menu' 		=> TRUE,
				'exclude_from_search' => TRUE,
				'show_in_nav_menus' => FALSE,
				//'menu_position' 	=> 26,
				//'menu_icon' 			=> WPROTO_THEME_URL . '/images/admin/team.png',
				'capability_type' => 'post',
				'hierarchical' 		=> FALSE,
				'supports' 				=> array( 'title', 'editor', 'custom-fields', 'thumbnail' ),
				'rewrite' 				=> FALSE,
				'has_archive' 		=> FALSE,
				'query_var' 			=> FALSE,
				'capabilities' => array(
        	'publish_posts' => 'edit_pages',
        	'edit_posts' => 'edit_pages',
        	'edit_others_posts' => 'edit_pages',
        	'delete_posts' => 'edit_pages',
        	'delete_others_posts' => 'edit_pages',
        	'read_private_posts' => 'edit_pages',
        	'edit_post' => 'edit_pages',
        	'delete_post' => 'edit_pages',
        	'read_post' => 'edit_pages',
    		),
				'labels' 					=> array(
					'name' 									=> __( 'Team', 'wproto'),
					'singular_name' 				=> __( 'Member', 'wproto'),
					'menu_name' 						=> __( 'Team members', 'wproto'),
					'add_new' 							=> __( 'Add team member', 'wproto'),
					'add_new_item' 					=> __( 'Add New team member', 'wproto'),
					'all_items' 						=> __( 'All team members', 'wproto'),
					'edit_item' 						=> __( 'Edit team member', 'wproto'),
					'new_item' 							=> __( 'New team member', 'wproto'),
					'view_item' 						=> __( 'View team member', 'wproto'),
					'search_items' 					=> __( 'Search team members', 'wproto'),
					'not_found' 						=> __( 'No team members Found', 'wproto'),
					'not_found_in_trash' 		=> __( 'No team members Found in Trash', 'wproto'),
					'parent_item_colon' 		=> __( 'Parent team member:', 'wproto') )
			)
		);
		
		register_post_type( 'wproto_benefits',
			array(
				'label' 					=> __( 'Benefits', 'wproto'),
				'description' 		=> '',
				'public' 					=> FALSE,
				'show_ui' 				=> TRUE,
				'show_in_menu' 		=> TRUE,
				'exclude_from_search' => TRUE,
				'show_in_nav_menus' => FALSE,
				//'menu_position' 	=> 26,
				//'menu_icon' 			=> WPROTO_THEME_URL . '/images/admin/benefit.png',
				'capability_type' => 'post',
				'hierarchical' 		=> FALSE,
				'supports' 				=> array( 'title', 'editor', 'custom-fields', 'thumbnail' ),
				'rewrite' 				=> FALSE,
				'has_archive' 		=> FALSE,
				'query_var' 			=> FALSE,
				'capabilities' => array(
        	'publish_posts' => 'edit_pages',
        	'edit_posts' => 'edit_pages',
        	'edit_others_posts' => 'edit_pages',
        	'delete_posts' => 'edit_pages',
        	'delete_others_posts' => 'edit_pages',
        	'read_private_posts' => 'edit_pages',
        	'edit_post' => 'edit_pages',
        	'delete_post' => 'edit_pages',
        	'read_post' => 'edit_pages',
    		),
				'labels' 					=> array(
					'name' 									=> __( 'Benefits', 'wproto'),
					'singular_name'					=> __( 'Benefit', 'wproto'),
					'menu_name' 						=> __( 'Benefits', 'wproto'),
					'add_new' 							=> __( 'Add Benefit', 'wproto'),
					'add_new_item' 					=> __( 'Add New Benefit', 'wproto'),
					'all_items' 						=> __( 'All Benefits', 'wproto'),
					'edit_item' 						=> __( 'Edit Benefit', 'wproto'),
					'new_item' 							=> __( 'New Benefit', 'wproto'),
					'view_item' 						=> __( 'View Benefit', 'wproto'),
					'search_items' 					=> __( 'Search Benefits', 'wproto'),
					'not_found' 						=> __( 'No Benefits Found', 'wproto'),
					'not_found_in_trash' 		=> __( 'No Benefits Found in Trash', 'wproto'),
					'parent_item_colon' 		=> __( 'Parent Benefit:', 'wproto') )
			)
		);
		
		register_post_type( 'wproto_testimonials',
			array(
				'label' 					=> __( 'Testimonials', 'wproto'),
				'description' 		=> '',
				'public' 					=> FALSE,
				'show_ui' 				=> TRUE,
				'show_in_menu' 		=> TRUE,
				'show_in_nav_menus' => FALSE,
				'exclude_from_search' => TRUE,
				//'menu_position' 	=> 26,
				//'menu_icon' 			=> WPROTO_THEME_URL . '/images/admin/testmonial.png',
				'capability_type' => 'post',
				'hierarchical' 		=> FALSE,
				'supports' 				=> array( 'title', 'editor', 'thumbnail' ),
				'rewrite' 				=> FALSE,
				'has_archive' 		=> FALSE,
				'query_var' 			=> FALSE,
				'capabilities' => array(
        	'publish_posts' => 'edit_pages',
        	'edit_posts' => 'edit_pages',
        	'edit_others_posts' => 'edit_pages',
        	'delete_posts' => 'edit_pages',
        	'delete_others_posts' => 'edit_pages',
        	'read_private_posts' => 'edit_pages',
        	'edit_post' => 'edit_pages',
        	'delete_post' => 'edit_pages',
        	'read_post' => 'edit_pages',
    		),
				'labels' 					=> array(
					'name' 									=> __( 'Testimonials', 'wproto'),
					'singular_name' 				=> __( 'Testimonial', 'wproto'),
					'menu_name' 						=> __( 'Testimonials', 'wproto'),
					'add_new' 							=> __( 'Add Testimonial', 'wproto'),
					'add_new_item' 					=> __( 'Add New Testimonial', 'wproto'),
					'all_items' 						=> __( 'All Testimonials', 'wproto'),
					'edit_item' 						=> __( 'Edit Testimonial', 'wproto'),
					'new_item' 							=> __( 'New Testimonial', 'wproto'),
					'view_item' 						=> __( 'View Testimonial', 'wproto'),
					'search_items'					=> __( 'Search Testimonials', 'wproto'),
					'not_found' 						=> __( 'No Testimonials Found', 'wproto'),
					'not_found_in_trash' 		=> __( 'No Testimonials Found in Trash', 'wproto'),
					'parent_item_colon' 		=> __( 'Parent Testimonial:', 'wproto') )
			)
		);
		
		if( $this->get_option( 'disable_video', 'general' ) != 'yes' ):
		
		register_post_type( 'wproto_video',
			array(
				'label' 					=> __( 'Videos', 'wproto'),
				'description' 		=> '',
				'public' 					=> TRUE,
				'show_ui' 				=> TRUE,
				'show_in_menu' 		=> TRUE,
				'show_in_nav_menus' => TRUE,
				//'menu_position' 	=> 10,
				//'menu_icon' 			=> WPROTO_THEME_URL . '/images/admin/video.png',
				'capability_type' => 'post',
				'hierarchical' 		=> FALSE,
				'supports' 				=> array( 'title', 'custom-fields', 'thumbnail', 'editor', 'excerpt', 'comments' ),
				'rewrite' 				=> array( 'slug' => 'video' ),
				'has_archive' 		=> FALSE,
				'query_var' 			=> TRUE,
				'capabilities' => array(
        	'publish_posts' => 'edit_pages',
        	'edit_posts' => 'edit_pages',
        	'edit_others_posts' => 'edit_pages',
        	'delete_posts' => 'edit_pages',
        	'delete_others_posts' => 'edit_pages',
        	'read_private_posts' => 'edit_pages',
        	'edit_post' => 'edit_pages',
        	'delete_post' => 'edit_pages',
        	'read_post' => 'edit_pages',
    		),
				'labels' 					=> array(
					'name' 									=> __( 'Videos', 'wproto'),
					'singular_name' 				=> __( 'Video', 'wproto'),
					'menu_name' 						=> __( 'Videos', 'wproto'),
					'add_new' 							=> __( 'Add Video', 'wproto'),
					'add_new_item' 					=> __( 'Add New Video', 'wproto'),
					'all_items' 						=> __( 'All Videos', 'wproto'),
					'edit_item' 						=> __( 'Edit Video', 'wproto'),
					'new_item' 							=> __( 'New Video', 'wproto'),
					'view_item' 						=> __( 'View Video', 'wproto'),
					'search_items' 					=> __( 'Search Videos', 'wproto'),
					'not_found' 						=> __( 'No Videos Found', 'wproto'),
					'not_found_in_trash' 		=> __( 'No Videos Found in Trash', 'wproto'),
					'parent_item_colon' 		=> __( 'Parent Video:', 'wproto') )
			)
		);
		
		endif;
		
		if( $this->get_option( 'disable_photoalbums', 'general' ) != 'yes' ):
		
		register_post_type( 'wproto_photoalbums',
			array(
				'label' 					=> __( 'Photo albums', 'wproto'),
				'description' 		=> '',
				'public' 					=> TRUE,
				'show_ui' 				=> TRUE,
				'show_in_menu' 		=> TRUE,
				'show_in_nav_menus' => TRUE,
				//'menu_position' 	=> 10,
				//'menu_icon' 			=> WPROTO_THEME_URL . '/images/admin/photoalbum.png',
				'capability_type' => 'post',
				'hierarchical' 		=> FALSE,
				'supports' 				=> array( 'title', 'custom-fields', 'thumbnail', 'editor', 'comments' ),
				'rewrite' 				=> array( 'slug' => 'album' ),
				'has_archive' 		=> FALSE,
				'query_var' 			=> TRUE,
				'capabilities' => array(
        	'publish_posts' => 'edit_pages',
        	'edit_posts' => 'edit_pages',
        	'edit_others_posts' => 'edit_pages',
        	'delete_posts' => 'edit_pages',
        	'delete_others_posts' => 'edit_pages',
        	'read_private_posts' => 'edit_pages',
        	'edit_post' => 'edit_pages',
        	'delete_post' => 'edit_pages',
        	'read_post' => 'edit_pages',
    		),
				'labels'					=> array(
					'name' 									=> __( 'Photo albums', 'wproto'),
					'singular_name' 				=> __( 'Photo album', 'wproto'),
					'menu_name' 						=> __( 'Photo albums', 'wproto'),
					'add_new' 							=> __( 'Add Photo album', 'wproto'),
					'add_new_item' 					=> __( 'Add New Photo album', 'wproto'),
					'all_items' 						=> __( 'All Photo albums', 'wproto'),
					'edit_item' 						=> __( 'Edit Photo album', 'wproto'),
					'new_item' 							=> __( 'New Photo album', 'wproto'),
					'view_item' 						=> __( 'View Photo album', 'wproto'),
					'search_items' 					=> __( 'Search Photo albums', 'wproto'),
					'not_found' 						=> __( 'No Photo albums Found', 'wproto'),
					'not_found_in_trash'		=> __( 'No Photo albums Found in Trash', 'wproto'),
					'parent_item_colon' 		=> __( 'Parent Photo album:', 'wproto') )
			)
		);
		
		endif;
		
	}
	
	/**
	 * Register custom taxonomies
	 **/
	function register_taxonomies() {
		
		register_taxonomy( 'wproto_sidebars',
			NULL,
			array(
				'hierarchical' 				=> FALSE,
				'show_ui' 						=> TRUE,
				'query_var' 					=> FALSE,
				'rewrite' 						=> FALSE,
				'show_admin_column'   => FALSE,
				'show_in_nav_menus' => FALSE,
				'labels'              => array(
					'name'                => _x( 'Widget Areas', 'taxonomy general name', 'wproto' ),
					'singular_name'       => _x( 'Widget Area', 'taxonomy singular name', 'wproto' ),
					'search_items'        => __( 'Search Areas', 'wproto' ),
					'all_items'           => __( 'All Widget Areas', 'wproto' ),
					'edit_item'           => __( 'Edit Widget Area', 'wproto' ), 
					'update_item'         => __( 'Update Widget Area', 'wproto' ),
					'add_new_item'        => __( 'Add New Widget Area', 'wproto' ),
					'new_item_name'       => __( 'New Widget Area', 'wproto' ),
					'menu_name'           => __( 'Widget Area', 'wproto' )
				)
			)
		);
		
		register_taxonomy( 'wproto_partners_category',
			'wproto_partners',
			array(
				'hierarchical' 				=> TRUE,
				'show_ui' 						=> TRUE,
				'query_var' 					=> FALSE,
				'rewrite' 						=> FALSE,
				'show_in_nav_menus' => FALSE,
				'show_admin_column'   => TRUE,
				'labels'              => array(
					'name'                => _x( 'Partners Categories', 'taxonomy general name', 'wproto' ),
					'singular_name'       => _x( 'Partners Category', 'taxonomy singular name', 'wproto' ),
					'search_items'        => __( 'Search in categories', 'wproto' ),
					'all_items'           => __( 'All Categories', 'wproto' ),
					'edit_item'           => __( 'Edit Category', 'wproto' ), 
					'update_item'         => __( 'Update Category', 'wproto' ),
					'add_new_item'        => __( 'Add New Category', 'wproto' ),
					'new_item_name'       => __( 'New Category', 'wproto' ),
					'menu_name'           => __( 'Partners Categories', 'wproto' )
				)
			)
		);
		
		register_taxonomy( 'wproto_catalog_category',
			'wproto_catalog',
			array(
				'hierarchical' 				=> TRUE,
				'show_ui' 						=> TRUE,
				'query_var' 					=> TRUE,
				'show_in_nav_menus' => TRUE,
				'rewrite' 						=> array( 'slug' => 'catalog-category' ),
				'show_admin_column'   => TRUE,
				'labels'              => array(
					'name'                => _x( 'Catalog Categories', 'taxonomy general name', 'wproto' ),
					'singular_name'       => _x( 'Catalog Category', 'taxonomy singular name', 'wproto' ),
					'search_items'        => __( 'Search in categories', 'wproto' ),
					'all_items'           => __( 'All Categories', 'wproto' ),
					'edit_item'           => __( 'Edit Category', 'wproto' ), 
					'update_item'         => __( 'Update Category', 'wproto' ),
					'add_new_item'        => __( 'Add New Category', 'wproto' ),
					'new_item_name'       => __( 'New Category', 'wproto' ),
					'menu_name'           => __( 'Catalog Categories', 'wproto' )
				)
			)
		);
		
		register_taxonomy( 'wproto_catalog_tag',
			'wproto_catalog',
			array(
				'hierarchical' 				=> FALSE,
				'show_ui' 						=> TRUE,
				'query_var' 					=> TRUE,
				'show_in_nav_menus' => TRUE,
				'rewrite' 						=> array( 'slug' => 'catalog-tag' ),
				'show_admin_column'   => TRUE,
				'labels'              => array(
					'name'                => _x( 'Catalog Tags', 'taxonomy general name', 'wproto' ),
					'singular_name'       => _x( 'Catalog Tag', 'taxonomy singular name', 'wproto' ),
					'search_items'        => __( 'Search in tags', 'wproto' ),
					'all_items'           => __( 'All tags', 'wproto' ),
					'edit_item'           => __( 'Edit tag', 'wproto' ), 
					'update_item'         => __( 'Update tag', 'wproto' ),
					'add_new_item'        => __( 'Add New tag', 'wproto' ),
					'new_item_name'       => __( 'New tag', 'wproto' ),
					'menu_name'           => __( 'Catalog Tags', 'wproto' )
				)
			)
		);
		
		register_taxonomy( 'wproto_benefits_category',
			'wproto_benefits',
			array(
				'hierarchical' 				=> TRUE,
				'show_ui' 						=> TRUE,
				'query_var' 					=> FALSE,
				'show_in_nav_menus' => FALSE,
				'rewrite' 						=> FALSE,
				'show_admin_column'   => TRUE,
				'labels'              => array(
					'name'                => _x( 'Benefits Categories', 'taxonomy general name', 'wproto' ),
					'singular_name'       => _x( 'Benefits Category', 'taxonomy singular name', 'wproto' ),
					'search_items'        => __( 'Search in categories', 'wproto' ),
					'all_items'           => __( 'All Categories', 'wproto' ),
					'edit_item'           => __( 'Edit Category', 'wproto' ), 
					'update_item'         => __( 'Update Category', 'wproto' ),
					'add_new_item'        => __( 'Add New Category', 'wproto' ),
					'new_item_name'       => __( 'New Category', 'wproto' ),
					'menu_name'           => __( 'Benefits Categories', 'wproto' )
				)
			)
		);
		
		register_taxonomy( 'wproto_portfolio_category',
			'wproto_portfolio',
			array(
				'hierarchical' 				=> TRUE,
				'show_ui' 						=> TRUE,
				'show_in_nav_menus' => TRUE,
				'query_var' 					=> TRUE,
				'rewrite' 						=> array( 'slug' => 'portfolio-category' ),
				'show_admin_column'   => TRUE,
				'labels'              => array(
					'name'                => _x( 'Portfolio Categories', 'taxonomy general name', 'wproto' ),
					'singular_name'       => _x( 'Portfolio Category', 'taxonomy singular name', 'wproto' ),
					'search_items'        => __( 'Search in categories', 'wproto' ),
					'all_items'           => __( 'All Categories', 'wproto' ),
					'edit_item'           => __( 'Edit Category', 'wproto' ), 
					'update_item'         => __( 'Update Category', 'wproto' ),
					'add_new_item'        => __( 'Add New Category', 'wproto' ),
					'new_item_name'       => __( 'New Category', 'wproto' ),
					'menu_name'           => __( 'Portfolio Categories', 'wproto' )
				)
			)
		);
		
		register_taxonomy( 'wproto_team_category',
			'wproto_team',
			array(
				'hierarchical' 				=> TRUE,
				'show_ui' 						=> TRUE,
				'query_var' 					=> FALSE,
				'show_in_nav_menus' => FALSE,
				'rewrite' 						=> FALSE,
				'show_admin_column'   => TRUE,
				'labels'              => array(
					'name'                => _x( 'Team Categories', 'taxonomy general name', 'wproto' ),
					'singular_name'       => _x( 'Team Category', 'taxonomy singular name', 'wproto' ),
					'search_items'        => __( 'Search in categories', 'wproto' ),
					'all_items'           => __( 'All Categories', 'wproto' ),
					'edit_item'           => __( 'Edit Category', 'wproto' ), 
					'update_item'         => __( 'Update Category', 'wproto' ),
					'add_new_item'        => __( 'Add New Category', 'wproto' ),
					'new_item_name'       => __( 'New Category', 'wproto' ),
					'menu_name'           => __( 'Team Categories', 'wproto' )
				)
			)
		);
		
		register_taxonomy( 'wproto_testimonials_category',
			'wproto_testimonials',
			array(
				'hierarchical' 				=> TRUE,
				'show_ui' 						=> TRUE,
				'query_var' 					=> FALSE,
				'show_in_nav_menus' => FALSE,
				'rewrite' 						=> FALSE,
				'show_admin_column'   => TRUE,
				'labels'              => array(
					'name'                => _x( 'Testimonials Categories', 'taxonomy general name', 'wproto' ),
					'singular_name'       => _x( 'Testimonials Category', 'taxonomy singular name', 'wproto' ),
					'search_items'        => __( 'Search in categories', 'wproto' ),
					'all_items'           => __( 'All Categories', 'wproto' ),
					'edit_item'           => __( 'Edit Category', 'wproto' ), 
					'update_item'         => __( 'Update Category', 'wproto' ),
					'add_new_item'        => __( 'Add New Category', 'wproto' ),
					'new_item_name'       => __( 'New Category', 'wproto' ),
					'menu_name'           => __( 'Testimonials Categories', 'wproto' )
				)
			)
		);
		
		register_taxonomy( 'wproto_video_category',
			'wproto_video',
			array(
				'hierarchical' 				=> TRUE,
				'show_ui' 						=> TRUE,
				'show_in_nav_menus' => TRUE,
				'query_var' 					=> TRUE,
				'rewrite' 						=> array( 'slug' => 'video-category' ),
				'show_admin_column'   => TRUE,
				'labels'              => array(
					'name'                => _x( 'Video Categories', 'taxonomy general name', 'wproto' ),
					'singular_name'       => _x( 'Video Category', 'taxonomy singular name', 'wproto' ),
					'search_items'        => __( 'Search in categories', 'wproto' ),
					'all_items'           => __( 'All Categories', 'wproto' ),
					'edit_item'           => __( 'Edit Category', 'wproto' ), 
					'update_item'         => __( 'Update Category', 'wproto' ),
					'add_new_item'        => __( 'Add New Category', 'wproto' ),
					'new_item_name'       => __( 'New Category', 'wproto' ),
					'menu_name'           => __( 'Video Categories', 'wproto' )
				)
			)
		);
		
		register_taxonomy( 'wproto_video_tag',
			'wproto_video',
			array(
				'hierarchical' 				=> FALSE,
				'show_ui' 						=> TRUE,
				'query_var' 					=> TRUE,
				'show_in_nav_menus' => TRUE,
				'rewrite' 						=> array( 'slug' => 'video-tag' ),
				'show_admin_column'   => TRUE,
				'labels'              => array(
					'name'                => _x( 'Video Tags', 'taxonomy general name', 'wproto' ),
					'singular_name'       => _x( 'Video Tag', 'taxonomy singular name', 'wproto' ),
					'search_items'        => __( 'Search in tags', 'wproto' ),
					'all_items'           => __( 'All tags', 'wproto' ),
					'edit_item'           => __( 'Edit tag', 'wproto' ), 
					'update_item'         => __( 'Update tag', 'wproto' ),
					'add_new_item'        => __( 'Add New tag', 'wproto' ),
					'new_item_name'       => __( 'New tag', 'wproto' ),
					'menu_name'           => __( 'Video Tags', 'wproto' )
				)
			)
		);
		
		register_taxonomy( 'wproto_photoalbums_category',
			'wproto_photoalbums',
			array(
				'hierarchical' 				=> TRUE,
				'show_ui' 						=> TRUE,
				'query_var' 					=> TRUE,
				'show_in_nav_menus' => TRUE,
				'rewrite' 						=> array( 'slug' => 'album-category' ),
				'show_admin_column'   => TRUE,
				'labels'              => array(
					'name'                => _x( 'Photoalbum Categories', 'taxonomy general name', 'wproto' ),
					'singular_name'       => _x( 'Photoalbum Category', 'taxonomy singular name', 'wproto' ),
					'search_items'        => __( 'Search in categories', 'wproto' ),
					'all_items'           => __( 'All Categories', 'wproto' ),
					'edit_item'           => __( 'Edit Category', 'wproto' ), 
					'update_item'         => __( 'Update Category', 'wproto' ),
					'add_new_item'        => __( 'Add New Category', 'wproto' ),
					'new_item_name'       => __( 'New Category', 'wproto' ),
					'menu_name'           => __( 'Photoalbum Categories', 'wproto' )
				)
			)
		);
		
	}
	
	/**
	 * Register sidebars
	 **/
	function register_sidebars() {
		
		global $pagenow;
		
		if( $pagenow == 'themes.php' && isset( $_GET['activated'] ) ) {
			
			$side_left = term_exists( 'sidebar-left', 'wproto_sidebars' );

			if( $side_left === 0 || $side_left === NULL ) {
				
				wp_insert_term( __( 'Left sidebar', 'wproto' ), 'wproto_sidebars', array(
					'description' => '',
					'slug' => 'sidebar-left'
				));
				
			}
		
			$side_right = term_exists( 'sidebar-right', 'wproto_sidebars' );
			
			if( $side_right === 0 || $side_right === NULL ) {
		
				wp_insert_term( __( 'Right sidebar', 'wproto' ), 'wproto_sidebars', array(
					'description' => '',
					'slug' => 'sidebar-right'
				));
		
			}
			
			$side_footer = term_exists( 'sidebar-footer', 'wproto_sidebars' );
			
			if( $side_footer === 0 || $side_footer === NULL ) {
			
				wp_insert_term( __( 'Footer Widget Area', 'wproto' ), 'wproto_sidebars', array(
					'description' => '',
					'slug' => 'sidebar-footer'
				));
				
			}
			
			$side_shop = term_exists( 'shop', 'wproto_sidebars' );
			
			if( $side_shop === 0 || $side_shop === NULL ) {
			
				wp_insert_term( __( 'Shop Widget Area', 'wproto' ), 'wproto_sidebars', array(
					'description' => '',
					'slug' => 'shop'
				));
				
			}
			
		}
		
		$sidebars = get_terms( 'wproto_sidebars', array( 'hide_empty' => false ) );
		
		if( count( $sidebars ) > 0 ) {
			foreach( $sidebars as $sidebar ) {
				
				register_sidebar( array(
					'name'          => $sidebar->name,
					'id'            => $sidebar->slug,
					'description'   => $sidebar->description,
					'class'         => $sidebar->slug,
					'before_widget' => '<div id="%1$s" class="widget %2$s">',
					'after_widget'  => '<div class="clear"></div></div>',
					'before_title'  => '<h4 class="widget-title">',
					'after_title'   => '</h4>'
				));
				
			}
		}
		
	}
		
}