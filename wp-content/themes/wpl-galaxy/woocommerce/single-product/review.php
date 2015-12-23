<?php
/**
 * Review Comments Template
 *
 * Closing li is left out on purpose!
 *
 * @author 		WooThemes
 * @package 	WooCommerce/Templates
 * @version     2.1.0
 */

if ( ! defined( 'ABSPATH' ) ) exit; // Exit if accessed directly

global $post, $wpl_galaxy_wp;
$rating = esc_attr( get_comment_meta( $GLOBALS['comment']->comment_ID, 'rating', true ) );
?>
<li itemprop="reviews" itemscope itemtype="http://schema.org/Review" <?php comment_class(); ?> id="li-comment-<?php comment_ID() ?>">
	<div id="comment-<?php comment_ID(); ?>" class="comment_container comment-inside">

		<div class="comment-avatar">
			<div><?php $avatar_size = wpl_galaxy_wp_utils::is_retina() ? 140 : 70; echo get_avatar( $GLOBALS['comment']->comment_ID, $avatar_size ); ?></div>
		</div>
		
		<div class="comment-data">
			<span class="author">
				<?php echo get_comment_author_link(); ?>
			</span>
			<span class="time">
				<span><?php echo get_comment_date( $wpl_galaxy_wp->get_option('date_format') ); ?></span>
			</span>

		</div>
		
		<div class="comment-content">
		
			<?php if ( get_option('woocommerce_enable_review_rating') == 'yes' ) : ?>

				<div class="star-rating">
					<span><?php echo wpl_galaxy_wp_front::get_rating_html( intval( get_comment_meta( $GLOBALS['comment']->comment_ID, 'rating', true ) ) ); ?></span>
				</div>

			<?php endif; ?>
		
			<?php comment_text(); ?>
		</div>

		<div class="clear"></div>
	</div>
