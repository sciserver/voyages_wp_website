	<?php
		global $wpl_galaxy_wp;
	?>
	
	<!--
				
		PAGE FOOTER
					
	-->
	<footer id="footer" data-appear-animation="fadeIn">
		<!-- widgetized footer content -->
		<?php wpl_galaxy_wp_front::widgetized_footer(); ?>
		
	</footer>
	<div id="primary-footer">
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
	</div>
</div>
	<?php wpl_galaxy_wp_front::footer(); wp_footer(); ?>
</body>
</html>