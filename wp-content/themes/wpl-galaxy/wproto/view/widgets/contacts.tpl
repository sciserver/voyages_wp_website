<?php echo $data['args']['before_widget']; ?>

<!-- widget title -->
<?php if ( isset( $data['title'] ) ) : ?>

	<?php echo $data['args']['before_title']; ?>
	
		<?php echo $data['title']; ?>
		
	<?php echo $data['args']['after_title']; ?>
	
<?php endif; ?>

<!-- widget content -->

<?php if( isset( $data['instance']['free_text'] ) && $data['instance']['free_text'] <> '' ): ?>
<div class="free_text">
	<?php echo $data['instance']['free_text']; ?>
</div>
<?php endif; ?>

<?php if( isset( $data['instance']['address'] ) && $data['instance']['address'] <> '' ): ?>
<address class="address">
	<i class="fa fa-map-marker"></i> <?php echo $data['instance']['address']; ?>
</address>
<?php endif; ?>

<?php if( isset( $data['instance']['phone'] ) && $data['instance']['phone'] <> '' ): ?>
<div class="phone">
	<i class="fa fa-phone"></i> <a href="tel:<?php echo $data['instance']['phone']; ?>"><?php echo $data['instance']['phone']; ?></a>
</div>
<?php endif; ?>

<?php if( isset( $data['instance']['email'] ) && $data['instance']['email'] <> '' ): ?>
<div class="email">
	<i class="fa fa-envelope"></i> <a href="mailto:<?php echo $data['instance']['email']; ?>"><?php echo $data['instance']['email']; ?></a>
</div>
<?php endif; ?>


<?php echo $data['args']['after_widget'];