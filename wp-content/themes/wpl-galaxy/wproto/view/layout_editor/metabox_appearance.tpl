<?php
	$wproto_post_hide_title = isset( $data['wproto_post_hide_title'] ) ? $data['wproto_post_hide_title'] : 'no';
	$wproto_post_hide_featured_image = isset( $data['wproto_post_hide_featured_image'] ) ? $data['wproto_post_hide_featured_image'] : 'no';
	$wproto_post_masonry_size = isset( $data['wproto_post_masonry_size'] ) ? $data['wproto_post_masonry_size'] : 'default';
	$wproto_post_display_related_posts = isset( $data['wproto_post_display_related_posts'] ) ? $data['wproto_post_display_related_posts'] : 'yes';
	$wproto_post_display_related_posts_type = isset( $data['wproto_post_display_related_posts_type'] ) ? $data['wproto_post_display_related_posts_type'] : 'same';
	
	$wproto_post_related_posts_block_title = isset( $data['wproto_post_related_posts_block_title'] ) ? $data['wproto_post_related_posts_block_title'] : __( 'Related posts', 'wproto');
	$wproto_post_related_posts_block_subtitle = isset( $data['wproto_post_related_posts_block_subtitle'] ) ? $data['wproto_post_related_posts_block_subtitle'] : __( 'posts can interested you and are related', 'wproto');
?>

<table class="form-table wproto-form-table">
	<tr>
		<th class="yesno-input"><label><?php _e( 'Hide page title and breadcrumbs', 'wproto' ); ?>:</label></th>
		<td>
		
			<div class="field switch">
				<label class="cb-enable <?php echo $wproto_post_hide_title == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
				<label class="cb-disable <?php echo $wproto_post_hide_title == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
				<input name="wproto_settings[wproto_post_hide_title]" type="hidden" value="<?php echo $wproto_post_hide_title; ?>" />
				<div class="clear"></div>
			</div>
		
		</td>
	</tr>
	<?php if( !in_array( $data['post_type'], array('page', 'product', 'wproto_catalog', 'wproto_video', 'wproto_photoalbums') ) ): ?>
	<tr>
		<th class="yesno-input"><label><?php _e( 'Hide featured image at post page', 'wproto' ); ?>:</label></th>
		<td>
		
			<div class="field switch">
				<label class="cb-enable <?php echo $wproto_post_hide_featured_image == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
				<label class="cb-disable <?php echo $wproto_post_hide_featured_image == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
				<input name="wproto_settings[wproto_post_hide_featured_image]" type="hidden" value="<?php echo $wproto_post_hide_featured_image; ?>" />
				<div class="clear"></div>
			</div>
		
		</td>
	</tr>
	<?php endif; ?>
	<?php if( !in_array( $data['post_type'], array('page', 'wproto_photoalbums') ) ): ?>
	<tr>
		<th class="yesno-input"><label><?php _e( 'Display related posts block', 'wproto' ); ?>:</label></th>
		<td>
		
			<div class="field switch">
				<label class="cb-enable <?php echo $wproto_post_display_related_posts == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
				<label class="cb-disable <?php echo $wproto_post_display_related_posts == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
				<input data-toggle-element=".wproto-repated-posts-options" name="wproto_settings[wproto_post_display_related_posts]" type="hidden" value="<?php echo $wproto_post_display_related_posts; ?>" />
				<div class="clear"></div>
			</div>
			
			<p style="<?php echo $wproto_post_display_related_posts != 'yes' ? 'display: none;' : ''; ?>">
				<select id="wproto_post_display_related_posts_type" class="wproto-repated-posts-options select" name="wproto_settings[wproto_post_display_related_posts_type]">
					<option value="same"><?php _e( 'Display related posts from same category', 'wproto' ); ?></option>
					<option <?php echo $wproto_post_display_related_posts_type == 'any' ? 'selected="selected"' : ''; ?> value="any"><?php _e( 'Display random posts from any category', 'wproto' ); ?></option>
				</select>
			</p>
		
		</td>
	</tr>
	<?php
		global $wpl_galaxy_wp;
		$common_related_posts_block = $wpl_galaxy_wp->get_option( 'common_related_posts_block');
		$common_related_posts_block = $common_related_posts_block != NULL ? $common_related_posts_block : 'yes';
		if( $common_related_posts_block == 'no' ):
	?>
	<tr class="wproto-repated-posts-options" style="<?php echo $wproto_post_display_related_posts != 'yes' ? 'display: none;' : ''; ?>"> 
		<th><label for="wproto_post_related_posts_block_title"><?php _e('Related posts block title', 'wproto'); ?>:</label></th>
		<td>
		
			<input type="text" class="text" name="wproto_settings[wproto_post_related_posts_block_title]" id="wproto_post_related_posts_block_title" value="<?php echo $wproto_post_related_posts_block_title; ?>" />
		
		</td>
	</tr>
	<tr class="wproto-repated-posts-options" style="<?php echo $wproto_post_display_related_posts != 'yes' ? 'display: none;' : ''; ?>">
		<th><label for="wproto_post_related_posts_block_subtitle"><?php _e('Related posts block sub-title', 'wproto'); ?>:</label></th>
		<td>
		
			<input type="text" class="text" name="wproto_settings[wproto_post_related_posts_block_subtitle]" id="wproto_post_related_posts_block_subtitle" value="<?php echo $wproto_post_related_posts_block_subtitle; ?>" />
		
		</td>
	</tr>
	<?php endif; ?>
	
	<?php endif; ?>
	<?php if( !in_array( $data['post_type'], array('page') ) ): ?>
	<tr>
		<th>
			<label for="wproto_post_masonry_size"><?php _e( 'Post size', 'wproto' ); ?>:</label><br />
			<p class="description"><?php _e( 'Will be applied only for Masonry Layout', 'wproto' ); ?></p>
		</th>
		<td>
		
			<select class="select" id="wproto_post_masonry_size" name="wproto_settings[wproto_post_masonry_size]">
				<option value="default"><?php _e( 'Default', 'wproto' ); ?></option>
				<option <?php echo $wproto_post_masonry_size == 'big' ? 'selected="selected"' : ''; ?> value="big"><?php _e( 'Big', 'wproto' ); ?></option>
			</select>
		
		</td>
	</tr>
	<?php endif; ?>
</table>