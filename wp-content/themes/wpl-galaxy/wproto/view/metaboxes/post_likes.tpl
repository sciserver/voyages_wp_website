<?php 
	$views = absint( @$data['views'] );
?>
<?php if( !isset( $data['hide_likes'] ) ): $likes = absint( $data['likes'] ); ?>
<p>
	<label><input type="number" min="0" class="wproto-likes-input" name="wproto_likes" value="<?php echo $likes; ?>" /> <?php echo wpl_galaxy_wp_utils::plural_form( $likes, __( 'Like', 'wproto'), __( 'Likes', 'wproto'), __( 'Likes', 'wproto')); ?></label>
</p>
<?php endif; ?>
<p>
	<label><input type="number" min="0" class="wproto-likes-input" name="wproto_views" value="<?php echo $views; ?>" /> <?php echo wpl_galaxy_wp_utils::plural_form( $views, __( 'View', 'wproto'), __( 'Views', 'wproto'), __( 'Views', 'wproto')); ?></label>
</p>