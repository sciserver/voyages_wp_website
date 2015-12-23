jQuery.noConflict()( function($){
	"use strict";

	var wprotoScreenSidebars = {
	
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
			
			/**
				Hide widgets screen from menu if no registered sidebars
			**/
			$( document ).on( 'click', 'a.delete-tag', function() {
				
				var count = $('#the-list tr').length;
		
				if( count - 1 == 0 ) {
					$('ul.wp-submenu a[href$="widgets.php"]').parent().hide();
				}
		
			});
	
			/**
				Show widgets screen from menu when first sidebar added
			**/
			$('#submit').click( function() {
				var count = $('#the-list tr').length;
		
				if( count + 1 > 0 ) {
					$('ul.wp-submenu a[href$="widgets.php"]').parent().show();
				}
		
			});

			
		}
		
	}
	
	wprotoScreenSidebars.initialize();
	
});
