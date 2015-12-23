<div class="post-slider">

	<div class="post-slider-carousel">
		<?php foreach( $data['items'] as $item ): ?>
			<?php
				$image_thumb = wpl_galaxy_wp_utils::is_retina() ? 'post-thumb-full-2x' : 'post-thumb-full';
				$image = wp_get_attachment_image_src( $item->ID, $image_thumb );
			?>
			<img src="<?php echo $image[0]; ?>" alt="" />
		<?php endforeach; ?>
	</div>
	<span class="post-slider-prev"><a href="javascript:;"></a></span>
	<span class="post-slider-next"><a href="javascript:;"></a></span>
	<div class="clear"></div>

</div>