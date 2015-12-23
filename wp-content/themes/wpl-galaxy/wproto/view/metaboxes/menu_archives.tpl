<div id="posttype-archive" class="posttypediv">
	<div class="tabs-panel tabs-panel-active">
 		<ul class="categorychecklist form-no-clear">

			<?php
				$home_page_id = get_option('page_on_front');
				$posts_page_id = get_option('page_for_posts');
			?>

			<?php if( absint( $home_page_id ) > 0 ): ?>
			<li>
				<label class="menu-item-title"><input type="checkbox" class="menu-item-checkbox" name="menu-item[-1][menu-item-object-id]" value="<?php echo $home_page_id; ?>" /> <?php _e( 'Home page', 'wproto'); ?></label>
				<input type="hidden" class="menu-item-object" name="menu-item[-1][menu-item-object]" value="page" />
				<input type="hidden" class="menu-item-parent-id" name="menu-item[-1][menu-item-parent-id]" value="0" />
				<input type="hidden" class="menu-item-type" name="menu-item[-1][menu-item-type]" value="post_type" />
				<input type="hidden" class="menu-item-title" name="menu-item[-1][menu-item-title]" value="<?php _e( 'Home page', 'wproto'); ?>" />
				<input type="hidden" class="menu-item-url" name="menu-item[-1][menu-item-url]" value="<?php echo home_url(); ?>" />
				<input type="hidden" value="custom" name="menu-item[-1][menu-item-type]" />
			</li>
			<?php endif; ?>

			<?php if( absint( $posts_page_id ) > 0 ): ?>
			<li>
				<label class="menu-item-title"><input type="checkbox" class="menu-item-checkbox" name="menu-item[-2][menu-item-object-id]" value="<?php echo $posts_page_id; ?>" /> <?php _e( 'Blog', 'wproto'); ?></label>
				<input type="hidden" class="menu-item-object" name="menu-item[-2][menu-item-object]" value="page" />
				<input type="hidden" class="menu-item-parent-id" name="menu-item[-2][menu-item-parent-id]" value="0" />
				<input type="hidden" class="menu-item-type" name="menu-item[-2][menu-item-type]" value="post_type" />
				<input type="hidden" class="menu-item-title" name="menu-item[-2][menu-item-title]" value="<?php _e( 'Blog', 'wproto'); ?>" />
				<input type="hidden" class="menu-item-url" name="menu-item[-2][menu-item-url]" value="<?php echo get_permalink( $posts_page_id ); ?>" />
				<input type="hidden" value="custom" name="menu-item[-2][menu-item-type]" />
			</li>
			<?php endif; ?>

			<li>
				<label class="menu-item-title"><input type="checkbox" class="menu-item-checkbox" name="menu-item[-3][menu-item-object-id]" value="wproto_video" /> <?php _e( 'Videos', 'wproto'); ?></label>
				<input type="hidden" class="menu-item-title" name="menu-item[-3][menu-item-title]" value="<?php _e( 'Videos', 'wproto'); ?>" />
				<input type="hidden" class="menu-item-url" name="menu-item[-3][menu-item-url]" value="<?php echo get_post_type_archive_link( 'wproto_video' ); ?>" />
				<input type="hidden" value="custom" name="menu-item[-3][menu-item-type]" />
			</li>
			
			<li>
				<label class="menu-item-title"><input type="checkbox" class="menu-item-checkbox" name="menu-item[-4][menu-item-object-id]" value="wproto_photoalbums" /> <?php _e( 'Photo albums', 'wproto'); ?></label>
				<input type="hidden" class="menu-item-title" name="menu-item[-4][menu-item-title]" value="<?php _e( 'Photo albums', 'wproto'); ?>" />
				<input type="hidden" class="menu-item-url" name="menu-item[-4][menu-item-url]" value="<?php echo get_post_type_archive_link( 'wproto_photoalbums' ); ?>" />
				<input type="hidden" value="custom" name="menu-item[-4][menu-item-type]" />
			</li>
			
			<li>
				<label class="menu-item-title"><input type="checkbox" class="menu-item-checkbox" name="menu-item[-5][menu-item-object-id]" value="wproto_catalog" /> <?php _e( 'Catalog', 'wproto'); ?></label>
				<input type="hidden" class="menu-item-title" name="menu-item[-5][menu-item-title]" value="<?php _e( 'Catalog', 'wproto'); ?>" />
				<input type="hidden" class="menu-item-url" name="menu-item[-5][menu-item-url]" value="<?php echo get_post_type_archive_link( 'wproto_catalog' ); ?>" />
				<input type="hidden" value="custom" name="menu-item[-5][menu-item-type]" />
			</li>
			
			<li>
				<label class="menu-item-title"><input type="checkbox" class="menu-item-checkbox" name="menu-item[-6][menu-item-object-id]" value="wproto_portfolio" /> <?php _e( 'Portfolio', 'wproto'); ?></label>
				<input type="hidden" class="menu-item-title" name="menu-item[-6][menu-item-title]" value="<?php _e( 'Portfolio', 'wproto'); ?>" />
				<input type="hidden" class="menu-item-url" name="menu-item[-6][menu-item-url]" value="<?php echo get_post_type_archive_link( 'wproto_portfolio' ); ?>" />
				<input type="hidden" value="custom" name="menu-item[-6][menu-item-type]" />
			</li>
			
			<?php if( wpl_galaxy_wp_utils::isset_woocommerce() ): ?>
			
			<?php $shop_page_id = woocommerce_get_page_id( 'shop' ); ?>
			
			<li>
				<label class="menu-item-title"><input type="checkbox" class="menu-item-checkbox" name="menu-item[-7][menu-item-object-id]" value="<?php echo $shop_page_id; ?>" /> <?php _e( 'Shop', 'wproto'); ?></label>
				<input type="hidden" class="menu-item-object" name="menu-item[-7][menu-item-object]" value="page" />
				<input type="hidden" class="menu-item-parent-id" name="menu-item[-7][menu-item-parent-id]" value="0" />
				<input type="hidden" class="menu-item-type" name="menu-item[-7][menu-item-type]" value="post_type" />
				<input type="hidden" class="menu-item-title" name="menu-item[-7][menu-item-title]" value="<?php _e( 'Shop', 'wproto'); ?>" />
				<input type="hidden" class="menu-item-url" name="menu-item[-7][menu-item-url]" value="<?php echo get_permalink( $shop_page_id ); ?>" />
				<input type="hidden" value="custom" name="menu-item[-7][menu-item-type]" />
			</li>
			
			<?php endif; ?>

		</ul>
	</div>
	<p class="button-controls">
		<span class="list-controls">
			<a href="nav-menus.php?page-tab=all&amp;selectall=1#posttype-archive" class="select-all"><?php _e( 'Select All', 'wproto'); ?></a>
		</span>
		<span class="add-to-menu">
			<input type="submit" class="button-secondary submit-add-to-menu right" value="<?php _e( 'Add to Menu', 'wproto'); ?>" name="add-post-type-menu-item" id="submit-posttype-archive">
			<span class="spinner"></span>
		</span>
	</p>
</div>