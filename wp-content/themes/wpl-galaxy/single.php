<?php get_header(); global $wpl_galaxy_wp; ?>

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
					
					<div class="ib post-date">
						
						<div class="ib day"><?php the_time('d'); ?></div>
						<div class="month"><?php the_time('F'); ?></div>
						<div class="year"><?php the_time('Y'); ?></div>
						
						<div class="comments-count"><a href="#comments"><i class="fa fa-comments-o"></i> <?php echo get_comments_number(); ?></a></div>
						
					</div>
					
					<!--
					
						POST CONTENT
						
					-->
					<div class="ib post-content">
					
						<!-- POST SLIDER OR POST THUMBNAIL -->
						<?php wpl_galaxy_wp_front::thumbnail( get_the_ID(), 'post-thumb-full', 'single' ); ?>
					
						<!-- LAYER SLIDER -->
						<?php wpl_galaxy_wp_front::slider('post_header'); ?>
					
						<!-- POST CONTENT -->
						<div class="post-text">
							<div class="post-content-container">
								<?php the_content(); ?>
								
								<?php wp_link_pages('before=<div class="pagination post-paginate">&after=</div>&next_or_number=next'); ?>
							</div>
							
							<?php if( !post_password_required() ): ?>
							<!--
						
								POST FOOTER
							
							-->
							<footer>
					
								<p>
									<span class="post-like"><?php wpl_galaxy_wp_front::likes( get_the_ID() ); ?></span> 
									<span class="post-views"><?php wpl_galaxy_wp_front::views( get_the_ID() ); ?></span>
								</p>  
					
								<?php
									$tags_list = wpl_galaxy_wp_front::get_valid_tags_list(', ');
									if( $tags_list <> '' ):
								?>
								<p>
									<strong><?php _e('Tags', 'wproto'); ?>:</strong>
									<?php echo $tags_list; ?>
								</p>
								<?php endif; ?>
							
								<?php
									$cats_list = wpl_galaxy_wp_front::get_valid_category_list(', ');
									if( $cats_list <> '' ):
								?>
								<p>
									<strong><?php _e('Categories', 'wproto'); ?>:</strong>
									<?php echo $cats_list; ?>
								</p>
								<?php endif; ?>
							
								<?php wpl_galaxy_wp_front::share_post_code(); ?>
							
								<!--
							
									AUTHOR INFO BLOCK
								
								-->
								<?php wpl_galaxy_wp_front::post_author_info(); ?>
					
							</footer>
							<?php endif; ?>
							
						</div>
					</div>
					
					<!-- 
					
						RELATED POSTS BLOCK
						
					-->
					<?php wpl_galaxy_wp_front::related_posts( get_the_ID() ); ?>
					
					<!--
						
						COMMENTS
						
					-->
					<?php if( !post_password_required() ): ?>
						<?php comments_template( '', true ); ?>
					<?php endif; ?>
					
					<?php endwhile; endif; ?>
				
				</article>
				
			</section>

			<?php get_sidebar(); ?>
			
		</div>
	</div> <!-- /content -->

<?php get_footer();