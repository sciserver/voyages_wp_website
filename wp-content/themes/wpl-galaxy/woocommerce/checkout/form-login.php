<?php
/**
 * Checkout login form
 *
 * @author 		WooThemes
 * @package 	WooCommerce/Templates
 * @version     2.0.0
 */
 
if ( ! defined( 'ABSPATH' ) ) exit; // Exit if accessed directly

global $woocommerce, $wpl_galaxy_wp;
$enable_google_oauth = $wpl_galaxy_wp->get_option( 'enable_google_oauth' );
$enable_facebook_oauth = $wpl_galaxy_wp->get_option( 'enable_facebook_oauth' );

if ( is_user_logged_in() || 'no' == get_option( 'woocommerce_enable_checkout_login_reminder' ) ) return;
?>

<h3><?php _e('Login', 'wproto'); ?>:</h3>

<?php
	woocommerce_login_form(
		array(
			'message'  => __( 'If you have shopped with us before, please enter your details in the boxes below. If you are a new customer please proceed to the Billing &amp; Shipping section.', 'woocommerce' ),
			'redirect' => get_permalink( wc_get_page_id( 'checkout') ),
			'hidden'   => true
		)
	);
?>

				<?php if( $enable_google_oauth == 'yes' ): ?>
				<a href="<?php echo add_query_arg( array( 'wproto_action' => 'oauth-run', 'provider' => 'google' ), home_url() ); ?>" class="button button-google-plus"><i class="fa fa-google-plus"></i> <span class="border"></span> <span class="text"><?php _e( 'Sign in with Google', 'wproto'); ?></span></a>
				<?php endif; ?>
				<?php if( $enable_facebook_oauth == 'yes' ): ?>
				<a href="<?php echo add_query_arg( array( 'wproto_action' => 'oauth-run', 'provider' => 'facebook' ), home_url() ); ?>" class="button button-facebook"><i class="fa fa-facebook"></i> <span class="border"></span> <span class="text"><?php _e( 'Sign in with Facebook', 'wproto'); ?></span></a>
				<?php endif; ?>
				<br /><br />