<?php
	global $wproto_section;
	$section_data = isset( $wproto_section->data ) ? unserialize( $wproto_section->data ) : array();
	$slider_id = isset( $section_data['slider_id'] ) ? $section_data['slider_id'] : 0;
?>
<!--

	SLIDER SECTION
						
-->

<section id="section-id-<?php echo $wproto_section->ID; ?>" class="slider <?php if( !isset( $section_data['display_call_to_action'] ) || $section_data['display_call_to_action'] != 'yes' ): ?>no-call-to-action<?php endif; ?>">
	<?php echo do_shortcode( '[layerslider id="' . $slider_id . '"]' ); ?>
</section>

<?php if( isset( $section_data['display_call_to_action'] ) && $section_data['display_call_to_action'] == 'yes' ): ?>
<section class="take-tour">

	<div class="wrapper">
			
		<div class="grid">
				
			<div class="unit whole">
			
				<?php if( isset( $section_data['button_text'] ) && $section_data['button_text'] <> '' ): ?>
				<a href="<?php echo isset( $section_data['button_link'] ) ?  $section_data['button_link'] : ''; ?>" class="button pull-right"><?php echo $section_data['button_text']; ?></a>
				<?php endif; ?>
				
				<?php echo apply_filters( 'the_content', $wproto_section->after_text ); ?>
						
			</div>
					
		</div>
				
	</div>

</section>
<?php endif; ?>