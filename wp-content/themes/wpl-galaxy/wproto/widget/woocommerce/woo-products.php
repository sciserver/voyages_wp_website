<?php

$override_widget = WP_PLUGIN_DIR . '/woocommerce/includes/widgets/class-wc-widget-products.php';

if( class_exists( 'woocommerce' ) && file_exists( $override_widget ) ) {
	
	require_once( $override_widget );
	
	if( class_exists('WC_Widget_Products') ) {

		class wpl_galaxy_wp_woo_products_widget extends WC_Widget_Products {

			public function widget( $args, $instance ) {

				if ( $this->get_cached_widget( $args ) )
					return;

				ob_start();
				extract( $args );

				$title       = apply_filters( 'widget_title', $instance['title'], $instance, $this->id_base );
				$number      = absint( $instance['number'] );
				$show        = sanitize_title( $instance['show'] );
				$orderby     = sanitize_title( $instance['orderby'] );
				$order       = sanitize_title( $instance['order'] );
				$show_rating = false;

				$query_args = array(
					'posts_per_page' => $number,
 					'post_status' 	 => 'publish',
  				'post_type' 	 => 'product',
  				'no_found_rows'  => 1,
  				'order'          => $order == 'asc' ? 'asc' : 'desc'
   			);

				$query_args['meta_query'] = array();

				if ( empty( $instance['show_hidden'] ) ) {
					$query_args['meta_query'][] = WC()->query->visibility_meta_query();
					$query_args['post_parent']  = 0;
				}

				if ( ! empty( $instance['hide_free'] ) ) {
    			$query_args['meta_query'][] = array(
			    	'key'     => '_price',
			    	'value'   => 0,
			    	'compare' => '>',
			    	'type'    => 'DECIMAL',
					);
    		}

	    	$query_args['meta_query'][] = WC()->query->stock_status_meta_query();
	    	$query_args['meta_query']   = array_filter( $query_args['meta_query'] );

    		switch ( $show ) {
    			case 'featured' :
    				$query_args['meta_query'][] = array(
							'key'   => '_featured',
							'value' => 'yes'
						);
  				break;
    			case 'onsale' :
	    			$product_ids_on_sale = wc_get_product_ids_on_sale();
						$product_ids_on_sale[] = 0;
						$query_args['post__in'] = $product_ids_on_sale;
  				break;
    		}

    		switch ( $orderby ) {
					case 'price' :
						$query_args['meta_key'] = '_price';
    				$query_args['orderby']  = 'meta_value_num';
					break;
					case 'rand' :
    				$query_args['orderby']  = 'rand';
					break;
				case 'sales' :
					$query_args['meta_key'] = 'total_sales';
    			$query_args['orderby']  = 'meta_value_num';
				break;
				default :
					$query_args['orderby']  = 'date';
    		}

				$r = new WP_Query( $query_args );

				if ( $r->have_posts() ) {

					echo $before_widget;

					if ( $title )
						echo $before_title . $title . $after_title;

					echo '<div class="items">';
					
					$i=0;
					while ( $r->have_posts()) {
						$r->the_post();
						$i++;
						global $product;

						$thumb_size = wpl_galaxy_wp_utils::is_retina() ? 'photo-small-2x' : 'photo-small';

						?>
						<div class="item">
							<div class="thumbnail">
								<a href="<?php the_permalink(); ?>"><?php echo ( has_post_thumbnail() ? get_the_post_thumbnail( $r->post->ID, $thumb_size ) : woocommerce_placeholder_img( $thumb_size ) ) ?></a>
								<div class="onsale appear-animation" data-appear-animation-delay="0.15" data-appear-animation="bounceIn"><?php echo $i; ?></div>
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

				$this->cache_widget( $args, $content );
			}

		}
		
		register_widget('wpl_galaxy_wp_woo_products_widget');
	
	}
	
}