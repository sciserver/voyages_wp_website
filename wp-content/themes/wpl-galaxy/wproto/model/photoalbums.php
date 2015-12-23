<?php
	/**
   * Photo Albums model
   **/
	class wpl_galaxy_wp_photoalbums extends wpl_galaxy_wp_database {                     
		/**
		 * Get All Photoalbums
		 * @return object
		 **/
		function get_all_albums() {
			
			$args = array(
				'post_type' => 'wproto_photoalbums',
				'post_status' => 'publish',
				'nopaging' => true
			);
			
			return new WP_Query( $args );
			
		}
		
		/**
		 * Get album
		 * @param int 
		 * @return array
		 **/
		function get_album( $id ) {
			
			$data = array();
			
			$data['album'] = get_post( $id );
			
			$args = array(
				'post_type' => 'attachment',
				'numberposts' => -1,
				'include' => get_post_meta( $id, 'wproto_attached_images', true )
			); 
			
			$data['album_photos'] = get_posts( $args );
			
			return $data;
			
		}
                
	}