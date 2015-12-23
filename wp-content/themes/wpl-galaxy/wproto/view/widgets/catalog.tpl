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
	$stylesheet_dir = get_bloginfo('stylesheet_directory');
	$type = $data['instance']['display_categories'] == 'all' ? 'all' : 'category';
	$posts = $wpl_galaxy_wp->model->post->get( $type, $data['instance']['posts_count'], $data['instance']['display_categories'], $data['instance']['order_by'], $data['instance']['sort'], 'wproto_catalog', 'wproto_catalog_category', $data['instance']['featured_only'], $data['instance']['sticky_only'] );
?>

<?php if( $posts->have_posts() ): ?>

	<div class="items">
	
		<?php while( $posts->have_posts() ): $posts->the_post(); ?>
		
		<div class="item">
					
			<?php
				global $wpl_galaxy_wp; 				
				$post_id = get_the_ID();
				$link = $data['instance']['link_to'] == 'custom_url' ? get_post_meta( $post_id, 'link_to_buy', true ) : get_permalink( $post_id );
				$likes_count = absint( get_post_meta( $post_id, 'wproto_likes', true ) );
				
				$old_price = get_post_meta( $post_id, 'old_price', true );
				$old_price = $old_price <> '' ? wpl_galaxy_wp_front::get_price( $old_price ) : '';
											
				$price = get_post_meta( $post_id, 'price', true );
				$price = $price <> '' ? wpl_galaxy_wp_front::get_price( $price ) : '';
				
			?>
					
			<?php if( has_post_thumbnail() && $data['instance']['display_thumb'] == 1 ): ?>
			<div class="thumbnail">
				<?php 
					$thumb = wpl_galaxy_wp_utils::is_retina() ? 'widget-product-2x' : 'widget-product';
					$image = wp_get_attachment_image_src( get_post_thumbnail_id( $post_id ), $thumb );
				?>
				<a href="<?php the_permalink(); ?>"><img src="<?php echo $image[0]; ?>" width="270" alt="" /></a>
			</div>
			<?php endif; ?>
						
			<a class="title" href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
			
			<?php if( $likes_count >= $wpl_galaxy_wp->get_option('five_star_likes_count') ): ?>
			<div class="rating">
				<img src="<?php echo $stylesheet_dir; ?>/images/star-1.png" width="19" height="18" alt="" />
				<img src="<?php echo $stylesheet_dir; ?>/images/star-1.png" width="19" height="18" alt="" />
				<img src="<?php echo $stylesheet_dir; ?>/images/star-1.png" width="19" height="18" alt="" />
				<img src="<?php echo $stylesheet_dir; ?>/images/star-1.png" width="19" height="18" alt="" />
				<img src="<?php echo $stylesheet_dir; ?>/images/star-1.png" width="19" height="18" alt="" />
			</div>
			<?php endif; ?>
								
			<?php if( $data['instance']['display_excerpt'] == 1 ): ?>
			<div class="excerpt">
				<?php the_excerpt(); ?>
			</div>
			<?php endif; ?>
			
			<?php if( $data['instance']['display_price'] == 1 && $price <> '' ): ?>
			<div class="price">
				<?php if( $old_price <> '' ): ?>
				<span class="old-price"><?php echo $old_price; ?></span>
				<?php endif; ?>
				<?php echo $price; ?>
			</div>
			<?php endif; ?>

			<a href="<?php echo $link; ?>" class="button"><?php _e('Buy it', 'wproto'); ?></a>

		</div>
		
		<?php endwhile; wp_reset_query(); ?>
	
	</div>

<?php endif; ?>

<?php echo $data['args']['after_widget'];