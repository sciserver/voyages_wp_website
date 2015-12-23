<?php
	global $wp_query, $wpl_galaxy_wp, $wpl_galaxy_wp_ajax_pagination;
	$left_side_html = '';
	$right_side_html = '';
?>

<?php $i=0; while ( $wp_query->have_posts() ) : $wp_query->the_post(); ?>

	<?php
		$post_format = get_post_format();
		$post_format = $post_format === false ? 'standard' : $post_format;
		
		$post_type = get_post_type();
	?>

	<?php ob_start(); ?>
	
	<article <?php post_class(); ?> data-appear-animation="fadeIn">
		<div class="inside">
			<!--
			=======================================================================================================================
			POST HEADER
			=======================================================================================================================
			-->
			<header class="date">
				<div class="post-date">
					<div class="day <?php if( !isset( $wpl_galaxy_wp_ajax_pagination ) ): ?>appear-animation<?php endif; ?>" data-appear-animation="bounceIn"><?php the_time('d'); ?></div>
					<div class="month"><?php the_time('F'); ?></div>
					<div class="year"><?php the_time('Y'); ?></div>
				</div>
				<div class="pointer"><span <?php if( !isset( $wpl_galaxy_wp_ajax_pagination ) ): ?>class="appear-animation"<?php endif; ?> data-appear-animation="bounceIn"></span></div>
			</header>
			<div class="clear"></div>
			
			<h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
			<?php if( $post_type == 'wproto_catalog' ): ?>
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
			
			<?php if( $post_format == 'gallery' || in_array( $post_type, array( 'wproto_photoalbums', 'wproto_portfolio' ) ) ): ?>
			<!--
			=======================================================================================================================
			GALLERIES / PHOTOALBUMS
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
			<div class="post-images-carousel">
						
				<div class="images-carousel">
					<?php foreach( $gallery_ids as $id ): ?>
						<?php
							$image_thumb = wpl_galaxy_wp_utils::is_retina() ? 'post-thumb-full-2x' : 'post-thumb-full';
							$image = wp_get_attachment_image_src( $id, $image_thumb );
						?>
						<img src="<?php echo $image[0]; ?>" alt="" />
					<?php endforeach; ?>
				</div>
						
				<span class="post-slider-prev"><a href="javascript:;"></a></span>
				<span class="post-slider-next"><a href="javascript:;"></a></span>
						
				<div class="post-slider-pagination"></div>
							
				<div class="comments">
					<a href="<?php comments_link(); ?>">
						<i class="fa fa-comments-o"></i> <?php echo get_comments_number(); ?>
					</a>
				</div>
							
				<div class="clear"></div>
			</div>
									
			<?php elseif( has_post_thumbnail() ): ?>
				<div class="thumbnail">
					<?php wpl_galaxy_wp_front::thumbnail( get_the_ID(), 'post-thumb-full' ); ?>
					<a href="<?php the_permalink(); ?>" class="thumb-hover"><span class="details"><?php _e('Read in details', 'wproto'); ?> <i class="menu-angle"></i></span></a>
					<div class="clear"></div>
				</div>
			<?php endif; ?>
								
			<footer></footer>
						
			<div class="clear"></div>
			
			<?php elseif( $post_type == 'wproto_video' ): ?>
			<!--
			=======================================================================================================================
			VIDEOS
			=======================================================================================================================
			-->
			
			<!-- VIDEO -->
			<?php
				$video_content = get_post_meta( get_the_ID(), 'player_code', true );
				if( $video_content <> '' ):
			?>
				<div class="thumbnail">
					<iframe src="<?php echo $video_content; ?>" width="100%" height="380"></iframe>
				</div>
			<?php endif; ?>
			
			<?php else: ?>
			<!--
			=======================================================================================================================
			COMMON POSTS
			=======================================================================================================================
			-->
				<?php if( has_post_thumbnail() ): ?>
				<div class="thumbnail">
					<?php wpl_galaxy_wp_front::thumbnail( get_the_ID(), 'post-thumb-full' ); ?>
					<a href="<?php the_permalink(); ?>" class="thumb-hover"><span class="details"><?php _e('Read in details', 'wproto'); ?> <i class="menu-angle"></i></span></a>
					<div class="clear"></div>
				</div>
				<?php endif; ?>
				
				<div class="text">
					<?php the_excerpt(); ?>			
				</div>
								
				<footer>
					<div class="tags">
						<a href="<?php comments_link(); ?>"><i class="fa fa-comments-o"></i> <?php echo get_comments_number(); ?></a>
							
						<strong><?php _e('By', 'wproto'); ?></strong> <?php the_author_posts_link(); ?> 
						
						<?php
							$cats_list = wpl_galaxy_wp_front::get_categories();
							if( $cats_list <> '' ):
						?>
						<strong><?php _e('In', 'wproto'); ?></strong> <?php echo $cats_list; ?>
						<?php
							endif; 
						?>
					</div>
							
					<a href="<?php the_permalink(); ?>" class="continue-reading"><?php _e('Keep reading', 'wproto'); ?> <i class="arrow-keep-reading"></i></a>
							
				</footer>
			
			<?php endif; ?>
			
		</div>
	</article>
	
	<?php
		if( $i == 0 ) {
			$left_side_html .= ob_get_clean();
		} else {
			$right_side_html .= ob_get_clean();
		}
	?>

<?php $i++; if( $i == 2 ) $i = 0; endwhile; ?>

<!--

	TIMELINE LAYOUT
	
-->
<?php if( !isset( $wpl_galaxy_wp_ajax_pagination ) ): ?>
<div class="posts grid" id="ajax-pagination-response-container">
<?php endif; ?>

	<!-- left side -->
	<div class="unit half left">
		<?php echo $left_side_html; ?>
	</div>
	
	<!-- right side -->
	<div class="unit half right">
		<?php echo $right_side_html; ?>
	</div>

<?php if( !isset( $wpl_galaxy_wp_ajax_pagination ) ): ?>
</div>
<?php endif;