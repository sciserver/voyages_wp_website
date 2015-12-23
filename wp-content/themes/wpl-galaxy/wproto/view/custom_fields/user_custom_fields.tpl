<h3><?php _e('OAuth Data', 'wproto'); ?></h3>

<table class="form-table">
	<tr>
		<th><label for="wproto-facebook-profile-id"><?php _e('Facebook Profile ID', 'wproto'); ?></label></th>
		<td>
			<input type="text" name="wproto_facebook_profile_id" id="wproto-facebook-profile-id" value="<?php echo esc_attr( get_the_author_meta( 'wproto_facebook_profile_id', $data['user']->ID ) ); ?>" class="regular-text" /><br />
		</td>
	</tr>
	<tr>
		<th><label for="wproto-google-profile-id"><?php _e('Google Profile ID', 'wproto'); ?></label></th>
		<td>
			<input type="text" name="wproto_google_profile_id" id="wproto-google-profile-id" value="<?php echo esc_attr( get_the_author_meta( 'wproto_google_profile_id', $data['user']->ID ) ); ?>" class="regular-text" /><br />
		</td>
	</tr>
</table>

<h3><?php _e('Links to social profiles', 'wproto'); ?></h3>

<table class="form-table">
	<tr>
		<th><label for="wproto_social_dribbble_url"><i class="fa-dribbble fa fa-2x"></i> <?php _e('Dribble profile URL', 'wproto'); ?></label></th>
		<td>
			<input type="text" name="wproto_social_dribbble_url" id="wproto_social_dribbble_url" value="<?php echo esc_attr( get_the_author_meta( 'wproto_social_dribbble_url', $data['user']->ID ) ); ?>" class="regular-text" /><br />
		</td>
	</tr>
	<tr>
		<th><label for="wproto_social_facebook_url"><i class="fa-facebook fa fa-2x"></i> <?php _e('Facebook profile URL', 'wproto'); ?></label></th>
		<td>
			<input type="text" name="wproto_social_facebook_url" id="wproto_social_facebook_url" value="<?php echo esc_attr( get_the_author_meta( 'wproto_social_facebook_url', $data['user']->ID ) ); ?>" class="regular-text" /><br />
		</td>
	</tr>
	<tr>
		<th><label for="wproto_social_flickr_url"><i class="fa-flickr fa fa-2x"></i> <?php _e('Flickr profile URL', 'wproto'); ?></label></th>
		<td>
			<input type="text" name="wproto_social_flickr_url" id="wproto_social_flickr_url" value="<?php echo esc_attr( get_the_author_meta( 'wproto_social_flickr_url', $data['user']->ID ) ); ?>" class="regular-text" /><br />
		</td>
	</tr>
	<tr>
		<th><label for="wproto_social_google_plus_url"><i class="fa-google-plus fa fa-2x"></i> <?php _e('Google plus profile URL', 'wproto'); ?></label></th>
		<td>
			<input type="text" name="wproto_social_google_plus_url" id="wproto_social_google_plus_url" value="<?php echo esc_attr( get_the_author_meta( 'wproto_social_google_plus_url', $data['user']->ID ) ); ?>" class="regular-text" /><br />
		</td>
	</tr>
	<tr>
		<th><label for="wproto_social_linkedin_url"><i class="fa-linkedin fa fa-2x"></i> <?php _e('LinkedIn profile URL', 'wproto'); ?></label></th>
		<td>
			<input type="text" name="wproto_social_linkedin_url" id="wproto_social_linkedin_url" value="<?php echo esc_attr( get_the_author_meta( 'wproto_social_linkedin_url', $data['user']->ID ) ); ?>" class="regular-text" /><br />
		</td>
	</tr>
	<tr>
		<th><label for="wproto_social_tumblr_url"><i class="fa-tumblr fa fa-2x"></i> <?php _e('Tumblr profile URL', 'wproto'); ?></label></th>
		<td>
			<input type="text" name="wproto_social_tumblr_url" id="wproto_social_tumblr_url" value="<?php echo esc_attr( get_the_author_meta( 'wproto_social_tumblr_url', $data['user']->ID ) ); ?>" class="regular-text" /><br />
		</td>
	</tr>
	<tr>
		<th><label for="wproto_social_twitter_url"><i class="fa-twitter fa fa-2x"></i> <?php _e('Twitter profile URL', 'wproto'); ?></label></th>
		<td>
			<input type="text" name="wproto_social_twitter_url" id="wproto_social_twitter_url" value="<?php echo esc_attr( get_the_author_meta( 'wproto_social_twitter_url', $data['user']->ID ) ); ?>" class="regular-text" /><br />
		</td>
	</tr>
	<tr>
		<th><label for="wproto_social_youtube_url"><i class="fa-youtube fa fa-2x"></i> <?php _e('YouTube profile URL', 'wproto'); ?></label></th>
		<td>
			<input type="text" name="wproto_social_youtube_url" id="wproto_social_youtube_url" value="<?php echo esc_attr( get_the_author_meta( 'wproto_social_youtube_url', $data['user']->ID ) ); ?>" class="regular-text" /><br />
		</td>
	</tr>
</table>