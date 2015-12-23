<?php
	global $wp_query, $wpl_galaxy_wp, $wpl_galaxy_wp_ajax_pagination;
?>
<!--

	HEXAGON LAYOUT
	
-->

<?php if( !isset( $wpl_galaxy_wp_ajax_pagination ) ): ?>
<div class="portfolio-items" id="ajax-pagination-response-container">
<?php endif; ?>

	<?php $i = 0.1; while ( $wp_query->have_posts() ) : $wp_query->the_post(); ?>
	
	<?php
		$post_type = get_post_type();
		
		switch( $post_type ) {
			default:
			case 'post':
				$view_link_text = __('View post', 'wproto');
				$launch_link_text = '';
			break;
			case 'wproto_portfolio':
				$view_link_text = __('View details', 'wproto');
				$launch_link_text = __('Launch project', 'wproto');
				
				$launch_link = get_post_meta( get_the_ID(), 'link', true );
				
			break;
			case 'wproto_video':
				$view_link_text = __('View post', 'wproto');
				$launch_link_text = '';
			break;
			case 'wproto_photoalbums':
				$view_link_text = __('View album', 'wproto');
				$launch_link_text = '';
			break;
			case 'wproto_catalog':
				$view_link_text = __('View product', 'wproto');
				$launch_link_text = '';
			break;
		}
		
		$img_thumb = '';
		
		if( $post_type == 'wproto_video' ) {
			
			$img_thumb = get_post_meta( get_the_ID(), 'thumbnail_big', true );
			
		} elseif( has_post_thumbnail() ) {
			$image_thumb = wpl_galaxy_wp_utils::is_retina() ? 'portfolio-hexagon-thumb-2x' : 'portfolio-hexagon-thumb';
			$image_arr = wp_get_attachment_image_src( get_post_thumbnail_id( get_the_ID() ), $image_thumb );
			$img_thumb = $image_arr[0];
		}
		

	?>
	
	<?php if( $img_thumb <> '' ): ?>
	<div class="item visible" <?php if( !isset( $wpl_galaxy_wp_ajax_pagination ) ): ?>data-appear-animation-delay="<?php echo $i; ?>" data-appear-animation="bounceIn"<?php endif; ?>>		
		<div class="hexagon">
			<div class="hexagon-in1">
 				<div class="hexagon-in2" style="<?php if( wpl_galaxy_wp_utils::is_retina() ): ?>background-size: 50% 50%;<?php endif; ?>background-image: url('<?php echo $img_thumb; ?>');"><div class="overflow"></div></div>
			</div>
		</div>
								
		<div class="links <?php echo $post_type != 'wproto_portfolio' ? 'without-launch' : ''; ?>">	
			<a href="<?php echo the_permalink(); ?>"><?php echo $view_link_text; ?> <i class="menu-angle"></i></a>
			<?php if( $post_type == 'wproto_portfolio' ): ?>
			<a target="_blank" href="<?php echo $launch_link; ?>"><?php echo $launch_link_text; ?> <i class="menu-angle"></i></a>
			<?php endif; ?>
		</div>
		<?php endif; ?>
								
	</div>
	
	<?php $i = $i + 0.1; if( $i > 0.8 ) $i = 0.1; endwhile; ?>

<?php if( !isset( $wpl_galaxy_wp_ajax_pagination ) ): ?>
</div>
<?php endif;