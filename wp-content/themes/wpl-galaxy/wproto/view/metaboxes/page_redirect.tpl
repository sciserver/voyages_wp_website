<?php
	$redirect_enabled = isset( $data['wproto_redirect_enabled'] ) ? $data['wproto_redirect_enabled'] : 'no'; 
	$redirect_code = isset( $data['wproto_redirect_code'] ) ? $data['wproto_redirect_code'] : '';
	$redirect_type = isset( $data['wproto_redirect_type'] ) ? $data['wproto_redirect_type'] : '';
	$redirect_url = isset( $data['wproto_redirect_url'] ) ? $data['wproto_redirect_url'] : '';
	$redirect_page_id= isset( $data['wproto_redirect_page_id'] ) ? $data['wproto_redirect_page_id'] : '';
?>


<div class="field switch">
	<label class="alignleft"><?php _e( sprintf('Redirect this %s', $data['post_type'] ), 'wproto' ); ?>: &nbsp; </label> 
	<label class="cb-enable <?php echo $redirect_enabled == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
	<label class="cb-disable <?php echo $redirect_enabled == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
	<input id="wproto-redirect-enabled-input" data-toggle-element="#wproto-redirect-form" name="wproto_settings[wproto_redirect_enabled]" type="hidden" value="<?php echo $redirect_enabled; ?>" />
	<div class="clear"></div>
</div>
<div id="wproto-redirect-form"<?php echo $redirect_enabled != 'yes' ? ' style="display: none"' : ''; ?>>

	<p>
		<label><?php _e( 'Redirect code', 'wproto' ); ?>
		<select name="wproto_settings[wproto_redirect_code]" style="width: 100%;">
			<option value="301"><?php _e('301 Moved Permanently', 'wproto'); ?></option>
			<option <?php echo $redirect_code == 302 ? 'selected="selected"' : ''; ?> value="302"><?php _e('302 Moved Temporarily', 'wproto'); ?></option>
			<option <?php echo $redirect_code == 307 ? 'selected="selected"' : ''; ?> value="307"><?php _e('307 Temporary Redirect', 'wproto'); ?></option>
		</select>
		</label>
	</p>

	<p class="wproto-redirect-form-type">
		<label><input class="wproto_redirect_type-input" <?php echo $redirect_type == '' || $redirect_type == 'page' ? 'checked="checked"' : ''; ?> type="radio" name="wproto_settings[wproto_redirect_type]" value="page" /> <?php _e( 'To another page', 'wproto' ); ?></label>
	</p>
	<p class="wproto-redirect-form-type">
		<label><input class="wproto_redirect_type-input" <?php echo $redirect_type == 'url' ? 'checked="checked"' : ''; ?> type="radio" name="wproto_settings[wproto_redirect_type]" value="url" /> <?php _e( 'To another URL', 'wproto' ); ?></label>
	</p>
	<p id="wproto-redirect-form-choose-page"<?php echo $redirect_type == '' || $redirect_type == 'page' ? '' : ' style="display: none"'; ?>>
		<label><?php _e( 'Choose a page', 'wproto' ); ?>:
		<?php wp_dropdown_pages('name=wproto_settings[wproto_redirect_page_id]&exclude=' . $data['post_id'] . '&selected=' . $redirect_page_id ); ?></label>
	</p>
	<p id="wproto-redirect-form-choose-url"<?php echo $redirect_type == 'url' ? '' : ' style="display: none"'; ?>>
		<label><?php _e( 'Type URL', 'wproto' ); ?>:
		<input type="text" style="width: 100%" name="wproto_settings[wproto_redirect_url]" value="<?php echo $redirect_url; ?>" /></label>
	</p>
</div>