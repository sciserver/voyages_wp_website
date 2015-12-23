<?php
/**
 * Login Form
 *
 * @author 		WooThemes
 * @package 	WooCommerce/Templates
 * @version     2.1.0
 */

if ( ! defined( 'ABSPATH' ) ) exit; // Exit if accessed directly
global $woocommerce, $wpl_galaxy_wp;
$enable_google_oauth = $wpl_galaxy_wp->get_option( 'enable_google_oauth' );
$enable_facebook_oauth = $wpl_galaxy_wp->get_option( 'enable_facebook_oauth' );
?>

<?php wc_print_notices(); ?>

<?php do_action( 'woocommerce_before_customer_login_form' ); ?>


<h2><?php _e( 'Login', 'woocommerce' ); ?></h2>

<form method="post" class="login">

	<?php do_action( 'woocommerce_login_form_start' ); ?>

			<p class="form-row form-row-wide">
				<label for="username"><?php _e( 'Username or email', 'woocommerce' ); ?> <span class="required">*</span></label>
				<input type="text" class="input-text" name="username" id="username" />
			</p>
			<p class="form-row form-row-wide">
				<label for="password"><?php _e( 'Password', 'woocommerce' ); ?> <span class="required">*</span></label>
				<input class="input-text" type="password" name="password" id="password" />
			</p>

			<?php do_action( 'woocommerce_login_form' ); ?>

			<p class="form-row">
				<?php wp_nonce_field( 'woocommerce-login' ); ?>
				<input type="submit" class="button" name="login" value="<?php _e( 'Login', 'woocommerce' ); ?>" />  
				<?php if( $enable_google_oauth == 'yes' || $enable_facebook_oauth == 'yes' ): ?>
				<span class="login-caption"><?php _e('or login with your social account', 'wproto'); ?></span>
				<?php endif; ?> 
				<?php if( $enable_google_oauth == 'yes' ): ?>
				<a href="<?php echo add_query_arg( array( 'wproto_action' => 'oauth-run', 'provider' => 'google' ), home_url() ); ?>" class="button button-google-plus"><i class="fa fa-google-plus"></i> <span class="border"></span> <span class="text"><?php _e( 'Sign in with Google', 'wproto'); ?></span></a>
				<?php endif; ?>
				<?php if( $enable_facebook_oauth == 'yes' ): ?>
				<a href="<?php echo add_query_arg( array( 'wproto_action' => 'oauth-run', 'provider' => 'facebook' ), home_url() ); ?>" class="button button-facebook"><i class="fa fa-facebook"></i> <span class="border"></span> <span class="text"><?php _e( 'Sign in with Facebook', 'wproto'); ?></span></a>
				<?php endif; ?>
			</p>

			<?php do_action( 'woocommerce_login_form_end' ); ?>

		</form>


<?php do_action( 'woocommerce_after_customer_login_form' ); ?>