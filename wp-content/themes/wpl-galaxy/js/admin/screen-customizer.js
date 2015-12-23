jQuery.noConflict()( function($){
	"use strict";

	var wprotoScreenCustomizer = {
	
		/**
			Constructor
		**/
		initialize: function() {

			this.build();
			this.events();

		},
		/**
			Build page elements
		**/
		build: function() {

			
		},
		/**
			Set page events
		**/
		events: function() {

			// Pattern
			$('select[data-customize-setting-link=wproto_boxed_pattern]').change( function() {
				$('#customize-control-wproto_background_image .actions a.remove').click().change();
				$('select[data-customize-setting-link=wproto_boxed_background_position]').val('left top').change();
				$('select[data-customize-setting-link=wproto_boxed_background_repeat]').val('no-repeat').change();
				$('#customize-control-wproto_boxed_background_fixed input:first').click().change();
				$('#customize-control-wproto_boxed_layout input[value=yes]').click().change();
			});
			
			// Custom bg, remove pattern
			$('#customize-control-wproto_background_image input[type=file]').on('change', function() {
				$('select[data-customize-setting-link=wproto_boxed_pattern]').val('none').change();
				//$('#customize-control-wproto_boxed_layout input[value=yes]').click().change();
				$('select[data-customize-setting-link=wproto_boxed_background_position]').val('left top').change();
				$('select[data-customize-setting-link=wproto_boxed_background_repeat]').val('no-repeat').change();
				$('#customize-control-wproto_boxed_background_fixed input:first').click().change();
			});
			
		}
	}
	
	wprotoScreenCustomizer.initialize();
	
});
