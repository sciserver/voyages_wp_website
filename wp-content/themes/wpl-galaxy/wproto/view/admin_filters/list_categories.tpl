<?php
	$terms_count = count( $data['terms'] );
	
	if( $terms_count > 0 && is_array( $data['terms'] ) ){
	
		$terms_array = array();
	
		foreach ( $data['terms'] as $term ) {
			$terms_array[] = $term->name;
		}

		echo join( ", ", $terms_array );
	
	} else {
		echo '&mdash;';
	}