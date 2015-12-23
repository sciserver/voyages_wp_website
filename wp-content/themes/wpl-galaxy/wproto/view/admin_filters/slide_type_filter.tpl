<select name="slide_type">
	<option value=""><?php _e( 'Slide Type', 'wproto'); ?></option>
	<option <?php echo @$_GET['slide_type'] == 'image' ? 'selected="selected"' : ''; ?> value="image"><?php _e( 'Image', 'wproto'); ?></option>
	<option <?php echo @$_GET['slide_type'] == 'video' ? 'selected="selected"' : ''; ?> value="video"><?php _e( 'Video', 'wproto'); ?></option>
</select>