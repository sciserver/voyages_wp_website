<?php echo $data['args']['before_widget']; ?>

<!-- widget title -->
<?php if ( isset( $data['title'] ) ) : ?>

	<?php echo $data['args']['before_title']; ?>
	
		<?php echo $data['title']; ?>
		
	<?php echo $data['args']['after_title']; ?>
	
<?php endif; ?>

<!-- widget content -->

	<?php $user = get_user_by( 'id', $data['instance']['user_id'] ); ?>

	<div class="image <?php if( $data['instance']['show_avatar'] != 1 ): ?>no-image<?php endif; ?> <?php if( $data['instance']['show_website'] != 1 ): ?>no-website<?php endif; ?> <?php if( $data['instance']['show_email'] != 1 ): ?>no-email<?php endif; ?>">
		<?php if( $data['instance']['show_avatar'] == 1 ): ?>
			<?php echo get_avatar( $user->ID, 140 ); ?>
		<?php endif; ?>
		
		<div class="name">
			<a href="<?php echo get_author_posts_url( $data['instance']['user_id'] ); ?>" class="title"><?php echo $user->display_name; ?></a>
			
			<?php if( $data['instance']['show_email'] == 1 ): ?>
			<a href="mailto:<?php echo $user->user_email; ?>"><i data-tip-gravity="s" title="E-mail" class="fa fa-envelope show-tooltip"></i></a>
			<?php endif; ?>
			
			<?php if( $data['instance']['show_website'] == 1 ): ?>
			
				<?php
					$user_meta = get_user_meta( $data['instance']['user_id'] );
					
					$dribble_url = isset( $user_meta['wproto_social_dribbble_url'][0] ) ? $user_meta['wproto_social_dribbble_url'][0] : '';
					$facebook_url = isset( $user_meta['wproto_social_facebook_url'][0] ) ? $user_meta['wproto_social_facebook_url'][0] : '';
					$flickr_url = isset( $user_meta['wproto_social_flickr_url'][0] ) ? $user_meta['wproto_social_flickr_url'][0] : '';
					$google_plus_url = isset( $user_meta['wproto_social_google_plus_url'][0] ) ? $user_meta['wproto_social_google_plus_url'][0] : '';
					$linkedin_url = isset( $user_meta['wproto_social_linkedin_url'][0] ) ? $user_meta['wproto_social_linkedin_url'][0] : '';
					$tumblr_url = isset( $user_meta['wproto_social_tumblr_url'][0] ) ? $user_meta['wproto_social_tumblr_url'][0] : '';
					$twitter_url = isset( $user_meta['wproto_social_twitter_url'][0] ) ? $user_meta['wproto_social_twitter_url'][0] : '';
					$youtube_url = isset( $user_meta['wproto_social_youtube_url'][0] ) ? $user_meta['wproto_social_youtube_url'][0] : '';
				?>
			
				<?php if( $dribble_url <> '' ): ?>
				<a href="<?php echo $dribble_url; ?>"><i data-tip-gravity="s" title="Dribble" class="fa fa-pinterest-square show-tooltip"></i></a>
				<?php endif; ?> 
				
				<?php if( $facebook_url <> '' ): ?>
				<a href="<?php echo $facebook_url; ?>"><i data-tip-gravity="s" title="Facebook" class="fa fa-facebook-square show-tooltip"></i></a>
				<?php endif; ?> 
				
				<?php if( $flickr_url <> '' ): ?>
				<a href="<?php echo $flickr_url; ?>"><i data-tip-gravity="s" title="Flickr" class="fa fa-flickr show-tooltip"></i></a>
				<?php endif; ?> 
				
				<?php if( $google_plus_url <> '' ): ?>
				<a href="<?php echo $google_plus_url; ?>"><i data-tip-gravity="s" title="Google Plus" class="fa fa-google-plus-square show-tooltip"></i></a>
				<?php endif; ?> 
				
				<?php if( $linkedin_url <> '' ): ?>
				<a href="<?php echo $linkedin_url; ?>"><i data-tip-gravity="s" title="LinkedIn" class="fa fa-linkedin-square show-tooltip"></i></a>
				<?php endif; ?> 
				
				<?php if( $tumblr_url <> '' ): ?>
				<a href="<?php echo $tumblr_url; ?>"><i data-tip-gravity="s" title="Tumblr" class="fa fa-tumblr-square show-tooltip"></i></a>
				<?php endif; ?> 
				
				<?php if( $twitter_url <> '' ): ?>
				<a href="<?php echo $twitter_url; ?>"><i data-tip-gravity="s" title="Twitter" class="fa fa-twitter-square show-tooltip"></i></a>
				<?php endif; ?> 
				
				<?php if( $youtube_url <> '' ): ?>
				<a href="<?php echo $youtube_url; ?>"><i data-tip-gravity="s" title="YouTube" class="fa fa-youtube-square show-tooltip"></i></a>
				<?php endif; ?> 
			
			<?php endif; ?>
			
		</div>
		
	</div>
	
	<div class="excerpt">
		<p><?php echo $user->user_description; ?></p>
	</div>

<?php echo $data['args']['after_widget'];