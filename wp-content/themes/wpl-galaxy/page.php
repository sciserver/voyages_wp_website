<?php get_header(); ?>

	<!-- 
	
		CONTENT SECTION
		
	-->
	
	<div id="content" class="wrapper">
		<div class="grid">

			<section class="<?php wpl_galaxy_wp_front::content_classes(); ?>">
				
				<article class="post">
				
					<?php if( have_posts() ): while ( have_posts() ) : the_post(); ?>
				
					<!--
					
						POST HEADER
						
					-->
				
					<?php wpl_galaxy_wp_front::post_header(); ?>
					
					<?php wpl_galaxy_wp_front::slider('post_header'); ?>
					
					<!--
					
						POST CONTENT
						
					-->
					<div class="post-content-container">
						<?php the_content(); ?>
						
						<?php wp_link_pages('before=<div class="pagination post-paginate">&after=</div>&next_or_number=next'); ?>
					</div>
					
					<?php comments_template( '', true ); ?>
					
					<?php endwhile; endif; ?>
				
				</article>
				
			</section>

			<?php get_sidebar(); ?>
			
		</div>
	</div> <!-- /content -->

<?php get_footer();