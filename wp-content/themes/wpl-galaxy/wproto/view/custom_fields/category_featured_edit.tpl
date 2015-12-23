<tr class="form-field">
	<th scope="row" valign="top">
		<label><?php _e( 'This category is featured', 'wproto' ); ?>:</label>
	</th>
	<td>
		<select name="term_meta[category_featured]">
			<option value="no"><?php _e( 'No', 'wproto' ); ?></option>
			<option value="yes" <?php echo $data['category_featured'] == 'yes' ? 'selected="selected"' : ''; ?>><?php _e( 'Yes', 'wproto' ); ?></option>
		</select>
	</td>
</tr>