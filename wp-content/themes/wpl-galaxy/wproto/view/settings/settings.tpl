<?php global $wpl_galaxy_wp; ?>
<div class="wrap" id="wproto-customize-screen">
	<div id="icon-themes" class="icon32"><br /></div>

	<h2 class="nav-tab-wrapper wproto-nav-tab-wrapper">
		<a data-tab-name="general-settings" class="nav-tab archive-page <?php echo !isset( $_REQUEST['wproto_tab'] ) || @$_REQUEST['wproto_tab'] == 'general-settings' ? 'nav-tab-active' : ''; ?>" href="#general-settings"><?php _e( 'General', 'wproto'); ?></a>
		<a data-tab-name="api" class="nav-tab archive-page <?php echo isset( $_REQUEST['wproto_tab'] ) && @$_REQUEST['wproto_tab'] == 'api' ? 'nav-tab-active' : ''; ?>" href="#api"><?php _e( 'API', 'wproto'); ?></a>
		<a data-tab-name="captcha" class="nav-tab archive-page <?php echo isset( $_REQUEST['wproto_tab'] ) && $_REQUEST['wproto_tab'] == 'captcha' ? 'nav-tab-active' : ''; ?>" href="#captcha"><?php _e( 'Captcha', 'wproto'); ?></a>
		<a data-tab-name="custom-modes" class="nav-tab archive-page <?php echo isset( $_REQUEST['wproto_tab'] ) && $_REQUEST['wproto_tab'] == 'custom-modes' ? 'nav-tab-active' : ''; ?>" href="#custom-modes"><?php _e( 'Custom modes', 'wproto'); ?></a>
		<a data-tab-name="custom-posts" class="nav-tab archive-page <?php echo isset( $_REQUEST['wproto_tab'] ) && $_REQUEST['wproto_tab'] == 'custom_posts' ? 'nav-tab-active' : ''; ?>" href="#custom-posts"><?php _e( 'Custom posts', 'wproto'); ?></a>
		<a data-tab-name="tools" class="nav-tab archive-page <?php echo isset( $_REQUEST['wproto_tab'] ) && $_REQUEST['wproto_tab'] == 'tools' ? 'nav-tab-active' : ''; ?>" href="#tools"><?php _e( 'Tools', 'wproto'); ?></a>
	</h2>  
	
	<?php if ( isset( $_REQUEST['updated'] ) && $_REQUEST['updated'] == true ): ?>
	<div class="updated fade"><p><strong><?php _e( 'Settings saved', 'wproto' ); ?></strong></p></div>
	<?php endif; ?>
	
	<form action="" method="post">
	
		<input type="hidden" name="wproto_tab" value="<?php echo isset( $_REQUEST['wproto_tab'] ) ? $_REQUEST['wproto_tab'] : 'general-settings'; ?>" />
		<input type="hidden" name="wproto_action" value="settings-save" />
		<input type="hidden" name="wproto_setting_action" value="settings" />
	
		<!--
	
			GENERAL SETTINGS
		
		-->
		<div class="wproto_tab" id="general-settings" <?php echo !isset( $_REQUEST['wproto_tab'] ) || @$_REQUEST['wproto_tab'] == 'general-settings' ? '' : ' style="display: none;"'; ?>>
	
			<h2><?php _e( 'Branding', 'wproto' ); ?></h2>
			
			<?php
				// get form values
				
				$retina_support = $wpl_galaxy_wp->get_option( 'retina_support', 'general' );
				$retina_support = $retina_support != NULL ? $retina_support : 'yes';
				
				$header_logo = $wpl_galaxy_wp->get_option( 'header_logo', 'general' );
				$header_logo = $header_logo != NULL ? $header_logo : 'image';
				
				$logo_type = $wpl_galaxy_wp->get_option( 'logo_type', 'general' );
				$logo_type = $logo_type != NULL ? $logo_type : 'default';
				
				$noimg = WPROTO_IS_RETINA ? WPROTO_THEME_URL . '/images/admin/noimage-2x.gif' : WPROTO_THEME_URL . '/images/admin/noimage.gif';
				$custom_logo_url = $wpl_galaxy_wp->get_option( 'custom_logo_url', 'general' );
				$custom_logo_url = $custom_logo_url <> '' ? $custom_logo_url : $noimg;
				
				$custom_logo_url_2x = $wpl_galaxy_wp->get_option( 'custom_logo_url_2x', 'general' );
				$custom_logo_url_2x = $custom_logo_url_2x <> '' ? $custom_logo_url_2x : $noimg;
				
				$site_title = get_bloginfo( 'name' );
				$site_tagline = get_bloginfo( 'description' );
				$favicon = $wpl_galaxy_wp->get_option( 'favicon', 'general' );
				$favicon_2x = $wpl_galaxy_wp->get_option( 'favicon_2x', 'general' );
			?>
			
			<table class="form-table wproto-form-table">
				<tr>
					<th><label for="wproto-header-logo-input"><?php _e( 'Header logo', 'wproto' ); ?>:</label></th>
					<td>
						<label><input class="wproto-header-logo-input" id="wproto-header-logo-input" <?php echo $header_logo == 'image' ? 'checked="checked"' : ''; ?> type="radio" name="general[header_logo]" value="image" /> <?php _e( 'Image logo', 'wproto' ); ?></label><br />
						<label><input class="wproto-header-logo-input" type="radio" name="general[header_logo]" <?php echo $header_logo == 'text' ? 'checked="checked"' : ''; ?> value="text" /> <?php _e( 'Text-based Site Title and Tagline.', 'wproto' ); ?></label><br />
					</td>
				</tr>
				<tr id="wproto-site-logo-type" <?php echo $header_logo == 'image' ? '' : ' style="display: none;"'; ?>>
					<th><label for="wproto-logo-type-input"><?php _e( 'Logo image', 'wproto' ); ?>:</label></th>
					<td>
						<label><input class="wproto-header-logo-type" id="wproto-logo-type-input" <?php echo $logo_type == 'default' ? 'checked="checked"' : ''; ?> type="radio" name="general[logo_type]" value="default" /> <?php _e( 'Default theme logo', 'wproto' ); ?></label><br />
						<label><input class="wproto-header-logo-type" type="radio" <?php echo $logo_type == 'custom' ? 'checked="checked"' : ''; ?> name="general[logo_type]" value="custom" /> <?php _e( 'Upload custom logo', 'wproto' ); ?></label><br />
					</td>
				</tr>
				<tr id="wproto-upload-custom-logo" <?php echo $logo_type == 'custom' && $header_logo == 'image' ? '' : ' style="display: none;"'; ?>>
					<th><label><?php _e( 'Custom website logo', 'wproto' ); ?>:</label></th>
					<td>
						<div style="float: left; margin-right: 25px;">
						<img src="<?php echo @$custom_logo_url; ?>" id="wproto-site-logo-image" alt="<?php _e( 'Your website logo', 'wproto' ); ?>" />
						<p>
							<input type="hidden" id="wproto-logo-url-input" name="general[custom_logo_url]" value="<?php echo $custom_logo_url; ?>" />
							<a href="javascript:;" data-url-input="#wproto-logo-url-input" data-src-target="#wproto-site-logo-image" class="button wproto-image-selector"><?php _e( 'Upload', 'wproto' ); ?></a> 
							<a href="javascript:;" data-url-input="#wproto-logo-url-input" data-src-target="#wproto-site-logo-image" data-default-img="<?php echo $noimg; ?>" class="button wproto-image-remover"><?php _e( 'Remove logo', 'wproto' ); ?></a>
							<br />
							<span class="description"><?php _e( 'Upload a logo for your theme.', 'wproto' ); ?></span>
						</p>
						</div>
						<?php if( $retina_support == 'yes' ): ?>
						<img src="<?php echo @$custom_logo_url_2x; ?>" id="wproto-site-logo-image-2x" alt="<?php _e( 'Your website logo', 'wproto' ); ?>" />
						<p>
							<input type="hidden" id="wproto-logo-url-input-2x" name="general[custom_logo_url_2x]" value="<?php echo $custom_logo_url_2x; ?>" />
							<a href="javascript:;" data-url-input="#wproto-logo-url-input-2x" data-src-target="#wproto-site-logo-image-2x" class="button wproto-image-selector"><?php _e( 'Upload', 'wproto' ); ?></a> 
							<a href="javascript:;" data-url-input="#wproto-logo-url-input-2x" data-src-target="#wproto-site-logo-image-2x" data-default-img="<?php echo $noimg; ?>" class="button wproto-image-remover"><?php _e( 'Remove logo', 'wproto' ); ?></a>
							<br />
							<span class="description"><?php _e( 'Hi-resolution logo website logo for Retina Displays (should have a twice size).', 'wproto' ); ?></span>
						</p>
						<?php endif; ?>
					</td>
				</tr>
				<tr id="wproto-site-title-and-tagline" <?php echo $header_logo == 'text' ? '' : ' style="display: none;"'; ?>>
					<th><label for="wproto-site-title-input"><?php _e( 'Site title and tagline', 'wproto' ); ?>:</label></th>
					<td>
						<p>
							<input type="text" id="wproto-site-title-input" class="text" name="general[site_title]" value="<?php echo $site_title; ?>" placeholder="<?php _e( 'Enter site title here', 'wproto' ); ?>" />
						</p>
						<p>
							<input type="text" class="text" name="general[site_tagline]" value="<?php echo $site_tagline; ?>" placeholder="<?php _e( 'Enter site tagline here', 'wproto' ); ?>" /><br />
							<span class="description"><?php _e( 'In a few words, explain what this site is about.', 'wproto' ); ?></span>
						</p>
					</td>
				</tr>
				<tr>
					<th><p><label for="wproto-favicon-input"><?php _e( 'Favicon', 'wproto' ); ?>:</label></p>
					<p class="description"><?php _e( sprintf( 'Upload a 16px x 16px <a href="%s" target="_blank">ico image</a> that will represent your website\'s favicon.', 'http://favicon-generator.org/' ), 'wproto' ); ?></p></th>
					<td>
						<p>
							<input type="text" id="wproto-favicon-input" class="text" name="general[favicon]" value="<?php echo @$favicon; ?>" /> <a href="javascript:;" class="button wproto-image-selector" data-url-input="#wproto-favicon-input"><?php _e( 'Upload', 'wproto' ); ?></a> <a href="javascript:;" class="button wproto-remove-favicon"><?php _e( 'Remove', 'wproto' ); ?></a><br />
							<span class="description"><?php _e( sprintf( 'Your website favicon' ), 'wproto' ); ?></span>
						</p>
						<?php if( $retina_support == 'yes' ): ?>
						<p>
							<input type="text" id="wproto-favicon-input-2x" class="text" name="general[favicon_2x]" value="<?php echo @$favicon_2x; ?>" /> <a href="javascript:;" class="button wproto-image-selector" data-url-input="#wproto-favicon-input-2x"><?php _e( 'Upload', 'wproto' ); ?></a> <a href="javascript:;" class="button wproto-remove-favicon"><?php _e( 'Remove', 'wproto' ); ?></a><br />
							<span class="description"><?php _e( sprintf( 'Your Hi-Resolution website favicon for Retina displays' ), 'wproto' ); ?></span>
						</p>
						<?php endif; ?>
					</td>
				</tr>
				<?php
					$apple_touch_57 = $wpl_galaxy_wp->get_option( 'apple_touch_icon_57x57', 'general' );
					$apple_touch_114 = $wpl_galaxy_wp->get_option( 'apple_touch_icon_114x114', 'general' );
					$apple_touch_72 = $wpl_galaxy_wp->get_option( 'apple_touch_icon_72x72', 'general' );
					$apple_touch_144 = $wpl_galaxy_wp->get_option( 'apple_touch_icon_144x144', 'general' );
				?>
				<tr>
					<th><p><label for="wproto-apple-touch-input"><?php _e( 'Apple touch icons', 'wproto' ); ?>:</label></p></th>
					<td>
						<p>
							<input type="text" id="wproto-apple-touch-input-57" class="text" name="general[apple_touch_icon_57x57]" value="<?php echo @$apple_touch_57; ?>" /> <a href="javascript:;" class="button wproto-image-selector" data-url-input="#wproto-apple-touch-input-57"><?php _e( 'Upload', 'wproto' ); ?></a> <a href="javascript:;" class="button wproto-remove-favicon"><?php _e( 'Remove', 'wproto' ); ?></a><br />
							<span class="description"><?php _e( sprintf( 'Apple touch icon 57x57 pixels (Standard iPhone)' ), 'wproto' ); ?></span>
						</p>
						<p>
							<input type="text" id="wproto-apple-touch-input-114" class="text" name="general[apple_touch_icon_114x114]" value="<?php echo @$apple_touch_114; ?>" /> <a href="javascript:;" class="button wproto-image-selector" data-url-input="#wproto-apple-touch-input-114"><?php _e( 'Upload', 'wproto' ); ?></a> <a href="javascript:;" class="button wproto-remove-favicon"><?php _e( 'Remove', 'wproto' ); ?></a><br />
							<span class="description"><?php _e( sprintf( 'Apple touch icon 114x114 pixels (Retina iPhone)' ), 'wproto' ); ?></span>
						</p>
						<p>
							<input type="text" id="wproto-apple-touch-input-72" class="text" name="general[apple_touch_icon_72x72]" value="<?php echo @$apple_touch_72; ?>" /> <a href="javascript:;" class="button wproto-image-selector" data-url-input="#wproto-apple-touch-input-72"><?php _e( 'Upload', 'wproto' ); ?></a> <a href="javascript:;" class="button wproto-remove-favicon"><?php _e( 'Remove', 'wproto' ); ?></a><br />
							<span class="description"><?php _e( sprintf( 'Apple touch icon 72x72 pixels (Standard iPad)' ), 'wproto' ); ?></span>
						</p>
						<p>
							<input type="text" id="wproto-apple-touch-input-144" class="text" name="general[apple_touch_icon_144x144]" value="<?php echo @$apple_touch_144; ?>" /> <a href="javascript:;" class="button wproto-image-selector" data-url-input="#wproto-apple-touch-input-144"><?php _e( 'Upload', 'wproto' ); ?></a> <a href="javascript:;" class="button wproto-remove-favicon"><?php _e( 'Remove', 'wproto' ); ?></a><br />
							<span class="description"><?php _e( sprintf( 'Apple touch icon 144x144 pixels (Retina iPad)' ), 'wproto' ); ?></span>
						</p>
					</td>
				</tr>
			</table>
	
			<h2><?php _e( 'Misc', 'wproto' ); ?></h2>
			
			<?php
				// get form values
				
				$contacts_page_id = $wpl_galaxy_wp->get_option( 'contacts_page_id' );
				$contacts_page_id = $contacts_page_id != NULL ? $contacts_page_id : 0;
				
				$icomoon_enabled = $wpl_galaxy_wp->get_option( 'icomoon_enabled' );
				$icomoon_enabled = $icomoon_enabled != NULL ? $icomoon_enabled : 'no';
				
				$rss_enabled = $wpl_galaxy_wp->get_option( 'rss_enabled', 'general' );
				$rss_enabled = $rss_enabled != NULL ? $rss_enabled : 'yes';
				
				$hide_infobox = $wpl_galaxy_wp->get_option( 'hide_infobox', 'general' );
				$hide_infobox = $hide_infobox != NULL ? $hide_infobox : 'no';
				
				$hide_adminbar_for_non_admins = $wpl_galaxy_wp->get_option( 'hide_adminbar_for_non_admins' );
				$hide_adminbar_for_non_admins = $hide_adminbar_for_non_admins != NULL ? $hide_adminbar_for_non_admins : 'no';
				
				$hide_author_info = $wpl_galaxy_wp->get_option( 'hide_author_info' );
				$hide_author_info = $hide_author_info != NULL ? $hide_author_info : 'no';
				
				$rss_display_thumbs = $wpl_galaxy_wp->get_option( 'rss_display_thumbs', 'general' );
				$rss_display_thumbs = $rss_display_thumbs != NULL ? $rss_display_thumbs : 'no';
				
				$display_breadcrumbs = $wpl_galaxy_wp->get_option( 'display_breadcrumbs', 'general' );
				$display_breadcrumbs = $display_breadcrumbs != NULL ? $display_breadcrumbs : 'yes';
				
				$display_gotop = $wpl_galaxy_wp->get_option( 'display_gotop', 'general' );
				$display_gotop = $display_gotop != NULL ? $display_gotop : 'yes';
				
				$copyright_text = $wpl_galaxy_wp->get_option( 'copyright_text', 'general' );
				$copyright_text = $copyright_text != NULL ? $copyright_text : '';
				
				$tracking_code = $wpl_galaxy_wp->get_option( 'tracking_code', 'general' );
				$tracking_code = $tracking_code != NULL ? $tracking_code : '';
				
				$show_wplab_info = $wpl_galaxy_wp->get_option( 'show_wplab_info', 'general' );
				$show_wplab_info = $show_wplab_info != NULL ? $show_wplab_info : 'no';
				
				$likes_on_posts = $wpl_galaxy_wp->get_option( 'likes_on_posts', 'general' );
				$likes_on_posts = $likes_on_posts != NULL ? $likes_on_posts : 'yes';
				
				$display_post_views_count = $wpl_galaxy_wp->get_option( 'display_post_views_count', 'general' );
				$display_post_views_count = $display_post_views_count != NULL ? $display_post_views_count : 'no';
				
				$likes_on_comments = $wpl_galaxy_wp->get_option( 'likes_on_comments', 'general' );
				$likes_on_comments = $likes_on_comments != NULL ? $likes_on_comments : 'yes';
				
				$phone_number = $wpl_galaxy_wp->get_option( 'phone_number', 'general' );
				$phone_number = $phone_number != NULL ? $phone_number : '';
				
				$catalog_currency = $wpl_galaxy_wp->get_option( 'catalog_currency', 'general' );
				$catalog_currency = $catalog_currency != NULL ? $catalog_currency : '$';
				
				$catalog_currency_display = $wpl_galaxy_wp->get_option( 'catalog_currency_display', 'general' );
				$catalog_currency_display = $catalog_currency_display != NULL ? $catalog_currency_display : 'before';
				
				$five_star_likes_count = $wpl_galaxy_wp->get_option( 'five_star_likes_count', 'general' );
				$five_star_likes_count = $five_star_likes_count != NULL ? $five_star_likes_count : 10;
				
				$common_related_posts_block = $wpl_galaxy_wp->get_option( 'common_related_posts_block', 'general' );
				$common_related_posts_block = $common_related_posts_block != NULL ? $common_related_posts_block : 'yes';
				
				$related_posts_block_title = $wpl_galaxy_wp->get_option( 'related_posts_block_title', 'general' );
				$related_posts_block_title = $related_posts_block_title != NULL ? $related_posts_block_title : __('Related posts', 'wproto');
				
				$related_posts_block_subtitle = $wpl_galaxy_wp->get_option( 'related_posts_block_subtitle', 'general' );
				$related_posts_block_subtitle = $related_posts_block_subtitle != NULL ? $related_posts_block_subtitle : __('posts can interested you and are related', 'wproto');
				
				$header_menu_scrolling = $wpl_galaxy_wp->get_option( 'header_menu_scrolling', 'general' );
				$header_menu_scrolling = $header_menu_scrolling != NULL ? $header_menu_scrolling : 'yes';

			?>
			
			<table class="form-table wproto-form-table">
				<tr>
					<th>
						<label><?php _e( 'Header menu scrolling', 'wproto' ); ?>:</label>
					</th>
					<td>
					
						<div class="field switch">
							<label class="cb-enable <?php echo $header_menu_scrolling == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Scroll', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $header_menu_scrolling == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'Do not scroll', 'wproto' ); ?></span></label>
							<input name="general[header_menu_scrolling]" type="hidden" value="<?php echo $header_menu_scrolling; ?>" />
							<div class="clear"></div>
						</div>
						
					</td>
				</tr>
				<tr>
					<th>
						<label><?php _e( 'Related posts block', 'wproto' ); ?>:</label>
						<p class="description"><?php _e( 'Block title and subtitle', 'wproto' ); ?></p>
					</th>
					<td>
					
						<div class="field switch">
							<label class="cb-enable <?php echo $common_related_posts_block == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Common for all pages', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $common_related_posts_block == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'Individual for each page', 'wproto' ); ?></span></label>
							<input data-toggle-element=".wproto-related-block-settings" name="general[common_related_posts_block]" type="hidden" value="<?php echo $common_related_posts_block; ?>" />
							<div class="clear"></div>
						</div>
						
					</td>
				</tr>
				<tr class="wproto-related-block-settings" <?php echo $common_related_posts_block == 'yes' ? '' : ' style="display: none;"'; ?>>
					<th>
						<label><?php _e( 'Related posts block title', 'wproto' ); ?>:</label>
					</th>
					<td>
					
						<input type="text" class="text" value="<?php echo $related_posts_block_title; ?>" name="general[related_posts_block_title]" />
						
					</td>
				</tr>
				<tr class="wproto-related-block-settings" <?php echo $common_related_posts_block == 'yes' ? '' : ' style="display: none;"'; ?>>
					<th>
						<label><?php _e( 'Related posts block subtitle', 'wproto' ); ?>:</label>
					</th>
					<td>
					
						<input type="text" class="text" value="<?php echo $related_posts_block_subtitle; ?>" name="general[related_posts_block_subtitle]" />
						
					</td>
				</tr>
				<tr>
					<th>
						<label><?php _e( 'Contacts page', 'wproto' ); ?>:</label>
					</th>
					<td>
					
						<?php wp_dropdown_pages( array( 'selected' => $contacts_page_id, 'name' => 'general[contacts_page_id]' ) ); ?> 
						
						<p class="description"><?php _e('This page link will be used at full-width header style', 'wproto'); ?></p>
						
					</td>
				</tr>
				<tr>
					<th style="vertical-align: middle">
						<label><?php _e( 'Retina Support', 'wproto' ); ?>:</label>
					</th>
					<td>
					
						<div class="field switch">
							<label class="cb-enable <?php echo $retina_support == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Enabled', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $retina_support == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'Disabled', 'wproto' ); ?></span></label>
							<input id="wproto-rss-enabled-input" name="general[retina_support]" type="hidden" value="<?php echo $retina_support; ?>" />
							<div class="clear"></div>
						</div>
						
						<p class="description"><?php _e('Disabling this option will reduce the space occupied by the site, but some images will be blurred at high pixel density displays.', 'wproto'); ?></p>
						
					</td>
				</tr>
				<tr>
					<th style="vertical-align: middle">
						<label><?php _e( 'Iconic Fonts', 'wproto' ); ?>:</label>
					</th>
					<td>
					
						<label><input type="checkbox" checked="checked" disabled="disabled" /> Font Awesome</label> <br />
						<label><input type="checkbox" <?php echo $icomoon_enabled == 'yes' ? 'checked="checked"' : ''; ?> value="yes" name="general[icomoon_enabled]" /> IcoMoon</label>
						
						<p class="description"><?php _e('Enabling additional font libraries will add 1200+ premium icons, but may affect site loading speed.', 'wproto'); ?></p>
						
					</td>
				</tr>
				<tr>
					<th style="vertical-align: middle"><label><?php _e( 'RSS', 'wproto' ); ?>:</label></th>
					<td>
					
						<div class="field switch">
							<label class="cb-enable <?php echo $rss_enabled == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Enabled', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $rss_enabled == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'Disabled', 'wproto' ); ?></span></label>
							<input id="wproto-rss-enabled-input" data-toggle-element="#wproto-enable-rss-thumbs" name="general[rss_enabled]" type="hidden" value="<?php echo $rss_enabled; ?>" />
							<div class="clear"></div>
						</div>

					</td>
				</tr>
				<tr id="wproto-enable-rss-thumbs" <?php echo $rss_enabled == 'yes' ? '' : ' style="display: none;"'; ?>>
					<th style="vertical-align: middle"><label><?php _e( 'Display thumbnails at RSS feed', 'wproto' ); ?>:</label></th>
					<td>
					
						<div class="field switch">
							<label class="cb-enable <?php echo $rss_display_thumbs == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $rss_display_thumbs == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input name="general[rss_display_thumbs]" type="hidden" value="<?php echo $rss_display_thumbs; ?>" />
							<div class="clear"></div>
						</div>

					</td>
				</tr>
				<tr>
					<th style="vertical-align: middle"><label><?php _e( 'Hide Infobox', 'wproto' ); ?>:</label></th>
					<td>
					
						<div class="field switch">
							<label class="cb-enable <?php echo $hide_infobox == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $hide_infobox == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input id="wproto-hide-infobox-input" name="general[hide_infobox]" type="hidden" value="<?php echo $hide_infobox; ?>" />
							<div class="clear"></div>
						</div>

						<p class="description"><?php _e('Enable / Disable infobox at some admin screens', 'wproto'); ?></p>

					</td>
				</tr>
				<tr>
					<th style="vertical-align: middle"><label><?php _e( 'Do not display admin bar for logged non-admins at front-end part', 'wproto' ); ?>:</label></th>
					<td>
					
						<div class="field switch">
							<label class="cb-enable <?php echo $hide_adminbar_for_non_admins == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $hide_adminbar_for_non_admins == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input id="wproto-hide-infobox-input" name="general[hide_adminbar_for_non_admins]" type="hidden" value="<?php echo $hide_adminbar_for_non_admins; ?>" />
							<div class="clear"></div>
						</div>

					</td>
				</tr>
				<tr>
					<th style="vertical-align: middle"><label><?php _e( 'Do not display author info block after posts content', 'wproto' ); ?>:</label></th>
					<td>
					
						<div class="field switch">
							<label class="cb-enable <?php echo $hide_author_info == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $hide_author_info == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input id="wproto-hide-infobox-input" name="general[hide_author_info]" type="hidden" value="<?php echo $hide_author_info; ?>" />
							<div class="clear"></div>
						</div>

					</td>
				</tr>
				<tr>
					<th style="vertical-align: middle"><label><?php _e( 'Breadcrumbs', 'wproto' ); ?>:</label></th>
					<td>
					
						<div class="field switch">
							<label class="cb-enable <?php echo $display_breadcrumbs == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Enabled', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $display_breadcrumbs == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'Disabled', 'wproto' ); ?></span></label>
							<input name="general[display_breadcrumbs]" type="hidden" value="<?php echo $display_breadcrumbs; ?>" />
							<div class="clear"></div>
						</div>

					</td>
				</tr>
				<tr>
					<th style="vertical-align: middle"><label><?php _e( 'Likes', 'wproto' ); ?>:</label></th>
					<td>
					
						<p><label><input <?php echo $likes_on_posts == 'yes' ? 'checked="checked"' : ''; ?> type="checkbox" name="general[likes_on_posts]" value="yes" /> <?php _e( 'Enable likes on posts', 'wproto' ); ?></label></p>
						
						<p><label><input <?php echo $likes_on_comments == 'yes' ? 'checked="checked"' : ''; ?> type="checkbox" name="general[likes_on_comments]" value="yes" /> <?php _e( 'Enable likes on comments', 'wproto' ); ?></label></p>

						<p>
							<label><input type="number" name="general[five_star_likes_count]" value="<?php echo absint( $five_star_likes_count ); ?>" min="1" max="999" /> <?php _e( 'Number of likes to display 5-star rating', 'wproto' ); ?></label>
						</p>

					</td>
				</tr>
				<tr>
					<th style="vertical-align: middle"><label><?php _e( 'Display post views count at front-end part', 'wproto' ); ?>:</label></th>
					<td>

						<div class="field switch">
							<label class="cb-enable <?php echo $display_post_views_count == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $display_post_views_count == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input name="general[display_post_views_count]" type="hidden" value="<?php echo $display_post_views_count; ?>" />
							<div class="clear"></div>
						</div>

					</td>
				</tr>
				<tr>
					<th style="vertical-align: middle"><label><?php _e( 'Display "GoTop" box at bottom of the page', 'wproto' ); ?>:</label></th>
					<td>
					
						<div class="field switch">
							<label class="cb-enable <?php echo $display_gotop == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $display_gotop == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input name="general[display_gotop]" type="hidden" value="<?php echo $display_gotop; ?>" />
							<div class="clear"></div>
						</div>

					</td>
				</tr>
				<tr>
					<th><label for="wproto-phone-number"><?php _e( 'Your telephone number', 'wproto' ); ?>:</label></th>
					<td>
						<input id="wproto-phone-number" type="text" class="text" name="general[phone_number]" value="<?php echo esc_textarea( $phone_number ); ?>" /><br />
						<span class="description"><?php _e( 'Phone number will be displayed at header sticker', 'wproto' ); ?></span>
					</td>
				</tr>
				<tr>
					<th><label for="wproto-copyrights-input"><?php _e( 'Copyright', 'wproto' ); ?>:</label></th>
					<td>
						<textarea id="wproto-copyrights-input" class="textarea" name="general[copyright_text]"><?php echo esc_textarea( $copyright_text ); ?></textarea><br />
						<span class="description"><?php _e( 'Your copyright information', 'wproto' ); ?></span>
					</td>
				</tr>
				<tr>
					<th><label for="wproto-tracking-code-input"><?php _e( 'Tracking code', 'wproto' ); ?>:</label></th>
					<td>
						<textarea id="wproto-tracking-code-input" class="textarea" name="general[tracking_code]"><?php echo esc_textarea( $tracking_code ); ?></textarea><br />
						<span class="description"><?php _e( 'Paste your Google Analytics (or other) tracking code here. This will be added into the footer template of your theme.', 'wproto' ); ?></span>
					</td>
				</tr>
				<tr>
					<th><label for="wproto-catalog-currency"><?php _e( 'Catalog currency', 'wproto' ); ?>:</label></th>
					<td>
						<input id="wproto-catalog-currency" type="text" class="text" name="general[catalog_currency]" value="<?php echo esc_textarea( $catalog_currency ); ?>" /><br />
						<span class="description"><?php _e( 'Currency name, like $', 'wproto' ); ?></span>
					</td>
				</tr>
				<tr>
					<th><label><?php _e( 'Display currency', 'wproto' ); ?>:</label></th>
					<td>
						<label><input <?php echo $catalog_currency_display == '' || $catalog_currency_display == 'before' ? 'checked="checked"' : ''; ?> type="radio" name="general[catalog_currency_display]" value="before" /> <?php _e( 'Before price', 'wproto' ); ?></label><br />
						<label><input <?php echo $catalog_currency_display == 'after' ? 'checked="checked"' : ''; ?> type="radio" name="general[catalog_currency_display]" value="after" /> <?php _e( 'After price', 'wproto' ); ?></label>
					</td>
				</tr>
				<tr>
					<th class="yesno-input"><label><?php _e( 'Give credits to WPlab', 'wproto' ); ?>:</label></th>
					<td>
					
						<div class="field switch">
							<label class="cb-enable <?php echo $show_wplab_info == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $show_wplab_info == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input id="wproto-show-wplab-credits" data-toggle-element="#wplab-thanks" name="general[show_wplab_info]" type="hidden" value="<?php echo $show_wplab_info; ?>" />
							<div class="clear"></div>
							<strong id="wplab-thanks" <?php echo $show_wplab_info == 'yes' ? '' : ' style="display: none;"'; ?>><?php _e( 'Thank you so much!', 'wproto' ); ?></strong>
						</div>
					
						
					</td>
				</tr>
			</table>
			
			<h2><?php _e( 'Social', 'wproto' ); ?></h2>

			<?php
				// get form values
				
				$dribble_url = $wpl_galaxy_wp->get_option( 'dribble_url', 'general' );
				$facebook_url = $wpl_galaxy_wp->get_option( 'facebook_url', 'general' );
				$flickr_url = $wpl_galaxy_wp->get_option( 'flickr_url', 'general' );
				$google_url = $wpl_galaxy_wp->get_option( 'google_url', 'general' );
				$linkedin_url = $wpl_galaxy_wp->get_option( 'linkedin_url', 'general' );
				$tumblr_url = $wpl_galaxy_wp->get_option( 'tumblr_url', 'general' );
				$twitter_url = $wpl_galaxy_wp->get_option( 'twitter_url', 'general' );
				$youtube_url = $wpl_galaxy_wp->get_option( 'youtube_url', 'general' );
				
				$instagram_url = $wpl_galaxy_wp->get_option( 'instagram_url', 'general' );
				$pinterest_url = $wpl_galaxy_wp->get_option( 'pinterest_url', 'general' );

			?>

			<table class="form-table wproto-form-table">
				<tr class="wproto-social-tr">
					<th><label><?php _e( 'Display social icons', 'wproto' ); ?>:</label></th>
					<td>
						<p class="wproto-social-input">
							<span class="i"><i class="fa-dribbble fa fa-2x"></i></span><input name="general[dribble_url]" placeholder="<?php _e( 'Paste your Dribble profile URL here', 'wproto' ); ?>" type="text" value="<?php echo @$dribble_url; ?>" class="text dribble" />
						</p>
						<p class="wproto-social-input">
							<span class="i"><i class="fa-facebook fa fa-2x"></i></span><input name="general[facebook_url]" placeholder="<?php _e( 'Paste your Facebook profile URL here', 'wproto' ); ?>" type="text" value="<?php echo @$facebook_url; ?>" class="text facebook" />
						</p>
						<p class="wproto-social-input">
							<span class="i"><i class="fa-flickr fa fa-2x"></i></span><input name="general[flickr_url]" placeholder="<?php _e( 'Paste your Flickr profile URL here', 'wproto' ); ?>" type="text" value="<?php echo @$flickr_url; ?>" class="text flickr" />
						</p>
						<p class="wproto-social-input">
							<span class="i"><i class="fa-google-plus fa fa-2x"></i></span><input name="general[google_url]" placeholder="<?php _e( 'Paste your Google profile URL here', 'wproto' ); ?>" type="text" value="<?php echo @$google_url; ?>" class="text google" />
						</p>
						<p class="wproto-social-input">
							<span class="i"><i class="fa-linkedin fa fa-2x"></i></span><input name="general[linkedin_url]" placeholder="<?php _e( 'Paste your LinkedIn profile URL here', 'wproto' ); ?>" type="text" value="<?php echo @$linkedin_url; ?>" class="text linkedin" />
						</p>
						<p class="wproto-social-input">
							<span class="i"><i class="fa-tumblr fa fa-2x"></i></span><input name="general[tumblr_url]" placeholder="<?php _e( 'Paste your Tumblr profile URL here', 'wproto' ); ?>" type="text" value="<?php echo @$tumblr_url; ?>" class="text tumbrl" />
						</p>
						<p class="wproto-social-input">
							<span class="i"><i class="fa-twitter fa fa-2x"></i></span><input name="general[twitter_url]" placeholder="<?php _e( 'Paste your Twitter profile URL here', 'wproto' ); ?>" type="text" value="<?php echo @$twitter_url; ?>" class="text twitter" />
						</p>
						<p class="wproto-social-input">
							<span class="i"><i class="fa-youtube fa fa-2x"></i></span><input name="general[youtube_url]" placeholder="<?php _e( 'Paste your YouTube profile URL here', 'wproto' ); ?>" type="text" value="<?php echo @$youtube_url; ?>" class="text youtube" />
						</p>
						
						<p class="wproto-social-input">
							<span class="i"><i class="fa-instagram fa fa-2x"></i></span><input name="general[instagram_url]" placeholder="<?php _e( 'Paste your Instagram profile URL here', 'wproto' ); ?>" type="text" value="<?php echo @$instagram_url; ?>" class="text" />
						</p>
						<p class="wproto-social-input">
							<span class="i"><i class="fa-pinterest-square fa fa-2x"></i></span><input name="general[pinterest_url]" placeholder="<?php _e( 'Paste your Pinterest profile URL here', 'wproto' ); ?>" type="text" value="<?php echo @$pinterest_url; ?>" class="text" />
						</p>
				
					</td>
				</tr>
				<?php
					$shared_buttons_code = $wpl_galaxy_wp->get_option( 'shared_buttons_code', 'general' );
				?>
				<tr>
					<th><label for="wproto-tracking-code-input"><?php _e( 'Share buttons code', 'wproto' ); ?>:</label></th>
					<td>
						<textarea id="wproto-tracking-code-input" class="textarea" name="general[shared_buttons_code]"><?php echo esc_textarea( $shared_buttons_code ); ?></textarea><br />
						<span class="description"><?php printf( __( 'Paste your <a href="%s" target="_blank">share buttons code</a> here. This code will be added before the comments list instead of default share buttons.', 'wproto' ), 'http://www.sharethis.com/' ); ?></span>
					</td>
				</tr>
			</table>
			
			<p>
				<input type="submit" class="button button-primary" value="<?php _e( 'Save settings', 'wproto' ); ?>" />
			</p>
	
		</div>
	
		<!--
	
			API
		
		-->
		<div class="wproto_tab" id="api" <?php echo isset( $_REQUEST['wproto_tab'] ) && @$_REQUEST['wproto_tab'] == 'api' ? '' : ' style="display: none;"'; ?>>
	
		<h2><?php _e( 'API Settings', 'wproto' ); ?></h2>
				
			<?php
				// get form values
				$google_api_key = $wpl_galaxy_wp->get_option( 'google_api_key' );
				
				$enable_google_oauth = $wpl_galaxy_wp->get_option( 'enable_google_oauth' );
				$enable_google_oauth = $enable_google_oauth != NULL ? $enable_google_oauth : 'no';
				
				$google_client_id = $wpl_galaxy_wp->get_option( 'google_client_id');
				$google_client_secret = $wpl_galaxy_wp->get_option( 'google_client_secret' );
				
				$enable_facebook_oauth = $wpl_galaxy_wp->get_option( 'enable_facebook_oauth' );
				$enable_facebook_oauth = $enable_facebook_oauth != NULL ? $enable_facebook_oauth : 'no';
				
				$facebook_client_id = $wpl_galaxy_wp->get_option( 'facebook_client_id' );
				$facebook_client_secret = $wpl_galaxy_wp->get_option( 'facebook_client_secret' );
			?>

		<h3>Google</h3>
				
		<table class="form-table wproto-form-table">
			<tr>
				<th>
					<label for="wproto-google-api-input"><?php _e( 'Google API key', 'wproto' ); ?>:</label>
					<br /><span class="description"><?php _e( 'Will be used to get Google Fonts', 'wproto' ); ?></span>
				</th>
				<td>
					<p>
						<input type="text" id="wproto-google-api-input" class="text" name="general[google_api_key]" value="<?php echo $google_api_key; ?>" />
						<br />
						<span class="description"><?php _e( sprintf( 'You can setup your Google key at <a href="%s" target="_blank">this page</a>.', 'https://code.google.com/apis/console' ), 'wproto' ); ?></span>
					</p>
				</td>
			</tr>
			<tr>
				<th>
					<label for="wproto-enable-gooble-input"><?php _e( 'Enable Google OAuth', 'wproto' ); ?>:</label>
					<br /><span class="description"><?php _e( 'Anyone will be able to login / signup with Google Account', 'wproto' ); ?></span>
				</th>
				<td>
						<div class="field switch">
							<label class="cb-enable <?php echo $enable_google_oauth == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $enable_google_oauth == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input id="wproto-enable-google-input" data-toggle-element="tr.wproto-google-oauth-fields" name="general[enable_google_oauth]" type="hidden" value="<?php echo $enable_google_oauth; ?>" />
							<div class="clear"></div>
						</div>
				</td>
			</tr>
			<tr <?php echo $enable_google_oauth == 'no' ? 'style="display: none"' : ''; ?> class="wproto-google-oauth-fields">
				<th>
					<label for="wproto-google-client-id-input"><?php _e( 'Google Client ID', 'wproto' ); ?>:</label>
					<br /><span class="description"><?php _e( 'Will be used for authentication with Google Account', 'wproto' ); ?></span>
				</th>
				<td>
					<p>
						<input type="text" id="wproto-google-client-id-input" class="text" name="general[google_client_id]" value="<?php echo $google_client_id; ?>" />
						<br />
						<span class="description"><?php _e( sprintf( 'You can setup your Google Client ID at <a href="%s" target="_blank">this page</a>.', 'https://code.google.com/apis/console' ), 'wproto' ); ?></span>
					</p>
				</td>
			</tr>
			<tr <?php echo $enable_google_oauth == 'no' ? 'style="display: none"' : ''; ?> class="wproto-google-oauth-fields">
				<th>
					<label for="wproto-google-client-secret-input"><?php _e( 'Google Client Secret', 'wproto' ); ?>:</label>
					<br /><span class="description"><?php _e( 'Will be used for authentication with Google Account', 'wproto' ); ?></span>
				</th>
				<td>
					<p>
						<input type="text" id="wproto-google-client-secret-input" class="text" name="general[google_client_secret]" value="<?php echo $google_client_secret; ?>" />
						<br />
						<span class="description"><?php _e( sprintf( 'You can setup your Google Client Secret at <a href="%s" target="_blank">this page</a>.', 'https://code.google.com/apis/console' ), 'wproto' ); ?></span>
					</p>
				</td>
			</tr>
		</table>

		<h3>Facebook</h3>
				
		<table class="form-table wproto-form-table">
			<tr>
				<th>
					<label for="wproto-enable-facebook-input"><?php _e( 'Enable Facebook OAuth', 'wproto' ); ?>:</label>
					<br /><span class="description"><?php _e( 'Anyone will be able to login / signup with Facebook Account', 'wproto' ); ?></span>
				</th>
				<td>
						<div class="field switch">
							<label class="cb-enable <?php echo $enable_facebook_oauth == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $enable_facebook_oauth == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input id="wproto-enable-facebook-input" data-toggle-element="tr.wproto-facebook-oauth-fields" name="general[enable_facebook_oauth]" type="hidden" value="<?php echo $enable_facebook_oauth; ?>" />
							<div class="clear"></div>
						</div>
				</td>
			</tr>
			<tr <?php echo $enable_facebook_oauth == 'no' ? 'style="display: none"' : ''; ?> class="wproto-facebook-oauth-fields">
				<th>
					<label for="wproto-facebook-client-id-input"><?php _e( 'Facebook App ID', 'wproto' ); ?>:</label>
					<br /><span class="description"><?php _e( 'Will be used for authentication with Facebook Account', 'wproto' ); ?></span>
				</th>
				<td>
					<p>
						<input type="text" id="wproto-facebook-client-id-input" class="text" name="general[facebook_client_id]" value="<?php echo $facebook_client_id; ?>" />
						<br />
						<span class="description"><?php _e( sprintf( 'You can setup your Facebook App ID at <a href="%s" target="_blank">this page</a>.', 'https://developers.facebook.com/apps' ), 'wproto' ); ?></span>
					</p>
				</td>
			</tr>
			<tr <?php echo $enable_facebook_oauth == 'no' ? 'style="display: none"' : ''; ?> class="wproto-facebook-oauth-fields">
				<th>
					<label for="wproto-facebook-client-secret-input"><?php _e( 'Facebook Client Secret', 'wproto' ); ?>:</label>
					<br /><span class="description"><?php _e( 'Will be used for authentication with Facebook Account', 'wproto' ); ?></span>
				</th>
				<td>
					<p>
						<input type="text" id="wproto-facebook-client-secret-input" class="text" name="general[facebook_client_secret]" value="<?php echo $facebook_client_secret; ?>" />
						<br />
						<span class="description"><?php _e( sprintf( 'You can setup your Facebook Client Secret at <a href="%s" target="_blank">this page</a>.', 'https://developers.facebook.com/apps' ), 'wproto' ); ?></span>
					</p>
				</td>
			</tr>
		</table>
			
		<p>
			<input type="submit" class="button button-primary" value="<?php _e( 'Save settings', 'wproto' ); ?>" />
		</p>
	
		</div>
	
		<!--
	
			CAPTCHA
		
		-->
		<div class="wproto_tab" id="captcha" <?php echo isset( $_REQUEST['wproto_tab'] ) && @$_REQUEST['wproto_tab'] == 'captcha' ? '' : ' style="display: none;"'; ?>>
	
			<h2><?php _e( 'Captcha settings', 'wproto' ); ?></h2>
			
			<?php
				// get form values
				
				$enable_at_comments = $wpl_galaxy_wp->get_option( 'enable_at_comments' );
				$enable_at_comments = $enable_at_comments != NULL ? $enable_at_comments : 'yes';
				
				$hide_from_logged = $wpl_galaxy_wp->get_option( 'hide_from_logged' );
				$hide_from_logged = $hide_from_logged != NULL ? $hide_from_logged : 'yes';
				
				$captcha_difficult = $wpl_galaxy_wp->get_option( 'captcha_difficult' );
				$captcha_difficult = $captcha_difficult != NULL ? $captcha_difficult : array('minus');
				
			?>
			
			<table class="form-table wproto-form-table">
				<tr>
					<th class="yesno-input"><label><?php _e( 'Display captcha at comment form', 'wproto' ); ?>:</label></th>
					<td>
						<div class="field switch">
							<label class="cb-enable <?php echo $enable_at_comments == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $enable_at_comments == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input name="general[enable_at_comments]" type="hidden" value="<?php echo $enable_at_comments; ?>" />
							<div class="clear"></div>
						</div>
					</td>
				</tr>
				<tr>
					<th class="yesno-input"><label><?php _e( 'Do not show captcha for registered users', 'wproto' ); ?>:</label></th>
					<td>
						<div class="field switch">
							<label class="cb-enable <?php echo $hide_from_logged == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $hide_from_logged == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input name="general[hide_from_logged]" type="hidden" value="<?php echo $hide_from_logged; ?>" />
							<div class="clear"></div>
						</div>
					</td>
				</tr>
				<tr>
					<th class="yesno-input"><label><?php _e( 'Arithmetic actions for captcha', 'wproto' ); ?>:</label></th>
					<td>
						<label><input value="minus" <?php echo @in_array( 'minus', $captcha_difficult ) ? 'checked="checked"' : ''; ?> type="checkbox" name="general[captcha_difficult][]" /> <?php _e( 'Minus (-)', 'wproto' ); ?></label><br />
						<label><input value="plus" <?php echo @in_array( 'plus', $captcha_difficult ) ? 'checked="checked"' : ''; ?> type="checkbox" name="general[captcha_difficult][]" /> <?php _e( 'Plus (+)', 'wproto' ); ?></label><br />
						<label><input value="division" <?php echo @in_array( 'division', $captcha_difficult ) ? 'checked="checked"' : ''; ?> type="checkbox" name="general[captcha_difficult][]" /> <?php _e( 'Division (/)', 'wproto' ); ?></label><br />
						<label><input value="multiply" <?php echo @in_array( 'multiply', $captcha_difficult ) ? 'checked="checked"' : ''; ?> type="checkbox" name="general[captcha_difficult][]" /> <?php _e( 'Multiply (*)', 'wproto' ); ?></label>
					</td>
				</tr>
			</table>
			
			<p>
				<input type="submit" class="button button-primary" value="<?php _e( 'Save settings', 'wproto' ); ?>" />
			</p>
	
		</div>
	
		<!--
	
			CUSTOM MODES
		
		-->
		<div class="wproto_tab" id="custom-modes" <?php echo isset( $_REQUEST['wproto_tab'] ) && @$_REQUEST['wproto_tab'] == 'custom-modes' ? '' : ' style="display: none;"'; ?>>
	
			<h2><?php _e( 'Maintenance mode', 'wproto' ); ?></h2>
			
			<?php
				// get form values
				$maintenance_enabled = $wpl_galaxy_wp->get_option( 'maintenance_enabled', 'general' );
				$maintenance_enabled = $maintenance_enabled != NULL ? $maintenance_enabled : 'no';
				
				$maintenance_text = $wpl_galaxy_wp->get_option( 'maintenance_text', 'general' );
				$maintenance_text = $maintenance_text != NULL ? $maintenance_text : '';
			?>
			
			<table class="form-table wproto-form-table">
				<tr>
					<th class="yesno-input"><label><?php _e( 'Enable maintenance mode', 'wproto' ); ?>:</label></th>
					<td>
						<div class="field switch">
							<label class="cb-enable <?php echo $maintenance_enabled == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $maintenance_enabled == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input name="general[maintenance_enabled]" data-toggle-element=".wproto-maintenance-mode-item" type="hidden" value="<?php echo $maintenance_enabled; ?>" />
							<div class="clear"></div>
							<span class="description"><?php _e( 'All pages of your website will be not availabled to visitors and search engines while maintenance mode is enabled.', 'wproto' ); ?></span>
						</div>
					</td>
				</tr>
				<tr class="wproto-maintenance-mode-item" <?php echo $maintenance_enabled != 'yes' ? 'style="display: none;"' : ''; ?>>
					<th><label><?php _e( 'Maintenance page text', 'wproto' ); ?>:</label></th>
					<td>
					
						<?php
							wp_editor(
    						$maintenance_text,
    						'wproto-maintenance-page-text-editor',
    						array(
      						'media_buttons' => false,
      						'textarea_name' => 'general[maintenance_text]',
     							'textarea_rows' => 8,
      						'tabindex' => 4,
									'teeny' => true,
      						'tinymce' => array(
										'theme_advanced_buttons1' => 'bold, italic',
        						'theme_advanced_buttons2' => '',
        						'theme_advanced_buttons3' => '',
        						'theme_advanced_buttons4' => ''
      						)	
    						)
							);
						?>
					
					</td>
				</tr>
			</table>
			
			<h3 class="wproto-maintenance-mode-item" <?php echo $maintenance_enabled != 'yes' ? 'style="display: none"' : ''; ?>><?php _e('Maintenance page style settings', 'wproto'); ?></h3>
				<?php
				
					$maintenance_logo = $wpl_galaxy_wp->get_option( 'maintenance_logo' );
					$maintenance_logo = $maintenance_logo != NULL ? $maintenance_logo : '';
					
					$maintenance_logo_2x = $wpl_galaxy_wp->get_option( 'maintenance_logo_2x' );
					$maintenance_logo_2x = $maintenance_logo_2x != NULL ? $maintenance_logo_2x : '';
				
					$maintenance_background = $wpl_galaxy_wp->get_option( 'maintenance_background' );
					$maintenance_background = $maintenance_background != NULL ? $maintenance_background : '';
					
					$maintenance_background_2x = $wpl_galaxy_wp->get_option( 'maintenance_background_2x' );
					$maintenance_background_2x = $maintenance_background_2x != NULL ? $maintenance_background_2x : '';
					
					$maintenance_background_repeat = $wpl_galaxy_wp->get_option( 'maintenance_background_repeat' );
					$maintenance_background_repeat = $maintenance_background_repeat != NULL ? $maintenance_background_repeat : '';
					
					$maintenance_background_h_pos = $wpl_galaxy_wp->get_option( 'maintenance_background_h_pos' );
					$maintenance_background_h_pos = $maintenance_background_h_pos != NULL ? $maintenance_background_h_pos : '';
					
					$maintenance_background_v_pos = $wpl_galaxy_wp->get_option( 'maintenance_background_v_pos' );
					$maintenance_background_v_pos = $maintenance_background_v_pos != NULL ? $maintenance_background_v_pos : '';
					
					$maintenance_background_fixed = $wpl_galaxy_wp->get_option( 'maintenance_background_fixed' );
					$maintenance_background_fixed = $maintenance_background_fixed != NULL ? $maintenance_background_fixed : 'yes';
					
					$maintenance_background_zoom = $wpl_galaxy_wp->get_option( 'maintenance_background_zoom' );
					$maintenance_background_zoom = $maintenance_background_zoom != NULL ? $maintenance_background_zoom : 'yes';
				?>
			<table class="form-table wproto-maintenance-mode-item wproto-form-table" <?php echo $maintenance_enabled != 'yes' ? 'style="display: none"' : ''; ?>>
				<tr>
					<th>
						<label><?php _e( 'Maintenance page style', 'wproto' ); ?>:</label>
					</th>
					<td>
					
						<p>
							<label><?php _e('Logo image:', 'wproto'); ?><br />
							<input type="text" id="wproto-maintenance-logo" class="text" name="general[maintenance_logo]" value="<?php echo @$maintenance_logo; ?>" /> <a href="javascript:;" class="button wproto-image-selector" data-url-input="#wproto-maintenance-logo"><?php _e( 'Upload', 'wproto' ); ?></a> 
							<a href="javascript:;" data-url-input="#wproto-maintenance-logo" class="button wproto-image-remover"><?php _e( 'Remove', 'wproto' ); ?></a></label>
						</p>
					
						<?php if( $retina_support == 'yes' ): ?>
					
							<p>
								<label><?php _e('Logo image for Retina Displays:', 'wproto'); ?> <span class="description">(<?php _e( 'image in twice size', 'wproto' ); ?>)</span><br />
								<input type="text" id="wproto-maintenance-logo-2x" class="text" name="general[maintenance_logo_2x]" value="<?php echo @$maintenance_logo_2x; ?>" /> <a href="javascript:;" class="button wproto-image-selector" data-url-input="#wproto-maintenance-logo-2x"><?php _e( 'Upload', 'wproto' ); ?></a> 
								<a href="javascript:;" data-url-input="#wproto-maintenance-logo-2x" class="button wproto-image-remover"><?php _e( 'Remove', 'wproto' ); ?></a></label>
							</p>
					
						<?php endif; ?>
					
						<p>
							<label><?php _e('Background image:', 'wproto'); ?><br />
							<input type="text" id="wproto-coming-soon-bg" class="text" name="general[maintenance_background]" value="<?php echo @$maintenance_background; ?>" /> <a href="javascript:;" class="button wproto-image-selector" data-url-input="#wproto-coming-soon-bg"><?php _e( 'Upload', 'wproto' ); ?></a> 
							<a href="javascript:;" data-url-input="#wproto-coming-soon-bg" class="button wproto-image-remover"><?php _e( 'Remove', 'wproto' ); ?></a></label>
						</p>
					
						<?php if( $retina_support == 'yes' ): ?>
					
							<p>
								<label><?php _e('Background image for Retina Displays:', 'wproto'); ?> <span class="description">(<?php _e( 'image in twice size', 'wproto' ); ?>)</span><br />
								<input type="text" id="wproto-coming-soon-bg-2x" class="text" name="general[maintenance_background_2x]" value="<?php echo @$maintenance_background_2x; ?>" /> <a href="javascript:;" class="button wproto-image-selector" data-url-input="#wproto-coming-soon-bg-2x"><?php _e( 'Upload', 'wproto' ); ?></a> 
								<a href="javascript:;" data-url-input="#wproto-coming-soon-bg-2x" class="button wproto-image-remover"><?php _e( 'Remove', 'wproto' ); ?></a></label>
							</p>
					
						<?php endif; ?>
						
						<p>
							<label>
								<?php _e('Background repeat:', 'wproto'); ?><br />
								<select name="general[maintenance_background_repeat]">
									<option value="repeat"><?php _e('Repeat horizontal and vertical','wproto'); ?></option>
									<option <?php echo $maintenance_background_repeat == 'repeat-x' ? 'selected="selected"' : ''; ?> value="repeat-x"><?php _e('Horizontal repeat','wproto'); ?></option>
									<option <?php echo $maintenance_background_repeat == 'repeat-y' ? 'selected="selected"' : ''; ?> value="repeat-y"><?php _e('Vertical repeat','wproto'); ?></option>
									<option <?php echo $maintenance_background_repeat == 'no-repeat' ? 'selected="selected"' : ''; ?> value="no-repeat"><?php _e('No repeat','wproto'); ?></option>
								</select>
							</label>
						</p>
						
						<p>
							<label>
								<?php _e('Horizontal background position:', 'wproto'); ?><br />
								<select name="general[maintenance_background_h_pos]">
									<option value="center"><?php _e('Center','wproto'); ?></option>
									<option <?php echo $maintenance_background_h_pos == 'left' ? 'selected="selected"' : ''; ?> value="left"><?php _e('Left','wproto'); ?></option>
									<option <?php echo $maintenance_background_h_pos == 'right' ? 'selected="selected"' : ''; ?> value="right"><?php _e('Right','wproto'); ?></option>
								</select>
							</label>
						</p>
						
						<p>
							<label>
								<?php _e('Vertical background position:', 'wproto'); ?><br />
								<select name="general[maintenance_background_v_pos]">
									<option value="center"><?php _e('Center','wproto'); ?></option>
									<option <?php echo $maintenance_background_v_pos == 'top' ? 'selected="selected"' : ''; ?> value="top"><?php _e('Top','wproto'); ?></option>
									<option <?php echo $maintenance_background_v_pos == 'bottom' ? 'selected="selected"' : ''; ?> value="bottom"><?php _e('Bottom','wproto'); ?></option>
								</select>
							</label>
						</p>						
						
					</td>
				</tr>
				<tr>
					<th>
						<label><?php _e('Fixed Background', 'wproto'); ?>:</label>
					</th>
					<td>
						<div class="field switch">
							<label class="cb-enable <?php echo $maintenance_background_fixed == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $maintenance_background_fixed == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input name="general[maintenance_background_fixed]" data-toggle-element="#maintenance-bg-effects" type="hidden" value="<?php echo $maintenance_background_fixed; ?>" />
							<div class="clear"></div>
						</div>				
					</td>
				</tr>
				<tr id="maintenance-bg-effects" <?php echo $maintenance_background_fixed != 'yes' ? ' style="display: none"' : ''; ?>>
					<th>
						<label><?php _e('Zoom Background Effect', 'wproto'); ?>:</label>
					</th>
					<td>
						<div class="field switch">
							<label class="cb-enable <?php echo $maintenance_background_zoom == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $maintenance_background_zoom == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input name="general[maintenance_background_zoom]" type="hidden" value="<?php echo $maintenance_background_zoom; ?>" />
							<div class="clear"></div>					
						</div>						
					</td>
				</tr>
			</table>
			
			<h2><?php _e( 'Coming soon mode', 'wproto' ); ?></h2>
			
			<?php
				// get form values
				
				$coming_soon_enabled = $wpl_galaxy_wp->get_option( 'coming_soon_enabled', 'general' );
				$coming_soon_enabled = $coming_soon_enabled != NULL ? $coming_soon_enabled : 'no';
				
				$site_opening_date = $wpl_galaxy_wp->get_option( 'site_opening_date', 'general' );
				$site_opening_date = $site_opening_date != NULL ? $site_opening_date : date( 'd M Y', strtotime( "+30 days" ) );
				
				$coming_soon_subscribe_form = $wpl_galaxy_wp->get_option( 'coming_soon_subscribe_form', 'general' );
				$coming_soon_subscribe_form = $coming_soon_subscribe_form != NULL ? $coming_soon_subscribe_form : 'yes';
				
				$coming_soon_mc_action = $wpl_galaxy_wp->get_option( 'coming_soon_mc_action', 'general' );
				$coming_soon_mc_action = $coming_soon_mc_action != NULL ? $coming_soon_mc_action : '';
				
				$coming_soon_mc_user_id = $wpl_galaxy_wp->get_option( 'coming_soon_mc_user_id', 'general' );
				$coming_soon_mc_user_id = $coming_soon_mc_user_id != NULL ? $coming_soon_mc_user_id : '';
				
				$coming_soon_mc_list_id = $wpl_galaxy_wp->get_option( 'coming_soon_mc_list_id', 'general' );
				$coming_soon_mc_list_id = $coming_soon_mc_list_id != NULL ? $coming_soon_mc_list_id : '';
				
				$coming_soon_mc_email_id = $wpl_galaxy_wp->get_option( 'coming_soon_mc_email_id', 'general' );
				$coming_soon_mc_email_id = $coming_soon_mc_email_id != NULL ? $coming_soon_mc_email_id : '';
			?>
			
			<table class="form-table wproto-form-table">
				<tr>
					<th class="yesno-input"><label><?php _e( 'Enable coming soon mode', 'wproto' ); ?>:</label></th>
					<td>
						<div class="field switch">
							<label class="cb-enable <?php echo $coming_soon_enabled == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $coming_soon_enabled == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input name="general[coming_soon_enabled]" data-toggle-element=".wproto-coming-soon-mode-item" type="hidden" value="<?php echo $coming_soon_enabled; ?>" />
							<div class="clear"></div>
							<span class="description"><?php _e( 'All pages of your website will be not availabled to visitors and search engines while coming soon mode is enabled.', 'wproto' ); ?></span>
						</div>
					</td>
				</tr>
			</table>
			<h3 <?php echo $coming_soon_enabled != 'yes' ? 'style="display: none"' : ''; ?> class="wproto-coming-soon-mode-item"><?php _e('Basic settings', 'wproto'); ?></h3>
			<table <?php echo $coming_soon_enabled != 'yes' ? 'style="display: none"' : ''; ?> class="form-table wproto-form-table wproto-coming-soon-mode-item">
				<tr>
					<th><label><?php _e( 'The planned website opening date', 'wproto' ); ?>:</label></th>
					<td>
						<input data-date-format="dd M yy" id="wproto-opening-date-picker" type="text" class="text" name="general[site_opening_date]" value="<?php echo esc_textarea( $site_opening_date ); ?>" />
						<p class="description"><?php _e( 'Day / Month / Year', 'wproto' ); ?></p>
					</td>
				</tr>
				<tr>
					<th>
						<label><?php _e( 'Show subscribe form', 'wproto' ); ?>:</label>
						<p class="description"><?php _e( sprintf( 'Read more about <a target="_blank" href="%s">MailChimp forms</a>', 'http://kb.mailchimp.com/article/can-i-host-my-own-sign-up-forms/' ), 'wproto' ); ?></p>
					</th>
					<td>
						
						<div class="field switch">
							<label class="cb-enable <?php echo $coming_soon_subscribe_form == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $coming_soon_subscribe_form == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input name="general[coming_soon_subscribe_form]" data-toggle-element="#coming-soon-mailchimp-form" type="hidden" value="<?php echo $coming_soon_subscribe_form; ?>" />
							<div class="clear"></div>
						</div>
						
						<div id="coming-soon-mailchimp-form" style="<?php echo $coming_soon_subscribe_form == 'no' ? 'display: none;' : ''; ?>">
						
							<p>
								<label><?php _e('Form action', 'wproto'); ?>:<br />
								<input class="text" placeholder="<?php _e('Enter MailChimp form action', 'wproto'); ?>" type="text" name="general[coming_soon_mc_action]" value="<?php echo $coming_soon_mc_action; ?>" /></label>
							</p>
							
							<p>
								<label><?php _e('User ID', 'wproto'); ?>:<br />
								<input class="text" placeholder="<?php _e('Enter MailChimp user ID', 'wproto'); ?>" type="text" name="general[coming_soon_mc_user_id]" value="<?php echo $coming_soon_mc_user_id; ?>" /></label>
							</p>
							
							<p>
								<label><?php _e('List ID', 'wproto'); ?>:<br />
								<input class="text" placeholder="<?php _e('Enter MailChimp list ID', 'wproto'); ?>" type="text" name="general[coming_soon_mc_list_id]" value="<?php echo $coming_soon_mc_list_id; ?>" /></label>
							</p>
							
							<p>
								<label><?php _e('"Your email" Input name', 'wproto'); ?>:<br />
								<input class="text" placeholder="<?php _e('Enter MailChimp \'Your email\' input name', 'wproto'); ?>" type="text" name="general[coming_soon_mc_email_id]" value="<?php echo $coming_soon_mc_email_id; ?>" /></label>
							</p>
						
						</div>
						
					</td>
				</tr>
			</table>
			
			<h3 class="wproto-coming-soon-mode-item" <?php echo $coming_soon_enabled != 'yes' ? 'style="display: none"' : ''; ?>><?php _e('Coming soon page style settings', 'wproto'); ?></h3>
				<?php
				
					$coming_soon_logo = $wpl_galaxy_wp->get_option( 'coming_soon_logo' );
					$coming_soon_logo = $coming_soon_logo != NULL ? $coming_soon_logo : '';
					
					$coming_soon_logo_2x = $wpl_galaxy_wp->get_option( 'coming_soon_logo_2x' );
					$coming_soon_logo_2x = $coming_soon_logo_2x != NULL ? $coming_soon_logo_2x : '';
				
					$coming_soon_background = $wpl_galaxy_wp->get_option( 'coming_soon_background' );
					$coming_soon_background = $coming_soon_background != NULL ? $coming_soon_background : '';
					
					$coming_soon_background_2x = $wpl_galaxy_wp->get_option( 'coming_soon_background_2x' );
					$coming_soon_background_2x = $coming_soon_background_2x != NULL ? $coming_soon_background_2x : '';
					
					$coming_soon_background_repeat = $wpl_galaxy_wp->get_option( 'coming_soon_background_repeat' );
					$coming_soon_background_repeat = $coming_soon_background_repeat != NULL ? $coming_soon_background_repeat : '';
					
					$coming_soon_background_h_pos = $wpl_galaxy_wp->get_option( 'coming_soon_background_h_pos' );
					$coming_soon_background_h_pos = $coming_soon_background_h_pos != NULL ? $coming_soon_background_h_pos : '';
					
					$coming_soon_background_v_pos = $wpl_galaxy_wp->get_option( 'coming_soon_background_v_pos' );
					$coming_soon_background_v_pos = $coming_soon_background_v_pos != NULL ? $coming_soon_background_v_pos : '';
					
					$coming_soon_background_fixed = $wpl_galaxy_wp->get_option( 'coming_soon_background_fixed' );
					$coming_soon_background_fixed = $coming_soon_background_fixed != NULL ? $coming_soon_background_fixed : 'yes';
					
					$coming_soon_background_zoom = $wpl_galaxy_wp->get_option( 'coming_soon_background_zoom' );
					$coming_soon_background_zoom = $coming_soon_background_zoom != NULL ? $coming_soon_background_zoom : 'yes';
				?>
			<table class="form-table wproto-coming-soon-mode-item wproto-form-table" <?php echo $coming_soon_enabled != 'yes' ? 'style="display: none"' : ''; ?>>
				<tr>
					<th>
						<label><?php _e( 'Coming soon page style', 'wproto' ); ?>:</label>
					</th>
					<td>
					
						<p>
							<label><?php _e('Logo image:', 'wproto'); ?><br />
							<input type="text" id="wproto-coming-soon-logo" class="text" name="general[coming_soon_logo]" value="<?php echo @$coming_soon_logo; ?>" /> <a href="javascript:;" class="button wproto-image-selector" data-url-input="#wproto-coming-soon-logo"><?php _e( 'Upload', 'wproto' ); ?></a> 
							<a href="javascript:;" data-url-input="#wproto-coming-soon-logo" class="button wproto-image-remover"><?php _e( 'Remove', 'wproto' ); ?></a></label>
						</p>
					
						<?php if( $retina_support == 'yes' ): ?>
					
							<p>
								<label><?php _e('Logo image for Retina Displays:', 'wproto'); ?> <span class="description">(<?php _e( 'image in twice size', 'wproto' ); ?>)</span><br />
								<input type="text" id="wproto-coming-soon-logo-2x" class="text" name="general[coming_soon_logo_2x]" value="<?php echo @$coming_soon_logo_2x; ?>" /> <a href="javascript:;" class="button wproto-image-selector" data-url-input="#wproto-coming-soon-logo-2x"><?php _e( 'Upload', 'wproto' ); ?></a> 
								<a href="javascript:;" data-url-input="#wproto-coming-soon-logo-2x" class="button wproto-image-remover"><?php _e( 'Remove', 'wproto' ); ?></a></label>
							</p>
					
						<?php endif; ?>
					
						<p>
							<label><?php _e('Background image:', 'wproto'); ?><br />
							<input type="text" id="coming_soon_background" class="text" name="general[coming_soon_background]" value="<?php echo @$coming_soon_background; ?>" /> <a href="javascript:;" class="button wproto-image-selector" data-url-input="#coming_soon_background"><?php _e( 'Upload', 'wproto' ); ?></a> 
							<a href="javascript:;" data-url-input="#coming_soon_background" class="button wproto-image-remover"><?php _e( 'Remove', 'wproto' ); ?></a></label>
						</p>
					
						<?php if( $retina_support == 'yes' ): ?>
					
							<p>
								<label><?php _e('Background image for Retina Displays:', 'wproto'); ?> <span class="description">(<?php _e( 'image in twice size', 'wproto' ); ?>)</span><br />
								<input type="text" id="coming_soon_background_2x" class="text" name="general[coming_soon_background_2x]" value="<?php echo @$coming_soon_background_2x; ?>" /> <a href="javascript:;" class="button wproto-image-selector" data-url-input="#coming_soon_background_2x"><?php _e( 'Upload', 'wproto' ); ?></a> 
								<a href="javascript:;" data-url-input="#coming_soon_background_2x" class="button wproto-image-remover"><?php _e( 'Remove', 'wproto' ); ?></a></label>
							</p>
					
						<?php endif; ?>
						
						<p>
							<label>
								<?php _e('Background repeat:', 'wproto'); ?><br />
								<select name="general[coming_soon_background_repeat]">
									<option value="repeat"><?php _e('Repeat horizontal and vertical','wproto'); ?></option>
									<option <?php echo $coming_soon_background_repeat == 'repeat-x' ? 'selected="selected"' : ''; ?> value="repeat-x"><?php _e('Horizontal repeat','wproto'); ?></option>
									<option <?php echo $coming_soon_background_repeat == 'repeat-y' ? 'selected="selected"' : ''; ?> value="repeat-y"><?php _e('Vertical repeat','wproto'); ?></option>
									<option <?php echo $coming_soon_background_repeat == 'no-repeat' ? 'selected="selected"' : ''; ?> value="no-repeat"><?php _e('No repeat','wproto'); ?></option>
								</select>
							</label>
						</p>
						
						<p>
							<label>
								<?php _e('Horizontal background position:', 'wproto'); ?><br />
								<select name="general[coming_soon_background_h_pos]">
									<option value="center"><?php _e('Center','wproto'); ?></option>
									<option <?php echo $coming_soon_background_h_pos == 'left' ? 'selected="selected"' : ''; ?> value="left"><?php _e('Left','wproto'); ?></option>
									<option <?php echo $coming_soon_background_h_pos == 'right' ? 'selected="selected"' : ''; ?> value="right"><?php _e('Right','wproto'); ?></option>
								</select>
							</label>
						</p>
						
						<p>
							<label>
								<?php _e('Vertical background position:', 'wproto'); ?><br />
								<select name="general[coming_soon_background_v_pos]">
									<option value="center"><?php _e('Center','wproto'); ?></option>
									<option <?php echo $coming_soon_background_v_pos == 'top' ? 'selected="selected"' : ''; ?> value="top"><?php _e('Top','wproto'); ?></option>
									<option <?php echo $coming_soon_background_v_pos == 'bottom' ? 'selected="selected"' : ''; ?> value="bottom"><?php _e('Bottom','wproto'); ?></option>
								</select>
							</label>
						</p>						
						
					</td>
				</tr>
				<tr>
					<th>
						<label><?php _e('Fixed Background', 'wproto'); ?>:</label>
					</th>
					<td>
						<div class="field switch">
							<label class="cb-enable <?php echo $coming_soon_background_fixed == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $coming_soon_background_fixed == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input name="general[coming_soon_background_fixed]" data-toggle-element="#coming-soon-bg-effects" type="hidden" value="<?php echo $coming_soon_background_fixed; ?>" />
							<div class="clear"></div>
						</div>				
					</td>
				</tr>
				<tr id="coming-soon-bg-effects" <?php echo $coming_soon_background_fixed != 'yes' ? ' style="display: none"' : ''; ?>>
					<th>
						<label><?php _e('Zoom Background Effect', 'wproto'); ?>:</label>
					</th>
					<td>
						<div class="field switch">
							<label class="cb-enable <?php echo $coming_soon_background_zoom == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $coming_soon_background_zoom == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input name="general[coming_soon_background_zoom]" type="hidden" value="<?php echo $coming_soon_background_zoom; ?>" />
							<div class="clear"></div>					
						</div>						
					</td>
				</tr>
			</table>
			
			<p>
				<input type="submit" class="button button-primary" value="<?php _e( 'Save settings', 'wproto' ); ?>" />
			</p>
	
		</div>
	
		<!--
	
			CUSTOM POSTS
		
		-->
		<div class="wproto_tab" id="custom-posts" <?php echo isset( $_REQUEST['wproto_tab'] ) && @$_REQUEST['wproto_tab'] == 'custom-posts' ? '' : ' style="display: none;"'; ?>>
	
			<h2><?php _e( 'Disable public custom post types', 'wproto' ); ?></h2>
			
			<?php
				// get form values
				
				$disable_video = $wpl_galaxy_wp->get_option( 'disable_video', 'general' );
				$disable_video = $disable_video != NULL ? $disable_video : 'no';
				
				$disable_photoalbums = $wpl_galaxy_wp->get_option( 'disable_photoalbums', 'general' );
				$disable_photoalbums = $disable_photoalbums != NULL ? $disable_photoalbums : 'no';
				
				$disable_catalog = $wpl_galaxy_wp->get_option( 'disable_catalog', 'general' );
				$disable_catalog = $disable_catalog != NULL ? $disable_catalog : 'no';
				
				$disable_portfolio = $wpl_galaxy_wp->get_option( 'disable_portfolio', 'general' );
				$disable_portfolio = $disable_portfolio != NULL ? $disable_portfolio : 'no';
				
			?>
			
			<table class="form-table wproto-form-table">
				<tr>
					<th class="yesno-input"><label><?php _e( 'Disable Videos', 'wproto' ); ?>:</label></th>
					<td>
						<div class="field switch">
							<label class="cb-enable <?php echo $disable_video == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $disable_video == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input name="general[disable_video]" type="hidden" value="<?php echo $disable_video; ?>" />
							<div class="clear"></div>
						</div>
					</td>
				</tr>
				<tr>
					<th class="yesno-input"><label><?php _e( 'Disable Photo Albums', 'wproto' ); ?>:</label></th>
					<td>
						<div class="field switch">
							<label class="cb-enable <?php echo $disable_photoalbums == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $disable_photoalbums == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input name="general[disable_photoalbums]" type="hidden" value="<?php echo $disable_photoalbums; ?>" />
							<div class="clear"></div>
						</div>
					</td>
				</tr>
				<tr>
					<th class="yesno-input"><label><?php _e( 'Disable Catalog', 'wproto' ); ?>:</label></th>
					<td>
						<div class="field switch">
							<label class="cb-enable <?php echo $disable_catalog == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $disable_catalog == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input name="general[disable_catalog]" type="hidden" value="<?php echo $disable_catalog; ?>" />
							<div class="clear"></div>
						</div>
					</td>
				</tr>
				<tr>
					<th class="yesno-input"><label><?php _e( 'Disable Portfolio', 'wproto' ); ?>:</label></th>
					<td>
						<div class="field switch">
							<label class="cb-enable <?php echo $disable_portfolio == 'yes' ? 'selected' : ''; ?>"><span><?php _e( 'Yes', 'wproto' ); ?></span></label>
							<label class="cb-disable <?php echo $disable_portfolio == 'no' ? 'selected' : ''; ?>"><span><?php _e( 'No', 'wproto' ); ?></span></label>
							<input name="general[disable_portfolio]" type="hidden" value="<?php echo $disable_portfolio; ?>" />
							<div class="clear"></div>
						</div>
					</td>
				</tr>
			</table>
			
			<p>
				<input type="submit" class="button button-primary" value="<?php _e( 'Save settings', 'wproto' ); ?>" />
			</p>
	
		</div>
	
	
		<!--
	
			TOOLS
		
		-->
		<div class="wproto_tab" id="tools" <?php echo isset( $_REQUEST['wproto_tab'] ) && @$_REQUEST['wproto_tab'] == 'tools' ? '' : ' style="display: none;"'; ?>>
	
			<h2><?php _e( 'Demo Data', 'wproto' ); ?></h2>
			
			<table class="form-table wproto-form-table">
				<tr>
					<th><label class="description"><?php _e( 'Click the button to import some demo data if you don\'t want to read documentation and you need a help :)', 'wproto' ); ?></label></th>
					<td>
						<p class="description"><?php _e( 'To start this operation, just click the button below.', 'wproto' ); ?></p>
						<p>
							<a href="javascript:;" id="wproto-install-sample-data" class="button wproto-green"><i class="fa fa-book"></i> <?php _e( 'Install Sample Data', 'wproto' ); ?></a>
						</p>
						<div id="wproto-install-sample-data-results" class="infodiv" style="display: none;">
							<p style="margin-bottom: 3px !important;"><img src="<?php echo WPROTO_THEME_URL; ?>/images/admin/ajax-loader@2x.gif" width="16" alt="" /> <?php _e( 'Please wait... It takes some time, so do not refresh this window until operation will be completed.', 'wproto' ); ?></p>
						</div>
					</td>
				</tr>
			</table>
	
			<h2><?php _e( 'Thumbnails Rebuild', 'wproto' ); ?></h2>
			
			<table class="form-table wproto-form-table">
				<tr>
					<th><label class="description"><?php _e( 'If you migrated from another wordpress theme, you need to regenerate existing thumbnails images.', 'wproto' ); ?></label></th>
					<td>
						<p class="description"><?php _e( 'To start this operation, just click the button below.', 'wproto' ); ?></p>
						<p>
							<a href="javascript:;" id="wproto-rebuild-all-thumbs" class="button"><?php _e( 'Rebuild all thumbnails', 'wproto' ); ?></a>
						</p>
						<div id="wproto-regenerate-results" class="infodiv" style="display: none;">
							<p style="margin-bottom: 3px !important;"><?php _e( 'Rebuilding 1 of 8', 'wproto' ); ?></p>
						</div>
					</td>
				</tr>
			</table>
			
			<h2><?php _e( 'Flush rewrite rules', 'wproto' ); ?></h2>
			
			<table class="form-table wproto-form-table">
				<tr>
					<th><label class="description"><?php _e( 'Update rewrite rules, if you have troubles with custom post types.', 'wproto' ); ?></label></th>
					<td>
						<p class="description"><?php _e( 'To start this operation, just click the button below.', 'wproto' ); ?></p>
						<p>
							<a href="javascript:;" id="wproto-flush-rewrite-rules" class="button"><?php _e( 'Flush rewrite rules', 'wproto' ); ?></a>
						</p>
						<div id="wproto-flush-results" class="infodiv" style="display: none;">
							<p style="margin-bottom: 3px !important;"><?php _e( 'Flushing...', 'wproto' ); ?></p>
						</div>
					</td>
				</tr>
			</table>
			
			<h2><?php _e( 'Grab Google Fonts', 'wproto' ); ?></h2>
			
			<table class="form-table wproto-form-table">
				<tr>
					<th><label class="description"><?php _e( 'To improve performance we cache list of Google fonts locally. As new fonts will be availabled at Google, you can download the new fonts list by clicking on the button at right. You need to enter Google API key at "Social" settings tab to get this data.', 'wproto' ); ?></label></th>
					<td>
						<p class="description"><?php _e( 'To start this operation, just click the button below.', 'wproto' ); ?></p>
						<p>
							<a href="javascript:;" id="wproto-grab-google-fonts" class="button"><?php _e( 'Grab google fonts list', 'wproto' ); ?></a>
						</p>
						<div id="wproto-google-fonts-grab-results" class="infodiv" style="display: none;">
							<p style="margin-bottom: 3px !important;"><img width="16" height="16" id="wproto-grab-google-fonts-loader" src="<?php echo WPROTO_THEME_URL; ?>/images/admin/ajax-loader<?php echo WPROTO_IS_RETINA ? '@2x' : ''; ?>.gif" alt="" /> <span><?php _e( 'Grabbing...', 'wproto' ); ?></span></p>
						</div>
					</td>
				</tr>
			</table>
			
			<h2><?php _e( 'Custom CSS code', 'wproto' ); ?></h2>
			
			<?php
				// get form values
				$custom_css = $wpl_galaxy_wp->get_option( 'custom_css', 'general' );
				$custom_css = $custom_css != NULL ? $custom_css : '';
			?>
			
			<table class="form-table wproto-form-table">
				<tr>
					<th><label><?php _e( 'Quickly add some CSS to your theme by adding it to this block.', 'wproto' ); ?>:</label></th>
					<td>
						<textarea id="wproto-tabbed" name="general[custom_css]"><?php echo $custom_css <> '' ? esc_textarea( $custom_css ) : ".my_custom_class {\r\n\tfont-size: 2em;\r\n}"; ?></textarea>
					</td>
				</tr>
			</table>
			
			<p>
				<input type="submit" class="button button-primary" value="<?php _e( 'Save settings', 'wproto' ); ?>" />
			</p>
	
		</div>
		
	</form>
	
</div>