<p>
	<label><?php _e( 'Link to the video', 'wproto'); ?>: <input type="text" id="wproto-video-link-input" value="" /></label> <input type="button" class="button-primary" id="wproto-grab-video" value="<?php _e( 'Get video', 'wproto'); ?>" />
</p>
<p>
	<span class="description"><?php _e( 'For example', 'wproto'); ?>: <a id="wproto-example-video-link" href="javascript:;">http://www.youtube.com/watch?v=yR6A-Bk9eZQ</a></span>
</p>
<p>
	<span class="description"><?php _e( 'Now supports', 'wproto'); ?>: <a target="_blank" href="http://youtube.com">YouTube</a> <?php _e( 'and', 'wproto'); ?> <a target="_blank" href="http://vimeo.com">Vimeo</a> <?php _e( 'services', 'wproto'); ?></span>
</p>

<div id="wproto-video-table" <?php if( !isset( $data['type']) || $data['type'] == '' ): ?>style="display: none;"<?php endif; ?>>
	<?php if( isset( $data['type']) || $data['type'] == '' ): ?>
		<?php include "video_content.tpl"; ?>
	<?php endif; ?>
</div>