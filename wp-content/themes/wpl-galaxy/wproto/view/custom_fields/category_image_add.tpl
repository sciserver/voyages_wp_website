<div class="form-field">
	<label><?php _e( 'Category image', 'wproto' ); ?></label>
	<p class="description"><?php _e( 'Choose an image to use it as a category image (optional)', 'wproto' ); ?></p>
	<input type="hidden" name="term_meta[category_image_id]" id="wproto-category-image-input" value="" />
</div>

<p class="wproto-cat-img-chooser">
	<img id="wproto-category-image-thumb" src="<?php echo WPROTO_THEME_URL; ?>/images/admin/noimage<?php echo wpl_galaxy_wp_utils::is_retina() ? '-2x' : ''; ?>.gif" width="110" height="85" alt="" />
	<a href="javascript:;" class="button button-primary wproto-image-selector" data-src-target="#wproto-category-image-thumb" data-url-target="#wproto-category-image-input"><?php _e( 'Select', 'wproto' ); ?></a>
	<a href="javascript:;" class="button wproto-image-remover" data-default-img="<?php echo WPROTO_THEME_URL; ?>/images/admin/noimage.gif" data-src-target="#wproto-category-image-thumb" data-url-target="#wproto-category-image-input"><?php _e( 'Remove', 'wproto' ); ?></a>
</p>