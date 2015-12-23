<?php

class wpl_galaxy_wp_installation extends wpl_galaxy_wp_database {
	/**
	 * Install Tables
	 **/
	function install() {
		global $wpl_galaxy_wp;
		$fonts_file = WPROTO_ENGINE_DIR . '/fonts.txt';

		update_option( 'wproto_show_demo_data_message', 'yes' );
		if( file_exists( $fonts_file ) ) {
			update_option( 'wproto_google_fonts_list', serialize( json_decode( file_get_contents( $fonts_file ) ) ) );
		}
		
		wp_schedule_event( time() + 1800, 'weekly', 'wproto_weekly_cron');
		
		require_once( ABSPATH . 'wp-admin/includes/upgrade.php' );
		
		/** Sections table **/
		$table_name = $this->tables['sections'];
		
		if( $this->wpdb->get_var( "SHOW TABLES LIKE '$table_name'" ) != $table_name ) {
		      
			$sql = "CREATE TABLE `" . $table_name . "` (
				`ID` bigint(20) NOT NULL AUTO_INCREMENT,
				`title` varchar(255) NOT NULL,
				`subtitle` varchar(255) NOT NULL,
				`before_text` longtext NOT NULL,
				`after_text` longtext NOT NULL,
				`status` enum('default','system') NOT NULL DEFAULT 'default',
				`type` varchar(100) NOT NULL,
				`data` longtext NOT NULL,
				PRIMARY KEY (`ID`)
				) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
			";

			dbDelta( $sql );
			
		}
		
		$default_settings = array(
			'general' => array(

			)
		);
		
		// set default settings
		foreach( $default_settings as $env=>$v ) {
				
			if( is_array( $v ) && count( $v ) > 0 ) {
				foreach( $v as $option_name=>$option_value )
				$wpl_galaxy_wp->set_option( $option_name, $option_value, $env );
			}
				
		}
			
		$wpl_galaxy_wp->write_all_settings();

	}

	/**
	 * Uninstall DB tables & remove options
	 **/
	function uninstall() {

		wp_clear_scheduled_hook( 'wproto_weekly_cron' );

		delete_option( 'wproto_show_demo_data_message' );
		delete_option( 'wproto_google_fonts_list' );
		delete_option( 'wproto_settings_general' );
		
		flush_rewrite_rules( true );

	}
	
}