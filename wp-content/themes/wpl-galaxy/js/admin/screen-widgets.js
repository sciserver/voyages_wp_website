jQuery.noConflict()( function($){
	"use strict";

	var wprotoScreenWidgets = {
	
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
				Toggles widget
			**/

			$( document ).on( 'click', '.wproto-edit-toggles-widget-p a.button', function() {
		
				$('#wproto-widget-toggles-dialog').remove();
		
				$('<div id="wproto-widget-toggles-dialog" title="' + wprotoVars.widgetTogglesTitle + '"></div>').appendTo('body').hide();
					var dialog = $('#wproto-widget-toggles-dialog');

					var shortcodeTextInput = document.getElementById( $(this).attr('data-content-id') );

					var shortcodeText = shortcodeTextInput.value;
					
					$.ajax({
						url: ajaxurl,
						type: "post",
						dataType: "json",
						data: {
							'action' : 'wproto_editor_button_form',
							'template' : 'wproto_insert_toggle_tabs',
							'settings' : shortcodeText
						},
						beforeSend: function() {
							dialog.html( wprotoVars.adminBigLoaderImage );

							dialog.dialog({
								height: 500,
								width: 450,
								modal: true,
								buttons: {
								"Ok": function() {

									var titles = [];
									var contents = [];
									
									
									$('#wproto-toggles-tabs-items .wproto-toggles-tabs-title').each( function() {
										titles.push( $(this).val() );
									});
											
									$('#wproto-toggles-tabs-items .wproto-toggles-tabs-content').each( function() {
										contents.push( $(this).val() );
									});

									var shortcodeInside = '';

									$( titles ).each( function( index, value ) {
										var c = $( contents ).get( index );
										shortcodeInside += '[toggle title="' + value + '"]' + c + '[/toggle]';
									});

									var insertContent = '[wproto_toggles]' + shortcodeInside + '[/wproto_toggles]';

									shortcodeTextInput.value = insertContent;

									$( shortcodeTextInput ).parents('form').find('input[type=submit]').trigger('click');
							
									dialog.dialog( "close" );
							
                                                                                        
								},
								Cancel: function() {
									dialog.dialog( "close" );
								}
							}
						});
                                                                
						dialog.css( 'overflowY', 'auto' );
						dialog.parent().parent().find('.ui-dialog-buttonpane').hide();
					},
					success: function( response ) {
						dialog.html( response.html );
						dialog.parent().parent().find('.ui-dialog-buttonpane').show();
							
						wprotoSetupTogglesTabsItems();
							
						$( "#wproto-toggles-tabs-items" ).sortable({
							placeholder: "ui-state-highlight",
							items: "> div.item",
							update: function (e, ui) {
								wprotoSetupTogglesTabsItems();
							}
						});
							
					},
					error: function() {
						dialog.dialog( "close" );                               
						wprotoAlertServerResponseError();
					},
					ajaxError: function() {
						dialog.dialog( "close" );                               
						wprotoAlertAjaxError();
					}
				}); 
		
				return false;
			});
			
			/**
				Progress bars widget
			**/
			$( document ).on( 'click', '.wproto-edit-progress-widget-p a.button', function() {
		
				$('#wproto-widget-progress-dialog').remove();
		
				$('<div id="wproto-widget-progress-dialog" title="' + wprotoVars.widgetProgressTitle + '"></div>').appendTo('body').hide();
					var dialog = $('#wproto-widget-progress-dialog');

					var shortcodeTextInput = $( $(this).attr('data-content-id') );

					var shortcodeText = shortcodeTextInput.val();
					var shortcodeSettings = new Object;
				
					var matchArray = null;

					if( ( matchArray = shortcodeText.match(/(titles)=["']{1}(.*?)["']{1}/i)) != null ) {
						shortcodeSettings.titles = matchArray[2];
					} 
					if( ( matchArray = shortcodeText.match(/(values)=["']{1}(.*?)["']{1}/i)) != null ) {
						shortcodeSettings.values = matchArray[2];
					} 
					
					$.ajax({
						url: ajaxurl,
						type: "post",
						dataType: "json",
						data: {
							'action' : 'wproto_editor_button_form',
							'template' : 'wproto_insert_progress',
							'settings' : shortcodeSettings
						},
						beforeSend: function() {
							dialog.html( wprotoVars.adminBigLoaderImage );

							dialog.dialog({
								height: 500,
								width: 450,
								modal: true,
								buttons: {
								"Ok": function() {

									var error = false;

									$( "#wproto-progress-items input[type=number], #wproto-progress-items input[type=text]" ).each( function() {
										var value = $(this).val();
										if( $.trim( value ) == '' ) {
											$(this).focus();
											error = true;
											return false;
										}
									});

									if( ! error ) {
										
										var titles = [];
										var values = [];
											
										$('#wproto-progress-items input[type=text]').each( function() {
											titles.push( $(this).val() );
										});
											
										$('#wproto-progress-items input[type=number]').each( function() {
											values.push( $(this).val() );
										});

										var insertContent = '[wproto_progress titles="' + titles.join('|') + '" values="' +  values.join('|') + '"]';

										shortcodeTextInput.val( insertContent );

										shortcodeTextInput.parents('form').find('input[type=submit]').trigger('click');
							
										dialog.dialog( "close" );
										
									}
                                                                                        
								},
								Cancel: function() {
									dialog.dialog( "close" );
								}
							}
						});
                                                                
						dialog.css( 'overflowY', 'auto' );
						dialog.parent().parent().find('.ui-dialog-buttonpane').hide();
					},
					success: function( response ) {
						dialog.html( response.html );
						dialog.parent().parent().find('.ui-dialog-buttonpane').show();
							
						wprotoSetupTogglesTabsItems();
							
						$( "#wproto-progress-items" ).sortable({
							placeholder: "ui-state-highlight",
							items: "> div.item",
							update: function (e, ui) {
								wprotoSetupTogglesTabsItems();
							}
						});
							
					},
					error: function() {
						dialog.dialog( "close" );                               
						wprotoAlertServerResponseError();
					},
					ajaxError: function() {
						dialog.dialog( "close" );                               
						wprotoAlertAjaxError();
					}
				}); 
		
				return false;
			});
			
		}
		
	}
	
	wprotoScreenWidgets.initialize();
	
});