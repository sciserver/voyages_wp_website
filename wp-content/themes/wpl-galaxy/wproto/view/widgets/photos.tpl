<?php echo $data['args']['before_widget']; ?>

<!-- widget title -->
<?php if ( isset( $data['title'] ) ) : ?>

	<?php echo $data['args']['before_title']; ?>
	
		<?php echo $data['title']; ?>
		
	<?php echo $data['args']['after_title']; ?>
	
<?php endif; ?>

<!-- widget content -->

<?php
	global $wpl_galaxy_wp;
	$album_id = isset( $data['instance']['album'] ) ? absint( $data['instance']['album'] ) : 0;
?>

<?php if( $album_id > 0 ): ?>

	<?php
		$album = get_post( $album_id );
		$photos = get_post_meta( $album_id, 'wproto_attached_images', true );
		$photos_limit = $data['instance']['posts_count'];
		if( is_array( $photos ) && count( $photos ) > 0 ):
		
			$i=0; foreach( $photos as $id ): $i++; if( $i > $photos_limit ) break;
			
				$image_thumb = wpl_galaxy_wp_utils::is_retina() ? 'shop-product-small-2x' : 'shop-product-small';
				$image = wp_get_attachment_image_src( $id, $image_thumb );
				$image_full = wp_get_attachment_image_src( $id, 'full' );
				$href = $data['instance']['link_to'] == 'file' ? $image_full[0] : get_permalink( $album_id );
	?>

		<a class="<?php if( $data['instance']['link_to'] == 'file' ): ?>lightbox<?php endif; if( $photos_limit == $i ): ?> last<?php endif; ?>" href="<?php echo $href; ?>"><img src="<?php echo $image[0]; ?>" width="87" height="87" alt="" /><span class="mask"><i class="fa zoom fa-search-plus"></i></span></a>

	<?php endforeach; endif; ?>

<?php endif; ?>

<?php echo $data['args']['after_widget'];