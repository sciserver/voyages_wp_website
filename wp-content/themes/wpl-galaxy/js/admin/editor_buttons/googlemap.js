jQuery.noConflict()( function($){
	"use strict";
	
	tinymce.PluginManager.add('wproto_insert_googlemap', function( editor, url ) {
		editor.addButton( 'wproto_insert_googlemap_button', {
			icon: 'mce_wproto_insert_googlemap_button',
			title : wprotoVars.mceButtonGoogleMap,
			onclick: function() {
				
				var shortcodeText = tinyMCE.activeEditor.selection.getContent();
				var shortcodeSettings = new Object;
				
				var matchArray = null;

				if( ( matchArray = shortcodeText.match(/(address)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.address = matchArray[2];
				} 
				
				if( ( matchArray = shortcodeText.match(/(zoom)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.zoom = matchArray[2];
				} 
				
				$('#wproto-editor-dialog').remove();
				$('<div id="wproto-editor-dialog" title="' + wprotoVars.mceButtonGoogleMap + '"></div>').appendTo('body').hide();
					var dialog = $('#wproto-editor-dialog');
					$.ajax({
						url: ajaxurl,
						type: "post",
						dataType: "json",
						data: {
							'action' : 'wproto_editor_button_form',
							'template' : 'wproto_insert_googlemap',
							'settings' : shortcodeSettings
						},
						beforeSend: function() {
							dialog.html( wprotoVars.adminBigLoaderImage );

							dialog.dialog({
								height: 280,
								width: 450,
								modal: true,
								buttons: {
									"Ok": function() {

										if( window.tinyMCE ) {

											var address = $('#wproto-google-map-address').val();
											
											var zoom = $('#wproto-google-map-zoom').val();

											var insertContent = '[wproto_map address="' + address + '" zoom="' + zoom + '"]';
											tinyMCE.activeEditor.selection.setContent( insertContent );
											$( this ).dialog( "close" );

										}

										
                                                                                        
									},
									Cancel: function() {
										$( this ).dialog( "close" );
									}
								}
							});
                                                                
							dialog.css( 'overflowY', 'auto' );
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