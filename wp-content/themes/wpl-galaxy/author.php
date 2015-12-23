<?php
	get_header();
	global $wp_query;
	$current_author = $wp_query->get_queried_object();
	$author_metadata = get_metadata( 'user', $current_author->ID );
?>

<!-- 
	
	CONTENT SECTION
		
-->
	
<div id="content" class="wrapper">

	<header class="post-header">
		<h1 class="post-title"><?php _e('Author\'s page', 'wproto'); ?>: <?php echo $current_author->display_name; ?></h1>
		<?php wpl_galaxy_wp_front::breadcrumbs( true, ' <i class="delimeter"></i> ', true ); ?>
	</header>
	
	<div id="about-author-section">
	
		<span class="author-photo">
		<?php
			$thumb_size = wpl_galaxy_wp_utils::is_retina() ? 534 : 267;
			echo get_avatar( $current_author->ID, $thumb_size );
		?>
		</span>
					
		<div class="info">
					
			<h1><?php _e( 'Author', 'wproto'); ?>: <span><?php echo $current_author->display_name; ?></span></h1>
						
			<p><?php echo $current_author->description; ?></p>
						
			<div class="social-icons">
				<strong><?php _e( 'Social profiles', 'wproto'); ?>:</strong>
				
				<?php if( isset( $author_metadata['wproto_social_dribbble_url'][0] ) && $author_metadata['wproto_social_dribbble_url'][0] <> '' ): ?>
				<a href="<?php echo $author_metadata['wproto_social_dribbble_url'][0]; ?>" title="Dribbble" data-tip-gravity="s" class="fa fa-dribbble show-tooltip"></a>
				<?php endif; ?> 
				
				<?php if( isset( $author_metadata['wproto_social_facebook_url'][0] ) && $author_metadata['wproto_social_facebook_url'][0] <> '' ): ?>
				<a href="<?php echo $author_metadata['wproto_social_facebook_url'][0]; ?>" title="Facebook" data-tip-gravity="s" class="fa fa-facebook-square show-tooltip"></a>
				<?php endif; ?> 
				
				<?php if( isset( $author_metadata['wproto_social_flickr_url'][0] ) && $author_metadata['wproto_social_flickr_url'][0] <> '' ): ?>
				<a href="<?php echo $author_metadata['wproto_social_flickr_url'][0]; ?>" title="Flickr" data-tip-gravity="s" class="fa fa-flickr show-tooltip"></a>
				<?php endif; ?> 
				
				<?php if( isset( $author_metadata['wproto_social_google_plus_url'][0] ) && $author_metadata['wproto_social_google_plus_url'][0] <> '' ): ?>
				<a href="<?php echo $author_metadata['wproto_social_google_plus_url'][0]; ?>" title="Google Plus" data-tip-gravity="s" class="fa fa-google-plus-square show-tooltip"></a>
				<?php endif; ?> 
				
				<?php if( isset( $author_metadata['wproto_social_linkedin_url'][0] ) && $author_metadata['wproto_social_linkedin_url'][0] <> '' ): ?>
				<a href="<?php echo $author_metadata['wproto_social_linkedin_url'][0]; ?>" title="LinkedIn" data-tip-gravity="s" class="fa fa-linkedin-square show-tooltip"></a>
				<?php endif; ?> 
				
				<?php if( isset( $author_metadata['wproto_social_tumblr_url'][0] ) && $author_metadata['wproto_social_tumblr_url'][0] <> '' ): ?>
				<a href="<?php echo $author_metadata['wproto_social_tumblr_url'][0]; ?>" title="Tumblr" data-tip-gravity="s" class="fa fa-tumblr-square show-tooltip"></a>
				<?php endif; ?> 
				
				<?php if( isset( $author_metadata['wproto_social_twitter_url'][0] ) && $author_metadata['wproto_social_twitter_url'][0] <> '' ): ?>
				<a href="<?php echo $author_metadata['wproto_social_twitter_url'][0]; ?>" title="Twitter" data-tip-gravity="s" class="fa fa-twitter-square show-tooltip"></a>
				<?php endif; ?> 
				
				<?php if( isset( $author_metadata['wproto_social_youtube_url'][0] ) && $author_metadata['wproto_social_youtube_url'][0] <> '' ): ?>
				<a href="<?php echo $author_metadata['wproto_social_youtube_url'][0]; ?>" title="YouTube" data-tip-gravity="s" class="fa fa-youtube-square show-tooltip"></a>
				<?php endif; ?> 
				
			</div>
					
		</div>
				
		<h3><?php _e( 'Posted by this author', 'wproto'); ?>:</h3>
				
	</div>
	
	<?php if( ! $wp_query->have_posts() ): ?>
	<p><?php _e( 'This author has no published posts.', 'wproto'); ?></p>
	<?php else: ?>
		
		<?php
			include_once( WPROTO_THEME_DIR . '/layouts/masonry.php' );
			wpl_galaxy_wp_front::pagination( 'ajax', 'masonry', '', 'author' );
		?>
		
	<?php endif; ?>

</div>

<?php get_footer();