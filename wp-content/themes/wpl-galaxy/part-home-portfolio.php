<?php 
	global $wpl_galaxy_wp_home_portfolio_count, $wpl_galaxy_wp_home_portfolio_pagination, $wpl_galaxy_wp_home_portfolio_items;
?>
<?php if( !isset( $wpl_galaxy_wp_home_portfolio_pagination ) ): ?>
<div class="home-portfolio portfolio-items">
<?php endif; ?>

<?php $j=0; while( $wpl_galaxy_wp_home_portfolio_items->have_posts() ): $wpl_galaxy_wp_home_portfolio_items->the_post(); $j++; ?>
	<div class="item <?php if( $j == 1 || $j == 6 ): ?>w2<?php endif; ?>">
				
	<?php
					
		if( $j == 1 || $j == 6 ) {
			$thumb = wpl_galaxy_wp_utils::is_retina() ? 'portfolio-square-big-2x' : 'portfolio-square-big';
			$size = 336;
		} else {
			$thumb = wpl_galaxy_wp_utils::is_retina() ? 'portfolio-square-medium-2x' : 'portfolio-square-medium';
			$size = 165;
		}
						
		$thumb_id = get_post_thumbnail_id();
						
		$img = wp_get_attachment_image_src( $thumb_id, $thumb );
		$full_img = wp_get_attachment_image_src( $thumb_id, 'full' );
					
	?>
				
		<a href="javascript:;"><img src="<?php echo $img[0]; ?>" width="<?php echo $size; ?>" height="<?php echo $size; ?>" alt="" /></a>
		<div class="overlay">
			<a href="<?php echo $full_img[0]; ?>" class="icon-zoom"></a>
			<a href="<?php the_permalink(); ?>" class="icon-document"></a>
		</div>
	</div>
	<?php if( $j == 9 ) $j = 0; endwhile; ?>
	
<?php if( !isset( $wpl_galaxy_wp_home_portfolio_pagination ) ): ?>
</div>
<?php endif; ?>

<?php if( isset( $wpl_galaxy_wp_home_portfolio_count ) && $wpl_galaxy_wp_home_portfolio_count->publish > 9 ): ?>
<div class="section-portfolio-filter-load loadmore">
	<a data-taxonomy-term="<?php echo isset( $wpl_galaxy_wp_home_portfolio_items->tax_query->queries[0]['terms'] ) ? implode(',', $wpl_galaxy_wp_home_portfolio_items->tax_query->queries[0]['terms']) : ''; ?>" data-current-page="<?php echo isset( $wpl_galaxy_wp_home_portfolio_items->query_vars['paged'] ) ? $wpl_galaxy_wp_home_portfolio_items->query_vars['paged'] : 1; ?>" data-max-pages="<?php echo isset( $wpl_galaxy_wp_home_portfolio_items->max_num_pages ) ? $wpl_galaxy_wp_home_portfolio_items->max_num_pages : 1; ?>" href="javascript:;" class="button iconic"><i class="fa fa-spinner"></i> <?php _e('Load more works', 'wproto'); ?></a>
</div>
<?php endif; ?>