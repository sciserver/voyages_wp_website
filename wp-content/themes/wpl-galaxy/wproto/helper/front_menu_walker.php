<?php

class wpl_galaxy_wp_front_nav_menu_walker extends Walker_Nav_Menu {
        
	function start_el( &$output, $item, $depth = 0, $args = array(), $current_id = 0 ) {
		global $wp_query;
		$indent = ( $depth ) ? str_repeat( "\t", $depth ) : '';

		$class_names = $value = '';

		$classes = empty( $item->classes ) ? array() : (array) $item->classes;
		$classes[] = 'menu-item-' . $item->ID;
		$classes[] = 'level-' . $depth;
		
		if( $item->mega_menu == 'yes' ) {
			$classes[] = 'mega-menu';
		}
		
		if( $item->hide_large_desktop == 'yes' ) {
			$classes[] = 'hide-on-large-desktop';
		}
		
		if( $item->hide_small_desktop == 'yes' ) {
			$classes[] = 'hide-on-small-desktop';
		}
		
		if( $item->hide_tablet == 'yes' ) {
			$classes[] = 'hide-on-tablet';
		}
		
		if( $item->hide_phone == 'yes' ) {
			$classes[] = 'hide-on-phone';
		}
		
		$posts_page_id = get_option('page_for_posts');
		
		if( $posts_page_id == $item->object_id ) {
			$classes[] = 'blog-menu-item';
			
			if( $wp_query->query_vars['post_type'] != '' || is_404() ) {
				$classes = array_diff( $classes, array( 'current_page_parent', 'current_page_item', 'current-menu-item' ));
			}
			
		}

		$class_names = join( ' ', apply_filters( 'nav_menu_css_class', array_filter( $classes ), $item, $args ) );
		$class_names = ' class="' . esc_attr( $class_names ) . '"';

		$id = apply_filters( 'nav_menu_item_id', 'menu-item-'. $item->ID, $item, $args );
		$id = strlen( $id ) ? ' id="' . esc_attr( $id ) . '"' : '';

		$output .= $indent . '<li' . $id . $value . $class_names .'>';

		$title_attr  	 = ! empty( $item->attr_title ) ? ' title="'  . esc_attr( $item->attr_title ) .'"' : '';
		$attributes 	 = ! empty( $item->target )     ? ' target="' . esc_attr( $item->target     ) .'"' : '';
		$attributes 	.= ! empty( $item->xfn )        ? ' rel="'    . esc_attr( $item->xfn        ) .'"' : '';
		$attributes 	.= ! empty( $item->url )        ? ' href="'   . esc_attr( $item->url        ) .'"' : '';

		$item_output = $args->before;

		$i = $item->menu_icon <> '' ? $item->menu_icon : '';
            
		$current_url = ( is_ssl() ? 'https://' : 'http://' ) . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI']; 
		$item_url = esc_attr( $item->url); 
		
		$href_class = $item->menu_icon <> '' ? 'item with-icon' : 'item no-icon';
		
		if( $item->attr_title <> '' ) {
			$href_class .= ' show-tooltip';
		}
		
		if( $item->dont_display_as_link == 'yes' ) {
			$item_output .= '<a data-tip-gravity="e" class="' . $href_class . ' " ' . $title_attr . '>';
		} else {
			if ( $item_url != $current_url ) {
				$item_output .= '<a data-tip-gravity="s" class="' . $href_class . '" '. $attributes .' ' . $title_attr . '>';
			} elseif( $depth == 1) {
				$item_output .= '<a data-tip-gravity="s" class="' . $href_class . '" ' . $title_attr . '>';
			} else {
				$item_output .= '<a data-tip-gravity="s" class="' . $href_class . '" ' . $title_attr . '>';
			}			
		}
  
  	$item_output .= '<span class="menu-item-content ib">';
  
  	if( $item->menu_icon <> '' && $depth > 0 ) {
  		$item_output .= '<span class="icon"><i class="' . $i . '"></i></span>';
  	}
  
		$item_output .= $args->link_before . '<span class="menu-text">' . apply_filters( 'the_title', $item->title, $item->ID ) . '</span>' . $args->link_after;
		
		$item_output .= '</span></a>';

		/**
		 * Display mega menu
		 **/    
		if( $item->mega_menu == 'yes' ) {
			
			$_locations = get_nav_menu_locations();
			$_menu_id = isset( $_locations[ $args->theme_location ] ) ? $_locations[ $args->theme_location ] : 0;
			
			$_items = wp_get_nav_menu_items( $_menu_id );
			
			$_submenu_items = false;
			
			if( is_array( $_items ) ) {
				$_submenu_items = wpl_galaxy_wp_utils::get_nav_menu_item_children( $item->ID, $_items, true );
			}

			if( $_submenu_items ) {
				
				$item_output .= '<div class="wproto-mega-menu-content">';

				$item_output .= wpl_galaxy_wp_utils::get_submenu_tree( $_submenu_items, $item->ID );				

				$item_output .= '<div class="clear"></div></div>';
				
			}
			
		}
        
		$item_output .= $args->after;

		$output .= apply_filters( 'walker_nav_menu_start_el', $item_output, $item, $depth, $args ); 
	}
}
