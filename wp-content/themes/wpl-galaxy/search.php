<?php get_header(); global $wp_query, $paged; $paged = $paged > 0 ? $paged : 0; ?>

	<!-- 
	
		CONTENT SECTION
		
	-->
	
	<div id="content" class="wrapper">
		<div class="grid">

			<section class="unit whole">
				
				<div class="post">
				
					<!--
					
						POST HEADER
						
					-->
				
					<header class="post-header">
						<h1 class="post-title"><?php _e( sprintf( 'Search results for &laquo;%s&raquo;', get_query_var('s') ), 'wproto' ); ?></h1>
						<?php wpl_galaxy_wp_front::breadcrumbs( true, ' <i class="delimeter"></i> ', true ); ?>
					</header>
					
					<!--
					
						POST CONTENT
						
					-->
					
					<div class="post-content">
						
						<section class="grid">
						
							<header class="unit whole search-page-form">
								<div class="inner">
								
									<?php wpl_galaxy_wp_front::pagination(); ?>
								
									<form action="<?php echo site_url(); ?>" class="search-form" method="get">
										<fieldset>
											<input type="text" name="s" value="<?php echo get_query_var('s'); ?>" placeholder="<?php _e('Search request here', 'wproto'); ?>" /> <a href="javascript:;" class="button"><i class="fa fa-search"></i>&nbsp;</a>
										</fieldset>
									</form>
								
									<div class="info">
										<?php _e( 'Page', 'wproto'); ?> <strong><?php echo $paged; ?></strong> <?php _e( 'of', 'wproto'); ?> <strong><?php echo $wp_query->max_num_pages > 0 ? $wp_query->max_num_pages : 1; ?></strong> [ <?php _e( 'results', 'wproto'); ?>: <strong><?php echo $wp_query->found_posts; ?></strong> ]
									</div>
									<div class="clear"></div>
								</div>
							</header>
							
							<!-- SEARCH RESULTS -->
							<div class="posts unit whole">
								<div class="inner">
									<?php if( have_posts() ): ?>
									
										<?php get_template_part( 'layouts/one_column_grid' ); ?>
									
									<?php else: ?>
										
										<h2><?php _e( 'Nothing was found. Try another search query.', 'wproto'); ?></h2>
										
									<?php endif; ?>
								</div>
							</div>

							<footer class="unit whole search-results-footer">
								<div class="inner">
									<?php wpl_galaxy_wp_front::pagination(); ?>
								</div>

							</footer>
							
						</section>
					</div>
				
				</div>
				
			</section>
			
		</div>
	</div> <!-- /content -->

<?php get_footer();