<?php

$override_widget = WP_PLUGIN_DIR . '/woocommerce/includes/widgets/class-wc-widget-top-rated-products.php';

if( class_exists( 'woocommerce' ) && file_exists( $override_widget ) ) {
	
	require_once( $override_widget );
	
	if( class_exists('WC_Widget_Top_Rated_Products') ) {

		class wpl_galaxy_wp_woo_top_rated_products_widget extends WC_Widget_Top_Rated_Products {

			public function widget($args, $instance) {

				if ( $this->get_cached_widget( $args ) )
					return;

				ob_start();
				extract( $args );

				$title  = apply_filters( 'widget_title', $instance['title'], $instance, $this->id_base );
				$number = absint( $instance['number'] );

				add_filter( 'posts_clauses',  array( WC()->query, 'order_by_rating_post_clauses' ) );

				$query_args = array('posts_per_page' => $number, 'no_found_rows' => 1, 'post_status' => 'publish', 'post_type' => 'product' );

				$query_args['meta_query'] = WC()->query->get_meta_query();

				$r = new WP_Query( $query_args );

				if ( $r->have_posts() ) {

					echo $before_widget;

					if ( $title )
						echo $before_title . $title . $after_title;

						?>
						<div class="items">
							<?php while ($r->have_posts()) : $r->the_post(); global $product;
							$thumb_size = wpl_galaxy_wp_utils::is_retina() ? 'photo-small-2x' : 'photo-small';
						?>
							<div class="item">
								<div class="thumbnail">
									<a href="<?php the_permalink(); ?>"><?php echo ( has_post_thumbnail() ? get_the_post_thumbnail( $r->post->ID, $thumb_size ) : woocommerce_placeholder_img( $thumb_size ) ) ?></a>
									<div class="featured appear-animation" data-appear-animation-delay="0.15" data-appear-animation="bounceIn"><i class="fa fa-thumbs-up"></i></div>
								</div>
						
								<div class="description">
						
									<a href="<?php the_permalink(); ?>" class="title"><?php the_title(); ?></a>
									<a href="<?php the_permalink(); ?>" class="price"><?php echo $product->get_price_html(); ?></a>
						
								</div>
							</div>
							<?php endwhile; ?>
						</div>
						<?php

					echo $after_widget;
				}

				remove_filter( 'posts_clauses', array( WC()->query, 'order_by_rating_post_clauses' ) );

				wp_reset_postdata();

				$content = ob_get_clean();

				echo $content;

				$this->cache_widget( $args, $content );
			}
		
		}
		
		register_widget('wpl_galaxy_wp_woo_top_rated_products_widget');
	
	}
	
}