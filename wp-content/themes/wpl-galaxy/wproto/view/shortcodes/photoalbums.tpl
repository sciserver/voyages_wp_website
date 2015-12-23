<?php
	$limit = isset( $data['limit'] ) && absint( $data['limit'] ) > 0 ? $data['limit'] : 0;
	if( isset( $data['id'] ) && is_numeric( $data['id'] ) && $data['id'] > 0 ):
?>
<div class="photoalbum-holder">
	<?php if( $data['title'] <> '' ): ?>
	<h4><?php echo $data['title']; ?></h4>
	<?php endif; ?>

	<!-- PHOTOALBUM CONTENT -->
	<?php
		$attached_images = get_post_meta( $data['id'], 'wproto_attached_images', true );
							
		if( is_array( $attached_images ) && count( $attached_images ) > 0 ):
	?>
						
	<div class="post-slider">

		<div class="post-slider-carousel">
		<?php $i=0; foreach( $attached_images as $id ): $i++; if( ($i > $limit) && ($limit > 0) ) break; ?>
								
			<?php
				$image_thumb = wpl_galaxy_wp_utils::is_retina() ? 'post-thumb-full-2x' : 'post-thumb-full';
				$image = wp_get_attachment_image_src( $id, $image_thumb );
				$image_full = wp_get_attachment_image_src( $id, 'full' );
			?>
			<a href="<?php echo $image_full[0]; ?>" class="popup"><img src="<?php echo $image[0]; ?>" alt="" /></a>
								
		<?php endforeach; ?>
		</div>
						
		<span class="post-slider-prev"><a href="javascript:;"></a></span>
		<span class="post-slider-next"><a href="javascript:;"></a></span>
		<div class="clear"></div>

	</div>
						
	<?php endif; ?>
</div>
<?php endif; ?>