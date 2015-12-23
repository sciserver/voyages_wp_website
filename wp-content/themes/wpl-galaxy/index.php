<?php global $wp_query; get_header(); ?>

	<!-- 
	
		CONTENT SECTION
		
	-->
	
	<div id="content" class="wrapper">
		<div class="grid">

			<section class="<?php wpl_galaxy_wp_front::content_classes(); ?>">
			
				<?php
					
					/**
					 * Page Title
					 **/
					
					$term = get_term_by( 'slug', get_query_var( 'term' ), get_query_var( 'taxonomy' ) );
				
					$title = __('Blog', 'wproto');
					
					if( is_archive() ) $title = __('Blog Archive', 'wproto');
					
					if( is_category() ) $title = sprintf( __( 'Posts in &laquo;%s&raquo; category', 'wproto' ), single_cat_title('', false) );
					
					if( is_tag() ) $title = sprintf( __( 'Posts tagged with &laquo;%s&raquo;', 'wproto' ), single_tag_title('', false) );
					
					if( is_tax('wproto_portfolio_category') ) $title = sprintf( __( 'Works in &laquo;%s&raquo; category', 'wproto' ), $term->name );
					
					if( is_tax('wproto_catalog_category') ) $title = sprintf( __( 'Products in &laquo;%s&raquo; category', 'wproto' ), $term->name );
					
					if( is_tax('wproto_photoalbums_category') ) $title = sprintf( __( 'Albums in &laquo;%s&raquo; category', 'wproto' ), $term->name );
					
					if( is_tax('wproto_video_category') ) $title = sprintf( __( 'Videos in &laquo;%s&raquo; category', 'wproto' ), $term->name );
					
					if( is_tax('wproto_video_tag') ) $title = sprintf( __( 'Videos tagged with &laquo;%s&raquo;', 'wproto' ), $term->name );
					
					if( is_tax('wproto_catalog_tag') ) $title = sprintf( __( 'Products tagged with &laquo;%s&raquo;', 'wproto' ), $term->name );
				
				?>
			
				<header class="post-header">
					<h1 class="post-title"><?php echo $title; ?></h1>
					<?php wpl_galaxy_wp_front::breadcrumbs( true, ' <i class="delimeter"></i> ', true ); ?>
				</header>

				<?php
					
					/**
					 * Category description and category featured image
					 **/
					
					if( is_category() || is_tax('wproto_portfolio_category') || is_tax('wproto_catalog_category') || is_tax('wproto_photoalbums_category') || is_tax('wproto_video_category') ):
						$tax_settings = get_option( "taxonomy_$wp_query->queried_object_id" );
						$cat_image_id = isset( $tax_settings['category_image_id'] ) ? absint( $tax_settings['category_image_id'] ) : 0;
						$category_image = wp_get_attachment_image_src( $cat_image_id, wpl_galaxy_wp_utils::is_retina() ? 'category-thumb-full-2x' : 'category-thumb-full' );
						
						$category_description = category_description();
						
						if( isset( $category_image[0] ) ):
						?>
						<div class="category-featured-image">
							<img src="<?php echo $category_image[0]; ?>" alt="" />
						</div>
						<?php endif; ?>
						<?php if( $category_description <> '' ): ?>
						<div class="category-description">
							<?php echo $category_description; ?>
						</div>
						<?php endif; ?>
						<?php
					endif;
					
				?>
				
				<?php if( $wp_query->have_posts() ): ?>

					<?php
						get_template_part( 'layouts/one_column_grid' );
						
						wpl_galaxy_wp_front::pagination();
						
					?>
				
				<?php else: ?>
	
					<div class="post-content">
						
						<section class="message-404">

							<h1><?php _e('No posts were found', 'wproto'); ?></h1>
							
							<p><?php _e('We\'re sorry, but this section does not have any post yet', 'wproto'); ?></p>

						</section>

					</div>
	
				<?php endif; ?>
				
			</section>

			<?php get_sidebar(); ?>
			
		</div>
	</div> <!-- /content -->

<?php get_footer();