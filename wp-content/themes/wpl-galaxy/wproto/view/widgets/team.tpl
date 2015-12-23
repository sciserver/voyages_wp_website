<?php echo $data['args']['before_widget']; ?>

<!-- widget title -->
<?php if ( isset( $data['title'] ) ) : ?>

	<?php echo $data['args']['before_title']; ?>
	
		<?php echo $data['title']; ?>
		
	<?php echo $data['args']['after_title']; ?>
	
<?php endif; ?>

<!-- widget content -->

<?php
	global $wpl_galaxy_wp;
	$type = $data['instance']['display_categories'] == 'all' ? 'all' : 'category';
	$posts = $wpl_galaxy_wp->model->post->get( $type, $data['instance']['posts_count'], $data['instance']['display_categories'], $data['instance']['order_by'], $data['instance']['sort'], 'wproto_team', 'wproto_team_category' );
?>

<?php if( $posts->have_posts() ): ?>

	<div class="items">
		<?php while( $posts->have_posts() ): $posts->the_post(); ?>
		
		<?php
			$custom_fields = get_post_custom();
			$has_thumb = has_post_thumbnail();
		?>
		
		<div class="item">
						
			<div class="image <?php if( !$has_thumb): ?>no-image<?php endif; ?>">
			
				<?php if( $has_thumb ): ?>
				
				<?php 
					$thumb = wpl_galaxy_wp_utils::is_retina() ? 'photo-small-2x' : 'photo-small';
					$image = wp_get_attachment_image_src( get_post_thumbnail_id( get_the_ID() ), $thumb );
				?>
				<img src="<?php echo $image[0]; ?>" width="70" alt="" />
				<?php endif; ?>
				
				<div class="name">
								
					<a class="title"><?php the_title(); ?></a>
					
					<?php if( isset( $custom_fields['twitter_url'][0] ) && $custom_fields['twitter_url'][0] <> '' ): ?>
					<a href="<?php echo $custom_fields['twitter_url'][0]; ?>"><i data-tip-gravity="s" title="Twitter" class="fa fa-twitter-square show-tooltip"></i></a>
					<?php endif; ?>
				 
				 	<?php if( isset( $custom_fields['facebook_url'][0] ) && $custom_fields['facebook_url'][0] <> '' ): ?>
					<a href="<?php echo $custom_fields['facebook_url'][0]; ?>"><i data-tip-gravity="s" title="Facebook" class="fa fa-facebook-square show-tooltip"></i></a>
					<?php endif; ?>
					
					<?php if( isset( $custom_fields['linkedin_url'][0] ) && $custom_fields['linkedin_url'][0] <> '' ): ?> 
					<a href="<?php echo $custom_fields['linkedin_url'][0]; ?>"><i data-tip-gravity="s" title="Linkedin" class="fa fa-linkedin-square show-tooltip"></i></a>
					<?php endif; ?>
								
				</div>
							
			</div>
							
			<dl>
				<?php if( $data['instance']['display_position'] == 1 && isset( $custom_fields['position'][0] ) && $custom_fields['position'][0] <> '' ): ?>
				<dt><?php _e('Position', 'wproto'); ?>:</dt>
				<dd><?php echo $custom_fields['position'][0]; ?></dd>
				<?php endif; ?>
				
				<?php if( $data['instance']['display_age'] == 1 && isset( $custom_fields['age'][0] ) && $custom_fields['age'][0] <> '' ): ?>
				<dt><?php _e('Age', 'wproto'); ?>:</dt>
				<dd><?php echo $custom_fields['age'][0]; ?></dd>
				<?php endif; ?>
				
				<?php if( $data['instance']['display_experience'] == 1 && isset( $custom_fields['experience'][0] ) && $custom_fields['experience'][0] <> '' ): ?>
				<dt><?php _e('Experience', 'wproto'); ?>:</dt>
				<dd><?php echo $custom_fields['experience'][0]; ?></dd>
				<?php endif; ?>
				
			</dl>
						
		</div>
		<?php endwhile; wp_reset_query(); ?>
	</div>

<?php endif; ?>

<?php echo $data['args']['after_widget'];