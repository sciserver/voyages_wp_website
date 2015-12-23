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
	<!--[if lt IE 9]>
		<link rel="stylesheet" href="<?php echo get_stylesheet_directory_uri(); ?>/css/ie.css">
		<script src="<?php echo get_stylesheet_directory_uri(); ?>/js/libs/respond.min.js"></script>
		<script src="<?php echo get_stylesheet_directory_uri(); ?>/js/libs/html5.js"></script>
	<![endif]-->
	<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>