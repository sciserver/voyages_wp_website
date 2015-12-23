<?php

wp_dropdown_categories(array(
	'show_option_none' 	=> __( "Show all categories", 'wproto'),
	'taxonomy'        	=>  $data['taxonomy'],
	'name'            	=>  'filter_by_category',
	'orderby'         	=>  'name',
	'selected'        	=>  @$_GET['filter_by_category'],
	'hierarchical'    	=>  true,
	'show_count'      	=>  true,
	'hide_empty'      	=>  false,
));