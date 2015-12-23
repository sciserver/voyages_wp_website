<?php
	global $wpl_galaxy_wp;
	$albums = $wpl_galaxy_wp->model->photoalbums->get_all_albums();	
?>
<p>
	<label for="wproto-photogallery-title"><?php _e( 'Title', 'wproto' ); ?>: </label> <br />
	<input value="<?php echo @$data['settings']['title']; ?>" class="full-width-input" type="text" id="wproto-photogallery-title" />
</p>
<p>
	<label for="wproto-photogallery-album"><?php _e( 'Choose an album', 'wproto' ); ?>: </label> <br />
	<select class="full-width-input" id="wproto-photogallery-album">
		<?php
			
			if( $albums->have_posts() ):
			while( $albums->have_posts() ):
			$albums->the_post();
		?>
		<option <?php echo @$data['settings']['album'] == get_the_ID() ? 'selected="selected"' : ''; ?> value="<?php the_ID(); ?>"><?php the_title(); ?></option>
		<?php
			endwhile;
			endif;
		?>
	</select>
</p>
<p>
	<label for="wproto-photogallery-limit"><?php _e( 'Photos Limit', 'wproto' ); ?>: </label> <br />
	<input value="<?php echo isset( $data['settings']['limit'] ) ? absint( $data['settings']['limit'] ) : 5; ?>" class="full-width-input" type="number" min="1" id="wproto-photogallery-limit" />
</p>