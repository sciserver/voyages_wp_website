<?php echo $data['args']['before_widget']; ?>

<!-- widget title -->
<?php if ( isset( $data['title'] ) ) : ?>

	<?php echo $data['args']['before_title']; ?>
	
		<?php echo $data['title']; ?>
		
	<?php echo $data['args']['after_title']; ?>
	
<?php endif; ?>

<!-- widget content -->

<?php if( !is_user_logged_in() ): ?>

	<?php get_template_part( 'part', 'oauth' ); ?>

<?php else: ?>

	<?php
		$user = wp_get_current_user();
	?>

	<p><?php _e( sprintf( 'Hello, %s!', $user->display_name ), 'wproto'); ?> <a href="<?php echo wp_logout_url( home_url( $_SERVER["REQUEST_URI"] )); ?>"><?php _e('Logout?', 'wproto'); ?></a></p>

<?php endif; ?>

<?php echo $data['args']['after_widget'];