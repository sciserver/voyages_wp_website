<?php
	global $wproto_section, $wpl_galaxy_wp;
	$section_data = isset( $wproto_section->data ) ? unserialize( $wproto_section->data ) : array();
	
	$_type = isset( $section_data['display_content_type'] ) ? $section_data['display_content_type'] : 'all';
	$_limit = isset( $section_data['limit'] ) ? absint( $section_data['limit'] ) : 4;
	$_category = isset( $section_data['posts_categories'] ) ? $section_data['posts_categories'] : 0;
	$_orderby = isset( $section_data['order'] ) ? $section_data['order'] : 'ID';
	$_sort = isset( $section_data['sort'] ) ? $section_data['sort'] : 'DESC';
	
	$result = $wpl_galaxy_wp->model->post->get( $_type, $_limit, $_category, $_orderby, $_sort, 'wproto_testimonials', 'wproto_testimonials_category' );
?>
<!--
						
	TESTIMONIALS
						
-->
<?php if( $result->have_posts() ): ?> 
<section id="section-id-<?php echo $wproto_section->ID; ?>" class="testimonials">

	<div class="wrapper">

		<?php if( $wproto_section->title <> '' ): ?>
		<header class="hgroup">
			<h2><?php echo $wproto_section->title; ?></h2>
			<?php if( $wproto_section->subtitle <> '' ): ?>
			<h5><?php echo $wproto_section->subtitle; ?></h5>
			<?php endif; ?>
		</header>
		<?php endif; ?>
				
		<div class="items" id="testimonials-carousel">
				
			<?php while( $result->have_posts() ): $result->the_post(); ?>
			<div class="item">
				<blockquote><?php the_content(); ?></blockquote>
						
				<div class="author <?php if( !has_post_thumbnail() ): ?>no-thumb<?php endif; ?>" data-appear-animation-delay="0.2" data-appear-animation="bounceIn">
					
					<?php
						$id = get_the_ID();
						$position = get_post_meta( $id, 'position', true );
						$thumb_name = wpl_galaxy_wp_utils::is_retina() ? 'photo-small-2x' : 'photo-small';
						$img = wp_get_attachment_image_src( get_post_thumbnail_id(), $thumb_name );
					?>
					
					<?php if( has_post_thumbnail() ): ?>
					<div class="thumbnail">
						<img src="<?php echo $img[0]; ?>" width="70" alt="" />
					</div>
					<?php endif; ?>
								
					<cite>
						<span class="who"><?php the_title(); ?></span>
						<?php echo $position; ?>
					</cite>
						
				</div>
						
			</div>
			<?php endwhile; ?>
				
		</div>
				
	</div>

</section>
<?php wp_reset_query(); endif; 