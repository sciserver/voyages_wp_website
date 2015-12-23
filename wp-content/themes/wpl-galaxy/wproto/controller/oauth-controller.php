<?php
/**
 *	Add custom fields to the navigation menus
 **/
class wpl_galaxy_wp_oauth_controller extends wpl_galaxy_wp_admin_controller {
	
	function __construct() {

	}
	
	/**
	 * Run the OAuth process
	 **/
	function run() {
		$provider = isset( $_GET['provider'] ) ? trim( $_GET['provider'] ) : '';
		
		if( $provider <> '' && ! is_user_logged_in() ) {
			
			require_once WPROTO_THEME_DIR . '/library/oauth/http.php';
			require_once WPROTO_THEME_DIR . '/library/oauth/oauth_client.php';
		
			$client = new oauth_client_class;
		
			$client->debug = false;
			$client->debug_http = false;
			
			$_SESSION['wproto_oauth_return_url'] = isset( $_SERVER['HTTP_REFERER'] ) ? $_SERVER['HTTP_REFERER'] : home_url();
			
			switch( $provider ) {
				default:
				
					wp_redirect( home_url('/') );
				
				break;
				case 'facebook':
				
					$client_id = $this->get_option( 'facebook_client_id' );
					$client_secret = $this->get_option( 'facebook_client_secret' );
				
					if( $this->get_option( 'enable_facebook_oauth' ) == 'yes' && $client_id <> '' && $client_secret <> '' ) {
						
						$client->server = 'Facebook';
						$client->redirect_uri = home_url('/?wproto_action=oauth-run&provider=facebook');
						$client->client_id = $client_id;
						$client->client_secret = $client_secret;
						$client->scope = 'email';
						
						// try to get data
						if( ( $success = $client->Initialize() ) ) {
							if( ( $success = $client->Process() ) ) {
								if( strlen( $client->access_token ) ) {
									$success = $client->CallAPI( 'https://graph.facebook.com/me', 'GET', array(), array( 'FailOnAccessError' => true ), $user);
								}
							}
							$success = $client->Finalize( $success );
						}
						
						if( $client->exit ) exit;

						if( $success ) {
							
							if( ! $this->_auth_user( $user, 'facebook' ) ) {
								$client->ResetAccessToken();
								wp_redirect( home_url('/?wproto_error=oauth&provider=facebook&text=' . urlencode( __( 'We can not identify the user because this email used for another account. Use another email address or contact to our support.', 'wproto') ) ) );
							}
							
						} else {
							$client->ResetAccessToken();
							wp_redirect( home_url('/?wproto_error=oauth&provider=facebook&text=' . urlencode( __( 'An unexpected error occurred. Unable to complete the operation. Please, try again later or contact to our support. Server response: ', 'wproto') . $client->error ) ) );
						}
						
					} else {
						wp_redirect( home_url('/?wproto_error=oauth&provider=facebook&text=' . urlencode( __('Wrong Facebook OAuth settings', 'wproto') ) ) );
					}
				
				break;
				case 'google':
				
					$client_id = $this->get_option( 'google_client_id' );
					$client_secret = $this->get_option( 'google_client_secret' );
					
					if( $this->get_option( 'enable_google_oauth' ) == 'yes' && $client_id <> '' && $client_secret <> '' ) {
						
						$client->server = 'Google';
						$client->redirect_uri = home_url('/?wproto_action=oauth-run&provider=google');
						$client->client_id = $client_id;
						$client->client_secret = $client_secret;
						$client->scope = 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile';
						
						if( ( $success = $client->Initialize() ) ) {
							if( ( $success = $client->Process() ) ) {
								if( strlen( $client->authorization_error ) ) {
									$client->error = $client->authorization_error;
									$success = false;
								} elseif( strlen( $client->access_token ) ) {
									$success = $client->CallAPI('https://www.googleapis.com/oauth2/v1/userinfo','GET', array(), array('FailOnAccessError'=>true), $user);
								}
							}
							$success = $client->Finalize($success);
						}
						
						if( $client->exit ) exit;
						
						if( $success ) {

							if( ! $this->_auth_user( $user, 'google' ) ) {
								$client->ResetAccessToken();
								wp_redirect( home_url('/?wproto_error=oauth&provider=google&text=' . urlencode( __( 'We can not identify the user because this email used for another account. Use another email address or contact to our support.', 'wproto') ) ) );
							}
							
						} else {
							$client->ResetAccessToken();
							wp_redirect( home_url('/?wproto_error=oauth&provider=google&text=' . urlencode( __( 'An unexpected error occurred. Unable to complete the operation. Please, try again later or contact to our support. Server response: ', 'wproto') . $client->error ) ) );
							
						}
						
					} else {
						wp_redirect( home_url('/?wproto_error=oauth&provider=facebook&text=' . urlencode( __('Wrong Google OAuth settings.', 'wproto') ) ) );
					}
				
				break;
			}
			
		} else {
			wp_redirect( home_url('/') );
		}
		
		exit;

	}
	
	/**
	 * Auth user
	 **/
	private function _auth_user( $user, $provider ) {
		
		$user_query = new WP_User_Query( array( 'search' => $user->email, 'search_columns' => array( 'user_email' ), 'meta_key' => 'wproto_' . $provider . '_profile_id', 'meta_value' => $user->id ) );
		$wp_user = get_user_by( 'email', $user->email );
		
		if( $wp_user !== false && $user_query->total_users == 0 ) {
			return false;
		}
		
		if( $wp_user === false ) {
			// create new user
			$user_id = wp_create_user( $user->email, wp_generate_password( 13, true ), $user->email );
			update_user_meta( $user_id, 'wproto_' . $provider . '_profile_id', $user->id );
			
			$first_name = '';
			$last_name = '';
			
			switch( $provider ) {
				case 'facebook':
					$first_name = $user->first_name;
					$last_name = $user->last_name;
				break;
				case 'google':
					$first_name = $user->given_name;
					$last_name = $user->family_name;
				break;
			}
			
			wp_update_user(
				array(
					'ID' => $user_id,
					'first_name' => $first_name,
					'last_name' => $last_name,
					'user_url' => $user->link,
					'display_name' => $first_name . ' ' . $last_name
				)
			);
			
			$this->_login_user( $user_id, $user->email );
			
		} else {
			// login 
			$this->_login_user( $wp_user->ID, $user->email );
		}

	}
	
	/**
	 * Login user
	 **/
	private function _login_user( $user_id, $login ) {
		
		$return_path = isset( $_SESSION['wproto_oauth_return_url'] ) ? $_SESSION['wproto_oauth_return_url'] : '';
		
		if( $return_path <> '' ) {
			$_SESSION['wproto_oauth_return_url'] = '';
		} else {
			$return_path = home_url();
		}
		
		wp_set_current_user( $user_id, $login );
		wp_set_auth_cookie( $user_id );
		do_action( 'wp_login', $login );
		wp_redirect( $return_path );
		die;
	}

}