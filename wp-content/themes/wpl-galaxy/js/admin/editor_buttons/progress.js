jQuery.noConflict()( function($){
	"use strict";
	
	tinymce.PluginManager.add('wproto_insert_progress', function( editor, url ) {
		editor.addButton( 'wproto_insert_progress_button', {
			icon: 'mce_wproto_insert_progress_button',
			title : wprotoVars.mceButtonInsertProgressBar,
			onclick: function() {
				
				var shortcodeText = tinyMCE.activeEditor.selection.getContent();
				var shortcodeSettings = new Object;
				
				var matchArray = null;

				if( ( matchArray = shortcodeText.match(/(titles)=["']{1}(.*?)["']{1}/i)) != null ) {
					shortcodeSettings.titles = matchArray[2];
				} 
				if( ( matchArray = shortcodeText.match(/(values)=["']{1}(.*?)["']{1}/i)) != null ) {
					shortcodeSettings.values = matchArray[2];
				} 
				
				$('#wproto-editor-dialog').remove();
				$('<div id="wproto-editor-dialog" title="' + wprotoVars.mceButtonInsertProgressBar + '"></div>').appendTo('body').hide();
					var dialog = $('#wproto-editor-dialog');
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

										if( window.tinyMCE && ! error ) {

											var titles = [];
											var values = [];
											
											$('#wproto-progress-items input[type=text]').each( function() {
												titles.push( $(this).val() );
											});
											
											$('#wproto-progress-items input[type=number]').each( function() {
												values.push( $(this).val() );
											});

											var insertContent = '[wproto_progress titles="' + titles.join('|') + '" values="' +  values.join('|') + '"]';
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
							
							$( "#wproto-progress-items" ).sortable({
								placeholder: "ui-state-highlight",
								items: "> div.item",
								update: function (e, ui) {
									wprotoSetupTogglesTabsItems();
								}
							});
							
							$('#wproto-progress-items input[type=text]').keyup(function() {
  							$(this).val($(this).val().replace(/[|]/g, ""));
							});
							
							wprotoSetupTogglesTabsItems();
							
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