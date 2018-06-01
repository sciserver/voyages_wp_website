<?php
/*
Plugin Name: SolarSystemSearch Core Plugin
Plugin URI: http://www.voyages.sdss.org
Description: Query SDSS MSSQL DB
Version: 1.0.0
Author: Bonnie Souter
Author URI: https://github.com/bonbons0220
License: MIT
*/

/**
 * Singleton class for setting up the plugin.
 *
 */
final class SolarSystemSearch {

	public $dir_path = '';
	public $dir_uri = '';
	//public $admin_dir = '';
	public $lib_dir = '';
	public $includes_dir = '';
	//public $templates_dir = '';
	public $css_uri = '';
	public $js_uri = '';
	public $bootstrap_uri = '';

	/**
	 * Returns the instance.
	 */
	public static function get_instance() {

		// THERE CAN ONLY BE ONE
		static $instance = null;
		if ( is_null( $instance ) ) {
			
			$instance = new SolarSystemSearch;
			$instance->setup();
			$instance->libs();
			$instance->setup_actions();
		}
		return $instance;
	}
	
	/**
	 * Constructor method.
	 */
	private function __construct() {
		
		//Add Scripts
		add_action( 'wp_enqueue_scripts', array( $this , 'register_ssswp_script' ) );
		
		//Add Shortcodes
		add_shortcode( 'solarsystemsearch' , array( $this , 'solarsystemsearch_shortcode' ) );
		
		//Add page(s) to the Admin Menu
		add_action( 'admin_menu' , array( $this , 'ssswp_menu' ) );

	}
	
	 /**
	 * Add shortcodes menu
	**/
	function ssswp_menu() {

		// Add a submenu item and page to Tools 
		add_management_page( 'SolarSystemSearch Settings', 'SolarSystemSearch Settings', 'export', 'ssswp-tools-page' , array( 	$this , 'ssswp_tools_page' ) );
		
	}

	/**
	 * Add shortcodes page
	**/
	function ssswp_tools_page() {
		
		if ( !current_user_can( 'export' ) )  {
				wp_die( __( 'You do not have sufficient permissions to access this page.' ) );
		}
		echo '<div class="ssswp-tools-wrap">';
		echo '<h2>SolarSystemSearch Settings</h2>';
		echo '</div>';	
	}

	//
	function register_ssswp_script() {
		
		//Scripts to be Registered, but not enqueued. This example requires jquery 
		wp_register_script( 'solarsystemsearch-script', $this->js_uri . "solarsystemsearch.js" , array() , '1.0.0', true );
		
		//Styles to be Registered, but not enqueued
		wp_register_style( 'solarsystemsearch-style', $this->css_uri . "solarsystemsearch.css" );
		
	}

	public function solarsystemsearch_shortcode( $atts = array() ) {

		$result='';

		$webroot = $this->dir_uri;
		
		$which = self::setAtts( $atts , 'where' , array( 'mcporb' ) , 'mpcorb' );
		
		//Shortcode loads scripts and styles
		wp_enqueue_script( 'solarsystemsearch-script' );
		wp_enqueue_style( 'solarsystemsearch-style' );
		if ( defined( 'SSSWP_DEVELOP' ) && SSSWP_DEVELOP ) 
			wp_enqueue_script( 'bootstrap' );
		else
			wp_enqueue_script( 'bootstrap-min' );
		
		$ssswp_form = file_get_contents( $this->includes_dir . "form-$which.php" );
		$ssswp_instructions = file_get_contents( $this->includes_dir . "instructions-$which.txt" );
		
		//Content 
		$result .= <<< EOT
<div id="ssswp-container" class="ssswp-wrap" data-ssswp-webroot="$webroot" data-ssswp-which="$which" >
<div class="row">
<div class="col-lg-12">
<div class="ssswp-messages-wrap">
<div class="ssswp-messages"></div>
</div>
</div>
<div class="col-xs-12">
<div class="ssswp-instructions-wrap well well-sm"> 
$ssswp_instructions
</div>
<div id="ssswp-form-wrap" class="ssswp-form-wrap well well-sm"> 
<p class="h4"><a role="button" data-toggle="collapse" href="#ssswp-form" aria-expanded="true" aria-controls="ssswp-form">SQL Search</a></p>
<div class="form ssswp-form collapse show">
$ssswp_form
</div>
</div>
</div>
<div class="col-xs-12">
<div class="ssswp-results-wrap well well-sm"> 
<p class="h4"><a role="button" data-toggle="collapse" href="#ssswp-results" aria-expanded="false" aria-controls="ssswp-results">Results</a></p>
<div id="ssswp-results" class="ssswp-results collapse"></div>
</div>
</div>
</div>
</div>
EOT;

		return $result;
	}

	/**
	 * Set the value for the attribute identified by $key 
	 * to one of allowed values, or to a default value.
	 */
	public function setAtts( $atts , $key , $allowed , $default ) {
	
		$value = ( !empty( $atts ) && 
			array_key_exists( $key , $atts ) && 
			in_array( $atts[ $key ] , $allowed ) ) ? 
				$atts[ $key ] : 
				$default ; 
			
			return $value;
	}

	/**
	 * Magic method to output a string if trying to use the object as a string.
	 */
	public function __toString() {
		return 'solarsystemsearch';
	}

	/**
	 * Magic method to keep the object from being cloned.
	 */
	public function __clone() {
		_doing_it_wrong( __FUNCTION__, esc_html__( 'Sorry, no can do.', 'solarsystemsearch' ), '1.0' );
	}

	/**
	 * Magic method to keep the object from being unserialized.
	 */
	public function __wakeup() {
		_doing_it_wrong( __FUNCTION__, esc_html__( 'Sorry, no can do.', 'solarsystemsearch' ), '1.0' );
	}

	/**
	 * Magic method to prevent a fatal error when calling a method that doesn't exist.
	 */
	public function __call( $method = '', $args = array() ) {
		_doing_it_wrong( "SolarSystemSearch::{$method}", esc_html__( 'Method does not exist.', 'solarsystemsearch' ), '1.0' );
		unset( $method, $args );
		return null;
	}

	/**
	 * Sets up globals.
	 */
	private function setup() {

		// Main plugin directory path and URI.
		$this->dir_path = trailingslashit( SSSWP_DIR_PATH );
		$this->dir_uri  = trailingslashit( SSSWP_DIR_URL );

		// Plugin directory paths.
		$this->lib_dir       = trailingslashit( $this->dir_path . 'lib'       );
		$this->includes_dir  = trailingslashit( $this->dir_path . 'includes'       );

		// Plugin directory URIs.
		$this->css_uri = trailingslashit( $this->dir_uri . 'css' );
		$this->js_uri  = trailingslashit( $this->dir_uri . 'js'  );
		$this->bootstrap_uri  = trailingslashit( $this->dir_uri . 'vendor/bootstrap/dist/js'  );
	}

	/**
	 * Loads files needed by the plugin.
	 */
	private function libs() {

		// Load include files.
		//require_once( $this->lib_dir . 'functions.php'                     );
		//require_once( $this->lib_dir . 'functions-widgets.php'             );

		// Load template files.
		//require_once( $this->lib_dir . 'template.php' );

		// Load admin/backend files.
		if ( is_admin() ) {

			// General admin functions.
			//require_once( $this->admin_dir . 'functions-admin.php' );
		
		}
	}

	/**
	 * Sets up main plugin actions and filters.
	 */
	private function setup_actions() {

		// Register activation hook.
		register_activation_hook( __FILE__, array( $this, 'activation' ) );
	}

	/**
	 * Method that runs only when the plugin is activated.
	 */
	public function activation() {

	}
	
}

/**
 * Gets the instance of the `SolarSystemSearch` class.  This function is useful for quickly grabbing data
 * used throughout the plugin.
 */
function ssswp_plugin() {
	return SolarSystemSearch::get_instance();
}
