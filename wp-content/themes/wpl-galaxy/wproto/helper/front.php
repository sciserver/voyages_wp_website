<?php

class wpl_galaxy_wp_front {

	/**
	 * Theme header
	 **/
	public static function head() {
		global $wpl_galaxy_wp;
				
		$stylesheet_dir = get_stylesheet_directory_uri();
				
		$favicon = wpl_galaxy_wp_utils::is_retina() ? $wpl_galaxy_wp->get_option( 'favicon_2x', 'general' ) : $wpl_galaxy_wp->get_option( 'favicon', 'general' );
		
		$apple_touch_57 = $wpl_galaxy_wp->get_option( 'apple_touch_icon_57x57', 'general' );
		$apple_touch_114 = $wpl_galaxy_wp->get_option( 'apple_touch_icon_114x114', 'general' );
		$apple_touch_72 = $wpl_galaxy_wp->get_option( 'apple_touch_icon_72x72', 'general' );
		$apple_touch_144 = $wpl_galaxy_wp->get_option( 'apple_touch_icon_144x144', 'general' );
		?>

		<?php if( $favicon <> '' ): ?>
		<!-- Favicons -->
		<link rel="shortcut icon" href="<?php echo $favicon; ?>">
		<link rel="icon" href="<?php echo $favicon; ?>" type="image/x-icon">
		<?php endif; ?>
		
		<?php if( $apple_touch_57 <> '' ): ?>
		<!-- Standard iPhone --> 
		<link rel="apple-touch-icon" sizes="57x57" href="<?php echo $apple_touch_57; ?>" />
		<?php endif; ?>
		
		<?php if( $apple_touch_114 <> '' ): ?>
		<!-- Retina iPhone --> 
		<link rel="apple-touch-icon" sizes="114x114" href="<?php echo $apple_touch_114; ?>" />
		<?php endif; ?>
		
		<?php if( $apple_touch_72 <> '' ): ?>
		<!-- Standard iPad --> 
		<link rel="apple-touch-icon" sizes="72x72" href="<?php echo $apple_touch_72; ?>" />
		<?php endif; ?>
		
		<?php if( $apple_touch_144 <> '' ): ?>
		<!-- Retina iPad --> 
		<link rel="apple-touch-icon" sizes="144x144" href="<?php echo $apple_touch_144; ?>" />
		<?php endif; ?>
		
		<?php
			$custom_css = trim( $wpl_galaxy_wp->get_option( 'custom_css', 'general' ) );
			if( $custom_css <> '' ):
		?>
		<style type="text/css">
			<?php echo $custom_css; ?>
		</style>
		<?php endif; ?>

		<!-- THEME FONTS, PRIMARY AND SECONDARY -->
		<?php if( defined( 'WPROTO_DEMO_STAND' ) && WPROTO_DEMO_STAND ): ?>

		<link href="http://fonts.googleapis.com/css?family=Pacifico|Roboto:300,400,700|Roboto+Slab:300,400,700" rel="stylesheet" type="text/css" />		
		<link rel="stylesheet" id="wproto-main-stylesheet" title="blue" href="<?php echo $stylesheet_dir; ?>/css/skin-blue.css" type="text/css" media="all" />
		<link rel="alternate stylesheet" title="brown" href="<?php echo $stylesheet_dir; ?>/css/skin-brown.css" type="text/css" media="all" />
		<link rel="alternate stylesheet" title="dark-green" href="<?php echo $stylesheet_dir; ?>/css/skin-dark-green.css" type="text/css" media="all" />
		<link rel="alternate stylesheet" title="gray" href="<?php echo $stylesheet_dir; ?>/css/skin-gray.css" type="text/css" media="all" />
		<link rel="alternate stylesheet" title="light-green" href="<?php echo $stylesheet_dir; ?>/css/skin-light-green.css" type="text/css" media="all" />
		<link rel="alternate stylesheet" title="orange" href="<?php echo $stylesheet_dir; ?>/css/skin-orange.css" type="text/css" media="all" />
		<link rel="alternate stylesheet" title="pink" href="<?php echo $stylesheet_dir; ?>/css/skin-pink.css" type="text/css" media="all" />
		<link rel="alternate stylesheet" title="purple" href="<?php echo $stylesheet_dir; ?>/css/skin-purple.css" type="text/css" media="all" />
		<link rel="alternate stylesheet" title="red" href="<?php echo $stylesheet_dir; ?>/css/skin-red.css" type="text/css" media="all" />
		<link rel="alternate stylesheet" title="sky-blue" href="<?php echo $stylesheet_dir; ?>/css/skin-sky-blue.css" type="text/css" media="all" />
		
		<?php else: ?>
		
			<?php
				$primary_font = get_theme_mod( 'wproto_primary_font', 'Roboto' );
				$secondary_font = get_theme_mod( 'wproto_secondary_font', 'Roboto Slab' );
				
				$custom_bg_color = get_theme_mod( 'wproto_bg_color', '' );
				
				$custom_background = get_theme_mod( 'wproto_boxed_background', '' );
				$custom_mega_menu = get_theme_mod( 'wproto_mega_menu_style', '' );
			?>
		
			<link href="http://fonts.googleapis.com/css?family=Pacifico|<?php echo urlencode($primary_font); ?>:300,400,700|<?php echo urlencode($secondary_font); ?>:300,400,700" rel="stylesheet" type="text/css" />
			<!-- MAIN THEME CSS -->
			<link id="wproto-main-stylesheet" href="<?php echo WPROTO_THEME_URL . '/css/' . get_theme_mod( 'wproto_color_scheme', 'skin-blue' ) . '.css'; ?>" rel="stylesheet" type="text/css" media="all" />
		
			<?php if( $primary_font != 'Roboto' || $secondary_font != 'Roboto Slab' ): ?>
			
				<style type="text/css">
					<?php echo self::parse_custom_fonts( $primary_font, $secondary_font ); ?>
				</style>
			
			<?php endif; ?>
			
			<?php if( $custom_background <> '' || $custom_bg_color <> '' ): ?>
				<style type="text/css">
					body {
						background: <?php if( $custom_bg_color <> '' ): echo $custom_bg_color; endif; ?> <?php if( $custom_background <> ''): ?> url(<?php echo $custom_background; ?>) <?php echo get_theme_mod( 'wproto_boxed_background_position', '' ); ?> <?php echo get_theme_mod( 'wproto_boxed_background_repeat', '' ); ?> <?php echo get_theme_mod( 'wproto_boxed_background_fixed', '' ); ?> <?php endif; ?> !important;
					}
				</style>
			<?php endif; ?>
			
			<?php if( $custom_mega_menu == 'relative' ): ?>
				<style type="text/css">
					#header-menu #header-menu-ul>li.mega-menu {
						position: relative !important;
					}
					#header-menu #header-menu-ul>li:hover .wproto-mega-menu-content {
						left: auto !important;
						right: 0 !important;
					}
				</style>
			<?php endif; ?>
		
		<?php endif; ?>
		<link rel="stylesheet/less" type="text/css" href="<?php echo $stylesheet_dir; ?>/css/less/font_switcher.less" />
		<link rel="stylesheet" id="main-stylesheet" href="<?php echo get_stylesheet_uri(); ?>" type="text/css" media="all" />
		<?php
	}
	
	/**
	 * Parse custom fonts file
	 **/
	public static function parse_custom_fonts( $primary_font, $secondary_font ) {
		return str_replace( '@font_secondary', $secondary_font, str_replace( '@font_primary', $primary_font, file_get_contents( WPROTO_THEME_DIR . '/css/less/font_switcher.less' ) ) );
	}
	
	/**
	 * Slider
	 **/
	public static function slider( $position = 'page_header' ) {
		global $wpl_galaxy_wp;
		
		if( (function_exists('is_shop') && is_shop()) || ( function_exists('is_product_category') && is_product_category()) || is_post_type_archive('product') ) {
			$post = get_post( woocommerce_get_page_id( 'shop' ) );
		} else {
			global $post;
		}
		
		if( wpl_galaxy_wp_utils::isset_layerslider() && isset( $post->ID ) && $post->ID > 0 ):
		
			$page_settings = $wpl_galaxy_wp->model->post->get_post_custom( $post->ID );
			
			if( isset( $page_settings->wproto_slider_show ) && $page_settings->wproto_slider_show == 'yes' ):
			
				if( isset( $page_settings->wproto_slider_position ) && $page_settings->wproto_slider_position != $position ) return false;
				
				$slideshow_id = isset( $page_settings->wproto_slider_id ) ? absint( $page_settings->wproto_slider_id ) : 0;
				
				// section after slider
				$display_section_after_slider = isset( $page_settings->wproto_display_text_after_slider ) ? $page_settings->wproto_display_text_after_slider : 'no';
				$section_text = isset( $page_settings->wproto_header_after_slider ) ? $page_settings->wproto_header_after_slider : '';
				$section_subtext = isset( $page_settings->wproto_subheader_after_slider ) ? $page_settings->wproto_subheader_after_slider : '';
				$section_button_link = isset( $page_settings->wproto_display_button_after_slider_link ) ? $page_settings->wproto_display_button_after_slider_link : '';
				$section_button_text = isset( $page_settings->wproto_display_button_after_slider_text ) ? $page_settings->wproto_display_button_after_slider_text : '';
				$section_button_at_new_window = isset( $page_settings->wproto_display_button_after_slider_at_new ) ? $page_settings->wproto_display_button_after_slider_at_new : 'no';
				$section_display_button = isset( $page_settings->wproto_display_button_after_slider ) ? $page_settings->wproto_display_button_after_slider : 'no';
		
		?>
		
		<section class="slider">
			<?php echo do_shortcode( '[layerslider id="' . $slideshow_id . '"]' ); ?>
		</section>
			
			<?php if( $display_section_after_slider == 'yes' && $position == 'page_header' ): ?>
			<section class="take-tour">
			
				<div class="wrapper">
			
					<div class="grid">
				
						<div class="unit whole">
			
							<?php if( $section_display_button == 'yes' ): ?>
							<a href="<?php echo $section_button_link; ?>" <?php echo $section_button_at_new_window == 'yes' ? 'target="_blank"' : ''; ?> class="button pull-right"><?php echo $section_button_text; ?></a>
							<?php endif; ?>
							<?php if( $section_text <> '' ): ?>
							<h4><?php echo $section_text; ?></h4>
							<?php endif; ?>
							<?php if( $section_subtext <> '' ): ?>
							<p><?php echo $section_subtext; ?></p>
							<?php endif; ?>
						
						</div>
					
					</div>
				
				</div>
			
			</section>
			<?php endif; ?>
			
		<?php
		
			endif;
			
		endif;
		
	}
	
	/**
	 * Post thumbnail
	 **/
	public static function thumbnail( $id, $size, $type = 'default' ) {
		global $wpl_galaxy_wp;
		$id = absint( $id );
		
		switch( $type ) {
			
			default:
			case 'default':
			
				$thumb_size = wpl_galaxy_wp_utils::is_retina() ? $size . '-2x' : $size;
				$image = wp_get_attachment_image_src( get_post_thumbnail_id( $id ), $thumb_size );
				if( isset( $image[0] ) )
					echo '<a href="' . get_permalink( $id ) . '"><img src="' . $image[0] . '" alt="" /></a>';
			
			break;
			case 'single':
			
				$page_settings = $wpl_galaxy_wp->model->post->get_post_custom( $id );
				$do_not_display_thumb = isset( $page_settings->wproto_post_hide_featured_image ) ? $page_settings->wproto_post_hide_featured_image : 'no';
			
				if( has_post_thumbnail() && $do_not_display_thumb != 'yes' ) {
					$thumb_size = wpl_galaxy_wp_utils::is_retina() ? $size . '-2x' : $size;
					echo '<div class="single-post-thumb">';
					the_post_thumbnail( $thumb_size );
					echo '</div>';
				}
			
			break;
			
		}
		
	}
	
	/**
	 * Theme footer
	 **/
	public static function footer() {
		global $wpl_galaxy_wp;
		
		if( defined( 'WPROTO_DEMO_STAND' ) && WPROTO_DEMO_STAND ):
		?>
		<!--
	
			STYLE SWITCHER
		
		-->
		<a href="http://themeforest.net/user/wplab/portfolio/?ref=wplab" id="buy-theme-link"></a>
		<a href="javascript:;" id="style-switcher-opener"><i class="fa fa-cog"></i> <span class="text"></span></a>
		<div id="style-switcher">
		
			<div class="switcher-elements">
				<div class="inside">
					<div class="item">
			
						<a href="javascript:;" class="toggle"><?php _e( 'Color Schemes', 'wproto' ); ?> <i></i></a>
				
						<div class="inside">
					
							<div class="colors" id="skin-switcher">
					
								<a href="javascript:;" data-skin="blue" class="blue current"><i class="fa fa-check"></i></a>
								<a href="javascript:;" data-skin="light-green" class="light-green"><i class="fa fa-check"></i></a>
								<a href="javascript:;" data-skin="dark-green" class="dark-green"><i class="fa fa-check"></i></a>
								<a href="javascript:;" data-skin="gray" class="gray"><i class="fa fa-check"></i></a>
								<a href="javascript:;" data-skin="red" class="red"><i class="fa fa-check"></i></a>
								<a href="javascript:;" data-skin="orange" class="orange"><i class="fa fa-check"></i></a>
								<a href="javascript:;" data-skin="sky-blue" class="sky-blue"><i class="fa fa-check"></i></a>
								<a href="javascript:;" data-skin="purple" class="purple"><i class="fa fa-check"></i></a>
								<a href="javascript:;" data-skin="pink" class="pink"><i class="fa fa-check"></i></a>
								<a href="javascript:;" data-skin="brown" class="brown"><i class="fa fa-check"></i></a>
					
							</div>
					
						</div>
			
					</div>
			
					<div class="item">
			
						<a href="javascript:;" class="toggle"><?php _e( 'Boxed layout', 'wproto' ); ?> <i></i></a>
						
						<div class="inside">
					
							<div class="row" id="switcher-boxed-layout">
								<label class="inline-label"><input type="radio" value="yes" name="boxed_layout" /> <?php _e( 'Yes', 'wproto' ); ?></label>
					
								<label class="inline-label"><input type="radio" value="no" name="boxed_layout" checked="checked" /> <?php _e( 'No', 'wproto' ); ?></label>
							</div>
					
							<div class="row" id="switcher-background">
								<label class="block-label"><?php _e( 'Background', 'wproto' ); ?>:</label>
								<select id="switcher-background-selector">
									<option value=""><?php _e( 'Choose background', 'wproto' ); ?>...</option>
									<option value="background-1"><?php _e( 'Background 1', 'wproto' ); ?></option>
									<option value="background-2"><?php _e( 'Background 2', 'wproto' ); ?></option>
									<option value="background-3"><?php _e( 'Background 3', 'wproto' ); ?></option>
									<option value="background-4"><?php _e( 'Background 4', 'wproto' ); ?></option>
								</select>
							</div> 
					
							<div class="row" id="switcher-pattern">
								<label class="block-label"><?php _e( 'Pattern', 'wproto' ); ?>:</label>
								<select id="switcher-pattern-selector">
									<option value=""><?php _e( 'Choose pattern', 'wproto' ); ?>...</option>
									<option value="pattern-1"><?php _e( 'Carbon fibre', 'wproto' ); ?></option>
									<option value="pattern-2"><?php _e( 'Cubes', 'wproto' ); ?></option>
									<option value="pattern-3"><?php _e( 'Escheresque', 'wproto' ); ?></option>
									<option value="pattern-4"><?php _e( 'Fabric of squares', 'wproto' ); ?></option>
									<option value="pattern-5"><?php _e( 'Gray wash wall', 'wproto' ); ?></option>
									<option value="pattern-6"><?php _e( 'Random grey variations', 'wproto' ); ?></option>
									<option value="pattern-7"><?php _e( 'Wood', 'wproto' ); ?></option>
									<option value="pattern-8"><?php _e( 'Material', 'wproto' ); ?></option>
									<option value="pattern-9"><?php _e( 'Tileable wood', 'wproto' ); ?></option>
									<option value="pattern-10"><?php _e( 'Tweed', 'wproto' ); ?></option>
								</select>
							</div> 
					
						</div>
			
					</div>
			
					<div class="item">
			
						<a href="javascript:;" class="toggle"><?php _e( 'Header top menu', 'wproto' ); ?> <i></i></a>
				
						<div class="inside">
							<div class="row" id="switcher-header-top-menu">
								<label class="inline-label"><input type="radio" value="yes" name="header_top_menu" checked="checked" /> <?php _e( 'On', 'wproto' ); ?></label>
					
								<label class="inline-label"><input type="radio" value="no" name="header_top_menu" /> <?php _e( 'Off', 'wproto' ); ?></label>
							</div>
						</div>
			
					</div>
		
					<div class="item">
			
						<a href="javascript:;" class="toggle"><?php _e( 'Header layouts', 'wproto' ); ?> <i></i></a>
				
						<div class="inside" id="switcher-header-layout">
							<label class="row block-label">
								<input type="radio" name="header_layout" value="header-default" checked="checked" /> <?php _e( 'Default', 'wproto' ); ?>
							</label>
							<label class="row block-label">
								<input type="radio" name="header_layout" value="header-default-centered" /> <?php _e( 'Default centered', 'wproto' ); ?>
							</label>
							<label class="row block-label">
								<input type="radio" name="header_layout" value="header-big-background" /> <?php _e( 'Big background', 'wproto' ); ?>
							</label>
							<label class="row block-label">
								<input type="radio" name="header_layout" value="header-classic" /> <?php _e( 'Classic', 'wproto' ); ?>
							</label>
							<label class="row block-label">
								<input type="radio" name="header_layout" value="header-classic-centered" /> <?php _e( 'Classic centered', 'wproto' ); ?>
							</label>
							<label class="row block-label">
								<input type="radio" name="header_layout" value="header-full-width" /> <?php _e( 'Full width', 'wproto' ); ?>
							</label>
						</div>
			
					</div>
			
					<div class="item">
			
						<a href="javascript:;" class="toggle"><?php _e( 'Fonts', 'wproto' ); ?> <i></i></a>
				
						<?php
							$fonts = wpl_galaxy_wp_utils::get_google_fonts();
						?>
				
						<div class="inside">
							<div class="row" id="switcher-primary-font">
								<label class="block-label"><?php _e( 'Primary font', 'wproto' ); ?>:</label>
								<select id="switcher-primary-font-selector">
									<?php foreach( $fonts as $name=>$title ): ?>
									<option value="<?php echo $name; ?>"><?php echo $title; ?></option>
									<?php endforeach; ?>
								</select>
							</div> 
					
							<div class="row" id="switcher-secondary-font">
								<label class="block-label"><?php _e( 'Secondary', 'wproto' ); ?>:</label>
								<select id="switcher-secondary-font-selector">
									<?php foreach( $fonts as $name=>$title ): ?>
									<option value="<?php echo $name; ?>"><?php echo $title; ?></option>
									<?php endforeach; ?>
								</select>
							</div> 
					
						</div>
			
					</div>
			
					<div class="row last">
						<a href="javascript:;" id="switcher-reset-styles" class="button"><?php _e( 'Reset styles', 'wproto' ); ?></a>
					</div>
		
				</div>
		
			</div>
		
		</div>
		<?php
		endif;
	}
	
	/**
	 * Print content section classes
	 **/
	public static function content_classes() {
		global $wpl_galaxy_wp, $post;
		
		$classes_string = 'unit three-quarters';
		
		if( is_single() || is_page() ) {
			
			$page_settings = $wpl_galaxy_wp->model->post->get_post_custom( $post->ID );
			
			if( !isset( $page_settings->wproto_page_sidebar ) || $page_settings->wproto_page_sidebar == 'none' ) {
				$classes_string = 'unit whole';
			}
		}
		
		echo $classes_string;
	}
	
	/**
	 * Echo post header
	 **/
	public static function post_header() {
		global $wpl_galaxy_wp, $post, $wp_query;
		
		if( is_single() && get_post_type($post) == 'product' ) {
			global $product;
			$sku = $product->get_sku();
			
			$page_settings = $wpl_galaxy_wp->model->post->get_post_custom( $post->ID );
			if( !isset( $page_settings->wproto_post_hide_title ) || $page_settings->wproto_post_hide_title != 'yes' ):
			
			?>
			<header class="post-header">
				<h1 class="post-title"><?php the_title(); ?><?php if( $sku <> '' ): echo ' <span class="sku">' . __('SKU', 'wproto') . ': ' . $sku . '</span>'; endif; ?></h1>
				<?php do_action('woocommerce_before_main_content'); ?>
			</header>
			<?php
			endif;
			
		} elseif ( is_single() || is_page() ) {
			$page_settings = $wpl_galaxy_wp->model->post->get_post_custom( $post->ID );
			if( !isset( $page_settings->wproto_post_hide_title ) || $page_settings->wproto_post_hide_title != 'yes' ):
			?>
			<header class="post-header">
				<h1 class="post-title"><?php the_title(); ?><?php $cat_item_sku = get_post_meta( $post->ID, 'sku', true ); if( get_post_type() == 'wproto_catalog' && $cat_item_sku <> '' ): echo ' <span class="sku">' . __('SKU', 'wproto') . ': ' . $cat_item_sku . '</span>'; endif; ?></h1>
				<?php wpl_galaxy_wp_front::breadcrumbs( true, ' <i class="delimeter"></i> ', true ); ?>
			</header>
			<?php
			endif;
		}
		
	}
	
	/**
	 * Get page sidebar
	 **/
	public static function get_sidebar() {
		global $wpl_galaxy_wp, $post;
		
		$sidebar_name = 'sidebar-right';
		$sidebar_enabled = 'yes';
		$sidebar_type = 'right';
		
		if( is_single() || is_page() ) {			
			$page_settings = $wpl_galaxy_wp->model->post->get_post_custom( $post->ID );
			
			$sidebar_enabled = isset( $page_settings->wproto_page_sidebar ) && $page_settings->wproto_page_sidebar != 'none' ? 'yes' : 'no';
			$sidebar_type = isset( $page_settings->wproto_page_sidebar ) ? $page_settings->wproto_page_sidebar : 'right';
			$sidebar_name = isset( $page_settings->wproto_page_sidebar_id ) ? $page_settings->wproto_page_sidebar_id : 'sidebar-right';
			
		}
		
		if( is_post_type_archive('product') || (function_exists('is_product_category') && is_product_category()) ) {
			$sidebar_enabled = 'yes';
			$sidebar_name = 'shop';
		}
		
		if( $sidebar_enabled == 'yes' ) {
			echo '<aside class="wproto-page-sidebar unit one-quarter sidebar sidebar-' . $sidebar_type . '">';
			
			do_action('woocommerce_sidebar');
			
			dynamic_sidebar( $sidebar_name );
			echo '</aside>';
		}   
	
	}
	
	/**
	 * Widgetized footer
	 **/
	public static function widgetized_footer() {
		global $wpl_galaxy_wp, $post;
		
		$footer_sidebar = 'sidebar-footer';
		$sidebar_enabled = 'yes';
		
		if( is_single() || is_page() ) {
			
			$page_settings = $wpl_galaxy_wp->model->post->get_post_custom( $post->ID );
			
			$page_tpl = get_post_meta( $post->ID, '_wp_page_template', true );
			
			if( $page_tpl == 'page-tpl-one-page.php' ) {
				$sidebar_enabled = isset( $page_settings->wproto_onepage_widgetized_footer ) ? $page_settings->wproto_onepage_widgetized_footer : 'no';
				$footer_sidebar = isset( $page_settings->wproto_onepage_footer_sidebar_id ) ? $page_settings->wproto_onepage_footer_sidebar_id : 'sidebar-footer';
			} else {
				$sidebar_enabled = isset( $page_settings->wproto_widgetized_footer ) ? $page_settings->wproto_widgetized_footer : 'yes';
				$footer_sidebar = isset( $page_settings->wproto_page_footer_sidebar_id ) ? $page_settings->wproto_page_footer_sidebar_id : 'sidebar-footer';		
			}
		
		}
		
		if( $sidebar_enabled == 'yes' ) {
			echo '<div class="wrapper grid">';
			dynamic_sidebar( $footer_sidebar );
			echo '</div>';
		}   
	}

	/**
	 * Theme logo
	 **/
	public static function logo() {
		global $wpl_galaxy_wp;

		$header_logo = $wpl_galaxy_wp->get_option( 'header_logo', 'general' );
		$logo_type = $wpl_galaxy_wp->get_option( 'logo_type', 'general' );
		$header_logo = $header_logo != NULL ? $header_logo : 'image';
		$logo_type = $logo_type != NULL ? $logo_type : 'default';
					
		if( $header_logo == 'image' ):
			if( $logo_type == 'default' ):
		?>
			<a id="logo" <?php if( !is_front_page() ): ?> href="<?php echo site_url(); ?>"<?php endif; ?>><img src="<?php echo WPROTO_THEME_URL; ?>/images/logo<?php echo wpl_galaxy_wp_utils::is_retina() ? '@2x' : ''; ?>.png" width="187" alt="" /></a>
		<?php
			else:
			$custom_logo_url = $wpl_galaxy_wp->get_option( 'custom_logo_url', 'general' );
			$custom_logo_url_2x = $wpl_galaxy_wp->get_option( 'custom_logo_url_2x', 'general' );
			$custom_logo_image = wpl_galaxy_wp_utils::is_retina() ? $custom_logo_url_2x : $custom_logo_url;
			$size = getimagesize( $custom_logo_url );
		?>
			<a id="logo" <?php if( !is_front_page() ): ?> href="<?php echo site_url(); ?>"<?php endif; ?>><img width="<?php echo isset( $size[0] ) ? $size[0] : ''; ?>" src="<?php echo @$custom_logo_image; ?>" alt="" /></a>
		<?php
			endif;
		else:
		?>
			<div id="text-logo">
				<a <?php if( !is_front_page() ): ?> href="<?php echo site_url(); ?>"<?php endif; ?> class="site-title"><?php echo get_bloginfo('name'); ?></a>
				<div class="site-tagline"><?php echo get_bloginfo('description'); ?></div>
			</div>
		<?php
		endif;
	}
	
	/**
	 * Echo social icons from settings
	 **/
	public static function social_icons( $footer = false, $show_tooltip = true ) {
		global $wpl_galaxy_wp;

		$tooltip_gravity = $footer ? 'data-tip-gravity="s"' : '';
		$show_tooltip_class = $show_tooltip ? 'show-tooltip' : '';

		$dribble_url = $wpl_galaxy_wp->get_option( 'dribble_url', 'general' );
		echo $dribble_url != NULL && $dribble_url <> '' ? '<a href="' . $dribble_url . '"><i ' . $tooltip_gravity . ' title="Dribbble" class="fa fa-dribbble ' . $show_tooltip_class . '"></i></a>' : '';
		
		$facebook_url = $wpl_galaxy_wp->get_option( 'facebook_url', 'general' );
		echo $facebook_url != NULL && $facebook_url <> '' ? '<a href="' . $facebook_url . '"><i ' . $tooltip_gravity . ' title="Facebook" class="fa fa-facebook-square ' . $show_tooltip_class . '"></i></a>' : '';
		
		$flickr_url = $wpl_galaxy_wp->get_option( 'flickr_url', 'general' );
		echo $flickr_url != NULL && $flickr_url <> '' ? '<a href="' . $flickr_url . '"><i ' . $tooltip_gravity . ' title="Flickr" class="fa fa-flickr ' . $show_tooltip_class . '"></i></a>' : '';
		
		$google_url = $wpl_galaxy_wp->get_option( 'google_url', 'general' );
		echo $google_url != NULL && $google_url <> '' ? '<a href="' . $google_url . '"><i ' . $tooltip_gravity . ' title="Google Plus" class="fa fa-google-plus-square ' . $show_tooltip_class . '"></i></a>' : '';
		
		$linkedin_url = $wpl_galaxy_wp->get_option( 'linkedin_url', 'general' );
		echo $linkedin_url != NULL && $linkedin_url <> '' ? '<a href="' . $linkedin_url . '"><i ' . $tooltip_gravity . ' title="LinkedIn" class="fa fa-linkedin ' . $show_tooltip_class . '"></i></a>' : '';
		
		$tumblr_url = $wpl_galaxy_wp->get_option( 'tumblr_url', 'general' );
		echo $tumblr_url != NULL && $tumblr_url <> '' ? '<a href="' . $tumblr_url . '"><i ' . $tooltip_gravity . ' title="Tumblr" class="fa fa-tumblr ' . $show_tooltip_class . '"></i></a>' : '';
		
		$twitter_url = $wpl_galaxy_wp->get_option( 'twitter_url', 'general' );
		echo $twitter_url != NULL && $twitter_url <> '' ? '<a href="' . $twitter_url . '"><i ' . $tooltip_gravity . ' title="Twitter" class="fa fa-twitter-square ' . $show_tooltip_class . '"></i></a>' : '';
		
		$youtube_url = $wpl_galaxy_wp->get_option( 'youtube_url', 'general' );
		echo $youtube_url != NULL && $youtube_url <> '' ? '<a href="' . $youtube_url . '"><i ' . $tooltip_gravity . ' title="YouTube" class="fa fa-youtube-square ' . $show_tooltip_class . '"></i></a>' : '';
		
		$instagram_url = $wpl_galaxy_wp->get_option( 'instagram_url', 'general' );
		echo $instagram_url != NULL && $instagram_url <> '' ? '<a href="' . $instagram_url . '"><i ' . $tooltip_gravity . ' title="Instagram" class="fa fa-instagram ' . $show_tooltip_class . '"></i></a>' : '';
		
		$pinterest_url = $wpl_galaxy_wp->get_option( 'pinterest_url', 'general' );
		echo $pinterest_url != NULL && $pinterest_url <> '' ? '<a href="' . $pinterest_url . '"><i ' . $tooltip_gravity . ' title="Pinterest" class="fa fa-pinterest-square ' . $show_tooltip_class . '"></i></a>' : '';
		
	}
	
	/**
	 * Display post likes
	 **/
	public static function likes( $id, $type = 'post', $only_display = FALSE ) {
		global $wpl_galaxy_wp;
		$id = absint( $id );
		
		if( $type == 'comment' ) {
			$likes_enabled = $wpl_galaxy_wp->get_option( 'likes_on_comments', 'general' );
			$likes_count = absint( get_comment_meta( $id, 'wproto_likes', true) );
		} else {
			$likes_enabled = $wpl_galaxy_wp->get_option( 'likes_on_posts', 'general' );
			$likes_count = absint( get_post_meta( $id, 'wproto_likes', true) );
		}

		if( $likes_enabled == 'yes' ):
		
		?>
		
			<?php if( $wpl_galaxy_wp->controller->front->is_already_voted( $id, $type ) || $only_display == true ): ?>
				<span><i class="fa fa-heart"></i> <span class="views"><?php echo $likes_count; ?></span></span>
			<?php else: ?>
				<a href="javascript:;" data-type="<?php echo $type; ?>" data-id="<?php echo $id; ?>" title="<?php _e('Click to like this post', 'wproto'); ?>" class="wproto-like"><span class="views"></span> <span class="title"><?php _e('Like', 'wproto'); ?></span> <i class="fa fa-heart"></i></a> 																	
			<?php endif; ?>
			
		<?php
		endif; 
	}
	
	/**
	 * Display post views
	 **/
	public static function views( $id ) {
		global $wpl_galaxy_wp;
		$id = absint( $id );
		
		$views = get_post_meta( $id, 'wproto_views', true );
		?>
		<span><i class="fa fa-eye"></i> <span class="views"><?php echo $views; ?></span></span>
		<?php
		
	}
	
	public static function get_categories( $separator = ', ' ) {
		
		$post_type = get_post_type();
		
		switch( $post_type ) {
			default:
			case 'post':
				return wpl_galaxy_wp_front::get_valid_category_list( $separator );
			break;
			case 'wproto_catalog':
				return get_the_term_list( get_the_ID(), 'wproto_catalog_category', '', $separator, '' );
			break;
			case 'wproto_photoalbums':
				return get_the_term_list( get_the_ID(), 'wproto_photoalbums_category', '', $separator, '' );
			break;
			case 'wproto_video':
				return get_the_term_list( get_the_ID(), 'wproto_video_category', '', $separator, '' );
			break;
			case 'wproto_portfolio':
				return get_the_term_list( get_the_ID(), 'wproto_portfolio_category', '', $separator, '' );
			break;
		}
		
	}
	
	public static function get_valid_category_list( $separator = ', ' ) {
		$s = str_replace( ' rel="category"', '', get_the_category_list( $separator ) );
		$s = str_replace( ' rel="category tag"', '', $s );
		return $s;
	}
	
	public static function get_valid_tags_list( $separator = ', ' ) {
		$s = str_replace( ' rel="tag"', '', get_the_tag_list( '', $separator, '' ) );
		return $s;
	}
	
	/**
	 * Show breadcrumbs
	 **/
	public static function breadcrumbs( $showOnHome = 1, $delimiter = '<span class="delimeter">&raquo;</span>', $showCurrent = 1, $before = '<span class="current">', $after = '</span>' ) {
  	global $post, $wp_query, $wpl_galaxy_wp;
  	
  	$breadcrumbs_enabled = $wpl_galaxy_wp->get_option( 'display_breadcrumbs' );
  	if( $breadcrumbs_enabled != 'yes' ) {
  		return false;
  	}
  	
		$home = __( 'Home', 'wproto' ); // text for the 'Home' link
  	$blog = __( 'Blog', 'wproto' ); // text for the 'Blog' link
  	$shop = __( 'Shop', 'wproto' ); 
  	
  	$page_for_posts = get_option( 'page_for_posts' );
		$page_for_posts = $page_for_posts > 0 ? get_permalink( $page_for_posts ) : site_url(); 
  
  	$homeLink = home_url() . '/';

		if ( is_front_page() ) {
			
			if ( $showOnHome == 1 ) echo '<div class="breadcrumbs" id="crumbs">' . $home;
			
		} elseif( is_home() ) {
			
			if ( $showOnHome == 1 ) echo '<div class="breadcrumbs" id="crumbs"><a href="' . $homeLink . '">' . $home . '</a> ' . $delimiter . ' ' . $blog;
			
		} else {

			echo '<div class="breadcrumbs" id="crumbs"><a href="' . $homeLink . '">' . $home . '</a> ' . $delimiter . ' ';

		}

		if ( is_category() ) {
  		
			echo '<a href="' . $page_for_posts . '">' . $blog . '</a>' . $delimiter;
		    
			$thisCat = get_category( get_query_var( 'cat' ), false );
			if ( $thisCat->parent != 0 ) echo get_category_parents( $thisCat->parent, TRUE, ' ' . $delimiter . ' ' );
			echo $before . __( 'Category', 'wproto') . ' "' . single_cat_title( '', false ) . '"' . $after;
  
		} elseif ( is_search() ) {
    		
			echo '<a href="' . $page_for_posts . '">' . $blog . '</a>' . $delimiter;
			echo $before . __( 'Search results for','wproto' ) . ' "' . get_search_query() . '"' . $after;

		} elseif ( is_day() ) {

			echo '<a href="' . $page_for_posts . '">' . $blog . '</a>' . $delimiter;
			echo '<a href="' . get_year_link( get_the_time( 'Y' ) ) . '">' . get_the_time( 'Y' ) . '</a> ' . $delimiter . ' ';
			echo '<a href="' . get_month_link( get_the_time( 'Y' ),get_the_time( 'm' ) ) . '">' . get_the_time( 'F' ) . '</a> ' . $delimiter . ' ';
			echo $before . get_the_time('d') . $after;
  
		} elseif ( is_month() ) {

			echo '<a href="' . $page_for_posts . '">' . $blog . '</a>' . $delimiter;
			echo '<a href="' . get_year_link( get_the_time( 'Y' )) . '">' . get_the_time( 'Y' ) . '</a> ' . $delimiter . ' ';
			echo $before . get_the_time( 'F' ) . $after;
  
		} elseif ( is_year() ) {

			echo '<a href="' . $page_for_posts . '">' . $blog . '</a>' . $delimiter;
			echo $before . get_the_time( 'Y' ) . $after;

		} elseif ( is_single() && !is_attachment() ) {
  			
			if ( get_post_type() != 'post' && get_post_type() != 'product' ) {
				$post_type = get_post_type_object(get_post_type());
				$slug = $post_type->rewrite;
				echo '<a href="' . $homeLink . $slug['slug'] . '/">' . $post_type->labels->name . '</a>';
				if ($showCurrent == 1) echo ' ' . $delimiter . ' ' . $before . get_the_title() . $after;
			} elseif( get_post_type() == 'product' && wpl_galaxy_wp_utils::isset_woocommerce() ) {

				echo '<a href="' . get_permalink( woocommerce_get_page_id( 'shop' ) )  . '">' . $shop .  '</a>' . $delimiter . get_the_title();

			} else {

				echo '<a href="' . $page_for_posts . '">' . $blog . '</a>' . $delimiter;

				$cat = get_the_category();
				$cat = $cat[0];
				$cats = get_category_parents( $cat, TRUE, ' ' . $delimiter . ' ');
				
				if ( !is_wp_error( $cats ) ) {
					if ( $showCurrent == 0 ) $cats = preg_replace( "#^(.+)\s$delimiter\s$#", "$1", $cats );
					echo $cats;
				}
				
				if ($showCurrent == 1) echo $before . get_the_title() . $after;

			}

		} elseif ( !is_single() && !is_page() && get_post_type() != 'post' && !is_404() ) {
			$post_type = get_post_type_object( get_query_var( 'post_type' ) );
			
			$label_name = isset( $post_type->labels->name ) ? $post_type->labels->name : '';
			
			$label = get_query_var( 'post_type' ) == 'product' ? $shop : $label_name;
			echo $before . $label . $after;

		} elseif ( is_attachment() ) {
			
			$parent = get_post( $post->post_parent );
			$cat = get_the_category( $parent->ID );
			$cat = isset( $cat[0] ) ? $cat[0] : 0;
			if( $cat > 0 ) {
				echo get_category_parents( $cat, TRUE, ' ' . $delimiter . ' ' );
				echo '<a href="' . get_permalink( $parent ) . '">' . $parent->post_title . '</a>';
			} else {
				_e( 'Attachment', 'wproto' );
			}

			if ($showCurrent == 1) echo ' ' . $delimiter . ' ' . $before . get_the_title() . $after;
  
		} elseif ( is_page() && !$post->post_parent ) {
			if ( $showCurrent == 1 ) echo $before . get_the_title() . $after;
		} elseif ( is_page() && $post->post_parent ) {
			$parent_id  = $post->post_parent;
			$breadcrumbs = array();
			while ( $parent_id ) {
				$page = get_page( $parent_id );
				$breadcrumbs[] = '<a href="' . get_permalink( $page->ID ) . '">' . get_the_title( $page->ID ) . '</a>';
				$parent_id  = $page->post_parent;
			}
			$breadcrumbs = array_reverse( $breadcrumbs );
			for ($i = 0; $i < count( $breadcrumbs ); $i++) {
				echo $breadcrumbs[$i];
				if ($i != count( $breadcrumbs ) -1 ) echo ' ' . $delimiter . ' ';
			}
			if ($showCurrent == 1) echo ' ' . $delimiter . ' ' . $before . get_the_title() . $after;
  
		} elseif ( is_tag() ) {
			echo $before . __( 'Posts tagged', 'wproto' ) . ' "' . single_tag_title( '', false ) . '"' . $after;
  
		} elseif ( is_author() ) {
			global $author;
			$userdata = get_userdata( $author );
			echo $before . __( 'Articles posted by', 'wproto' ) . ' ' . $userdata->display_name . $after;
  
		} elseif ( is_404() ) {
			echo $before . __( 'Error 404', 'wproto' ) . '' . $after;
		}
  
  	$tax = isset( $wp_query->query_vars['taxonomy'] ) ? $wp_query->query_vars['taxonomy'] : NULL;
  
		if( $tax != NULL ) {
			
			$taxonomy = get_taxonomy( $wp_query->query_vars['taxonomy'] );
			echo $before . $taxonomy->labels->name . $after;
			
		}
  
		if ( get_query_var( 'paged' ) ) {
			echo ' (';
			echo __( 'Page', 'wproto' ) . ' ' . get_query_var( 'paged' );
			echo ')';
		}

		echo '</div>'; 
	}
	
	/**
	 * Show pagination
	 **/
	public static function pagination( $pagination_style = 'numeric', $loop_template = 'one_column_grid', $post_type = '', $display_type = 'all' ) {
		global $paged, $post, $wp_query, $wpl_galaxy_wp;

		if( $wp_query->max_num_pages <= 1 ) return false;

		$permalinks_enabled = get_option('permalink_structure') != '';
		
		if( empty( $paged ) ) $paged = 1;
			
			switch( $pagination_style ) {
				
				default:
				case 'numeric':

					$format = $permalinks_enabled ? 'page/%#%' : '&paged=%#%';
					$base = $permalinks_enabled && !is_search() ? get_pagenum_link(1) .'%_%' : str_replace( 9999999, '%#%', esc_url( get_pagenum_link( 9999999 ) ) );
				
					echo '<div class="pagination">';
					
					if( is_search() ):
						_e( 'Go to page:', 'wproto');
					endif; 
					
					echo '<div class="numeric">';
					echo paginate_links( array(
						'format' => $format,
						'base' => $base,
						'current' => max( 1, get_query_var('paged') ),
						'total' => $wp_query->max_num_pages,
						'prev_text' => __('Previous', 'wproto'),
						'next_text' => __('Next', 'wproto'),
						'mid_size' => 1
					));
					
					echo '</div></div>';
				
				break;
				
				case 'text':
				
					echo '<div class="pagination text">';
					?>
						<div class="nav-previous alignleft"><?php next_posts_link( __( 'Older posts', 'wproto' ) ); ?></div>
						<div class="nav-next alignright"><?php previous_posts_link( __( 'Newer posts', 'wproto' ) ); ?></div>
						<div class="clear"></div>
					<?php
					echo '</div>';
				
				break;
				
				case 'ajax':
				
					if( $wp_query->max_num_pages <= $paged ) return '';
				
					$q_obj = $wp_query->get_queried_object();
				
					$tax = isset( $wp_query->tax_query->queries[0]['taxonomy'] ) ? $wp_query->tax_query->queries[0]['taxonomy'] : NULL;
					if( $tax != NULL ) $taxonomy = get_taxonomy( $tax );
					
					echo '<div class="pagination ajax">';
					?>
					
					<a href="javascript:;" data-author="<?php echo is_author() ? $q_obj->ID : ''; ?>" data-posts_per_page="<?php echo get_query_var('posts_per_page'); ?>" data-display_type="<?php echo $display_type; ?>" data-loop-template="<?php echo $loop_template; ?>" data-max-pages="<?php echo isset( $wp_query->max_num_pages ) ? $wp_query->max_num_pages : 1; ?>" data-current-page="<?php echo $paged; ?>" data-next-page="<?php echo $paged + 1; ?>" data-post-type="<?php echo $post_type; ?>" data-taxonomy-name="<?php echo isset( $taxonomy->name ) ? $taxonomy->name : ''; ?>" data-taxonomy-term="<?php echo isset( $wp_query->tax_query->queries[0]['terms'] ) ? implode(',', $wp_query->tax_query->queries[0]['terms']) : ''; ?>" data-search-string="<?php echo htmlspecialchars( get_query_var('s')); ?>" id="wproto-load-more-posts-link" class="button iconic"><i class="fa fa-spinner"></i> <?php _e( 'Load more posts', 'wproto' ); ?></a>
					<?php
					echo '</div>';
				
				break;
				
			}
		
	}
	/**
	 * Share post code
	 **/
	public static function share_post_code() {
		global $wpl_galaxy_wp, $post;
		$share_post_code = $wpl_galaxy_wp->get_option('shared_buttons_code');
		if( trim( $share_post_code ) <> '' ):
			?>
				<p class="share-post">
					<strong><?php _e('Share post', 'wproto'); ?>:</strong> 
					<?php echo $share_post_code; ?>
				</p>
			<?php
		else:
			$post_url = urlencode( get_permalink( $post ) );
			$post_title = urlencode( get_the_title() );
			$thumb_url = wp_get_attachment_image_src( get_post_thumbnail_id( $post->ID ), 'post-thumb-big' );
			?>
				<p class="share-post default-sharer">
					<strong><?php _e('Share post', 'wproto'); ?>:</strong> 
					<a target="_blank" href="http://pinterest.com/pin/create/button/?url=<?php echo $post_url; ?><?php if( isset( $thumb_url[0] ) ): ?>&amp;media=<?php echo $thumb_url[0]; endif; ?>&amp;description=<?php echo $post_title; ?>"><i data-tip-gravity="s" title="Pinterest" class="fa fa-pinterest-square show-tooltip"></i></a>
					<a target="_blank" href="http://www.facebook.com/sharer/sharer.php?u=<?php echo $post_url; ?>"><i data-tip-gravity="s" title="Facebook" class="fa fa-facebook-square show-tooltip"></i></a>
					<a target="_blank" href="https://www.linkedin.com/cws/share?url=<?php echo $post_url; ?>"><i data-tip-gravity="s" title="LinkedIn" class="fa fa-linkedin-square show-tooltip"></i></a>
					<a target="_blank" href="http://twitter.com/share?text=<?php echo $post_title; ?>&amp;url=<?php echo $post_url; ?>"><i data-tip-gravity="s" title="Twitter" class="fa fa-twitter-square show-tooltip"></i></a>
				</p>
			<?php
		endif;
	}
	
	/**
	 * Post author info block
	 **/
	public static function post_author_info() {
		global $wpl_galaxy_wp;
		$hide_authors_block = $wpl_galaxy_wp->get_option('hide_author_info');
		
		if( $hide_authors_block != 'yes' ):
									
			$author_id = get_the_author_meta( 'ID' );
			$avatar_size = wpl_galaxy_wp_utils::is_retina() ? 140 : 70;
			$author_description = get_the_author_meta( 'description' );
			?>
			<div class="author-info">
							
				<div class="avatar">
					<?php echo get_avatar( $author_id, $avatar_size ); ?>
				</div>
								
				<div class="text">
					<a class="author-title" href="<?php echo get_author_posts_url( $author_id ); ?>"><span><?php _e('About the author', 'wproto'); ?>:</span> <?php the_author_meta( 'display_name' ); ?></a>
					<?php if( $author_description <> '' ): ?>
					<p><?php echo $author_description; ?></p>
					<?php endif; ?>
					<div class="social-icons">
										
					<?php
						$author_dribbble_url = esc_attr( get_the_author_meta( 'wproto_social_dribbble_url', $author_id ) );
						$author_facebook_url = esc_attr( get_the_author_meta( 'wproto_social_facebook_url', $author_id ) );
						$author_flickr_url = esc_attr( get_the_author_meta( 'wproto_social_flickr_url', $author_id ) );
						$author_google_plus_url = esc_attr( get_the_author_meta( 'wproto_social_google_plus_url', $author_id ) );
						$author_linkedin_url = esc_attr( get_the_author_meta( 'wproto_social_linkedin_url', $author_id ) );
						$author_tumblr_url = esc_attr( get_the_author_meta( 'wproto_social_tumblr_url', $author_id ) );
						$author_twitter_url = esc_attr( get_the_author_meta( 'wproto_social_twitter_url', $author_id ) );
						$author_youtube_url = esc_attr( get_the_author_meta( 'wproto_social_youtube_url', $author_id ) );
					?>
					
					<?php if( $author_dribbble_url <> '' ): ?>
						<a href="<?php echo $author_dribbble_url; ?>"><i title="Dribbble" data-tip-gravity="s" class="fa fa-dribbble show-tooltip"></i></a>
					<?php endif; ?>
					
					<?php if( $author_facebook_url <> '' ): ?>
						<a href="<?php echo $author_facebook_url; ?>"><i title="Facebook" data-tip-gravity="s" class="fa fa-facebook-square show-tooltip"></i></a>
					<?php endif; ?>
					
					<?php if( $author_flickr_url <> '' ): ?>
						<a href="<?php echo $author_flickr_url; ?>"><i title="Flickr" data-tip-gravity="s" class="fa fa-flickr show-tooltip"></i></a>
					<?php endif; ?>
					
					<?php if( $author_google_plus_url <> '' ): ?>
						<a href="<?php echo $author_google_plus_url; ?>"><i title="Google Plus" data-tip-gravity="s" class="fa fa-google-plus-square show-tooltip"></i></a>
					<?php endif; ?>
					
					<?php if( $author_linkedin_url <> '' ): ?>
						<a href="<?php echo $author_linkedin_url; ?>"><i title="Linkedin" data-tip-gravity="s" class="fa fa-linkedin-square show-tooltip"></i></a>
					<?php endif; ?>
					
					<?php if( $author_tumblr_url <> '' ): ?>
						<a href="<?php echo $author_tumblr_url; ?>"><i title="Tumblr" data-tip-gravity="s" class="fa fa-tumblr show-tooltip"></i></a>
					<?php endif; ?>
					
					<?php if( $author_twitter_url <> '' ): ?>
						<a href="<?php echo $author_twitter_url; ?>"><i title="Twitter" data-tip-gravity="s" class="fa fa-twitter-square show-tooltip"></i></a>
					<?php endif; ?>
					
					<?php if( $author_youtube_url <> '' ): ?>
						<a href="<?php echo $author_youtube_url; ?>"><i title="YouTube" data-tip-gravity="s" class="fa fa-youtube-square show-tooltip"></i></a>
					<?php endif; ?>
					
					</div>
				</div>							
			</div>
			<?php
		endif;
	}

	/**
	 * Related posts block
	 **/
	public static function related_posts( $post_id, $limit = 8, $taxonomy = 'category' ) {
		global $wpl_galaxy_wp;
		
		$post_id = absint( $post_id );
		
		if( $post_id > 0 ):
			$page_settings = $wpl_galaxy_wp->model->post->get_post_custom( $post_id );
			
			$block_title_type = $wpl_galaxy_wp->get_option('common_related_posts_block');
			$block_title_type = $block_title_type != NULL ? $block_title_type : 'yes';
			
			if( $block_title_type == 'yes' ) {
				$block_title = $wpl_galaxy_wp->get_option('related_posts_block_title');
				$block_subtitle = $wpl_galaxy_wp->get_option('related_posts_block_subtitle');
			} else {
				$block_title = isset( $page_settings->wproto_post_related_posts_block_title ) ? $page_settings->wproto_post_related_posts_block_title : '';
				$block_subtitle = isset( $page_settings->wproto_post_related_posts_block_subtitle ) ? $page_settings->wproto_post_related_posts_block_subtitle : '';
			}
			
			// get related posts
			
			$post_type = get_post_type( $post_id );
			
			if( isset( $page_settings->wproto_post_display_related_posts_type ) && $page_settings->wproto_post_display_related_posts_type == 'any' ) {
				$related_posts = $wpl_galaxy_wp->model->post->get_random_posts( $post_type, $limit );
			} else {
				$related_posts = $wpl_galaxy_wp->model->post->get_related_posts( $post_id, $limit, $taxonomy );
			}
			
			if( $post_type == 'product' && $block_title_type == 'yes' ) {
				$block_title = __('Related Products', 'wproto');
				$block_subtitle = __('products can interested you and are related', 'wproto');
			}

			/**
			 * RELATED PRODUCTS OUTPUT
			 **/
			if( in_array( $post_type, array('product', 'wproto_catalog') ) && $related_posts != false && $related_posts->have_posts() ):
		?>
		<div class="related-products" data-appear-animation="fadeIn">
						
			<header>
				<?php if( $block_title <> '' ): ?>
				<h2><?php echo $block_title; ?></h2>
				<?php endif; ?>
				<?php if( $block_subtitle <> '' ): ?>
				<h5><?php echo $block_subtitle; ?></h5>
				<?php endif; ?>
			</header>
							
			<div class="items">
			
				<?php while ( $related_posts->have_posts() ): $related_posts->the_post(); ?>

					<div class="item box">
								
						<div class="inside">
									
							<?php if( has_post_thumbnail() ): ?>
							
							<?php
								$thumb_size = wpl_galaxy_wp_utils::is_retina() ? 'shop-related-2x' : 'shop-related';
								$thumb = wp_get_attachment_image_src( get_post_thumbnail_id( get_the_ID() ), $thumb_size );
							?>
							
							<a class="thumbnail" href="<?php the_permalink(); ?>">
								<img src="<?php echo $thumb[0]; ?>" width="180" height="182" alt="" />
							</a>
							<?php endif; ?>
											
							<a class="title" href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
							
							<?php if( $post_type == 'product' ): ?>
							
							<?php
								$product = get_product( get_the_ID() );
								
								$average = $product->get_average_rating();

								$rating_html = wpl_galaxy_wp_front::get_rating_html( $average );
								$comments_count = wp_count_comments( get_the_ID() );
							?>

							<div class="rating">
								<?php echo $rating_html; ?>
								<span>(<strong><?php echo $comments_count->total_comments; ?></strong> <?php _e('reviews', 'wproto'); ?>)</span>
							</div>

							<!-- 
							
								WOOCOMMERCE PRODUCTS
								
							-->
							
							<div class="price"><?php echo $product->get_price_html(); ?></div>
							<a href="<?php the_permalink(); ?>" class="button"><?php _e('Add to cart', 'wproto'); ?></a>
							<a href="<?php the_permalink(); ?>" class="button mobile"><?php _e('Buy', 'wproto'); ?></a>
							
							<?php elseif( $post_type == 'wproto_catalog' ): ?>
							
							<!--
							
								CATALOG ITEMS
								
							-->
							
								<?php
								
									$old_price = get_post_meta( get_the_ID(), 'old_price', true );
									$old_price = $old_price <> '' ? wpl_galaxy_wp_front::get_price( $old_price ) : '';
											
									$price = get_post_meta( get_the_ID(), 'price', true );
									$price = $price <> '' ? wpl_galaxy_wp_front::get_price( $price ) : '';
											
									$link_to_buy = get_post_meta( get_the_ID(), 'link_to_buy', true );
											
								?>
							
							<?php if( $price <> '' ): ?>
							<div class="price">
								<?php if( $old_price <> '' ): ?>
								<span class="old-price"><?php echo $old_price; ?></span>
								<?php endif; ?>
								<?php echo $price; ?>
							</div>
							<?php endif; ?>
							
								<?php if( $link_to_buy <> '' ): ?>
								<a href="<?php echo $link_to_buy; ?>" class="button"><?php _e('Buy it now', 'wproto'); ?></a>
								<a href="<?php echo $link_to_buy; ?>" class="button mobile"><?php _e('Buy', 'wproto'); ?></a>
								<?php endif; ?>
								
							<?php endif; ?>
										
							<div class="clear"></div>
									
						</div>
								
					</div>
				
				<?php endwhile; wp_reset_query(); ?>
			
			</div>
			
		</div>
		<?php
			endif;
			
			/**
			 * RELATED POSTS OUTPUT
			 **/

			if( !in_array( $post_type, array('product', 'wproto_catalog') ) && $related_posts != false && $related_posts->have_posts() ):
		?>
		<div class="related-posts" data-appear-animation="fadeIn">
		
			<?php if( $block_title <> '' ): ?>
				<h2><?php echo $block_title; ?></h2>
			<?php endif; ?>
			<?php if( $block_subtitle <> '' ): ?>
				<h4><?php echo $block_subtitle; ?></h4>
			<?php endif; ?>
			
			<div class="items">
			
				<?php while ( $related_posts->have_posts() ): $related_posts->the_post(); ?>
				
				<?php
					$post_format = get_post_format();
					$post_type = get_post_type();
				?>
				
				<div class="item post box <?php if( $post_format <> '' ): ?>format-<?php echo $post_format; endif ?> <?php if( $post_type <> '' ): ?>type-<?php echo $post_type; endif; ?>">
				
					<?php if( has_post_thumbnail() ): ?>
					<div class="thumbnail">
					
						<?php
							$thumb_size = wpl_galaxy_wp_utils::is_retina() ? 'post-related-medium-2x' : 'post-related-medium';
							
							if( $post_format == 'gallery' || $post_format == 'image' || $post_type == 'wproto_photoalbums' || $post_type == 'wproto_portfolio' ) {
								$thumb_size = wpl_galaxy_wp_utils::is_retina() ? 'post-related-big-2x' : 'post-related-big';
							}
							
							$thumb = wp_get_attachment_image_src( get_post_thumbnail_id( get_the_ID() ), $thumb_size );
						?>
					
						<a href="<?php the_permalink(); ?>">
							<img src="<?php echo $thumb[0]; ?>" alt="" />
							
							<?php if( $post_format == 'video' || $post_type == 'wproto_video' ): ?>
							<span class="mask"><i class="fa zoom fa-play-circle-o"></i></span>
							<?php else: ?>
							<span class="mask"><i class="fa zoom fa-search-plus"></i></span>
							<?php endif; ?>
										
						</a>
									
						<div class="clear"></div>
					
					</div>
					<?php endif; ?>
					
					<?php if( $post_type == 'wproto_video' ): ?>
					
						<?php
							$thumb = get_post_meta( get_the_ID(), 'thumbnail_big', true );
							if( $thumb <> '' ):
							$isset_custom_video_thumb = true;
						?>	
						<div class="thumbnail">
						
						<a href="<?php the_permalink(); ?>">
							<img src="<?php echo $thumb; ?>" alt="" />
							
							<?php if( $post_format == 'video' || $post_type == 'wproto_video' ): ?>
							<span class="mask"><i class="fa zoom fa-play-circle-o"></i></span>
							<?php endif; ?>
										
						</a>
									
						<div class="clear"></div>
						
						</div>
						<?php endif; ?>
					
					<?php endif; ?>
					
					<?php if( $post_format == 'gallery' || $post_format == 'image' || $post_type == 'wproto_photoalbums' || $post_type == 'wproto_portfolio' ): ?>
						<span class="comments"><a href="<?php the_permalink(); ?>"><i class="fa fa-comments-o"></i> <?php echo get_comments_number(); ?></a></span>
					<?php else: ?>
					
						<h5><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h5>
					
						<?php
							$date_format = get_option('date_format');
						?>
								
						<header>
							<strong><?php the_time( $date_format ); ?></strong> <span class="comments"><a href="<?php the_permalink(); ?>"><i class="fa fa-comments-o"></i> <?php echo get_comments_number(); ?></a></span>
						</header>
								
						<div class="excerpt">
							<p>
							<?php
								$ex_length = has_post_thumbnail() || isset( $isset_custom_video_thumb ) ? 80 : 230;
								echo wpl_galaxy_wp_utils::custom_excerpt( get_the_excerpt(), $ex_length ); 
							?></p>
						</div>
								
						<footer>
							<a href="<?php the_permalink(); ?>"><?php _e('Keep reading', 'wproto'); ?> <i class="arrow-keep-reading"></i></a>
						</footer>
					
					<?php endif; ?>

				</div>
				<?php endwhile; ?>
			
			</div>
			
			<div class="clear"></div>
			<?php wp_reset_query(); ?>
		</div>
		<?php
			endif;
		endif;
	}
	
	/**
	 * Display price
	 **/
	public static function get_price( $price ) {
		global $wpl_galaxy_wp;
		
		$currency_char = $wpl_galaxy_wp->get_option('catalog_currency');
		$currency_display = $wpl_galaxy_wp->get_option('catalog_currency_display');
		
		$price_format = $currency_display == 'after' ? '%s' . $currency_char : $currency_char . '%s';
		
		return sprintf( $price_format, (string)$price );
		
	}
	
	/**
	 * Get rating HTML
	 **/
	public static function get_rating_html( $rating ) {
		
		$rating = absint( $rating );
		
		$return = '';
		
		$retina = wpl_galaxy_wp_utils::is_retina() ? '@2x' : '';
		
		for( $i=1; $i<6; $i++ ) {
			
			if( $rating >= $i ) {
				$return .= '<img src="' . get_stylesheet_directory_uri() . '/images/star-1' . $retina . '.png" width="19" height="18" alt="" />';
			} else {
				$return .= '<img src="' . get_stylesheet_directory_uri() . '/images/star-2' . $retina . '.png" width="19" height="18" alt="" />';
			}
			
		}
		
		return $return;
		
	}
	
	/**
	 * Convert number to human-readable column
	 **/
	public static function get_column_name( $number ) {
		
		$number = absint( $number );
		
		if( $number <=0 || $number > 6 ) return '';
		
		switch( $number ) {
			case 1:
				return 'whole';
			break;
			case 2:
				return 'half';
			break;
			case 3:
				return 'one-third';
			break;
			case 4:
				return 'one-quarter';
			break;
			case 5:
				return 'one-fifth';
			break;
			case 6:
				return 'one-sixth';
			break;
		}
		
	}
	
}