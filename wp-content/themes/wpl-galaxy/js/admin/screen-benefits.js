jQuery.noConflict()( function($){
	"use strict";

	var wprotoScreenBenefits = {
	
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
			
			this.changeStyle();
			
		},
		/**
			Set page events
		**/
		events: function() {
			
			var self = this;
			
			// Choose from benefit style icon / image
			$('.wproto-benefit-style-chooser').change( function() {
				self.changeStyle();
				return false;
			});
			
		},
		
		/**************************************************************************************************************************
			Class methods
		**************************************************************************************************************************/
		changeStyle: function() {
			var iconPicker = $('#wproto-benefit-icon-chooser');
			var imagePicker = $('#postimagediv');
			var value = $('input.wproto-benefit-style-chooser:checked').val();
		
			if( value == 'icon' ) {
				imagePicker.hide();
				iconPicker.show();
			} else {
				imagePicker.show();
				iconPicker.hide();
			}
		}
		
	}
	
	wprotoScreenBenefits.initialize();
	
});