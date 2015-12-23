<?php

class wpl_galaxy_wp_utils {
	
	/**
	 * Check for Retina display
	 **/
	public static function is_retina() {
		global $wpl_galaxy_wp;
		$retina_support_enabled = $wpl_galaxy_wp->get_option( 'retina_support', 'general' );
		return WPROTO_IS_RETINA && $retina_support_enabled == 'yes';
	}
	
	/**
	 * Check for Retina display
	 **/
	public static function is_retina_enabled() {
		global $wpl_galaxy_wp;
		$retina_support_enabled = $wpl_galaxy_wp->get_option( 'retina_support', 'general' );
		return $retina_support_enabled == 'yes';
	}
	
	/**
	 * Clear old transients
	 **/
	public static function purge_transients( $older_than = '7 days', $safemode = true ) {
		global $wpdb;

		$older_than_time = strtotime('-' . $older_than);
		if ($older_than_time > time() || $older_than_time < 1) {
			return false;
		}

		$transients = $wpdb->get_col(
			$wpdb->prepare( "
					SELECT REPLACE(option_name, '_transient_timeout_', '') AS transient_name 
					FROM {$wpdb->options} 
					WHERE option_name LIKE '\_transient\_timeout\__%%'
						AND option_value < %s
			", $older_than_time)
		);
		if ($safemode) {
			foreach($transients as $transient) {
				get_transient($transient);
			}
		} else {
			$options_names = array();
			foreach($transients as $transient) {
				$options_names[] = '_transient_' . $transient;
				$options_names[] = '_transient_timeout_' . $transient;
			}
			if ($options_names) {
				$options_names = array_map(array($wpdb, 'escape'), $options_names);
				$options_names = "'". implode("','", $options_names) ."'";

				$result = $wpdb->query( "DELETE FROM {$wpdb->options} WHERE option_name IN ({$options_names})" );
				if (!$result) {
					return false;
				}
			}
		}

		return $transients;
	}
	
	/**
	 * Get google fonts
	 **/
	public static function get_google_fonts() {
		
		$google_fonts = array();

		$fonts = self::grab_google_fonts();

		if( count( $fonts->items ) > 0 ) {
			
			foreach( $fonts->items as $item ) {
				$google_fonts[ $item->family ] = $item->family;
			}
			
		}
		
		return $google_fonts;
		
	}
	
	/**
	 * Grab fonts from google
	 **/
	public static function grab_google_fonts( $force = false ) {
		global $wpl_galaxy_wp;
		
		$fonts = unserialize( get_option( 'wproto_google_fonts_list' ) );
		
		$google_api_key = $wpl_galaxy_wp->get_option( 'google_api_key' );
		
		if( $google_api_key == NULL ) {
			return $fonts;
		}

		if( gettype( $fonts ) != 'object' || $force == true ) {
			$response = @file_get_contents( 'https://www.googleapis.com/webfonts/v1/webfonts?key=' . $google_api_key );
			
			try {
				$json = json_decode( $response );
			} catch ( Exception $ex ) {
				$json = null;
				return false;
			}

			update_option( 'wproto_google_fonts_list', serialize( $json ));
			
			return $json;
			
		} else {
			return gettype( $fonts ) == 'object' ? $fonts : '';
		}
		
	}
	
	/**
	 * Is layerSlider Active
	 **/
	public static function isset_layerslider() {
		return shortcode_exists( 'layerslider' );
	}
	
	/**
	 * Is WooCommerce Active
	 **/
	public static function isset_woocommerce() {
		return class_exists( 'woocommerce' );
	}
	
	/**
	 * Get all CSS classes from FontAwesome Library
 	 **/
	public static function get_icons() {
		global $wpl_galaxy_wp;
		
		// get results from cache
		$icons = get_transient( 'wproto_font_icons' );
			
		if( $icons == false ) {
			
			$icons = array();
			
			// get Font Awesome icons
			$pattern = '/\.(fa-(?:\w+(?:-)?)+):before\s+{\s*content:\s*"(.+)";\s+}/';
			$subject = file_get_contents( WPROTO_THEME_DIR . '/css/libs/font-awesome/css/font-awesome.css');

			preg_match_all( $pattern, $subject, $matches, PREG_SET_ORDER);

			foreach( $matches as $match){
				$icons['font-awesome'][ $match[1]] = $match[2];
			}
			
			// get IcoMoon icons
			$ico_moon_enabled = $wpl_galaxy_wp->get_option('icomoon_enabled');
			if( $ico_moon_enabled == 'yes' ) {
				$pattern = '/\.(icon-(?:\w+(?:-)?)+):before\s+{\s*content:\s*"(.+)";\s+}/';
				$subject = file_get_contents( WPROTO_THEME_DIR . '/css/libs/icomoon/style.css');

				preg_match_all( $pattern, $subject, $matches, PREG_SET_ORDER);

				foreach( $matches as $match){
					$icons['icomoon'][ $match[1]] = $match[2];
				}
			}
				
			// cache results
			set_transient( 'wproto_font_icons', $icons, 60*60*12 );
				
		}

		return $icons;
	}
	
	/**
	 * Plural form function
	 * @param int
	 * @param string
	 * @param string
	 * @param string
	 * @return string
	**/
	public static function plural_form( $n, $form1, $form2, $form5) {
		$n = abs($n) % 100;
		$n1 = $n % 10;
		if ($n > 10 && $n < 20) return $form5;
		if ($n1 > 1 && $n1 < 5) return $form2;
		if ($n1 == 1) return $form1;
		return $form5;
	}
	
	/**
	 * Make post sticky
	 **/
	public static function make_post_sticky( $post_id, $make_sticky = true ) {
		$sticky_posts = get_option( 'sticky_posts' );
			
		if( $make_sticky ) {
			// make post sticky
			$sticky_posts[] = $post_id;
			update_option( 'sticky_posts', $sticky_posts );
			
		} else {
			// make post default
			$new_array = array();
			foreach( $sticky_posts as $k=>$v ) {
				if( $v == $post_id ) continue;
				$new_array[] = $v;
			}
			update_option( 'sticky_posts', $new_array );
		}
	}
	
	/**
	 * Is shortcode exists
	 * @param string
	 * @param object
	 * @return mixed
	 **/
	public static function get_shortcode( $shortcode, $text ) {
		$pattern = get_shortcode_regex();
		preg_match_all( '/'. $pattern . '/s', $text, $matches);

		if( is_array( $matches) && array_key_exists( 3, $matches ) && array_key_exists( 2, $matches )) {
			if( is_array( $matches[2])) {

				if( $shortcode == $matches[2][0]) {
					return trim( $matches[3][0]);
				}

			} else {
                    
				if( in_array( $shortcode, $matches[2])) {
					return trim( $matches[3][0]);
				}
                                                            
			}
		} else {
			return false;
		}
           
	}
	
	/**
	 * Get shortcode attribute
	 * @param string
	 * @param string
	 * @return mixed
	 **/
	public static function get_shortcode_attribute( $text, $attr){
		$keysvals = array();
		preg_match_all('/([\w_]+)=(["\'])([\w\W][^"\']+)\2/i', $text, $matches);
		for ($i = 0; $i < count( $matches[0]); $i++) {
			$keysvals[ $matches[1][$i]] = $matches[3][$i];
		}
		return isset( $keysvals[ $attr]) ? $keysvals[ $attr] : false;
	}
	
	/**
	 * Break apart images
	 **/
	public static function break_apart_images( $images ) {
		// extract attributes from each image and place in $images array
		$image_attr = array();
		foreach ( $images as $img ) {
			preg_match_all( "#(\w+)=['\"]{1}([^'\"]*)#", $img, $matches2 );
			$tempArray = array();
			foreach( $matches2[1] as $key => $val )
				$tempArray[ $val ] = $matches2[2][ $key ];

				$image_attr[] = $tempArray;
			}

		return $image_attr;
	}
	
	/**
	 * Get all post custom fields in nice array
	 **/
	public static function get_post_custom( $post_id ) {
		
		$return = array();
		
		$custom_fields = get_post_custom( $post_id );
		
		if( is_array( $custom_fields ) && count( $custom_fields ) > 0 ) {
			foreach( $custom_fields as $key => $value ) {
				$return[$key] = is_array( $value ) && count( $value ) > 1 ? $value : $value[0];
			}
		}
		
		return $return;
		
	}
	
	/**
	 * Returns all child nav_menu_items under a specific parent
	 *
	 * @param   int       the parent nav_menu_item ID
	 * @param   array     nav_menu_items
	 * @param   bool      gives all children or direct children only
	 * @return  array     returns filtered array of nav_menu_items
	 */
	public static function get_nav_menu_item_children( $parent_id, $nav_menu_items, $depth = true ) {

		$nav_menu_item_list = array();

		foreach ( (array) $nav_menu_items as $nav_menu_item ) {

			if ( $nav_menu_item->menu_item_parent == $parent_id ) {
				$nav_menu_item_list[] = $nav_menu_item;
					if ( $depth ) {
						if ( $children = self::get_nav_menu_item_children( $nav_menu_item->ID, $nav_menu_items ) )
							$nav_menu_item_list = array_merge( $nav_menu_item_list, $children );
					}

			}

		}

    return $nav_menu_item_list;
	}
	
	/**
	 * Print submenu three
	 **/
	public static function get_submenu_tree( $items, $parent = 0, $level = 0 ) {

    $ret = '';
    foreach( $items as $index => $item ){
     if( $item->menu_item_parent == $parent ) {
     		if( $item->dont_display_as_link == 'yes' ) {
     			$ret .= '<li class="lvl-' . $level . '">' . $item->title;
     		} else {
     			$ret .= '<li class="lvl-' . $level . '"><a href="' . $item->url . '">' . $item->title . '</a>';
     		}
				
				if( $item->type == 'taxonomy' ) {
					$_tax_meta = get_option( "taxonomy_" . $item->object_id );
					$_tax_featured = isset( $_tax_meta['category_featured'] ) ? $_tax_meta['category_featured'] : '';
					$_tax_new = isset( $_tax_meta['category_new'] ) ? $_tax_meta['category_new'] : '';
					$_tax_img = isset( $_tax_meta['category_image_id'] ) ? $_tax_meta['category_image_id'] : '';
					
					if( ! $_tax_img && self::isset_woocommerce() ) {
						$_tax_img = get_woocommerce_term_meta( $item->object_id, 'thumbnail_id', true );
					}
					
					if( $_tax_new == 'yes' ) {
						$ret .= '<span class="new-item">' . __('new', 'wproto') . '</span>';
					}
					
					if( $_tax_featured == 'yes' && absint( $_tax_img ) > 0 && $level == 0 ) {
						
						$image = wp_get_attachment_image_src( $_tax_img, 'wproto-mega-menu-thumb' );
						$image_2x = wp_get_attachment_image_src( $_tax_img, 'wproto-mega-menu-thumb-2x' );
						
						$img_src = self::is_retina() ? $image[0] : $image_2x[0];
						
						$ret .= '<div class="featured-cat-img"><a href="' . $item->url . '"><img src="' . $img_src . '" width="290" height="80" alt="" /></a></div>';

						$cat_description = $item->description <> '' ? $item->description : category_description( $item->object_id );

						if( $cat_description <> '' ) {
							$ret .= '<div class="featured-cat-desc">' . strip_tags( $cat_description ) . '</div>';
						}
						
						$ret .= '<a class="more" href="' . $item->url . '">' . __('Learn more', 'wproto') . '</a>';
						
					}
					
					if( $_tax_featured == 'yes' && $level == 1 ) {
						$ret .= '<span class="featured-item"><i class="fa fa-thumbs-up"></i></span>';
					}
					
				}
				
				$ret .= self::get_submenu_tree( $items, $item->ID , $level + 1 );
				
				$ret .= '</li>';
			}
		}
		
		$class = $level == 0 ? 'ul-item' : '';		
		return $ret <> '' ? '<ul class="' . $class . '">' . $ret . '</ul>' : '';
	}
	
	/**
	 * Get current URL string
	 **/
	public static function get_current_url(){
		return (!empty($_SERVER['HTTPS'])) ? "https://" . $_SERVER['SERVER_NAME'] . $_SERVER['REQUEST_URI'] : "http://" . $_SERVER['SERVER_NAME'] . $_SERVER['REQUEST_URI'];
	}
	
	/**
	 * Print custom excerpt
	 **/
	public static function custom_excerpt( $text, $length, $end = '[...]' ) {
		
		$text = strip_tags( $text );
		
		if( strlen( $text ) > $length ) {
			$text = substr( $text, 0, $length ) . $end;
		} 
		
		return $text;
		
	}
	
}