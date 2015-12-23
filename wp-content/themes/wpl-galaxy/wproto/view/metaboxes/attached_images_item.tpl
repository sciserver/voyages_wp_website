<?php
	$id = isset( $id ) ? $id : $data['id'];
	// get image
	$image = get_post( $id );
	$image_data = get_post_custom( $id );
	
	$thumb = wpl_galaxy_wp_utils::is_retina() ? 'wproto-admin-thumb-medium-2x' : 'wproto-admin-thumb-medium';
	
?>
<div class="wproto-attached-image-item">
	<input type="hidden" class="wproto-attached-image-item-id" name="wproto_attached_images[]" value="<?php echo $id; ?>" />
	
	<?php $url_arr = wp_get_attachment_image_src( $id, $thumb ); echo '<img width="150" height="150" src="' . $url_arr[0] . '" alt="" />'; ?>
	
	<div class="wproto-attached-image-details-holder">
	
		<table class="wproto-attached-image-details">
			<tr>
				<th><?php _e( 'Title', 'wproto'); ?>:</th>
				<td><?php echo apply_filters( 'the_title', $image->post_title ); ?></td>
			</tr>
			<tr>
				<th><?php _e( 'Alternative text', 'wproto'); ?>:</th>
				<td><?php echo isset( $image_data['_wp_attachment_image_alt'][0] ) ? $image_data['_wp_attachment_image_alt'][0] : ''; ?></td>
			</tr>
			<tr>
				<th><?php _e( 'Caption', 'wproto'); ?>:</th>
				<td><?php echo $image->post_excerpt; ?></td>
			</tr>
			<tr>
				<th><?php _e( 'Description', 'wproto'); ?>:</th>
				<td><?php echo $image->post_content; ?></td>
			</tr>
		</table>
	</div>
	
	<a href="javascript:;" class="wproto-attached-image-edit" data-id="<?php echo $id; ?>"></a>
	<a href="javascript:;" class="wproto-attached-image-delete" data-id="<?php echo $id; ?>"></a>
</div>