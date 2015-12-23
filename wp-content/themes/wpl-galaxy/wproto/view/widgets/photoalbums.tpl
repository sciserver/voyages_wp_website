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
	?>

	<div class="widget-content">
	
		<div class="slider">
			<div class="slides">
				<?php $i=0; foreach( $photos as $id ): $i++; if( $i > $photos_limit ) break; ?>
				
				<?php
					$image_thumb = wpl_galaxy_wp_utils::is_retina() ? 'widget-post-2x' : 'widget-post';
					$image = wp_get_attachment_image_src( $id, $image_thumb );
					$image_full = wp_get_attachment_image_src( $id, 'full' );
					$href = $data['instance']['link_to'] == 'file' ? $image_full[0] : get_permalink( $album_id ); 
				?>
				
				<a <?php if( $data['instance']['link_to'] == 'file' ): ?>class="lightbox"<?php endif; ?> href="<?php echo $href; ?>"><img src="<?php echo $image[0]; ?>" width="270" alt="" /></a>
				<?php endforeach; ?>							
			</div>
			<div class="slider-pagination"></div>
		</div>
						
		<div class="text">
			<a href="<?php echo get_permalink( $album_id ); ?>" class="title"><?php echo $album->post_title; ?></a>
			<div class="icons">
								
				<span class="item-views"><?php wpl_galaxy_wp_front::views( $album_id ); ?></span>
				<?php wpl_galaxy_wp_front::likes( $album_id ); ?>
								
			</div>
		</div>
	
	</div>
	<?php endif; ?>

<?php endif; ?>

<?php echo $data['args']['after_widget'];