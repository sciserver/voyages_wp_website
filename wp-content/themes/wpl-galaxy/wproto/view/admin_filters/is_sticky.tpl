<a data-value="<?php echo is_sticky( @$data['id'] ) ? 'true' : 'false'; ?>" data-pointer-title="<?php _e( 'Change &laquo;Sticky&raquo; status', 'wproto' ); ?>" data-pointer-content="<?php _e( 'Click here to make a post sticky or default.', 'wproto' ); ?>" href="javascript:;" data-post-id="<?php echo $data['post_id']; ?>" class="wproto_change_post_status wproto_change_sticky">
	<img width="16" height="16" src="<?php echo WPROTO_THEME_URL; ?>/images/admin/<?php echo is_sticky( @$data['id'] ) ? 'true' : 'false'; ?><?php echo wpl_galaxy_wp_utils::is_retina() ? '@2x' : ''; ?>.png" alt="" />
</a>
