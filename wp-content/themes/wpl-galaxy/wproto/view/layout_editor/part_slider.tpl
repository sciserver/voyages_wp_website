
<h2><?php _e('Slider section', 'wproto'); ?></h2>

<table class="form-table wproto-form-table">
	<tr>
		<th><label for="wproto_section_data-slider_id"><?php _e( 'Choose slideshow', 'wproto' ); ?>:</label></th>
		<td>
		
			<?php
			
				$slider = isset( $data['wproto_section_data']['slider_id'] ) ? $data['wproto_section_data']['slider_id'] : '';
			
				global $wpl_galaxy_wp;
				$slideshows = $wpl_galaxy_wp->model->slider->get_layerslider_slideshows();
			?>
		
			<select class="select" id="wproto_section_data-slider_id" name="wproto_section_data[slider_id]">
				<?php if( gettype( $slideshows ) == 'array' && count( $slideshows ) > 0 ): ?>
					<?php foreach( $slideshows as $ls_item ): ?>
						<option <?php echo $slider == $ls_item->id ? 'selected="selected"' : ''; ?> value="<?php echo $ls_item->id; ?>"><?php echo $ls_item->name; ?></option>
					<?php endforeach; ?>
				<?php endif; ?>
			</select>
		
		</td>
	</tr>
	<tr>
		<th><?php _e( 'Display call to action block below slider', 'wproto' ); ?></th>
		<td>
		
			<?php
				$display_call_to_action = isset( $data['wproto_section_data']['display_call_to_action'] ) ? $data['wproto_section_data']['display_call_to_action'] : 'no';
			?>
		
			<div class="field switch">
				<label class="cb-enable <?php echo $display_call_to_action == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
				<label class="cb-disable <?php echo $display_call_to_action == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
				<input data-toggle-element="tr.wproto-slider-below-block" name="wproto_section_data[display_call_to_action]" type="hidden" value="<?php echo $display_call_to_action; ?>" />
				<div class="clear"></div>
			</div>
		
		</td>
	</tr>
	<tr class="wproto-slider-below-block" style="<?php echo $display_call_to_action != 'yes' ? 'display: none' : ''; ?>">
		<th><label for="wproto-section-editor-after-text"><?php _e( 'Call to action text', 'wproto' ); ?>:</label></th>
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
	<tr class="wproto-slider-below-block" style="<?php echo $display_call_to_action != 'yes' ? 'display: none' : ''; ?>">
		<th><label for="wproto_section_data-button-title"><?php _e( 'Button text', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_data-button-title" name="wproto_section_data[button_text]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_data']['button_text'] ) ? $data['wproto_section_data']['button_text'] : __('Take a tour', 'wproto'); ?>" />
		
		</td>
	</tr>
	<tr class="wproto-slider-below-block" style="<?php echo $display_call_to_action != 'yes' ? 'display: none' : ''; ?>">
		<th><label for="wproto_section_data-button_link"><?php _e( 'Button link', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_data-button_link" name="wproto_section_data[button_link]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_data']['button_link'] ) ? $data['wproto_section_data']['button_link'] : ''; ?>" />
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto_section_data-menu_title"><?php _e( 'Menu title (fot one-page template)', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_data-menu_title" name="wproto_section_data[menu_title]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_data']['menu_title'] ) ? $data['wproto_section_data']['menu_title'] : ''; ?>" />
		
		</td>
	</tr>
</table>