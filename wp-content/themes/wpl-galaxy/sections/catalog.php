<?php
	global $wproto_section, $wpl_galaxy_wp;
	$section_data = isset( $wproto_section->data ) ? unserialize( $wproto_section->data ) : array();
	
	$_type = isset( $section_data['display_content_type'] ) ? $section_data['display_content_type'] : 'all';
	$_limit = isset( $section_data['limit'] ) ? absint( $section_data['limit'] ) : 4;
	$_category = isset( $section_data['posts_categories'] ) ? $section_data['posts_categories'] : 0;
	$_orderby = isset( $section_data['order'] ) ? $section_data['order'] : 'ID';
	$_sort = isset( $section_data['sort'] ) ? $section_data['sort'] : 'DESC';
	
	$result = $wpl_galaxy_wp->model->post->get( $_type, $_limit, $_category, $_orderby, $_sort, 'wproto_catalog', 'wproto_catalog_category' );
?>
<!--
					
	CATALOG
						
-->
<?php if( $result->have_posts() ): ?> 
<section id="section-id-<?php echo $wproto_section->ID; ?>" class="new-arrivals wrapper">

	<div class="new-arrivals" data-appear-animation="fadeIn">
						
		<?php if( $wproto_section->title <> '' ): ?>
		<header class="hgroup">
			<h2><?php echo $wproto_section->title; ?></h2>
			<?php if( $wproto_section->subtitle <> '' ): ?>
			<h5><?php echo $wproto_section->subtitle; ?></h5>
			<?php endif; ?>
		</header>
		<?php endif; ?>
							
		<div class="items">
		
			<?php while( $result->have_posts() ): $result->the_post(); ?>
			<div class="item box">
								
				<div class="inside">
				
					<?php
						$post_id = get_the_ID();
						$thumb_name = wpl_galaxy_wp_utils::is_retina() ? 'shop-related-2x' : 'shop-related';
						$img = wp_get_attachment_image_src( get_post_thumbnail_id(), $thumb_name );
					?>
				
					<?php if( has_post_thumbnail() ): ?>
					<a class="thumbnail" href="<?php the_permalink(); ?>">
						<img src="<?php echo $img[0]; ?>" width="180" height="182" alt="" />
					</a>
					<?php endif; ?>

					<div class="additional-info">
							
						<?php
							$attached_images = get_post_meta( $post_id, 'wproto_attached_images', true );
							$product_images_count = is_array( $attached_images ) ? count( $attached_images ) : 0;
							
							$old_price = get_post_meta( $post_id, 'old_price', true );
							$old_price = $old_price <> '' ? wpl_galaxy_wp_front::get_price( $old_price ) : '';
											
							$price = get_post_meta( $post_id, 'price', true );
							$price = $price <> '' ? wpl_galaxy_wp_front::get_price( $price ) : '';
											
							$link_to_buy = get_post_meta( $post_id, 'link_to_buy', true );
						?>
						
						<?php if( $product_images_count > 0 ): ?>
						<div class="product-scroller">
							
							<div class="scroller">
								<?php $i_num = 0; foreach( $attached_images as $id ): $i_num++; if( $i_num > 3 ) break; ?>
								
								<?php
									$_thumb_name = wpl_galaxy_wp_utils::is_retina() ? 'shop-product-preview-small-2x' : 'shop-product-preview-small';
									$_thumb = wp_get_attachment_image_src( $id, $_thumb_name );
								?>
								
								<a href="<?php the_permalink(); ?>" class="zoom image-link first">
									<img width="67" height="68" src="<?php echo $_thumb[0]; ?>" class="attachment-shop_thumbnail" alt="" />
								</a>
								<?php endforeach; ?>
							</div>
									
						</div>
						<?php endif; ?>
						
						<?php if( absint( get_post_meta( $post_id, 'wproto_likes', true ) ) >= $wpl_galaxy_wp->get_option('five_star_likes_count') ): ?>
						<div class="rating">
							<img src="<?php echo get_stylesheet_directory_uri(); ?>/images/star-1<?php echo wpl_galaxy_wp_utils::is_retina() ? '@2x' : '' ?>.png" width="19" height="18" alt="" />
							<img src="<?php echo get_stylesheet_directory_uri(); ?>/images/star-1<?php echo wpl_galaxy_wp_utils::is_retina() ? '@2x' : '' ?>.png" width="19" height="18" alt="" />
							<img src="<?php echo get_stylesheet_directory_uri(); ?>/images/star-1<?php echo wpl_galaxy_wp_utils::is_retina() ? '@2x' : '' ?>.png" width="19" height="18" alt="" />
							<img src="<?php echo get_stylesheet_directory_uri(); ?>/images/star-1<?php echo wpl_galaxy_wp_utils::is_retina() ? '@2x' : '' ?>.png" width="19" height="18" alt="" />
							<img src="<?php echo get_stylesheet_directory_uri(); ?>/images/star-1<?php echo wpl_galaxy_wp_utils::is_retina() ? '@2x' : '' ?>.png" width="19" height="18" alt="" /> 
							<span>(<?php echo get_comments_number(); ?> <?php _e('reviews', 'wproto'); ?>)</span>
						</div>
						<?php else: ?>
						<div class="rating">
							<img src="<?php echo get_stylesheet_directory_uri(); ?>/images/star-2<?php echo wpl_galaxy_wp_utils::is_retina() ? '@2x' : '' ?>.png" width="19" height="18" alt="" />
							<img src="<?php echo get_stylesheet_directory_uri(); ?>/images/star-2<?php echo wpl_galaxy_wp_utils::is_retina() ? '@2x' : '' ?>.png" width="19" height="18" alt="" />
							<img src="<?php echo get_stylesheet_directory_uri(); ?>/images/star-2<?php echo wpl_galaxy_wp_utils::is_retina() ? '@2x' : '' ?>.png" width="19" height="18" alt="" />
							<img src="<?php echo get_stylesheet_directory_uri(); ?>/images/star-2<?php echo wpl_galaxy_wp_utils::is_retina() ? '@2x' : '' ?>.png" width="19" height="18" alt="" />
							<img src="<?php echo get_stylesheet_directory_uri(); ?>/images/star-2<?php echo wpl_galaxy_wp_utils::is_retina() ? '@2x' : '' ?>.png" width="19" height="18" alt="" /> 
							<span>(<?php echo get_comments_number(); ?> <?php _e('reviews', 'wproto'); ?>)</span>
						</div>
						<?php endif; ?>
					</div>

					<a class="title" href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
							
					<p class="desc"><?php echo wpl_galaxy_wp_utils::custom_excerpt( get_the_excerpt(), 65 );  ?></p>
					
					<?php if( $price <> '' ): ?>
					<div class="price"><?php if( $old_price <> ''): ?><span class="old-price"><?php echo $old_price; ?></span><?php endif; ?> <?php echo $price; ?></div>
					<?php endif; ?>
										
					<a href="<?php echo $link_to_buy; ?>" class="button"><?php _e('Buy', 'buy'); ?></a>
					<a href="<?php echo $link_to_buy; ?>" class="button mobile"><?php _e('Buy', 'buy'); ?></a>
										
					<div class="clear"></div>
									
				</div>
								
			</div>
			<?php endwhile; ?>
			
		</div> <!-- /items -->
		
	</div>
</section>
<?php wp_reset_query(); endif; 