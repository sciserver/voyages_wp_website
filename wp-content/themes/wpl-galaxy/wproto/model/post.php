<?php
	/**
   * Post model
   **/
	class wpl_galaxy_wp_post extends wpl_galaxy_wp_database {                     
		/**
		 * Get items
		 * @return object
		 **/
		function get( $type, $limit = 3, $category = 0, $order = 'date', $sort = 'DESC', $post_type = 'post', $tax_name = 'category', $featured_only = false, $sticky_only = false, $with_thumbnail_only = false, $paged = 1 ) {
			global $post;
			
			$args = array(
				'post_type' => $post_type,
				'post_status' => 'publish',
				'posts_per_page' => $limit,
				'order' => $sort,
				'orderby' => $order,
				'post__not_in' => isset( $post->ID ) ? array( $post->ID ) : array(),
				'ignore_sticky_posts' => 1,
				'paged' => $paged
			);
			
			if( $type == 'category' || $type == 'only' ) {
				$args['tax_query'] = array(
					array(
						'taxonomy' => $tax_name,
						'field' => 'id',
						'terms' => $category
					)
				);
			}
			
			if( $type == 'category_except' || $type == 'all_except' ) {
				$args['tax_query'] = array(
					array(
						'taxonomy' => $tax_name,
						'field' => 'id',
						'terms' => $category,
						'operator' => 'NOT IN'
					)
				);
			}
			
			if( $featured_only ) {
				$args['meta_query'][] = array(
					'key' => 'featured',
					'value' => 'yes'
				);
			}
			
			if( $with_thumbnail_only ) {
				$args['meta_query'][] = array(
					'key' => '_thumbnail_id'
				);
			}
			
			if( $sticky_only ) {
				$args['post__in'] = get_option( 'sticky_posts' );
			}
			
			return new WP_Query( $args );
			
		}
		
		/**
		 * Get all posts
		 **/
		function get_all_posts( $post_type ) {
			global $post;
			
			$args = array(
				'post_type' => $post_type,
				'post_status' => 'publish',
				'nopaging' => true
			);
			
			return new WP_Query( $args );
		}
		
		/**
		 * Get popular posts
		 **/
 		function get_popular_posts( $post_type, $popularity, $limit ) {
			$args = array(
				'post_type' => $post_type,
				'post_status' => 'publish',
				'posts_per_page' => $limit,
				'order' => 'DESC',
				'ignore_sticky_posts' => true
			);
			
			switch( $popularity ) {
				case 'likes':
					$args['meta_key'] = 'wproto_likes';
					$args['orderby'] = 'meta_value_num';
				break;
				case 'views':
					$args['meta_key'] = 'wproto_views';
					$args['orderby'] = 'meta_value_num';
				break;
				case 'comments':
					$args['orderby'] = 'comment_count';
				break;
			}
			
			return new WP_Query( $args );
 		}
 		
 		/**
 		 * Get recent posts
 		 **/
		function get_recent_posts( $post_type, $limit ) {
			$args = array(
				'post_type' => $post_type,
				'post_status' => 'publish',
				'posts_per_page' => $limit,
				'order' => 'DESC',
				'ignore_sticky_posts' => true
			);
			
			return new WP_Query( $args );
		}
		
		/**
		 * Get featured posts
		 **/
		function get_featured_posts( $post_type, $limit ) {
			$args = array(
				'post_type' => $post_type,
				'post_status' => 'publish',
				'posts_per_page' => $limit,
				'order' => 'DESC',
				'ignore_sticky_posts' => true,
				'meta_key' => 'featured',
				'meta_value' => 'yes',
				'orderby' => 'date'
			);
			
			return new WP_Query( $args );
		}
		
		/**
		 * Get related posts
		 **/
 		function get_related_posts( $primary_post_id, $limit, $taxonomy = 'category' ) {
 			
 			$terms = wp_get_post_terms( $primary_post_id, $taxonomy );
 			
 			$response = false;
 			
			if( count( $terms ) > 0 ) {
				
				$post_type = get_post_type( $primary_post_id );
				$post_terms_ids = array();
				
				foreach( $terms as $term ) {
					$post_terms_ids[] = $term->term_id;
				}
				
				$args = array(
					'post_type' => $post_type,
					'post_status' => 'publish',
					'posts_per_page' => $limit,
					'order' => 'DESC',
					'orderby' => 'rand',
					'ignore_sticky_posts' => true,
					'tax_query' => array(
						'relation' => 'OR',
						array(
							'taxonomy' => $taxonomy,
							'field' => 'id',
							'terms' => $post_terms_ids
						)
					)
				);
				
				$response = new WP_Query( $args );
				
			}
 			
 			return $response;
 		}
		
		/**
		 * Get random posts
		 **/
		function get_random_posts( $post_type, $limit ) {
			$args = array(
				'post_type' => $post_type,
				'post_status' => 'publish',
				'posts_per_page' => $limit,
				'ignore_sticky_posts' => true,
				'orderby' => 'rand'
			);
			
			return new WP_Query( $args );
		}
		
		/**
		 * Search post
		 **/
		function search_post_by_title( $search, $post_type ) {

			$query = "SELECT ID, post_title FROM " . $this->wpdb->posts . "
        WHERE post_title LIKE '%$search%'
        AND post_type = '$post_type'
        AND post_status = 'publish'
        ORDER BY post_title ASC";
			
			return $this->wpdb->get_results( $query );
		}
		
		/**
		 * Get all pricing tables
		 **/
		function get_all_pricing_tables() {
			$args = array(
				'post_type' => 'wproto_pricing_table',
				'post_status' => 'publish',
				'posts_per_page' => -1
			);
			
			return new WP_Query( $args );
		}
		
		/**
		 * Return custom fields in a nice way
		 **/
		function get_post_custom( $post_id ) {
			$custom_fields = get_post_custom( $post_id );
			$return = array();
			if( count( $custom_fields ) > 0 ) {
				foreach( $custom_fields as $k=>$v ) {
					if( $k[0] != '_' )
						$return[$k] = $v[0];
				}
			}
			return (object)$return;
		}
                
	}