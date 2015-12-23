<table class="form-table wproto-form-table">
	<tr>
		<th>
			<label for="wproto-price"><?php _e( 'Price', 'wproto' ); ?>:</label>
		</th>
		<td>
			<input id="wproto-price" class="wproto-price-input" type="text" value="<?php echo $data['price']; ?>" name="price" />
		</td>
	</tr>
	<tr>
		<th>
			<label for="wproto-old-price"><?php _e( 'Old price', 'wproto' ); ?>:</label>
			<p class="description"><?php _e( '(optional)', 'wproto' ); ?></p>
		</th>
		<td>
			<input id="wproto-old-price" class="wproto-price-input" type="text" value="<?php echo $data['old_price']; ?>" name="old_price" />		
		</td>
	</tr>
	<tr>
		<th>
			<label for="wproto-sku"><?php _e( 'SKU', 'wproto' ); ?>:</label>
			<p class="description"><?php _e( '(optional)', 'wproto' ); ?></p>
		</th>
		<td>
			<input id="wproto-sku" class="wproto-price-input" type="text" value="<?php echo $data['sku']; ?>" name="sku" />		
		</td>
	</tr>
	<tr>
		<th>
			<label for="wproto-link-to-buy"><?php _e( 'Link to buy', 'wproto' ); ?>:</label>
		</th>
		<td>
			<textarea id="wproto-link-to-buy" class="wproto-link-to-buy-textarea" name="link_to_buy"><?php echo $data['link_to_buy']; ?></textarea>	
		</td>
	</tr>
	<tr>
		<th>
			<label><?php _e( 'Display additional badges', 'wproto' ); ?>:</label>
		</th>
		<td>
			
			<label><input type="radio" <?php echo $data['badge'] == '' ? 'checked="checked"' : ''; ?> name="badge" value="" /> <?php _e( 'Do not display', 'wproto' ); ?></label><br />		
			<label><input type="radio" <?php echo $data['badge'] == 'onsale' ? 'checked="checked"' : ''; ?> name="badge" value="onsale" /> <?php _e( 'Display "On Sale" badge', 'wproto' ); ?></label><br />
			<label><input type="radio" <?php echo $data['badge'] == 'best_price' ? 'checked="checked"' : ''; ?> name="badge" value="best_price" /> <?php _e( 'Display "Best price" badge', 'wproto' ); ?></label>
						
		</td>
	</tr>
</table>