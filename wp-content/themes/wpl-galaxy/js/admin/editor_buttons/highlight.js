jQuery.noConflict()( function($){
	"use strict";
	
	tinymce.PluginManager.add('wproto_insert_highlight', function( editor, url ) {
		editor.addButton( 'wproto_insert_highlight_button', {
			icon: 'mce_wproto_insert_highlight_button',
			title : wprotoVars.mceButtonHighlight,
			onclick: function() {
				
						var selectedText = tinyMCE.activeEditor.selection.getContent({format : 'text'});
						var color = '';
						var text = '';
						
						var matchArray = null;
						if( ( matchArray = selectedText.match(/(color)=["|']{1}(.*?)["|']{1}/i)) != null ) {
							color = matchArray[2];
						} 
						if( ( matchArray = selectedText.match(/(content)=["|']{1}(.*?)["|']{1}/i)) != null ) {
							text = matchArray[2];
						} 

						$('#wproto-editor-dialog').remove();
						$('<div id="wproto-editor-dialog" title="' + wprotoVars.mceButtonHighlight + '"></div>').appendTo('body').hide();
						var dialog = $('#wproto-editor-dialog');
						$.ajax({
							url: ajaxurl,
							type: "post",
							dataType: "json",
							data: {
								'action' : 'wproto_editor_button_form',
								'template' : 'wproto_insert_highlight',
								'selected_text' : text,
								'color' : color
							},
							beforeSend: function() {
								dialog.html( wprotoVars.adminBigLoaderImage );

								dialog.dialog({
									height: 450,
									width: 450,
									modal: true,
									buttons: {
										"Ok": function() {

											if( window.tinyMCE ) {

												var color = $('#wproto-highlight-color').val();
												var content = $('#wproto-highlight-content').val();
												var selection = tinyMCE.activeEditor.selection;

												if ( typeof selection != "undefined" ) {
													selection.setContent( '[wproto_highlight color="' + color + '" content="' + content + '"]' );
												}

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
								$('#wproto-highlight-color').wpColorPicker();
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