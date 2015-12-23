jQuery.noConflict()( function($){
	"use strict";
	
	tinymce.PluginManager.add('wproto_insert_contact_form_button', function( editor, url ) {
		editor.addButton( 'wproto_insert_contact_form_button', {
			icon: 'mce_wproto_insert_contact_form_button',
			title : wprotoVars.mceButtonContactForm,
			onclick: function() {
				
				var shortcodeText = tinyMCE.activeEditor.selection.getContent();
				var shortcodeSettings = new Object;
				
				var matchArray = null;

				if( ( matchArray = shortcodeText.match(/(to)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.to = matchArray[2];
				} 
				if( ( matchArray = shortcodeText.match(/(subject)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.subject = matchArray[2];
				} 
				if( ( matchArray = shortcodeText.match(/(title)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.title = matchArray[2];
				} 
				if( ( matchArray = shortcodeText.match(/(text)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.text = matchArray[2];
				}
				if( ( matchArray = shortcodeText.match(/(captcha)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.captcha = matchArray[2];
				}
				
				$('#wproto-editor-dialog').remove();
				$('<div id="wproto-editor-dialog" title="' + wprotoVars.mceButtonContactForm + '"></div>').appendTo('body').hide();
					var dialog = $('#wproto-editor-dialog');
					$.ajax({
						url: ajaxurl,
						type: "post",
						dataType: "json",
						data: {
							'action' : 'wproto_editor_button_form',
							'template' : 'wproto_insert_contact_form',
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

										if( window.tinyMCE ) {

											var to = $('#wproto-insert-contact-recipient-email').val();
											var subject = $('#wproto-insert-contact-form-subject').val();
											var title = $('#wproto-insert-contact-form-title').val();
											var text = $('#wproto-insert-contact-form-text').val();
											var form_id = $('#wproto-insert-contact-form-formid').val();
											
											var captchaInput = $('#wproto-insert-contact-form-captcha');
											
											var captcha = captchaInput.is(':checked') ? 'yes' : 'no';

											var insertContent = '[wproto_contact_form form_id="' + form_id + '" to="' + to + '" subject="' + subject + '" title="' + title + '" text="' + text + '" captcha="' + captcha + '"]';
											//ed.execCommand( 'mceInsertContent', false, insertContent );
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