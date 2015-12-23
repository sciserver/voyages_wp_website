jQuery.noConflict()( function($){
	"use strict";
	
	tinymce.PluginManager.add('wproto_insert_animation', function( editor, url ) {
		editor.addButton( 'wproto_insert_animation_button', {
			icon: 'mce_wproto_insert_animation_button',
			title : wprotoVars.mceButtonAnimation,
			onclick: function() {
				
				var shortcodeText = tinyMCE.activeEditor.selection.getContent();
				var currentAnimation = '';
				
				var matchArray = null;
				
				if( ( matchArray = shortcodeText.match(/(data\-appear\-animation)=["|']{1}(.*?)["|']{1}/i)) != null ) {
					currentAnimation = matchArray[2];
				} 

				$('#wproto-editor-dialog').remove();
				$('<div id="wproto-editor-dialog" title="' + wprotoVars.mceButtonAnimation + '"></div>').appendTo('body').hide();
				var dialog = $('#wproto-editor-dialog');
				$.ajax({
					url: ajaxurl,
					type: "post",
					dataType: "json",
					data: {
						'action' : 'wproto_editor_button_form',
						'template' : 'wproto_insert_animation',
						'current_animation' : currentAnimation
					},
					beforeSend: function() {
						dialog.html( wprotoVars.adminBigLoaderImage );

						dialog.dialog({
							height: 280,
							width: 400,
							modal: true,
							buttons: {
								"Ok": function() {

									var animation = $('#wproto-add-amination-select').val();
									var selection = tinyMCE.activeEditor.selection;
									var imageHTML = selection.getContent();
									
									var tempDiv = $( '#wproto-temporary-div' );
									
									tempDiv.html( imageHTML );			
									
									if( animation == '' ) {
										tempDiv.find('img').removeAttr('data-appear-animation');
									} else {
										tempDiv.find('img').attr('data-appear-animation', animation );
									}
									
									if ( typeof selection != "undefined" ) {
										selection.setContent( tempDiv.html() );
									}
									
									$( this ).dialog( "close" );

                                                                                        
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