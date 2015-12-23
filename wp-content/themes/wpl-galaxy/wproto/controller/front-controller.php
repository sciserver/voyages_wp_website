<?php
/**
 * Front-end controller
 **/
class wpl_galaxy_wp_front_controller extends wpl_galaxy_wp_base_controller {
	
	function __construct() {
		
		// Post views
		add_action( 'wp_head', array( $this, 'track_post_views' ) );
		
		// make valid HTML output
		add_filter( 'get_search_form', array( $this, 'custom_search' ) );
		add_filter( 'wp_list_categories', array( $this, 'remove_rel_attr') );
		add_filter( 'get_the_category_list', array( $this, 'remove_rel_attr'));
		add_filter( 'get_archives_link', array( $this, 'theme_get_archives_link' ) );
		add_filter( 'wp_tag_cloud', array( $this, 'highlight_tags' ) );
		add_filter( 'embed_oembed_html', array( $this, 'custom_embed_html' ), 10, 3 );
		add_filter( 'img_caption_shortcode', array( $this, 'custom_caption_html' ), 10, 3 );
		
		// add images to RSS feed
		add_filter( 'the_excerpt_rss', array( $this, 'add_featured_image_to_feed' ), 1000, 1);
		add_filter( 'the_content_feed', array( $this, 'add_featured_image_to_feed' ), 1000, 1);
		
		//add_filter( 'excerpt_more', array( $this, 'excerpt_more' ) );
		
		// Hide admin bar from non-admins if this required by theme settings
		add_action( 'after_setup_theme',  array( $this, 'remove_admin_bar' ) );
		
		// "Like" post
		add_action( 'wp_ajax_wproto_ajax_like', array( $this, 'ajax_like' ) );
		add_action( 'wp_ajax_nopriv_wproto_ajax_like', array( $this, 'ajax_like' ) );
		
		add_action( 'wp_enqueue_scripts', array( $this, 'remove_styles' ), 99 );
		add_action( 'wp_print_scripts', array( $this, 'remove_scripts' ), 100 );
		
		// Replace content images with retina
		add_filter( 'the_content', array( $this, 'filter_retina_images' ) );
		add_filter( 'the_content', array( $this, 'filter_post_format' ) );
		add_filter( 'the_content', array( $this, 'add_grid_wrapper' ) );
		
		// search custom posts
		add_filter( 'pre_get_posts', array( $this, 'filter_search' ));
		
		add_action( 'wp_enqueue_scripts', array( $this, 'add_scripts' ) );
		add_action( 'wp_enqueue_scripts', array( $this, 'add_styles' ) );
		
		add_filter( 'body_class', array( $this, 'filter_body_classes' ) );
		add_filter( 'post_class', array( $this, 'add_post_classes' ));
		
		// check for maintenance mode
		add_action( 'template_redirect', array( $this, 'template_redirect' ) );
		
		// AJAX Pagination
		add_action( 'wp_ajax_wproto_ajax_pagination', array( $this, 'ajax_pagination' ) );
		add_action( 'wp_ajax_nopriv_wproto_ajax_pagination', array( $this, 'ajax_pagination' ) );
		
	}
	
	/**
	 * Track post views
	 **/
	function track_post_views( $post_id ) {
		
		if ( !is_single() ) return;
    if ( empty ( $post_id) ) {
			global $post;
			$post_id = $post->ID;   
		}
		$meta_IP = get_post_meta( $post_id, "wproto_views_IP" );
		$views_IP = isset( $meta_IP[0] ) && is_array( $meta_IP[0] ) ? $meta_IP[0] : array();
		
		$ip = $_SERVER['REMOTE_ADDR'];
		
		if( ! in_array( $ip, array_keys( $views_IP)) ) {
			$views_IP[$ip] = time();
			$meta_count = absint( get_post_meta( $post_id, "wproto_views", true ) );
			$meta_count = $meta_count + 1;
			update_post_meta( $post_id, "wproto_views", $meta_count );
			update_post_meta( $post_id, "wproto_views_IP", $views_IP );
		}
	}
	
	/**
	 * Do a lot of job to make valid default HTML output
	 **/
		
	function custom_caption_html( $current_html, $attr, $content ) {
		extract(shortcode_atts(array(
			'id'    => '',
			'align' => 'alignnone',
			'width' => '',
			'caption' => ''
		), $attr));
		if ( 1 > (int)$width || empty( $caption ) )
			return $content;

		if ( $id ) $id = 'id="' . esc_attr( $id ) . '" ';

			$html = '<div ' . $id . 'class="wp-caption ' . esc_attr( $align ) . '" style="width: ' . ( 10 + (int) $width ) . 'px">' . do_shortcode( $content ) . '<p class="wp-caption-text">' . $caption . '</p></div>';
			return preg_replace( '/(rel="attachment wp\-att\-[0-9]+")/i', '', $html );
	}
		
	function custom_embed_html( $html, $url, $attr ) {
			
		return str_replace( '</embed>', '', $html );
			
	}
		
	function highlight_tags( $cloud ) {
		global $wpdb, $wp_query;
		$tags = single_tag_title('', false);
		$tags_array = explode(" + ", $tags);
		foreach ($tags_array as $tag_name) {
			$tag_id = isset( $wp_query->queried_object->term_id ) ? $wp_query->queried_object->term_id : 0;
				
			if( $tag_id ) {
				$cloud = str_replace( "tag-link-$tag_id", "current-term tag-link-$tag_id", $cloud);
			}
				
		}
		return $cloud;
	}
		
	function theme_get_archives_link( $link_html ) {
		global $wp_query;
			
		$current = '';
		if( isset( $wp_query->query['m'] ) ) {
			$current = $wp_query->query['m'];
		}
		if( isset( $wp_query->query['year'] ) && $wp_query->query['monthnum'] ) {
			$current = $wp_query->query['year'] . '\/+' . $wp_query->query['monthnum'];
		}
			
		if ( $current <> '' && preg_match( '/' . $current . '/i', $link_html ) )
			$link_html = preg_replace( '/<li>/i', '<li class="current">', $link_html );
			
		return $link_html;
	}
		
	function remove_rel_attr( $text ) {
		$text = str_replace( 'rel="category tag"', '', $text );
		$text = str_replace( 'rel="category"', '', $text );
		$text = str_replace( 'rel="tag"', '', $text );
		return $text;
	}
		
	function custom_search() {
		ob_start();
		include WPROTO_THEME_DIR . '/part-searchform.php';
		return ob_get_clean();
	}
	
	/**
	 * Add featured images to RSS feed
	 **/
	function add_featured_image_to_feed( $content ) {
		global $post, $wpl_galaxy_wp;
		
		$rss_display_thumbs = $wpl_galaxy_wp->get_option( 'rss_display_thumbs' );
		
		if( $rss_display_thumbs == 'yes' ) {
			
			if ( has_post_thumbnail( $post->ID ) ){
				$thumb_name = wpl_galaxy_wp_utils::is_retina_enabled() ? 'wproto-rss-image' : 'wproto-rss-image-2x';
				$img_src = wp_get_attachment_image_src( get_post_thumbnail_id( $post->ID ), $thumb_name );
				$content = '<!-- POST THUMBNAIL --><img src="' . $img_src[0] . '" width="540" height="340" alt="" />' . $content;
			}
			
		}
		return $content;
	}
	
	/**
	 * Change default excerpt end
	 **/
	function excerpt_more() {
		return ' ...';
	}
	
	/**
	 * Hide admin bar from non-admins
	 **/
	function remove_admin_bar() {
		
		$hide_bar_from_non_admins = $this->get_option('hide_adminbar_for_non_admins');
		
		if ( $hide_bar_from_non_admins == 'yes' && !current_user_can('administrator') && !is_admin()) {
			show_admin_bar( false );
		}
	}
	
	/**
	 * "Like" post
	 **/
	function ajax_like() {
		$nonce = $_POST['nonce'];
		
    if ( !wp_verify_nonce( $nonce, 'wproto-engine-ajax-nonce' ) ) {
    	die( __( 'This request not allowed', 'wproto' ) );
    }

		$ip = $_SERVER['REMOTE_ADDR'];
		
		if( isset( $_POST['post_like'])) {
			
			$post_id = absint( $_POST['post_id'] );
			$meta_IP = get_post_meta( $post_id, "wproto_voted_IP" );

			$voted_IP = isset( $meta_IP[0] ) && is_array( $meta_IP[0] ) ? $meta_IP[0] : array();
		
			$meta_count = absint( get_post_meta( $post_id, "wproto_likes", true ) );

			if( ! $this->is_already_voted( $post_id, 'post' )) {
				$voted_IP[$ip] = time();

				$meta_count = $meta_count + 1;

				update_post_meta( $post_id, "wproto_voted_IP", $voted_IP );
				update_post_meta( $post_id, "wproto_likes", $meta_count );

			} 
			
			echo $meta_count;
			
		}
		
		if( isset( $_POST['comment_like'])) {
			
			$comment_id = absint( $_POST['post_id'] );
			$meta_IP = get_comment_meta( $comment_id, "wproto_voted_IP" );

			$voted_IP = @$meta_IP[0];
			
			if( !is_array( $voted_IP )) $voted_IP = array();
		
			$meta_count = absint( get_comment_meta( $comment_id, "wproto_likes", true ) );

			if( ! $this->is_already_voted( $comment_id, 'comment' )) {
				$voted_IP[$ip] = time();

				$meta_count = $meta_count + 1;

				update_comment_meta( $comment_id, "wproto_voted_IP", $voted_IP );
				update_comment_meta( $comment_id, "wproto_likes", $meta_count );

			} 
			
			echo $meta_count;
			
		}
	
		die;
		
	}
	
	/**
	 * Check if user already voted
	 **/
	public function is_already_voted( $id, $type = 'post' ) {
		if( $type == 'comment' ) {
			$meta_IP = get_comment_meta( $id, "wproto_voted_IP" );
		} else {
			$meta_IP = get_post_meta( $id, "wproto_voted_IP" );
		}
		
		$voted_IP = isset( $meta_IP[0] ) ? $meta_IP[0] : array();
		
		if( !is_array( $voted_IP )) $voted_IP = array();
		
		$ip = $_SERVER['REMOTE_ADDR'];
	
		return in_array( $ip, array_keys( $voted_IP));
	}
	
	/**
	 * Remove some styles
	 **/
	function remove_styles() {
		wp_dequeue_style( 'woocommerce_frontend_styles' );
		wp_dequeue_style( 'woocommerce_fancybox_styles' );
		wp_dequeue_style( 'woocommerce_chosen_styles' );
		wp_dequeue_style( 'woocommerce_prettyPhoto_css' );
		wp_dequeue_style( 'woocommerce_frontend_styles_smallscreen' );
		//wp_deregister_style( 'bbp-default' );
	}
	
	/**
	 * Remove WooScripts
	 **/
	function remove_scripts() {
		wp_dequeue_script( 'prettyPhoto' );
		wp_dequeue_script( 'prettyPhoto-init' );
		wp_dequeue_script( 'wc-chosen' );
		//wp_dequeue_script( 'wc-checkout' );
		//wp_dequeue_script( 'wc-add-to-cart' );
		//wp_dequeue_script( 'wc-add-to-cart-variation' );
		//wp_dequeue_script( 'wc-single-product' );
	}
	
	/**
	 * Filter retina images
	 **/
	function filter_retina_images( $content ) {
		
		$new_content = $content;
		
		if( wpl_galaxy_wp_utils::is_retina() ) {

			preg_match_all( "#<img(.*?)\/?>#", $content, $matches );
			
			$defaults = array( 'size-medium', 'size-large', 'size-thumbnail' );
			
			$new_image_tags = array();

			foreach ( wpl_galaxy_wp_utils::break_apart_images( $matches[1] ) as $key => $image ) {

				$classes = explode( ' ', $image['class'] );

				foreach ( $classes as $class_key => $value ) {

					if ( in_array( $value, $defaults ) ) {
						$classes[] .= $classes[ $class_key ] . '-2x';
						$twox_class = substr( $classes[ $class_key ] . '-2x', 5 );
					}

					if ( strstr( $value, 'wp-image-' ) ) {
						$id_classes = explode( '-', $value );
						$image_id = $id_classes[2];
					}
				
				}

				if ( ! empty( $image_id ) && ! empty( $twox_class ) ) {

					$new_src = wp_get_attachment_image_src( $image_id, $twox_class );

					$new_image_tags[ $key ] = array( $matches[0][ $key ] );

					$new_image_tags[ $key ][] = '<img src="' . $new_src[0] . '" width="' . $image['width'] . '" height="' . $image['height'] . '" class="' . implode( ' ', $classes ) . '" />';

				}
			}

			//Replace old image with new
			foreach ( $new_image_tags as $new_img )
				$new_content = str_replace( $new_img[0], $new_img[1], $new_content );
		}

    return $new_content;
	}
	
	/**
	 * Filter post status
	 **/
	function filter_post_format( $content ) {
		global $post;
		
		if( isset( $post->ID ) ) {
			$post_format = get_post_format( $post->ID );
			if( in_array( $post_format, array('quote', 'status') ) ) {
				$content = '<blockquote><p>' . strip_tags( $content ) . '</p></blockquote>';
			}
		}
		
		return $content;
		
	}
	
	/**
	 * Add grid wrapper if visual
	 **/
	function add_grid_wrapper( $content ) {
		
		if( preg_match('/<div class=\"unit/s', $content, $matches) ) {
			return '<div class="grid">' . $content . '</div>';
		}
		
		return $content;
		
	}
	
	/**
	 * Filter search custom posts
	 **/
	function filter_search( $query ) {
		if ( $query->is_search ) {
			$query->set( 'post_type', array( 'post', 'page', 'wproto_video', 'wproto_photoalbums', 'wproto_catalog', 'wproto_portfolio', 'product' ));
			//$query->set( 'post__not_in', get_option('sticky_posts'));
		};
    return $query;
	}
	
	/**
	 * Template redirect
	 **/
	function template_redirect() {
		global $wpl_galaxy_wp;
		
		$is_maintenance = $wpl_galaxy_wp->get_option('maintenance_enabled');
		
		$is_admin = current_user_can('activate_plugins');
		
		if( $is_maintenance == 'yes' && !$is_admin ) {
			include( WPROTO_THEME_DIR . '/page-maintenance.php' );
			exit();
		}

		$is_coming_soon = $wpl_galaxy_wp->get_option('coming_soon_enabled');
		
		if( $is_coming_soon == 'yes' && !$is_admin ) {
			include( WPROTO_THEME_DIR . '/page-coming-soon.php' );
			exit();
		}
		
	}
	
	/**
	 * Ajax pagination
	 **/
	function ajax_pagination() {
		global $wpl_galaxy_wp;
		
		$allowed_tags = wp_kses_allowed_html( 'post' );
		
		$max_pages = isset( $_POST['max_pages'] ) ? absint( $_POST['max_pages'] ) : 0;
		$current_page = isset( $_POST['current_page'] ) ? absint( $_POST['current_page'] ) : 0;
		$next_page = isset( $_POST['next_page'] ) ? absint( $_POST['next_page'] ) : 0;
		$post_type = isset( $_POST['post_type'] ) ? wp_kses( $_POST['post_type'], $allowed_tags ) : '';
		$taxonomy_name = isset( $_POST['taxonomy_name'] ) ? wp_kses( $_POST['taxonomy_name'], $allowed_tags ) : '';
		$taxonomy_term = isset( $_POST['taxonomy_term'] ) ? wp_kses( $_POST['taxonomy_term'], $allowed_tags ) : '';
		$loop_template = isset( $_POST['loop_template'] ) ? wp_kses( $_POST['loop_template'], $allowed_tags ) : '';
		$search_string = isset( $_POST['search_string'] ) ? wp_kses( $_POST['search_string'], $allowed_tags ) : '';
		$posts_per_page = isset( $_POST['posts_per_page'] ) ? absint( $_POST['posts_per_page'] ) : get_option('posts_per_page');
		$display_cats_type = isset( $_POST['display_type'] ) ? wp_kses( $_POST['display_type'], $allowed_tags ) : 'all';
		$current_author = isset( $_POST['current_author'] ) ? absint( $_POST['current_author'] ) : '';
		
		$taxonomy_terms = explode( ',', $taxonomy_term );

		$response = array();

		if( $loop_template <> '' ) {

			$args = array(
				'post_type' => $post_type,
				'posts_per_page' => $posts_per_page,
				'paged' => $next_page,
				'post_status' => 'publish'
			);
			
			if( is_numeric( $current_author ) ) {
				$args['author'] = $current_author;
			}
			
			if( $search_string <> '' ) {
				$args['s'] = $search_string;
			}

			if( $taxonomy_name <> '' && $taxonomy_term <> '' ) {
				
				if( $display_cats_type == 'all' || $display_cats_type == 'only' ) {
					
					$args['tax_query'] = array( array(
						'taxonomy' => $taxonomy_name,
						'field' => 'id', 
						'terms' => $taxonomy_terms
					));
					
				} 
				
				if( $display_cats_type == 'all_except' ) {
					
					$args['tax_query'] = array( array(
						'taxonomy' => $taxonomy_name,
						'field' => 'id', 
						'terms' => $taxonomy_terms,
						'operator' => 'NOT IN'
					));
					
				}
				

			}

			query_posts( $args );
			
			global $wpl_galaxy_wp_ajax_pagination;
			$wpl_galaxy_wp_ajax_pagination = true;
			
			ob_start();
			get_template_part( 'layouts/' . $loop_template );
			
			$response['html'] = ob_get_clean();
			wp_reset_postdata();
			
			$response['next_page'] = $next_page + 1;
			$response['current_page'] = $next_page;
			
			if( $response['next_page'] > $max_pages ) {
				$response['hide_link'] = 'yes';
			}
			
		}
		
		die( json_encode( $response ) );
	}
	
	/**
	 * Add scripts to the front
	 **/
	function add_scripts() {
		global $wpl_galaxy_wp, $wp_query;
		
		wp_enqueue_script( 'jquery' );
		
		if ( is_singular() && get_option( 'thread_comments' ) )
			wp_enqueue_script( 'comment-reply' );
			
		wp_enqueue_script( 'nprogress', WPROTO_THEME_URL . '/js/libs/nprogress.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
		wp_enqueue_script( 'jquery-tipsy', WPROTO_THEME_URL . '/js/libs/jquery.tipsy.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
		
		if( $wpl_galaxy_wp->get_option('display_gotop') != 'no' ) {
			wp_enqueue_script( 'jquery-totop', WPROTO_THEME_URL . '/js/libs/jquery.ui.totop.min.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
		}
		
		wp_enqueue_script( 'jquery-fs-scroller', WPROTO_THEME_URL . '/js/libs/jquery.fs.scroller.min.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
		wp_enqueue_script( 'jquery-fs-selecter', WPROTO_THEME_URL . '/js/libs/jquery.fs.selecter.min.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
		wp_enqueue_script( 'jquery-magnific-popup', WPROTO_THEME_URL . '/js/libs/jquery.magnific-popup.min.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
		wp_enqueue_script( 'jquery-easing', WPROTO_THEME_URL . '/js/libs/jquery.easing.1.3.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
		wp_enqueue_script( 'jquery-liquid-slider', WPROTO_THEME_URL . '/js/libs/jquery.liquid-slider.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
		wp_enqueue_script( 'jquery-touch-swipe', WPROTO_THEME_URL . '/js/libs/jquery.touchSwipe.min.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
		wp_enqueue_script( 'jquery-waitforimages', WPROTO_THEME_URL . '/js/libs/jquery.waitforimages.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
		wp_enqueue_script( 'jquery-icheck', WPROTO_THEME_URL . '/js/libs/jquery.icheck.min.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
		wp_enqueue_script( 'jquery-bxslider', WPROTO_THEME_URL . '/js/libs/jquery.bxslider.min.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
		wp_enqueue_script( 'jquery-owl-carousel', WPROTO_THEME_URL . '/js/libs/owl.carousel.min.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
		wp_enqueue_script( 'jquery-appear', WPROTO_THEME_URL . '/js/libs/jquery.appear.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
		wp_enqueue_script( 'wproto-masonry', WPROTO_THEME_URL . '/js/libs/masonry.pkgd.min.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
		
		wp_enqueue_script( 'jquery-swiper', WPROTO_THEME_URL . '/js/libs/idangerous.swiper-2.4.min.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
		
		wp_enqueue_script( 'jquery-vex', WPROTO_THEME_URL . '/js/libs/vex.combined.min.js', false, $this->settings['res_cache_time'], true );
		wp_enqueue_script( 'jquery-fitvids', WPROTO_THEME_URL . '/js/libs/jquery.fitvids.js', false, $this->settings['res_cache_time'], true );
		//wp_enqueue_script( 'jquery-history', WPROTO_THEME_URL . '/js/libs/jquery.history.js', false, $this->settings['res_cache_time'], true );
		
		if( defined( 'WPROTO_DEMO_STAND' ) && WPROTO_DEMO_STAND ) {
			wp_enqueue_script( 'jquery-cookie', WPROTO_THEME_URL . '/js/libs/jquery.cookie.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
			wp_enqueue_script( 'jquery-custom-scrollbar', WPROTO_THEME_URL . '/js/libs/jquery.mCustomScrollbar.min.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
			wp_enqueue_script( 'less-js', WPROTO_THEME_URL . '/js/libs/less-1.5.1.min.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
			wp_enqueue_script( 'wproto-style-switcher', WPROTO_THEME_URL . '/js/styleSwitcher.js', array( 'jquery' ), $this->settings['res_cache_time'], true );	
		}
		
		$is_coming_soon = $wpl_galaxy_wp->get_option('coming_soon_enabled');
		if( $is_coming_soon == 'yes' ) {
			wp_enqueue_script( 'wproto-countdown', WPROTO_THEME_URL . '/js/libs/countdown.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
			wp_enqueue_script( 'wproto-coming-soon', WPROTO_THEME_URL . '/js/coming-soon.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
		}
		
		$current_post_id = isset( $wp_query->post->ID ) ? $wp_query->post->ID : 0;
		
		$template_name = get_post_meta( $current_post_id, '_wp_page_template', true );
		
		if( $template_name == 'page-tpl-contacts.php' || $template_name == 'page-tpl-one-page.php' ) {
			
			wp_enqueue_script( 'google-map', 'https://maps.googleapis.com/maps/api/js?v=3.exp&amp;sensor=true' );
			
		}
		
		if( $template_name == 'page-tpl-one-page.php' ) {
			wp_enqueue_script( 'jquery-scrollto', WPROTO_THEME_URL . '/js/libs/jquery.scrollTo.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
			wp_enqueue_script( 'jquery-onepage-nav', WPROTO_THEME_URL . '/js/libs/jquery.nav.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
		}
		
		wp_register_script( 'wproto-front', WPROTO_THEME_URL . '/js/front.js', array( 'jquery' ), $this->settings['res_cache_time'], true );
		wp_enqueue_script( 'wproto-front' );
		
		$js_vars = array(
			'ajaxNonce' => wp_create_nonce( 'wproto-engine-ajax-nonce' ),
			'ajaxurl' => admin_url( 'admin-ajax.php' ),
			'homeUrl' => home_url(),
			'searchVar' => get_query_var('s'),
			'post_id' => $current_post_id,
			'strTypeCaptchaAnswer' => __('Please, enter captcha value', 'wproto'),
			'messageWasSent' => __('Your message has been sent. Thank you!', 'wproto'),
			'strAJAXError' => __( 'An AJAX error occurred when performing a query. Please contact support if the problem persists.', 'wproto' ),
			'strServerResponseError' => __( 'The script have received an invalid response from the server. Please contact support if the problem persists.', 'wproto' )
		);
		
		if( $template_name == 'page-tpl-contacts.php' ) {
			$contacts_settings = $this->model->post->get_post_custom( $current_post_id );
			$js_vars['contact_address'] = isset( $contacts_settings->wproto_tpl_contact_address ) ? trim( $contacts_settings->wproto_tpl_contact_address ) : '';
			$js_vars['contact_map_pointer'] = isset( $contacts_settings->wproto_tpl_contact_google_pointer_img ) ? trim( $contacts_settings->wproto_tpl_contact_google_pointer_img ) : WPROTO_THEME_URL . '/images/map_pointer.png';
			$js_vars['contact_map_logo'] = isset( $contacts_settings->wproto_tpl_contact_google_img ) ? trim( $contacts_settings->wproto_tpl_contact_google_img ) : '';
			
			if( isset( $contacts_settings->wproto_tpl_contact_success_text ) && $contacts_settings->wproto_tpl_contact_success_text <> '' ) {
				$js_vars['messageWasSent'] = $contacts_settings->wproto_tpl_contact_success_text;
			}
			
		}
		
		wp_localize_script( 'wproto-front', 'wprotoEngineVars', $js_vars );
		
		if( isset( $_GET['wproto_error'] ) ) {
			wp_register_script( 'wproto-error', WPROTO_THEME_URL . '/js/error.js', false, $this->settings['res_cache_time'], true );
			wp_enqueue_script( 'wproto-error' );
			$lang_vars = array('errorStr' => isset( $_GET['text'] ) ? strip_tags( trim( $_GET['text'] ) ) : __( 'An unexpected error occurred. Try again later or contact to our support.', 'wproto') );
			wp_localize_script( 'wproto-error', 'wprotoEngineErrorVars', $lang_vars );
		}
		
	}
	
	/**
	 * Add front CSS styles
	 **/
	function add_styles() {
		global $wpl_galaxy_wp;
		wp_enqueue_style( 'wproto-font-awesome', WPROTO_THEME_URL . '/css/libs/font-awesome/css/font-awesome.min.css?' . $this->settings['res_cache_time'] );
		wp_enqueue_style( 'wproto-liquid-slider', WPROTO_THEME_URL . '/css/libs/liquid-slider.css?' . $this->settings['res_cache_time'] );
		wp_enqueue_style( 'wproto-magnific-popup', WPROTO_THEME_URL . '/css/libs/magnific-popup.css?' . $this->settings['res_cache_time'] );
		wp_enqueue_style( 'wproto-owl-carousel', WPROTO_THEME_URL . '/css/libs/owl.carousel.css?' . $this->settings['res_cache_time'] );
		wp_enqueue_style( 'wproto-animate-css', WPROTO_THEME_URL . '/css/libs/animate.min.css?' . $this->settings['res_cache_time'] );
		
		$icomoon_enabled = $wpl_galaxy_wp->get_option('icomoon_enabled');
		if( $icomoon_enabled == 'yes' ) {
			wp_enqueue_style( 'wproto-icomoon', WPROTO_THEME_URL . '/css/libs/icomoon/style.css?' . $this->settings['res_cache_time'] );
		}
		
	}
	
	/**
	 * Add custom body classes
	 **/
	function filter_body_classes( $classes ) {
		global $post, $wpl_galaxy_wp;
		
		$is_admin = current_user_can('activate_plugins');
		
		/**
		 * Do not scroll header menu
		 **/
		$header_menu_scrolling = $wpl_galaxy_wp->get_option('header_menu_scrolling');
		
		if( $header_menu_scrolling == 'no' ) {
			$classes[] = 'no-scrolling-menu';
		}
		
		/**
		 * Maintenance
		 **/
		$is_maintenance = $wpl_galaxy_wp->get_option('maintenance_enabled');
		
		if( $is_maintenance == 'yes' && !$is_admin ) {
			$classes[] = 'template-maintenance';
		}
		
		/**
		 * Coming soon
		 **/
		$is_coming_soon = $wpl_galaxy_wp->get_option('coming_soon_enabled');
		
		if( $is_coming_soon == 'yes' && !$is_admin ) {
			$classes[] = 'coming-soon';
		}
		
		/**
		 * Custom header layout
		 **/
		$header_layout = get_theme_mod( 'wproto_header_layout', 'header-default' );
		if( $header_layout != 'header-default' ) {
			$classes[] = $header_layout;
		}
		
		/**
		 * Header top menu
		 **/
		$header_top_menu = get_theme_mod( 'wproto_header_top_menu', 'yes' );
		if( $header_top_menu == 'no' ) {
			$classes[] = 'no-top-menu';
		}
		
		/**
		 * Boxed layout
		 **/
		$boxed_layout = get_theme_mod( 'wproto_boxed_layout', 'no' );
		if( $boxed_layout == 'yes' ) {
			$classes[] = 'boxed-layout';
			
			// custom patterns
			$boxed_layout = get_theme_mod( 'wproto_boxed_pattern', '' );
			if( $boxed_layout <> '' ) {
				$classes[] = $boxed_layout;
			}
			
		}
		
		/**
		 * Widgetized footer
		 **/
		 
	 $widgetized_footer = 'yes';
		 
		if( is_page() || is_single() ) {
			
			$widgetized_footer = get_post_meta( $post->ID, 'wproto_widgetized_footer', true );
			
		}
		
		if( $widgetized_footer != 'no' ) {
			$classes[] = 'widgetized-footer';
		}
		
		/**
		 * Custom template classes
		 **/
		if( is_page() ) {
			
			$template_name = get_post_meta( $post->ID, '_wp_page_template', true );
			
			switch( $template_name ) {
				case( 'page-tpl-blog.php' ):
				case( 'page-tpl-portfolio.php' ):
				case( 'page-tpl-photoalbums.php' ):
				case( 'page-tpl-videos.php' ):
				case( 'page-tpl-catalog.php' ):

					$template_layout = get_post_meta( $post->ID, 'wproto_content_layout', true );
					
					if( $template_layout <> '' ) {
						$classes[] = 'template-' . str_replace( '_', '-', $template_layout );
					}
				
				break;
			}
			
		}
		
		if( is_author() ) {
			$classes[] = 'template-masonry';
			$classes = array_diff( $classes, array('archive'));
		}
		
		if( is_search() ) {
			$classes = array_diff( $classes, array('archive', 'author', 'template-masonry'));
		}
		
		/**
		 * Single catalog post
		 **/
	 	if( is_single('') && get_post_type() == 'wproto_catalog' ) {
	 		$classes[] = 'single-product';
	 	}
	 	
	 	/**
	 	 * WooCommerce
	 	 **/
		if( is_post_type_archive('product') || (function_exists('is_product_category') && is_product_category()) ) {
			$classes = array_diff( $classes, array('archive'));
			$classes[] = 'post-type-archive-product';
		}
		
		if( get_post_type() == 'product' ) {
			$classes = array_diff( $classes, array('single'));
		}

		return $classes;
		
	}
	
	/**
	 * Add custom classes to post
	 **/
	function add_post_classes( $classes ) {
		$classes[] = 'post';
		
		if ( has_post_thumbnail() || (get_post_format() == 'gallery' && get_post_gallery()) ) {
			$classes[] = 'with-feature-image';
			$classes[] = 'with-thumbnail';
		} elseif( get_post_type() == 'wproto_video' ) {
			$video_thumb = get_post_meta( get_the_ID(), 'thumbnail_big', true );
			if( $video_thumb <> '' ) {
				$classes[] = 'with-feature-image';
				$classes[] = 'with-thumbnail';
			} else {
				$classes[] = 'without-feature-image';
				$classes[] = 'without-thumbnail';
			}
		} else {
			$classes[] = 'without-feature-image';
			$classes[] = 'without-thumbnail';
		}
		return $classes;
	}
	
}