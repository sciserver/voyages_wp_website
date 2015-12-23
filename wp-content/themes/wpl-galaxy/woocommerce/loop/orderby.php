<?php
/**
 * Show options for ordering
 *
 * @author 		WooThemes
 * @package 	WooCommerce/Templates
 * @version     2.2.0
 */
	global $woocommerce, $wp_query;
	
?>
			<!--
					
				SHOP CONTROLS
						
			-->
			
			<div class="shop-items-controls">
				<form class="woocommerce-ordering" method="get">
				<?php if ( $wp_query->have_posts() || woocommerce_products_will_display() ): ?>
				<span class="pull-right">
					<a href="javascript:;" class="view-grid <?php echo !isset( $_GET['wproto_view'] ) || $_GET['wproto_view'] == 'grid' ? 'current' : ''; ?> change-shop-view"></a>
					<a href="javascript:;" class="view-list <?php echo isset( $_GET['wproto_view'] ) && $_GET['wproto_view'] == 'list' ? 'current' : ''; ?> change-shop-view"></a>
					<input type="hidden" name="wproto_view" value="<?php echo isset( $_GET['wproto_view'] ) && in_array( $_GET['wproto_view'], array('grid', 'list') ) ? $_GET['wproto_view'] : 'grid'; ?>" />
				</span>
				
				
				<span class="sort">
					<label><?php _e('Sort by', 'wproto'); ?>:</label> 
					<select id="sort-by" name="orderby">
					<?php
						$catalog_orderby = apply_filters( 'woocommerce_catalog_orderby', array(
							'menu_order' => __( 'Default', 'wproto' ),
							'popularity' => __( 'Popularity', 'wproto' ),
							'rating'     => __( 'Rating', 'wproto' ),
							'date'       => __( 'Newness', 'wproto' ),
							'price'      => __( 'Price: low to high', 'wproto' ),
							'price-desc' => __( 'Price: high to low', 'wproto' )
						) );

						if ( get_option( 'woocommerce_enable_review_rating' ) == 'no' )
							unset( $catalog_orderby['rating'] );

						foreach ( $catalog_orderby as $id => $name )
							echo '<option value="' . esc_attr( $id ) . '" ' . selected( $orderby, $id, false ) . '>' . esc_attr( $name ) . '</option>';
					?>
					</select>
				</span>
				
				<?php
					// Keep query string vars intact
					foreach ( $_GET as $key => $val ) {
						if ( 'orderby' == $key )
							continue;
			
						if (is_array($val)) {
							foreach($val as $innerVal) {
								echo '<input type="hidden" name="' . esc_attr( $key ) . '[]" value="' . esc_attr( $innerVal ) . '" />';
							}
			
						} else {
							echo '<input type="hidden" name="' . esc_attr( $key ) . '" value="' . esc_attr( $val ) . '" />';
						}
					}
				?>
				
				<?php endif; ?>
				
				</form>
			</div>