<?php
/**
 * Single Product Image
 *
 * @author 		WooThemes
 * @package 	WooCommerce/Templates
 * @version     2.0.14
 */

if ( ! defined( 'ABSPATH' ) ) exit; // Exit if accessed directly

global $post, $woocommerce, $product;

?>
<div class="images">
	<?php
		$badge = get_post_meta( get_the_ID(), 'badge', true ); 
		if( $badge == 'onsale' ):
	?>
	<span class="sale" data-appear-animation="rotateIn"><?php _e('Sale', 'wproto'); ?></span>
	<?php elseif( $badge == 'best_price' ): ?>
	<span class="best-price" data-appear-animation="rotateIn"><?php _e('Best<br />Price', 'wproto'); ?></span>
	<?php endif; ?>

	<?php
	
		$thumb_size = wpl_galaxy_wp_utils::is_retina() ? 'shop-product-big-2x' : 'shop-product-big';
		$img = wp_get_attachment_image_src( get_post_thumbnail_id( get_the_ID() ), $thumb_size );
		$img_full = wp_get_attachment_image_src( get_post_thumbnail_id( get_the_ID() ), 'full' );
		$image = has_post_thumbnail() && isset( $img[0] ) ? $img[0] : woocommerce_placeholder_img_src();
	
	?>

	<a href="<?php echo isset( $img_full[0] ) ?  $img_full[0] : woocommerce_placeholder_img_src(); ?>" class="woocommerce-main-image image-link zoom"><img width="360" height="369" src="<?php echo $image; ?>" class="attachment-shop_single wp-post-image" alt="" title="" /></a>

	<?php
		$gallery_images = $product->get_gallery_attachment_ids();
		
		if( count( $gallery_images ) > 0 ):
	?>
	<div class="thumbnails product-scroller">
							
		<div class="scroller">
			<?php foreach( $gallery_images as $k=>$id ): ?>
			
			<?php
				$thumb_size = wpl_galaxy_wp_utils::is_retina() ? 'photo-small-2x' : 'photo-small';
				$img = wp_get_attachment_image_src( $id, $thumb_size );
				$img_medium = wp_get_attachment_image_src( $id, wpl_galaxy_wp_utils::is_retina() ? 'shop-product-big-2x' : 'shop-product-big' );
				$img_full = wp_get_attachment_image_src( $id, 'full' );
			?>
			
			<a data-full-src="<?php echo $img_full[0]; ?>" data-medium-src="<?php echo $img_medium[0]; ?>" href="<?php echo $img_full[0]; ?>" class="small-image-link first">
				<img width="67" height="68" src="<?php echo $img[0]; ?>" class="attachment-shop_thumbnail" alt="" />
			</a>
			<?php endforeach; ?>
		</div>									
	</div>
	<?php endif; ?>

</div>
