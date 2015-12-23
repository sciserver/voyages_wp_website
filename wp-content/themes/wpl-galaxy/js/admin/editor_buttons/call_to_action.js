jQuery.noConflict()( function($){
	"use strict";
	
	tinymce.PluginManager.add('wproto_insert_call_to_action', function( editor, url ) {
		editor.addButton( 'wproto_insert_call_to_action_button', {
			icon: 'mce_wproto_insert_call_to_action_button',
			title : wprotoVars.mceButtonCallToAction,
			onclick: function() {
				
				var shortcodeText = tinyMCE.activeEditor.selection.getContent();
				var shortcodeSettings = new Object;
				
				var matchArray = null;
				
				if( ( matchArray = shortcodeText.match(/(button_text)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.button_text = matchArray[2];
				} 
				if( ( matchArray = shortcodeText.match(/(button_color)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.button_color = matchArray[2];
				} 
				if( ( matchArray = shortcodeText.match(/(button_text_color)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.button_text_color = matchArray[2];
				} 
				if( ( matchArray = shortcodeText.match(/(title)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.title = matchArray[2];
				} 
				if( ( matchArray = shortcodeText.match(/(title_color)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.title_color = matchArray[2];
				} 
				if( ( matchArray = shortcodeText.match(/(text_content)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.text_content = matchArray[2];
				} 
				if( ( matchArray = shortcodeText.match(/(content_color)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.content_color = matchArray[2];
				} 
				if( ( matchArray = shortcodeText.match(/(show_button)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.show_button = matchArray[2];
				} 
				if( ( matchArray = shortcodeText.match(/(link)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.link = matchArray[2];
				} 
				if( ( matchArray = shortcodeText.match(/(button_size)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.button_size = matchArray[2];
				} 
				if( ( matchArray = shortcodeText.match(/(icon)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.icon = matchArray[2];
				} 
				if( ( matchArray = shortcodeText.match(/(icon_color)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.icon_color = matchArray[2];
				} 
				if( ( matchArray = shortcodeText.match(/(background)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.background = matchArray[2];
				} 
				if( ( matchArray = shortcodeText.match(/(border_color)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.border_color = matchArray[2];
				} 
				if( ( matchArray = shortcodeText.match(/(new_window)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.new_window = matchArray[2];
				} 
				
				$('#wproto-editor-dialog').remove();
				$('<div id="wproto-editor-dialog" title="' + wprotoVars.mceButtonCallToAction + '"></div>').appendTo('body').hide();
					var dialog = $('#wproto-editor-dialog');
					$.ajax({
						url: ajaxurl,
						type: "post",
						dataType: "json",
						data: {
							'action' : 'wproto_editor_button_form',
							'template' : 'wproto_insert_call_to_action',
							'settings' : shortcodeSettings
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

											var title = $('#wproto-call-to-action-title').val();
											var titleColor = $('#wproto-call-to-action-title-color').val();
												
											var text_content = $('#wproto-call-to-action-text').val();
											var content_color = $('#wproto-call-to-action-text-color').val();
												
											var button = $('#wproto-call-to-action-show-button').is(':checked');
											
											var button_text = $('#wproto-call-to-action-button-text').val();
											var button_color = $('#wproto-call-to-action-button-color').val();
											var button_text_color = $('#wproto-call-to-action-button-text-color').val();
												
											var show_button = button == true ? ' show_button="yes" ' : '';
												
											var link = button == true ? ' link="' + $('#wproto-call-to-action-link').val() + '" ' : '';
											var button_size = button == true ? ' button_size="' + $('#wproto-call-to-action-button-size').val() + '" ' : '';
											var new_window = button == true ? ' new_window="' + $('#wproto-call-to-action-new-window').val() + '" ' : '';
												
											var icon = $('#wproto-call-to-action-icon').val();
												
											var box_icon = icon != '' ? ' icon="' + icon + '" ' : '';
											var box_icon_color = box_icon != '' ? ' icon_color="' + $('#wproto-call-to-action-icon-color').val() + '" ' : '';
												
											var border_color = $('#wproto-call-to-action-border-color').val();
											var bg_color = $('#wproto-call-to-action-background-color').val();

											var selection = tinyMCE.activeEditor.selection;

											if ( typeof selection != "undefined" ) {
												$( this ).dialog( "close" );
												//ed.execCommand( 'mceInsertContent', false,  );
												tinyMCE.activeEditor.selection.setContent( '[wproto_call_to_action button_text="' + button_text + '" button_color="' + button_color + '" button_text_color="' + button_text_color + '" title="' + title + '" title_color="' + titleColor + '" text_content="' + text_content + '" content_color="' + content_color + '"' + show_button + link + button_size + new_window + box_icon + box_icon_color + ' border_color="' + border_color + '"'  + ' background="' + bg_color + '"' + '] ' );
											}

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
							$('#wproto-call-to-action-button-color, #wproto-call-to-action-button-text-color, #wproto-call-to-action-title-color, #wproto-call-to-action-text-color, #wproto-call-to-action-icon-color, #wproto-call-to-action-background-color, #wproto-call-to-action-border-color').wpColorPicker();
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
	
	$( document ).on( 'change', '#wproto-call-to-action-show-button', function() {
		
		var block = $('#wproto-call-to-action-show-button-block');
		
		$(this).is(':checked') ? block.show() : block.hide();
		
		return false;
	});
	
});