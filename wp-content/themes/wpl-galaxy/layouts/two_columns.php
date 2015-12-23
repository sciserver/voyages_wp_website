<?php
	global $wp_query, $wpl_galaxy_wp, $wpl_galaxy_wp_ajax_pagination;
?>
<!--

	FOUR COLUMNS LAYOUT
	
-->
<?php if( !is_search() && !isset( $wpl_galaxy_wp_ajax_pagination ) ): ?>
<div class="posts grid" id="ajax-pagination-response-container">
<?php endif; ?>

	<?php while ( $wp_query->have_posts() ) : $wp_query->the_post(); ?>
	
	<?php
		$post_format = get_post_format();
		$post_format = $post_format === false ? 'standard' : $post_format;
		
		$post_type = get_post_type();
	?>
	
	<article data-appear-animation="fadeIn" class="unit half <?php echo implode(' ', get_post_class()); ?>">
	
		<?php if( $post_format == 'gallery' || in_array( $post_type, array( 'wproto_photoalbums', 'wproto_portfolio' ) ) ): ?>
		<!--
			
		=======================================================================================================================
		GALLERY / PORTFOLIO / PHOTOALBUMS THUMBNAILS
		=======================================================================================================================
			
		-->
		
			<?php
			
			$gallery_ids = get_post_meta( get_the_ID(), 'wproto_attached_images', true );
			
			if( $gallery_ids == '' && get_post_gallery() ) {
				$gallery = get_post_gallery( get_the_ID(), false );
				$gallery_ids = isset( $gallery['ids'] ) ? $gallery['ids'] : '';
			}
			
			if( is_string( $gallery_ids ) && $gallery_ids <> '' ) {
				$gallery_ids = explode( ',', $gallery_ids );
			}
			
			if( is_array( $gallery_ids ) && count( $gallery_ids ) > 0 ):
			?>
			<div class="item-slider">
				<div class="post-slider">	
					<div class="post-slider-carousel">
						<?php foreach( $gallery_ids as $id ): ?>
							<?php
								$image_thumb = wpl_galaxy_wp_utils::is_retina() ? 'post-thumb-big-2x' : 'post-thumb-big';
								$image = wp_get_attachment_image_src( $id, $image_thumb );
							?>
							<img src="<?php echo $image[0]; ?>" alt="" />
						<?php endforeach; ?>
					</div>
					<span class="post-slider-prev"><a href="javascript:;"></a></span>
					<span class="post-slider-next"><a href="javascript:;"></a></span>
					<div class="clear"></div>
				</div>
			</div>
			<?php elseif( has_post_thumbnail() ): ?>
				<div class="thumbnail">
					<?php wpl_galaxy_wp_front::thumbnail( get_the_ID(), 'post-thumb-big' ); ?>
					<a href="<?php the_permalink(); ?>" class="thumb-hover"><span class="details"><?php _e('Read in details', 'wproto'); ?> <i class="menu-angle"></i></span></a>
					<div class="clear"></div>
				</div>
			<?php endif; ?>
		
		<?php elseif( $post_type == 'wproto_video' ): ?>
		<!--
			
		=======================================================================================================================
		VIDEO THUMBNAILS
		=======================================================================================================================
			
		-->
		
			<!-- VIDEO -->
			<?php
				$video_content = get_post_meta( get_the_ID(), 'player_code', true );
				if( $video_content <> '' ):
			?>
				<div class="thumbnail">
					<iframe src="<?php echo $video_content; ?>" width="100%" height="480"></iframe>
				</div>
			<?php endif; ?>
		
		<?php else: ?>
		<!--
			
		=======================================================================================================================
		COMMON POST THUMBNAILS
		=======================================================================================================================
			
		-->
		<?php if( has_post_thumbnail() ): ?>
		<div class="thumbnail">
			<?php wpl_galaxy_wp_front::thumbnail( get_the_ID(), 'post-thumb-big' ); ?>
			<a href="<?php the_permalink(); ?>" class="thumb-hover">
				<span class="details"><?php _e('Read more', 'wproto'); ?> <i class="menu-angle"></i></span>
			</a>
			<div class="clear"></div>
		</div>
		<?php endif; ?>
		
		<?php endif; ?>
		
		<!--
			
		=======================================================================================================================
		POST HEADER AND EXCERPT
		=======================================================================================================================
			
		-->
		
		<div class="text">
							
			<h4><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h4>
			
			<?php if( $post_type != 'wproto_catalog' ): ?>
			<div class="date"><?php the_time( $wpl_galaxy_wp->settings['date_format'] ); ?></div>
			<?php else: ?>
			<div class="price">
			<?php
				$old_price = get_post_meta( get_the_ID(), 'old_price', true );
				$old_price = $old_price <> '' ? wpl_galaxy_wp_front::get_price( $old_price ) : '';
											
				$price = get_post_meta( get_the_ID(), 'price', true );
				$price = $price <> '' ? wpl_galaxy_wp_front::get_price( $price ) : '';
			?>
					
			<?php if( $old_price <> '' ): ?>
			<del class="old-price"><?php echo $old_price; ?></del>
			<?php endif; ?>
			<?php echo $price; ?>
			</div>
			<?php endif; ?>
			
			<?php if( $post_type == 'wproto_catalog' && ( absint( get_post_meta( get_the_ID(), 'wproto_likes', true ) ) >= $wpl_galaxy_wp->get_option('five_star_likes_count') ) ): ?>
				
			<?php
				echo wpl_galaxy_wp_front::get_rating_html( 5 );
			?>
				
			<?php endif; ?>
								
			<p><?php echo wpl_galaxy_wp_utils::custom_excerpt( get_the_excerpt(), 120 ); ?></p>
					
			<?php
				$cats_list = wpl_galaxy_wp_front::get_categories();
				if( $cats_list <> '' ):
			?>		
			<div class="categories">
				<strong><?php _e('In', 'wproto'); ?></strong> <?php echo $cats_list; ?>
			</div>
			<?php
				endif; 
			?>
								
			<a href="<?php the_permalink(); ?>" class="continue-reading"><?php _e('Read more', 'wproto'); ?> <i class="arrow-keep-reading"></i></a>
							
		</div>
		
	</article>
	
	<?php endwhile; ?>

<?php if( !is_search() && !isset( $wpl_galaxy_wp_ajax_pagination ) ): ?>
</div>
<?php endif;