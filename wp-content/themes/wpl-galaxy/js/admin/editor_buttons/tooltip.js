jQuery.noConflict()( function($){
	"use strict";
	
	tinymce.PluginManager.add('wproto_insert_tooltip', function( editor, url ) {
		editor.addButton( 'wproto_insert_tooltip_button', {
			icon: 'mce_wproto_insert_tooltip_button',
			title : wprotoVars.mceButtonInsertTooltip,
			onclick: function() {
				
					$('#wproto-editor-dialog').remove();
					$('<div id="wproto-editor-dialog" title="' + wprotoVars.mceButtonInsertTooltip + '"></div>').appendTo('body').hide();
					var dialog = $('#wproto-editor-dialog');
					$.ajax({
						url: ajaxurl,
						type: "post",
						dataType: "json",
						data: {
							'action' : 'wproto_editor_button_form',
							'template' : 'wproto_insert_tooltip_button'
						},
						beforeSend: function() {
							dialog.html( wprotoVars.adminBigLoaderImage );

							dialog.dialog({
								height: 390,
								width: 400,
								modal: true,
								buttons: {
									"Ok": function() {

										if( window.tinyMCE ) {

											var title = $('#wproto-tooltip-title').val();
											var content = $('#wproto-tooltip-content').val();
											var selection = tinyMCE.activeEditor.selection;

											if ( typeof selection != "undefined" ) {
												selection.setContent( '[wproto_tooltip title="' + title + '" content="' + content + '"]' );
											}

										}

										$( this ).dialog( "close" );
                                                                                        
									},
									Cancel: function() {
										$( this ).dialog( "close" );
									}
								}
							});
                                                                
							$('#wproto-editor-dialog').css( 'overflowY', 'auto' );

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