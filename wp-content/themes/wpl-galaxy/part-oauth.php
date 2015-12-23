<?php
	global $wpl_galaxy_wp;
	$enable_google_oauth = $wpl_galaxy_wp->get_option( 'enable_google_oauth' );
	$enable_facebook_oauth = $wpl_galaxy_wp->get_option( 'enable_facebook_oauth' );
				
	if( $enable_google_oauth == 'yes' || $enable_facebook_oauth == 'yes' ):
?>
			
	<div class="wrapper-block oauth-links">
			
		<?php if( $enable_google_oauth == 'yes' ): ?>
		<a href="<?php echo add_query_arg( array( 'wproto_action' => 'oauth-run', 'provider' => 'google' ), home_url() ); ?>" class="button button-google-plus"><i class="fa fa-google-plus"></i> <span class="border"></span> <span class="text"><?php _e( 'Sign in with Google', 'wproto'); ?></span></a>
		<?php endif; ?>
		<?php if( $enable_facebook_oauth == 'yes' ): ?>
		<a href="<?php echo add_query_arg( array( 'wproto_action' => 'oauth-run', 'provider' => 'facebook' ), home_url() ); ?>" class="button button-facebook"><i class="fa fa-facebook"></i> <span class="border"></span> <span class="text"><?php _e( 'Sign in with Facebook', 'wproto'); ?></span></a>
		<?php endif; ?>
			
	</div>
			
	<?php endif;