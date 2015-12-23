<?php
	/**
	 * Anything to do with templates
	 * and outputting client code
	 **/
  class wpl_galaxy_wp_view {
		/**
		 * Load view WITH header/footer
		 **/
		function load_page( $path = '', $data = array(), $header = 'header', $footer = 'footer' ) {
			// WARNING: Must not be optional for security reasons
			// $data = $this->esc_html( $data );

			//! TODO: Secure this, e.g. don't allow '..'
			$full_path = dirname( __FILE__ ) . '/' . $path . '.tpl';

			// Allow custom header path
			if ($header == 'header') {
				$header_path = get_stylesheet_directory() . '/header.php';
			} else {
				$header_path = $header . '.tpl';
			}

			// Allow custom footer path
			if ($footer == 'footer') {
				$footer_path = get_stylesheet_directory() . '/header.php';
			} else {
				$footer_path = $footer . '.tpl';
			}

			if ( file_exists( $full_path ) ) {
				if ( is_admin() ) {
					// WARNING: Link to an existing admin URL, such as /wp-admin/index.php?wproto_action=xxx, else trouble!
					
					// Load WP admin header, our file and footer, set empty menu to avoid errors
					global $menu;
					$menu = array();
					
					require_once ABSPATH . 'wp-admin/admin-header.php';
					require_once $full_path;
					require_once ABSPATH . 'wp-admin/admin-footer.php';
				} else {
					if( file_exists( $header_path ) ) {
						require_once $header_path;
					}
					
					require_once $full_path;
					
					if( file_exists( $footer_path ) ) {
						require_once $footer_path;
					}
				}
			} else {
				//! TODO: Introduce error emails throughout this plugin and a 404/500 page for the user
				throw new Exception( 'The view path ' . $full_path . ' can not be found.' );
			}

			exit;
		}

		/**
		 * Load view WITHOUT header/footer, in case you would like
		 * to nest templates, to loop through the same template, or
		 * to use a mixture of different templates in any other way.
		 **/
		function load_partial( $path = '', $data = array() ) {

			//! TODO: Secure this, e.g. don't allow '..'
			$full_path = dirname( __FILE__ ) . '/' . $path . '.tpl';

			if ( file_exists( $full_path ) ) {
				require $full_path;
			} else {
				throw new Exception( 'The view path ' . $full_path . ' can not be found.' );
			}
		}

		/**
		 * Load view WITHOUT header/footer for AJAX purposes. We will
		 * have to exit, or AJAX success code 1/0 will be outputted.
		 **/
		function load_ajax_partial( $path = '', $data = array() ) {
			$this->load_partial( $path, $data );
			exit;
		}

		/**
		 * HTML escape any PHP variables for security reasons
		 * before they reach the view template (this will
		 * recursively escape arrays and objects). If individual
		 * variables need different escaping, any of the "esc_"
		 * methods in this class can be called directly from the
		 * view template.
		 */
		function esc_html( $var ) {
			switch ( gettype( $var ) ){
				case 'object':
					foreach ( $var as $prop => $v ){
						$var->$prop = $this->esc_html( $v );
					}
					break;
				case 'array' :
					foreach ( $var as $k => &$v ){
						$var[$k] = $this->esc_html( $v );
					}
					break;
				default:
					$var = htmlentities( $var, ENT_QUOTES, 'UTF-8', false );
			}

			return $var;
		}

		/**
		 * You can call $this->esc_js($string) in your templates,
		 * should you NOT want the default HTML escaping, but javascript
		 * escaping instead
		 **/
		function esc_js( $html_encoded_string = '' ) {
			$string = html_entity_decode( $html_encoded_string, ENT_QUOTES, 'UTF-8' );
			return esc_js( $string );
		}

		/**
		 * You can call $this->esc_url($string) in your templates,
		 * should you NOT want the default HTML escaping, but URL
		 * escaping instead
		 **/
		function esc_url( $html_encoded_string = '' ) {
			$string = html_entity_decode( $html_encoded_string, ENT_QUOTES, 'UTF-8' );
			return esc_url( $string );
		}

		/**
		 * You can call $this->esc_email($string) in your templates,
		 * should you NOT want the default HTML escaping, but email
		 * address obfuscating instead, so that bots can not harvest
		 * the email address from your web page to send spam to
		 **/
		function esc_email( $html_encoded_string = '' ) {
			$string = html_entity_decode( $html_encoded_string, ENT_QUOTES, 'UTF-8' );
			$string = sanitize_email( $string );
			return antispambot( $string );
		}

		/**
		 * You can call $this->show_pure_html($string) in your templates,
		 * should you NOT want the default HTML escaping, but the HTML
		 * echoed as such instead. Only dangerous HTML tags and attributes
		 * are stripped from the output here.
		 **/
		function show_pure_html( $html_encoded_string = '' ) {
			global $allowedposttags;
			$string = html_entity_decode( $html_encoded_string, ENT_QUOTES, 'UTF-8' );
			return wp_kses( $string, $allowedposttags);
		}
  }