<!doctype html>
<!--[if lt IE 7]> <html class="no-js ie6 oldie"> <![endif]-->
<!--[if IE 7]>    <html class="no-js ie7 oldie"> <![endif]-->
<!--[if IE 8]>    <html class="no-js ie8"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" <?php language_attributes(); ?>> <!--<![endif]-->
<head>
	<meta charset="<?php bloginfo( 'charset'); ?>" />
	<title><?php bloginfo('name'); ?> <?php if( is_home()){ echo ' | '; bloginfo('description'); } else { wp_title( ' | '); }; ?></title>
	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" /> 
	<?php
		global $woocommerce, $wpl_galaxy_wp;
		wpl_galaxy_wp_front::head();
	?>
	<!--[if IE 9]>
		<link rel="stylesheet" href="<?php echo get_stylesheet_directory_uri(); ?>/css/ie.css">
		<script src="<?php echo get_stylesheet_directory_uri(); ?>/js/libs/respond.min.js"></script>
		<script src="<?php echo get_stylesheet_directory_uri(); ?>/js/libs/html5.js"></script>
	<![endif]-->
	<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<div class="primary-wrapper">
	<!-- 
	
		SMALL PAGE HEADER
		
	-->

	<header class="small">
		
		<form method="get" action="<?php echo site_url(); ?>" id="top-search-form" class="pull-right">
			<fieldset>
				<input type="text" name="s" value="" placeholder="<?php _e('Search...', 'wproto'); ?>" />
				<a href="javascript:;"><i class="fa fa-search"></i></a>
			</fieldset>
		</form>
		
		<?php if( wpl_galaxy_wp_utils::isset_woocommerce() ): ?>
		<div class="pull-right">
			<a href="<?php echo get_permalink( get_option( 'woocommerce_myaccount_page_id' ) ); ?>" class="my-account"><i class="fa fa-user"></i> <?php _e('My account', 'wproto'); ?></a>
			<a href="<?php echo $woocommerce->cart->get_cart_url(); ?>" class="my-cart"><i class="fa fa-shopping-cart"></i> <?php _e('Cart:', 'wproto'); ?> <?php echo sprintf(_n('%d item', '%d items', $woocommerce->cart->cart_contents_count, 'wproto' ), $woocommerce->cart->cart_contents_count);?> / <?php echo $woocommerce->cart->get_cart_total(); ?></a>
			
			<div id="wproto-ajax-header-cart">
				<div class="triangle"></div>
				<div class="inner">
					<img class="ajax-loader" src="<?php echo get_stylesheet_directory_uri(); ?>/images/ajax-loader.gif" width="16" alt="" />
					<div class="cart-content">
				
					</div>
				</div>
			</div>
			
		</div>
		<?php endif; ?>
		
		<span class="social-icons">
			<?php wpl_galaxy_wp_front::social_icons(); ?>
		</span>      
		
		<?php $phone = $wpl_galaxy_wp->get_option( 'phone_number', 'general' ); ?>
		<?php if( $phone <> '' ): ?>
		<span class="call-to-us"><?php _e('Call us:', 'wproto'); ?> <a href="tel:<?php echo str_replace( ' ', '', $phone ); ?>"><?php echo $phone; ?></a></span>
		<?php endif; ?>
		
	</header>
	
	<!--
	
		BIG HEADER, LOGO AND MENU
		
	-->
	
	<div class="big-header-wrapper">
	
		<?php
			$contacts_page_id = $wpl_galaxy_wp->get_option( 'contacts_page_id' );
		?>
		<a href="<?php echo get_permalink( $contacts_page_id );?>" class="header-contact-link"><i class="fa fa-envelope-o"></i></a>
	
		<div class="wrapper">
		
			<div class="header-info-block">
				<p><strong><?php _e('Phone:','wproto'); ?></strong> <?php echo $phone; ?></p>
				<p><strong><?php _e('Email:','wproto'); ?></strong> <a href="mailto:<?php bloginfo('admin_email'); ?>"><?php bloginfo('admin_email'); ?></a></p>
			</div>
		
			<div class="grid">

				<header class="big box unit whole">
					<div class="grid">
						<div class="unit one-quarter">
						
							<a href="javascript:;" id="phone-toggle-menu" class="show-on-phone"><i class="fa fa-angle-down"></i></a>
						
							<?php wpl_galaxy_wp_front::logo(); ?>
							
						</div>
			
						<nav id="header-menu" class="unit three-quarters hide-on-phone">
						
						<?php
							wp_nav_menu( array(
								'theme_location' => 'header_menu',
								'menu' => '',
								'walker' => new wpl_galaxy_wp_front_nav_menu_walker,
								'menu_id' => 'header-menu-ul',
								'fallback_cb' => false
							));
						?>
						
						</nav>
						
					</div>
				</header>

			</div>
		</div>
	</div>
	
	<?php wpl_galaxy_wp_front::slider(); ?>