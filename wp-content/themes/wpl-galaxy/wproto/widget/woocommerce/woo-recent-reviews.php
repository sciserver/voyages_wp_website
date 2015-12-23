<?php

$override_widget = WP_PLUGIN_DIR . '/woocommerce/includes/widgets/class-wc-widget-recent-reviews.php';

if( class_exists( 'woocommerce' ) && file_exists( $override_widget ) ) {
	
	require_once( $override_widget );
	
	if( class_exists('WC_Widget_Recent_Reviews') ) {

		class wpl_galaxy_wp_woo_recent_reviews_widget extends WC_Widget_Recent_Reviews {

	 		public function widget( $args, $instance ) {
				global $comments, $comment, $woocommerce;

				if ( $this->get_cached_widget( $args ) )
					return;

					ob_start();
					extract( $args );

					$title    = apply_filters( 'widget_title', $instance['title'], $instance, $this->id_base );
					$number   = absint( $instance['number'] );
					$comments = get_comments( array( 'number' => $number, 'status' => 'approve', 'post_status' => 'publish', 'post_type' => 'product' ) );

					if ( $comments ) {
						echo $before_widget;
						if ( $title ) echo $before_title . $title . $after_title;
						echo '<div class="items">';

						foreach ( (array) $comments as $comment) {

							$_product = get_product( $comment->comment_post_ID );

							$rating = intval( get_comment_meta( $comment->comment_ID, 'rating', true ) );

							$rating_html = wpl_galaxy_wp_front::get_rating_html( $rating );
							$comments_count = wp_count_comments( $comment->comment_post_ID );
						
							?>
							<div class="item">
					
								<div class="thumbnail">
									<a href="<?php echo esc_url( get_comment_link( $comment->comment_ID ) ); ?>"><?php echo $_product->get_image(); ?></a>
								</div>
						
								<div class="description">
									<a href="<?php echo esc_url( get_comment_link( $comment->comment_ID ) ); ?>" class="title"><?php echo $_product->get_title(); ?></a>
									<div class="review-by"><?php printf( _x( 'by %1$s', 'by comment author', 'wproto' ), get_comment_author() ); ?></div>
								</div>
					
								<div class="rating">
									<?php echo $rating_html; ?>
									(<strong><?php echo $comments_count->total_comments; ?></strong> <?php echo wpl_galaxy_wp_utils::plural_form( $comments_count->total_comments, __('review', 'wproto'), __('reviews', 'wproto'), __('reviews', 'wproto') ); ?>)
								</div>

							</div>
							<?php
						}

						echo '</div>';
						echo $after_widget;
					}

					$content = ob_get_clean();

					echo $content;

					$this->cache_widget( $args, $content );
				}
		
		}
		
		register_widget('wpl_galaxy_wp_woo_recent_reviews_widget');
	
	}
	
}