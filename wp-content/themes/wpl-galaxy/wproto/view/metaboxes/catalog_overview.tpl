<?php
	wp_editor(
		$data['overview_text'],
		'wproto-catalog-overview-text-editor',
		array(
			'media_buttons' => false,
			'textarea_name' => 'overview_text',
			'textarea_rows' => 15,
			'tabindex' => 4
		)
	);