<?php
/**
 * Benefits Custom post type controller
 **/
class wpl_galaxy_wp_benefits_controller extends wpl_galaxy_wp_base_controller {

	function __construct() {
		// Security: Admin only
		if ( is_admin() ) {
			// Add custom meta boxes
			add_action( 'add_meta_boxes', array( $this, 'add_remove_metaboxes' ) );
			// Save custom data
			add_action( 'save_post', array( $this, 'save_custom_meta' ) );
			
			add_filter( 'manage_edit-wproto_benefits_columns', array( $this, 'manage_admin_columns' ) );
			add_action( 'manage_wproto_benefits_posts_custom_column', array( $this, 'get_admin_columns' ), 10, 2);
			// add info box
			add_action( 'admin_footer', array( $this, 'add_info_box'));
			
			// Filter by category
			add_action( 'restrict_manage_posts', array( $this, 'add_flter_posts_by_category' ) );
			add_filter( 'parse_query', array( $this, 'add_posts_query_filter' ) );
			
			// Add JS 
			add_action( 'admin_enqueue_scripts', array( $this, 'add_scripts' ) );
		}
	}
	
	/**
	 * Remove unused metaboxes and add custom
	 **/
	function add_remove_metaboxes() {
		remove_meta_box( 'postcustom', 'wproto_benefits', 'normal');
		remove_meta_box( 'slugdiv', 'wproto_benefits', 'normal');
		
		add_meta_box(
			'wproto_meta_benefit_type'
			,__( 'Style settings', 'wproto' )
			,array( $this, 'render_meta_box_benefit_type' )
			,'wproto_benefits'
			,'side'
			,'default'
		);
		
	}
	
	/**
	 * Save custom meta data
	 **/
	function save_custom_meta( $post_id ) {
				
		$post_type = get_post_type( $post_id );
		
		if( $post_type == 'wproto_benefits' ) {
			
			// Stop WP from clearing custom fields on autosave
			if ( defined( 'DOING_AUTOSAVE') && DOING_AUTOSAVE )
				return;

			// Prevent quick edit from clearing custom fields
			if ( defined( 'DOING_AJAX') && DOING_AJAX )
				return;

			if( empty( $_POST) )
				return;
				
			$allowed_tags = wp_kses_allowed_html( 'post' );
			
			update_post_meta( $post_id, "wproto_benefit_link", isset( $_POST["wproto_benefit_link"] ) ? wp_kses( $_POST["wproto_benefit_link"], $allowed_tags ) : '' );	
			update_post_meta( $post_id, "wproto_benefit_style", isset( $_POST["wproto_benefit_style"] ) ? wp_kses( $_POST["wproto_benefit_style"], $allowed_tags ) : '' );
			update_post_meta( $post_id, "wproto_benefit_icon_name", isset( $_POST["wproto_benefit_icon_name"] ) ? wp_kses( $_POST["wproto_benefit_icon_name"], $allowed_tags ) : '' );
			update_post_meta( $post_id, "wproto_benefit_animation", isset( $_POST["wproto_benefit_animation"] ) ? wp_kses( $_POST["wproto_benefit_animation"], $allowed_tags ) : '' );
			update_post_meta( $post_id, "wproto_benefit_animation_delay", isset( $_POST["wproto_benefit_animation_delay"] ) ? wp_kses( $_POST["wproto_benefit_animation_delay"], $allowed_tags ) : '' );
			
		}
	}
	
	/**
	 * Render "Benefit type" metabox
	 **/
	function render_meta_box_benefit_type() {
		global $post;
		$data = array();
		$data['link'] = get_post_meta( $post->ID, 'wproto_benefit_link', true );
		$data['style'] = get_post_meta( $post->ID, 'wproto_benefit_style', true );
		$data['icon'] = get_post_meta( $post->ID, 'wproto_benefit_icon_name', true );
		$data['animation'] = get_post_meta( $post->ID, 'wproto_benefit_animation', true );
		$data['animation_delay'] = get_post_meta( $post->ID, 'wproto_benefit_animation_delay', true );
		
		$this->view->load_partial( 'metaboxes/benefits_style', $data );
	}
	
	/**
	 * Manage admin columns
	 **/
	function manage_admin_columns( $columns ) {
		$new_columns['cb'] = '<input type="checkbox" />';
		$new_columns['image'] = __( 'Icon / Image', 'wproto');
		$new_columns['title'] = __( 'Title', 'wproto' );
		$new_columns['text'] = __( 'Text', 'wproto' );
		$new_columns['category'] = __( 'Categories', 'wproto');
		
		$new_columns['date'] = __( 'Date', 'wproto');
		
		return $new_columns;
	}
	
	/**
	 * Get the data for admin columns
	 **/
	function get_admin_columns( $column_name, $id ) {
		
		$style = get_post_meta( $id, 'wproto_benefit_style', true );
		
		switch ( $column_name ) {
			case 'image':
				echo '<a href="' . admin_url( 'post.php?post=' . $id . '&action=edit' ) . '">';
				echo '<div class="wproto-admin-thumb">';
				
				$thumb = wpl_galaxy_wp_utils::is_retina() ? 'wproto-admin-thumb-2x' : 'wproto-admin-thumb';
				$img = wpl_galaxy_wp_utils::is_retina() ? 'noimage-2x.gif' : 'noimage.gif';
				
				if( $style == '' || $style == 'image' ) {

					if ( has_post_thumbnail() ):
						$url_arr = wp_get_attachment_image_src( get_post_thumbnail_id( $id ), $thumb );
					
						echo '<img width="100" height="75" src="' . $url_arr[0] . '" alt="" />';
					else: 
						echo '<img width="100" height="75" src="' . WPROTO_THEME_URL . '/images/admin/' . $img . '" alt="" />';
					endif;
					
				} else {
					
					$icon = get_post_meta( $id, 'wproto_benefit_icon_name', true );
					
					if ( $icon <> '' ) {
						echo '<i class="fa-4x ' . $icon . '"></i>';
					} else {
						
						echo '<img width="100" height="75" src="' . WPROTO_THEME_URL . '/images/admin/' . $img . '" alt="" />';
					}
					
				}
				

				echo '</div>';
				echo '</a>';
			break;
			case 'text':
				the_excerpt();
			break;
			case 'category':
				$terms = get_the_terms( $id, 'wproto_benefits_category' );
				$this->view->load_partial( 'admin_filters/list_categories', array( 'terms' => $terms ) );
			break;
		}
	}
	
	/**
	 * Add info box
	 **/
	function add_info_box() {
		$screen = get_current_screen();
		$hide_infobox = $this->get_option( 'hide_infobox', 'general' );
		// Add - edit sidebars screen
		if( $hide_infobox != 'yes' && ( isset( $screen->base ) && $screen->base == 'edit' ) && $_GET['post_type'] == 'wproto_benefits' ):
			$this->view->load_partial( 'infobox/infobox', array('title' => __( 'Benefits', 'wproto'), 'content' => '<p>' . __( 'Benefits - it\'s a not public post type. Use this feature to collect your advantages records and show them at website as a widget or as a part of page content.', 'wproto') . '</p>' . '<p>' . __( sprintf( '<a href="%s">Divide them into categories</a> for easy management.', admin_url('edit-tags.php?taxonomy=wproto_benefits_category&post_type=wproto_benefits')), 'wproto') . '</p>') );
		endif; 
	}
	
	/**
	 * Filter query by category at admin screen
	 **/
	function add_flter_posts_by_category() {
		global $post, $wp_query;
		if ( get_post_type( $post ) == 'wproto_benefits' ) {
			$data = array();
			$data['wp_query'] = $wp_query;
			$data['taxonomy'] = 'wproto_benefits_category';
			$this->view->load_partial( 'admin_filters/category_filter', $data );
		}
	}
	
	/**
	 * Query filter by category at admin screen
	 **/
	function add_posts_query_filter( $query ) {
		
		global $post;
			
		if ( get_post_type( $post ) == 'wproto_benefits' ) {
				
			if( isset( $_GET['filter_by_category'] ) && $_GET['filter_by_category'] > 0 ) {
				$query->set( 'tax_query', array(
					array(
						'taxonomy' => 'wproto_benefits_category',
						'terms' => $_GET['filter_by_category'] 
					)
				));
			}
				
		}
		
	}
	
	/**
	 * Add JS Scripts
	 **/
	function add_scripts() {
		global $post;
		
		if( get_post_type( $post ) == 'wproto_benefits' ) {
			wp_register_script( 'wproto-benefits', WPROTO_THEME_URL . '/js/admin/screen-benefits.js?' . $this->settings['res_cache_time'] );
			wp_enqueue_script( 'wproto-benefits', array( 'jquery' ) );
		}
		
	}

}