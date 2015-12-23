<?php if( count( $data['icons'] ) > 0 ): ?>

	<div id="icon-picker-filters">
	
		<?php		
			global $wpl_galaxy_wp;
			$icomoon_enabled = $wpl_galaxy_wp->get_option('icomoon_enabled');
		?>
	
		<select id="icon-picker-filter">
			<option value="all"><?php _e('Display all libraries', 'wproto'); ?></option>
			<option value="font-awesome"><?php _e('Font Awesome Library', 'wproto'); ?></option>
			<?php if( $icomoon_enabled == 'yes' ): ?>
			<option value="icomoon"><?php _e('Ico Moon Library', 'wproto'); ?></option>
			<?php endif; ?>
		</select>
		
		<input type="text" id="icon-picker-text-filter" placeholder="Type text to filter icons..." />
	
	</div>

	<div id="icon-picker-icons">
	
		<div class="font-awesome-icon-list">
			<h1><?php _e('Font Awesome Icons', 'wproto'); ?></h1>
	
			<?php foreach( $data['icons']['font-awesome'] as $k=>$v ): ?>
	
				<i data-name="<?php echo $k; ?>" data-library="fa" class="wproto-icon-picker-icon fa-3x fa <?php echo $k; ?>"></i>
	
			<?php endforeach; ?>
			
		</div>
	
		<?php if( isset( $data['icons']['icomoon'] ) && count( $data['icons']['icomoon'] ) > 0 ): ?>
		
			<div class="clear"></div>
		
			<div class="icomoon-icon-list">
				<h1><?php _e('IcoMoon Icons', 'wproto'); ?></h1>
			
				<?php foreach( $data['icons']['icomoon'] as $k=>$v ): ?>
		
					<i data-name="<?php echo $k; ?>" data-library="icomoon" class="wproto-icon-picker-icon fa-3x <?php echo $k; ?>"></i>
	
				<?php endforeach; ?>
				
			</div>
		
		<?php endif; ?>
	
		<div class="clear"></div>
	
	</div>

<?php else: ?>
	<p><strong><?php _('Error', 'wproto'); ?></strong> <?php _('No icons founded', 'wproto'); ?></p>
<?php endif; ?>