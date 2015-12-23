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
	$posts = $wpl_galaxy_wp->model->post->get( $type, $data['instance']['posts_count'], $data['instance']['display_categories'], $data['instance']['order_by'], $data['instance']['sort'], 'wproto_partners', 'wproto_partners_category' );
?>

<?php if( $posts->have_posts() ): ?>

	<div class="items">
		<?php while( $posts->have_posts() ): $posts->the_post(); ?>
		<div class="item">
		
			<?php if( has_post_thumbnail() ): ?>
			<div class="thumbnail">
				<?php 
					$thumb = wpl_galaxy_wp_utils::is_retina() ? 'partners-clients-logo-2x' : 'partners-clients-logo';
					$image = wp_get_attachment_image_src( get_post_thumbnail_id( get_the_ID() ), $thumb );
				?>
				<img src="<?php echo $image[0]; ?>" width="170" alt="" />
			</div>
			<?php endif; ?>

		</div>
		<?php endwhile; wp_reset_query(); ?>
	</div>

<?php endif; ?>

<?php echo $data['args']['after_widget'];