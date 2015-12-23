<?php
/**
 * Back-end controller
 **/
class wpl_galaxy_wp_admin_controller extends wpl_galaxy_wp_base_controller {
	
	function __construct() {
		
		if( is_admin() ) {
			
			add_filter( 'admin_body_class', array( $this, 'check_wp_version' ));
			
			// Add admin scripts and styles
			add_action( 'admin_enqueue_scripts', array( $this, 'add_scripts' ) );
			add_action( 'admin_enqueue_scripts', array( $this, 'add_styles' ) );
			
			// Cron jobs
			add_filter( 'cron_schedules', array( $this, 'schedule_cron'));
			add_action( 'weekly_cron', array( $this, 'weekly_cron'));
			
			// Footer notice
			add_filter( 'admin_footer_text', array( $this, 'add_footer_wproto_info'));
			
			// Demo notice
			add_action( 'admin_notices', array( $this, 'add_demo_data_notice'));
			add_action( 'wp_ajax_wproto_dismiss_demo_data_notice', array( $this, 'dismiss_demo_data_notice' ) );
			
			// hide infobox
			add_action( 'wp_ajax_wproto_ajax_hide_infobox', array( $this, 'ajax_hide_infobox' ) );
			
			// Setup admin menu
			add_action( 'admin_menu', array( $this, 'setup_admin_menu' ) );
			add_action( 'admin_enqueue_scripts', array( $this, 'highlight_menu' ) );
			add_action( 'admin_enqueue_scripts', array( $this, 'fix_admin_icons' ) );
			
			// Icon picker dialog
			add_action( 'wp_ajax_wproto_ajax_show_icon_picker_form', array( $this, 'ajax_show_icon_picker_form' ) );
			
			// Attach images to the post
			add_action( 'wp_ajax_wproto_ajax_get_html_for_attached_images', array( $this, 'get_html_for_attached_images' ) );
			add_action( 'save_post', array( $this, 'save_custom_meta' ) );
			
			// Change post status
			add_action( 'wp_ajax_wproto_ajax_change_post_status', array( $this, 'ajax_change_post_status' ) );

		}
		
	}
	
	function check_wp_version( $classes ) {
		global $wp_version;
		
		if( version_compare( $wp_version, '3.8', '<' ) ) {
			$classes .= 'wproto-old-admin-style';
		} else {
			$classes .= 'wproto-new-admin-style';
		}
		
		return $classes;
	}
	
	/**
	 * Add admin scripts
	 **/
	function add_scripts() {
		global $post;
		
		wp_enqueue_script( 'jquery' );
		wp_enqueue_script( 'jquery-ui-core' );
		wp_enqueue_script( 'jquery-ui-sortable' );
		wp_enqueue_script( 'jquery-ui-slider' );
		wp_enqueue_script( 'jquery-ui-dialog' );
		wp_enqueue_script( 'jquery-ui-datepicker' );
		wp_enqueue_script( 'jquery-ui-accordion' );
		wp_enqueue_script( 'jquery-ui-autocomplete' );

		wp_enqueue_script( 'thickbox' );
		wp_enqueue_script( 'editor' );
		wp_enqueue_script( 'quicktags' );
		wp_enqueue_script( 'wp-pointer' );
		wp_enqueue_script( 'wp-color-picker' );

		wp_enqueue_media();
		
		$js_vars = array(
			'ajaxNonce' => wp_create_nonce( 'wproto-engine-ajax-nonce' ),
			'adminURL' => admin_url(),
			'postID' => isset( $post->ID ) ? $post->ID : 0,
			'adminBigLoaderImage' => wpl_galaxy_wp_utils::is_retina() ? '<img id="wproto-big-loader" width="48" height="48" src="' . WPROTO_THEME_URL . '/images/admin/ajax-loader-big@2x.gif" alt="" />' : '<img id="wproto-big-loader" src="' . WPROTO_THEME_URL . '/images/admin/ajax-loader-big.gif" alt="" />',
			'mceTransImg' => '/wp-includes/js/tinymce/plugins/wordpress/img/trans.gif',
			'adminBigLoaderImageTransp' => wpl_galaxy_wp_utils::is_retina() ? '<img id="wproto-big-loader-transp" width="48" height="48" src="' . WPROTO_THEME_URL . '/images/admin/ajax-loader-big-transp@2x.gif" alt="" />' : '<img id="wproto-big-loader-transp" src="' . WPROTO_THEME_URL . '/images/admin/ajax-loader-big-transp.gif" alt="" />',
			'adminIconTrue' => wpl_galaxy_wp_utils::is_retina() ? WPROTO_THEME_URL . '/images/admin/true@2x.png' : WPROTO_THEME_URL . '/images/admin/true.png',
			'adminIconFalse' => wpl_galaxy_wp_utils::is_retina() ? WPROTO_THEME_URL . '/images/admin/false@2x.png' : WPROTO_THEME_URL . '/images/admin/false.png',
			'strError' => __( 'Error', 'wproto' ),
			'strRemove' => __( 'Remove', 'wproto' ),
			'strRename' => __( 'Rename', 'wproto' ),
			'strDelete' => __( 'Delete', 'wproto' ),
			'strChange' => __( 'Change', 'wproto' ),
			'strSticky' => __( 'Sticky', 'wproto' ),
			'strSelect' => __( 'Select', 'wproto' ),
			'strSuccess' => __( 'Successfully', 'wproto' ),
			'strGrabbing' => __( 'Grabbing', 'wproto' ),
			'strCantConnectToGoogle' => __( 'Cannot connect to Google', 'wproto' ),
			'strPleaseWait' => __( 'Please, wait...', 'wproto' ),
			'strNoAttachmentsFound' => __( 'No images was found.', 'wproto' ),
			'strAllDone' => __( 'All done', 'wproto' ),
			'strRebuilding' => __( 'Rebuilding', 'wproto' ),
			'strOf' => __( 'of', 'wproto' ),
			'strSelectImage' => __( 'Select an image', 'wproto' ),
			'strNoImagesSelected' => __( 'No images selected', 'wproto' ),
			'strOneImagesSelected' => __( 'One image selected', 'wproto' ),
			'strImagesSelected' => __( 'images selected', 'wproto' ),
			'strAttachImages' => __( 'Attach Images', 'wproto' ),
			'strInsertAttachedImages' => __( 'Select', 'wproto' ),
			'strAJAXError' => __( 'An AJAX error occurred when performing a query. Please contact Customer Support if the problem persists.', 'wproto' ),
			'strServerResponseError' => __( 'The script have received an invalid response from the server. Please contact Customer Support if the problem persists.', 'wproto' ),
			'strConfirm' => __( 'Confirm action', 'wproto' ),
			'strConfirmDelete' => __( 'Are you sure you want to delete? This action cannot be undone.', 'wproto' ),
			'strIconPicker' => __( 'Icon Picker', 'wproto' ),
			'strRemoveIcon' => __( 'Remove Icon', 'wproto' ),
			'strSelectIcon' => __( 'Select Icon', 'wproto' ),
			'strFullWidth' => __( 'Whole Width', 'wproto' ),
			'strGoldenLarge' => __( 'Golden Large', 'wproto' ),
			'strGoldenSmall' => __( 'Golden Small', 'wproto' ),
			'strBold' => __( 'Bold', 'wproto' ),
			'strItalic' => __( 'Italic', 'wproto' ),
			'strStrokeThrough' => __( 'Stroke through', 'wproto' ),
			'strLowercase' => __( 'Lowercase', 'wproto' ),
			'strUppercase' => __( 'Uppercase', 'wproto' ),
			'strTextIndent' => __( 'Text indent', 'wproto' ),
			'strLetterSpacing' => __( 'Letter spacing', 'wproto' ),
			'strLineHeight' => __( 'Line height', 'wproto' ),
			'strAlignments' => __( 'Alignments', 'wproto' ),
			'strLeft' => __( 'Left', 'wproto' ),
			'strCenter' => __( 'Center', 'wproto' ),
			'strRight' => __( 'Right', 'wproto' ),
			'strJustify' => __( 'Justify', 'wproto' ),
			'strPaddingMargin' => __( 'Padding/Margin', 'wproto' ),
			'strTop' => __( 'Top', 'wproto' ),
			'strLeft' => __( 'Left', 'wproto' ),
			'strRight' => __( 'Right', 'wproto' ),
			'strProcessing' => __( 'Processing...', 'wproto'),
			'strBottom' => __( 'Bottom', 'wproto' ),
			'mceButtonSlider' => __( 'Insert slider', 'wproto' ),
			'mceButtonColumnFormatting' => __( 'Column formatting', 'wproto' ),
			'mceButtonRemoveColumnFormatting' => __( 'Remove column formatting', 'wproto' ),
			'mceButtonLineBefore' => __( 'Insert line before', 'wproto' ),
			'mceButtonAnimation' => __( 'Add animation to image', 'wproto' ),
			'mceButtonLineAfter' => __( 'Insert line after', 'wproto' ),
			'mceButtonInsertButton' => __( 'Insert button', 'wproto' ),
			'mceButtonInsertNextPage' => __( 'Insert next page', 'wproto' ),
			'mceButtonInsertTooltip' => __( 'Insert tooltip', 'wproto' ),
			'mceButtonInsertToggle' => __( 'Insert toggle', 'wproto' ),
			'mceButtonInsertTabs' => __( 'Insert tabs', 'wproto' ),
			'mceButtonInsertProgressBar' => __( 'Insert Progress Bar', 'wproto' ),
			'mceButtonInsertPricingTables' => __( 'Insert pricing tables', 'wproto' ),
			'mceButtonHighlight' => __( 'Highlight text', 'wproto' ),
			'mceButtonBenefits' => __( 'Insert Benefits', 'wproto' ),
			'mceButtonPhotogallery' => __( 'Insert Photo Albums', 'wproto' ),
			'mceButtonTwitter' => __( 'Insert Tweets', 'wproto' ),
			'mceButtonImages' => __( 'Add images', 'wproto' ),
			'mceButtonTestimonials' => __( 'Insert Testimonials', 'wproto' ),
			'mceButtonVideo' => __( 'Insert Video', 'wproto' ),
			'mceButtonPosts' => __( 'Insert Posts', 'wproto' ),
			'mceButtonTeam' => __( 'Insert Team', 'wproto' ),
			'mceButtonCatalog' => __( 'Insert Catalog', 'wproto' ),
			'mceButtonShortedLink' => __( 'Insert Shorted Link', 'wproto' ),
			'mceButtonAudio' => __( 'Insert Audio', 'wproto' ),
			'mceButtonGoogleMap' => __( 'Insert Google Map', 'wproto' ),
			'mceButtonCallToAction' => __( 'Insert Call to action', 'wproto' ),
			'mceButtonPortfolio' => __( 'Insert Portfolio', 'wproto' ),
			'mceButtonClientsPartners' => __( 'Insert Clients, Partners etc...', 'wproto' ),
			'mceButtonPriceTable' => __( 'Insert Pricing table', 'wproto' ),
			'mceButtonContactForm' => __( 'Insert Contact form', 'wproto' ),
			'mceButtonTextBox' => __( 'Insert Text box', 'wproto' ),
			'mceButtonDivider' => __( 'Insert Divider', 'wproto' ),
			'buttonImagePath' => WPROTO_THEME_URL . '/images/admin/buttons',
			'moveImgSrc' => wpl_galaxy_wp_utils::is_retina() ? WPROTO_THEME_URL . '/images/admin/move@2x.png' : WPROTO_THEME_URL . '/images/admin/move.png',
			'widgetTogglesTitle' => __( 'Edit Toggles content', 'wproto' ),
			'widgetProgressTitle' => __( 'Edit Progress bars', 'wproto' ),
			'strValue' => __( 'Value', 'wproto' ),
			'strYourFeature' => __( 'Feature name', 'wproto' ),
			'strPackageName' => __( 'Package name', 'wproto' )
		);

		wp_register_script( 'wproto-engine-functions', WPROTO_THEME_URL . '/js/admin/functions.js?' . $this->settings['res_cache_time'] );
		wp_enqueue_script( 'wproto-engine-functions', array( 'jquery' ) );

		wp_register_script( 'wproto-engine-backend', WPROTO_THEME_URL . '/js/admin/backend.js?' . $this->settings['res_cache_time'] );
		wp_enqueue_script( 'wproto-engine-backend', array( 'wproto-engine-functions' ) );
		wp_localize_script( 'wproto-engine-backend', 'wprotoVars', $js_vars );
		
		if( isset( $_GET['wproto_admin_noheader'] ) ) {
			wp_register_script( 'wproto-remove-header', WPROTO_THEME_URL . '/js/admin/admin-noheader.js?' . $this->settings['res_cache_time'] );
			wp_enqueue_script( 'wproto-remove-header', array( 'jquery' ) );
		}	
		
		$screen = get_current_screen();
						
		if( isset( $screen->base ) && $screen->base == 'widgets' ) {
			wp_register_script( 'wproto-widgets-js', WPROTO_THEME_URL . '/js/admin/screen-widgets.js?' . $this->settings['res_cache_time'] );
			wp_enqueue_script( 'wproto-widgets-js', array( 'jquery' ) );
		}	
		
	}
	
	/**
	 * Add admin styles
	 **/
	function add_styles() {
		global $wp_styles;
		
		$screen = get_current_screen();
								
		wp_enqueue_style( 'wp-pointer' );
		wp_enqueue_style( 'thickbox' );
		wp_enqueue_style( 'editor' );
		wp_enqueue_style( 'wp-color-picker' );
		
		wp_enqueue_style( 'wproto-ui', WPROTO_THEME_URL . '/css/libs/ui/delta/jquery-ui.css?' . $this->settings['res_cache_time'] );
		wp_enqueue_style( 'wproto-backend', WPROTO_THEME_URL . '/css/admin/backend.css?' . $this->settings['res_cache_time'] );
		wp_enqueue_style( 'wproto-font-awesome', WPROTO_THEME_URL . '/css/libs/font-awesome/css/font-awesome.min.css?' . $this->settings['res_cache_time'] );

		$icomoon_enabled = $this->get_option( 'icomoon_enabled' );
		
		if( $icomoon_enabled == 'yes' ) {
			wp_enqueue_style( 'wproto-icomoon', WPROTO_THEME_URL . '/css/libs/icomoon/style.css?' . $this->settings['res_cache_time'] );
		}

		if( isset( $_GET['wproto_admin_noheader'] ) ) {
			wp_enqueue_style( 'wproto-backend-noheader', WPROTO_THEME_URL . '/css/admin/backend-noheader.css?' . $this->settings['res_cache_time'] );
		}
		
		$hide_infobox = $this->get_option( 'hide_infobox', 'general' );
		
		if( !isset( $_GET['post_type'] ) ) $_GET['post_type'] = '';
		if( !isset( $_GET['page'] ) ) $_GET['page'] = '';
		
		if( $hide_infobox != 'yes' && ( isset( $screen->base ) && $screen->base == 'edit' && ( in_array( @$_GET['post_type'], array( 'wproto_pricing_table', 'wproto_benefits', 'wproto_team', 'wproto_testimonials', 'wproto_partners', 'wproto_portfolio', 'wproto_catalog', 'wproto_photoalbums', 'wproto_video', 'wproto_slides' ) )) || @$_GET['page'] == 'wproto_theme_settings' ) ) {
			wp_enqueue_style( 'wproto-custom-admin', WPROTO_THEME_URL . '/css/admin/custom-admin.css?' . $this->settings['res_cache_time'] );
		}
		
	}
	
	
	/**
	 * Add cron jobs
	 **/
	function schedule_cron( $schedules ) {
		if( !is_array( $schedules ) ) $schedules = array();
		// add a 'weekly' schedule to the existing set
		$schedules['weekly'] = array(
			'interval' => 604800,
			'display' => __( 'Once Weekly', 'wproto')
		);            
		return $schedules;
	}
	
	/**
	 * Wproto weekly cron
	 **/
	function weekly_cron() {
		wpl_galaxy_wp_utils::purge_transients();
	}
	
	/**
	 * Add footer info
	 **/
	function add_footer_wproto_info( $text ) {
		return $text . ' ' . __( sprintf( 'And thank you for pursharing the theme! Visit <a href="%s" target="_blank">WPlab\'s</a> website to say hello to us.', 'http://www.wplab.pro/' ), 'wproto' );
	}
	
	/**
	 * Add demo data notice after install
	 **/
	function add_demo_data_notice() {
		if( get_option('wproto_show_demo_data_message') == 'yes' ):
			$this->view->load_partial( 'dialog/demo_data_notice' );
		endif;
	}
	
	/**
	 * Remove demo data info box
	 **/
	function dismiss_demo_data_notice() {
		delete_option('wproto_show_demo_data_message');
		die;
	}
	
	/**
	 * Disable infobox
	 **/
	function ajax_hide_infobox() {
		$this->write_option( 'hide_infobox', 'yes', 'general' );
		die;
	}
	
	/**
	 * Setup admin menu
	 **/
	function setup_admin_menu() {
		global $menu, $submenu, $wp_registered_sidebars;
		
		if ( current_user_can( 'manage_options' ) ) {
			
			add_menu_page( __( 'Theme Options', 'wproto' ),
													__( 'Theme Options', 'wproto' ),
													'administrator',
													'wproto_theme_settings',
													array( $this->controller->settings, 'display_settings_screen' ),
													'' );

			add_submenu_page( 'wproto_theme_settings',
														 __( 'Settings', 'wproto' ),
														 __( 'Settings', 'wproto' ),
														 'administrator',
														 'wproto_theme_settings',
														 array( $this->controller->settings, 'display_settings_screen' ) );
														 
			add_submenu_page( 'wproto_theme_settings',
														 __( 'Customize', 'wproto' ),
														 __( 'Customize', 'wproto' ),
														 'administrator',
														 'customize.php' );

			add_submenu_page( 'wproto_theme_settings',
														 __( 'Widget Areas', 'wproto' ),
														 __( 'Widget Areas', 'wproto' ),
														 'administrator',
														 'edit-tags.php?taxonomy=wproto_sidebars' );


		}																							
		
	}
	
	/**
	 * Highlight menu
	 **/
	function highlight_menu() {
		global $parent_file, $submenu_file;

		if( $submenu_file == 'edit-tags.php?taxonomy=wproto_sidebars' ) {
			$parent_file = 'wproto_theme_settings';
			$submenu_file = 'edit-tags.php?taxonomy=wproto_sidebars';
		}
		
	}
	
	/**
	 * Fix admin icons
	 **/
	function fix_admin_icons() {
		?>
    <style type="text/css">
			#icon-wproto_theme_settings { background: url(images/icons32.png?ver=20121105) -11px -5px no-repeat; }
			@media only screen and (-webkit-min-device-pixel-ratio:1.5) {
				#icon-wproto_theme_settings { background-image: url(images/icons32-2x.png?ver=20121105); background-size: 756px 45px; }
			}
		</style>
		<?php
	}
	
	/**
	 * AJAX - Show Wproto Icon Picker Dialog
	 **/
	function ajax_show_icon_picker_form() {
		$response = array();
		$icons = array();
		$icons = wpl_galaxy_wp_utils::get_icons();
		
		ob_start();
			$this->view->load_partial( 'dialog/icon_picker', array('icons' => $icons ) );
		$response['html'] = ob_get_clean();
		die( json_encode( $response ) );
	}
	
	/**
	 * Get HTML for attached images
	 **/
	function get_html_for_attached_images() {
		$response = array();

		ob_start();

		if( is_array( $_POST['images'] ) ) {
			foreach( $_POST['images'] as $image ) {
				
				if( (isset( $_POST['already_attached'] ) && is_array( $_POST['already_attached'] )) && in_array( $image['id'] , $_POST['already_attached'] ) ) {
					continue;
				}
				
				$this->view->load_partial( 'metaboxes/attached_images_item', array( 'id' => $image['id'] ) );
			}
		}
		
		$response['html'] = ob_get_clean();
		
		die( json_encode( $response ) );
	}
	
	/**
	 * Save meta for custom metaboxes
	 **/
	function save_custom_meta( $post_id ) {
		
		$post_type = get_post_type( $post_id );
		
		if(  in_array( $post_type, array( 'wproto_portfolio', 'wproto_photoalbums', 'wproto_catalog', 'page', 'post') ) ) {
			
			// Stop WP from clearing custom fields on autosave
			if ( defined( 'DOING_AUTOSAVE') && DOING_AUTOSAVE )
				return;

			// Prevent quick edit from clearing custom fields
			if ( defined( 'DOING_AJAX') && DOING_AJAX )
				return;

			if( empty( $_POST) )
				return;
				
			if( isset( $_POST["wproto_attached_images"] ) && is_array( $_POST["wproto_attached_images"] ) ) {
				
				update_post_meta( $post_id, "wproto_attached_images", $_POST["wproto_attached_images"] );
				
			} else {
				update_post_meta( $post_id, "wproto_attached_images", '' );
			}
			
		}
		
	}
	
	/**
	 * AJAX - Change post status
	 **/
	function ajax_change_post_status() {
		
		$response = array();
		
		if ( current_user_can( 'edit_pages' ) ):
		
			$post_id = absint( $_POST['post_id'] );
		
			if( $_POST['post_status'] == 'sticky' ) {
			
				wpl_galaxy_wp_utils::make_post_sticky( $_POST['post_id'], is_sticky( $post_id ) ? false : true );
			
			}
		
			if( $_POST['post_status'] == 'featured' ) {
			
				if( get_post_meta( $post_id, 'featured', true ) == 'yes' ) {
					// make post default
					update_post_meta( $post_id, 'featured', 'no' );
				} else {
					// make post featured
					update_post_meta( $post_id, 'featured', 'yes' );
				}
			
			}
		
		endif;
		
		die( json_encode( $response ) );
		
	}
	
}