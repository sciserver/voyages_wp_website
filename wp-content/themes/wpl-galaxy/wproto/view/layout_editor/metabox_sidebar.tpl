<?php global $wpl_galaxy_wp; ?>
<div class="wproto-metabox-layout-editor">

	<?php
		// get values		
		$page_sidebar = isset( $data['wproto_page_sidebar'] ) ? $data['wproto_page_sidebar'] : 'right';
		$page_sidebar_id = isset( $data['wproto_page_sidebar_id'] ) ? $data['wproto_page_sidebar_id'] : 'sidebar-right';

		$widgetized_footer = isset( $data['wproto_widgetized_footer'] ) ? $data['wproto_widgetized_footer'] : 'yes';
		
		$page_footer_sidebar_id = isset( $data['wproto_page_footer_sidebar_id'] ) ? $data['wproto_page_footer_sidebar_id'] : 'sidebar-footer';
	?>

	<ul class="wproto-layout-type wproto-sidebars-layouts">
		<li data-sidebar="left" class="ib <?php echo $page_sidebar == 'left' ? 'selected' : ''; ?>"><a href="javascript:;" class="layout-sidebar-link layout-sidebar-left"></a><a href="javascript:;"><?php _e( 'With Left Sidebar', 'wproto' ); ?></a></li>
		<li data-sidebar="right" class="ib <?php echo $page_sidebar == 'right' ? 'selected' : ''; ?>"><a href="javascript:;" class="layout-sidebar-link layout-sidebar-right"></a><a href="javascript:;"><?php _e( 'With Right Sidebar', 'wproto' ); ?></a></li>
		<li data-sidebar="none" class="ib <?php echo $page_sidebar == 'none' || $page_sidebar == NULL ? 'selected' : ''; ?>"><a href="javascript:;" class="layout-sidebar-link layout-no-sidebar"></a><a href="javascript:;"><?php _e( 'No Sidebar', 'wproto' ); ?></a></a></li>
	</ul>
	
	<input type="hidden" id="wproto-layout-type-input" class="wproto-hidden" name="wproto_settings[wproto_page_sidebar]" value="<?php echo $page_sidebar == NULL ? 'none' : $page_sidebar; ?>" />
	
	<div class="clear"></div>
	
	<div class="wproto-metabox-inside-bg wproto-layout-type-settings-inside">
	
		<div class="wproto-layout-type-hide-if-no-sidebar <?php if( $page_sidebar == 'none' || $page_sidebar == NULL ): ?>hidden<?php endif; ?>">
		<h4><a href="javascript:;" class="inline-link wproto-toggle-form-block"><?php _e( 'Page sidebar', 'wproto' ); ?></a> <i class="icon-angle-right"></i></h4>
		
		<table class="form-table wproto-form-table" style="display: none;">
			<tbody>
				<tr>
					<th><p><?php _e( 'Choose a widget area which will be displayed at sidebar', 'wproto' ); ?>:</p></th>
					<td>
						<select class="select" name="wproto_settings[wproto_page_sidebar_id]">
							<option value="">&mdash;</option>
							<?php if( is_array( $data['registered_sidebars'] ) && count( $data['registered_sidebars'] ) > 0 ): ?>
				
								<?php foreach( $data['registered_sidebars'] as $sidebar ): ?>
								<option <?php echo $page_sidebar_id == $sidebar['id'] ? 'selected="selected"' : ''; ?> value="<?php echo $sidebar['id']; ?>"><?php echo $sidebar['name']; ?></option>
								<?php endforeach; ?>
				
							<?php endif; ?>
						</select>
					</td>
				</tr>
			</tbody>
		</table>
		</div>
		
		<h4><a href="javascript:;" class="inline-link wproto-toggle-form-block"><?php _e( 'Widgetized Footer', 'wproto' ); ?></a> <i class="icon-angle-right"></i></h4>
		
		<table class="form-table wproto-form-table" style="display: none;">
			<tbody>
				<tr>
					<th style="vertical-align: middle"><p><?php _e( 'Show widgetized footer', 'wproto' ); ?>:</p></th>
					<td>
					
						<div class="field switch">		
							<label class="cb-enable <?php echo $widgetized_footer == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $widgetized_footer == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input type="hidden" data-toggle-element="tr.wproto-widgetized-footer-tr" name="wproto_settings[wproto_widgetized_footer]" class="checkbox wproto_widgetized_footer_input" value="<?php echo $widgetized_footer; ?>" />
							<div class="clear"></div>
						</div>
					
					</td>
				</tr>
				<tr class="wproto-widgetized-footer-tr" style="<?php echo $widgetized_footer == 'no' ? 'display: none;' : ''; ?>">
					<th><p><?php _e( 'Choose a widget area which will be displayed at footer', 'wproto' ); ?>:</p></th>
					<td>
						<select class="select" name="wproto_settings[wproto_page_footer_sidebar_id]">
							<option value="">&mdash;</option>
							<?php if( is_array( $data['registered_sidebars'] ) && count( $data['registered_sidebars'] ) > 0 ): ?>
				
								<?php foreach( $data['registered_sidebars'] as $sidebar ): ?>
								<option <?php echo $page_footer_sidebar_id == $sidebar['id'] ? 'selected="selected"' : ''; ?> value="<?php echo $sidebar['id']; ?>"><?php echo $sidebar['name']; ?></option>
								<?php endforeach; ?>
				
							<?php endif; ?>
						</select>
					</td>
				</tr>
			</tbody>
		</table>
	
	</div>
	
</div>
