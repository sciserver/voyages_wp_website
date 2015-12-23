<?php
	$content_layout = isset( $data['wproto_content_layout'] ) ? $data['wproto_content_layout'] : 'one_column_list';
	$wproto_content_layout_filters = isset( $data['wproto_content_layout_filters'] ) ? $data['wproto_content_layout_filters'] : 'no';
	$wproto_content_layout_display_page_text = isset( $data['wproto_content_layout_display_page_text'] ) ? $data['wproto_content_layout_display_page_text'] : 'hide';
	$wproto_content_layout_posts_per_page = isset( $data['wproto_content_layout_posts_per_page'] ) && $data['wproto_content_layout_posts_per_page'] > 0 ? absint( $data['wproto_content_layout_posts_per_page'] ) : get_option('posts_per_page');
	
	$wproto_content_pagination = isset( $data['wproto_content_pagination'] ) ? $data['wproto_content_pagination'] : 'yes';
	$wproto_content_pagination_style = isset( $data['wproto_content_pagination_style'] ) ? $data['wproto_content_pagination_style'] : 'numeric';
	
	$wproto_content_display_posts_type = isset( $data['wproto_content_display_posts_type'] ) ? $data['wproto_content_display_posts_type'] : 'all';
	
	$wproto_content_layout_products_view = isset( $data['wproto_content_layout_products_view'] ) ? $data['wproto_content_layout_products_view'] : 'grid';
	
	$wproto_content_display_categories = isset( $data['wproto_content_display_categories'] ) ? unserialize( $data['wproto_content_display_categories'] ) : array();
	
	$wproto_content_display_posts_order = isset( $data['wproto_content_display_posts_order'] ) ? $data['wproto_content_display_posts_order'] : 'ID';
	$wproto_content_display_posts_sort = isset( $data['wproto_content_display_posts_sort'] ) ? $data['wproto_content_display_posts_sort'] : 'DESC';

?>

<div id="wproto-metabox-content-layout-editor">

	<ul class="wproto-content-layout-type">

		<!-- ONE COLUMN LAYOUT -->
		<li data-layout="one_column_list" class="ib <?php echo $content_layout == 'one_column_list' ? 'selected' : ''; ?>"><a href="javascript:;" class="content-layout-link one-column-list"></a><a href="javascript:;"><?php _e( 'One Column List', 'wproto' ); ?></a></li>
			
		<!-- ONE COLUMN GRID -->
		<li data-layout="one_column_grid" class="ib <?php echo $content_layout == 'one_column_grid' ? 'selected' : ''; ?>"><a href="javascript:;" class="content-layout-link one-column-grid"></a><a href="javascript:;"><?php _e( 'One Column Grid', 'wproto' ); ?></a></li>
			
		<!-- TWO COLUMNS -->
		<li data-layout="two_columns" class="ib <?php echo $content_layout == 'two_columns' ? 'selected' : ''; ?>"><a href="javascript:;" class="content-layout-link two-columns"></a><a href="javascript:;"><?php _e( 'Two Columns', 'wproto' ); ?></a></li>
			
		<!-- THREE COLUMNS -->
		<li data-layout="three_columns" class="ib <?php echo $content_layout == 'three_columns' ? 'selected' : ''; ?>"><a href="javascript:;" class="content-layout-link three-columns"></a><a href="javascript:;"><?php _e( 'Three Columns', 'wproto' ); ?></a></a></li>
			
		<!-- FOUR COLUMNS -->
		<li data-layout="four_columns" class="ib <?php echo $content_layout == 'four_columns' ? 'selected' : ''; ?>"><a href="javascript:;" class="content-layout-link four-columns"></a><a href="javascript:;"><?php _e( 'Four Columns', 'wproto' ); ?></a></a></li>
			
		<!-- MASONRY LAYOUT -->
		<li data-layout="masonry" class="ib <?php echo $content_layout == 'masonry' ? 'selected' : ''; ?>"><a href="javascript:;" class="content-layout-link masonry"></a><a href="javascript:;"><?php _e( 'Masonry Layout', 'wproto' ); ?></a></a></li>
			
		<!-- TIMELINE LAYOUT -->
		<li data-layout="timeline" class="ib <?php echo $content_layout == 'timeline' ? 'selected' : ''; ?>"><a href="javascript:;" class="content-layout-link timeline"></a><a href="javascript:;"><?php _e( 'Timeline', 'wproto' ); ?></a></a></li>
		
		<!-- HEXAGON LAYOUT -->
		<li data-layout="hexagon" class="ib <?php echo $content_layout == 'hexagon' ? 'selected' : ''; ?>"><a href="javascript:;" class="content-layout-link hexagon"></a><a href="javascript:;"><?php _e( 'Hexagon', 'wproto' ); ?></a></a></li>
		
	</ul>
	
	<input type="hidden" class="wproto-hidden" id="wproto-content-layout-input" name="wproto_settings[wproto_content_layout]" value="<?php echo $content_layout; ?>" />
	
	<div class="clear"></div>
	
	<div class="wproto-metabox-inside-bg wproto-layout-type-settings-inside">
	
		<table class="form-table wproto-form-table">
			<tr id="wproto-layout-filters-tr" style="<?php echo $content_layout != 'hexagon' ? 'display: none' : ''; ?>">
				<th class="yesno-input"><label><?php _e( 'Display posts filters', 'wproto' ); ?>:</label></th>
				<td>

					<div class="field switch">
						<label class="cb-enable <?php echo $wproto_content_layout_filters == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
						<label class="cb-disable <?php echo $wproto_content_layout_filters == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
						<input name="wproto_settings[wproto_content_layout_filters]" type="hidden" value="<?php echo $wproto_content_layout_filters; ?>" />
						<div class="clear"></div>
					</div>
		
				</td>
			</tr>
			<tr id="wproto-product-view-tr">
				<th><label for="wproto_content_layout_products_view"><?php _e( 'Products default view', 'wproto' ); ?>:</label></th>
				<td>

					<select class="select" name="wproto_settings[wproto_content_layout_products_view]" id="wproto_content_layout_products_view">
						<option value="grid"><?php _e( 'Grid', 'wproto' ); ?></option>
						<option <?php echo $wproto_content_layout_products_view == 'list' ? 'selected="selected"' : ''; ?> value="list"><?php _e( 'List', 'wproto' ); ?></option>
					</select>
		
				</td>
			</tr>
			<tr>
				<th><label for="wproto_content_layout_display_page_text"><?php _e( 'Display page content', 'wproto' ); ?>:</label></th>
				<td>

					<select class="select" name="wproto_settings[wproto_content_layout_display_page_text]" id="wproto_content_layout_display_page_text">
						<option value="hide"><?php _e( 'Do not display page content', 'wproto' ); ?></option>
						<option <?php echo $wproto_content_layout_display_page_text == 'before' ? 'selected="selected"' : ''; ?> value="before"><?php _e( 'Display before list of posts', 'wproto' ); ?></option>
						<option <?php echo $wproto_content_layout_display_page_text == 'after' ? 'selected="selected"' : ''; ?> value="after"><?php _e( 'Display after list of posts', 'wproto' ); ?></option>
					</select>
		
				</td>
			</tr>
			<tr>
				<th><label for=""><?php _e( 'Posts per page', 'wproto' ); ?>:</label></th>
				<td>

					<input type="number" name="wproto_settings[wproto_content_layout_posts_per_page]" id="wproto_content_layout_posts_per_page" min="1" max="50" value="<?php echo $wproto_content_layout_posts_per_page; ?>" />
		
				</td>
			</tr>
			<tr id="wproto-pagination-show-hide" class="no-hexagon-with-filters">
				<th><label><?php _e( 'Show pagination', 'wproto' ); ?>:</label></th>
				<td>

					<div class="field switch">
						<label class="cb-enable <?php echo $wproto_content_pagination == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
						<label class="cb-disable <?php echo $wproto_content_pagination == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
						<input data-toggle-element="tr.wproto-pagination-settings" name="wproto_settings[wproto_content_pagination]" type="hidden" value="<?php echo $wproto_content_pagination; ?>" />
						<div class="clear"></div>
					</div>
		
				</td>
			</tr>
			<tr class="wproto-pagination-settings no-hexagon-with-filters" style="<?php echo $wproto_content_pagination != 'yes' ? 'display: none;' : ''; ?>">
				<th><label><?php _e( 'Pagination style', 'wproto' ); ?>:</label></th>
				<td>

					<label><input <?php echo $wproto_content_pagination_style == 'numeric' ? 'checked="checked"' : ''; ?> type="radio" name="wproto_settings[wproto_content_pagination_style]" value="numeric" /> <?php _e( 'Numeric', 'wproto' ); ?></label><br />
					<label><input <?php echo $wproto_content_pagination_style == 'text' ? 'checked="checked"' : ''; ?> type="radio" name="wproto_settings[wproto_content_pagination_style]" value="text" /> <?php _e( 'Previous / Next', 'wproto' ); ?></label><br />
					<label><input <?php echo $wproto_content_pagination_style == 'ajax' ? 'checked="checked"' : ''; ?> type="radio" name="wproto_settings[wproto_content_pagination_style]" value="ajax" /> <?php _e( 'AJAX', 'wproto' ); ?></label><br />
		
				</td>
			</tr>
			<tr id="wproto-ls-display-from-cats-tr" class="no-hexagon-with-filters">
				<th><p><?php _e( 'Display posts from categories', 'wproto' ); ?>:</p></th>
				<td class="wproto-display-posts-controls">
					<a href="javascript:;" data-display-posts="all" class="button <?php echo $wproto_content_display_posts_type == 'all' ? 'button-primary' : ''; ?>"><?php _e( 'All', 'wproto' ); ?></a>
					<a href="javascript:;" data-display-posts="only" class="button <?php echo $wproto_content_display_posts_type == 'only' ? 'button-primary' : ''; ?>"><?php _e( 'Only', 'wproto' ); ?></a>
					<a href="javascript:;" data-display-posts="all_except" class="button <?php echo $wproto_content_display_posts_type == 'all_except' ? 'button-primary' : ''; ?>"><?php _e( 'All, Except', 'wproto' ); ?></a>
					
					<span class="alignright" <?php echo $wproto_content_display_posts_type == 'all' ? 'style="display: none;"' : ''; ?>>
						<a href="javascript:;" class="select-all"><?php _e( 'Select all', 'wproto' ); ?></a> | 
						<a href="javascript:;" class="select-none"><?php _e( 'Select none', 'wproto' ); ?></a>
					</span>
					
					<input type="hidden" class="wproto-display-posts-categories-input" name="wproto_settings[wproto_content_display_posts_type]" value="<?php echo $wproto_content_display_posts_type; ?>" />
											
				</td>
			</tr>
			<tr class="wproto-display-posts-control-block no-hexagon-with-filters" <?php echo $wproto_content_display_posts_type == 'all' ? 'style="display: none;"' : ''; ?>>
				<th></th>
				<td>
				
					<?php foreach( $data['_wproto_taxonomies'] as $tax_k=>$tax_v ): ?>
					
						<?php
							$tpl = '';
							switch( $tax_k ) {
								case( 'category' ):
									$tpl = 'page-tpl-blog.php';
								break;
								case( 'wproto_video_category' ):
									$tpl = 'page-tpl-videos.php';
								break;
								case( 'wproto_catalog_category' ):
									$tpl = 'page-tpl-catalog.php';
								break;
								case( 'wproto_portfolio_category' ):
									$tpl = 'page-tpl-portfolio.php';
								break;
								case( 'product_cat' ):
									$tpl = 'page-tpl-shop.php';
								break;
							}
						?>
					
						<div data-tpl="<?php echo $tpl; ?>" class="wproto-posts-categories-chooser-content">

							<?php if( count( $tax_v ) > 0 ): ?>
								<?php foreach( $tax_v as $term ): ?>
							
									<?php
										$selected = isset( $wproto_content_display_categories[ $tax_k ] ) && is_array( $wproto_content_display_categories[ $tax_k ] ) && in_array( $term->term_id, $wproto_content_display_categories[ $tax_k ]);
									?>
							
									<a href="javascript:;" class="<?php echo $selected ? 'selected' : ''; ?>">
										<input <?php echo $selected ? 'checked="checked"' : ''; ?> type="checkbox" name="wproto_settings[wproto_content_display_categories][<?php echo $tax_k; ?>][]" value="<?php echo $term->term_id; ?>" /> <span><?php echo $term->name; ?></span>
									</a>
							
								<?php endforeach; ?>
							<?php else: ?>
						
								<p><?php _e('You did not create any categories yet.', 'wproto'); ?></p>
						
							<?php endif; ?>

						</div>
					
					<?php endforeach; ?>
				
				</td>
			</tr>
			<tr id="wproto-ls-order-tr" class="no-hexagon-with-filters">
				<th><label for="wproto_content_display_posts_order"><?php _e( 'Posts order', 'wproto' ); ?>:</label></th>
				<td>

					<select name="wproto_settings[wproto_content_display_posts_order]">
						<option value="ID">ID</option>
						<option <?php echo $wproto_content_display_posts_order == 'title' ? 'selected="selected"' : ''; ?> value="title"><?php _e( 'Post title', 'wproto' ); ?></option>
						<option <?php echo $wproto_content_display_posts_order == 'date' ? 'selected="selected"' : ''; ?> value="date"><?php _e( 'Post date', 'wproto' ); ?></option>
						<option <?php echo $wproto_content_display_posts_order == 'modified' ? 'selected="selected"' : ''; ?> value="modified"><?php _e( 'Modified date', 'wproto' ); ?></option>
						<option <?php echo $wproto_content_display_posts_order == 'name' ? 'selected="selected"' : ''; ?> value="name"><?php _e( 'Post slug', 'wproto' ); ?></option>
						<option <?php echo $wproto_content_display_posts_order == 'author' ? 'selected="selected"' : ''; ?> value="author"><?php _e( 'Post author', 'wproto' ); ?></option>
						<option <?php echo $wproto_content_display_posts_order == 'comment_count' ? 'selected="selected"' : ''; ?> value="comment_count"><?php _e( 'Comments count', 'wproto' ); ?></option>
					</select>
		
				</td>
			</tr>
			<tr id="wproto-ls-sort-tr" class="no-hexagon-with-filters">
				<th><label><?php _e( 'Posts sort', 'wproto' ); ?>:</label></th>
				<td>

					<select id="wproto_content_display_posts_sort" name="wproto_settings[wproto_content_display_posts_sort]">
						<option value="DESC"><?php _e( 'Descending', 'wproto' ); ?></option>
						<option <?php echo $wproto_content_display_posts_sort == 'ASC' ? 'selected="selected"' : ''; ?> value="ASC"><?php _e( 'Ascending', 'wproto' ); ?></option>
					</select>
		
				</td>
			</tr>
		</table>
	
	</div>

</div>