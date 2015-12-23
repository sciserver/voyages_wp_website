<?php
/**
 * The Template for displaying all single products.
 *
 * Override this template by copying it to yourtheme/woocommerce/single-product.php
 *
 * @author 		WooThemes
 * @package 	WooCommerce/Templates
 * @version     1.6.4
 */
 
	if ( ! defined( 'ABSPATH' ) ) exit; // Exit if accessed directly
	get_header();
?>

<!-- 
	
	CONTENT SECTION
		
-->
	
<div id="content" class="wrapper">
	<div class="grid">

		<section class="<?php wpl_galaxy_wp_front::content_classes(); ?>">
		
			<article class="post">
				
				<?php
	 				if ( ! post_password_required() ):
				?>
				
				<?php if( have_posts() ): while ( have_posts() ) : the_post(); ?>
				
					<!--
					
						POST HEADER
						
					-->
				
					<?php wpl_galaxy_wp_front::post_header(); ?>
					
					<?php wpl_galaxy_wp_front::slider('post_header'); ?>
					
					<!--
					
						POST CONTENT
						
					-->
					<?php do_action( 'woocommerce_before_single_product' ); ?>
					<div class="ib post-content">
						
						<div class="post-text">
						
							<div <?php post_class(); ?>>
								<?php do_action( 'woocommerce_before_single_product_summary' ); ?>
								<div class="summary entry-summary">
								<?php do_action( 'woocommerce_single_product_summary' ); ?>
								</div>
							</div>
						
						</div>
						
					</div>
					
					<?php
						do_action( 'woocommerce_after_single_product_summary' );
						do_action( 'woocommerce_after_single_product' );
					?>
				
				<?php wpl_galaxy_wp_front::related_posts( get_the_ID(), 8, 'product_cat' ); ?>
				
				<?php endwhile; endif; ?>
				
				<?php do_action('woocommerce_after_main_content'); ?>
				
				<?php else: ?>
				
					<?php echo get_the_password_form(); ?>
					
				<?php endif; ?>
				
			</article>
				
		</section>

		<?php get_sidebar(); ?>
			
	</div>
</div> <!-- /content -->

<?php
	get_footer();