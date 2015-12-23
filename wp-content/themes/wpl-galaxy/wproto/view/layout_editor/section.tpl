<?php
$icon = '';
$title = '';
			
switch( $section->type ) {
	case 'benefits':
		$icon = 'fa-trophy';
		$title = __('Benefits', 'wproto');
	break;
	case 'catalog':
		$icon = 'fa-shopping-cart';
		$title = __('Catalog', 'wproto');
	break;
	case 'portfolio':
		$icon = 'fa-briefcase';
		$title = __('Portfolio', 'wproto');				
	break;
	case 'text':
		$icon = 'fa-pencil';
		$title = __('Text block', 'wproto');					
	break;
	case 'slider':
		$icon = 'fa-caret-square-o-right';
		$title = __('Slider', 'wproto');	
	break;
	case 'testimonials':
		$icon = 'fa-comment';
		$title = __('Testimonials', 'wproto');	
	break;
	case 'product':
		$icon = 'fa-shopping-cart';
		$title = __('Products', 'wproto');
	break;
	case 'posts':
		$icon = 'fa-edit';
		$title = __('Posts Carousel', 'wproto');
	break;
	case 'posts_video':
		$icon = 'fa-video-camera';
		$title = __('Video Posts Carousel', 'wproto');
	break;
	case 'posts_photoalbum':
		$icon = 'fa-camera';
		$title = __('Photoalbums Posts Carousel', 'wproto');
	break;
	case 'subscribe_form':
		$icon = 'fa-envelope';
		$title = __('Subscribe form', 'wproto');
	break;
	case 'parallax':
		$icon = 'fa-picture-o';
		$title = __('Parallax', 'wproto');
	break;
	case 'hexagon_carousel':
		$icon = 'fa-indent';
		$title = __('Hexagon carousel', 'wproto');
	break;
	case 'pricing_tables':
		$icon = 'fa-usd';
		$title = __('Pricing tables', 'wproto');
	break;
	case 'contact':
		$icon = 'fa-map-marker';
		$title = __('Contact &amp; Map', 'wproto');
	break;
}
			
	if( $icon <> '' && $title <> '' ):
			
?>
		
<div data-section-type="<?php echo $section->type; ?>" class="wproto_section">
	
	<a href="javascript:;" data-pointer-title="<?php _e('Delete section', 'wproto'); ?>" data-pointer-content="<?php _e('Click here to remove section', 'wproto'); ?>" class="delete-section"><i class="fa fa-times"></i></a>
	<a href="javascript:;" data-pointer-title="<?php echo $title; ?>" data-pointer-content="<?php _e('Click here to edit section content', 'wproto'); ?>" class="icon edit-section show-tooltip-left"><i class="fa <?php echo $icon; ?>"></i></a>
		
	<div class="add-section-menu">
		<a href="javascript:;" class="edit-section"><?php echo $title; ?></a>
	</div>
		
	<input type="hidden" name="wproto_settings[page_sections][]" value="<?php echo $section->ID; ?>" />
	
</div>
		
<?php
	endif;
?>