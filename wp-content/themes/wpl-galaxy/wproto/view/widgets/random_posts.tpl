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
	
	<div class="item">
	
		<?php if( has_post_thumbnail() && $data['instance']['display_thumbnails'] == 1 ): ?>
		<div class="thumbnail">
				<?php 
					$thumb = wpl_galaxy_wp_utils::is_retina() ? 'widget-recent-posts-2x' : 'widget-recent-posts';
					$image = wp_get_attachment_image_src( get_post_thumbnail_id( get_the_ID() ), $thumb );
				?>
				<a href="<?php the_permalink(); ?>"><img src="<?php echo $image[0]; ?>" width="270" alt="" /></a>
		</div>
		<?php endif; ?>
						
		<a class="title" href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
						
		<span class="date"><?php the_time( $wpl_galaxy_wp->settings['date_format'] ); ?></span>
						
		<?php if( $data['instance']['display_comments_count'] == 1 ): ?>
			<a href="<?php comments_link(); ?>" class="comments"><i class="fa fa-comments-o"></i> <?php echo comments_number('0', '1', '%'); ?></a>
		<?php endif; ?>
					
	</div>
	
	<?php endwhile; wp_reset_query(); ?>
	</div>
<?php endif; ?>
				
<?php echo $data['args']['after_widget'];