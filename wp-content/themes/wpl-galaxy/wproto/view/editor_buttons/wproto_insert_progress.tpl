<?php
	$items = array();
	
	$title_string = isset( $data['settings']['titles'] ) ? $data['settings']['titles'] : '';
	$value_string = isset( $data['settings']['values'] ) ? $data['settings']['values'] : '';
	
	$titles = explode("|", $title_string );
	$values = explode("|", $value_string );
	
	if( is_array( $titles ) && count( $titles ) > 0 ) {
		for ( $i=0; $i<count( $titles ); $i++ ) {
			if( $titles[ $i ] != '' ) {
				$items[$i]['title'] = isset( $titles[ $i ] ) ? $titles[ $i ] : '';
				$items[$i]['value'] = isset( $values[ $i ] ) ? $values[ $i ] : '';	
			}
		}
	}
	
?>

<h3><?php _e( 'Add Progress Bar', 'wproto' ); ?>:</h3>

<div id="wproto-progress-items">

	<?php if( count( $items ) > 0 ): foreach( $items as $k=>$item ): ?>
	
	<div class="item">
		<p>
			<label><?php _e( 'Progress bar title', 'wproto' ); ?>:  <br />
			<input class="wproto-toggles-tabs-title full-width-input" value="<?php echo $item['title']; ?>" type="text" /> </label>
		</p>
		<p>
			<label><?php _e( 'Value', 'wproto' ); ?>: <input type="number" min="1" max="100" value="<?php echo $item['value']; ?>" /></label> 
		</p>

		<div class="controls">
			<a href="javascript:;" class="remove"></a>
			<a href="javascript:;" class="add"></a>
		</div>
		
	</div>
	
	<?php endforeach; else: ?>
	
	<div class="item">
		<p>
			<label><?php _e( 'Progress bar title', 'wproto' ); ?>:  <br />
			<input class="wproto-toggles-tabs-title full-width-input" type="text" /> </label>
		</p>
		<p>
			<label><?php _e( 'Value', 'wproto' ); ?>: <input type="number" min="1" max="100" value="25" /></label> 
		</p>

		<div class="controls">
			<a href="javascript:;" class="remove"></a>
			<a href="javascript:;" class="add"></a>
		</div>
		
	</div>
	
	<?php endif; ?>

</div>