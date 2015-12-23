<style>
	#setting-error-tgmpa, #wproto-first-activation-notice {
		display: none !important;
	}
</style>
<form id="wproto-add-section-form" action="" method="post">
	<fieldset>

		<input type="hidden" name="wproto_action" value="template-save" />
		<input type="hidden" name="section_id" value="<?php echo $data['id']; ?>" />
		<input type="hidden" name="section_type" value="<?php echo $data['section']; ?>" />

		<?php include 'part_' . $data['section'] . '.tpl'; ?>

		<input type="submit" class="button button-primary" value="<?php _e('Save &amp; Close', 'wproto'); ?>" />

	</fieldset>
</form>