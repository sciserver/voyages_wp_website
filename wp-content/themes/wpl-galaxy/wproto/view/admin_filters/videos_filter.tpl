<?php if( $data['typenow'] == 'wproto_video' ): ?>
<select name="video_type">
	<option value=""><?php _e( 'Video type', 'wproto'); ?></option>
	<option <?php echo @$_GET['video_type'] == 'youtube' ? 'selected="selected"' : ''; ?> value="youtube"><?php _e( 'YouTube', 'wproto'); ?></option>
	<option <?php echo @$_GET['video_type'] == 'vimeo' ? 'selected="selected"' : ''; ?> value="vimeo"><?php _e( 'Vimeo', 'wproto'); ?></option>
</select>
<?php endif; ?>