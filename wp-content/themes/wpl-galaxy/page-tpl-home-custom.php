<?php
	/**
	 * Template name: 1. Home / Custom
	 **/

	get_header();
	global $wpl_galaxy_wp;
	if( have_posts() ): while ( have_posts() ) : the_post();

	?>
	<!-- 
		CONTENT SECTION
	-->
	<div id="content">
	<?php

		$data = wpl_galaxy_wp_utils::get_post_custom( $post->ID );
		$_sections = isset( $data['page_sections'] ) ? unserialize( $data['page_sections'] ) : array();
		$_sections = $wpl_galaxy_wp->model->sections->get( array_values( $_sections ) );
		
		if( is_array( $_sections ) && count( $_sections ) > 0 ):
		
			foreach( $_sections as $wproto_section ):
			
				get_template_part( 'sections/' . $wproto_section->type );
			
			endforeach;
		
		endif;
		
	?>
	</div> <!-- /content -->
	<?php
	endwhile; endif;
	get_footer();