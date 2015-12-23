<?php
	/**
   * Taxonomies model
   **/
	class wpl_galaxy_wp_taxonomies extends wpl_galaxy_wp_database {    
		
		/**
		 * Get supported taxonomies
		 **/
		function get_supported() {
			
			$taxes = array();
			
			$taxes['category'] = get_terms( 'category', array(
				'hide_empty' => 0
			));
		
			$taxes['wproto_portfolio_category'] = get_terms( 'wproto_portfolio_category', array(
				'hide_empty' => 0
			));
		
			$taxes['wproto_video_category'] = get_terms( 'wproto_video_category', array(
				'hide_empty' => 0
			));
		
			$taxes['wproto_catalog_category'] = get_terms( 'wproto_catalog_category', array(
				'hide_empty' => 0
			));
		
			$taxes['product_cat'] = get_terms( 'product_cat', array(
				'hide_empty' => 0
			));
			
			return $taxes;
			
		}
		
	}
	
	