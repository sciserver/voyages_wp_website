<?php
/**
 * Custom templates controller
 **/
class wpl_galaxy_wp_template_controller extends wpl_galaxy_wp_base_controller {
	
	/**
	 * Below ALL add_action() and add_filter() hooks that
	 * get served by the methods of this controller
	 **/
	function __construct() {
		
		if( is_admin() ) {
			// Add JavaScript
			add_action( 'admin_enqueue_scripts', array( $this, 'add_scripts' ) );
			// Add custom meta boxes
			add_action( 'add_meta_boxes', array( $this, 'add_metaboxes' ) );
			// Save custom data
			add_action( 'save_post', array( $this, 'save_custom_meta' ) );
			// Search for posts
			add_action( 'wp_ajax_wproto_autocomplete_posts', array( $this, 'ajax_find_posts' ));
			
			// Section manipulations
			add_action( 'wp_ajax_wproto_ajax_delete_section', array( $this, 'ajax_delete_section' ));
			add_action( 'wp_ajax_wproto_ajax_add_edit_section', array( $this, 'ajax_add_edit_section' ));
			
		}
		
		// Custom theme templates init
		add_action( 'template_redirect',  array( $this, 'theme_template_init' ), 10, 1);
		
	}
	
	/**
	 * Add JS Scripts
	 **/
	function add_scripts() {
		wp_register_script( 'wproto-template-editor', WPROTO_THEME_URL . '/js/admin/template-editor.js?' . $this->settings['res_cache_time'] );
		wp_enqueue_script( 'wproto-template-editor', array( 'jquery' ) );
	}
	
	/**
	 * Add custom metaboxes
	 **/
	function add_metaboxes() {
		global $post;
		
		//$shop_page_id = get_option( 'woocommerce_shop_page_id' ); 
		//$front_page_id = get_option( 'page_on_front' );
		//$blog_page_id = get_option( 'page_for_posts');
		
		foreach( array('page', 'post', 'wproto_video', 'wproto_photoalbums', 'wproto_catalog', 'wproto_portfolio', 'product') as $post_type ) {
			// Page redirect metabox
			add_meta_box(
				'wproto_redirect'
				,__( 'Redirect Options', 'wproto' )
				,array( $this, 'render_redirect_metabox' )
				,$post_type
				,'side'
				,'low'
			);
			
			// Sidebar chooser
			add_meta_box(
				'wproto_sidebar_settings'
				,__( 'Sidebar options', 'wproto' )
				,array( $this, 'render_metabox_sidebar_options' )
				,$post_type
				,'normal'
				,'default'
			);
			
			// Slider settings
			if( wpl_galaxy_wp_utils::isset_layerslider() ) {
				add_meta_box(
					'wproto_slider_settings'
					,__( 'Slider settings', 'wproto' )
					,array( $this, 'render_metabox_slider_settings' )
					,'page'
					,'normal'
					,'default'
				);
			}
			
			// Post / page style settings
			add_meta_box(
				'wproto_post_appearance_settings'
				,__( 'Appearance options', 'wproto' )
				,array( $this, 'render_metabox_post_appearance' )
				,$post_type
				,'normal'
				,'default'
			);
				
		}
		
		// Contact page settings
		add_meta_box(
			'wproto_tpl_page_contacts'
			,__( 'Contact\'s page settings', 'wproto' )
			,array( $this, 'render_metabox_page_contacts' )
			,'page'
			,'normal'
			,'default'
		);
		
		// Layout settings metabox
		add_meta_box(
			'wproto_tpl_page_layout'
			,__( 'Layout settings', 'wproto' )
			,array( $this, 'render_metabox_page_layout' )
			,'page'
			,'normal'
			,'default'
		);
		
		// Media layout settings
		add_meta_box(
			'wproto_tpl_page_media_layout'
			,__( 'Media Layout settings', 'wproto' )
			,array( $this, 'render_metabox_page_media_layout' )
			,'page'
			,'normal'
			,'default'
		);
		
		// One page template settings
		add_meta_box(
			'wproto_tpl_one_page_template'
			,__( 'One page template settings', 'wproto' )
			,array( $this, 'render_metabox_one_page_template' )
			,'page'
			,'normal'
			,'default'
		);
		
		// Custom layout builder metabox
		add_meta_box(
			'wproto_tpl_page_custom_layout_builder'
			,__( 'Layout builder', 'wproto' )
			,array( $this, 'render_metabox_custom_layout_builder' )
			,'page'
			,'normal'
			,'default'
		);
		
	}
	
	/**
	 * Page redirect metabox
	 **/
	function render_redirect_metabox( $post ) {
		
		$data = array();
		
		$data = wpl_galaxy_wp_utils::get_post_custom( $post->ID );

		$data['post_type'] = get_post_type( $post->ID ) == 'page' ? __('page', 'wproto') : __('post', 'wproto');
		$data['post_id'] = $post->ID;
		
		$this->view->load_partial( 'metaboxes/page_redirect', $data );
	}
	
	/**
	 * Sidebar settings metabox
	 **/
	function render_metabox_sidebar_options( $post ) {
		global $wp_registered_sidebars;
		$data = array();
		
		$data = wpl_galaxy_wp_utils::get_post_custom( $post->ID );
		
		$data['registered_sidebars'] = $wp_registered_sidebars;
		$data['post_id'] = $post->ID;
		
		$this->view->load_partial( 'layout_editor/metabox_sidebar', $data );
	}
	
	/**
	 * Contacts page metabox
	 **/
	function render_metabox_page_contacts( $post ) {
		$data = wpl_galaxy_wp_utils::get_post_custom( $post->ID );
		$this->view->load_partial( 'layout_editor/metabox_tpl_contacts', $data );
	}
	
	/**
	 * Slider settings metabox
	 **/
	function render_metabox_slider_settings( $post ) {
		$data = wpl_galaxy_wp_utils::get_post_custom( $post->ID );
		
		$data['layerslider_items'] = $this->model->slider->get_layerslider_slideshows();

		$this->view->load_partial( 'layout_editor/metabox_slider', $data );
	}
	
	/**
	 * Appearance settings for post / page etc.
	 **/
	function render_metabox_post_appearance( $post ) {
		$data = wpl_galaxy_wp_utils::get_post_custom( $post->ID );
		$data['post_id'] = $post->ID;
		$data['post_type'] = get_post_type( $post->ID );
		$this->view->load_partial( 'layout_editor/metabox_appearance', $data );
	}
	
	/**
	 * Page layout metabox
	 **/
	function render_metabox_page_layout( $post ) {
		$data = wpl_galaxy_wp_utils::get_post_custom( $post->ID );
		
		$data['_wproto_taxonomies'] = $this->model->taxonomies->get_supported();
		
		$this->view->load_partial( 'layout_editor/metabox_page_layout_settings', $data );
	}
	
	/**
	 * Media layout settings
	 **/
	function render_metabox_page_media_layout( $post ) {
		$data = wpl_galaxy_wp_utils::get_post_custom( $post->ID );
		
		$this->view->load_partial( 'layout_editor/metabox_page_media_layout_settings', $data );
	}
	
	/**
	 * Custom layout builder metabox
	 **/
	function render_metabox_custom_layout_builder( $post ) {
		$data = wpl_galaxy_wp_utils::get_post_custom( $post->ID );
		
		$_sections = isset( $data['page_sections'] ) ? unserialize( $data['page_sections'] ) : array();
		
		$data['wproto_custom_sections'] = $this->model->sections->get( array_values( $_sections ) );
		
		$this->view->load_partial( 'layout_editor/metabox_page_layout_builder', $data );
	}
	
	/**
	 * One page template metabox
	 **/
	function render_metabox_one_page_template( $post ) {
		global $wp_registered_sidebars;
		
		$data = wpl_galaxy_wp_utils::get_post_custom( $post->ID );
		
		$data['registered_sidebars'] = $wp_registered_sidebars;
		$data['post_id'] = $post->ID;
		
		$this->view->load_partial( 'layout_editor/metabox_one_page_template', $data );
		
	}
	
	/**
	 * Save custom fields
	 **/
	function save_custom_meta( $post_id ) {

		// Stop WP from clearing custom fields on autosave
		if ( defined( 'DOING_AUTOSAVE') && DOING_AUTOSAVE )
			return;

		// Prevent quick edit from clearing custom fields
		if ( defined( 'DOING_AJAX') && DOING_AJAX )
			return;

		if( empty( $_POST) )
			return;
		
		$post_type = get_post_type( $post_id );
		
		$allowed_tags = wp_kses_allowed_html( 'post' );
		
		if( isset( $_POST['wproto_settings'] ) && is_array( $_POST['wproto_settings'] ) && count( $_POST['wproto_settings'] ) > 0 ) {
			
			foreach( $_POST['wproto_settings'] as $k=>$v ) {
				update_post_meta( $post_id, wp_kses( $k, $allowed_tags ), is_string( $v ) ? wp_kses( str_replace( "'", '&#39;', stripslashes( $v ) ), $allowed_tags ) : $v );
			}
			
		}
		
	}
	
	/**
	 * Custom theme templates
	 **/
	function theme_template_init() {
		global $post;
		
		/**
		 * Check for custom user redirect
		 **/
		if( gettype( $post ) == 'object' ) {

			$data = wpl_galaxy_wp_utils::get_post_custom( $post->ID );

			$data['wproto_redirect_url'] = isset( $data['wproto_redirect_url'] ) ? $data['wproto_redirect_url'] : '';
			$data['wproto_redirect_page_id'] = isset( $data['wproto_redirect_page_id'] ) ? $data['wproto_redirect_page_id'] : '';
			$data['wproto_redirect_type'] = isset( $data['wproto_redirect_type'] ) ? $data['wproto_redirect_type'] : '';
			$data['wproto_redirect_enabled'] = isset( $data['wproto_redirect_enabled'] ) ? $data['wproto_redirect_enabled'] : 'no';
			$data['wproto_redirect_code'] = isset( $data['wproto_redirect_code'] ) ? $data['wproto_redirect_code'] : '';
		
			if( $data['wproto_redirect_enabled'] == 'yes' ) {
				$to = $data['wproto_redirect_type'] == 'page' ? get_permalink( $data['wproto_redirect_page_id'] ) : $data['wproto_redirect_url'];
			}
		
			if( isset( $to ) && trim( $to ) <> '' ) {
				wp_redirect( $to, $data['wproto_redirect_code'] );
				exit;
			}	
		}
		
		
		
	}
	
	/**
	 * Find posts by post title and post type via ajax
	 **/
	function ajax_find_posts() {
		
		$response = array();
		
		$post_type = isset( $_GET['post_type'] ) ? trim( strip_tags( $_GET['post_type'] ) ) : '';
		$search_string = isset( $_GET['term'] ) ? like_escape( $_GET['term'] ) : '';
		
		if( $post_type <> '' && $search_string <> '' ) {
			
			$posts = $this->model->post->search_post_by_title( $search_string, $post_type );
			
			if( is_array( $posts ) ) {
				
				for( $i=0; $i<count( $posts ); $i++ ) {
					$response[ $i ]['title'] = $posts[$i]->post_title;
					$response[ $i ]['value'] = $posts[$i]->ID;
					$response[ $i ]['label'] = $posts[$i]->post_title;
				}
				
			}

		}
		
		die( json_encode( $response ) );
	}
	
	/**
	 * Delete section
	 **/
	function ajax_delete_section() {
		
		$section_id = isset( $_POST['section_id'] ) ? absint( $_POST['section_id'] ) : 0;
		
		$this->model->sections->delete( $section_id );
		
		die;
	}
	
	/**
	 * Add section
	 **/
	function ajax_add_edit_section() {
		
		$data = array();
		
		$_subaction = isset( $_GET['subaction'] ) && $_GET['subaction'] == 'edit' ? 'edit' : 'add';
		$_id = $_subaction == 'edit' && isset( $_GET['id'] ) ? absint( $_GET['id'] ) : 0;
				
		$data = $_subaction == 'edit' ? $this->model->sections->get_single( $_id ) : array();
		$data['section'] = isset( $_GET['type'] ) ? strip_tags( $_GET['type'] ) : '';
		$data['id'] = $_id;
		
		if( in_array( $data['section'], array( 'benefits', 'catalog', 'portfolio', 'text', 'testimonials', 'slider', 'product', 'posts', 'posts_video', 'posts_photoalbum', 'subscribe_form', 'parallax', 'hexagon_carousel', 'pricing_tables', 'contact' ) ) ) {
			
			$this->view->load_page('layout_editor/add_edit_section', $data );
		} else {
			_e('Invalid section type', 'wproto');
		}
		
		die;
	}
	
	/**
	 * Submit add / edit section form
	 **/
	function save() {
		
		$id = isset( $_POST['section_id'] ) ? absint( $_POST['section_id'] ) : 0;
		
		$allowed_tags = wp_kses_allowed_html( 'post' );
		
		// prepare data
		$section = array(
			'title' => isset( $_POST['wproto_section_content']['title'] ) ? wp_kses( $_POST['wproto_section_content']['title'], $allowed_tags ) : '',
			'subtitle' => isset( $_POST['wproto_section_content']['subtitle'] ) ? wp_kses( $_POST['wproto_section_content']['subtitle'], $allowed_tags ) : '',
			'before_text' => isset( $_POST['wproto_section_content']['before_text'] ) ? wp_kses( str_replace( "'", '&#39;', stripslashes( $_POST['wproto_section_content']['before_text'] ) ), $allowed_tags ) : '',
			'after_text' => isset( $_POST['wproto_section_content']['after_text'] ) ? wp_kses( str_replace( "'", '&#39;', stripslashes( $_POST['wproto_section_content']['after_text'] ) ), $allowed_tags ) : '',
			'type' => isset( $_POST['section_type'] ) ? wp_kses( $_POST['section_type'], $allowed_tags ) : '',
			'data' => isset( $_POST['wproto_section_data'] ) ? serialize( $_POST['wproto_section_data'] ) : ''
		);
		
		if( $id > 0 ) {
			// edit existing record
			$section['ID'] = $id;
			$this->model->sections->update( $section );
			
		} else {
			
			// save new record
			$section_id = $this->model->sections->add( $section );
			$section['ID'] = $section_id;
			
			$section = (object)$section;
			
			ob_start();
				include WPROTO_ENGINE_DIR . '/view/layout_editor/section.tpl';
			$new_section_html = ob_get_clean();
			$new_section_html = trim( str_replace( "\t", '', str_replace(array("\n", "\r"), '', $new_section_html ) ) );
			
			echo "<script>self.parent.jQuery('#wproto_tpl_page_custom_layout_builder .sections').append('" . $new_section_html . "'); self.parent.wprotoSetupTooltips();</script>";
			
		}
		
		// close ThickBox window and exit
		echo '<script>top.tb_remove();</script>';
		die;
		
	}
	
}