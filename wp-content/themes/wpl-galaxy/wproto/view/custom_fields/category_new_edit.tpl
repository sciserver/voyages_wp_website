<tr class="form-field">
	<th scope="row" valign="top">
		<label><?php _e( 'Display this category as "new"', 'wproto' ); ?>:</label>
	</th>
	<td>
		<select name="term_meta[category_new]">
			<option value="no"><?php _e( 'No', 'wproto' ); ?></option>
			<option value="yes" <?php echo $data['category_new'] == 'yes' ? 'selected="selected"' : ''; ?>><?php _e( 'Yes', 'wproto' ); ?></option>
		</select>
	</td>
</tr>