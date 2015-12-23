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
	$posts = $wpl_galaxy_wp->model->post->get( $type, $data['instance']['posts_count'], $data['instance']['display_categories'], $data['instance']['order_by'], $data['instance']['sort'], 'post', 'category', $data['instance']['featured_only'], $data['instance']['sticky_only'] );
?>

<?php if( $posts->have_posts() ): ?>

	<div class="items">
	
		<?php while( $posts->have_posts() ): $posts->the_post(); ?>
		
		<div class="item">
		
			<?php if( has_post_thumbnail() && $data['instance']['display_thumb'] == 1 ): ?>
			<div class="thumbnail">
				<?php 
					$thumb = wpl_galaxy_wp_utils::is_retina() ? 'widget-post-2x' : 'widget-post';
					$image = wp_get_attachment_image_src( get_post_thumbnail_id( get_the_ID() ), $thumb );
				?>
				<a href="<?php the_permalink(); ?>"><img src="<?php echo $image[0]; ?>" width="270" alt="" /></a>
			</div>
			<?php endif; ?>
						
			<a class="title" href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
						
			<header>
				<span class="date"><?php the_time( $wpl_galaxy_wp->settings['date_format'] ); ?></span>			
			</header>
			
			<?php if( $data['instance']['display_excerpt'] == 1 ): ?>
			<div class="excerpt">
				<?php the_excerpt(); ?>
			</div>
			<?php endif; ?>
							
			<footer>
				<span class="author"><strong><?php _e('By', 'wproto'); ?></strong> <?php the_author_posts_link(); ?></span>
				<?php
					$cats_list = wpl_galaxy_wp_front::get_valid_category_list(', ');
					if( $cats_list <> '' ):
				?>
				<strong><?php _e('In', 'wproto'); ?></strong> <?php echo $cats_list; ?>
				<?php endif; ?> 
				<div class="likes-views">
					<?php if( $data['instance']['display_likes'] == 1 ): ?>
						<span class="item">
							<?php wpl_galaxy_wp_front::likes( get_the_ID() ); ?>
						</span>
					<?php endif; ?>
					<?php if( $data['instance']['display_views'] == 1 ): ?>
						<span class="item">
							<?php wpl_galaxy_wp_front::views( get_the_ID() ); ?>
						</span>
					<?php endif; ?>
					<?php if( $data['instance']['display_comments_count'] == 1 ): ?>
						<span class="item">
							<a href="<?php comments_link(); ?>" class="comments"><i class="fa fa-comments-o"></i> <?php echo comments_number('0', '1', '%'); ?></a>
						</span>
					<?php endif; ?>
				</div>	
			</footer>
								
			<a href="<?php the_permalink(); ?>" class="continue-reading"><?php _e('Keep reading', 'wproto'); ?> <i class="arrow-keep-reading"></i></a>

		</div>
		
		<?php endwhile; wp_reset_query(); ?>
	
	</div>

<?php endif; ?>

<?php echo $data['args']['after_widget'];