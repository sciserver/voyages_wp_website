<?php
/**
 * Mini-cart
 *
 * Contains the markup for the mini-cart, used by the cart widget
 *
 * @author 		WooThemes
 * @package 	WooCommerce/Templates
 * @version     2.1.0
 */
 
	if ( ! defined( 'ABSPATH' ) ) exit; // Exit if accessed directly
	global $woocommerce;
	$thumb_size = wpl_galaxy_wp_utils::is_retina() ? 'photo-small-2x' : 'photo-small';
?>

<?php do_action( 'woocommerce_before_mini_cart' ); ?>

	<?php if ( sizeof( $woocommerce->cart->get_cart() ) > 0 ) : ?>
		<?php foreach ( $woocommerce->cart->get_cart() as $cart_item_key => $cart_item ) :

			$_product = $cart_item['data'];

			// Only display if allowed
			if ( ! apply_filters('woocommerce_widget_cart_item_visible', true, $cart_item, $cart_item_key ) || ! $_product->exists() || $cart_item['quantity'] == 0 )
				continue;

			// Get price
			$product_price = get_option( 'woocommerce_tax_display_cart' ) == 'excl' ? $_product->get_price_excluding_tax() : $_product->get_price_including_tax();

			$product_price = apply_filters( 'woocommerce_cart_item_price_html', woocommerce_price( $product_price ), $cart_item, $cart_item_key );
			?>

			<div class="item">

				<div class="thumbnail">
					<a href="<?php echo get_permalink( $cart_item['product_id'] ); ?>">
						<?php echo ( has_post_thumbnail( $cart_item['product_id'] ) ? get_the_post_thumbnail( $cart_item['product_id'], $thumb_size ) : woocommerce_placeholder_img( $thumb_size ) ) ?>
					</a>
				</div>
						
				<div class="description">
						
					<a href="<?php echo get_permalink( $cart_item['product_id'] ); ?>" class="title"><?php echo apply_filters('woocommerce_widget_cart_product_title', $_product->get_title(), $_product ); ?></a>
					<?php echo apply_filters( 'woocommerce_widget_cart_item_quantity', '<span class="quantity">' . sprintf( '<span class="price">%s</span> <span class="amount">&times; <strong>%s</strong></span>', $product_price, $cart_item['quantity'] ) . '</span>', $cart_item, $cart_item_key ); ?>
						
				</div>

			</div>

		<?php endforeach; ?>

	<?php else : ?>

		<p><?php _e( 'No products in the cart.', 'woocommerce' ); ?></p>

	<?php endif; ?>

<?php if ( sizeof( $woocommerce->cart->get_cart() ) > 0 ) : ?>

	<div class="subtotal"><?php _e( 'Subtotal', 'woocommerce' ); ?>: <?php echo $woocommerce->cart->get_cart_subtotal(); ?></div>

	<?php do_action( 'woocommerce_widget_shopping_cart_before_buttons' ); ?>

	<a href="<?php echo $woocommerce->cart->get_cart_url(); ?>" class="button"><?php _e( 'View Cart', 'woocommerce' ); ?></a>
	<a href="<?php echo $woocommerce->cart->get_checkout_url(); ?>" class="button checkout"><?php _e( 'Checkout', 'woocommerce' ); ?></a>

<?php endif; ?>

<?php do_action( 'woocommerce_after_mini_cart' ); ?>
