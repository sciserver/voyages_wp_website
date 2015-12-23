<?php
	global $wproto_section, $wpl_galaxy_wp;
	$section_data = isset( $wproto_section->data ) ? unserialize( $wproto_section->data ) : array();
	
	$id = isset( $section_data['table_id'] ) ? absint( $section_data['table_id'] ) : 0; 
?>
<!--

	PRICING TABLES
	
-->
<section id="section-id-<?php echo $wproto_section->ID; ?>" class="pricing-tables">
	<div class="wrapper grid">

		<?php if( $wproto_section->before_text <> '' ): ?>
		<div class="unit whole">
			<?php echo apply_filters( 'the_content', $wproto_section->before_text ); ?>
		</div>
		<?php endif; ?>

		<?php echo do_shortcode('[wproto_pricing_tables id="' . $id . '"]'); ?>

		<?php if( $wproto_section->before_text <> '' ): ?>
		<div class="unit whole">
			<?php echo apply_filters( 'the_content', $wproto_section->before_text ); ?>
		</div>
		<?php endif; ?>
	</div>
</section>