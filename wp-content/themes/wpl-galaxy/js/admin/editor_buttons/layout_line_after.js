jQuery.noConflict()( function($){
	"use strict";
	
	tinymce.PluginManager.add('wproto_insert_line_after', function( editor, url ) {
		editor.addButton( 'wproto_insert_line_after_button', {
			icon: 'mce_wproto_insert_line_after_button',
			title : wprotoVars.mceButtonLineAfter,
			onclick: function() {
				
				if( window.tinyMCE ) {
					var node = tinyMCE.activeEditor.selection.getNode(),
					parents	= tinyMCE.activeEditor.dom.getParents(node).reverse(),
					oldestParent = parents[2];
					var blank = document.createElement('p');
			
					blank.innerHTML = "&nbsp;";
			
					if (typeof oldestParent != "undefined") {
						var n = tinyMCE.activeEditor.dom.insertAfter(blank, oldestParent);
					} else if (typeof node != "undefined") {
						var n = tinyMCE.activeEditor.dom.insertAfter(blank, node);
					}
							
					tinyMCE.activeEditor.selection.select(n);

				}
				
			}
		});
	});
	
});