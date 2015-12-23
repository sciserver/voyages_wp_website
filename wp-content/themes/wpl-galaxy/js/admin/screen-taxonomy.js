jQuery.noConflict()( function($){
	"use strict";

	var wprotoScreenTaxonomy = {
	
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

			$(document).ajaxStop(function () {
				var imgPreview = $('#wproto-category-image-thumb');
				imgPreview.attr( 'src', $('.wproto-image-remover').attr('data-default-img') );
				$('#wproto-category-image-input').val('0');
			});
			
		}
	}
	
	wprotoScreenTaxonomy.initialize();
	
});
