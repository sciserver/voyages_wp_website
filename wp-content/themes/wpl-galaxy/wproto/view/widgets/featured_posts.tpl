<?php global $wpl_galaxy_wp; echo $data['args']['before_widget']; ?>

<!-- widget title -->
<?php if ( isset( $data['title'] ) ) : ?>

	<?php echo $data['args']['before_title']; ?>
	
		<?php echo $data['title']; ?>
		
	<?php echo $data['args']['after_title']; ?>
	
<?php endif; ?>

<!-- widget content -->

<?php if ( $data['posts']->have_posts() ): ?>
	<div class="items">
	<?php while ( $data['posts']->have_posts() ): $data['posts']->the_post(); ?>
	
		<?php $has_thumb = has_post_thumbnail(); ?>
	
	<div class="item <?php if( !$has_thumb ): ?>no-thumb<?php endif; ?>">
	
		<?php if( $has_thumb ): ?>
		<div class="thumbnail">
				<?php 
					$thumb = wpl_galaxy_wp_utils::is_retina() ? 'photo-small-2x' : 'photo-small';
					$image = wp_get_attachment_image_src( get_post_thumbnail_id( get_the_ID() ), $thumb );
				?>
			<a href="<?php the_permalink(); ?>"><img src="<?php echo $image[0]; ?>" width="70" height="70" alt="" /></a>
		</div>
		<?php endif; ?>
						
		<div class="text">
			<a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
			<div class="date"><?php the_time( $wpl_galaxy_wp->settings['date_format'] ); ?></div>
		</div>
					
	</div>
	
	<?php endwhile; wp_reset_query(); ?>
	</div>
<?php endif; ?>
				
<?php echo $data['args']['after_widget'];