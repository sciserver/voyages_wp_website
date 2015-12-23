jQuery.noConflict()( function($){
	"use strict";
	
	tinymce.PluginManager.add('wproto_insert_benefits', function( editor, url ) {
		editor.addButton( 'wproto_insert_benefits_button', {
			icon: 'mce_wproto_insert_benefits_button',
			title : wprotoVars.mceButtonBenefits,
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
				if( ( matchArray = shortcodeText.match(/(cols)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					shortcodeSettings.cols = matchArray[2];
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
				
				$('#wproto-editor-dialog').remove();
				$('<div id="wproto-editor-dialog" title="' + wprotoVars.mceButtonBenefits + '"></div>').appendTo('body').hide();
					var dialog = $('#wproto-editor-dialog');
					$.ajax({
						url: ajaxurl,
						type: "post",
						dataType: "json",
						data: {
							'action' : 'wproto_editor_button_form',
							'template' : 'wproto_insert_benefits',
							'settings' : shortcodeSettings
						},
						beforeSend: function() {
							dialog.html( wprotoVars.adminBigLoaderImage );

							dialog.dialog({
								height: 510,
								width: 450,
								modal: true,
								buttons: {
									"Ok": function() {

										if( window.tinyMCE ) {

											var title = $('#wproto-benefits-title').val();
											var limit = $('#wproto-benefits-numberposts').val();
											var show = $('#wproto-benefits-show').val();
											var cols = $('#wproto-benefits-cols').val();
											
											var category = show == 'category' ? ' category="' + $('#wproto-benefits-category').val() + '" ' : '';
											
											var orderby = $('#wproto-benefits-orderby').val();
											var sort = $('#wproto-benefits-sort').val();

											var insertContent = '[wproto_benefits show="' + show + '" cols="' + cols + '" title="' + title + '" limit="' + limit + '" orderby="' + orderby + '" sort="' + sort + '"' + category + ']';
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