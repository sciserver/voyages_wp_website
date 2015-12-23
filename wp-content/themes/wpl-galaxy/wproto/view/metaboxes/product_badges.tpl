<p>

	<?php _e( 'Display additional badges', 'wproto' ); ?>:<br />

	<label><input type="radio" <?php echo $data['badge'] == '' ? 'checked="checked"' : ''; ?> name="badge" value="" /> <?php _e( 'Do not display', 'wproto' ); ?></label><br />		
	<label><input type="radio" <?php echo $data['badge'] == 'onsale' ? 'checked="checked"' : ''; ?> name="badge" value="onsale" /> <?php _e( 'Display "On Sale" badge', 'wproto' ); ?></label><br />
	<label><input type="radio" <?php echo $data['badge'] == 'best_price' ? 'checked="checked"' : ''; ?> name="badge" value="best_price" /> <?php _e( 'Display "Best price" badge', 'wproto' ); ?></label>

</p>