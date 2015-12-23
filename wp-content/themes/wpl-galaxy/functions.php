<?php

	// TRUE to show demo stand
	// define( 'WPROTO_DEMO_STAND', true );

	if ( ! isset( $content_width ) ) $content_width = 0;

	// Define constants
	define( 'WPROTO_THEME_DIR', get_template_directory() );
	define( 'WPROTO_ENGINE_DIR', WPROTO_THEME_DIR . '/wproto' );
	define( 'WPROTO_THEME_URL', get_template_directory_uri() );
	define( 'WPROTO_ENGINE_URL', WPROTO_THEME_URL . '/wproto' );
	
	define( 'WPROTO_IS_RETINA', isset( $_COOKIE["device_pixel_ratio"] ) && $_COOKIE["device_pixel_ratio"] >= 2 );
	
	if( !function_exists( 'wp_dump' ) ) {
		function wp_dump() {
			if ( func_num_args() > 0 ) {
				
				$args = func_get_args();
				
				foreach( $args as $arg ) {
					echo '<pre>';
					var_dump( $arg );
					echo '</pre>';
				}
				
			}
		}
	}
	
	// Instantiate base controller that will autoload
	// all application classes. Each controller must state
	// the add_action() and add_filter() hooks it executes
	// in its own constructor for a quick orientation of
	// which methods serve which exact browser requests
	require_once 'wproto/controller/base-controller.php';
	global $wpl_galaxy_wp;
	$wpl_galaxy_wp = new wpl_galaxy_wp_base_controller( array( 'res_cache_time' => '240320141308' ));
	$wpl_galaxy_wp->dispatch();
	
	//Enqueue scripts
	add_action( 'wp_enqueue_scripts', 'voyages_add_scripts' );
	function voyages_add_scripts() {
		//enqueue latest bootstrap minified script from cdn
		wp_enqueue_script( 'bootstrap', 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js', array( 'jquery' ), false, false );
	}