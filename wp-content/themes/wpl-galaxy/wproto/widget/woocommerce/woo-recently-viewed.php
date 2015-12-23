<?php

$override_widget = WP_PLUGIN_DIR . '/woocommerce/classes/widgets/class-wc-widget-recently-viewed.php';

if( class_exists( 'woocommerce' ) && file_exists( $override_widget ) ) {
	
	require_once( $override_widget );
	
	if( class_exists('WC_Widget_Recently_Viewed') ) {

		class wpl_galaxy_wp_woo_recently_viewed_widget extends WC_Widget_Recently_Viewed {

			function widget($args, $instance) {

				$viewed_products = ! empty( $_COOKIE['woocommerce_recently_viewed'] ) ? (array) explode( '|', $_COOKIE['woocommerce_recently_viewed'] ) : array();
				$viewed_products = array_filter( array_map( 'absint', $viewed_products ) );

				if ( empty( $viewed_products ) )
					return;

				ob_start();
				extract( $args );

				$title  = apply_filters( 'widget_title', $instance['title'], $instance, $this->id_base );
				$number = absint( $instance['number'] );

	    	$query_args = array( 'posts_per_page' => $number, 'no_found_rows' => 1, 'post_status' => 'publish', 'post_type' => 'product', 'post__in' => $viewed_products, 'orderby' => 'rand' );

				$query_args['meta_query'] = array();
	    	$query_args['meta_query'][] = WC()->query->stock_status_meta_query();
	    	$query_args['meta_query'] = array_filter( $query_args['meta_query'] );

				$r = new WP_Query($query_args);

				if ( $r->have_posts() ) {

					echo $before_widget;
	
					if ( $title )
						echo $before_title . $title . $after_title;

						echo '<div class="items">';

						while ( $r->have_posts()) {
							$r->the_post();
							global $product;

							$thumb_size = wpl_galaxy_wp_utils::is_retina() ? 'photo-small-2x' : 'photo-small';

							?>
							<div class="item">
								<div class="thumbnail">
									<a href="<?php the_permalink(); ?>"><?php echo ( has_post_thumbnail() ? get_the_post_thumbnail( $r->post->ID, $thumb_size ) : woocommerce_placeholder_img( $thumb_size ) ) ?></a>
								</div>
						
								<div class="description">
						
									<a href="<?php the_permalink(); ?>" class="title"><?php the_title(); ?></a>
									<a href="<?php the_permalink(); ?>" class="price"><?php echo $product->get_price_html(); ?></a>
						
								</div>
							</div>
							<?php
						}

					echo '</div>';

					echo $after_widget;
				}

				wp_reset_postdata();

				$content = ob_get_clean();

				echo $content;
			}
		
		}
		
		register_widget('wpl_galaxy_wp_woo_recently_viewed_widget');
	
	}
	
}