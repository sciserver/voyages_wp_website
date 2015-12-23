<?php
/**
 * Video custom post controller
 **/
class wpl_galaxy_wp_video_controller extends wpl_galaxy_wp_base_controller {

	function __construct() {
		// Security: Admin only
		if ( is_admin() ) {
			// add info box
			add_action( 'admin_footer', array( $this, 'add_info_box'));
			// Metaboxes
			add_action( 'admin_menu', array( $this, 'manage_meta_boxes' ) );
			// Save custom data
			add_action( 'save_post', array( $this, 'save_custom_meta' ) );
			// Grab the video
			add_action( 'wp_ajax_wproto_ajax_grab_video', array( $this, 'ajax_grab_video' ) );
			// Admin screen filters
			add_filter( 'manage_edit-wproto_video_columns', array( $this, 'manage_admin_columns' ) );
			add_action( 'manage_wproto_video_posts_custom_column', array( $this, 'get_admin_columns' ), 10, 2);
			add_filter( 'manage_edit-wproto_video_sortable_columns', array( $this, 'manage_sortable_columns' ));
			add_filter( 'request', array( $this, 'make_sortable_request' ) );
			// Post filters
			add_action( 'restrict_manage_posts', array( $this, 'add_posts_admin_filters' ) );
			add_filter( 'parse_query', array( $this, 'add_posts_admin_query_filters' ) );
		}
	}
	
	/**
	 * Add info box
	 **/
	function add_info_box() {
		$screen = get_current_screen();
		$hide_infobox = $this->get_option( 'hide_infobox', 'general' );
		// Add - edit sidebars screen
		if( $hide_infobox != 'yes' && ( isset( $screen->base ) && $screen->base == 'edit' ) && $_GET['post_type'] == 'wproto_video' && $_GET['page'] != 'wproto-video-layout-editor' ):
			$this->view->load_partial( 'infobox/infobox', array('title' => __( 'Video', 'wproto'), 'content' => '<p>' . __( 'Use this post type to grab videos from YouTube and Vimeo services.', 'wproto') . '</p>' ) );
		endif; 
	}
	
	/**
	 * Manage meta boxes
	 **/
	function manage_meta_boxes() {
		remove_meta_box( 'postcustom', 'wproto_video', 'normal');
		remove_meta_box( 'slugdiv', 'wproto_video', 'normal');
		
		add_meta_box(
			'wproto_meta_featured'
			,__( 'Featured video', 'wproto' )
			,array( $this, 'render_meta_box_featured' )
			,'wproto_video'
			,'side'
			,'high'
		);
		
		add_meta_box(
			'wproto_meta_likes'
			,__( 'Video Rating', 'wproto' )
			,array( $this, 'render_meta_box_likes' )
			,'wproto_video'
			,'side'
			,'high'
		);
		
		add_meta_box(
			'wproto_meta_video'
			,__( 'Video Options', 'wproto' )
			,array( $this, 'render_meta_box_video' )
			,'wproto_video'
			,'normal'
			,'high'
		);
		
	}
	
	/**
	 * Render "Featured" metabox
	 **/
	function render_meta_box_featured() {
		global $post;
		$data = array();
		$data['featured'] = get_post_meta( $post->ID, 'featured', true );
		
		$this->view->load_partial( 'metaboxes/post_featured', $data );
	}
	
	/**
	 * Render "Likes" metabox
	 **/
	function render_meta_box_likes() {
		global $post;
		$data = array();
		$data['likes'] = get_post_meta( $post->ID, 'wproto_likes', true );
		$data['views'] = get_post_meta( $post->ID, 'wproto_views', true );
		
		$likes_enabled = $this->get_option( 'likes_on_posts', 'general' );
		if( $likes_enabled == 'no' ) {
			$data['hide_likes'] = true;
		}
		
		$this->view->load_partial( 'metaboxes/post_likes', $data );
	}
	
	/**
	 * Render "Video options" options metabox
	 **/
	function render_meta_box_video() {
		global $post;
		$data = array();
		$data['player_code'] = get_post_meta( $post->ID, 'player_code', true );
		$data['thumbnail_small'] = get_post_meta( $post->ID, 'thumbnail_small', true );
		$data['thumbnail_medium'] = get_post_meta( $post->ID, 'thumbnail_medium', true );
		$data['thumbnail_big'] = get_post_meta( $post->ID, 'thumbnail_big', true );
		$data['title'] = get_post_meta( $post->ID, 'title', true );
		$data['type'] = get_post_meta( $post->ID, 'type', true );
		$data['video_width'] = get_post_meta( $post->ID, 'video_width', true );
		$data['video_height'] = get_post_meta( $post->ID, 'video_height', true );
		
		$this->view->load_partial( 'metaboxes/video', $data );
	}
	
	/**
	 * Save custom fields
	 **/
	function save_custom_meta( $post_id ) {
		
		$post_type = get_post_type( $post_id );
		
		if( $post_type == 'wproto_video' ) {
			
			// Stop WP from clearing custom fields on autosave
			if ( defined( 'DOING_AUTOSAVE') && DOING_AUTOSAVE )
				return;

			// Prevent quick edit from clearing custom fields
			if ( defined( 'DOING_AJAX') && DOING_AJAX )
				return;

			if( empty( $_POST) )
				return;
			
			$allowed_tags = wp_kses_allowed_html( 'post' );
			
			update_post_meta( $post_id, "featured", isset( $_POST["featured"] ) ? wp_kses( $_POST["featured"], $allowed_tags ) : '' );
				
			update_post_meta( $post_id, "player_code", isset( $_POST["player_code"] ) ? wp_kses( $_POST["player_code"], $allowed_tags ) : '' );
			update_post_meta( $post_id, "thumbnail_small", isset( $_POST["thumbnail_small"] ) ? wp_kses( $_POST["thumbnail_small"], $allowed_tags ) : '' );
			update_post_meta( $post_id, "thumbnail_medium", isset( $_POST["thumbnail_medium"] ) ? wp_kses( $_POST["thumbnail_medium"], $allowed_tags ) : '' );
			update_post_meta( $post_id, "thumbnail_big", isset( $_POST["thumbnail_big"] ) ? wp_kses( $_POST["thumbnail_big"], $allowed_tags ) : '' );
			update_post_meta( $post_id, "title", isset( $_POST["title"] ) ? wp_kses( $_POST["title"], $allowed_tags ) : '' );
			update_post_meta( $post_id, "type", isset( $_POST["type"] ) ? wp_kses( $_POST["type"], $allowed_tags ) : '' );
			
			update_post_meta( $post_id, "video_width", isset( $_POST["video_width"] ) ? wp_kses( $_POST["video_width"], $allowed_tags ) : '' );
			update_post_meta( $post_id, "video_height", isset( $_POST["video_height"] ) ? wp_kses( $_POST["video_height"], $allowed_tags ) : '' );
			
			update_post_meta( $post_id, "wproto_likes", isset( $_POST["wproto_likes"] ) ? absint( $_POST["wproto_likes"] ) : 0 );
			update_post_meta( $post_id, "wproto_views", isset( $_POST["wproto_views"] ) ? absint( $_POST["wproto_views"] ) : 0 );
			
		}
		
	}
	
	/**
	 * Grab the video
	 **/
	function ajax_grab_video() {
		
		$result = array();
     
		// Vimeo link
		if( preg_match( "/^((http)|(https)):\/\/[www]*\.*vimeo\.com\/([0-9]+)/i", $_POST['link'], $matches) ) {
			$video_id = end( $matches);
                
			$url = "http://vimeo.com/api/v2/video/$video_id.json";
                
			$request = new WP_Http;
			$result = $request->request( $url );
                
			if( isset($result['body']) ) {
				$vimeo = json_decode( $result['body']);

				$data = array(
					'type' => 'vimeo',                    
					'title' => $vimeo[0]->title,
					'player_code' => 'http://player.vimeo.com/video/' . $video_id,
					'thumbnail_big' => $vimeo[0]->thumbnail_large,
					'thumbnail_small' => $vimeo[0]->thumbnail_small,
					'thumbnail_medium' => $vimeo[0]->thumbnail_medium                                               
				);

				include WPROTO_ENGINE_DIR . "/view/metaboxes/video_content.tpl";

			} else {
				die( __('Server access error', 'wproto') . curl_error( $curl));
			}
                
		} else {
		
			// Youtube link
		
			$u = parse_url($_POST['link']);
    	parse_str($u['query'], $queryVars);
    	$youtube_id = '';

    	if ( $u['query'] && $queryVars['v'] ) {
				$youtube_id = $queryVars['v'];
    	} else if ($u['fragment']) {
    		$youtube_id = basename($u['fragment']);
    	} else if ($u['path']) {
    		$youtube_id = basename($u['path']);
    	}
		
			if( $youtube_id <> '' ) {
				$video_id = $youtube_id;
				$url = "http://gdata.youtube.com/feeds/api/videos/" . $video_id;

				$request = new WP_Http;
				$result = $request->request( $url );
                
				if( isset( $result['body'] ) ) {
					$xml = new SimpleXMLElement( $result['body'] );
					$media = $xml->children( 'media', true);
                    
					$thumbnail_big = $media->group->thumbnail[0]->attributes();
					$thumbnail_small = $media->group->thumbnail[1]->attributes();
					$player_link = $media->group->player[0]->attributes();
                    
					$data = array(
						'type' => 'youtube',                    
						'title' => $xml->title,
						'player_code' => 'http://www.youtube.com/embed/' . $video_id,
						'thumbnail_big' => $thumbnail_big['url'],
						'thumbnail_small' => $thumbnail_small['url'],
						'thumbnail_medium' => $thumbnail_big['url']                                                   
					);
                    
					include WPROTO_ENGINE_DIR . "/view/metaboxes/video_content.tpl";
                    
				} else {
					die( __( 'Server access error', 'wproto') . curl_error( $curl));
				}
                
			}
			
		}
		
		die;
	}
	
	/**
	 * Manage admin columns
	 **/
	function manage_admin_columns( $columns ) {
	
		$likes_on_posts = $this->get_option( 'likes_on_posts', 'general' );
	
		$new_columns['cb'] = '<input type="checkbox" />';
		$new_columns['image'] = __( 'Thumbnail', 'wproto');
		$new_columns['title'] = __( 'Title', 'wproto' );
		$new_columns['video_type'] = __( 'Type', 'wproto');
		
		if( $likes_on_posts == 'yes' ) $new_columns['rating'] = __( 'Likes', 'wproto');
		
		$new_columns['views'] = __( 'Views', 'wproto');
		$new_columns['is_featured'] = __( 'Featured', 'wproto');
		$new_columns['category'] = __( 'Categories', 'wproto');
		$new_columns['tag'] = __( 'Tags', 'wproto');
		$new_columns['date'] = __( 'Date', 'wproto' );
		
		return $new_columns;
	}
	
	/**
	 * Get the data for admin columns
	 **/
	function get_admin_columns( $column_name, $id ) {
		
		switch ( $column_name ) {
			case 'image':
			
				$thumb = wpl_galaxy_wp_utils::is_retina() ? 'wproto-admin-thumb-2x' : 'wproto-admin-thumb';
				$img = wpl_galaxy_wp_utils::is_retina() ? 'noimage-2x.gif' : 'noimage.gif';
				$video_thumb = get_post_meta( $id, 'thumbnail_small', true );
				echo '<a href="' . admin_url( 'post.php?post=' . $id . '&action=edit' ) . '">';
				if ( has_post_thumbnail() ):
					echo '<div class="wproto-admin-thumb wproto-video-thumb">';
					
					$url_arr = wp_get_attachment_image_src( get_post_thumbnail_id( $id ), $thumb );
					
					echo '<img width="100" height="75" src="' . $url_arr[0] . '" alt="" />';
					echo '</div>';
				elseif( $video_thumb <> '' ):
					echo '<div class="wproto-admin-thumb wproto-video-thumb">';
					
					echo '<img src="' . $video_thumb . '" width="100" height="75" alt="" />';
					echo '</div>';
				else: 
					echo '<div class="wproto-admin-thumb wproto-video-thumb">';
					echo '<img width="100" height="75" src="' . WPROTO_THEME_URL . '/images/admin/' . $img . '" alt="" />';
					echo '</div>';
				endif;
				echo '</a>';
				
			break;
			case 'is_featured': 
			
				$this->view->load_partial( 'admin_filters/is_featured', array( 'post_id' => $id, 'is_featured' => get_post_meta( $id, 'featured', true ) ) );
				
			break;
			case 'category':
				$terms = get_the_terms( $id, 'wproto_video_category' );
				$this->view->load_partial( 'admin_filters/list_categories', array( 'terms' => $terms ) );
			break;
			case 'tag':
				$terms = get_the_terms( $id, 'wproto_video_tag' );
				$this->view->load_partial( 'admin_filters/list_categories', array( 'terms' => $terms ) );
			break;
			case 'video_type':
				$type = get_post_meta( $id, 'type', true );
				
				if( $type == 'youtube' ):
					echo 'YouTube';
				elseif( $type == 'vimeo' ):
					echo 'Vimeo';
				else:
				
				endif;
				
			break;
			case 'rating':
			
				$likes = get_post_meta( $id, 'wproto_likes', true );
				$like_img = WPROTO_IS_RETINA ? 'like@2x.png' : 'like.png';
				echo absint( $likes ) . ' <img width="16" height="16" src="' . WPROTO_THEME_URL . '/images/admin/' . $like_img . '" alt="" />';
			
			break;
			case 'views':
				$views = get_post_meta( $id, 'wproto_views', true );
				$view_img = WPROTO_IS_RETINA ? 'views@2x.png' : 'views.png';
				echo absint( $views ) . ' <img width="16" height="16" src="' . WPROTO_THEME_URL . '/images/admin/' . $view_img . '" alt="" />';
			break;
		}
	}
	
	/**
	 * Setup sortable columns
	 **/
	function manage_sortable_columns( $columns ) {
		$columns['rating'] = 'rating';
		$columns['views'] = 'views';
  	return $columns;
	}
	
	/**
	 * Sortable by custom column, change request
	 **/
	function make_sortable_request( $vars ) {
		if ( isset( $vars['orderby'] ) && 'rating' == $vars['orderby'] ) {
			$vars = array_merge( $vars, array(
				'meta_key' => 'wproto_likes',
				'orderby' => 'meta_value_num'
			));
		}
		if ( isset( $vars['orderby'] ) && 'views' == $vars['orderby'] ) {
			$vars = array_merge( $vars, array(
				'meta_key' => 'wproto_views',
				'orderby' => 'meta_value_num'
			));
		}
    return $vars;
	}
	
	/**
	 * Filter query by category at admin screen
	 **/
	function add_posts_admin_filters() {
		global $post, $wp_query;
		if ( get_post_type( $post ) == 'wproto_video' ) {
			$data = array( 'typenow' => 'wproto_video' );
			$data['wp_query'] = $wp_query;
			$data['taxonomy'] = 'wproto_video_category';
			$this->view->load_partial( 'admin_filters/category_filter', $data );
			$this->view->load_partial( 'admin_filters/posts_filter', $data );
			$this->view->load_partial( 'admin_filters/videos_filter', $data );
			$this->view->load_partial( 'admin_filters/ajax_loader' );
		}
	}
	
	/**
	 * Query filter by category at admin screen
	 **/
	function add_posts_admin_query_filters( $query ) {
		
		global $post;
			
		if ( get_post_type( $post ) == 'wproto_video' ) {
			
			if( isset( $_GET['featured'] ) && $_GET['featured'] == 'yes' ) {
				$query->set( 'meta_query', array(
					array(
						'key' => 'featured',
						'value' => 'yes'
					)
				));
			}
			
			if( isset( $_GET['video_type'] ) ) {
				$query->set( 'meta_query', array(
					array(
						'key' => 'type',
						'value' => $_GET['video_type']
					)
				));
			}
			
			if( isset( $_GET['filter_by_category'] ) && $_GET['filter_by_category'] > 0 ) {
				$query->set( 'tax_query', array(
					array(
						'taxonomy' => 'wproto_video_category',
						'terms' => $_GET['filter_by_category'] 
					)
				));
			}
				
		}
		
	}

}