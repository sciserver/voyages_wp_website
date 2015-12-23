<?php
	$images_count = is_array( $data['images'] ) ? count( $data['images'] ) : 0; 
?>
<div id="wproto-attached-images">

	<div id="wproto-metabox-content">
		<?php
			if( $images_count > 0 ):
			foreach( $data['images'] as $id ):
			
				include 'attached_images_item.tpl';
			
			endforeach;
			endif;
		?>
		
	</div>
	<div class="clear"></div>
	
	<div id="wproto-metabox-footer">
	
		<ul>
			<li class="ib left"><a href="javascript:;" id="wproto-img-picker-add-images" class="button button-primary"><?php _e( 'Add images', 'wproto' ); ?></a></li>
			<li class="ib btn current"><span class="divider ib"></span><a href="javascript:;" class="view-button ib view-thumbs"></a></li><li class="ib btn"><span class="divider ib"></span><a href="javascript:;" class="view-button ib view-table"></a><span class="divider ib"></span></li>
			<li class="ib right"><img src="<?php echo WPROTO_THEME_URL; ?>/images/admin/ajax-loader.gif" id="wproto-list-attached-images-loader" style="display: none; vertical-align: middle;" alt="" />  
			
				<span id="wproto-attached-images-count">
				<?php if( $images_count == 1 ): ?>
					<?php _e( '1 image selected', 'wproto'); ?>
				<?php elseif( $images_count <= 0 ): ?>
					<?php _e( 'No images selected', 'wproto'); ?>
				<?php else: ?>
					<?php _e( sprintf( '%s images selected', $images_count ), 'wproto'); ?>
				<?php endif; ?>
				</span>
			
			</li>
		</ul>

	</div>
	
</div>