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
<div class="primary-wrapper">
	
	<!--
	
		BIG HEADER, LOGO AND MENU
		
	-->
	
	<div class="big-header-wrapper scrolled">
	
		<div class="wrapper">
		
			<div class="grid">

				<header class="big box unit whole">
					<div class="grid">
						<div class="unit one-quarter">
						
							<a href="javascript:;" id="phone-toggle-menu" class="show-on-phone"><i class="fa fa-angle-down"></i></a>
						
							<?php wpl_galaxy_wp_front::logo(); ?>
							
						</div>
			
						<nav id="header-menu" class="unit three-quarters hide-on-phone">
						
							<!-- ONE PAGE MENU -->
							<div class="menu-header-menu-container">
								<ul id="header-menu-ul" class="menu">
									
									<?php
										$data = wpl_galaxy_wp_utils::get_post_custom( get_the_ID() );
										$show_external_blog_link = isset( $data['wproto_onepage_display_external_blog_link'] ) ? $data['wproto_onepage_display_external_blog_link'] : 'yes';
										$_sections = isset( $data['page_sections'] ) ? unserialize( $data['page_sections'] ) : array();
										$_sections = $wpl_galaxy_wp->model->sections->get( array_values( $_sections ) );
										
										$i=0; if( is_array( $_sections ) && count( $_sections ) > 0 ): $i++;
											foreach( $_sections as $wproto_section ):
											
												$_data = unserialize( $wproto_section->data );
												$section_title = isset( $_data['menu_title'] ) ? $_data['menu_title'] : '';

											?>
											<li id="menu-item-id-<?php echo $wproto_section->ID; ?>" class="menu-item level-0"><a class="item no-icon" href="#section-id-<?php echo $wproto_section->ID; ?>"><span class="menu-item-content ib"><span class="menu-text"><?php echo $section_title; ?></span></span></a></li>
											<?php
											endforeach;
										endif;
										
										if( $show_external_blog_link == 'yes' ):
									?>
									<li class="menu-item level-0"><a class="item no-icon external" href="<?php if( get_option( 'show_on_front' ) == 'page' ) echo get_permalink( get_option('page_for_posts' ) ); else echo home_url();?>"><span class="menu-item-content ib"><span class="menu-text"><?php _e('Blog', 'wproto'); ?> &rarr;</span></span></a></li>
									<?php
										endif;
									?>
									
								</ul>
							</div>
						
						</nav>
						
					</div>
				</header>

			</div>
		</div>
	</div>