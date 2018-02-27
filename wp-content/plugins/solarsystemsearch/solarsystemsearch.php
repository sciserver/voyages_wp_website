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

// Only allow this script to be run within WordPress
defined('ABSPATH') or die("Unknown Access Error");

define( 'SSSWP_DIR_PATH' , plugin_dir_path( __FILE__ ) );
define( 'SSSWP_DIR_URL' , plugin_dir_url( __FILE__ ) );
define( 'SSSWP_DEVELOP' , TRUE );

// load the class file
require_once( SSSWP_DIR_PATH . 'lib/solarsystemsearch.php' );

// Let's roll!
ssswp_plugin();
