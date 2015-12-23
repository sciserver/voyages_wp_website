<?php
/**
 * The template for displaying product content within loops.
 *
 * Override this template by copying it to yourtheme/woocommerce/content-product.php
 *
 * @author 		WooThemes
 * @package 	WooCommerce/Templates
 * @version     1.6.4
 */
 
if ( ! defined( 'ABSPATH' ) ) exit; // Exit if accessed directly

global $product, $woocommerce_loop;

// Store loop count we're currently on
if ( empty( $woocommerce_loop['loop'] ) )
	$woocommerce_loop['loop'] = 0;

// Store column count for displaying the grid
if ( empty( $woocommerce_loop['columns'] ) ) {
	$woocommerce_loop['columns'] = apply_filters( 'loop_shop_columns', 1 );
} 
// Ensure visibility
if ( ! $product || ! $product->is_visible() )
	return;

// Increase loop count
$woocommerce_loop['loop']++;

// Extra post classes
$classes = array('unit');
if ( 0 == ( $woocommerce_loop['loop'] - 1 ) % $woocommerce_loop['columns'] || 1 == $woocommerce_loop['columns'] )
	$classes[] = 'first';
if ( 0 == $woocommerce_loop['loop'] % $woocommerce_loop['columns'] )
	$classes[] = 'last';

if( $woocommerce_loop['columns'] > 1 ) {
	$classes[] = wpl_galaxy_wp_front::get_column_name( $woocommerce_loop['columns'] );
}

?>
<div <?php post_class( $classes ); ?>>

	<?php do_action( 'woocommerce_before_shop_loop_item' ); ?>

	<a href="<?php the_permalink(); ?>">

		<?php
			$thumb_size = wpl_galaxy_wp_utils::is_retina() ? 'shop-product-preview-2x' : 'shop-product-preview';
			$image = wp_get_attachment_image_src( get_post_thumbnail_id( get_the_ID() ), $thumb_size );
			if( isset( $image[0] ) ):
		?>
		<img src="<?php echo $image[0]; ?>" width="180" alt="" />
		<?php endif; ?>

		<h3><?php the_title(); ?></h3>

	</a>
	
	<p><?php echo wpl_galaxy_wp_utils::custom_excerpt( get_the_excerpt(), 120 );  ?></p>

	<?php do_action( 'woocommerce_after_shop_loop_item_title' ); ?>

	<?php do_action( 'woocommerce_after_shop_loop_item' ); ?>

</div>