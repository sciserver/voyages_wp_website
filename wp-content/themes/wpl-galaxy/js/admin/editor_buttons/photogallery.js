jQuery.noConflict()( function($){
	"use strict";
	
	tinymce.PluginManager.add('wproto_insert_photogallery', function( editor, url ) {
		editor.addButton( 'wproto_insert_photogallery_button', {
			icon: 'mce_wproto_insert_photogallery_button',
			title : wprotoVars.mceButtonPhotogallery,
			onclick: function() {
				
				var shortcodeText = tinyMCE.activeEditor.selection.getContent();
				var shortcodeSettings = new Object;
				
				var matchArray = null;

				if( ( matchArray = shortcodeText.match(/(album)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.album = matchArray[2];
				} 
				
				if( ( matchArray = shortcodeText.match(/(title)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.title = matchArray[2];
				}
				
				if( ( matchArray = shortcodeText.match(/(limit)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.limit = matchArray[2];
				}  
				
				$('#wproto-editor-dialog').remove();
				$('<div id="wproto-editor-dialog" title="' + wprotoVars.mceButtonPhotogallery + '"></div>').appendTo('body').hide();
					var dialog = $('#wproto-editor-dialog');
					$.ajax({
						url: ajaxurl,
						type: "post",
						dataType: "json",
						data: {
							'action' : 'wproto_editor_button_form',
							'template' : 'wproto_insert_photogallery',
							'settings' : shortcodeSettings
						},
						beforeSend: function() {
							dialog.html( wprotoVars.adminBigLoaderImage );

							dialog.dialog({
								height: 350,
								width: 450,
								modal: true,
								buttons: {
									"Ok": function() {

										if( window.tinyMCE ) {

											var album = $('#wproto-photogallery-album').val();
											var title = $('#wproto-photogallery-title').val();
											var limit = $('#wproto-photogallery-limit').val();

											var insertContent = '[wproto_photoalbums album="' + album + '" title="' + title + '" limit="' + limit + '"]';
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