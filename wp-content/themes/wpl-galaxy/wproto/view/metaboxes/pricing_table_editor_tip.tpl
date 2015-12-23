<p><?php _e( 'You can use these shortcodes to display some graphics in your table. Selected shortcode will be replaced with appropriate icon', 'wproto'); ?>:</p>

<?php
	$is_retina = wpl_galaxy_wp_utils::is_retina();
?>

<table class="widefat">
	<tr>
		<th style="width: 50%;"><?php _e('Shortcode', 'wproto'); ?></th>
		<th><?php _e('Icon', 'wproto'); ?></th>
	</tr>
	<tr>
		<td><strong>[y]</strong></td>
		<td><img src="<?php echo $is_retina ? WPROTO_THEME_URL . '/images/shortcodes/y@2x.png' : WPROTO_THEME_URL . '/images/shortcodes/y.png'; ?>" alt="" width="16" height="16" /></td>
	</tr>
	<tr>
		<td><strong>[n]</strong></td>
		<td><img src="<?php echo $is_retina ? WPROTO_THEME_URL . '/images/shortcodes/n@2x.png' : WPROTO_THEME_URL . '/images/shortcodes/n.png'; ?>" alt="" width="16" height="16" /></td>
	</tr>
	<tr>
		<td><strong>[na]</strong></td>
		<td><img src="<?php echo $is_retina ? WPROTO_THEME_URL . '/images/shortcodes/na@2x.png' : WPROTO_THEME_URL . '/images/shortcodes/na.png'; ?>" alt="" width="16" height="16" /></td>
	</tr>
	<tr>
		<td><strong>[star0]</strong></td>
		<td><img src="<?php echo $is_retina ? WPROTO_THEME_URL . '/images/shortcodes/star0@2x.png' : WPROTO_THEME_URL . '/images/shortcodes/star0.png'; ?>" alt="" width="16" height="16" /></td>
	</tr>
	<tr>
		<td><strong>[star50]</strong></td>
		<td><img src="<?php echo $is_retina ? WPROTO_THEME_URL . '/images/shortcodes/star50@2x.png' : WPROTO_THEME_URL . '/images/shortcodes/star50.png'; ?>" alt="" width="16" height="16" /></td>
	</tr>
	<tr>
		<td><strong>[star100]</strong></td>
		<td><img src="<?php echo $is_retina ? WPROTO_THEME_URL . '/images/shortcodes/star100@2x.png' : WPROTO_THEME_URL . '/images/shortcodes/star100.png'; ?>" alt="" width="16" height="16" /></td>
	</tr>
	<tr>
		<td><strong>[cool]</strong></td>
		<td><img src="<?php echo $is_retina ? WPROTO_THEME_URL . '/images/shortcodes/cool@2x.png' : WPROTO_THEME_URL . '/images/shortcodes/cool.png'; ?>" alt="" width="16" height="16" /></td>
	</tr>
</table>