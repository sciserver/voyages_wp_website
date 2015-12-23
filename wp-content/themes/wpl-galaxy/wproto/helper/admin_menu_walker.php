<?php
/**
 * Admin nav menu custom fields walker
 **/
class wpl_galaxy_wp_admin_nav_menu_walker extends Walker_Nav_Menu  {

	function start_lvl( &$output, $depth = 0, $args = array() ) {	
		
	}
	
	function end_lvl( &$output, $depth = 0, $args = array() ) {
		
	}
	
	function start_el( &$output, $item, $depth = 0, $args = array(), $current_id = 0 ) {
		global $_wp_nav_menu_max_depth;
	   
		$_wp_nav_menu_max_depth = $depth > $_wp_nav_menu_max_depth ? $depth : $_wp_nav_menu_max_depth;
	
		$indent = ( $depth ) ? str_repeat( "\t", $depth ) : '';
	
		ob_start();
		$item_id = esc_attr( $item->ID );
		$removed_args = array(
			'action',
			'customlink-tab',
			'edit-menu-item',
			'menu-item',
			'page-tab',
			'_wpnonce',
		);
	
		$original_title = '';
		if ( 'taxonomy' == $item->type ) {
			$original_title = get_term_field( 'name', $item->object_id, $item->object, 'raw' );
				if ( is_wp_error( $original_title ) )
					$original_title = false;
		} elseif ( 'post_type' == $item->type ) {
			$original_object = get_post( $item->object_id );
			$original_title = $original_object->post_title;
		}
	
		$classes = array(
			'menu-item menu-item-depth-' . $depth,
			'menu-item-' . esc_attr( $item->object ),
			'menu-item-edit-' . ( ( isset( $_GET['edit-menu-item'] ) && $item_id == $_GET['edit-menu-item'] ) ? 'active' : 'inactive'),
		);
	
		$title = $item->title;
	
		if ( ! empty( $item->_invalid ) ) {
			$classes[] = 'menu-item-invalid';
			/* translators: %s: title of menu item which is invalid */
			$title = sprintf( __( '%s (Invalid)', 'wproto' ), $item->title );
		} elseif ( isset( $item->post_status ) && 'draft' == $item->post_status ) {
			$classes[] = 'pending';
			/* translators: %s: title of menu item in draft status */
			$title = sprintf( __('%s (Pending)', 'wproto'), $item->title );
		}
	
		$title = empty( $item->label ) ? $title : $item->label;
	
	?>
	<li id="menu-item-<?php echo $item_id; ?>" class="<?php echo implode(' ', $classes ); ?>">
		<dl class="menu-item-bar">
			<dt class="menu-item-handle">
				<span class="item-title"><?php echo esc_html( $title ); ?></span>
					<span class="item-controls">
						<span class="item-type"><?php echo esc_html( $item->type_label ); ?></span>
							<span class="item-order hide-if-js">
								<a href="<?php
									echo wp_nonce_url( add_query_arg( array(
													'action' => 'move-up-menu-item',
													'menu-item' => $item_id,
												),
												remove_query_arg($removed_args, admin_url( 'nav-menus.php' ) )
											),
											'move-menu_item'
									);
									?>" class="item-move-up"><abbr>&#8593;</abbr></a>
									|
									<a href="<?php
										echo wp_nonce_url( add_query_arg( array(
												'action' => 'move-down-menu-item',
												'menu-item' => $item_id,
											),
											remove_query_arg($removed_args, admin_url( 'nav-menus.php' ) )
										),
										'move-menu_item'
										);
									?>" class="item-move-down"><abbr>&#8595;</abbr></a>
								</span>
								<a class="item-edit" id="edit-<?php echo $item_id; ?>" href="<?php
									echo ( isset( $_GET['edit-menu-item'] ) && $item_id == $_GET['edit-menu-item'] ) ? admin_url( 'nav-menus.php' ) : add_query_arg( 'edit-menu-item', $item_id, remove_query_arg( $removed_args, admin_url( 'nav-menus.php#menu-item-settings-' . $item_id ) ) );
								?>"><?php _e( 'Edit Menu Item', 'wproto' ); ?></a>
						</span>
					</dt>
				</dl>
	
				<div class="menu-item-settings" id="menu-item-settings-<?php echo $item_id; ?>">
					<?php if( 'custom' == $item->type ) : ?>
						<p class="field-url description description-wide">
							<label for="edit-menu-item-url-<?php echo $item_id; ?>">
								<?php _e( 'URL', 'wproto' ); ?><br />
								<input type="text" id="edit-menu-item-url-<?php echo $item_id; ?>" class="widefat code edit-menu-item-url" name="menu-item-url[<?php echo $item_id; ?>]" value="<?php echo esc_attr( $item->url ); ?>" />
							</label>
						</p>
					<?php endif; ?>
					<p class="description description-thin">
						<label for="edit-menu-item-title-<?php echo $item_id; ?>">
							<?php _e( 'Navigation Label', 'wproto' ); ?><br />
							<input type="text" id="edit-menu-item-title-<?php echo $item_id; ?>" class="widefat edit-menu-item-title" name="menu-item-title[<?php echo $item_id; ?>]" value="<?php echo esc_attr( $item->title ); ?>" />
						</label>
					</p>
					<p class="description description-thin">
						<label for="edit-menu-item-attr-title-<?php echo $item_id; ?>">
							<?php _e( 'Title Attribute', 'wproto' ); ?><br />
							<input type="text" id="edit-menu-item-attr-title-<?php echo $item_id; ?>" class="widefat edit-menu-item-attr-title" name="menu-item-attr-title[<?php echo $item_id; ?>]" value="<?php echo esc_attr( $item->post_excerpt ); ?>" />
						</label>
					</p>
					<p class="field-link-target description">
						<label for="edit-menu-item-target-<?php echo $item_id; ?>">
							<input type="checkbox" id="edit-menu-item-target-<?php echo $item_id; ?>" value="_blank" name="menu-item-target[<?php echo $item_id; ?>]"<?php checked( $item->target, '_blank' ); ?> />
							<?php _e( 'Open link in a new window/tab', 'wproto' ); ?>
						</label>
					</p>
					<p class="field-css-classes description description-thin">
						<label for="edit-menu-item-classes-<?php echo $item_id; ?>">
							<?php _e( 'CSS Classes (optional)', 'wproto' ); ?><br />
							<input type="text" id="edit-menu-item-classes-<?php echo $item_id; ?>" class="widefat code edit-menu-item-classes" name="menu-item-classes[<?php echo $item_id; ?>]" value="<?php echo esc_attr( implode(' ', $item->classes ) ); ?>" />
						</label>
					</p>
					<p class="field-xfn description description-thin">
						<label for="edit-menu-item-xfn-<?php echo $item_id; ?>">
						<?php _e( 'Link Relationship (XFN)', 'wproto' ); ?><br />
						<input type="text" id="edit-menu-item-xfn-<?php echo $item_id; ?>" class="widefat code edit-menu-item-xfn" name="menu-item-xfn[<?php echo $item_id; ?>]" value="<?php echo esc_attr( $item->xfn ); ?>" />
						</label>
					</p>
					<p class="field-description description description-wide">
						<label for="edit-menu-item-description-<?php echo $item_id; ?>">
							<?php _e( 'Description', 'wproto' ); ?><br />
							<textarea id="edit-menu-item-description-<?php echo $item_id; ?>" class="widefat edit-menu-item-description" rows="3" cols="20" name="menu-item-description[<?php echo $item_id; ?>]"><?php echo esc_html( $item->description ); // textarea_escaped ?></textarea>
							<span class="description"><?php _e('The description will be displayed in the menu if the current theme supports it.', 'wproto'); ?></span>
						</label>
					</p>        
					<?php
						/* New fields insertion starts here */
					?>      
					<div style="clear: both"></div>
					<p class="field-custom description description-wide">
						<label for="edit-menu-item-icon-<?php echo $item_id; ?>">
							<?php _e( 'Menu icon', 'wproto' ); ?><br />
							
							<?php echo $item->menu_icon <> '' ? '<i class="wproto-icon-holder ' . $item->menu_icon . ' fa fa-4x"></i> <a href="javascript:;" class="wproto-icon-chooser">' . __( 'Change', 'wproto') . '</a>' : '<i data-name="" class="wproto-icon-holder icon-2x"></i> <a href="javascript:;" class="wproto-icon-chooser">' . __( 'Select icon', 'wproto') . '</a>'; ?>
							<input type="hidden" value="<?php echo $item->menu_icon; ?>" name="menu_item_icon[<?php echo $item_id; ?>]" class="wproto-icon-holder-input" />
						</label>
					</p>
					<p class="field-custom description description-wide">
						<label>
							<input <?php echo $item->dont_display_as_link == 'yes' ? 'checked="checked"' : ''; ?> type="checkbox" name="menu_item_dont_display_as_link[<?php echo $item_id; ?>]" value="yes" /> <?php _e( 'Do not display as link', 'wproto' ); ?>
						</label>
						<?php if( $depth == 0 ): ?>
						<br />
						<label>
							<input <?php echo $item->mega_menu == 'yes' ? 'checked="checked"' : ''; ?> type="checkbox" name="menu_item_mega_menu[<?php echo $item_id; ?>]" value="yes" /> <?php _e( '&laquo;Mega menu&raquo; style', 'wproto' ); ?>
						</label>
						<?php endif; ?>
					</p>
					<p class="field-custom description description-wide" style="margin-bottom: 4px;">
						<strong><?php _e( 'Hide this menu item at', 'wproto' ); ?>:</strong>
					</p>
					<p class="field-custom description description-wide">
						<label>
							<input <?php echo $item->hide_large_desktop == 'yes' ? 'checked="checked"' : ''; ?> type="checkbox" name="menu_item_hide_large_desktop[<?php echo $item_id; ?>]" value="yes" /> <?php _e( 'Large Desktops', 'wproto' ); ?>
						</label><br />
						<label>
							<input <?php echo $item->hide_small_desktop == 'yes' ? 'checked="checked"' : ''; ?> type="checkbox" name="menu_item_hide_small_desktop[<?php echo $item_id; ?>]" value="yes" /> <?php _e( 'Desktop, width less than 1199px', 'wproto' ); ?>
						</label><br />
						<label>
							<input <?php echo $item->hide_tablet == 'yes' ? 'checked="checked"' : ''; ?> type="checkbox" name="menu_item_hide_tablet[<?php echo $item_id; ?>]" value="yes" /> <?php _e( 'Tablet', 'wproto' ); ?>
						</label><br />
						<label>
							<input <?php echo $item->hide_phone == 'yes' ? 'checked="checked"' : ''; ?> type="checkbox" name="menu_item_hide_phone[<?php echo $item_id; ?>]" value="yes" /> <?php _e( 'Phone', 'wproto' ); ?>
						</label>
					</p>
					<?php
						/* New fields insertion ends here */
					?>
					<div class="menu-item-actions description-wide submitbox">
						<?php if( 'custom' != $item->type && $original_title !== false ) : ?>
						<p class="link-to-original">
							<?php printf( __('Original: %s', 'wproto'), '<a href="' . esc_attr( $item->url ) . '">' . esc_html( $original_title ) . '</a>' ); ?>
						</p>
						<?php endif; ?>
						<a class="item-delete submitdelete deletion" id="delete-<?php echo $item_id; ?>" href="<?php
						echo wp_nonce_url( add_query_arg( array(
								'action' => 'delete-menu-item',
								'menu-item' => $item_id,
							),
							remove_query_arg($removed_args, admin_url( 'nav-menus.php' ) ) ),
							'delete-menu_item_' . $item_id
						); ?>"><?php _e('Remove', 'wproto'); ?></a> <span class="meta-sep"> | </span> <a class="item-cancel submitcancel" id="cancel-<?php echo $item_id; ?>" href="<?php echo esc_url( add_query_arg( array('edit-menu-item' => $item_id, 'cancel' => time()), remove_query_arg( $removed_args, admin_url( 'nav-menus.php' ) ) ) ); ?>#menu-item-settings-<?php echo $item_id; ?>"><?php _e('Cancel', 'wproto'); ?></a>
					</div>
	
					<input class="menu-item-data-db-id" type="hidden" name="menu-item-db-id[<?php echo $item_id; ?>]" value="<?php echo $item_id; ?>" />
					<input class="menu-item-data-object-id" type="hidden" name="menu-item-object-id[<?php echo $item_id; ?>]" value="<?php echo esc_attr( $item->object_id ); ?>" />
					<input class="menu-item-data-object" type="hidden" name="menu-item-object[<?php echo $item_id; ?>]" value="<?php echo esc_attr( $item->object ); ?>" />
					<input class="menu-item-data-parent-id" type="hidden" name="menu-item-parent-id[<?php echo $item_id; ?>]" value="<?php echo esc_attr( $item->menu_item_parent ); ?>" />
					<input class="menu-item-data-position" type="hidden" name="menu-item-position[<?php echo $item_id; ?>]" value="<?php echo esc_attr( $item->menu_order ); ?>" />
					<input class="menu-item-data-type" type="hidden" name="menu-item-type[<?php echo $item_id; ?>]" value="<?php echo esc_attr( $item->type ); ?>" />
				</div><!-- .menu-item-settings-->
				<ul class="menu-item-transport"></ul>
			<?php
	    
				$output .= ob_get_clean();

		}
}
