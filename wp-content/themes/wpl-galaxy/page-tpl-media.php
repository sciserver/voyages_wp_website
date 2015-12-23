<?php
	/**
	 * Template name: 4. Full screen Media (Portfolio / Photos)
	 **/
	global $wpl_galaxy_wp;
	get_header();
	$page_settings = $wpl_galaxy_wp->model->post->get_post_custom( get_the_ID() );
	
	$images_post = isset( $page_settings->wproto_media_tpl_post_id ) ? $page_settings->wproto_media_tpl_post_id : 0;
	
	$attached_images = array();
	
	if( $images_post > 0 ) {
		$attached_images = get_post_meta( $images_post, 'wproto_attached_images', true );
	}
	
	$images_count = count( (array)$attached_images );
	
	$display_images_data = isset( $page_settings->display_images_data ) ? $page_settings->display_images_data : 'no';
	$display_call_to_action = isset( $page_settings->display_call_to_action ) ? $page_settings->display_call_to_action : 'no';
	$call_to_action_text = isset( $page_settings->call_to_action_text ) ? $page_settings->call_to_action_text : '';
	
	$call_to_action_button_title = isset( $page_settings->call_to_action_button_text ) ? $page_settings->call_to_action_button_text : '';
	$call_to_action_button_link = isset( $page_settings->call_to_action_button_link ) ? $page_settings->call_to_action_button_link : '';
	
?>
<div id="content">
			
	<section class="portfolio-full-slider">
		
		<div class="full-portfolio-slider preload">
		<!-- FULL IMAGES -->
		<?php if( $images_count > 0 ): ?>
		
			<?php foreach( $attached_images as $id ): ?>
			
				<?php
					$thumb = wp_get_attachment_image_src( $id, 'full' );
					$image = get_post( $id );
				?>
				<div class="item">
					<img class="lazy" data-src="<?php echo $thumb[0]; ?>" alt="" />
					<div class="text">
						<?php if( $display_images_data == 'yes' ): ?>
						<h4><?php echo $image->post_title; ?></h4>
						<div class="date"><?php echo get_the_time( $wpl_galaxy_wp->settings['date_format'], $id); ?></div>
						<?php endif; ?>
					</div>
				</div>
			
			<?php endforeach; ?>
		
		<?php endif; ?>
		</div>
			
		<a href="javascript:;" class="toggle-panel"></a>
		<div class="portfolio-thumbnails">
			
			<div id="portfolio-pager" class="jThumbnailScroller">
				
				<a href="javascript:;" class="jTscrollerPrevButton"></a>
				<a href="javascript:;" class="jTscrollerNextButton"></a>
				
				<div class="swiper-container jTscrollerContainer">
					
					<div class="swiper-wrapper jTscroller">
					<!-- thumb scroller -->
					<?php $i=0; foreach( $attached_images as $id ): ?>
					
					<?php
						$thumb_name = wpl_galaxy_wp_utils::is_retina() ? 'portfolio-scroll-thumb-2x' : 'portfolio-scroll-thumb';
						$thumb = wp_get_attachment_image_src( $id, $thumb_name );
					?>
					
					<a data-slide-index="<?php echo $i; ?>" class="swiper-slide" href="javascript:;"><img src="<?php echo $thumb[0]; ?>" width="170" height="108" alt="" /></a>
					<?php $i++; endforeach; ?>
					</div>
				</div>
			</div>
			
		</div>
				
	</section>
	<?php if( $display_call_to_action == 'yes' ): ?>
	<div class="take-tour">
			
		<div class="wrapper">
			
			<?php if( $call_to_action_button_title <> '' ): ?>
			<a href="<?php echo $call_to_action_button_link; ?>" class="button pull-right"><?php echo $call_to_action_button_title; ?></a>
			<?php endif; ?>
			<?php echo $call_to_action_text; ?>
				
		</div>
			
	</div>
	<?php endif; ?>
</div>
<?php
	get_footer();