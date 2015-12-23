<?php echo $data['args']['before_widget']; ?>

<!-- widget content -->
<?php if( isset( $data['instance']['logo'] ) && $data['instance']['logo'] <> '' ): ?>

	<?php
		$logo_url = wpl_galaxy_wp_utils::is_retina() && $data['instance']['logo_2x'] <> '' ? $data['instance']['logo_2x'] : $data['instance']['logo']; 
	?>

<a href="<?php bloginfo('wpurl'); ?>" class="footer-logo ib"><img src="<?php echo $logo_url; ?>" width="<?php echo $data['instance']['logo_width']; ?>" alt="" /></a>
<?php endif; ?>

<?php if( isset( $data['instance']['description'] ) && $data['instance']['description'] <> '' ): ?>
<p><?php echo $data['instance']['description']; ?></p>
<?php endif; ?>

<?php echo $data['args']['after_widget'];