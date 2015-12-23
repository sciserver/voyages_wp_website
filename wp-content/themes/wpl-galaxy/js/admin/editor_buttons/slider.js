jQuery.noConflict()( function($){
	"use strict";
	
	tinymce.PluginManager.add('wproto_insert_slider', function( editor, url ) {
		editor.addButton( 'wproto_insert_slider', {
			icon: 'mce_wproto_insert_slider',
			title : wprotoVars.mceButtonSlider,
			onclick: function( ) {
				
				var shortcodeText = tinyMCE.activeEditor.selection.getContent();
				var shortcodeSettings = new Object;
				
				var matchArray = null;
				if( ( matchArray = shortcodeText.match(/(id)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.id = matchArray[2];
				} 
				
				$('#wproto-editor-dialog').remove();
				$('<div id="wproto-editor-dialog" title="' + wprotoVars.mceButtonSlider + '"></div>').appendTo('body').hide();
					var dialog = $('#wproto-editor-dialog');
					$.ajax({
						url: ajaxurl,
						type: "post",
						dataType: "json",
						data: {
							'action' : 'wproto_editor_button_form',
							'template' : 'wproto_insert_slider',
							'settings' : shortcodeSettings
						},
						beforeSend: function() {
							dialog.html( wprotoVars.adminBigLoaderImage );

							dialog.dialog({
								height: 220,
								width: 450,
								modal: true,
								buttons: {
									"Ok": function() {

										if( window.tinyMCE ) {

											var id = $('#wproto-layerslider-id').val();
											var insertContent = '[layerslider id="' + id + '"]';
											//tinyMCE.execCommand( 'mceInsertContent', false, insertContent );
											tinyMCE.activeEditor.selection.setContent( insertContent );
											

										}

										$( this ).dialog( "close" );
                                                                                        
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