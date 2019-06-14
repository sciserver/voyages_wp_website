<?php if ( ! defined( 'ABSPATH' ) ) exit;
$this->save(); ?>
<div class="wrap">
<h2><?php _e('Equation Editor', 'equation-editor');?></h2>
           <div class="notice notice-success">
<p><?php _e('<strong>Install <a href="http://modalwebstore.com/product/equation-editor-pro/" target="_blank">Equation Editor PRO</a> with new and multiple advanced features.</strong>', 'equation-editor');?> <a href="http://modalwebstore.com/product/equation-editor-pro/" class="button button-primary" target="_blank">Install Now</a></p></button>
    </div>
<form action="" method="post" id="ffm_manager">
<?php wp_nonce_field( 'mw_equation_editor_action', 'mw_equation_editor_nonce' ); //common ?>
<table class="form-table">

<tbody><tr>
<th scope="row"><label for="enable"><?php _e('Enable Equation Editor', 'equation-editor');?></label></th>
<td>
<input name="enable_eq_editor" id="enable_eq_editor" value="1" type="checkbox" <?php echo (isset($this->settings['enable_eq_editor']) && $this->settings['enable_eq_editor'] == '1') ? 'checked="checked"' : '';?>><?php _e('Check to enable Equation Editor', 'equation-editor');?>
</td>
</tr>
<tr>
<th scope="row"><label for="select_eq_editor"><?php _e('Select Editor Type', 'equation-editor');?></label></th>
<td><select name="select_eq_editor" id="select_eq_editor">
	<option value="wiris" <?php echo (isset($this->settings['select_eq_editor']) && $this->settings['select_eq_editor'] == 'wiris') ? 'selected="checked"' : '';?>><?php _e('Wiris Editor', 'equation-editor');?></option>
	<option value="latex" <?php echo (isset($this->settings['select_eq_editor']) && $this->settings['select_eq_editor'] == 'latex') ? 'selected="checked"' : '';?>><?php _e('Latex Editor', 'equation-editor');?></option>
    <option value="both" <?php echo (isset($this->settings['select_eq_editor']) && $this->settings['select_eq_editor'] == 'both') ? 'selected="checked"' : '';?>><?php _e('Both', 'equation-editor');?></option>
	</select>
<p class="description"><?php _e('Default: Wiris Editor', 'equation-editor');?></p>
</td>
</tr>
</tbody>
</table>
<p class="submit"><input name="submit" id="submit" class="button button-primary" value="Save Changes" type="submit"></p>
</form>
<table>
<tr><th><a href="https://wordpress.org/support/plugin/equation-editor/reviews/?filter=5" target="_blank" title="Click to Rate Us">
<?php echo '<img src="' . plugins_url( 'rateus.png', __FILE__ ) . '"> '; ?></a><p style="color:red"><?php _e('Equation Editor is a new plugin on wordpress. Please spend 2 minutes to appreciate our work with ratings.', 'equation-editor');?>
</p></th></tr>
</table>
 <table>
 <tr>
 <th><a href="http://modalwebstore.com/product/equation-editor-pro/" class="button" target="_blank">Documentation</a></th>
 <th><a href="http://modalwebstore.com/contact-us/" class="button" target="_blank">Support</a></th>
 <th><a href="http://modalwebstore.com/donate" class="button" target="_blank">Donate</a></th>
 </tr>
</table>
</div>