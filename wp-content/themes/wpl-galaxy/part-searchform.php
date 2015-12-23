<form action="<?php echo site_url(); ?>" class="search-form" method="get">
	<input type="text" placeholder="<?php _e('Search request here', 'wproto'); ?>" name="s" value="<?php echo get_query_var('s'); ?>" />
	<a href="javascript:;" class="button"><i class="fa fa-search"></i></a>
</form>
