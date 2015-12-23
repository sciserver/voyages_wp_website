<select name="page_template">
	<option value=""><?php _e('Filter by page template', 'wproto'); ?>...</option>
	<?php if( is_array( $data['templates'] ) && count( $data['templates'] ) > 0 ): ?>
	
		<?php foreach( $data['templates'] as $k=>$v ): ?>
		<option <?php echo isset( $_GET['page_template'] ) && $_GET['page_template'] == $v ? 'selected="selected"' : ''; ?> value="<?php echo $v; ?>"><?php echo $k; ?></option>
		<?php endforeach; ?>
	
	<?php endif; ?>
</select>

<select name="page_redirect">
	<option value=""><?php _e( 'Redirect filter', 'wproto'); ?>...</option>
	<option <?php echo isset( $_GET['page_redirect'] ) && $_GET['page_redirect'] == 'yes' ? 'selected="selected"' : ''; ?> value="yes"><?php _e( 'Pages with redirect', 'wproto'); ?></option>
</select>