<?php
class wpl_galaxy_wp_category_walker extends Walker_Category {

	function start_el( &$output, $item, $depth = 0, $args = array(), $current_id = 0 ) {
		
		extract( $args );
		
		$cat_name = esc_attr( $item->name );
		$cat_name = apply_filters( 'list_cats', $cat_name, $item );
		
		if( isset( $wproto_new_sticker ) || isset( $wproto_featured_sticker ) || isset( $wproto_display_image ) || isset( $wproto_display_description ) || isset( $wproto_display_categories ) ) {
			$term_meta = get_option( "taxonomy_" . $item->term_id );
		}
		
		$return = '<li><a href="' . esc_attr( get_term_link( $item ) ) . '">';
		
		if( $show_count ) {
			$return .= ' <span class="count">' . $item->category_count . '</span>';
		}
		
		$return .= $cat_name;
		
		if( isset( $wproto_new_sticker ) && $wproto_new_sticker && $term_meta['category_new'] == 'yes' ) {
			$return .= ' <span class="new">' . __( 'new', 'wproto' ) . '</span> ';
		}
		
		if( isset( $wproto_featured_sticker ) && $wproto_featured_sticker && $term_meta['category_featured'] == 'yes' ) {
			$return .= ' <span class="featured">' . __( 'featured', 'wproto' ) . '</span> ';
		}
		
		$return .=  '</a>';
		
		if( isset( $wproto_display_image ) && $wproto_display_image ) {
			$img_id = absint( $term_meta['category_image_id'] );
			if( $img_id > 0 ) {
				$thumb = wpl_galaxy_wp_utils::is_retina() ? 'widget-recent-posts-2x' : 'widget-recent-posts';
				$image_attributes = wp_get_attachment_image_src( $img_id, $thumb );
				$return .= '<span class="cat-image"><img src="' . $image_attributes[0] . '" alt="" /></span>';
			}
		}
		
		if( isset( $wproto_display_description ) && $wproto_display_description && isset( $item->description ) && $item->description <> '' ) {
			$return .= '<p>' . $item->description . '</p>';
		}
		
		$return .= '</li>';
		
		if( !isset( $wproto_display_categories ) || $wproto_display_categories == 'all' ) {
			$output .= $return;
		}
		
		if( isset( $wproto_display_categories ) && $wproto_display_categories == 'only_featured' && $term_meta['category_featured'] == 'yes' && $term_meta['category_new'] != 'yes' ) {
			$output .= $return;
		}
		
		if( isset( $wproto_display_categories ) && $wproto_display_categories == 'only_new' && $term_meta['category_new'] == 'yes' && $term_meta['category_featured'] != 'yes' ) {
			$output .= $return;
		}
		
		if( isset( $wproto_display_categories ) && $wproto_display_categories == 'only_new_and_featured' && ( $term_meta['category_new'] == 'yes' || $term_meta['category_featured'] == 'yes' ) ) {
			$output .= $return;
		}

	}
	
}