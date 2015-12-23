jQuery.noConflict()( function($){
	"use strict";
	
	tinymce.PluginManager.add('wproto_insert_divider', function( editor, url ) {
		editor.addButton( 'wproto_insert_divider_button', {
			icon: 'mce_wproto_insert_divider_button',
			title : wprotoVars.mceButtonDivider,
			onclick: function() {
				
					var shortcodeText = tinyMCE.activeEditor.selection.getContent();
					var shortcodeSettings = new Object;
				
					var matchArray = null;
					if( ( matchArray = shortcodeText.match(/(style)=["|']{1}(.*?)["|']{1}/i)) != null ) {
						shortcodeSettings.style = matchArray[2];
					} 
					
					$('#wproto-editor-dialog').remove();
					$('<div id="wproto-editor-dialog" title="' + wprotoVars.mceButtonDivider + '"></div>').appendTo('body').hide();
					var dialog = $('#wproto-editor-dialog');
					$.ajax({
						url: ajaxurl,
						type: "post",
						dataType: "json",
						data: {
							'action' : 'wproto_editor_button_form',
							'template' : 'wproto_insert_divider_button',
							'settings' : shortcodeSettings
						},
						beforeSend: function() {
							dialog.html( wprotoVars.adminBigLoaderImage );

							dialog.dialog({
								height: 290,
								width: 400,
								modal: true,
								buttons: {
									"Ok": function() {

										if( window.tinyMCE ) {

											var style = $('.wproto-divider-style input:checked').val();
											var selection = tinyMCE.activeEditor.selection;

											if ( typeof selection != "undefined" ) {
												selection.setContent( '[wproto_divider style="' + style + '"]' );
											}

										}

										$( this ).dialog( "close" );
                                                                                        
									},
									Cancel: function() {
										$( this ).dialog( "close" );
									}
								}
							});
                                                                
							dialog.css( 'overflowY', 'hidden' );
							dialog.parent().parent().find('.ui-dialog-buttonpane').hide();

						},
						success: function( response ) {
							dialog.html( response.html );
							dialog.parent().parent().find('.ui-dialog-buttonpane').show();
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
				
			}
		});
	});
	
});