<?php
	$post_type = get_query_var('post_type');
	
	$tax_name = '';
	
	switch( $post_type ) {
		case 'post':
			$tax_name = 'category';
		break;
		case 'wproto_video':
			$tax_name = 'wproto_video_category';
		break;
		case 'wproto_photoalbums':
			$tax_name = 'wproto_photoalbums_category';
		break;
		case 'wproto_catalog':
			$tax_name = 'wproto_catalog_category';
		break;
		case 'wproto_portfolio':
			$tax_name = 'wproto_portfolio_category';
		break;
	}
	
	if( $tax_name <> '' ):
		$terms = get_terms( $tax_name, array(
 			'orderby'    => 'count',
 			'hide_empty' => 0
 		));
?>
<div class="filters">
						
	<ul class="hexagon-filter-links sorter">
		<li class="current filter" data-post-type="<?php echo $post_type; ?>" data-tax-name="<?php echo $tax_name; ?>" data-filter="0"><?php _e('All', 'wproto'); ?></li>
		<?php if( count( $terms ) > 0 ): ?>
		
			<?php foreach ( $terms as $term ): ?>
				<li class="filter" data-post-type="<?php echo $post_type; ?>" data-tax-name="<?php echo $tax_name; ?>" data-filter="<?php echo $term->term_id; ?>"><?php echo $term->name; ?></li>
			<?php endforeach; ?>
		
		<?php endif; ?>
	</ul>
							
	<div class="clear"></div>

</div>
<?php endif; 