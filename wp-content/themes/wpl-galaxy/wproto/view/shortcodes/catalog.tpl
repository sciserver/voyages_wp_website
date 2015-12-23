<?php if( isset( $data['title'] ) && $data['title'] <> '' ): ?>
<h4><?php echo $data['title']; ?></h4>
<?php endif; ?>

<?php if( $data['posts']->have_posts() ): ?>

<div class="grid catalog-holder">
	<?php
		$cols = isset( $data['cols'] ) ? absint( $data['cols'] ) : 4;
		$cols = $cols <= 0 ? 4 : $cols;
		$col_size_human = wpl_galaxy_wp_front::get_column_name( $cols );
	?>
	
	<?php while( $data['posts']->have_posts() ): $data['posts']->the_post(); ?>
	<div class="unit <?php echo $col_size_human; ?>">
	
		<?php
			$post_id = get_the_ID();
			$old_price = get_post_meta( $post_id, 'old_price', true );
			$old_price = $old_price <> '' ? wpl_galaxy_wp_front::get_price( $old_price ) : '';
											
			$price = get_post_meta( $post_id, 'price', true );
			$price = $price <> '' ? wpl_galaxy_wp_front::get_price( $price ) : '';
											
			$link_to_buy = get_post_meta( $post_id, 'link_to_buy', true );
											
		?>
	
		<div class="item">
			<div class="image">
			
				<?php if( has_post_thumbnail() ): ?>
					<?php
						$img = wp_get_attachment_image_src( get_post_thumbnail_id(), 'post-thumb-full' );
						$img_2x = wp_get_attachment_image_src( get_post_thumbnail_id(), 'post-thumb-full-2x' );
					?>
					<img width="<?php echo $img[1]; ?>" height="<?php echo $img[2]; ?>" src="<?php echo wpl_galaxy_wp_utils::is_retina() ? $img_2x[0] : $img[0]; ?>" alt="" />
				<?php endif; ?>
				<div class="clear"></div>
				<a href="<?php the_permalink(); ?>"><span class="overlay"></span></a>
				<a class="more" href="<?php the_permalink(); ?>"><i class="fa fa-shopping-cart"></i></a>
			</div>
			
			<div class="text">
				<?php if( $old_price <> '' ): ?>
				<del class="old-price"><?php echo $old_price; ?></del>
				<?php endif; ?>
										
				<?php if( $price <> '' ): ?>
				<span class="price"><?php echo $price; ?></span>
				<?php endif; ?>
				<h6><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h6>
			</div>
		</div>
		
	</div>
	<?php endwhile; wp_reset_query(); ?>
</div>

<?php endif; ?>