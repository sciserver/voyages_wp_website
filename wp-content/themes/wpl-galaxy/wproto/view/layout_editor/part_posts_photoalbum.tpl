
<h2><?php _e('Photoalbum posts carousel', 'wproto'); ?></h2>

<table class="form-table wproto-form-table">
	<tr>
		<th><label for="wproto_section_content-title"><?php _e( 'Section title (optional)', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_content-title" name="wproto_section_content[title]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_content']['title'] ) ? $data['wproto_section_content']['title'] : ''; ?>" />
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto_section_content-subtitle"><?php _e( 'Section subtitle (optional)', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_content-subtitle" name="wproto_section_content[subtitle]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_content']['subtitle'] ) ? $data['wproto_section_content']['subtitle'] : ''; ?>" />
		
		</td>
	</tr>
	<tr>
		<?php
			$display_type = isset( $data['wproto_section_data']['display_content_type'] ) ? $data['wproto_section_data']['display_content_type'] : 'all';
		?>
		<th><p><?php _e( 'Display videos from categories', 'wproto' ); ?>:</p></th>
		<td class="wproto-display-posts-controls">
			<a href="javascript:;" data-display-posts="all" class="button <?php echo $display_type == 'all' ? 'button-primary' : ''; ?>"><?php _e( 'All', 'wproto' ); ?></a>
			<a href="javascript:;" data-display-posts="only" class="button <?php echo $display_type == 'only' ? 'button-primary' : ''; ?>"><?php _e( 'Only', 'wproto' ); ?></a>
			<a href="javascript:;" data-display-posts="all_except" class="button <?php echo $display_type == 'all_except' ? 'button-primary' : ''; ?>"><?php _e( 'All, Except', 'wproto' ); ?></a>
					
			<span class="alignright" <?php echo $display_type == 'all' ? 'style="display: none;"' : ''; ?>>
				<a href="javascript:;" class="select-all"><?php _e( 'Select all', 'wproto' ); ?></a> | 
				<a href="javascript:;" class="select-none"><?php _e( 'Select none', 'wproto' ); ?></a>
			</span>
					
			<input type="hidden" class="wproto-display-posts-categories-input" name="wproto_section_data[display_content_type]" value="<?php echo $display_type; ?>" />
											
		</td>
	</tr>
	<tr class="wproto-display-posts-control-block" <?php echo $display_type == 'all' ? 'style="display: none;"' : ''; ?>>
		<th></th>
		<td>
		
			<div class="wproto-posts-categories-chooser-content">

				<?php
					$tax = get_terms( 'wproto_photoalbums_category', array(
						'hide_empty' => 0
					));
				?>

				<?php if( count( $tax ) > 0 ): ?>
					<?php foreach( $tax as $term ): ?>
							
						<?php
							$selected = isset( $data['wproto_section_data']['posts_categories' ] ) && is_array( $data['wproto_section_data']['posts_categories' ] ) && in_array( $term->term_id, $data['wproto_section_data']['posts_categories' ]);
						?>
							
						<a href="javascript:;" class="<?php echo $selected ? 'selected' : ''; ?>">
							<input <?php echo $selected ? 'checked="checked"' : ''; ?> type="checkbox" name="wproto_section_data[posts_categories][]" value="<?php echo $term->term_id; ?>" /> <span><?php echo $term->name; ?></span>
						</a>
							
					<?php endforeach; ?>
				<?php else: ?>
						
					<p><?php _e('You did not create any categories yet.', 'wproto'); ?></p>
						
				<?php endif; ?>

			</div>
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto_section_data-order"><?php _e( 'Items order', 'wproto' ); ?>:</label></th>
		<td>

			<?php
				$order = isset( $data['wproto_section_data']['order'] ) ? $data['wproto_section_data']['order'] : 'ID';
			?>

			<select id="wproto_section_data-order" name="wproto_section_data[order]">
				<option value="ID">ID</option>
				<option <?php echo $order == 'title' ? 'selected="selected"' : ''; ?> value="title"><?php _e( 'Post title', 'wproto' ); ?></option>
				<option <?php echo $order == 'date' ? 'selected="selected"' : ''; ?> value="date"><?php _e( 'Post date', 'wproto' ); ?></option>
				<option <?php echo $order == 'modified' ? 'selected="selected"' : ''; ?> value="modified"><?php _e( 'Modified date', 'wproto' ); ?></option>
				<option <?php echo $order == 'name' ? 'selected="selected"' : ''; ?> value="name"><?php _e( 'Post slug', 'wproto' ); ?></option>
				<option <?php echo $order == 'author' ? 'selected="selected"' : ''; ?> value="author"><?php _e( 'Post author', 'wproto' ); ?></option>
				<option <?php echo $order == 'comment_count' ? 'selected="selected"' : ''; ?> value="comment_count"><?php _e( 'Comments count', 'wproto' ); ?></option>
			</select>
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto_section_data-sort"><?php _e( 'Items sort', 'wproto' ); ?>:</label></th>
		<td>

			<select id="wproto_section_data-sort" name="wproto_section_data[sort]">
				<option value="DESC"><?php _e( 'Descending', 'wproto' ); ?></option>
				<option <?php echo isset( $data['wproto_section_data']['sort'] ) && $data['wproto_section_data']['sort'] == 'ASC' ? 'selected="selected"' : ''; ?> value="ASC"><?php _e( 'Ascending', 'wproto' ); ?></option>
			</select>
		
		</td>
	</tr>
	<tr>
		<th><label for="wproto_section_data-menu_title"><?php _e( 'Menu title (fot one-page template)', 'wproto' ); ?>:</label></th>
		<td>
		
			<input id="wproto_section_data-menu_title" name="wproto_section_data[menu_title]" class="text" type="text" maxlength="255" value="<?php echo isset( $data['wproto_section_data']['menu_title'] ) ? $data['wproto_section_data']['menu_title'] : ''; ?>" />
		
		</td>
	</tr>
</table>