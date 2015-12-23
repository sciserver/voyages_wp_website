<?php if( $data['tables']->have_posts() ): ?>
	
<p>
	<label for="wproto-pricingtable-id"><?php _e( 'Choose a table', 'wproto' ); ?>: </label> <br />
	<select class="full-width-input" name="" id="wproto-pricingtable-id">
	<?php while( $data['tables']->have_posts() ): $data['tables']->the_post(); ?>
	<option <?php echo isset( $data['settings']['id'] ) && get_the_ID() == $data['settings']['id'] ? 'selected="selected"' : ''; ?> value="<?php the_ID(); ?>"><?php the_title(); ?></option>
	<?php endwhile; ?>
	</select>
</p>
	
<?php else: ?>
	
	<p><?php _e( sprintf( 'You have not created any pricing table yet, so we cannot retrieve the tables list. <a href="%s" target="_blank">Create your first pricing table</a>.', admin_url('post-new.php?post_type=wproto_pricing_table') ), 'wproto' ); ?></p>
	
<?php endif; ?>