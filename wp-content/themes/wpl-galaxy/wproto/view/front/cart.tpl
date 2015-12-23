<?php global $woocommerce; ?>

<?php if( count( $data['cart'] ) > 0 ): ?>

	<?php foreach( $data['cart'] as $id=>$item ): ?>
	
	<?php
		$product = get_product( $item['data']->post->ID );
		
		$thumb_size = wpl_galaxy_wp_utils::is_retina() ? 'photo-small-2x' : 'photo-small';
		$img = wp_get_attachment_image_src( get_post_thumbnail_id( $item['data']->post->ID ), $thumb_size );
		$img_full = wp_get_attachment_image_src( get_post_thumbnail_id( $item['data']->post->ID ), 'full' );
		$image = has_post_thumbnail( $item['data']->post->ID ) && isset( $img[0] ) ? $img[0] : woocommerce_placeholder_img_src();
	?>
	
	<div class="item">
		<a href="<?php echo $woocommerce->cart->get_remove_url( $id ); ?>" class="cart-remove" data-id="">&times;</a>
		<div class="thumb">
			<a href="<?php echo get_permalink( $item['data']->post->ID ); ?>"><img src="<?php echo $image; ?>" width="75" alt="" /></a>
		</div>
		
		<div class="desc">
			<h3><?php echo $item['data']->post->post_title; ?></h3>
			<div class="count">
				<?php echo $item['quantity']; ?> &times; <?php echo $product->get_price_html(); ?>
			</div>
		</div>
	
	</div>
	
	<?php endforeach; ?>
	
	<div class="cart-subtotal">
		<?php _e('Cart subtotal', 'wproto'); ?>: <span class="pull-right"><?php echo $data['totals']; ?></span>
		<div class="clear"></div>
	</div>
	
	<div class="cart-links">
	
		<a href="<?php echo $woocommerce->cart->get_cart_url(); ?>" class="button pull-left"><?php _e('View Cart','wproto'); ?></a>
		<a href="<?php echo $woocommerce->cart->get_checkout_url(); ?>" class="button pull-right"><?php _e('Checkout','wproto'); ?></a>
		<div class="clear"></div>
	</div>

<?php else: ?>

	<p class="empty"><a href="javascript:;" class="pull-right button" id="wproto-close-ajax-cart"><?php _e('Close', 'wproto'); ?></a> <?php _e('Your cart is currently empty.', 'wproto'); ?></p> 

<?php endif;