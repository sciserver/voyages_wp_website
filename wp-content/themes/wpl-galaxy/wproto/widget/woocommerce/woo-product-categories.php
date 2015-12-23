<?php
$override_widget = WP_PLUGIN_DIR . '/woocommerce/includes/widgets/class-wc-widget-product-categories.php';

if( class_exists( 'woocommerce' ) && file_exists( $override_widget ) ) {
	
	require_once( $override_widget );
	
	if( class_exists('WC_Widget_Product_Categories') ) {

		class wpl_galaxy_wp_woo_product_categories_widget extends WC_Widget_Product_Categories {

			public function widget( $args, $instance ) {
				extract( $args );

				$title = apply_filters( 'widget_title', $instance['title'], $instance, $this->id_base );
				$c     = ( isset( $instance['count'] ) && $instance['count'] ) ? '1' : '0';
				$h     = $instance['hierarchical'] ? true : false;
				$s     = ( isset( $instance['show_children_only'] ) && $instance['show_children_only'] ) ? '1' : '0';
				$d     = ( isset( $instance['dropdown'] ) && $instance['dropdown'] ) ? '1' : '0';
				$o     = $instance['orderby'] ? $instance['orderby'] : 'order';

				echo $before_widget;

				if ( $title )
					echo $before_title . $title . $after_title;

				$cat_args = array( 'show_count' => $c, 'hierarchical' => $h, 'taxonomy' => 'product_cat' );

				$cat_args['menu_order'] = false;

				if ( $o == 'order' ) {

					$cat_args['menu_order'] = 'asc';

				} else {

					$cat_args['orderby'] = 'title';

				}

				if ( $d ) {

					// Stuck with this until a fix for http://core.trac.wordpress.org/ticket/13258
					wc_product_dropdown_categories( array(
						'show_counts'        => $c,
						'hierarchical'       => $h,
						'show_uncategorized' => 0,
						'orderby'            => $o
					) );
					?>
					<script type='text/javascript'>
					/* <![CDATA[ */
						var product_cat_dropdown = document.getElementById("dropdown_product_cat");
						function onProductCatChange() {
							if ( product_cat_dropdown.options[product_cat_dropdown.selectedIndex].value !=='' ) {
								location.href = "<?php echo home_url(); ?>/?product_cat="+product_cat_dropdown.options[product_cat_dropdown.selectedIndex].value;
							}
						}
						product_cat_dropdown.onchange = onProductCatChange;
					/* ]]> */
					</script>
					<?php

				} else {

					global $wp_query, $post, $woocommerce;

					$this->current_cat = false;
					$this->cat_ancestors = array();

					if ( is_tax('product_cat') ) {

						$this->current_cat = $wp_query->queried_object;
						$this->cat_ancestors = get_ancestors( $this->current_cat->term_id, 'product_cat' );

					} elseif ( is_singular('product') ) {

						$product_category = wc_get_product_terms( $post->ID, 'product_cat', array( 'orderby' => 'parent' ) );

						if ( $product_category ) {
							$this->current_cat   = end( $product_category );
							$this->cat_ancestors = get_ancestors( $this->current_cat->term_id, 'product_cat' );
						}

					}

					include_once( WC()->plugin_path() . '/includes/walkers/class-product-cat-list-walker.php' );

					$cat_args['walker'] 				= new wpl_galaxy_wp_category_walker;
					$cat_args['title_li'] 			= '';
					$cat_args['show_children_only']	= ( isset( $instance['show_children_only'] ) && $instance['show_children_only'] ) ? 1 : 0;
					$cat_args['pad_counts'] 		= 1;
					$cat_args['show_option_none'] 	= __('No product categories exist.', 'woocommerce' );
					$cat_args['current_category']	= ( $this->current_cat ) ? $this->current_cat->term_id : '';
					$cat_args['current_category_ancestors']	= $this->cat_ancestors;

					echo '<ul class="list">';

					wp_list_categories( apply_filters( 'woocommerce_product_categories_widget_args', $cat_args ) );

					echo '</ul>';
				}

				echo $after_widget;

			}
		
		}
		
		register_widget('wpl_galaxy_wp_woo_product_categories_widget');
	
	}
	
}