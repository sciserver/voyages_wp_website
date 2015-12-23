<p>
	<div class="field switch">
		<label class="cb-enable <?php echo $data['featured'] == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
		<label class="cb-disable <?php echo $data['featured'] == 'no' || $data['featured'] == '' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
		<input id="wproto-rss-enabled-input" name="featured" type="hidden" value="<?php echo $data['featured']; ?>" />
		<div class="clear"></div>
	</div>
</p>
