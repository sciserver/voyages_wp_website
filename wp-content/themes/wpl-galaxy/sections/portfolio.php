<?php
	global $wproto_section, $wpl_galaxy_wp, $wpl_galaxy_wp_home_portfolio_count, $wpl_galaxy_wp_home_portfolio_items;
	$section_data = isset( $wproto_section->data ) ? unserialize( $wproto_section->data ) : array();
	
	$wpl_galaxy_wp_home_portfolio_items = $wpl_galaxy_wp->model->post->get( 'all', 9, '', 'date', 'DESC', 'wproto_portfolio', 'wproto_portfolio_category' );
?>
<!--

	PORTFOLIO SECTION
						
-->
<?php if( $wpl_galaxy_wp_home_portfolio_items->have_posts() ): ?> 
<section id="section-id-<?php echo $wproto_section->ID; ?>" class="portfolio wrapper">

	<div class="grid">
	
		<?php if( $wproto_section->title <> '' ): ?>
		<header class="unit hgroup whole">
			<h2><?php echo $wproto_section->title; ?></h2>
			<?php if( $wproto_section->subtitle <> '' ): ?>
			<h5><?php echo $wproto_section->subtitle; ?></h5>
			<?php endif; ?>
		</header>
		<?php endif; ?>
		
		<?php if( $wproto_section->before_text <> '' ): ?>
		<div class="unit whole">
			<?php echo apply_filters( 'the_content', $wproto_section->before_text ); ?>
		</div>
		<?php endif; ?>
		
		<div class="unit one-quarter">
				
			<ul class="portfolio-categories">
				<?php
					$wpl_galaxy_wp_home_portfolio_count = wp_count_posts('wproto_portfolio');
					$portfolio_categories = get_terms( 'wproto_portfolio_category', array(
 						'orderby'    	=> 'count',
 						'order'				=> 'DESC',
 						'hide_empty' 	=> 1
 					) );
				?>
				
				<li class="current"><a data-filter="0" href="javascript:;"><?php _e('All works', 'wproto'); ?> <span data-appear-animation-delay="0.15" data-appear-animation="bounceIn"><?php echo $wpl_galaxy_wp_home_portfolio_count->publish; ?></span></a></li>
				
				<?php if( count( $portfolio_categories ) > 0 ): ?>
					
					<?php foreach( $portfolio_categories as $cat ): ?>
					<li><a data-filter="<?php echo $cat->term_id;?>" href="javascript:;"><?php echo $cat->name; ?> <span data-appear-animation-delay="0.25" data-appear-animation="bounceIn"><?php echo $cat->count; ?></span></a></li>
					<?php endforeach; ?>
					
				<?php endif; ?>
			</ul>
			
			<?php if( $wproto_section->after_text <> '' ): ?>
			<div class="portfolio-categories-description"><?php echo apply_filters( 'the_content', $wproto_section->after_text ); ?></div>
			<?php endif; ?>
			
			<?php if( isset( $section_data['display_call_to_action_button'] ) && $section_data['display_call_to_action_button'] == 'yes' ): ?>
			<p>
				<a href="<?php echo isset( $section_data['button_link'] ) ? $section_data['button_link'] : ''; ?>" class="button"><?php echo isset( $section_data['button_text'] ) ? $section_data['button_text'] : ''; ?></a>
			</p>
			<?php endif; ?>
				
		</div>
		
		<div class="unit three-quarters home-portfolio-items-container">
			<?php get_template_part('part-home-portfolio'); ?>
		</div>
		
	</div>

</section>
<?php wp_reset_query(); endif; 