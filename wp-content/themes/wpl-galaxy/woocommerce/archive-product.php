<?php
/**
 * The Template for displaying product archives, including the main shop page which is a post type archive.
 *
 * Override this template by copying it to yourtheme/woocommerce/archive-product.php
 *
 * @author 		WooThemes
 * @package 	WooCommerce/Templates
 * @version     2.0.0
 */
 
	if ( ! defined( 'ABSPATH' ) ) exit; // Exit if accessed directly
	get_header();
	global $wpl_galaxy_wp, $wp_query;
?>

<!-- 
	
	CONTENT SECTION
		
-->
	
<div id="content" class="wrapper">
	<div class="grid">

		<section class="<?php wpl_galaxy_wp_front::content_classes(); ?>">
		
		<?php
			$page_settings = $wpl_galaxy_wp->model->post->get_post_custom( woocommerce_get_page_id( 'shop' ) );
			if( !isset( $page_settings->wproto_post_hide_title ) || $page_settings->wproto_post_hide_title != 'yes' ):
		?>
		
		<header class="post-header">
			<h1 class="post-title"><?php woocommerce_page_title(); ?></h1>
			<?php do_action('woocommerce_before_main_content'); ?>
		</header>
		
		<?php
			endif;
		?>
		
		<?php if( !is_product_category() ) wpl_galaxy_wp_front::slider('post_header'); ?>
		
		<?php
			// get category image
			$term = $wp_query->get_queried_object();
			if( is_object( $term ) && isset( $term->term_id ) ) {
				$thumbnail_id = get_woocommerce_term_meta( $term->term_id, 'thumbnail_id', true );
				
				$category_image = wp_get_attachment_image_src( $thumbnail_id, wpl_galaxy_wp_utils::is_retina() ? 'category-thumb-full-2x' : 'category-thumb-full' );
					
			}
			if( is_object( $term ) && isset( $category_image[0] ) ):
		?>
			<div class="term-image">
				<img src="<?php echo $category_image[0]; ?>" alt="" />
			</div>
		<?php
			endif;
			// category description
			do_action( 'woocommerce_archive_description' );
		?>
		
		<?php if ( have_posts() ) : ?>
		
			<div class="grid">
				<?php woocommerce_product_subcategories(); ?>
			</div>
		
			<?php do_action( 'woocommerce_before_shop_loop' ); ?>
			
			<!--
					
				PRODUCTS
						
			-->
			<?php
				$view = !isset( $_GET['wproto_view'] ) || $_GET['wproto_view'] == 'grid' ? 'grid' : 'list';
			?>
			<div id="shop-posts-list" class="posts view-<?php echo $view; ?>" data-appear-animation="fadeIn">
					
				<?php while ( have_posts() ) : the_post(); ?>
					
					<?php
						global $product;
						$sku = $product->get_sku();
						$average = $product->get_average_rating();
						$rating_html = wpl_galaxy_wp_front::get_rating_html( $average );
						$comments_count = wp_count_comments( get_the_ID() );
					?>
					
					<article class="post">
						
						<div class="outer"></div>
						
							<div class="inside">
						
								<div class="thumbnail">
									<?php wpl_galaxy_wp_front::thumbnail( get_the_ID(), 'shop-product-thumb' ); ?>
									<?php
										$badge = get_post_meta( get_the_ID(), 'badge', true ); 
										if( $badge == 'onsale' ):
									?>
									<div class="sale" data-appear-animation="rotateIn"><?php _e('Sale', 'wproto'); ?></div>
									<?php elseif( $badge == 'best_price' ): ?>
									<div class="best-price" data-appear-animation="rotateIn"><?php _e('Best<br />Price', 'wproto'); ?></div>
									<?php 
										endif;
									?>
								</div>
							
								<div class="post-content">
							
									<h4><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h4>
							
									<?php if( $sku <> '' ): ?>
									<div class="sku list-only">
										SKU: <?php echo $sku; ?>
									</div>
									<?php endif; ?>
							
									<div class="rating">
										<?php echo $rating_html; ?>
										<span>(<strong><?php echo $comments_count->total_comments; ?></strong> <?php _e('reviews', 'wproto'); ?>)</span>
									</div>
							
									<div class="price list-only">
										<?php echo $product->get_price_html(); ?>
									</div>
							
									<div class="excerpt list-only">
										<p><?php echo wpl_galaxy_wp_utils::custom_excerpt( get_the_excerpt(), 213 ); ?></p>
									</div>
								
									<div class="excerpt grid-only">
										<p><?php echo wpl_galaxy_wp_utils::custom_excerpt( get_the_excerpt(), 45 ); ?></p>
									</div>
							
									<div class="price grid-only">
										<?php echo $product->get_price_html(); ?>
									</div>
							
									<a href="<?php echo add_query_arg( array('add-to-cart' => get_the_ID() ), get_permalink() ); ?>" class="button desktop"><?php _e('Add to cart', 'wproto'); ?></a>
									
									<a href="<?php echo add_query_arg( array('add-to-cart' => get_the_ID() ), get_permalink() ); ?>" class="button show-on-phone"><?php _e('Buy it', 'wproto'); ?></a>
								
								</div>
							</div>
						
					</article>
					
				<?php endwhile; // end of the loop. ?>
				
			</div>
			
			<?php do_action( 'woocommerce_after_shop_loop' ); ?>
		
		<?php elseif( ! woocommerce_product_subcategories( array( 'before' => woocommerce_product_loop_start( false ), 'after' => woocommerce_product_loop_end( false ) ) ) ): ?>
		
			<div class="post-content">
						
				<section class="message-404">

					<h1><?php _e('No products were found', 'wproto'); ?></h1>
							
					<p><?php _e('We\'re sorry, but this category does not have any product yet', 'wproto'); ?></p>

				</section>

			</div>
		
		<?php endif; ?>
		
		<?php do_action('woocommerce_after_main_content'); ?>
		
		</section>

		<?php get_sidebar(); ?>
			
	</div>
</div> <!-- /content -->

<?php
	get_footer();