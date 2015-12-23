<table class="widefat" id="wproto-pricing-table-editor">
	<?php if( !is_array( $data['pricing_table'] ) || count( $data['pricing_table'] ) <= 0 ): ?>
	<thead>
		<tr>
			<th class="ex"><?php _e('Packages &amp; Features', 'wproto'); ?></th>
			<th class="package-title"><input name="pt[packages][names][0]" type="text" value="<?php _e('Basic', 'wproto'); ?>" /></th>
			<th class="package-title"><input name="pt[packages][names][1]" type="text" value="<?php _e('Pro', 'wproto'); ?>" /></th>
			<th class="package-title"><input name="pt[packages][names][2]" type="text" value="<?php _e('Unlimited', 'wproto'); ?>" /></th>
			<th class="ex"><a href="javascript:;" class="wproto-add-pricing-package button"><i class="fa fa-plus"></i> <?php _e('Add package', 'wproto'); ?></a></th>
		</tr>
	</thead>
	<tfoot>
		<tr>
			<th class="ex"><a href="javascript:;" class="wproto-add-pricing-feature button"><i class="fa fa-plus"></i> <?php _e('Add feature', 'wproto'); ?></a></th>
			<th class="center"><a href="javascript:;" class="wproto-delete-package button"><i class="fa fa-times"></i></a> <a href="javascript:;" class="wproto-make-featured-price button"><i class="fa fa-star"></i><input type="radio" name="pt[pricing_table][featured]" value="0" /></a></th>
			<th class="center"><a href="javascript:;" class="wproto-delete-package button"><i class="fa fa-times"></i></a> <a href="javascript:;" class="wproto-make-featured-price button button-primary"><i class="fa fa-star"></i><input type="radio" name="pt[pricing_table][featured]" checked="checked" value="1" /></a></th>
			<th class="center"><a href="javascript:;" class="wproto-delete-package button"><i class="fa fa-times"></i></a> <a href="javascript:;" class="wproto-make-featured-price button"><i class="fa fa-star"></i><input type="radio" name="pt[pricing_table][featured]" value="2" /></a></th>
			<th class="ex"></th>
		</tr>
	</tfoot>
	<tbody>
		<tr class="move system-item item-price">
			<td class="description ex">
				<i><?php _e('Price', 'wproto'); ?></i>
			</td>
			<td><input name="pt[features][price][0][]" type="text" value="" /></td>
			<td><input name="pt[features][price][1][]" type="text" value="" /></td>
			<td><input name="pt[features][price][2][]" type="text" value="" /></td>
			<td class="ex"></td>
		</tr>
		<!--
		<tr class="move system-item item-details">
			<td class="description ex">
				<i><?php _e('Details', 'wproto'); ?></i>
			</td>
			<td><input name="pt[features][details][0][]" type="text" value="" /></td>
			<td><input name="pt[features][details][1][]" type="text" value="" /></td>
			<td><input name="pt[features][details][2][]" type="text" value="" /></td>
			<td class="ex"></td>
		</tr>
		-->
		<tr class="move system-item item-button">
			<td class="description ex">
				<i><?php _e('Button text', 'wproto'); ?></i><br />
				<i><?php _e('Button URL', 'wproto'); ?></i>
			</td>
			<td>
				<input name="pt[features][button_text][0][]" type="text" value="" /><br />
				<input name="pt[features][button_url][0][]" type="text" value="" />
			</td>
			<td>
				<input name="pt[features][button_text][1][]" type="text" value="" /><br />
				<input name="pt[features][button_url][1][]" type="text" value="" />
			</td>
			<td>
				<input name="pt[features][button_text][2][]" type="text" value="" /><br />
				<input name="pt[features][button_url][2][]" type="text" value="" />
			</td>
			<td class="ex"></td>
		</tr>
		<tr class="move custom-item">
			<td class="description ex">
			
				<a href="javascript:;" class="button wproto-delete-feature"><i class="fa fa-times"></i></a>
			
				<input name="pt[features][user_features_names][0][]" type="text" value="<?php _e( 'Your feature', 'wproto'); ?>" />
			</td>
			<td><input name="pt[features][user_features_values][0][]" type="text" value="<?php _e( 'Basic value', 'wproto'); ?>" /></td>
			<td><input name="pt[features][user_features_values][1][]" type="text" value="<?php _e( 'Pro value', 'wproto'); ?>" /></td>
			<td><input name="pt[features][user_features_values][2][]" type="text" value="<?php _e( 'Unlimited value', 'wproto'); ?>" /></td>
			<td class="center ex"><img width="16" height="16" src="<?php echo WPROTO_THEME_URL . '/images/admin/'; ?><?php echo wpl_galaxy_wp_utils::is_retina() ? 'move@2x.png' : 'move.png' ; ?>" alt="" /></td>
		</tr>
	</tbody>
	<?php else: ?>
	<thead>
		<tr>
			<th class="ex"><?php _e('Packages &amp; Features', 'wproto'); ?></th>
			<?php if( isset( $data['pricing_table']['packages']['names'] ) && is_array( $data['pricing_table']['packages']['names'] ) && count( $data['pricing_table']['packages']['names'] ) > 0 ): ?>
			
				<?php foreach( $data['pricing_table']['packages']['names'] as $k=>$v ): ?>
				<th class="package-title"><input name="pt[packages][names][<?php echo $k; ?>]" type="text" value="<?php echo $v; ?>" /></th>
				<?php endforeach; ?>
			
			<?php endif; ?>
			<th class="ex"><a href="javascript:;" class="wproto-add-pricing-package button"><i class="fa fa-plus"></i> <?php _e('Add package', 'wproto'); ?></a></th>
		</tr>
	</thead>
	<tfoot>
		<tr>
			<th class="ex"><a href="javascript:;" class="wproto-add-pricing-feature button"><i class="fa fa-plus"></i> <?php _e('Add feature', 'wproto'); ?></a></th>
			<?php if( isset( $data['pricing_table']['packages']['names'] ) && is_array( $data['pricing_table']['packages']['names'] ) && count( $data['pricing_table']['packages']['names'] ) > 0 ): ?>
			
				<?php foreach( $data['pricing_table']['packages']['names'] as $k=>$v ): ?>
				
				<?php
					$featured = isset( $data['pricing_table']['pricing_table']['featured'] ) ? absint( $data['pricing_table']['pricing_table']['featured'] ) : 0;
				?>
				
				<th class="center"><a href="javascript:;" class="wproto-delete-package button"><i class="fa fa-times"></i></a> <a href="javascript:;" class="wproto-make-featured-price button<?php echo $k == $featured ? ' button-primary' : ''; ?>"><i class="fa fa-star"></i><input type="radio" <?php echo $k == $featured ? 'checked="checked"' : ''; ?> name="pt[pricing_table][featured]" value="<?php echo $k; ?>" /></a></th>
				<?php endforeach; ?>
			
			<?php endif; ?>
			<th class="ex"></th>
		</tr>
	</tfoot>
	<tbody>
		<tr class="move system-item item-price">
			<td class="description ex">
				<i><?php _e('Price', 'wproto'); ?></i>
			</td>
			<?php for( $i=0; $i<count( $data['pricing_table']['packages']['names'] ); $i++ ): ?>
			<td><input name="pt[features][price][<?php echo $i; ?>][]" type="text" value="<?php echo isset($data['pricing_table']['features']['price'][ $i ][0]) ? $data['pricing_table']['features']['price'][ $i ][0] : ''; ?>" /></td>
			<?php endfor; ?>
			<td class="ex"></td>
		</tr>
		<!--
		<tr class="move system-item item-details">
			<td class="description ex">
				<i><?php _e('Details', 'wproto'); ?></i>
			</td>
			<?php for( $i=0; $i<count( $data['pricing_table']['packages']['names'] ); $i++ ): ?>
			<td><input name="pt[features][details][<?php echo $i; ?>][]" type="text" value="<?php echo isset($data['pricing_table']['features']['details'][ $i ][0]) ? $data['pricing_table']['features']['details'][ $i ][0] : ''; ?>" /></td>
			<?php endfor; ?>
			<td class="ex"></td>
		</tr>
		-->
		<tr class="move system-item item-button">
			<td class="description ex">
				<i><?php _e('Button text', 'wproto'); ?></i><br />
				<i><?php _e('Button URL', 'wproto'); ?></i>
			</td>
			<?php for( $i=0; $i<count( $data['pricing_table']['packages']['names'] ); $i++ ): ?>
			<td>
				<input name="pt[features][button_text][<?php echo $i; ?>][]" type="text" value="<?php echo isset($data['pricing_table']['features']['button_text'][ $i ][0]) ? $data['pricing_table']['features']['button_text'][ $i ][0] : ''; ?>" /><br />
				<input name="pt[features][button_url][<?php echo $i; ?>][]" type="text" value="<?php echo isset($data['pricing_table']['features']['button_url'][ $i ][0]) ? $data['pricing_table']['features']['button_url'][ $i ][0] : ''; ?>" />
			</td>
			<?php endfor; ?>
			<td class="ex"></td>
		</tr>
		<?php if( isset( $data['pricing_table']['features']['user_features_names'] ) && count( $data['pricing_table']['features']['user_features_names'] ) ): ?>
		
			<?php foreach( $data['pricing_table']['features']['user_features_names'] as $k=>$v ): ?>
			
			<tr class="move custom-item">
				<td class="description ex">
			
					<a href="javascript:;" class="button wproto-delete-feature"><i class="fa fa-times"></i></a>
			
					<input name="pt[features][user_features_names][<?php $k; ?>][]" type="text" value="<?php echo isset( $v[0] ) ? $v[0] : ''; ?>" />
				</td>
				
				<?php for( $i=0; $i<count( $data['pricing_table']['packages']['names'] ); $i++ ): ?>
				<td><input name="pt[features][user_features_values][<?php echo $i; ?>][]" type="text" value="<?php echo isset( $data['pricing_table']['features']['user_features_values'][$i][$k] ) ? $data['pricing_table']['features']['user_features_values'][$i][$k] : ''; ?>" /></td>
				<?php endfor; ?>
				<td class="center ex"><img width="16" height="16" src="<?php echo WPROTO_THEME_URL . '/images/admin/'; ?><?php echo wpl_galaxy_wp_utils::is_retina() ? 'move@2x.png' : 'move.png' ; ?>" alt="" /></td>
			</tr>
			
			<?php endforeach; ?>
		
		<?php endif; ?>
		
	</tbody>
	
	<?php endif; ?>
</table>