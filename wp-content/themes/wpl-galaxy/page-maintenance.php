<?php
	get_header('simple');
	global $wpl_galaxy_wp;
	
	$logo = wpl_galaxy_wp_utils::is_retina() ? $wpl_galaxy_wp->get_option('maintenance_logo_2x') : $wpl_galaxy_wp->get_option('maintenance_logo');
	$logo_size = @getimagesize( $wpl_galaxy_wp->get_option('maintenance_logo') );
	
	$bg_image = wpl_galaxy_wp_utils::is_retina() ? $wpl_galaxy_wp->get_option('maintenance_background_2x') : $wpl_galaxy_wp->get_option('maintenance_background');
	$bg_h_pos = $wpl_galaxy_wp->get_option('maintenance_background_h_pos');
	$bg_v_pos = $wpl_galaxy_wp->get_option('maintenance_background_v_pos');
	$bg_repeat = $wpl_galaxy_wp->get_option('maintenance_background_repeat');
	$bg_animate = $wpl_galaxy_wp->get_option('maintenance_background_zoom');
?>
<div class="background <?php echo $bg_animate != 'no' ? 'animate-bg' : ''; ?>" style="background: url(<?php echo $bg_image; ?>) <?php echo $bg_h_pos; ?> <?php echo $bg_v_pos; ?> <?php echo $bg_repeat; ?>;"></div>
<!-- 
	
	PAGE HEADER
		
-->

<header class="wrapper">
		
	<img src="<?php echo $logo; ?>" width="<?php echo isset( $logo_size[0] ) ? $logo_size[0] : ''; ?>" height="<?php echo isset( $logo_size[1] ) ? $logo_size[1] : ''; ?>" alt="" />
		
</header>
	
<!-- 
	
	CONTENT SECTION
		
-->
	
<div id="content">
				
	<div class="line">
				
		<div class="wrapper">
			<h1><?php _e('We are under maintenance', 'wproto'); ?></h1>
			
			<div class="text">
				<?php echo nl2br( $wpl_galaxy_wp->get_option('maintenance_text') ); ?>
			</div>
			
			<div class="icon">
				<img src="<?php echo get_stylesheet_directory_uri(); ?>/images/icons/icon-maintenance<?php echo wpl_galaxy_wp_utils::is_retina() ? '@2x' : ''; ?>.png" width="274" height="295" alt="" />
			</div>
						
		</div>
					
	</div>
			
	<div class="wrapper social-icons">
		<?php wpl_galaxy_wp_front::social_icons( true, false ); ?>
	</div>
				
</div>

<!-- 
	
	FOOTER SECTION
		
-->

<footer id="primary-footer">
	<div class="wrapper grid">
		<div class="unit whole">
			<?php echo $wpl_galaxy_wp->get_option('copyright_text'); ?>
			<?php if( $wpl_galaxy_wp->get_option('show_wplab_info') == 'yes' ): ?>
			Design &amp; Development by <a href="http://wplab.pro">WPlab.pro</a>
			<?php endif; ?>
		</div>
	</div>
</footer>
<?php wp_footer(); ?>
</body>
</html>