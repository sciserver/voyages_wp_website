<?php

	class wpl_galaxy_wp_shortcodes_controller extends wpl_galaxy_wp_base_controller {
		
		function __construct() {
			
			add_shortcode( 'wproto_divider', array( $this, 'divider' ) );
			add_shortcode( 'wproto_highlight', array( $this, 'highlight' ) );
			add_shortcode( 'wproto_button', array( $this, 'button' ) );
			add_shortcode( 'wproto_tooltip', array( $this, 'tooltip' ) );
			add_shortcode( 'wproto_call_to_action', array( $this, 'call_to_action' ) );
			add_shortcode( 'wproto_map', array( $this, 'map' ) );
			add_shortcode( 'wproto_progress', array( $this, 'progress' ) );
			add_shortcode( 'wproto_contact_form', array( $this, 'contact_form' ) );
			
			// tabs
			add_shortcode( 'wproto_tabs', array( $this, 'tabs' ) );
			// toggles
			add_shortcode( 'wproto_toggles', array( $this, 'toggles' ) );
			
			// replace default gallery shortcode
			remove_shortcode( 'gallery' );
			add_shortcode( 'gallery', array( $this, 'gallery') );
			
			add_shortcode( 'wproto_photoalbums', array( $this, 'photoalbums') );
			
			add_shortcode( 'wproto_portfolio', array( $this, 'get_custom_posts_shortcode') );
			add_shortcode( 'wproto_posts', array( $this, 'get_custom_posts_shortcode') );
			add_shortcode( 'wproto_catalog', array( $this, 'get_custom_posts_shortcode') );
			add_shortcode( 'wproto_team', array( $this, 'get_custom_posts_shortcode') );
			add_shortcode( 'wproto_benefits', array( $this, 'get_custom_posts_shortcode') );
			add_shortcode( 'wproto_testimonials', array( $this, 'get_custom_posts_shortcode') );
			add_shortcode( 'wproto_clients_partners', array( $this, 'get_custom_posts_shortcode') );
			
			add_shortcode( 'wproto_pricing_tables', array( $this, 'pricing_tables') );
			
			// send a contact form action
			add_action( 'wp_ajax_wproto_send_contact_form', array( $this, 'send_contact_form' ));
			add_action( 'wp_ajax_nopriv_wproto_send_contact_form', array( $this, 'send_contact_form' ));
			
		}
		
		/**
		 * Divider shortcode
		 **/
		function divider( $params ) {
			
			$style = isset( $params['style'] ) ? $params['style'] : 'narrow';
			
			$return = '<hr class="wproto_divider style-' . $style . '">';
			
			return $return;
			
		}
		
		/**
		 * Highlight the text
		 **/
 		function highlight( $params ) {
			$style = isset( $params['color'] ) ? $params['color'] : 'narrow';
			$content = isset( $params['content'] ) ? $params['content'] : '';
			
			$return = '<span style="color: ' . $style . ' !important;">' . $content . '</span>';
			
			return $return;
 		}
 		
 		/**
 		 * Button shortcode
 		 **/
		function button( $params ) {
			
			$at_new_window = isset( $params['new_window'] ) && $params['new_window'] == 'yes' ? ' target="_blank"' : '';
			$href = isset( $params['link'] ) ? $params['link'] : '';
			
			if( !isset( $params['size'] ) || $params['size'] == '' ) {
				$size = 'small';
			} else {
				$size = $params['size'];
			}
			
			if( !isset( $params['color'] ) || $params['color'] == '' ) {
				$color = 'default';
			} else {
				$color = $params['color'];
			}
			
			$icon = isset( $params['icon'] ) ? '<i class="' . $params['icon'] . '"></i> ' : '';
			
			$iconic = $icon <> '' ? 'iconic' : '';
			
			$text = isset( $params['text'] ) ? $params['text'] : '';
			
			$return = '<a href="' . $href . '" class="button ' . $iconic . ' size-' . $size . ' color-' . $color . '"' . $at_new_window . '>' . $icon . $text . '</a>';
			
			return $return;
		}
		
		/**
		 * Tooltip shortcode
		 **/
 		function tooltip( $params ) {
 			
 			$title = isset( $params['title'] ) ? $params['title'] : '';
 			$content = isset( $params['content'] ) ? $params['content'] : '';
 			
 			$gravity = '';
 			
 			$return = '<span class="wproto_tooltip" data-tip-gravity="s" title="' . esc_html( $title ) . '">' . $content . '</span>';
 			
 			return $return;
 		}
 		
 		/**
 		 * Call to action shortcode
 		 **/
		function call_to_action( $params ) {
			
 			ob_start();
 				$this->view->load_partial( 'shortcodes/call_to_action', $params );
 			return ob_get_clean();
			
		}
		
		/**
		 * Show google map by address
		 **/
 		function map( $params ) {
 			$return = '';
 			
 			if( isset( $params['address'] ) && trim( $params['address'] ) <> '' ) {
 				
 				$title = isset( $params['title'] ) ? $params['title'] : '';
 				
 				ob_start();
 					$this->view->load_partial( 'shortcodes/map', $params );
 				return ob_get_clean();
 				
 			}
 			
 			return $return;
 		}
 		
 		/**
 		 * Progress bars shortcode
 		 **/
 		function progress( $params ) {
 			
			$data = array();
			
			$data['titles'] = isset( $params['titles'] ) ? explode( '|', $params['titles'] ) : array();
			$data['values'] = isset( $params['values'] ) ? explode( '|', $params['values'] ) : array();
			
			if( (is_array( $data['titles'] ) && count( $data['titles'] ) > 0) && (is_array( $data['values'] ) && count( $data['values'] ) > 0) ) {
				
 				ob_start();
 				$this->view->load_partial( 'shortcodes/progress', $data );
 				return ob_get_clean();
				
			}
			
 		}
 		
 		/**
 		 * Contact form shortcode
 		 **/
		function contact_form( $params ) {		
			
			if( isset( $params['form_id'] ) && get_transient( 'wprcf_' . md5( $params['form_id'] ) ) == 'ok' ) {
				delete_transient( 'wprcf_' . md5( $params['form_id'] ) );
				$params['sent'] = 'ok';
			}
			
 			ob_start();
 				$this->view->load_partial( 'shortcodes/contact_form', $params );
 			return ob_get_clean();
		}
		
		/**
		 * Gallery shortcode
		 **/
 		function gallery( $params ) {
			global $post;
			
			$data['cols'] = isset( $params['columns'] ) ? absint( $params['columns'] ) : 0;
			$data['cols'] = $data['cols'] == 0 ? 3 : $data['cols'];
			
			$ids_str = isset( $params['ids'] ) ? $params['ids'] : '';
			
			$ids = explode( ',', $ids_str );
			
			$args = array(
				'post_type' => 'attachment',
				'numberposts' => -1,
				'post_status' => null
			); 
				
			if( is_array( $ids ) && count( $ids ) > 0 ) {
				$args['include'] = $ids;
			} else {
				$args['post_parent'] = $post->ID;
			}
			
			$data['items'] = get_posts( $args );
			
			if( count( $data['items'] ) > 0 && is_array( $data['items'] ) ) {
				
				ob_start();
				$this->view->load_partial( 'shortcodes/gallery', $data );
				return ob_get_clean();
				
				
			}
 			
 		}
 		
 		/**
 		 * Tabs
 		 **/
 		 
		function tabs( $atts, $content ) {
			
			$tabs = array_filter( explode( '[/tab]', $content ) );
			
			$inside = '';
			
			if( is_array( $tabs ) && count( $tabs ) > 0 ) {
				foreach( $tabs as $tab ) {

					preg_match( '/\[tab title=("|\')(.*)("|\')\](.*)$/s', $tab, $matches );

					$title = isset( $matches[2] ) ? $matches[2] : '';
					$c = isset( $matches[4] ) ? $matches[4] : '';
					
					if( $title <> '' && $c <> '' )
						$inside .= '<div class="tab"><h2 class="title">' . $title . '</h2><div class="tab-content">' . apply_filters( 'the_content', $c ) . '</div></div>';
				}
			}
			
			return '<div class="tabs-holder"><div class="liquid-slider content-slider" id="tabs-' . uniqid() .  '">' . $inside . '</div></div>';
  
		}
	
		/**
		 * Toggles shortcode
		 **/
		function toggles( $atts, $content ) {
			
			$toggles = array_filter( explode( '[/toggle]', $content ) );
			
			$inside = '';
			
			if( is_array( $toggles ) && count( $toggles ) > 0 ) {
				foreach( $toggles as $toggle ) {

					preg_match( '/\[toggle title=("|\')(.*)("|\')\](.*)$/s', $toggle, $matches );

					$title = isset( $matches[2] ) ? $matches[2] : '';
					$c = isset( $matches[4] ) ? $matches[4] : '';
					
					if( $title <> '' && $c <> '' )
						$inside .= '<div class="toggle"><h4><i class="icon-plus"></i>' . $title . '</h4><div class="toggle-content">' . apply_filters( 'the_content', $c ) . '</div></div>';
				}
			}
			
			return '<div class="toggles">' . $inside . '</div>';
			
		}
		
		/**
		 * Photo Albums
		 **/
		function photoalbums( $params ) {
			
			$data = array();
			$data['id'] = isset( $params['album'] ) ? absint( $params['album'] ) : 0;
			$data['title'] = isset( $params['title'] ) ? $params['title'] : 0;
			$data['limit'] = isset( $params['limit'] ) ? $params['limit'] : 0;
			
			$this->controller->front->track_post_views( $data['id'] );
			
			ob_start();
			$this->view->load_partial( 'shortcodes/photoalbums', $data );
			return ob_get_clean();
		}
		
		/**
		 * Custom posts shortcode
		 **/
		function get_custom_posts_shortcode( $params, $content, $tag ) {
			
			$view = str_replace( 'wproto_', '', $tag );
			
			$data = array();
			$data['title'] = isset( $params['title'] ) ? $params['title'] : '';
			$data['cols'] = isset( $params['cols'] ) ? absint( $params['cols'] ) : 3;
			
			$type = isset( $params['show'] ) ? $params['show'] : '';
			$limit = isset( $params['limit'] ) ? absint( $params['limit'] ) : 3;
			$orderby = isset( $params['orderby'] ) ? $params['orderby'] : 'date';
			$sort = isset( $params['sort'] ) ? $params['sort'] : 'DESC';
			$category = isset( $params['category'] ) ? $params['category'] : 0;
			
			switch( $tag ) {
				case 'wproto_portfolio':
					$data['posts'] = $this->model->post->get( $type, $limit, $category, $orderby, $sort, 'wproto_portfolio', 'wproto_portfolio_category' );
				break;
				case 'wproto_catalog':
					$data['posts'] = $this->model->post->get( $type, $limit, $category, $orderby, $sort, 'wproto_catalog', 'wproto_catalog_category' );
				break;
				case 'wproto_team':
					$data['posts'] = $this->model->post->get( $type, $limit, $category, $orderby, $sort, 'wproto_team', 'wproto_team_category' );
				break;
				case 'wproto_benefits':
					$data['posts'] = $this->model->post->get( $type, $limit, $category, $orderby, $sort, 'wproto_benefits', 'wproto_benefits_category' );
				break;
				case 'wproto_testimonials':
					$data['posts'] = $this->model->post->get( $type, $limit, $category, $orderby, $sort, 'wproto_testimonials', 'wproto_testimonials_category' );
				break;
				case 'wproto_clients_partners':
					$data['posts'] = $this->model->post->get( $type, $limit, $category, $orderby, $sort, 'wproto_partners', 'wproto_partners_category' );
				break;
				default:
					$data['posts'] = $this->model->post->get( $type, $limit, $category, $orderby, $sort, 'post', 'category', false, false, true );
				break;
			}

			ob_start();
			$this->view->load_partial( 'shortcodes/' . $view, $data );
			$return = ob_get_clean();
			//wp_reset_query();
			return $return;
			
		}
		
		/**
		 * Pricing tables shortcode
		 **/
		function pricing_tables( $params ) {
			
			$data = array();
			$table_id = isset( $params['id'] ) ? absint( $params['id'] ) : 0;
			
			if( $table_id > 0 ) {
				
				$data['pricing_table'] = get_post_meta( $table_id, 'pricing_table', true );
				$data['style'] = get_post_meta( $table_id, 'table_style', true );
				$data['title'] = get_the_title( $table_id );
				$data['subtitle'] = get_post_meta( $table_id, 'subtitle', true );
				
				ob_start();
				$this->view->load_partial( 'shortcodes/pricing_tables', $data );
				return ob_get_clean();
			}
			
		}
		
		/**
		 * Send contact form
		 **/
		function send_contact_form() {
			
			$form_id = isset( $_POST['form_id'] ) ? trim( strip_tags( $_POST['form_id'] ) ) : '';
			$post_id = isset( $_POST['post_id'] ) ? absint( $_POST['post_id'] ) : 0;
			$name = isset( $_POST['name'] ) ? trim( strip_tags( $_POST['name'] ) ) : '';
			$email = isset( $_POST['email'] ) ? trim( strip_tags( $_POST['email'] ) ) : '';
			$subject = isset( $_POST['subject'] ) ? trim( strip_tags( $_POST['subject'] ) ) : '';
			$text = isset( $_POST['text'] ) ? trim( strip_tags( $_POST['text'] ) ) : '';
			$captcha_id = isset( $_POST['captcha_id'] ) ? trim( strip_tags( $_POST['captcha_id'] ) ) : '';
			$captcha_value = isset( $_POST['captcha_value'] ) ? absint( $_POST['captcha_value'] ) : '';
			$from_widget = isset( $_POST['from_widget'] ) ? trim( strip_tags( $_POST['from_widget'] ) ) : '';
			
			$to = isset( $_POST['to'] ) && is_email( $_POST['to'] ) ? $_POST['to'] : get_bloginfo('admin_email');
			$cookie_name = isset( $_COOKIE['wproto_captcha_session_id'] ) ? $_COOKIE['wproto_captcha_session_id'] : '';
			
			$response = array( 'status' => 'ok' );
			
			if( $name == '' ) {
				$response['error_text'] = __('Enter your name', 'wproto');
			}
			
			if( !is_email( $email ) ) {
				$response['error_text'] = __('Enter valid email', 'wproto');
			}
			
			if( $text == '' ) {
				$response['error_text'] = __('Enter your message', 'wproto');
			}
			
			if( $form_id == '' ) {
				$response['error_text'] = __('Wrong form ID', 'wproto');
			}
			
			if( $post_id <= 0 ) {
				$response['error_text'] = __('Wrong post ID', 'wproto');
			}
			
			if( ! isset( $response['error_text'] ) ) {
				
				/** Check for captcha, primary form **/
				if( $form_id == 'primary-contact-form' ) {
					
					$page_settings = $this->model->post->get_post_custom( $post_id );
					
					$to =  isset( $page_settings->wproto_tpl_contact_email_to ) && is_email( $page_settings->wproto_tpl_contact_email_to ) ? $page_settings->wproto_tpl_contact_email_to : get_bloginfo('admin_email');
					
					if( ! isset( $page_settings->wproto_tpl_contact_display_captcha ) || $page_settings->wproto_tpl_contact_display_captcha != 'no' ) {
						
						if( ! $this->controller->captcha->validate_captcha_answer( $captcha_value, $captcha_id ) ) {
							$response['error_text'] = __('Wrong captcha value', 'wproto');
						} 
						
					}
					
				} elseif( $from_widget == '' ) {
					/** check for captcha, post shortcode **/
					$post = get_post( $post_id );
					$content = isset( $post->post_content ) ? $post->post_content : '';
					
					if( has_shortcode( $content, 'wproto_contact_form' ) ) {
						
						$shortcode = wpl_galaxy_wp_utils::get_shortcode( 'wproto_contact_form', $content );
						$captcha_enabled = wpl_galaxy_wp_utils::get_shortcode_attribute( $shortcode, 'captcha' );
						$shortcode_id = wpl_galaxy_wp_utils::get_shortcode_attribute( $shortcode, 'form_id' );
						
						if( ($shortcode_id == $form_id && $captcha_enabled == 'yes') && ! $this->controller->captcha->validate_captcha_answer( $captcha_value, $captcha_id ) ) {
							$response['error_text'] = __('Wrong captcha value', 'wproto');
						}
						
					}
					
				} elseif( $from_widget <> '' ) {
					/** check for captcha, widgets **/
					
					$widget_num = str_replace( 'wproto-contact-form-widget-', '', $from_widget );
					
					$widget_options = get_option( 'widget_wproto-contact-form-widget' );
					
					if( isset( $widget_options[ $widget_num ] ) && is_array( $widget_options[ $widget_num ] ) ) {
						
						if( ! isset( $widget_options[ $widget_num ]['enable_captcha'] ) || $widget_options[ $widget_num ]['enable_captcha'] != 'no' ) {
							
							if( ! $this->controller->captcha->validate_captcha_answer( $captcha_value, $captcha_id ) ) {
								$response['error_text'] = __('Wrong captcha value', 'wproto');
							} 
							
						}
						
					} else {
						$response['error_text'] = __('Cannot read widget settings', 'wproto');
					}
					
					
				}
				
				/** send the message **/
				if( ! isset( $response['error_text'] ) ) {
					delete_transient( 'wprc_' . $cookie_name . '_' . $captcha_id );
					wp_mail( $to, $subject, $text, 'From: ' . $name . ' <' . $email . '>' . "\r\n" );
				} else {
					$response['status'] = 'error';
				}
				
			}
			
			die( json_encode( $response ) );
		}
	
	}