<?php
	get_header('simple');
	global $wpl_galaxy_wp;
	
	$logo = wpl_galaxy_wp_utils::is_retina() ? $wpl_galaxy_wp->get_option('coming_soon_logo_2x') : $wpl_galaxy_wp->get_option('coming_soon_logo');
	$logo_size = @getimagesize( $wpl_galaxy_wp->get_option('coming_soon_logo') );
	
	$bg_image = wpl_galaxy_wp_utils::is_retina() ? $wpl_galaxy_wp->get_option('coming_soon_background_2x') : $wpl_galaxy_wp->get_option('coming_soon_background');
	$bg_h_pos = $wpl_galaxy_wp->get_option('coming_soon_background_h_pos');
	$bg_v_pos = $wpl_galaxy_wp->get_option('coming_soon_background_v_pos');
	$bg_repeat = $wpl_galaxy_wp->get_option('coming_soon_background_repeat');
	$bg_animate = $wpl_galaxy_wp->get_option('coming_soon_background_zoom');
	
?>
<div class="background <?php echo $bg_animate != 'no' ? 'animate-bg' : ''; ?>" style="background: url(<?php echo $bg_image; ?>) <?php echo $bg_h_pos; ?> <?php echo $bg_v_pos; ?> <?php echo $bg_repeat; ?>;"></div>
<!-- 
	
	PAGE HEADER
		
-->

<header class="wrapper">
		
	<img src="<?php echo $logo; ?>" width="<?php echo isset( $logo_size[0] ) ? $logo_size[0] : ''; ?>" height="<?php echo isset( $logo_size[1] ) ? $logo_size[1] : ''; ?>" alt="" />
		
</header>
<!-- 
	
	CONTENT SECTION
		
-->
	
<div id="content" class="wrapper">
	<div class="grid">
			
		<section class="unit whole">
				
			<div class="counter">
				
				<div class="wrapper">
					<h1><?php _e('Welcome', 'wproto'); ?></h1>
					
					<h3><?php _e('site will be alive in', 'wproto'); ?></h3>
				
					<ul id="countdown">
						<li class="ib li-days">
							<span class="days">00</span>
							<p class="timeRefDays"><?php _e('days', 'wproto'); ?></p>
						</li>
						<li class="ib li-hours">
							<span class="hours">00</span>
							<p class="timeRefHours"><?php _e('hours', 'wproto'); ?></p>
						</li>
						<li class="ib li-minutes">
							<span class="minutes">00</span>
							<p class="timeRefMinutes"><?php _e('minutes', 'wproto'); ?></p>
						</li>
						<li class="ib li-seconds">
							<span class="seconds">00</span>
							<p class="timeRefSeconds"><?php _e('seconds', 'wproto'); ?></p>
						</li>
					</ul>
				</div>

				
			</div>
				
		</section>
			
	</div>
</div>

<?php
	$show_subscribe_form = $wpl_galaxy_wp->get_option('coming_soon_subscribe_form');
	
	$form_action = $wpl_galaxy_wp->get_option('coming_soon_mc_action');
	$form_user_id = $wpl_galaxy_wp->get_option('coming_soon_mc_user_id');
	$form_list_id = $wpl_galaxy_wp->get_option('coming_soon_mc_list_id');
	$form_email_input_name = $wpl_galaxy_wp->get_option('coming_soon_mc_email_id');
?>

<?php if( $show_subscribe_form == 'yes' ): ?>
<footer id="coming-soon-subscribe">
	
	<div class="wrapper">
		
		<h4><?php _e('Notify me when it\'s ready', 'wproto'); ?></h4>
		
		<form target="_blank" action="<?php echo $form_action; ?>" method="post">
			<fieldset>
			
				<input type="hidden" name="u" value="<?php echo $form_user_id; ?>" />
				<input type="hidden" name="id" value="<?php echo $form_list_id; ?>" />
			
				<input type="email" name="<?php echo $form_email_input_name; ?>" id="input-email" value="" placeholder="<?php _e('Your email', 'wproto'); ?>" /> <input type="submit" value="<?php _e('Subscribe', 'wproto'); ?>" />
			</fieldset>
		</form>
	</div>
	
</footer>
<?php endif; ?>

<footer id="primary-footer">
	<div class="wrapper grid">
		<div class="unit half">
			<?php echo $wpl_galaxy_wp->get_option('copyright_text'); ?>
			<?php if( $wpl_galaxy_wp->get_option('show_wplab_info') == 'yes' ): ?>
			Design &amp; Development by <a href="http://wplab.pro">WPlab.pro</a>
			<?php endif; ?>
		</div>
		<div class="unit half">
			<span class="social-icons">
				<?php wpl_galaxy_wp_front::social_icons( true ); ?>
			</span>   
		</div>
	</div>
</footer>

<script>
jQuery.noConflict()( function(){
	"use strict";
	
	// Countdown timer
	<?php $start_timer = $wpl_galaxy_wp->get_option( 'site_opening_date', 'general' ); ?>
	jQuery("#countdown").countdown({
			date: "<?php echo $start_timer; ?> 00:00:00",
			format: "on"
		},
		function() {
			location.reload();
		}
	);
	
});
</script>
	
<?php wp_footer(); ?>
</body>
</html>