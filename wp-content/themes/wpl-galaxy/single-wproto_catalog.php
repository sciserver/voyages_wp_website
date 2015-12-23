<?php get_header(); global $wpl_galaxy_wp; ?>

	<!-- 
	
		CONTENT SECTION
		
	-->
	
	<div id="content" class="wrapper">
		<div class="grid">

			<section class="<?php wpl_galaxy_wp_front::content_classes(); ?>">
				
				<article class="post">
				
					<?php
						if( have_posts() ): while ( have_posts() ) :
							the_post();
							$post_id = get_the_ID();
							$page_settings = $wpl_galaxy_wp->model->post->get_post_custom( $post_id );
						?>
				
					<!--
					
						POST HEADER
						
					-->
				
					<?php wpl_galaxy_wp_front::post_header(); ?>
					
					<!--
					
						POST CONTENT
						
					-->
					<div class="ib post-content">
					
						<div class="post-text">
						
							<?php
								$attached_images = get_post_meta( $post_id, 'wproto_attached_images', true );
								$product_images_count = is_array( $attached_images ) ? count( $attached_images ) : 0;
							?>
						
							<div class="product <?php echo $product_images_count <= 0 ? 'no-images' : ''; ?>">
							<!--
								Product images
							-->
							<?php
								if( is_array( $attached_images ) && $product_images_count > 0 ):
							?>
								<div class="images">
									<?php if( isset( $page_settings->badge ) && $page_settings->badge == 'onsale' ): ?>
									<span class="sale" data-appear-animation="rotateIn"><?php _e('Sale', 'wproto'); ?></span>
									<?php endif; ?>
									<?php if( isset( $page_settings->badge ) && $page_settings->badge == 'best_price' ): ?>
									<span class="best-price" data-appear-animation="rotateIn"><?php _e('Best<br/>Price', 'wproto'); ?></span>
									<?php endif; ?>
									
									<?php
										$main_image = wp_get_attachment_image_src( $attached_images[0], 'shop-product-big' );
										$main_image_2x = wp_get_attachment_image_src( $attached_images[0], 'shop-product-big-2x' );
									?>
									
									<a href="<?php echo $main_image_2x[0]; ?>" class="woocommerce-main-image image-link zoom"><img width="360" height="369" src="<?php echo wpl_galaxy_wp_utils::is_retina() ? $main_image_2x[0] : $main_image[0]; ?>" class="attachment-shop_single wp-post-image" alt="" title="" /></a>
									
									<?php if( $product_images_count >= 1 ): ?>
									<div class="thumbnails product-scroller">
							
										<div class="scroller">
											<?php
												foreach( $attached_images as $id ):
													$thumb_name = wpl_galaxy_wp_utils::is_retina() ? 'shop-product-preview-small-2x' : 'shop-product-preview-small';
													$thumb = wp_get_attachment_image_src( $id, $thumb_name );
													$image_2x = wp_get_attachment_image_src( $id, 'shop-product-big-2x' );
													$img_medium = wp_get_attachment_image_src( $id, wpl_galaxy_wp_utils::is_retina() ? 'shop-product-big-2x' : 'shop-product-big' );
													$img_full = wp_get_attachment_image_src( $id, 'full' );
											?>
											<a data-full-src="<?php echo $img_full[0]; ?>" data-medium-src="<?php echo $img_medium[0]; ?>" href="<?php echo $image_2x[0]; ?>" class="small-image-link first">
												<img width="67" height="68" src="<?php echo $thumb[0]; ?>" class="attachment-shop_thumbnail" alt="" />
											</a>
											<?php endforeach; ?>
										</div>
									
									</div>
									<?php endif; ?>
									
								</div>
							
							<?php endif; ?>
							
								<div class="summary entry-summary">
								
									<header>
									
										<?php
											$old_price = get_post_meta( $post_id, 'old_price', true );
											$old_price = $old_price <> '' ? wpl_galaxy_wp_front::get_price( $old_price ) : '';
											
											$price = get_post_meta( $post_id, 'price', true );
											$price = $price <> '' ? wpl_galaxy_wp_front::get_price( $price ) : '';
											
											$link_to_buy = get_post_meta( $post_id, 'link_to_buy', true );
											
										?>
									
										<?php if( $old_price <> '' ): ?>
										<span class="old-price"><?php echo $old_price; ?></span>
										<?php endif; ?>
										
										<?php if( $price <> '' ): ?>
										<span class="price"><?php echo $price; ?></span>
										<?php endif; ?>
										
										<?php if( $link_to_buy <> '' ): ?>
										<span class="add-to-cart">
											<a href="<?php echo $link_to_buy; ?>" class="button"><?php _e('Buy', 'wproto'); ?></a>
										</span>
										<?php endif; ?>
										
										<?php if( absint( get_post_meta( $post_id, 'wproto_likes', true ) ) >= $wpl_galaxy_wp->get_option('five_star_likes_count') ): ?>
										<div class="rating">
											<img src="<?php echo get_stylesheet_directory_uri(); ?>/images/star-1<?php echo wpl_galaxy_wp_utils::is_retina() ? '@2x' : '' ?>.png" width="19" height="18" alt="" />
											<img src="<?php echo get_stylesheet_directory_uri(); ?>/images/star-1<?php echo wpl_galaxy_wp_utils::is_retina() ? '@2x' : '' ?>.png" width="19" height="18" alt="" />
											<img src="<?php echo get_stylesheet_directory_uri(); ?>/images/star-1<?php echo wpl_galaxy_wp_utils::is_retina() ? '@2x' : '' ?>.png" width="19" height="18" alt="" />
											<img src="<?php echo get_stylesheet_directory_uri(); ?>/images/star-1<?php echo wpl_galaxy_wp_utils::is_retina() ? '@2x' : '' ?>.png" width="19" height="18" alt="" />
											<img src="<?php echo get_stylesheet_directory_uri(); ?>/images/star-1<?php echo wpl_galaxy_wp_utils::is_retina() ? '@2x' : '' ?>.png" width="19" height="18" alt="" />
										</div>
										<?php endif; ?>
									
									</header>
									
									<div class="product-description">
										<?php the_content(); ?>
										
										<?php wp_link_pages('before=<div class="pagination post-paginate">&after=</div>&next_or_number=next'); ?>
										
									</div>
									
									<footer>
									
										<p>
											<span class="post-like"><?php wpl_galaxy_wp_front::likes( $post_id ); ?></span> 
											<span class="post-views"><?php wpl_galaxy_wp_front::views( $post_id ); ?></span>
										</p>  
					
										<?php
											$tags_list = get_the_term_list( $post_id, 'wproto_catalog_tag', '', ', ', '' );
											if( $tags_list <> '' ):
										?>
										<p>
											<span><?php _e('Tags', 'wproto'); ?>:</span>
											<?php echo $tags_list; ?> 
										</p>
										<?php endif; ?>
							
										<?php
											$cats_list = get_the_term_list( $post_id, 'wproto_catalog_category', '', ', ', '' );
											if( $cats_list <> '' ):
										?>
										<p>
											<span><?php _e('Categories', 'wproto'); ?>:</span>
											<?php echo $cats_list; ?>
										</p>
										<?php endif; ?>
										
										<?php wpl_galaxy_wp_front::share_post_code(); ?>
									
									</footer>
								
								</div>
							
							</div>
						
						</div>
						
						<!--
					
							PRODUCT TABS
						
						-->
						
						<div class="clear"></div>
						
						<?php
							$overview_text = get_post_meta( $post_id, 'overview_text', true );
						?>
						
						<?php if( $overview_text <> '' || comments_open() ): ?>
						<section class="tabs">
							<div class="liquid-slider content-slider" id="product-tabs">
								<?php if( $overview_text <> '' ): ?>
								<div>
									<h2 class="title"><?php _e('Overview', 'wproto'); ?></h2>
									<?php echo apply_filters( 'the_content', $overview_text ); ?>
								</div>
								<?php endif; ?>
								
								<?php if( comments_open() ): ?>
								<div>
									<h2 class="title"><?php _e('Reviews', 'wproto'); ?> (<?php echo get_comments_number(); ?>)</h2>

									<?php if( !post_password_required() ): ?>
										<?php comments_template( '', true ); ?>
									<?php endif; ?>
									
								</div>
								<?php endif; ?>
								
							</div>
						</section>
						<?php endif; ?>

					</div>
					
					<!-- 
					
						RELATED POSTS BLOCK
						
					-->
					<?php wpl_galaxy_wp_front::related_posts( get_the_ID(), 8, 'wproto_catalog_category' ); ?>

					
					<?php endwhile; endif; ?>
				
				</article>
				
			</section>

			<?php get_sidebar(); ?>
			
		</div>
	</div> <!-- /content -->

<?php get_footer();