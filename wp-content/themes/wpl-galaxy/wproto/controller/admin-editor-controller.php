<?php
/**
 * Visual Editor Controller
 **/
class wpl_galaxy_wp_admin_editor_controller extends wpl_galaxy_wp_admin_controller {
	
	function __construct() {
		
		if( is_admin() ) {
			
			
			// add custom buttons to the Editor
			add_action( 'admin_init', array( $this, 'add_editor_buttons' ) );
			// Visual shortcodes
			add_filter( 'jpb_visual_shortcodes', array( $this, 'add_visual_shortcodes'));
			
			add_action( 'wp_ajax_wproto_editor_button_form', array( $this, 'ajax_show_button_form' ) );
			add_action( 'wp_ajax_wproto_editor_minify_link', array( $this, 'ajax_minify_link' ) );
			
			// TODO: Add Visual Composer. Filter to Replace default css class for Visual Composer
			// if( function_exists('vc_set_as_theme')) vc_set_as_theme();
			// add_filter( 'vc_shortcodes_css_class', array( $this, 'add_vc_custom_grid' ), 10, 2);
			
		}
		
	}
	
	
	/**
	 * Add custom buttons to the default WP Editor
	 **/
	function add_editor_buttons() {
		global $typenow;
		add_editor_style();
		
		if ( current_user_can( 'edit_posts' ) && current_user_can( 'edit_pages' ) ) {
			
			$allowed_type = $typenow == '' ? 'post' : $typenow;
			
			$allowed = array( 'post', 'page' );
			if( in_array( $allowed_type, $allowed ) ) {
				add_filter( 'mce_buttons_3', array( $this, 'filter_mce_button' ) );
				add_filter( 'mce_external_plugins', array( $this, 'filter_mce_plugin' ) );
			}
			
		}
	}
	
	function filter_mce_button( $buttons ) {
		
		array_push( $buttons, 'wproto_column_formatting_button');
		array_push( $buttons, 'wproto_remove_column_formatting_button');
		array_push( $buttons, 'wproto_insert_line_before_button');
		array_push( $buttons, 'wproto_insert_line_after_button');
		
		array_push( $buttons, 'wproto_insert_animation_button');
		array_push( $buttons, 'wproto_insert_divider_button');
		array_push( $buttons, 'wproto_insert_highlight_button');
		array_push( $buttons, 'wproto_insert_audio_button');
		array_push( $buttons, 'wproto_insert_video_button');
		array_push( $buttons, 'wproto_insert_shorted_link_button');
		array_push( $buttons, 'wproto_insert_btn_button');
		array_push( $buttons, 'wproto_insert_tooltip_button');
		array_push( $buttons, 'wproto_insert_call_to_action_button');
		array_push( $buttons, 'wproto_insert_slider');
		array_push( $buttons, 'wproto_insert_contact_form_button');
		array_push( $buttons, 'wproto_insert_googlemap_button');
		array_push( $buttons, 'wproto_insert_progress_button');
		array_push( $buttons, 'wproto_insert_toggle_button');
		array_push( $buttons, 'wproto_insert_tabs_button');
		array_push( $buttons, 'wproto_insert_pricing_tables_button');
		array_push( $buttons, 'wproto_insert_posts_button');
		array_push( $buttons, 'wproto_insert_catalog_button');
		array_push( $buttons, 'wproto_insert_team_button');
		array_push( $buttons, 'wproto_insert_benefits_button');
		array_push( $buttons, 'wproto_insert_photogallery_button');
		array_push( $buttons, 'wproto_insert_testimonials_button');
		array_push( $buttons, 'wproto_insert_portfolio_button');
		array_push( $buttons, 'wproto_insert_partners_clients_button');
		
		return $buttons;
	}
	
	function filter_mce_plugin( $plugins ) {
		$plugins[ 'wproto_column_formatting' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/layout.js';
		
		$plugins[ 'wproto_remove_column_formatting' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/layout_remove.js';
		$plugins[ 'wproto_insert_line_before' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/layout_line_before.js';
		$plugins[ 'wproto_insert_line_after' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/layout_line_after.js';
		
		$plugins[ 'wproto_insert_btn' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/btn.js';
		$plugins[ 'wproto_insert_tooltip' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/tooltip.js';
		$plugins[ 'wproto_insert_toggle' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/toggle.js';
		$plugins[ 'wproto_insert_tabs' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/tabs.js';
		$plugins[ 'wproto_insert_pricing_tables' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/pricing_tables.js';
		$plugins[ 'wproto_insert_highlight' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/highlight.js';
		$plugins[ 'wproto_insert_audio' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/audio.js';
		$plugins[ 'wproto_insert_video' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/video.js';
		$plugins[ 'wproto_insert_slider' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/slider.js';
		$plugins[ 'wproto_insert_divider' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/divider.js';
		$plugins[ 'wproto_insert_animation' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/animation.js';
		$plugins[ 'wproto_insert_call_to_action' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/call_to_action.js';
		$plugins[ 'wproto_insert_contact_form_button' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/contact_form.js';
		$plugins[ 'wproto_insert_shorted_link' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/shorted_link.js';
		$plugins[ 'wproto_insert_googlemap' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/googlemap.js';
		$plugins[ 'wproto_insert_progress' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/progress.js';
		$plugins[ 'wproto_insert_benefits' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/benefits.js';
		$plugins[ 'wproto_insert_posts' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/posts.js';
		$plugins[ 'wproto_insert_catalog' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/catalog.js';
		$plugins[ 'wproto_insert_team' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/team.js';
		$plugins[ 'wproto_insert_photogallery' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/photogallery.js';
		$plugins[ 'wproto_insert_testimonials' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/testimonials.js';
		$plugins[ 'wproto_insert_portfolio' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/portfolio.js';
		$plugins[ 'wproto_insert_partners_clients' ] = WPROTO_THEME_URL . '/js/admin/editor_buttons/partners_clients.js';
		return $plugins;
	}
	
	/**
	 * Add Visual Shortcodes
	 **/
	function add_visual_shortcodes( $shortcodes ) {
		
		$shortcodes[] = array(
			'shortcode' => 'wproto_contact_form',
			'image'     => WPROTO_THEME_URL . '/images/admin/shortcodes/contact_form.png',
			'command'   => 'cmd_wproto_contact_form'
		);
		
		/*
    $shortcodes[] = array(
			'shortcode' => 'wproto_toggle',
			'image'     => WPROTO_THEME_URL . '/images/admin/shortcodes/toggle.png',
			'command'   => 'cmd_wproto_toggle'
		);    

    $shortcodes[] =  array(
			'shortcode' => 'wproto_tabs',
			'image'     => WPROTO_THEME_URL . '/images/admin/shortcodes/tabs.png',
			'command'   => 'cmd_wproto_tabs'
		);*/      
		
    $shortcodes[] =  array(
			'shortcode' => 'wproto_pricing_tables',
			'image'     => WPROTO_THEME_URL . '/images/admin/shortcodes/pricing_table.png',
			'command'   => 'cmd_wproto_pricing_tables'
		);    
		
    $shortcodes[] = array(
			'shortcode' => 'layerslider',
			'image'     => WPROTO_THEME_URL . '/images/admin/shortcodes/slider.png',
			'command'   => 'cmd_wproto_slider'
		);    
		
    $shortcodes[] = array(
			'shortcode' => 'wproto_call_to_action',
			'image'     => WPROTO_THEME_URL . '/images/admin/shortcodes/call_to_action.png',
			'command'   => 'cmd_wproto_call_to_action'
		); 
		
    $shortcodes[] = array(
			'shortcode' => 'wproto_map',
			'image'     => WPROTO_THEME_URL . '/images/admin/shortcodes/google_map.png',
			'command'   => 'cmd_wproto_google_map'
		); 
		
    $shortcodes[] = array(
			'shortcode' => 'wproto_progress',
			'image'     => WPROTO_THEME_URL . '/images/admin/shortcodes/progress.png',
			'command'   => 'cmd_wproto_progress'
		); 
		
    $shortcodes[] = array(
			'shortcode' => 'wproto_benefits',
			'image'     => WPROTO_THEME_URL . '/images/admin/shortcodes/benefits.png',
			'command'   => 'cmd_wproto_benefits'
		); 
		
    $shortcodes[] = array(
			'shortcode' => 'wproto_posts',
			'image'     => WPROTO_THEME_URL . '/images/admin/shortcodes/posts.png',
			'command'   => 'cmd_wproto_posts'
		); 
		
    $shortcodes[] = array(
			'shortcode' => 'wproto_catalog',
			'image'     => WPROTO_THEME_URL . '/images/admin/shortcodes/catalog.png',
			'command'   => 'cmd_wproto_catalog'
		); 
		
    $shortcodes[] = array(
			'shortcode' => 'wproto_team',
			'image'     => WPROTO_THEME_URL . '/images/admin/shortcodes/team.png',
			'command'   => 'cmd_wproto_team'
		); 
		
    $shortcodes[] = array(
			'shortcode' => 'wproto_photoalbums',
			'image'     => WPROTO_THEME_URL . '/images/admin/shortcodes/photoalbums.png',
			'command'   => 'cmd_wproto_photoalbums'
		); 
		
    $shortcodes[] = array(
			'shortcode' => 'wproto_testimonials',
			'image'     => WPROTO_THEME_URL . '/images/admin/shortcodes/testimonials.png',
			'command'   => 'cmd_wproto_testimonials'
		); 
		
    $shortcodes[] = array(
			'shortcode' => 'wproto_portfolio',
			'image'     => WPROTO_THEME_URL . '/images/admin/shortcodes/portfolio.png',
			'command'   => 'cmd_wproto_portfolio'
		); 
		
    $shortcodes[] = array(
			'shortcode' => 'wproto_clients_partners',
			'image'     => WPROTO_THEME_URL . '/images/admin/shortcodes/clients_partners.png',
			'command'   => 'cmd_wproto_clients_partners'
		); 

		return $shortcodes;
	}
	
	/**
	 * Show forms for buttons
	 **/
	
	function ajax_show_button_form() {

		$response = array();
		$data = array();
		$_POST = wp_unslash( $_POST );
		$data = isset( $_POST ) ? $_POST : array();
		
		$template = $_POST['template'];
		
		if( $template == 'wproto_insert_slider' ) {
			$data['layerslider_slideshows'] = $this->model->slider->get_layerslider_slideshows();
		}
		
		if( $template == 'wproto_insert_pricing_tables' ) {
			$data['tables'] = $this->model->post->get_all_posts('wproto_pricing_table');
		}
		
		ob_start();
		
		$this->view->load_partial( 'editor_buttons/' . $template, $data );
		
		$response['html'] = ob_get_clean();
		
		die( json_encode( $response ) );
	}
	
	/**
	 * Minify link
	 **/
	function ajax_minify_link() {
		
		$settings = get_option( 'wproto_theme_settings' );
		
		$api_key = isset( $settings['social']['google_api_key'] ) ? $settings['social']['google_api_key'] : '';
		
		$googl = new Googl( $api_key ); 
		$link = $googl->set_short( $_POST['link'] );
		die( isset( $link['id'] ) ? $link['id'] : $_POST['link'] );
		
	}
	
	/**
	 * Visual composer grid
	 **/
	function add_vc_custom_grid( $class_string, $tag ) {

  	if ( $tag=='vc_row' || $tag=='vc_row_inner' ) {
    	$class_string = str_replace( 'vc_row-fluid', 'grid', $class_string );
  	}
  	if ( $tag=='vc_column' || $tag=='vc_column_inner' ) {
  		$class_string = str_replace( 'vc_span12', 'unit whole', $class_string );
  		$class_string = str_replace( 'vc_span10', 'unit five-sixth', $class_string );
  		$class_string = str_replace( 'vc_span9', 'unit three-quarters', $class_string );
  		$class_string = str_replace( 'vc_span8', 'unit two-thirds', $class_string );
  		$class_string = str_replace( 'vc_span6', 'unit half', $class_string );
  		$class_string = str_replace( 'vc_span4', 'unit one-third', $class_string );
  		$class_string = str_replace( 'vc_span3', 'unit one-quarter', $class_string );
  		$class_string = str_replace( 'vc_span2', 'unit one-sixth', $class_string );
 		}
  	return $class_string;
	}
	
}