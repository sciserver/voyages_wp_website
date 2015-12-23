<?php if( isset( $data['title'] ) && $data['title'] <> '' ): ?>
<h4><?php echo $data['title']; ?></h4>
<?php endif; ?>

<?php if( $data['posts']->have_posts() ): ?>
<div class="grid our-team-holder">
	<?php
		$cols = isset( $data['cols'] ) ? absint( $data['cols'] ) : 4;
		$cols = $cols <= 0 ? 4 : $cols;
		$col_size_human = wpl_galaxy_wp_front::get_column_name( $cols );
		
		while( $data['posts']->have_posts() ): $data['posts']->the_post();
		
			$member_data = get_post_custom();
			$twitter_url = isset( $member_data['twitter_url'][0] ) ? $member_data['twitter_url'][0] : '';
			$facebook_url = isset( $member_data['facebook_url'][0] ) ? $member_data['facebook_url'][0] : '';
			$linkedin_url = isset( $member_data['linkedin_url'][0] ) ? $member_data['linkedin_url'][0] : '';
			$age = isset( $member_data['age'][0] ) ? $member_data['age'][0] : '';
			$position = isset( $member_data['position'][0] ) ? $member_data['position'][0] : '';
			$experience = isset( $member_data['experience'][0] ) ? $member_data['experience'][0] : '';
	?>
	<div class="unit <?php echo $col_size_human; ?>">
	
		<div class="image">
			<?php if( has_post_thumbnail() ): ?>
				<?php the_post_thumbnail('full'); ?>
			<?php endif; ?>
			<div class="clear"></div>
			<div class="overlay"></div>
			
			<div class="description">
				<?php the_content(); ?>
				<div class="clear"></div>
				<div class="social">
				<?php
					echo $twitter_url <> '' ? '<a href="' . $twitter_url . '" class="twitter"><i class="fa fa-twitter-square"></i></a>' : '';
					echo $facebook_url <> '' ? '<a href="' . $facebook_url . '" class="facebook"><i class="fa fa-facebook-square"></i></a>' : '';
					echo $linkedin_url <> '' ? '<a href="' . $linkedin_url . '" class="linkedin"><i class="fa fa-linkedin-square"></i></a>' : '';
				?>
				</div>
			</div>
			
		</div>
		
		<div class="text">
			<h6><?php the_title(); ?></h6>
			<div class="position">
				<?php 
					echo $position <> '' ? $position : '';
				?>
			</div>
			<div class="age">
				<?php echo $age <> '' ? $age . ' ' .  __( 'years old', 'wproto' ) : ''; ?>
			</div>
		</div>
	
	</div>
	<?php
		endwhile; wp_reset_query();
	?>

</div>
<?php endif; ?>