jQuery.noConflict()( function($){
	"use strict";
	
	tinymce.PluginManager.add('wproto_insert_btn', function( editor, url ) {
		editor.addButton( 'wproto_insert_btn_button', {
			icon: 'mce_wproto_insert_btn_button',
			title : wprotoVars.mceButtonInsertButton,
			onclick: function() {
				
				$('#wproto-editor-dialog').remove();
				$('<div id="wproto-editor-dialog" title="' + wprotoVars.mceButtonInsertButton + '"></div>').appendTo('body').hide();
				var dialog = $('#wproto-editor-dialog');
				$.ajax({
					url: ajaxurl,
					type: "post",
					dataType: "json",
					data: {
						'action' : 'wproto_editor_button_form',
						'template' : 'wproto_insert_button'
					},
					beforeSend: function() {
						dialog.html( wprotoVars.adminBigLoaderImage );

						dialog.dialog({
							height: 480,
							width: 400,
							modal: true,
							buttons: {
								"Ok": function() {

									if( window.tinyMCE ) {

										var text = $('#wproto-insert-button-text').val();
										var size = $('#wproto-insert-button-size').val();
										var color = $('#wproto-insert-button-color').val();
										var icon = $('#wproto-insert-button-icon').val();
										var link = $('#wproto-insert-button-link').val();
										var nw = $('#wproto-insert-button-new-window').val();
										var new_window = nw == 'yes' ? 'yes' : 'no';

										var insertContent = '[wproto_button text="' + text + '" size="' + size + '" color="' + color + '" icon="' + icon + '" link="' + link + '" new_window="' + new_window + '"]';
										//ed.execCommand( 'mceInsertContent', false, insertContent );
										tinyMCE.activeEditor.selection.setContent( insertContent );

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