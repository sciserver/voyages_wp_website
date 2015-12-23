<h2><a href="javascript:;" data-pointer-title="<?php _e( 'Grab Title', 'wproto'); ?>" data-pointer-content="<?php _e( 'Click at the link to use this title as a post title.', 'wproto'); ?>" id="wproto-use-video-title"><?php echo $data['title']; ?></a></h2>

<table width="100%" class="widefat">
	<thead>
		<tr>
			<th><?php _e( 'Video thumbnail', 'wproto'); ?></th>
			<th><?php _e( 'Parameters', 'wproto'); ?></th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>
				<img class="wproto-video-thumb-small-metabox" src="<?php echo $data['thumbnail_small']; ?>" alt="" />
			</td>
			<td style="width: 100%">
				<p>
					<label><?php _e( 'Width', 'wproto'); ?>: &nbsp; <input id="wproto-video-container-width" style="width: 40px" type="text" value="<?php echo isset( $data['video_width'] ) ? $data['video_width'] : 640; ?>" name="video_width" /></label>px
				</p>
				<p>
					<label><?php _e( 'Height', 'wproto'); ?>: <input id="wproto-video-container-height" style="width: 40px" type="text" value="<?php echo isset( $data['video_height'] ) ? $data['video_height'] : 480; ?>" name="video_height" /></label>px
				</p>
				<p class="wproto-container-size-links">
					<a href="javascript:;" class="button">420x315</a>
					<a href="javascript:;" class="button">480x360</a>
					<a href="javascript:;" class="button">640x480</a>
					<a href="javascript:;" class="button">960x720</a>
				</p>
			</td>
		</tr>
	</tbody>
</table>

<input type="hidden" name="player_code" value="<?php echo $data['player_code']; ?>" />
<input type="hidden" name="thumbnail_small" value="<?php echo $data['thumbnail_small']; ?>" />
<input type="hidden" name="thumbnail_medium" value="<?php echo $data['thumbnail_medium']; ?>" />
<input type="hidden" name="thumbnail_big" value="<?php echo $data['thumbnail_big']; ?>" />
<input type="hidden" name="title" value="<?php echo $data['title']; ?>" />
<input type="hidden" name="type" value="<?php echo $data['type']; ?>" />