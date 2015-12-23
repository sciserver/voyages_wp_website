<?php

$override_widget = WP_PLUGIN_DIR . '/woocommerce/includes/widgets/class-wc-widget-product-search.php';

if( class_exists( 'woocommerce' ) && file_exists( $override_widget ) ) {
	
	require_once( $override_widget );
	
	if( class_exists('WC_Widget_Product_Search') ) {

		class wpl_galaxy_wp_woo_product_search_widget extends WC_Widget_Product_Search {

			function widget( $args, $instance ) {
				extract( $args );

				$title = $instance['title'];
				$title = apply_filters('widget_title', $title, $instance, $this->id_base);

				echo $before_widget;

				if ($title) echo $before_title . $title . $after_title;

				?>
				
				<form action="<?php echo site_url(); ?>" class="search-form" method="get">
					<input type="text" placeholder="<?php _e('Search request here', 'wproto'); ?>" name="s" value="<?php echo get_query_var('s'); ?>" />
					<input type="hidden" name="post_type" value="product" />
					<a href="javascript:;" class="button"><i class="fa fa-search"></i></a>
				</form>

				
				<?php

				echo $after_widget;

			}
		
		}
		
		register_widget('wpl_galaxy_wp_woo_product_search_widget');
	
	}
	
}