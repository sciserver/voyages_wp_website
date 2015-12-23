<?php
	/**
	 * Template name: 7. Contact us 
	 **/

	get_header();
	global $wpl_galaxy_wp, $post;
	
	$page_settings = $wpl_galaxy_wp->model->post->get_post_custom( $post->ID );
	
	$zoom = isset( $page_settings->wproto_tpl_contact_display_map_zoom ) ? absint( $page_settings->wproto_tpl_contact_display_map_zoom ) : 10;
	$map_draggable = isset( $page_settings->wproto_tpl_contact_display_map_draggable ) ? $page_settings->wproto_tpl_contact_display_map_draggable : 'yes';
	$map_zoom_controls = isset( $page_settings->wproto_tpl_contact_display_map_zoom_control ) ? $page_settings->wproto_tpl_contact_display_map_zoom_control : 'no';
?>

	<!--
		GOOGLE MAP
	-->
	<section id="google-map-contact" data-zoom="<?php echo $zoom; ?>" data-draggable="<?php echo $map_draggable; ?>" data-zoom-controls="<?php echo $map_zoom_controls; ?>"></section>

	<!-- 
	
		CONTENT SECTION
		
	-->
	
	<div id="content" class="wrapper">
		<div class="grid">

			<section class="<?php wpl_galaxy_wp_front::content_classes(); ?>">
				
				<article class="post">
				
					<?php
						if( have_posts() ): while ( have_posts() ) :
						
							the_post();
							
					?>

					<!--
					
						POST CONTENT
						
					-->
					
					<?php the_content(); ?>
					
					<!--
					
						CONTACT FORM
						
					-->
					<form id="contact-form-main" class="wproto-contact-form" action="javascript:;" method="post" class="wrapper grid">

						<input type="hidden" name="wproto_form_id" value="primary-contact-form" />

						<section id="contact-form-part" class="unit half">
		
							<h3><?php _e( 'Send us a message', 'wproto' ); ?>:</h3>
				
							<div class="grid">
								<div class="unit half">
					
									<label for="input-name"><?php _e( 'Name', 'wproto' ); ?>:</label>
									<input type="text" name="name" value="" id="input-name" />
						
									<div class="error"><?php _e( 'Please type your name', 'wproto' ); ?></div>
				
								</div>
				
								<div class="unit half">
				
									<label for="input-email"><?php _e( 'Email', 'wproto' ); ?>:</label>
									<input type="email" name="email" value="" id="input-email" />
						
									<div class="error"><?php _e( 'Please type valid email address', 'wproto' ); ?></div>
				
								</div>
				
								<div class="unit whole">
									<label for="input-subject"><?php _e( 'Subject', 'wproto' ); ?>:</label>
									<input type="text" name="subject" value="" id="input-subject" />
								</div>
					
								<div class="unit whole">
									<label for="input-message"><?php _e( 'Your message', 'wproto' ); ?>:</label>
									<textarea id="input-message" name="message" rows="4"></textarea>
						
									<div class="error"><?php _e( 'Please type your message', 'wproto' ); ?></div>
						
								</div>
								
								<?php if( isset( $page_settings->wproto_tpl_contact_display_captcha ) && $page_settings->wproto_tpl_contact_display_captcha != 'no' ): ?>
									<div class="unit whole unit-contacts">
										<?php $wpl_galaxy_wp->controller->captcha->generate_captcha_phrase(); ?>
									</div>
								<?php endif; ?>
								
								<div class="unit whole">
									<input type="submit" value="<?php _e( 'Send message', 'wproto' ); ?>" />
								</div>

							</div>
		
						</section>
		
						<section class="unit half">
		
							<?php
								// get contact values
								$address = isset( $page_settings->wproto_tpl_contact_address ) ? trim( $page_settings->wproto_tpl_contact_address ) : '';
								$phone = isset( $page_settings->wproto_tpl_contact_phone ) ? trim( $page_settings->wproto_tpl_contact_phone ) : '';
								$fax = isset( $page_settings->wproto_tpl_contact_fax ) ? trim( $page_settings->wproto_tpl_contact_fax ) : '';
								$email = isset( $page_settings->wproto_tpl_contact_email_to ) ? trim( $page_settings->wproto_tpl_contact_email_to ) : '';
							?>
		
							<?php if( $address <> '' && $phone <> '' && $fax <> '' && $email <> '' ): ?>
							
							<h3><?php _e( 'Contact details', 'wproto' ); ?>:</h3>
							
							<?php endif; ?>
						
							<?php if( $address <> '' ): ?>
								<p><strong><?php _e( 'Office address', 'wproto' ); ?>:</strong> <?php echo $address; ?></p>
							<?php endif; ?>
				
							<?php if( $phone <> '' ): ?>
								<p><strong><?php _e( 'Phone', 'wproto' ); ?>:</strong> <?php echo $phone; ?></p>
							<?php endif; ?>
				
							<?php if( $fax <> '' ): ?>
								<p><strong><?php _e( 'Fax', 'wproto' ); ?>:</strong> <?php echo $fax; ?></p>
							<?php endif; ?>
				
							<?php if( $email <> '' ): ?>
								<p><strong><?php _e( 'Email', 'wproto' ); ?>:</strong> <a href="mailto:<?php echo $email; ?>"><?php echo $email; ?></a></p>
							<?php endif; ?>
							
							<?php if( isset( $page_settings->wproto_tpl_contact_display_social ) && $page_settings->wproto_tpl_contact_display_social != 'no' ): ?>
							<h3><?php _e('We are social', 'wproto'); ?>:</h3>
				
							<div class="social-icons">
								<?php wpl_galaxy_wp_front::social_icons( true ); ?>
							</div>
							<?php endif; ?>
			
						</section>
		
					</form>
					
					<?php endwhile; endif; ?>
				
				</article>
				
			</section>

			<?php wpl_galaxy_wp_front::get_sidebar(); ?>
			
		</div>
	</div> <!-- /content -->

<?php get_footer();