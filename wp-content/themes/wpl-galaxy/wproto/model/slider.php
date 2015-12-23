<?php
	/**
   * Slides model
   **/
	class wpl_galaxy_wp_slider extends wpl_galaxy_wp_database {                     
		/**
		 * Get Layer Slider slideshows
		 **/
		function get_layerslider_slideshows() {
			
			$table = $this->tables['layerslider'];

			return $this->wpdb->get_results(
				"SELECT *
					FROM $table
					WHERE 1"
			);
			
		}
                
	}