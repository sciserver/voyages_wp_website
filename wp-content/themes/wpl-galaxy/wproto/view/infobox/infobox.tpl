<div id="wproto-info-box-holder">
	<div id="wproto-screen-right">
		<div id="wproto-info-box">

			<div class="wproto-wp-box">
				<div class="inner">
					<h3><?php echo $data['title']; ?></h3>
					<?php echo $data['content']; ?>
					<p><img id="wproto-hide-infobix-loader" style="display: none;" src="<?php echo WPROTO_THEME_URL; ?>/images/admin/ajax-loader.gif" alt="" /></p>
				</div>
				<div class="wproto-wp-box-footer">
					<?php include 'copyright.tpl'; ?>
				</div>
			</div>
		</div>
	</div>
</div>
<script>
jQuery.noConflict()( function(){
	
	/**
		Custom info boxes at admin screen
	**/
	jQuery('#nav-menus-frame, #col-container, .wrap').addClass('wprotoAdminContainer');
	jQuery('.wprotoAdminContainer').wrap('<div id="wproto-screen-cols" />');
	jQuery('#wproto-screen-cols').wrapInner('<div id="wproto-screen-left" />');
	jQuery('#wproto-screen-cols').prepend( jQuery('#wproto-info-box-holder').html() );
	jQuery('#wproto-info-box-holder').html('');
	
});
</script>