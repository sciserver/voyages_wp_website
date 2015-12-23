<?php if( isset( $data['title'] ) && $data['title'] <> '' ): ?>
<h3><?php echo $data['title']; ?></h3>
<?php endif; ?>

<?php if( $data['posts']->have_posts() ): ?>

<div class="grid benefits-holder">
	
	<?php
		$cols = isset( $data['cols'] ) ? absint( $data['cols'] ) : 4;
		$cols = $cols <= 0 ? 4 : $cols;
		$col_size_human = wpl_galaxy_wp_front::get_column_name( $cols );
	?>
	
		<?php while( $data['posts']->have_posts() ): $data['posts']->the_post(); ?>
		<div class="unit <?php echo $col_size_human; ?>">

			<?php
				$id = get_the_ID();
				$icon_style = get_post_meta( $id, 'wproto_benefit_style', true );
				$link = get_post_meta( $id, 'wproto_benefit_link', true );
				$icon_style = $icon_style == '' ? 'image' : $icon_style;
				$thumb_name = wpl_galaxy_wp_utils::is_retina() ? 'benefits-icon-2x' : 'benefits-icon';
				$img = wp_get_attachment_image_src( get_post_thumbnail_id(), $thumb_name );
				$icon_name = get_post_meta( $id, 'wproto_benefit_icon_name', true );
				$animation = get_post_meta( $id, 'wproto_benefit_animation', true );
				$animation = $animation == '' ? 'bounceIn' : $animation;
				$animation_delay = get_post_meta( $id, 'wproto_benefit_animation_delay', true );
			?>

			<div data-appear-animation-delay="<?php echo $animation_delay; ?>" data-appear-animation="<?php echo $animation; ?>" class="appear-animation icon-container">
				<a href="<?php echo $link == '' ? 'javascript:;' : $link; ?>" class="icon">
					<?php if( $icon_style == 'icon' ): ?>
						<i class="<?php echo $icon_name; ?>"></i>
					<?php else: ?>
						<img width="97" height="97" src="<?php echo $img[0]; ?>" alt="" />
					<?php endif; ?>
				</a>
			</div>

			<h4><?php the_title(); ?></h4>
			<?php the_content(); ?>		

		</div>
		<?php endwhile; wp_reset_query(); ?>
</div>
<?php endif;