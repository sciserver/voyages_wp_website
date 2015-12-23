<?php
/**
 * Back-end controller
 **/
class wpl_galaxy_wp_user_controller extends wpl_galaxy_wp_base_controller {
	
	function __construct() {
		
		if( is_admin() ) {
			// add user custom fields for oAUTH
			add_filter( 'show_user_profile', array( $this, 'add_user_custom_fields' ));
			add_filter( 'edit_user_profile', array( $this, 'add_user_custom_fields' ));
			
			add_action( 'personal_options_update', array( $this, 'save_user_custom_fields' ));
			add_action( 'edit_user_profile_update', array( $this, 'save_user_custom_fields' ));
		}
		
	}
	
	/**
	 * Add user custom fields
	 **/
	function add_user_custom_fields( $user ) {
		$this->view->load_partial( 'custom_fields/user_custom_fields', array( 'user' => $user ) );
	}
	
	/**
	 * Save user custom fields
	 **/
	function save_user_custom_fields( $user_id ) {
		if ( !current_user_can( 'edit_user', $user_id ) )
			return false;
		
		$allowed_tags = wp_kses_allowed_html( 'post' );
		
		update_user_meta( $user_id, 'wproto_facebook_profile_id', wp_kses( $_POST['wproto_facebook_profile_id'], $allowed_tags ) );
		update_user_meta( $user_id, 'wproto_google_profile_id', wp_kses( $_POST['wproto_google_profile_id'], $allowed_tags ) );
		
		update_user_meta( $user_id, 'wproto_social_dribbble_url', wp_kses( $_POST['wproto_social_dribbble_url'], $allowed_tags ) );
		update_user_meta( $user_id, 'wproto_social_facebook_url', wp_kses( $_POST['wproto_social_facebook_url'], $allowed_tags ) );
		update_user_meta( $user_id, 'wproto_social_flickr_url', wp_kses( $_POST['wproto_social_flickr_url'], $allowed_tags ) );
		update_user_meta( $user_id, 'wproto_social_google_plus_url', wp_kses( $_POST['wproto_social_google_plus_url'], $allowed_tags ) );
		update_user_meta( $user_id, 'wproto_social_linkedin_url', wp_kses( $_POST['wproto_social_linkedin_url'], $allowed_tags ) );
		update_user_meta( $user_id, 'wproto_social_tumblr_url', wp_kses( $_POST['wproto_social_tumblr_url'], $allowed_tags ) );
		update_user_meta( $user_id, 'wproto_social_twitter_url', wp_kses( $_POST['wproto_social_twitter_url'], $allowed_tags ) );
		update_user_meta( $user_id, 'wproto_social_youtube_url', wp_kses( $_POST['wproto_social_youtube_url'], $allowed_tags ) );
	}
	
}