<?php echo $data['args']['before_widget']; ?>

<!-- widget title -->
<?php if ( isset( $data['title'] ) ) : ?>

	<?php echo $data['args']['before_title']; ?>
	
		<?php echo $data['title']; ?>
		
	<?php echo $data['args']['after_title']; ?>
	
<?php endif; ?>

<!-- widget content -->

<?php if( isset( $data['instance']['before_text'] ) && $data['instance']['before_text'] <> '' ): ?>
<p><?php echo $data['instance']['before_text']; ?></p>
<?php endif; ?>

<iframe width="100%" height="170" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/maps?q=<?php echo urlencode( $data['instance']['address'] ); ?>&amp;iwloc=near&amp;t=m&amp;z=13&amp;output=embed"></iframe>

<address><span><?php _e('Address', 'wproto'); ?>:</span> <?php echo $data['instance']['address']; ?></address>

<?php if( isset( $data['instance']['after_text'] ) && $data['instance']['after_text'] <> '' ): ?>
<p><?php echo $data['instance']['after_text']; ?></p>
<?php endif; ?>

<?php echo $data['args']['after_widget'];