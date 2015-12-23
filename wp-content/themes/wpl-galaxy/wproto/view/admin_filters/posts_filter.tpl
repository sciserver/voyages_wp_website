<select name="featured">
	<option value=""><?php _e( 'Is Featured?...', 'wproto'); ?></option>
	<option <?php echo @$_GET['featured'] == 'yes' ? 'selected="selected"' : ''; ?> value="yes"><?php _e( 'Featured posts', 'wproto'); ?></option>
</select>

<?php if( $data['typenow'] == 'post' ): ?>
<select name="post_format">
	<option value=""><?php _e( 'Post format...', 'wproto'); ?></option>
	<option <?php echo @$_GET['post_format'] == 'post-format-aside' ? 'selected="selected"' : ''; ?> value="post-format-aside"><?php _e( 'Aside', 'wproto'); ?></option>
	<option <?php echo @$_GET['post_format'] == 'post-format-gallery' ? 'selected="selected"' : ''; ?> value="post-format-gallery"><?php _e( 'Gallery', 'wproto'); ?></option>
	<option <?php echo @$_GET['post_format'] == 'post-format-link' ? 'selected="selected"' : ''; ?> value="post-format-link"><?php _e( 'Link', 'wproto'); ?></option>
	<option <?php echo @$_GET['post_format'] == 'post-format-image' ? 'selected="selected"' : ''; ?> value="post-format-image"><?php _e( 'Image', 'wproto'); ?></option>
	<option <?php echo @$_GET['post_format'] == 'post-format-quote' ? 'selected="selected"' : ''; ?> value="post-format-quote"><?php _e( 'Quote', 'wproto'); ?></option>
	<option <?php echo @$_GET['post_format'] == 'post-format-status' ? 'selected="selected"' : ''; ?> value="post-format-status"><?php _e( 'Status', 'wproto'); ?></option>
	<option <?php echo @$_GET['post_format'] == 'post-format-video' ? 'selected="selected"' : ''; ?> value="post-format-video"><?php _e( 'Video', 'wproto'); ?></option>
	<option <?php echo @$_GET['post_format'] == 'post-format-audio' ? 'selected="selected"' : ''; ?> value="post-format-audio"><?php _e( 'Audio', 'wproto'); ?></option>
	<option <?php echo @$_GET['post_format'] == 'post-format-chat' ? 'selected="selected"' : ''; ?> value="post-format-chat"><?php _e( 'Chat', 'wproto'); ?></option>
</select>
<?php endif; ?>