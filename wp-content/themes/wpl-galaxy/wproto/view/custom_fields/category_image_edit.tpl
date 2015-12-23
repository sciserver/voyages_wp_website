<?php
	$image_id = absint( $data['category_image_id'] );
	
	if( $image_id == 0 ) {
		$image_preview = wpl_galaxy_wp_utils::is_retina() ? WPROTO_THEME_URL . '/images/admin/category-no-image@2x.jpg' : WPROTO_THEME_URL . '/images/admin/category-no-image.jpg';
	} else {
		$image_preview = wp_get_attachment_image_src( $image_id, wpl_galaxy_wp_utils::is_retina() ? 'wproto-admin-category-thumb-2x' : 'wproto-admin-category-thumb' );
		$image_preview = @$image_preview[0];
	}

?>
<tr class="form-field">
	<th scope="row" valign="top">
		<label><?php _e( 'Category image', 'wproto' ); ?></label>
	</th>
	<td>
		<p class="description"><?php _e( 'Choose an image to use it as a category image (optional)', 'wproto' ); ?></p>
		<input type="hidden" name="term_meta[category_image_id]" id="wproto-category-image-input" value="<?php echo $image_id; ?>" />
		<p class="wproto-cat-img-chooser">
			<img id="wproto-category-image-thumb" src="<?php echo $image_preview; ?>" width="270" height="170" alt="" />
			<input type="button" style="width: auto !important;" class="button button-primary wproto-image-selector" data-src-target="#wproto-category-image-thumb" data-url-target="#wproto-category-image-input" value="<?php _e( 'Select', 'wproto' ); ?>" />
			<input type="button" style="width: auto !important;" class="button wproto-image-remover" data-default-img="<?php echo WPROTO_THEME_URL; ?>/images/admin/category-no-image<?php echo wpl_galaxy_wp_utils::is_retina() ? '@2x' : ''; ?>.jpg" data-src-target="#wproto-category-image-thumb" data-url-target="#wproto-category-image-input"  value="<?php _e( 'Remove', 'wproto' ); ?>" />
		</p>
	</td>
</tr>