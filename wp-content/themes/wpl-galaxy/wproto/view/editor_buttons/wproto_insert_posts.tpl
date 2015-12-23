<p>
	<label for="wproto-posts-title"><?php _e( 'Title', 'wproto' ); ?>: </label> <br />
	<input value="<?php echo @$data['settings']['title']; ?>" class="full-width-input" type="text" id="wproto-posts-title" />
</p>
<p>
	<label for="wproto-posts-numberposts"><?php _e( 'Number of posts to display', 'wproto' ); ?>: </label> <br />
	<input value="<?php echo @$data['settings']['limit'] == '' ? '7' : @$data['settings']['limit']; ?>" class="full-width-input" min="1" type="number" id="wproto-posts-numberposts" />
</p>
<p>
	<label for="wproto-posts-cols"><?php _e( 'Number of columns', 'wproto' ); ?>: </label> <br />
	<select class="full-width-input" id="wproto-posts-cols">
		<option <?php echo @$data['settings']['cols'] == 2 ? 'selected="selected"' : ''; ?> value="2">2</option>
		<option <?php echo @$data['settings']['cols'] == 3 ? 'selected="selected"' : ''; ?> value="3">3</option>
		<option <?php echo @$data['settings']['cols'] == 4 ? 'selected="selected"' : ''; ?> value="4">4</option>
	</select>
</p>
<p>
	<label for="wproto-posts-show"><?php _e( 'Display posts', 'wproto' ); ?>: </label> <br />
	<select class="full-width-input" id="wproto-posts-show">
		<option <?php echo @$data['settings']['show'] == 'all' ? 'selected="selected"' : ''; ?> value="all"><?php _e( 'All categories', 'wproto' ); ?></option>
		<option <?php echo @$data['settings']['show'] == 'category' ? 'selected="selected"' : ''; ?> value="category"><?php _e( 'Select category...', 'wproto' ); ?></option>
	</select>
</p>
<p id="wproto-posts-category-div" <?php echo @$data['settings']['show'] == 'category' ? '' : 'style="display: none;"'; ?>>
	<label for="wproto-posts-category"><?php _e( 'Category', 'wproto' ); ?>: </label> <br />
	<select class="full-width-input" id="wproto-posts-category">
		<?php
			$categories = get_terms( 'category', array(
				'hide_empty' => 0
			));
			if( count( $categories ) > 0 ):
			foreach( $categories as $cat ):
		?>
		<option <?php echo @$data['settings']['category'] == $cat->term_id ? 'selected="selected"' : ''; ?> value="<?php echo $cat->term_id; ?>"><?php echo $cat->name; ?></option>
		<?php
			endforeach;
			endif;
		?>
	</select>
</p>
<p>
	<label for="wproto-posts-orderby"><?php _e( 'Order by', 'wproto' ); ?>: </label> <br />
	<select class="full-width-input" id="wproto-posts-orderby">
		<option <?php echo @$data['settings']['orderby'] == 'id' ? 'selected="selected"' : ''; ?> value="id"><?php _e( 'ID', 'wproto' ); ?></option>
		<option <?php echo @$data['settings']['orderby'] == 'date' ? 'selected="selected"' : ''; ?> value="date"><?php _e( 'Date', 'wproto' ); ?></option>
		<option <?php echo @$data['settings']['orderby'] == 'modified' ? 'selected="selected"' : ''; ?> value="modified"><?php _e( 'Modified', 'wproto' ); ?></option>
		<option <?php echo @$data['settings']['orderby'] == 'title' ? 'selected="selected"' : ''; ?> value="title"><?php _e( 'Title', 'wproto' ); ?></option>
		<option <?php echo @$data['settings']['orderby'] == 'rand' ? 'selected="selected"' : ''; ?> value="rand"><?php _e( 'Random', 'wproto' ); ?></option>
		<option <?php echo @$data['settings']['orderby'] == 'menu' ? 'selected="selected"' : ''; ?> value="menu"><?php _e( 'Menu order', 'wproto' ); ?></option>
	</select>
</p>
<p>
	<label for="wproto-posts-sort"><?php _e( 'Sort', 'wproto' ); ?>: </label> <br />
	<select class="full-width-input" id="wproto-posts-sort">
		<option <?php echo @$data['settings']['sort'] == 'ASC' ? 'selected="selected"' : ''; ?> value="ASC"><?php _e( 'Ascending', 'wproto' ); ?></option>
		<option <?php echo @$data['settings']['sort'] == 'DESC' ? 'selected="selected"' : ''; ?> value="DESC"><?php _e( 'Descending', 'wproto' ); ?></option>
	</select>
</p>