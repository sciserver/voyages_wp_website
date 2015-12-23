<?php
	global $wproto_section, $wpl_galaxy_wp;
	$section_data = isset( $wproto_section->data ) ? unserialize( $wproto_section->data ) : array();
?>
<!--

	CONTACTS SECTION
						
-->
<section id="section-id-<?php echo $wproto_section->ID; ?>" class="contacts">

	<div class="wrapper">
		
		<div class="grid">
		
			<div class="unit one-third">
			
				<?php if( $wproto_section->title <> '' ): ?>
				<header class="hgroup">
					<h2><?php echo $wproto_section->title; ?></h2>
					<?php if( $wproto_section->subtitle <> '' ): ?>
					<h5><?php echo $wproto_section->subtitle; ?></h5>
					<?php endif; ?>
				</header>
				<?php endif; ?>
				
				<dl>
					<?php if( isset( $section_data['address'] ) && $section_data['address'] <> '' ): ?>
					<dt><?php _e('Address', 'wproto'); ?></dt>
					<dd><?php echo $section_data['address']; ?></dd>
					<?php endif; ?>
					<?php if( isset( $section_data['phone'] ) && $section_data['phone'] <> '' ): ?>
					<dt><?php _e('Phone', 'wproto'); ?></dt>
					<dd><?php echo $section_data['phone']; ?></dd>
					<?php endif; ?>
					<?php if( isset( $section_data['email'] ) && $section_data['email'] <> '' ): ?>
					<dt><?php _e('E-mail', 'wproto'); ?></dt>
					<dd><a href="mailto:<?php echo $section_data['email']; ?>"><?php echo $section_data['email']; ?></a></dd>
					<?php endif; ?>
					<?php if( isset( $section_data['working_hours'] ) && $section_data['working_hours'] <> '' ): ?>
					<dt><?php _e('We are open', 'wproto'); ?></dt>
					<dd><?php echo $section_data['working_hours']; ?></dd>
					<?php endif; ?>
				</dl>
			
			</div>
			
			<div class="unit two-thirds">
			
				<?php if( isset( $section_data['address'] ) && $section_data['address'] <> '' ): ?>
				<div class="google-map" id="google-map-section-<?php echo $wproto_section->ID; ?>"></div>
				
				<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=true" ></script> 
				<script type="text/javascript">
	
					var geocoder = new google.maps.Geocoder();
		
					var latlong;	
					geocoder.geocode( { 'address': '<?php echo strip_tags( $section_data['address'] ); ?>' }, function(results, status) {
						if (status == google.maps.GeocoderStatus.OK) {
							latlong = results[0].geometry.location;

							var googleMapOptions = {
								zoom: 10,
								center: latlong,
								mapTypeId: google.maps.MapTypeId.ROADMAP,
								panControl: false,
								zoomControl: false,
								scrollwheel: false,
								disableDoubleClickZoom: true,
								disableDefaultUI: true,
								draggable: true,
								scaleControl: false
							};

							var map = new google.maps.Map( document.getElementById('google-map-section-<?php echo $wproto_section->ID; ?>'), googleMapOptions );
		
							var image = new google.maps.MarkerImage(
 								'<?php echo get_stylesheet_directory_uri(); ?>/images/map_pointer.png',
								new google.maps.Size(22,29),
								new google.maps.Point(0,0),
								new google.maps.Point(0,35)
							);

							var marker = new google.maps.Marker({
								draggable: false,
								raiseOnDrag: false,
								icon: image,
								map: map,
									position: latlong
								});

							}
					});	
				</script>
				<?php endif; ?>
			
			</div>
		
		</div>
		
	</div>

</section>