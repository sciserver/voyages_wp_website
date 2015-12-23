jQuery.noConflict()( function($){
	"use strict";

	var wprotoScreenSettings = {
	
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
			
			if( $('#wproto-tabbed').length ) {
				wprotoEnableTabOnTextarea('wproto-tabbed');
			}
			
			
			
		},
		/**
			Set page events
		**/
		events: function() {

			/**
				Install sample data
			**/
			$('#wproto-install-sample-data').click( function() {
				
				var button = $(this);
				
				if( button.attr('disabled') == 'disabled' ) {
					return false;
				}
				
				var resultsDiv = $('#wproto-install-sample-data-results');
				
				$.ajax({
					url: ajaxurl,
					type: "POST",
					data: {
						'action' : 'wproto_install_sample_data'
					},
					beforeSend: function() {
						resultsDiv.show();
						button.attr('disabled', 'disabled');
					},
					success: function( result) {
						resultsDiv.find('p').html( wprotoVars.strAllDone );
					}
				});
				
				return false;
			});

			/**
				Branding settings
			**/
	
			$('.wproto-header-logo-input').change( function() {
				var val = $(this).val();
				var child = $('#wproto-site-logo-type');
				var child2 = $('#wproto-site-title-and-tagline');
				if( val == 'image' ) {
					child.show();
					child2.hide();
			
					if( $('.wproto-header-logo-type:checked').val() == 'custom' ) {
						$('#wproto-upload-custom-logo').show();
					}
			
				} else {
					child.hide();
					child2.show();
					$('#wproto-upload-custom-logo').hide();
				}
		
			});
	
			$('.wproto-header-logo-type').change( function() {
				var val = $(this).val();
				var child = $('#wproto-upload-custom-logo');
				if( val == 'custom' ) {
					child.show();
				} else {
					child.hide();
				}
		
			});
	
			$('.wproto-remove-favicon').click( function() {
				$(this).parent().find('input[type=text]').val('').focus();
				return false;
			});
	
			$('.wproto-remove-favicon').click( function() {
				$(this).parent().find('input[type=text]').val('').focus();
				return false;
			});

			/**
				Rebuild thumbnails
			**/
			$( '#wproto-rebuild-all-thumbs').click( function() {
				$( this).attr( 'disabled', true);
        
				var submitBtn = $( this);
				var resultDiv = $( '#wproto-regenerate-results');
        
				resultDiv.find( 'p').html( wprotoVars.strPleaseWait);
        
				resultDiv.show();

				$.ajax({
					url: ajaxurl,
					type: "POST",
					data: {
						'action' : 'wproto_rebuild_thumbnails',
						'subaction' : 'getlist'
					},
					success: function( result) {
						var list = eval( result);
						var curr = 0;
                
						if ( !list) {
							resultDiv.find( 'p').html( wprotoVars.strNoAttachmentsFound);
							submitBtn.attr( 'disabled', false);
						}
                
						function wprotoRegenerateItem() {
                    
							if (curr >= list.length) {
								submitBtn.attr( 'disabled', false);
								resultDiv.find( 'p').html( '<strong>' + wprotoVars.strAllDone + '</strong>');
								resultDiv.fadeOut( 2000);
								return;
							}
                    
							resultDiv.find( 'p').html( wprotoVars.strRebuilding + " " + (curr + 1) + " " + wprotoVars.strOf + " " + list.length);
                    
							$.ajax({
								url: ajaxurl,
								type: "POST",
								data: {
									'action' : 'wproto_rebuild_thumbnails',
									'subaction' : 'regen',
									'id' : list[curr].id
								},
								success: function( result) {
									curr = curr + 1;
									wprotoRegenerateItem();
								}
							});
                    
						}
                
						wprotoRegenerateItem();
                
					},
					error: function(request, status, error) {
						resultDiv.find( 'p').html( wprotoVars.strError + ": " + request.status);
					}
				});
        
				return false;
			});
	
			/**
				Flush rewrite rules
			**/ 
			$( '#wproto-flush-rewrite-rules').click( function() {
				$( this).attr( 'disabled', true);
        
				var submitBtn = $( this );
				var resultDiv = $( '#wproto-flush-results');
        
				resultDiv.find( 'p').html( wprotoVars.strPleaseWait);
        
				resultDiv.show();

				$.ajax({
					url: ajaxurl,
					type: "POST",
					data: {
						'action' : 'wproto_flush_rewrite_rules'
					},
					beforeSend: function() {
						submitBtn.attr( 'disabled', 'disabled');
					},
					success: function() {
						resultDiv.find( 'p').html( wprotoVars.strAllDone );    
						resultDiv.fadeOut(1200);
						submitBtn.attr( 'disabled', false);
					},
					error: function(request, status, error) {
						resultDiv.find( 'p').html( wprotoVars.strError + ": " + request.status);
					}
				});
        
				return false;
			});
	
			/**
				Grab google fonts
			**/
			$('#wproto-grab-google-fonts').click( function() {
		
				var status_div = $('#wproto-google-fonts-grab-results');
				var loader = $('#wproto-grab-google-fonts-loader');
				var submitBtn = $( this );
		
				$.ajax({
					url: ajaxurl,
					type: "POST",
					data: {
						'action' : 'wproto_grab_google_fonts_list'
					},
					beforeSend: function() {
						status_div.addClass('infodiv').removeClass('error').show();
						status_div.find('span').html( wprotoVars.strGrabbing );
						loader.show();
						submitBtn.attr( 'disabled', 'disabled');
					},
					success: function( status ) {
				
						loader.hide();
				
						if( status == 'ok' ) {
					
							loader.hide();
							status_div.addClass('infodiv');
							status_div.find('span').html( wprotoVars.strSuccess );
							status_div.fadeOut(2000);
					
						} else {
							status_div.find('span').html( wprotoVars.strCantConnectToGoogle );
							status_div.addClass('error').removeClass('infodiv');
						}
				
						submitBtn.attr( 'disabled', false);
				
					},
					error: function(request, status, error) {
						loader.hide();
						status_div.find('span').html( wprotoVars.strError + ": " + request.status );
						status_div.addClass('error').removeClass('infodiv');
					}
				});
		
				return false;
			});

			
		}
		
	}
	
	wprotoScreenSettings.initialize();
	
});