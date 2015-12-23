<?php if( wpl_galaxy_wp_utils::isset_layerslider() ): ?>

	<?php if( is_array( $data['layerslider_slideshows'] ) && count( $data['layerslider_slideshows'] ) > 0 ): ?>
	
	<p>
		<label for="wproto-layerslider-id"><?php _e( 'Choose a slider', 'wproto' ); ?>: </label> <br />
		<select class="full-width-input" name="" id="wproto-layerslider-id">
			<?php foreach( $data['layerslider_slideshows'] as $slide ): ?>
			<option <?php echo $slide->id == absint( @$data['settings']['id'] ) ? 'selected="selected"' : ''; ?> value="<?php echo $slide->id; ?>"><?php echo $slide->name; ?></option>
			<?php endforeach; ?>
		</select>
	</p>
	
	<?php else: ?>
	
		<p><?php _e( sprintf( 'You have not created any slideshows yet, so we cannot retrieve the slideshow list. <a href="%s" target="_blank">Create your first</a>.', admin_url('admin.php?page=layerslider') ), 'wproto' ); ?></p>
	
	<?php endif; ?>

<?php else: ?>

	<p><?php _e( 'You have not installed Layer Slider plugin yet, so we cannot retrieve the slideshows list.', 'wproto' ); ?></p>

<?php endif; ?>