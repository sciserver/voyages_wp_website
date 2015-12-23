<p>
	<label for="wproto-google-map-address"><?php _e( 'Type address', 'wproto' ); ?>: </label> <br />
	<input value="<?php echo @$data['settings']['address'] == '' ? __('California', 'wproto') : @$data['settings']['address']; ?>" class="full-width-input" type="text" id="wproto-google-map-address" />
</p>
<p>
	<label><?php _e( 'Map zoom', 'wproto' ); ?></label><br />
	<input type="number" value="<?php echo @$data['settings']['zoom'] == '' ? 10 : absint( @$data['settings']['zoom'] ); ?>" name="zoom" id="wproto-google-map-zoom" />
</p>