<?php

	$_post_type = $data['post_type'];
	$_taxonomy_name = $data['taxonomy_name'];

	global $wp_query, $post, $wpl_galaxy_wp;
	get_header();	
	$paged = (get_query_var('paged')) ? get_query_var('paged') : 1;

?>

	<!-- 
	
		CONTENT SECTION
		
	-->
	
	<div id="content" class="wrapper">
		<div class="grid">

			<section class="<?php wpl_galaxy_wp_front::content_classes(); ?>">

				<?php if( have_posts() ): while ( have_posts() ) : the_post(); ?>
				
				<?php
					$_page_query = $wp_query;
					$_post = $post;
					$page_content = apply_filters('the_content', get_the_content() );
	
					$template_settings = $wpl_galaxy_wp->model->post->get_post_custom( get_the_ID() );
				?>

				<?php wpl_galaxy_wp_front::post_header(); ?>
					
				<?php wpl_galaxy_wp_front::slider('post_header'); ?>
				
				<?php if( isset( $template_settings->wproto_content_layout_display_page_text ) && $template_settings->wproto_content_layout_display_page_text == 'before' ): ?>
				
					<article class="post">
						<?php echo $page_content; ?>
					</article>
				
				<?php endif; ?>
				
				<?php
				
					// Make query of posts
				
					$layout = isset( $template_settings->wproto_content_layout ) ? $template_settings->wproto_content_layout : '';
					$display_filters = isset( $template_settings->wproto_content_layout_filters ) ? $template_settings->wproto_content_layout_filters : 'no';
					$display_type = isset( $template_settings->wproto_content_display_posts_type ) ? $template_settings->wproto_content_display_posts_type : 'all';
					$posts_count = isset( $template_settings->wproto_content_layout_posts_per_page ) ? $template_settings->wproto_content_layout_posts_per_page : get_option('posts_per_page');
					$display_categories = isset( $template_settings->wproto_content_display_categories ) ? unserialize( $template_settings->wproto_content_display_categories ) : 0;
					$display_categories = is_array( $display_categories ) && isset( $display_categories[ $_taxonomy_name ] ) ? $display_categories[ $_taxonomy_name ] : 0;
					
					$order_by = isset( $template_settings->wproto_content_display_posts_order ) ? $template_settings->wproto_content_display_posts_order : 'date';
					$sort_by = isset( $template_settings->wproto_content_display_posts_sort ) ? $template_settings->wproto_content_display_posts_sort : 'DESC';
				
					if( $layout == 'hexagon' && $display_filters == 'yes' ) {
						$display_type = 'all';
						$display_categories = '';
						$order_by = 'date';
						$sort_by = 'DESC';
					}
				
					$wp_query = $wpl_galaxy_wp->model->post->get( $display_type, $posts_count, $display_categories, $order_by, $sort_by, $_post_type, $_taxonomy_name, false, false, false, $paged );
				
					if( $layout == 'hexagon' && $display_filters == 'yes' ) {
						get_template_part( 'part-hexagon-filters' );
					}
				
					get_template_part( 'layouts/' . $layout );
					
					$show_pagination = isset( $template_settings->wproto_content_pagination ) ? $template_settings->wproto_content_pagination : 'yes';
					$pagination_style = isset( $template_settings->wproto_content_pagination_style ) ? $template_settings->wproto_content_pagination_style : 'numeric';
					
					if( $layout == 'hexagon' && $display_filters == 'yes' ) {
						$show_pagination = 'yes';
						$pagination_style = 'ajax';
					}
					
					if( $show_pagination != 'no' ) wpl_galaxy_wp_front::pagination( $pagination_style, $layout, $_post_type, $display_type );
					
					// get back to the main query
					$wp_query = $_page_query;
					$post = $_post;
				?>
				
				<?php if( isset( $template_settings->wproto_content_layout_display_page_text ) && $template_settings->wproto_content_layout_display_page_text == 'after' ): ?>
				
					<article class="post">
						<?php echo $page_content; ?>
					</article>
				
				<?php endif; ?>
    
    		<?php endwhile; endif; ?>
    
			</section>
			
			<?php get_sidebar(); ?>
			
		</div>
	</div>

<?php
	get_footer(); 