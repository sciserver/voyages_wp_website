<?php
	global $wproto_section, $wpl_galaxy_wp;
	$section_data = isset( $wproto_section->data ) ? unserialize( $wproto_section->data ) : array();
	
?>
<!--

	TEXT SECTION
						
-->
<section id="section-id-<?php echo $wproto_section->ID; ?>" class="text wrapper">

	<?php if( $wproto_section->title <> '' ): ?>
	<header class="unit hgroup whole">
		<h2><?php echo $wproto_section->title; ?></h2>
		<?php if( $wproto_section->subtitle <> '' ): ?>
		<h5><?php echo $wproto_section->subtitle; ?></h5>
		<?php endif; ?>
	</header>
	<?php endif; ?>

	<?php if( $wproto_section->before_text <> '' ): ?>
	<div class="grid">
		<?php echo apply_filters( 'the_content', stripslashes( str_replace( "'", "&#39;", $wproto_section->before_text ) ) ); ?>
	</div>
	<?php endif; ?>	

</section>