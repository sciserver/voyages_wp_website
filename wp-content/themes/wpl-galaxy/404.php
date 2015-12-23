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
						<h1 class="post-title"><?php _e( 'Not Found', 'wproto' ); ?></h1>
						<?php wpl_galaxy_wp_front::breadcrumbs( true, ' <i class="delimeter"></i> ', true ); ?>
					</header>
					
					<!--
					
						POST CONTENT
						
					-->
					
					<div class="post-content">
						
						<section class="grid">
						
							<header class="whole search-page-form">
								<div class="inner">
							
									<?php wpl_galaxy_wp_front::pagination(); ?>
									
									<h2><?php _e( 'It looks like nothing was found at this location. Maybe try a search?', 'wproto' ); ?></h2>
								
									<form action="<?php echo site_url(); ?>" class="search-form" method="get">
										<fieldset>
											<input type="text" name="s" value="<?php echo get_query_var('s'); ?>" placeholder="<?php _e('Search request here', 'wproto'); ?>" /> <a href="javascript:;" class="button"><i class="fa fa-search"></i>&nbsp;</a>
										</fieldset>
									</form>
								
									<div class="clear"></div>
								</div>
							</header>
														
						</section>
					</div>
				
				</div>
				
			</section>
			
		</div>
	</div> <!-- /content -->

<?php get_footer();