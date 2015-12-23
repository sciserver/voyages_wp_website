<?php
/**
 * Single Product Price, including microdata for SEO
 *
 * @author 		WooThemes
 * @package 	WooCommerce/Templates
 * @version     1.6.4
 */

if ( ! defined( 'ABSPATH' ) ) exit; // Exit if accessed directly

global $post, $product;
$average = $product->get_average_rating();
$rating_html = wpl_galaxy_wp_front::get_rating_html( $average );
$comments_count = wp_count_comments( get_the_ID() );
?>
<header>

	<div class="price"><?php echo $product->get_price_html(); ?></div>
	
	<span class="add-to-cart">
		
	</span>
	
	<div class="rating">
		<?php echo $rating_html; ?> 
		<span>(<strong><?php echo $comments_count->total_comments; ?></strong> <?php _e('reviews', 'wproto'); ?>)</span>
	</div>

</header>