jQuery.noConflict()( function($){
	"use strict";
	
	tinymce.PluginManager.add('wproto_insert_shorted_link', function( editor, url ) {
		editor.addButton( 'wproto_insert_shorted_link_button', {
			icon: 'mce_wproto_insert_shorted_link_button',
			title : wprotoVars.mceButtonShortedLink,
			onclick: function() {
				
				$('#wproto-editor-dialog').remove();
				$('<div id="wproto-editor-dialog" title="' + wprotoVars.mceButtonShortedLink + '"></div>').appendTo('body').hide();
				var dialog = $('#wproto-editor-dialog');
				$.ajax({
					url: ajaxurl,
					type: "post",
					dataType: "json",
					data: {
						'action' : 'wproto_editor_button_form',
						'template' : 'wproto_insert_shorted_link'
					},
					beforeSend: function() {
						dialog.html( wprotoVars.adminBigLoaderImage );

						dialog.dialog({
							height: 280,
							width: 400,
							modal: true,
							buttons: {
								"Ok": function() {

									var long_ling = $('#wproto-short-link').val();
									var loader = $('#wproto-minify-link-loader');
									
									if( $.trim( long_ling ) == '' ) {
										$('#wproto-short-link').focus();
										return false;
									} else {
				
										$.ajax({
											url: ajaxurl,
											type: "post",
											data: {
												'action' : 'wproto_editor_minify_link',
												'link' : long_ling
											},
											beforeSend: function() {
												loader.show();
											},
											success: function( response ) {
												loader.hide();
												dialog.dialog( "close" );
												if( window.tinyMCE ) {
													
													var text = $('#wproto-short-link-text').val();
													
													var linktext = $.trim( text ) == '' ? response : text;
													
													var insert = '<a href="' + response + '">' + text + '</a>';
													
													//ed.execCommand( 'mceInsertContent', false, insert );
													tinyMCE.activeEditor.selection.setContent( insert );
												}

											},
											ajaxError: function() {
												dialog.dialog( "close" );                               
												wprotoAlertAjaxError();
											}
										});
										
									}

									
                                                                                        
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