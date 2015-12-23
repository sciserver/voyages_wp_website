
<h2><?php _e('Pricing tables section', 'wproto'); ?></h2>

<table class="form-table wproto-form-table">
	<tr>
		<th><label for="wproto-section-editor-before-text"><?php _e( 'Text before table (optional)', 'wproto' ); ?>:</label></th>
		<td>
		
		<?php
			$content = isset( $data['wproto_section_content']['before_text'] ) ? $data['wproto_section_content']['before_text'] : '';
			wp_editor(
				stripslashes( str_replace( '\'', "&#39;", $content ) ),
				'wproto-section-editor-before-text',
				array(
					'media_buttons' => false,
					'textarea_name' => 'wproto_section_content[before_text]',
					'textarea_rows' => 8,
					'teeny' => true,
					'quicktags' => true,
					'tinymce' => array(
						'theme_advanced_buttons2' => '',
						'theme_advanced_buttons3' => '',
						'theme_advanced_buttons4' => ''
					)	
				)
			);
		?>
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto_section_data-table_id"><?php _e( 'Select table to display', 'wproto' ); ?>:</label></th>
		<td>
		
			<?php
			
				$table = isset( $data['wproto_section_data']['table_id'] ) ? $data['wproto_section_data']['table_id'] : '';
			
				global $wpl_galaxy_wp;
				$pricing_tables = $wpl_galaxy_wp->model->post->get_all_pricing_tables();
			?>
		
			<select class="select" id="wproto_section_data-table_id" name="wproto_section_data[table_id]">
				<?php if( $pricing_tables->have_posts() ): while ( $pricing_tables->have_posts() ) : $pricing_tables->the_post(); ?>
				<option <?php echo $table == get_the_ID() ? 'selected="selected"' : ''; ?> value="<?php the_ID(); ?>"><?php the_title(); ?></option>
				<?php endwhile; endif; ?>
			</select>
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto-section-editor-after-text"><?php _e( 'Text after table (optional)', 'wproto' ); ?>:</label></th>
		<td>
		
		<?php
			$content = isset( $data['wproto_section_content']['after_text'] ) ? $data['wproto_section_content']['after_text'] : '';
			wp_editor(
				stripslashes( str_replace( '\'', "&#39;", $content ) ),
				'wproto-section-editor-after-text',
				array(
					'media_buttons' => false,
					'textarea_name' => 'wproto_section_content[after_text]',
					'textarea_rows' => 8,
					'teeny' => true,
					'quicktags' => true,
					'tinymce' => array(
						'theme_advanced_buttons2' => '',
						'theme_advanced_buttons3' => '',
						'theme_advanced_buttons4' => ''
					)	
				)
			);
		?>
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto_section_data-menu_title"><?php _e( 'Menu title (fot one-page template)', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_data-menu_title" name="wproto_section_data[menu_title]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_data']['menu_title'] ) ? $data['wproto_section_data']['menu_title'] : ''; ?>" />
		
		</td>
	</tr>
</table>