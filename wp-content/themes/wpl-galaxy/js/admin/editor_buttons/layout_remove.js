jQuery.noConflict()( function($){
	"use strict";
	
	tinymce.PluginManager.add('wproto_remove_column_formatting', function( editor, url ) {
		editor.addButton( 'wproto_remove_column_formatting_button', {
			icon: 'mce_wproto_remove_column_formatting_button',
			title : wprotoVars.mceButtonRemoveColumnFormatting,
			onclick: function() {
				
				wprotoRegisterTinyMCEFormats();
				
				tinyMCE.activeEditor.formatter.remove('whole');
				tinyMCE.activeEditor.formatter.remove('half');
				tinyMCE.activeEditor.formatter.remove('one-third');
				tinyMCE.activeEditor.formatter.remove('two-thirds');
				tinyMCE.activeEditor.formatter.remove('one-quarter');
				tinyMCE.activeEditor.formatter.remove('three-quarters');
				tinyMCE.activeEditor.formatter.remove('one-fifth');
				tinyMCE.activeEditor.formatter.remove('one-sixth');
				tinyMCE.activeEditor.formatter.remove('two-fifths');
				tinyMCE.activeEditor.formatter.remove('three-fifths');
				tinyMCE.activeEditor.formatter.remove('four-fifths');
				tinyMCE.activeEditor.formatter.remove('golden-large');
				tinyMCE.activeEditor.formatter.remove('golden-small');
				
			}
		});
	});
	
});