<?php if( $data['posts']->have_posts() ): ?>

<div class="widget wproto-logos-carousel-widget">

	<?php if( isset( $data['title'] ) && $data['title'] <> '' ): ?>
	<h4 class="widget-title"><?php echo $data['title']; ?></h4>
	<?php endif; ?>

	<div class="items">
		<?php while( $data['posts']->have_posts() ): $data['posts']->the_post(); ?>
		<div class="item">
		
			<?php if( has_post_thumbnail() ): ?>
			<div class="thumbnail">
				<?php 
					$thumb = wpl_galaxy_wp_utils::is_retina() ? 'partners-clients-logo-2x' : 'partners-clients-logo';
					$image = wp_get_attachment_image_src( get_post_thumbnail_id( get_the_ID() ), $thumb );
				?>
				<img src="<?php echo $image[0]; ?>" width="170" alt="" />
			</div>
			<?php endif; ?>

		</div>
		<?php endwhile; wp_reset_query(); ?>
	</div>

</div>

<?php endif; ?>
