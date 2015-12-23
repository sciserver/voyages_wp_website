<p>
	<?php _e( 'Choose divider style', 'wproto' ); ?>: 
	
	<div class="wproto-divider-style ui-buttonset">
	
		<label><input type="radio" <?php echo @$data['settings']['style'] == '' || @$data['settings']['style'] == 'narrow' ? 'checked="checked"' : ''; ?> name="wproto-divider-style" value="narrow" /> <?php _e( 'Narrow', 'wproto' ); ?></label> <br />
	
		<label><input type="radio" <?php echo @$data['settings']['style'] == 'wide' ? 'checked="checked"' : ''; ?> name="wproto-divider-style" value="wide" /> <?php _e( 'Wide', 'wproto' ); ?></label> <br />
	
		<label><input type="radio" <?php echo @$data['settings']['style'] == 'gap' ? 'checked="checked"' : ''; ?> name="wproto-divider-style" value="gap" /> <?php _e( 'Gap', 'wproto' ); ?></label> <br />
	
		<label><input type="radio" <?php echo @$data['settings']['style'] == 'double-gap' ? 'checked="checked"' : ''; ?> name="wproto-divider-style" value="double-gap" /> <?php _e( 'Double Gap', 'wproto' ); ?></label>
		
	</div>

</p>