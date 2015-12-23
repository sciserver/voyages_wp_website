<?php
/**
 * Theme customizer controller
 **/
class wpl_galaxy_wp_customizer_controller extends wpl_galaxy_wp_base_controller {
	
	/**
	 * Below ALL add_action() and add_filter() hooks that
	 * get served by the methods of this controller
	 **/
	function __construct() {
		
		if( is_admin() ) {
			add_action( 'customize_register', array( $this, 'init_customizer' ) );
			add_action( 'customize_controls_print_footer_scripts', array( $this, 'init_customizer_js' ) );
		}
		add_action( 'customize_preview_init', array( $this, 'customizer_preview' ) );
		
	}
	
	/**
	 * Init theme customizer
	 **/
	function init_customizer( $wp_customize ) {
		
		/**
		 * Customizer sections
		 **/
		
		$wp_customize->add_section(
			'wproto_mega_menu',
			array(
				'title'     => __('Mega menu style', 'wproto'),
				'priority'  => 200
			)
		);
		
		// color schemes
		$wp_customize->add_section(
			'wproto_color_schemes',
			array(
				'title'     => __('Color Schemes', 'wproto'),
				'priority'  => 201
			)
		);
		
		$wp_customize->add_section(
			'wproto_boxed_layout',
			array(
				'title'     => __('Layout', 'wproto'),
				'priority'  => 202
			)
		);
		
		$wp_customize->add_section(
			'wproto_header_top_menu',
			array(
				'title'     => __('Header top menu', 'wproto'),
				'priority'  => 203
			)
		);
		
		$wp_customize->add_section(
			'wproto_header_layouts',
			array(
				'title'     => __('Header layouts', 'wproto'),
				'priority'  => 204
			)
		);
		
		$wp_customize->add_section(
			'wproto_fonts',
			array(
				'title'     => __('Fonts', 'wproto'),
				'priority'  => 205
			)
		);
		
		/**
		 * Customizer options
		 **/
		
		// mega menu style
		
		$wp_customize->add_setting(
			'wproto_mega_menu_style',
			array(
				'default'   => 'wide',
				'transport' => 'postMessage'
			)
		);
		
		$wp_customize->add_control(
			'wproto_mega_menu_style',
			array(
				'section'  => 'wproto_mega_menu',
				'label'    => __('Mega Menu Style', 'wproto'),
				'type'     => 'select',
				'choices'  => array(
					'wide' => __('Wide (full width)', 'wproto'),
					'relative' => __('Relative to parent', 'wproto')
				)
			)
		);
		
		// Color scheme settings
		$wp_customize->add_setting(
			'wproto_color_scheme',
			array(
				'default'   => 'skin-blue',
				'transport' => 'postMessage'
			)
		);
		
		$wp_customize->add_control(
			'wproto_color_scheme',
			array(
				'section'  => 'wproto_color_schemes',
				'label'    => __('Color scheme', 'wproto'),
				'type'     => 'select',
				'choices'  => array(
					'skin-blue' => __('Blue', 'wproto'),
					'skin-brown' => __('Brown', 'wproto'),
					'skin-dark-green' => __('Dark Green', 'wproto'),
					'skin-gray' => __('Gray', 'wproto'),
					'skin-light-green' => __('Light Green', 'wproto'),
					'skin-orange' => __('Orange', 'wproto'),
					'skin-pink' => __('Pink', 'wproto'),
					'skin-purple' => __('Purple', 'wproto'),
					'skin-red' => __('Red', 'wproto'),
					'skin-sky-blue' => __('Sky Blue', 'wproto')
				)
			)
		);
		
		// Boxed layout
		$wp_customize->add_setting(
			'wproto_boxed_layout',
			array(
				'default'   => 'no',
				'transport' => 'postMessage'
			)
		);
		
		$wp_customize->add_control(
			'wproto_boxed_layout',
			array(
				'section'  => 'wproto_boxed_layout',
				'label'    => __('Boxed Layout', 'wproto'),
				'type'     => 'radio',
				'choices'  => array(
					'no' => __('No', 'wproto'),
					'yes' => __('Yes', 'wproto')
				)
			)
		);
		
		// Custom background color
		$wp_customize->add_setting(
    	'wproto_bg_color',
    	array(
        'default' => '#FFFFFF',
        'sanitize_callback' => 'sanitize_hex_color',
				'transport' => 'postMessage'
    	)
		);
		
		$wp_customize->add_control(
    	new WP_Customize_Color_Control(
        $wp_customize,
        'wproto_background_color',
        array(
            'label' => 'Background color',
            'section' => 'wproto_boxed_layout',
            'settings' => 'wproto_bg_color',
        )
    	)
		);
		
		// Boxed layout background
		$wp_customize->add_setting(
			'wproto_boxed_background',
			array(
				'default'   => '',
				'transport' => 'postMessage'
			)
		);
		
		$wp_customize->add_control(
  		new WP_Customize_Image_Control(
    		$wp_customize,
     		'wproto_background_image',
     		array(
      		'label'    => __('Custom background image', 'wproto'),
       		'settings' => 'wproto_boxed_background',
       		'section'  => 'wproto_boxed_layout'
       	)
       )
      );
      
		// Custom background position
		$wp_customize->add_setting(
			'wproto_boxed_background_position',
			array(
				'default'   => 'left top',
				'transport' => 'postMessage'
			)
		);
		
		$wp_customize->add_control(
			'wproto_boxed_background_position',
			array(
				'section'  => 'wproto_boxed_layout',
				'label'    => __('Custom background position', 'wproto'),
				'type'     => 'select',
				'choices'  => array(
					'left top' => 'left top',
					'right top' => 'right top',
					'left bottom' => 'left bottom',
					'right bottom' => 'right bottom'
				)
			)
		);
		
		// Custom background repeat
		$wp_customize->add_setting(
			'wproto_boxed_background_repeat',
			array(
				'default'   => 'no-repeat',
				'transport' => 'postMessage'
			)
		);
		
		$wp_customize->add_control(
			'wproto_boxed_background_repeat',
			array(
				'section'  => 'wproto_boxed_layout',
				'label'    => __('Custom background repeat', 'wproto'),
				'type'     => 'select',
				'choices'  => array(
					'no-repeat' => 'no-repeat',
					'repeat' => 'repeat x and y',
					'repeat-x' => 'repeat-x',
					'repeat-y' => 'repeat-y'
				)
			)
		);
		
		// Custom fixed background
		$wp_customize->add_setting(
			'wproto_boxed_background_fixed',
			array(
				'default'   => '',
				'transport' => 'postMessage'
			)
		);
		
		$wp_customize->add_control(
			'wproto_boxed_background_fixed',
			array(
				'section'  => 'wproto_boxed_layout',
				'label'    => __('Fixed background', 'wproto'),
				'type'     => 'radio',
				'choices'  => array(
					'' => __('Off', 'wproto'),
					'fixed' => __('On', 'wproto')
				)
			)
		);
		
		// Boxed layout pattern
		$wp_customize->add_setting(
			'wproto_boxed_pattern',
			array(
				'default'   => 'none',
				'transport' => 'postMessage'
			)
		);
		
		$wp_customize->add_control(
			'wproto_boxed_pattern',
			array(
				'section'  => 'wproto_boxed_layout',
				'label'    => __('Pattern', 'wproto'),
				'type'     => 'select',
				'choices'  => array(
					'none' => __('No pattern...', 'wproto'),
					'pattern-1' => __('Carbon fibre', 'wproto'),
					'pattern-2' => __('Cubes', 'wproto'),
					'pattern-3' => __('Escheresque', 'wproto'),
					'pattern-4' => __('Fabric of squares', 'wproto'),
					'pattern-5' => __('Gray wash wall', 'wproto'),
					'pattern-6' => __('Random grey variations', 'wproto'),
					'pattern-7' => __('Wood', 'wproto'),
					'pattern-8' => __('Material', 'wproto'),
					'pattern-9' => __('Tileable wood', 'wproto'),
					'pattern-10' => __('Tweed', 'wproto')
				)
			)
		);
		
		// Header top menu
		$wp_customize->add_setting(
			'wproto_header_top_menu',
			array(
				'default'   => 'yes',
				'transport' => 'postMessage'
			)
		);
		
		$wp_customize->add_control(
			'wproto_header_top_menu',
			array(
				'section'  => 'wproto_header_top_menu',
				'label'    => __('Header top menu', 'wproto'),
				'type'     => 'radio',
				'choices'  => array(
					'no' => __('Off', 'wproto'),
					'yes' => __('On', 'wproto')
				)
			)
		);
		
		// Header layouts
		$wp_customize->add_setting(
			'wproto_header_layout',
			array(
				'default'   => 'header-default',
				'transport' => 'postMessage'
			)
		);
		
		$wp_customize->add_control(
			'wproto_header_layout',
			array(
				'section'  => 'wproto_header_layouts',
				'label'    => __('Header layout', 'wproto'),
				'type'     => 'select',
				'choices'  => array(
					'header-default' => __('Default', 'wproto'),
					'header-default-centered' => __('Default centered', 'wproto'),
					'header-big-background' => __('Big background', 'wproto'),
					'header-classic' => __('Classic', 'wproto'),
					'header-classic-centered' => __('Classic centered', 'wproto'),
					'header-full-width' => __('Full width', 'wproto')
				)
			)
		);
		
		$fonts = wpl_galaxy_wp_utils::get_google_fonts();
		
		// Primary font
		$wp_customize->add_setting(
			'wproto_primary_font',
			array(
				'default'   => 'Roboto',
				'transport' => 'postMessage'
			)
		);
		
		$wp_customize->add_control(
			'wproto_primary_font',
			array(
				'section'  => 'wproto_fonts',
				'label'    => __('Primary Font', 'wproto'),
				'type'     => 'select',
				'choices'  => $fonts
			)
		);
		
		// Secondary font
		$wp_customize->add_setting(
			'wproto_secondary_font',
			array(
				'default'   => 'Roboto Slab',
				'transport' => 'postMessage'
			)
		);
		
		$wp_customize->add_control(
			'wproto_secondary_font',
			array(
				'section'  => 'wproto_fonts',
				'label'    => __('Secondary Font', 'wproto'),
				'type'     => 'select',
				'choices'  => $fonts
			)
		);
		
  	$wp_customize->get_setting( 'blogname' )->transport = 'postMessage';
   	$wp_customize->get_setting( 'blogdescription' )->transport = 'postMessage';
		
	}
	
	/**
	 * Custom controls handle
	 **/
	function init_customizer_js() {
		wp_enqueue_script( 'wproto-customizer-preview', get_template_directory_uri() . '/js/admin/screen-customizer.js' );
	}
	
	/**
	 * Preview the changes
	 **/
	function customizer_preview() {
		
		wp_enqueue_script( 'less', get_template_directory_uri() . '/js/libs/less-1.5.1.min.js' );
		wp_enqueue_script( 'wproto-customizer-preview', get_template_directory_uri() . '/js/admin/customizer-preview.js', array( 'jquery', 'customize-preview' ) );
		$js_vars = array(
			'themeURL' => WPROTO_THEME_URL
		);
		wp_localize_script( 'wproto-customizer-preview', 'wprotoCustomizer', $js_vars );
		
	}
	
}