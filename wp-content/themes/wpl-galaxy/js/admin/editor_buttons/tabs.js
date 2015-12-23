jQuery.noConflict()( function($){
	"use strict";
	
	tinymce.PluginManager.add('wproto_insert_tabs', function( editor, url ) {
		editor.addButton( 'wproto_insert_tabs_button', {
			icon: 'mce_wproto_insert_tabs_button',
			title : wprotoVars.mceButtonInsertTabs,
			onclick: function() {
				
				var shortcodeText = tinyMCE.activeEditor.selection.getContent();
				
				$('#wproto-editor-dialog').remove();
				$('<div id="wproto-editor-dialog" title="' + wprotoVars.mceButtonInsertTabs + '"></div>').appendTo('body').hide();
					var dialog = $('#wproto-editor-dialog');
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

										if( window.tinyMCE ) {

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
												shortcodeInside += '[tab title="' + value + '"]' + c + '[/tab]';
											});

											var insertContent = '[wproto_tabs]' + shortcodeInside + '[/wproto_tabs]';
																						
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
							
							wprotoSetupTogglesTabsItems();
							
							$( "#wproto-toggles-tabs-items" ).sortable({
								placeholder: "ui-state-highlight",
								items: "> div.item",
								update: function (e, ui) {
									wprotoSetupTogglesTabsItems();
								}
							});
							
							$('.wproto-toggles-tabs-title, wproto-toggles-tabs-content').keyup(function() {
  							$(this).val($(this).val().replace(/[|]/g, ""));
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
				
			}
		});
	});
	
});