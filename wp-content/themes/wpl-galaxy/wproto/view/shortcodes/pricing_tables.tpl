<?php
	$col_count = isset( $data['pricing_table']['packages']['names'] ) ? count( $data['pricing_table']['packages']['names'] ) : 0;
	$col_size = $col_count > 0 ? 100 / ($col_count + 1) : 0;
	$col_size_human = wpl_galaxy_wp_front::get_column_name( $col_count );
	
?>

<?php if( $data['title'] <> '' ): ?>
<header class="subheader centered">
	<h1><?php echo $data['title']; ?></h1>
	<?php if( $data['subtitle'] <> '' ): ?>
	<h5><?php echo $data['subtitle']; ?></h5>
	<?php endif; ?>
</header>
<?php endif; ?>

<?php if( !is_array( $data['pricing_table'] ) || $col_count > 0 ): ?>
<div class="pricing-table <?php echo $data['style']; ?>" data-appear-animation="fadeIn">

	<?php
		/**************************************************************************************************************************
			FIRST STYLE
		**************************************************************************************************************************/
		if( $data['style'] == 'style_1' ):
	?>
		<div style="width: <?php echo $col_size; ?>%;" class="col features-list hide-on-phone">
			<div class="inside">
				<ul class="features-items-left">
					<li class="even"><?php _e('Plane', 'wproto'); ?></li>
					<li class="odd"><?php _e('Price', 'wproto'); ?></li>
					
					<?php if( isset( $data['pricing_table']['features']['user_features_names'] ) && is_array( $data['pricing_table']['features']['user_features_names'] ) && count( $data['pricing_table']['features']['user_features_names'] ) ): ?>
			
						<?php $i=1; foreach( $data['pricing_table']['features']['user_features_names'] as $k=>$v ): $i++; ?>
						<li class="<?php echo $i & 1 ? 'odd' : 'even'; ?>"><?php echo isset( $v[0] ) ? $v[0] : ''; ?></li>
						<?php endforeach; ?>
			
					<?php endif; ?>
					
				</ul>
			</div>
		</div>
		
		<?php if( isset( $data['pricing_table']['packages']['names'] ) && is_array( $data['pricing_table']['packages']['names'] ) && count( $data['pricing_table']['packages']['names'] ) > 0 ): ?>
			
			<?php $i=0; foreach( $data['pricing_table']['packages']['names'] as $k=>$v ): ?>
			
			<?php
				$featured = isset( $data['pricing_table']['pricing_table']['featured'] ) ? absint( $data['pricing_table']['pricing_table']['featured'] ) : 0;
			?>
			
			<div style="width: <?php echo $col_size; ?>%;" class="col feature <?php echo $k == $featured ? ' best-value' : ''; ?>">
				<div class="inside">
					<ul class="features-items-right">
						<li class="even title"><?php echo $v; ?></li>
						<li class="odd price"><?php echo isset($data['pricing_table']['features']['price'][ $i ][0]) ? $data['pricing_table']['features']['price'][ $i ][0] : ''; ?></li>
						
						<?php $j=1; foreach( $data['pricing_table']['features']['user_features_names'] as $key=>$val ): $j++; ?>
						<li class="<?php echo $j & 1 ? 'odd' : 'even'; ?>">
							<span class="desc-mobile"><?php echo isset( $val[0] ) ? $val[0] : ''; ?></span>
							<?php echo isset( $data['pricing_table']['features']['user_features_values'][$i][$key] ) ? wpl_galaxy_wp_pricing_tables_controller::check_shortcode( $data['pricing_table']['features']['user_features_values'][$i][$key] ) : ''; ?>
						</li>
						<?php endforeach; ?>

					</ul>
					<div class="buy-button">
						<a href="<?php echo isset($data['pricing_table']['features']['button_url'][ $i ][0]) ? $data['pricing_table']['features']['button_url'][ $i ][0] : ''; ?>" class="button"><?php echo isset($data['pricing_table']['features']['button_text'][ $i ][0]) ? $data['pricing_table']['features']['button_text'][ $i ][0] : ''; ?></a>
					</div>
				</div>
			</div>
			<?php $i++; endforeach; ?>
		<?php endif; ?>
			
	<?php
		/**************************************************************************************************************************
			SECOND AND THIRD STYLE
		**************************************************************************************************************************/
		elseif( $data['style'] == 'style_2' || $data['style'] == 'style_3' ):
	?>
	
	<?php if( isset( $data['pricing_table']['packages']['names'] ) && is_array( $data['pricing_table']['packages']['names'] ) && count( $data['pricing_table']['packages']['names'] ) > 0 ): ?>
			
		<?php $i=0; foreach( $data['pricing_table']['packages']['names'] as $k=>$v ): ?>
	
		<?php
			$featured = isset( $data['pricing_table']['pricing_table']['featured'] ) ? absint( $data['pricing_table']['pricing_table']['featured'] ) : 0;
		?>
	
		<div class="unit <?php echo $col_size_human; ?> <?php echo $k == $featured ? ' best-value' : ''; ?>">
			<div class="inside">
				<div class="inner">
					<h4><?php echo $v; ?></h4>
								
					<ul>
						<li class="odd price"><?php echo isset($data['pricing_table']['features']['price'][ $i ][0]) ? $data['pricing_table']['features']['price'][ $i ][0] : ''; ?></li>
						
						<?php $j=1; foreach( $data['pricing_table']['features']['user_features_names'] as $key=>$val ): $j++; ?>
						<li class="<?php echo $j & 1 ? 'odd' : 'even'; ?>">
							<?php echo isset( $val[0] ) ? $val[0] : ''; ?>
							<strong><?php echo isset( $data['pricing_table']['features']['user_features_values'][$i][$key] ) ? wpl_galaxy_wp_pricing_tables_controller::check_shortcode( $data['pricing_table']['features']['user_features_values'][$i][$key] ) : ''; ?></strong>
						</li>
						<?php endforeach; ?>

						<li class="buy-button"><a href="<?php echo isset($data['pricing_table']['features']['button_url'][ $i ][0]) ? $data['pricing_table']['features']['button_url'][ $i ][0] : ''; ?>" class="button"><?php echo isset($data['pricing_table']['features']['button_text'][ $i ][0]) ? $data['pricing_table']['features']['button_text'][ $i ][0] : ''; ?></a></li>
					</ul>
				</div>
			</div>
		</div>
		
		<?php $i++; endforeach; ?>
	
	<?php endif; ?>
	<?php endif; ?>
	<div class="clear"></div>
</div>
<?php endif;