<p>
	<select name="table_style" style="width: 100%;">
		<option <?php echo $data['table_style'] == 'style_1' ? 'selected="selected"' : ''; ?> value="style_1"><?php _e('Exquisite', 'wproto'); ?></option>
		<option <?php echo $data['table_style'] == 'style_2' ? 'selected="selected"' : ''; ?> value="style_2"><?php _e('Standard', 'wproto'); ?></option>
		<option <?php echo $data['table_style'] == 'style_3' ? 'selected="selected"' : ''; ?> value="style_3"><?php _e('Colored', 'wproto'); ?></option>
	</select>
</p>