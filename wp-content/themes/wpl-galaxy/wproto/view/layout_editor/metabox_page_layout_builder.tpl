
<!--
	ADD NEW SECTION BLOCK
-->
<div style="clear: both" id="wproto-lb-add-new-section" class="wproto_section">

	<a href="javascript:;" data-pointer-title="<?php _e('Add section', 'wproto'); ?>" data-pointer-content="<?php _e('Click here to add new content section', 'wproto'); ?>" class="icon show-tooltip-left"><i class="fa fa-plus"></i></a>
		
	<div class="add-section-menu">
		<a href="javascript:;"><?php _e('Add section', 'wproto'); ?> <i class="fa fa-chevron-down"></i></a>
		<ul class="wproto-add-section-links">
			<li><a data-section="benefits" href="javascript:;"><i class="fa fa-trophy"></i><?php _e('Benefits', 'wproto'); ?></a></li>
			<?php if( post_type_exists('wproto_catalog') ): ?>
			<li><a data-section="catalog" href="javascript:;"><i class="fa fa-shopping-cart"></i><?php _e('Catalog', 'wproto'); ?></a></li>
			<?php endif; ?>
			<?php if( post_type_exists('wproto_portfolio') ): ?>
			<li><a data-section="portfolio" href="javascript:;"><i class="fa fa-briefcase"></i><?php _e('Portfolio', 'wproto'); ?></a></li>
			<?php endif; ?>
			<li><a data-section="hexagon_carousel" href="javascript:;"><i class="fa fa-indent"></i><?php _e('Hexagon portfolio', 'wproto'); ?></a></li>
			<li><a data-section="text" href="javascript:;"><i class="fa fa-pencil"></i><?php _e('Text block', 'wproto'); ?></a></li>
			<li><a data-section="testimonials" href="javascript:;"><i class="fa fa-comment"></i><?php _e('Testimonials', 'wproto'); ?></a></li>
			<?php if( wpl_galaxy_wp_utils::isset_layerslider() ): ?>
			<li><a data-section="slider" href="javascript:;"><i class="fa fa-caret-square-o-right"></i><?php _e('Slider', 'wproto'); ?></a></li>
			<?php endif; ?>
			<?php if( wpl_galaxy_wp_utils::isset_woocommerce() ): ?>
			<li><a data-section="product" href="javascript:;"><i class="fa fa-shopping-cart"></i><?php _e('WooCommerce Products', 'wproto'); ?></a></li>
			<?php endif; ?>
			<li><a data-section="posts" href="javascript:;"><i class="fa fa-edit"></i><?php _e('Blog Posts Carousel', 'wproto'); ?></a></li>
			<li><a data-section="posts_video" href="javascript:;"><i class="fa fa-video-camera"></i><?php _e('Video Posts Carousel', 'wproto'); ?></a></li>
			<li><a data-section="posts_photoalbum" href="javascript:;"><i class="fa fa-camera"></i><?php _e('Photoalbums Posts Carousel', 'wproto'); ?></a></li>
			<li><a data-section="subscribe_form" href="javascript:;"><i class="fa fa-envelope"></i><?php _e('Subscribe form', 'wproto'); ?></a></li>
			<li><a data-section="parallax" href="javascript:;"><i class="fa fa-picture-o"></i><?php _e('Parallax', 'wproto'); ?></a></li>
			<li><a data-section="pricing_tables" href="javascript:;"><i class="fa fa-usd"></i><?php _e('Pricing table', 'wproto'); ?></a></li>
			<li><a data-section="contact" href="javascript:;"><i class="fa fa-map-marker"></i><?php _e('Contact &amp; Map', 'wproto'); ?></a></li>
		</ul>
	</div>

</div>

<div class="sections">

	<input type="hidden" name="wproto_settings[page_sections][]" value="1" />

	<?php if( isset( $data['wproto_custom_sections'] ) && is_array( $data['wproto_custom_sections'] ) && count( $data['wproto_custom_sections'] ) > 0 ): ?>
	
		<?php foreach( $data['wproto_custom_sections'] as $section ): ?>
		
		<?php
			
			if( post_type_exists('wproto_catalog') == false && $section->type == 'catalog' ) continue;
			if( post_type_exists('wproto_portfolio') == false && $section->type == 'portfolio' ) continue;
			
			if( wpl_galaxy_wp_utils::isset_woocommerce() == false && $section->type == 'product' ) continue;
			if( wpl_galaxy_wp_utils::isset_layerslider() == false && $section->type == 'slider' ) continue;
			
				include 'section.tpl';
		
			endforeach; ?>
	
	<?php endif; ?>
	
</div> 
