<h3><?php _e( 'Text colors', 'wproto' ); ?></h3>
<p>
	<label for="wproto-call-to-action-title"><?php _e( 'Title', 'wproto' ); ?>: </label> 
	<input class="full-width-input" type="text" id="wproto-call-to-action-title" value="<?php echo @$data['settings']['title']; ?>" />
</p>
<p>
	<label for="wproto-call-to-action-title-color"><?php _e( 'Title color', 'wproto' ); ?>: </label> <br />
	<input class="wp-color-picker-field" type="text" id="wproto-call-to-action-title-color" data-default-color="<?php echo @$data['settings']['title_color'] == '' ? '#3c4247' : @$data['settings']['title_color'] ; ?>" value="<?php echo @$data['settings']['title_color'] == '' ? '#3c4247' : @$data['settings']['title_color'] ; ?>" />
</p>
<p>
	<label for="wproto-call-to-action-text"><?php _e( 'Text', 'wproto' ); ?>: </label> 
	<textarea class="full-width-textarea" style="height: 100px" id="wproto-call-to-action-text"><?php echo @$data['settings']['text_content']; ?></textarea>
</p>
<p>
	<label for="wproto-call-to-action-text-color"><?php _e( 'Text color', 'wproto' ); ?>: </label> <br />
	<input class="wp-color-picker-field" type="text" id="wproto-call-to-action-text-color" data-default-color="<?php echo @$data['settings']['text_color'] == '' ? '#3c4247' : @$data['settings']['text_color'] ; ?>" value="<?php echo @$data['settings']['text_color'] == '' ? '#777f8a' : @$data['settings']['text_color'] ; ?>" />
</p>
<h3><?php _e( 'Action button', 'wproto' ); ?></h3>
<p>
	<label><input type="checkbox" id="wproto-call-to-action-show-button" <?php echo @$data['settings']['show_button'] == 'yes' ? 'checked="checked"' : ''; ?> /> <?php _e( 'Show link button', 'wproto' ); ?></label>
</p>
<div id="wproto-call-to-action-show-button-block" <?php echo @$data['settings']['show_button'] == 'yes' ? '' : 'style="display: none;"'; ?>>
<p>
	<label for="wproto-call-to-action-button-text"><?php _e( 'Button text', 'wproto' ); ?>: </label> 
	<input class="full-width-input" type="text" id="wproto-call-to-action-button-text" value="<?php echo @$data['settings']['button_text']; ?>" />
</p>
<p>
	<label for="wproto-call-to-action-button-color"><?php _e( 'Button Background Color', 'wproto' ); ?>: </label> <br />
	<input class="wp-color-picker-field" type="text" id="wproto-call-to-action-button-color" data-default-color="<?php echo @$data['settings']['button_color'] == '' ? '#3492d1' : @$data['settings']['button_color'] ; ?>" value="<?php echo @$data['settings']['button_color'] == '' ? '#3492d1' : @$data['settings']['button_color'] ; ?>" />
</p>
<p>
	<label for="wproto-call-to-action-button-text-color"><?php _e( 'Button Text Color', 'wproto' ); ?>: </label> <br />
	<input class="wp-color-picker-field" type="text" id="wproto-call-to-action-button-text-color" data-default-color="<?php echo @$data['settings']['button_text_color'] == '' ? '#FFFFFF' : @$data['settings']['button_text_color'] ; ?>" value="<?php echo @$data['settings']['button_text_color'] == '' ? '#FFFFFF' : @$data['settings']['button_text_color'] ; ?>" />
</p>
<p>
	<label for="wproto-call-to-action-link"><?php _e( 'Link', 'wproto' ); ?>: </label> 
	<input class="full-width-input" type="text" id="wproto-call-to-action-link" value="<?php echo @$data['settings']['link']; ?>" />
</p>
<p>
	<label><input type="checkbox" value="yes" id="wproto-call-to-action-new-window" <?php echo @$data['settings']['new_window'] == 'yes' ? 'checked="checked"' : ''; ?> /> <?php _e( 'Open link at new window?', 'wproto' ); ?></label>
</p>
<p>
	<label for="wproto-call-to-action-button-size"><?php _e( 'Button size', 'wproto' ); ?>: </label>
	<select id="wproto-call-to-action-button-size">
		<option <?php echo @$data['settings']['button_size'] == 'small' || @$data['settings']['button_size'] == '' ? 'selected="selected"' : ''; ?> value="small"><?php _e( 'Small', 'wproto' ); ?></option>
		<option <?php echo @$data['settings']['button_size'] == 'medium' ? 'selected="selected"' : ''; ?> value="medium"><?php _e( 'Medium', 'wproto' ); ?></option>
		<option <?php echo @$data['settings']['button_size'] == 'big' ? 'selected="selected"' : ''; ?> value="big"><?php _e( 'Big', 'wproto' ); ?></option>
	</select> 
</p>
</div>
<h3><?php _e( 'Box Icon', 'wproto' ); ?></h3>
<p>
	<label for="wproto-call-to-action-icon"><?php _e( 'Icon', 'wproto' ); ?>: </label> <br />
	<i data-name="<?php echo @$data['settings']['icon']; ?>" class="wproto-icon-holder <?php echo @$data['settings']['icon']; ?> icon-2x"></i> <a href="javascript:;" class="wproto-icon-chooser"><?php _e( 'Select icon', 'wproto' ); ?></a>
	<input type="hidden" id="wproto-call-to-action-icon" value="<?php echo @$data['settings']['icon']; ?>" name="wproto_benefit_icon_name" class="wproto-icon-holder-input" />
</p>
<p>
	<label for="wproto-call-to-action-icon-color"><?php _e( 'Icon Color', 'wproto' ); ?>: </label> <br />
	<input class="wp-color-picker-field" type="text" id="wproto-call-to-action-icon-color" data-default-color="<?php echo @$data['settings']['icon_color'] == '' ? '#3492d1' : @$data['settings']['icon_color'] ; ?>" value="<?php echo @$data['settings']['icon_color'] == '' ? '#3492d1' : @$data['settings']['icon_color'] ; ?>" />
</p>
<h3><?php _e( 'Box style', 'wproto' ); ?></h3>
<p>
	<label for="wproto-call-to-action-border-color"><?php _e( 'Border Color', 'wproto' ); ?>: </label> <br />
	<input class="wp-color-picker-field" type="text" id="wproto-call-to-action-border-color" data-default-color="<?php echo @$data['settings']['border_color'] == '' ? '#3492d1' : @$data['settings']['border_color'] ; ?>" value="<?php echo @$data['settings']['border_color'] == '' ? '#3492d1' : @$data['settings']['border_color'] ; ?>" />
</p>
<p>
	<label for="wproto-call-to-action-background-color"><?php _e( 'Background Color', 'wproto' ); ?>: </label> <br />
	<input class="wp-color-picker-field" type="text" id="wproto-call-to-action-background-color" data-default-color="<?php echo @$data['settings']['background'] == '' ? '#f0f2f3' : @$data['settings']['background'] ; ?>" value="<?php echo @$data['settings']['background'] == '' ? '#f0f2f3' : @$data['settings']['background'] ; ?>" />
</p>