<?php echo $data['args']['before_widget']; ?>

<!-- widget title -->
<?php if ( isset( $data['title'] ) ) : ?>

	<?php echo $data['args']['before_title']; ?>
	
		<?php echo $data['title']; ?>
		
	<?php echo $data['args']['after_title']; ?>
	
<?php endif; ?>

<!-- widget content -->

<div class="<?php echo $data['instance']['display_icons'] != 1 ? 'no-icons' : ''; ?>">
<?php

	wp_nav_menu( array(
		'theme_location' => '',
		'menu' => $data['instance']['menu'],
		'walker' => new wpl_galaxy_wp_front_side_menu_walker,
		'menu_id' => '',
		'fallback_cb' => false
	));
	
?>
</div>


<?php echo $data['args']['after_widget'];