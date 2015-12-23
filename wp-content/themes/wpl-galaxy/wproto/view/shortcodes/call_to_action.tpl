<div class="call-to-action <?php echo isset( $data['icon'] ) && $data['icon'] <> '' ? 'with-icon' : ''; ?>" style="<?php echo isset( $data['border_color'] ) ? 'border-color: ' . $data['border_color'] . ' !important;' : ''; ?> <?php echo isset( $data['background'] ) ? 'background-color: ' . $data['background'] . ' !important;' : ''; ?>">

	<?php if( isset( $data['icon'] ) && $data['icon'] <> '' ): ?>
	<div class="block-icon">
		<a><i style="<?php echo isset( $data['icon_color'] ) ? 'color: ' . $data['icon_color'] . ' !important;' : ''; ?>" class="<?php echo $data['icon']; ?>"></i></a>
	</div>
	<?php endif; ?>

	<div class="block-content">
		<?php if( isset( $data['title'] ) && $data['title'] <> '' ): ?>
			<h3 style="<?php echo isset( $data['title_color'] ) ? 'color: ' . $data['title_color'] . ' !important;' : ''; ?>"><?php echo $data['title']; ?></h3>
		<?php endif; ?>
		<?php if( isset( $data['text_content'] ) && $data['text_content'] <> '' ): ?>
			<div style="<?php echo isset( $data['text_color'] ) ? 'color: ' . $data['text_color'] . ' !important;' : ''; ?>"><?php echo $data['text_content']; ?></div>
			<div class="clear"></div>
		<?php endif; ?>
		<?php if( isset( $data['show_button'] ) && $data['show_button'] == 'yes' ): ?>
		<br />
		<a <?php echo isset( $data['new_window'] ) && $data['new_window'] == 'yes' ? 'target="_blank"' : ''; ?> href="<?php echo isset( $data['link'] ) ? $data['link'] : ''; ?>" class="button <?php echo isset( $data['button_size'] ) ? 'size-' . $data['button_size'] : ''; ?>" style="<?php echo isset( $data['button_text_color'] ) ? 'color: ' . $data['button_text_color'] . ' !important;' : ''; ?> <?php echo isset( $data['button_color'] ) ? 'background-color: ' . $data['button_color'] . ' !important;' : ''; ?>"><?php echo isset( $data['button_text'] ) ? $data['button_text'] : ''; ?></a>
		<?php endif; ?>
	</div>

</div>