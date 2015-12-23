<p>
	<label for="wproto-highlight-color"><?php _e( 'Color', 'wproto' ); ?>: </label> <br />
	<input class="wp-color-picker-field" type="text" id="wproto-highlight-color" name="title" data-default-color="<?php echo @$data['color'] <> '' ? $data['color'] : '#ff0000' ; ?>" value="<?php echo @$data['color'] <> '' ? $data['color'] : '#ff0000' ; ?>" />
</p>
<p>
	<label for="wproto-highlight-content"><?php _e( 'Text', 'wproto' ); ?>: </label> 
	<textarea class="full-width-textarea" style="height: 200px" id="wproto-highlight-content" name="content"><?php echo @$data['selected_text']; ?></textarea>
</p>