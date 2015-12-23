<?php
/**
 * Comments controller
 **/
class wpl_galaxy_wp_comments_controller extends wpl_galaxy_wp_base_controller {
	
	function __construct() {
		// Security: Admin only
		if ( is_admin() ) {
			add_filter( 'manage_edit-comments_columns', array( $this, 'add_admin_comment_columns' ) );
			add_action( 'manage_comments_custom_column', array( $this, 'get_admin_columns' ), 10, 2 );
			add_filter( 'manage_edit-comments_sortable_columns', array( $this, 'manage_sortable_columns' ));
		}
	}
	
	/**
	 * Add custom columns to admin comments screen
	 **/
	function add_admin_comment_columns( $columns ) {
		
		$settings = get_option( 'wproto_theme_settings' );
		$likes_on_comments = $this->get_option( 'likes_on_comments', 'general' );
		
		if( $likes_on_comments != 'no' ) {
			$columns['rating'] = __( 'Likes', 'wproto' );
		}
		
		return $columns;
	}
	
	/**
	 * Get admin columns value
	 **/
	function get_admin_columns( $column_name, $id ) {
		switch ( $column_name ) {
			case 'rating':
				
				$likes = get_comment_meta( $id, 'wproto_likes', true );
				$like_img = wpl_galaxy_wp_utils::is_retina() ? 'like@2x.png' : 'like.png';
				echo absint( $likes ) . ' <img width="16" height="16" src="' . WPROTO_THEME_URL . '/images/admin/' . $like_img . '" alt="" />';
				
			break;
		}
	}
	
	/**
	 * Sortable by comment likes
	 **/
	function manage_sortable_columns( $columns ) {
		$columns['rating'] = 'rating';
		return $columns;
	}
	
}