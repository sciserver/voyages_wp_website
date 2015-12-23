<?php
	global $wproto_section, $wpl_galaxy_wp;
	$section_data = isset( $wproto_section->data ) ? unserialize( $wproto_section->data ) : array();
	
	$_type = isset( $section_data['display_content_type'] ) ? $section_data['display_content_type'] : 'all';
	$_limit = isset( $section_data['limit'] ) ? absint( $section_data['limit'] ) : 4;
	$_category = isset( $section_data['posts_categories'] ) ? $section_data['posts_categories'] : 0;
	$_orderby = isset( $section_data['order'] ) ? $section_data['order'] : 'ID';
	$_sort = isset( $section_data['sort'] ) ? $section_data['sort'] : 'DESC';
	
	$result = $wpl_galaxy_wp->model->post->get( $_type, $_limit, $_category, $_orderby, $_sort, 'wproto_portfolio', 'wproto_portfolio_category' );
?>
<!--

	HEXAGON CAROUSEL
	
-->
<?php if( $result->have_posts() ): ?> 
<section id="section-id-<?php echo $wproto_section->ID; ?>" class="hex-portfolio">

	<div class="wrapper">
	
		<?php if( $wproto_section->title <> '' ): ?>
		<header class="hgroup">
			<h2><?php echo $wproto_section->title; ?></h2>
			
			<h5><?php if( $wproto_section->subtitle <> '' ): ?><?php echo $wproto_section->subtitle; ?><?php endif; ?>&nbsp;</h5>
			
		</header>
		<?php endif; ?>
		
		<div class="items">
		<?php $i=0; while( $result->have_posts() ): $result->the_post(); $i++; ?>
		
			<?php
				$launch_link = get_post_meta( get_the_ID(), 'link', true );
			?>
			<div class="item <?php if( $launch_link == '' ): ?>no-launch-link<?php endif; ?> <?php if( $i <= 4 ): ?>appear-animation<?php endif; ?>" <?php if( $i <= 4 ): ?>data-appear-animation="bounceIn"<?php endif; ?>>		
				<div class="hexagon">
					<div class="hexagon-in1">
						<?php
							$thumb_name = wpl_galaxy_wp_utils::is_retina() ? 'portfolio-square-big-2x' : 'portfolio-square-big';
							$img = wp_get_attachment_image_src( get_post_thumbnail_id(), $thumb_name );
						?>
 						<div class="hexagon-in2" style="background-image: url('<?php echo $img[0]; ?>'); <?php if( wpl_galaxy_wp_utils::is_retina() ): ?>background-size: 336px 336px;<?php endif; ?>"><div class="overflow"></div></div>
					</div>
				</div>
								
				<div class="links">	
					<a href="<?php the_permalink(); ?>"><?php _e('View details', 'wproto'); ?> <i class="menu-angle"></i></a>
					<?php 
						if( $launch_link <> '' ):
					?>
					<a target="_blank" href="<?php echo $launch_link; ?>"><?php _e('Launch project', 'wproto'); ?> <i class="menu-angle"></i></a>
					<?php endif; ?>
				</div>
								
				<div class="desc">
					<h4><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h4>
					<?php
						$cats_list = get_the_term_list( get_the_ID(), 'wproto_portfolio_category', '', ', ', '' );
						if( $cats_list <> '' ):
					?>
					<p><?php echo $cats_list; ?></p>
					<?php endif; ?>
				</div>
								
			</div>
		
		<?php endwhile; ?>
		</div>
	
	</div>

</section>
<?php wp_reset_query(); endif; 