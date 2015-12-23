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
	$type = $data['instance']['display_categories'] == 'all' ? 'all' : 'category';
	$posts = $wpl_galaxy_wp->model->post->get( $type, $data['instance']['posts_count'], $data['instance']['display_categories'], $data['instance']['order_by'], $data['instance']['sort'], 'wproto_portfolio', 'wproto_portfolio_category', $data['instance']['featured_only'] );
?>

<?php if( $posts->have_posts() ): ?>

	<div class="items">
		<?php while( $posts->have_posts() ): $posts->the_post(); ?>
		<div class="item">
		
			<?php if( has_post_thumbnail() ): ?>
			<div class="thumbnail">
				<?php 
					$thumb = wpl_galaxy_wp_utils::is_retina() ? 'widget-post-2x' : 'widget-post';
					$image = wp_get_attachment_image_src( get_post_thumbnail_id( get_the_ID() ), $thumb );
				?>
				<a href="<?php the_permalink(); ?>"><img src="<?php echo $image[0]; ?>" width="270" alt="" /></a>
			</div>
			<?php endif; ?>
						
			<a class="title" href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
			
			<?php if( $data['instance']['display_excerpt'] == 1 ): ?>
			<div class="excerpt">
				<?php the_excerpt(); ?>
			</div>
			<?php endif; ?>
								
			<a href="<?php the_permalink(); ?>" class="continue-reading"><?php _e('Details', 'wproto'); ?> <i class="arrow-keep-reading"></i></a>

		</div>
		<?php endwhile; wp_reset_query(); ?>
	</div>

<?php endif; ?>

<?php echo $data['args']['after_widget'];