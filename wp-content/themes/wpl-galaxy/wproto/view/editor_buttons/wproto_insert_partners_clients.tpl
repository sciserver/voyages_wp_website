<p>
	<label for="wproto-partners-title"><?php _e( 'Title', 'wproto' ); ?>: </label> <br />
	<input value="<?php echo @$data['settings']['title']; ?>" class="full-width-input" type="text" id="wproto-partners-title" />
</p>
<p>
	<label for="wproto-partners-numberposts"><?php _e( 'Number of posts to display', 'wproto' ); ?>: </label> <br />
	<input value="<?php echo @$data['settings']['limit'] == '' ? '7' : @$data['settings']['limit']; ?>" class="full-width-input" min="1" type="number" id="wproto-partners-numberposts" />
</p>
<p>
	<label for="wproto-partners-show"><?php _e( 'Display posts', 'wproto' ); ?>: </label> <br />
	<select class="full-width-input" id="wproto-partners-show">
		<option <?php echo @$data['settings']['show'] == 'all' ? 'selected="selected"' : ''; ?> value="all"><?php _e( 'All categories', 'wproto' ); ?></option>
		<option <?php echo @$data['settings']['show'] == 'category' ? 'selected="selected"' : ''; ?> value="category"><?php _e( 'Select category...', 'wproto' ); ?></option>
	</select>
</p>
<p id="wproto-partners-category-div" <?php echo @$data['settings']['show'] == 'category' ? '' : 'style="display: none;"'; ?>>
	<label for="wproto-partners-category"><?php _e( 'Category', 'wproto' ); ?>: </label> <br />
	<select class="full-width-input" id="wproto-partners-category">
		<?php
			$categories = get_terms( 'wproto_partners_category', array(
				'hide_empty' => 0
			));
			if( is_array( $categories ) && count( $categories ) > 0 ):
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
	<label for="wproto-partners-orderby"><?php _e( 'Order by', 'wproto' ); ?>: </label> <br />
	<select class="full-width-input" id="wproto-partners-orderby">
		<option <?php echo @$data['settings']['orderby'] == 'id' ? 'selected="selected"' : ''; ?> value="id"><?php _e( 'ID', 'wproto' ); ?></option>
		<option <?php echo @$data['settings']['orderby'] == 'date' ? 'selected="selected"' : ''; ?> value="date"><?php _e( 'Date', 'wproto' ); ?></option>
		<option <?php echo @$data['settings']['orderby'] == 'modified' ? 'selected="selected"' : ''; ?> value="modified"><?php _e( 'Modified', 'wproto' ); ?></option>
		<option <?php echo @$data['settings']['orderby'] == 'title' ? 'selected="selected"' : ''; ?> value="title"><?php _e( 'Title', 'wproto' ); ?></option>
		<option <?php echo @$data['settings']['orderby'] == 'random' ? 'selected="selected"' : ''; ?> value="random"><?php _e( 'Random', 'wproto' ); ?></option>
		<option <?php echo @$data['settings']['orderby'] == 'menu' ? 'selected="selected"' : ''; ?> value="menu"><?php _e( 'Menu order', 'wproto' ); ?></option>
	</select>
</p>
<p>
	<label for="wproto-partners-sort"><?php _e( 'Sort', 'wproto' ); ?>: </label> <br />
	<select class="full-width-input" id="wproto-partners-sort">
		<option <?php echo @$data['settings']['sort'] == 'ASC' ? 'selected="selected"' : ''; ?> value="ASC"><?php _e( 'Ascending', 'wproto' ); ?></option>
		<option <?php echo @$data['settings']['sort'] == 'DESC' ? 'selected="selected"' : ''; ?> value="DESC"><?php _e( 'Descending', 'wproto' ); ?></option>
	</select>
</p>