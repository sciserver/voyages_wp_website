<?php if( isset( $data['title'] ) && $data['title'] <> '' ): ?>
<h4><?php echo $data['title']; ?></h4>
<?php endif; ?>

<?php if( $data['posts']->have_posts() ): ?>
<div class="testimonials-holder">
	<div class="items" id="id-<?php echo uniqid(); ?>">

		<?php while( $data['posts']->have_posts() ): $data['posts']->the_post(); ?>
	
		<div class="item">
					
			<div class="text">
				<blockquote>
					<p><?php echo strip_tags( get_the_content() ); ?></p>
					<cite>&nbsp;</cite>
				</blockquote>
			</div>
							
			<div class="author<?php if( !has_post_thumbnail()): ?> no-thumb<?php endif; ?>">
							
				<div class="owl-external control-buttons">
					<div class="prev"></div>
					<div class="next"></div>
				</div>
				
				<?php if( has_post_thumbnail() ): ?>
				<div class="thumbnail">
				
					<?php 
						$thumb = wpl_galaxy_wp_utils::is_retina() ? 'photo-small-2x' : 'photo-small';
						$image = wp_get_attachment_image_src( get_post_thumbnail_id( get_the_ID() ), $thumb );
					?>
				
					<img src="<?php echo $image[0]; ?>" width="70" alt="" />
				</div>
				<?php endif; ?>
								
				<cite>
					<span class="who"><?php the_title(); ?></span>
					<?php echo get_post_meta( get_the_ID(), 'position', true ); ?>
				</cite>
							
			</div>

		</div>
	
		<?php endwhile; wp_reset_query(); ?>

	</div>
</div>
<?php endif; ?>