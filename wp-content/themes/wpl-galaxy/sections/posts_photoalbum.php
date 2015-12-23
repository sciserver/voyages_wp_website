<?php
	global $wproto_section, $wpl_galaxy_wp;
	$section_data = isset( $wproto_section->data ) ? unserialize( $wproto_section->data ) : array();
	
	$_type = isset( $section_data['display_content_type'] ) ? $section_data['display_content_type'] : 'all';
	$_category = isset( $section_data['posts_categories'] ) ? $section_data['posts_categories'] : 0;
	$_orderby = isset( $section_data['order'] ) ? $section_data['order'] : 'ID';
	$_sort = isset( $section_data['sort'] ) ? $section_data['sort'] : 'DESC';
	
	$result = $wpl_galaxy_wp->model->post->get( $_type, 15, $_category, $_orderby, $_sort, 'wproto_photoalbums', 'wproto_photoalbums_category', false, false, false );
?>
<!--
					
	Photoalbums carousel
						
-->
<?php if( $result->have_posts() ): ?> 

<section id="section-id-<?php echo $wproto_section->ID; ?>" class="blog-posts" data-appear-animation="fadeIn">

	<?php if( $wproto_section->title <> '' ): ?>
	<header class="wrapper hgroup">
		<h2><?php echo $wproto_section->title; ?></h2>
		
		<h5><?php if( $wproto_section->subtitle <> '' ): ?><?php echo $wproto_section->subtitle; ?><?php endif; ?>&nbsp;</h5>
		
	</header>
	<?php endif; ?>
	
	<div class="blog-posts-home jThumbnailScroller">
		<div class="swiper-container">
 			<div class="swiper-wrapper">
 			<?php while( $result->have_posts() ): $result->the_post(); ?>
 			<div class="swiper-slide">
    	<a class="item" href="<?php the_permalink(); ?>">
    		<?php if( has_post_thumbnail() ): ?>
    		<span class="thumbnail">
					<?php
						$thumb_name = wpl_galaxy_wp_utils::is_retina() ? 'new-scroll-thumb-2x' : 'new-scroll-thumb';
						$img = wp_get_attachment_image_src( get_post_thumbnail_id(), $thumb_name );
					?>
					<img src="<?php echo $img[0]; ?>" width="280" alt="" />
					<span class="thumb-hover"><span class="details"> <?php _e('Read in details','wproto'); ?> <i class="menu-angle"></i></span></span>
				</span>
				<?php endif; ?>
				<span class="title">
					<?php the_title(); ?>
				</span>
				<span class="date">
					<strong><?php the_time( $wpl_galaxy_wp->settings['date_format'] ); ?></strong> <i class="fa fa-comments-o"></i> <span class="comments-count"><?php echo get_comments_number(); ?></span>
				</span>
				<span class="description">
					<?php echo wpl_galaxy_wp_utils::custom_excerpt( get_the_excerpt(), 105 );  ?>
				</span>
				<span class="continue-reading"><?php _e('Keep reading','wproto'); ?> <i class="arrow-keep-reading"></i></span>
			</a>
			</div>
 			<?php endwhile; ?>
 			</div>
		</div>
		<a href="javascript:;" class="jTscrollerPrevButton"></a>
		<a href="javascript:;" class="jTscrollerNextButton"></a>
	</div>
	<div class="clear"></div>
</section>

<?php wp_reset_query(); endif; 