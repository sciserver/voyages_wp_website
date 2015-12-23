<?php
	global $wproto_section, $wpl_galaxy_wp, $woocommerce;
	$section_data = isset( $wproto_section->data ) ? unserialize( $wproto_section->data ) : array();
	$section_style = isset( $section_data['section_style'] ) ? $section_data['section_style'] : 'style_2';
?>

<?php
	/*********************************************************************************************************************
		NEW ARRIVALS AND BEST SELLERS
	*********************************************************************************************************************/
	if( $section_style == 'style_2' || $section_style == 'style_3' ):
?>

	<?php
		if( $section_style == 'style_2' ) {
			$result = $wpl_galaxy_wp->model->post->get( 'all', 8, 0, 'date', 'DESC', 'product' );
		}
		if( $section_style == 'style_3' ) {
    	$query_args = array(
    		'posts_per_page' => 8,
    		'post_status' => 'publish',
    		'post_type' => 'product',
    		'meta_key' => 'total_sales',
    		'orderby' => 'meta_value_num',
    		'no_found_rows' => 1,
    	);

    	$query_args['meta_query'] = $woocommerce->query->get_meta_query();
			
			// hide free products
			$query_args['meta_query'][] = array(
   			'key' => '_price',
		    'value' => 0,
		    'compare' => '>',
		    'type' => 'DECIMAL',
			);

			$result = new WP_Query( $query_args );
		}
	?>

<!--

	PRODUCTS
	
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
		
			<?php $i_p = 0; while( $result->have_posts() ): $result->the_post(); $i_p++; ?>
			<div class="item box">
								
				<div class="inside">
				
					<?php
						$post_id = get_the_ID();
						$woo_product = new WC_Product_Factory();
						$product = $woo_product->get_product( $post_id );
						$average = $product->get_average_rating();
						$thumb_name = wpl_galaxy_wp_utils::is_retina() ? 'shop-related-2x' : 'shop-related';
						$img = wp_get_attachment_image_src( get_post_thumbnail_id(), $thumb_name );
					?>
				
					<?php if( has_post_thumbnail() ): ?>
					<a class="thumbnail" href="<?php the_permalink(); ?>">
						<img src="<?php echo $img[0]; ?>" width="180" height="182" alt="" />
						<?php if( $section_style == 'style_3' ): ?>
						<span class="number appear-animation" data-appear-animation-delay="0.<?php echo $i_p; ?>5" data-appear-animation="bounceIn"><?php echo $i_p; ?></span>
						<?php endif; ?>
					</a>
					<?php endif; ?>

					<div class="additional-info">
							
						<?php
							$attached_images = $product->get_gallery_attachment_ids();
							
							$product_images_count = count( $attached_images );
						?>
						
						<?php if( $product_images_count > 0 ): ?>
						<div class="product-scroller">
							
							<div class="scroller">
								<?php $i_num = 0; foreach( $attached_images as $k=>$id ): $i_num++; if( $i_num > 3 ) break; ?>
								
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
						
						<div class="rating">
							<?php echo wpl_galaxy_wp_front::get_rating_html( $average ); ?> 
							<span>(<?php echo get_comments_number(); ?> <?php _e('reviews', 'wproto'); ?>)</span>
						</div>
					</div>

					<a class="title" href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
							
					<p class="desc"><?php echo wpl_galaxy_wp_utils::custom_excerpt( get_the_excerpt(), 65 );  ?></p>
					
					<div class="price">
					<?php echo $product->get_price_html(); ?>
					</div>
										
					<a href="<?php the_permalink(); ?>" class="button"><?php _e('Buy', 'buy'); ?></a>
					<a href="<?php the_permalink(); ?>" class="button mobile"><?php _e('Buy', 'buy'); ?></a>
										
					<div class="clear"></div>
									
				</div>
								
			</div>
			<?php endwhile; ?>
			
		</div> <!-- /items -->
		
	</div>
</section>
<?php wp_reset_query(); endif; ?>

<?php endif; ?>

<?php
	/*********************************************************************************************************************
		 Display "Best ratings", "Reviews on our blog" and "Best sellers"
	*********************************************************************************************************************/
	if( $section_style == 'style_1' ):
?>
<!--
					
	BEST ITEMS
						
-->
<section class="best-items" data-appear-animation="fadeIn">
	<div class="wrapper grid">
	
		<!-- 
			BEST RATINGS
		-->
		<div class="unit best-ratings one-third">
			<?php
				$query_args = array('posts_per_page' => 9, 'no_found_rows' => 1, 'post_status' => 'publish', 'post_type' => 'product' );
				$query_args['meta_query'] = $woocommerce->query->get_meta_query();
				$result = new WP_Query( $query_args );
			?>
					
				<h3><?php _e('Best ratings', 'wproto'); ?></h3>
					
				<div class="items">
				<?php if( $result->have_posts() ): ?> 
				
					<?php																				
						$_bs_num = 0; $_i_all = 0;
						while( $result->have_posts() ): $result->the_post();
							$_bs_num++; $_i_all++;
					?>
					
					<?php if( $_bs_num == 1 ): ?><div class="item"><ul><?php endif; ?>
					
					<li>

						<?php
							$product_id = get_the_ID();
							$woo_product = new WC_Product_Factory();
							$product = $woo_product->get_product( $product_id );
							$average = $product->get_average_rating();
							$thumb_size = wpl_galaxy_wp_utils::is_retina() ? 'photo-small-2x' : 'photo-small';
						?>

						<div class="thumbnail">
							<a href="<?php the_permalink(); ?>"><?php echo ( has_post_thumbnail() ? get_the_post_thumbnail( $product_id, $thumb_size ) : woocommerce_placeholder_img( $thumb_size ) ) ?></a>
						</div>
									
						<div class="text">
									
							<a href="<?php the_permalink(); ?>" class="title"><?php the_title(); ?></a>
									
							<div class="rating">
								<?php echo wpl_galaxy_wp_front::get_rating_html( $average ); ?> 
								<span>(<?php echo get_comments_number(); ?> <?php _e('reviews', 'wproto'); ?>)</span>
							</div>
										
							<div class="price"><?php echo $product->get_price_html(); ?></div>
									
						</div>
								
					</li>
					
					<?php if( $_bs_num == 3 || ( ( 1 + $_i_all) > $result->post_count ) ): ?></ul></div><?php endif; ?>
					
					<?php if( $_bs_num == 3 ) $_bs_num = 0; endwhile; ?>
				
				<?php endif; ?>
				</div>
			
		</div>
		<!--
			LATEST REVIEWS
		-->
		<div class="unit reviews one-third">
			<?php
				$result = get_comments( array( 'number' => 9, 'status' => 'approve', 'post_status' => 'publish', 'post_type' => 'product' ) );
			?>		
			<h3><?php _e('Reviews on our blog', 'wproto'); ?></h3>
			<div class="items">
			<?php if( $result ): ?>
			
				<?php $_bs_num = 0; $_i_all = 0; foreach ( (array)$result as $comment): $_bs_num++; $_i_all++; ?>
				
					<?php if( $_bs_num == 1 ): ?><div class="item"><ul><?php endif; ?>
					
					<?php
						$_product = get_product( $comment->comment_post_ID );
						$rating = intval( get_comment_meta( $comment->comment_ID, 'rating', true ) );
						$rating_html = $_product->get_rating_html( $rating );
					?>
					
					<li>
					
						<div class="thumbnail">
							<a href="<?php echo esc_url( get_comment_link( $comment->comment_ID ) ); ?>"><?php echo $_product->get_image(); ?></a>
						</div>
									
						<div class="text">
									
							<a href="<?php echo esc_url( get_comment_link( $comment->comment_ID ) ); ?>" class="title"><?php echo $_product->get_title(); ?></a>
									
							<p><?php echo wpl_galaxy_wp_utils::custom_excerpt( $_product->post->post_excerpt, 87 );  ?></p>
									
						</div>
								
					</li>
					
					<?php if( $_bs_num == 3|| ( ( 1 + $_i_all) > count( $result ) ) ): ?></ul></div><?php endif; ?>
				
				<?php if( $_bs_num == 3 ) $_bs_num = 0; endforeach; ?>
			
			<?php endif; ?>
			</div>
		</div>
		<!--
			BEST SELLERS
		-->
		<div class="unit home-best-sellers one-third">
			<?php
    		$query_args = array(
    			'posts_per_page' => 9,
    			'post_status' => 'publish',
    			'post_type' => 'product',
    			'meta_key' => 'total_sales',
    			'orderby' => 'meta_value_num',
    			'no_found_rows' => 1,
    		);

    		$query_args['meta_query'] = $woocommerce->query->get_meta_query();
			
				// hide free products
				$query_args['meta_query'][] = array(
   				'key' => '_price',
		    	'value' => 0,
		    	'compare' => '>',
		    	'type' => 'DECIMAL',
				);

				$result = new WP_Query( $query_args );
			?>
			
			<h3><?php _e('Best Sellers', 'wproto'); ?></h3>
			<div class="items">
			<?php if( $result->have_posts() ): ?> 
				<?php $_bs_num = 0; $_bs_num_all = 0; while( $result->have_posts() ): $result->the_post(); $_bs_num++; $_bs_num_all++; ?>
				
					<?php if( $_bs_num == 1 ): ?><div class="item"><ul><?php endif; ?>
					
					<li>
					
						<?php
							$product_id = get_the_ID();
							$woo_product = new WC_Product_Factory();
							$product = $woo_product->get_product( $product_id );
							$average = $product->get_average_rating();
							$thumb_size = wpl_galaxy_wp_utils::is_retina() ? 'photo-small-2x' : 'photo-small';
						?>
					
						<div class="thumbnail">
							<a href="<?php the_permalink(); ?>"><?php echo ( has_post_thumbnail() ? get_the_post_thumbnail( $product_id, $thumb_size ) : woocommerce_placeholder_img( $thumb_size ) ) ?></a>
							<span class="number appear-animation" data-appear-animation-delay="0.15" data-appear-animation="bounceIn"><?php echo $_bs_num_all; ?></span>
						</div>
									
						<div class="text">
									
							<a href="<?php the_permalink(); ?>" class="title"><?php the_title(); ?></a>
									
							<div class="rating">
								<?php echo wpl_galaxy_wp_front::get_rating_html( $average ); ?> 
								<span>(<?php echo get_comments_number(); ?> <?php _e('reviews', 'wproto'); ?>)</span>
							</div>
										
							<div class="price"><?php echo $product->get_price_html(); ?></div>
									
						</div>
								
					</li>
					
					<?php if( $_bs_num == 3 || ( ( 1 + $_bs_num_all) > $result->post_count ) ): ?></ul></div><?php endif; ?>
				
				<?php if( $_bs_num == 3 ) $_bs_num = 0; endwhile; ?>
			<?php endif; ?>
			</div>
		</div>
	
	</div>
</section>
<?php endif; wp_reset_query();