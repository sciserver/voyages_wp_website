<?php
	global $wproto_section, $wpl_galaxy_wp;
	$section_data = isset( $wproto_section->data ) ? unserialize( $wproto_section->data ) : array();
	
	$_type = isset( $section_data['display_content_type'] ) ? $section_data['display_content_type'] : 'all';
	$_limit = isset( $section_data['limit'] ) ? absint( $section_data['limit'] ) : 4;
	$_category = isset( $section_data['posts_categories'] ) ? $section_data['posts_categories'] : 0;
	$_orderby = isset( $section_data['order'] ) ? $section_data['order'] : 'ID';
	$_sort = isset( $section_data['sort'] ) ? $section_data['sort'] : 'DESC';
	
	$result = $wpl_galaxy_wp->model->post->get( $_type, $_limit, $_category, $_orderby, $_sort, 'wproto_benefits', 'wproto_benefits_category' );
?>
<!--

	BENEFITS SECTION
						
-->

<?php if( $result->have_posts() ): ?> 
<section id="section-id-<?php echo $wproto_section->ID; ?>" class="benefits wrapper">

	<div class="grid">
	
		<?php if( $wproto_section->title <> '' ): ?>
		<header class="unit hgroup whole">
			<h2><?php echo $wproto_section->title; ?></h2>
			
			<h5><?php if( $wproto_section->subtitle <> '' ): ?><?php echo $wproto_section->subtitle; ?><?php endif; ?>&nbsp;</h5>
			
		</header>
		<?php endif; ?>
		
		<?php if( $wproto_section->before_text <> '' ): ?>
		<div class="unit whole">
			<?php echo apply_filters( 'the_content', $wproto_section->before_text ); ?>
		</div>
		<?php endif; ?>
	
		<?php while( $result->have_posts() ): $result->the_post(); ?>
		<div class="unit one-quarter">
					
			<?php
				$id = get_the_ID();
				
				$link = get_post_meta( $id, 'wproto_benefit_link', true );
				
				$icon_style = get_post_meta( $id, 'wproto_benefit_style', true );
				$icon_style = $icon_style == '' ? 'image' : $icon_style;
				$thumb_name = wpl_galaxy_wp_utils::is_retina() ? 'benefits-icon-2x' : 'benefits-icon';
				$img = wp_get_attachment_image_src( get_post_thumbnail_id(), $thumb_name );
				$icon_name = get_post_meta( $id, 'wproto_benefit_icon_name', true );
				$animation = get_post_meta( $id, 'wproto_benefit_animation', true );
				$animation = $animation == '' ? 'bounceIn' : $animation;
				
				$animation_delay = get_post_meta( $id, 'wproto_benefit_animation_delay', true );
			?>

			<div data-appear-animation-delay="<?php echo $animation_delay; ?>" data-appear-animation="<?php echo $animation; ?>" class="appear-animation icon-container">
				<a href="<?php echo $link == '' ? 'javascript:;' : $link; ?>" class="icon">
					<?php if( $icon_style == 'icon' ): ?>
						<i class="<?php echo $icon_name; ?>"></i>
					<?php else: ?>
						<img width="97" height="97" src="<?php echo $img[0]; ?>" alt="" />
					<?php endif; ?>
				</a>
			</div>

			<h4><?php the_title(); ?></h4>
			<?php the_content(); ?>		
					
		</div>
		<?php endwhile; ?>
		
		<?php if( $wproto_section->after_text <> '' ): ?>
		<div class="unit whole">
			<?php echo apply_filters( 'the_content', $wproto_section->after_text ); ?>
		</div>
		<?php endif; ?>
		
	</div>

</section>
<?php wp_reset_query(); endif; 