<?php for( $i=0; $i<count( $data['titles'] ); $i++ ): ?>
	
<div class="progress">
	<div class="title"><?php echo $data['titles'][$i]; ?> <span><?php echo isset( $data['values'][$i] ) ? $data['values'][$i] : 0; ?>%</span></div>
	<div class="progress-value"><div class="value" data-appear-animation-delay="0.15" data-appear-animation="animateWidth" data-width="<?php echo isset( $data['values'][$i] ) ? $data['values'][$i] : 0; ?>%" style="width: 0%"></div></div>
</div>
	
<?php endfor; ?>
