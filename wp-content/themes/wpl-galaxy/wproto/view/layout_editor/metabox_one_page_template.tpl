<?php
	$wproto_onepage_display_external_blog_link = isset( $data['wproto_onepage_display_external_blog_link'] ) ? $data['wproto_onepage_display_external_blog_link'] : 'yes';
	$widgetized_footer = isset( $data['wproto_onepage_widgetized_footer'] ) ? $data['wproto_onepage_widgetized_footer'] : 'no';
	$page_footer_sidebar_id = isset( $data['wproto_onepage_footer_sidebar_id'] ) ? $data['wproto_onepage_footer_sidebar_id'] : 'sidebar-footer';
?>
<table class="form-table wproto-form-table">
	<tr>
		<th><label for="wproto_slider_show"><?php _e( 'Display external blog link at header menu', 'wproto' ); ?>:</label></th>
		<td>

			<div class="field switch">
				<label class="cb-enable <?php echo $wproto_onepage_display_external_blog_link == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
				<label class="cb-disable <?php echo $wproto_onepage_display_external_blog_link == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
				<input data-toggle-element="tr.wproto-slider-options" name="wproto_settings[wproto_onepage_display_external_blog_link]" type="hidden" value="<?php echo $wproto_onepage_display_external_blog_link; ?>" />
				<div class="clear"></div>
			</div>

		</td>
	</tr>
	<tr>
		<th style="vertical-align: middle"><p><?php _e( 'Show widgetized footer', 'wproto' ); ?>:</p></th>
		<td>
					
			<div class="field switch">		
				<label class="cb-enable <?php echo $widgetized_footer == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
				<label class="cb-disable <?php echo $widgetized_footer == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
				<input type="hidden" data-toggle-element="tr.wproto-onepage-widgetized-footer-tr" name="wproto_settings[wproto_onepage_widgetized_footer]" value="<?php echo $widgetized_footer; ?>" />
				<div class="clear"></div>
			</div>
					
		</td>
	</tr>
	<tr class="wproto-onepage-widgetized-footer-tr" style="<?php echo $widgetized_footer == 'no' ? 'display: none;' : ''; ?>">
		<th><p><?php _e( 'Choose a widget area which will be displayed at footer', 'wproto' ); ?>:</p></th>
		<td>
			<select class="select" name="wproto_settings[wproto_onepage_footer_sidebar_id]">
				<option value="">&mdash;</option>
				<?php if( is_array( $data['registered_sidebars'] ) && count( $data['registered_sidebars'] ) > 0 ): ?>
				
					<?php foreach( $data['registered_sidebars'] as $sidebar ): ?>
					<option <?php echo $page_footer_sidebar_id == $sidebar['id'] ? 'selected="selected"' : ''; ?> value="<?php echo $sidebar['id']; ?>"><?php echo $sidebar['name']; ?></option>
					<?php endforeach; ?>
				
				<?php endif; ?>
			</select>
		</td>
	</tr>
</table>