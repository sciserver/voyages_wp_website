jQuery.noConflict()( function($){
	"use strict";
	
	tinymce.PluginManager.add('wproto_insert_team', function( editor, url ) {
		editor.addButton( 'wproto_insert_team_button', {
			icon: 'mce_wproto_insert_team_button',
			title : wprotoVars.mceButtonTeam,
			onclick: function() {
				
				var shortcodeText = tinyMCE.activeEditor.selection.getContent();
				var shortcodeSettings = new Object;
				
				var matchArray = null;

				if( ( matchArray = shortcodeText.match(/(title)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.title = matchArray[2];
				} 
				if( ( matchArray = shortcodeText.match(/(limit)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.limit = matchArray[2];
				} 
				if( ( matchArray = shortcodeText.match(/(orderby)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.orderby = matchArray[2];
				} 
				if( ( matchArray = shortcodeText.match(/(sort)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.sort = matchArray[2];
				}
				if( ( matchArray = shortcodeText.match(/(category)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.category = matchArray[2];
				}
				if( ( matchArray = shortcodeText.match(/(show)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.show = matchArray[2];
				}
				if( ( matchArray = shortcodeText.match(/(cols)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.cols = matchArray[2];
				} 
				
				$('#wproto-editor-dialog').remove();
				$('<div id="wproto-editor-dialog" title="' + wprotoVars.mceButtonTeam + '"></div>').appendTo('body').hide();
					var dialog = $('#wproto-editor-dialog');
					$.ajax({
						url: ajaxurl,
						type: "post",
						dataType: "json",
						data: {
							'action' : 'wproto_editor_button_form',
							'template' : 'wproto_insert_team',
							'settings' : shortcodeSettings
						},
						beforeSend: function() {
							dialog.html( wprotoVars.adminBigLoaderImage );

							dialog.dialog({
								height: 530,
								width: 450,
								modal: true,
								buttons: {
									"Ok": function() {

										if( window.tinyMCE ) {

											var title = $('#wproto-team-title').val();
											var cols = $('#wproto-team-cols').val();
											var limit = $('#wproto-team-numberposts').val();
											var show = $('#wproto-team-show').val();
											
											var category = show == 'category' ? ' category="' + $('#wproto-team-category').val() + '" ' : '';
											
											var orderby = $('#wproto-team-orderby').val();
											var sort = $('#wproto-team-sort').val();

											var insertContent = '[wproto_team cols="' + cols + '" show="' + show + '" title="' + title + '" limit="' + limit + '" orderby="' + orderby + '" sort="' + sort + '"' + category + ']';
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