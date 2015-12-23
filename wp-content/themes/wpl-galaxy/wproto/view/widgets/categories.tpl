<?php echo $data['args']['before_widget']; ?>

<!-- widget title -->
<?php if ( isset( $data['title'] ) ) : ?>

	<?php echo $data['args']['before_title']; ?>
	
		<?php echo $data['title']; ?>
		
	<?php echo $data['args']['after_title']; ?>
	
<?php endif; ?>

<!-- widget content -->

<ul class="list">
<?php
	wp_list_categories(
		array(
			'walker' => new wpl_galaxy_wp_category_walker,
			'taxonomy' => $data['instance']['tax_name'],
			'title_li' => '',
			'hide_empty' => $data['instance']['do_not_display_empty'],
			'hierarchical' => $data['instance']['style'] == 'tree',
			'show_count' => $data['instance']['show_count'],
			'wproto_new_sticker' => $data['instance']['display_new'],
			'wproto_featured_sticker' => $data['instance']['display_featured'],
			'wproto_display_image' => $data['instance']['display_image'],
			'wproto_display_description' => $data['instance']['display_description'],
			'wproto_display_categories' => $data['instance']['display']
		)
	);
?>
</ul>

<?php echo $data['args']['after_widget'];