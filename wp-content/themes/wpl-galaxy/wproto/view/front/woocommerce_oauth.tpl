<?php if( !is_user_logged_in() ): ?>

	<h4><?php _e('Sign In / Sign Up with social networks', 'wproto'); ?></h4>

	<?php
		global $wpl_galaxy_wp;
		$google_enabled = $wpl_galaxy_wp->get_option( 'enable_google_oauth', 'api' );
		$facebook_enabled = $wpl_galaxy_wp->get_option( 'enable_google_oauth', 'api' );
	?>
	<?php if( $facebook_enabled == 'yes' ): ?>
	<p>
		<a href="<?php echo home_url('/?wproto_action=oauth-run&provider=facebook'); ?>" class="button"><i class="icon-facebook"></i> <?php _e('Login with Facebook', 'wproto'); ?></a>
	</p>
	<?php endif; ?>

	<?php if( $google_enabled == 'yes' ): ?>
	<p>
		<a href="<?php echo home_url('/?wproto_action=oauth-run&provider=google'); ?>" class="button"><i class="icon-google-plus"></i> <?php _e('Login with Google', 'wproto'); ?></a>
	</p>
	<?php endif; ?>

<?php endif; ?>