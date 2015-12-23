jQuery.noConflict()( function($){
	"use strict";
	
	tinymce.PluginManager.add('wproto_column_formatting', function( editor, url ) {
		editor.addButton( 'wproto_column_formatting_button', {
			icon: 'mce_wproto_colum_formatter_button',
			title : wprotoVars.mceButtonColumnFormatting,
			type: 'menubutton',
			menu: [
				{
					text: wprotoVars.strFullWidth,
					onclick: function() {
						
						
							wprotoRegisterTinyMCEFormats();
						
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
							tinyMCE.activeEditor.formatter.remove('golden-small');
							tinyMCE.activeEditor.formatter.remove('golden-large');
							
							tinyMCE.activeEditor.formatter.toggle('whole');
					}
				},
				{
					text: '1/2',
					onclick: function() {
						
						
							wprotoRegisterTinyMCEFormats();
						
							tinyMCE.activeEditor.formatter.remove('whole');
							tinyMCE.activeEditor.formatter.remove('one-third');
							tinyMCE.activeEditor.formatter.remove('two-thirds');
							tinyMCE.activeEditor.formatter.remove('one-quarter');
							tinyMCE.activeEditor.formatter.remove('three-quarters');
							tinyMCE.activeEditor.formatter.remove('one-fifth');
							tinyMCE.activeEditor.formatter.remove('one-sixth');
							tinyMCE.activeEditor.formatter.remove('two-fifths');
							tinyMCE.activeEditor.formatter.remove('three-fifths');
							tinyMCE.activeEditor.formatter.remove('four-fifths');
							tinyMCE.activeEditor.formatter.remove('golden-small');
							tinyMCE.activeEditor.formatter.remove('golden-large');
							
							tinyMCE.activeEditor.formatter.toggle('half');
					}
				},
				{
					text: '1/3',
					onclick: function() {
						
						
							wprotoRegisterTinyMCEFormats();
						
							tinyMCE.activeEditor.formatter.remove('whole');
							tinyMCE.activeEditor.formatter.remove('half');
							tinyMCE.activeEditor.formatter.remove('two-thirds');
							tinyMCE.activeEditor.formatter.remove('one-quarter');
							tinyMCE.activeEditor.formatter.remove('three-quarters');
							tinyMCE.activeEditor.formatter.remove('one-fifth');
							tinyMCE.activeEditor.formatter.remove('one-sixth');
							tinyMCE.activeEditor.formatter.remove('two-fifths');
							tinyMCE.activeEditor.formatter.remove('three-fifths');
							tinyMCE.activeEditor.formatter.remove('four-fifths');
							tinyMCE.activeEditor.formatter.remove('golden-small');
							tinyMCE.activeEditor.formatter.remove('golden-large');
							
							tinyMCE.activeEditor.formatter.toggle('one-third');
					}
				},
				{
					text: '1/4',
					onclick: function() {
						
						
							wprotoRegisterTinyMCEFormats();
						
							tinyMCE.activeEditor.formatter.remove('whole');
							tinyMCE.activeEditor.formatter.remove('half');
							tinyMCE.activeEditor.formatter.remove('one-third');
							tinyMCE.activeEditor.formatter.remove('two-thirds');
							tinyMCE.activeEditor.formatter.remove('three-quarters');
							tinyMCE.activeEditor.formatter.remove('one-fifth');
							tinyMCE.activeEditor.formatter.remove('one-sixth');
							tinyMCE.activeEditor.formatter.remove('two-fifths');
							tinyMCE.activeEditor.formatter.remove('three-fifths');
							tinyMCE.activeEditor.formatter.remove('four-fifths');
							tinyMCE.activeEditor.formatter.remove('golden-small');
							tinyMCE.activeEditor.formatter.remove('golden-large');
							
							tinyMCE.activeEditor.formatter.toggle('one-quarter');
					}
				},
				{
					text: '2/3',
					onclick: function() {
						
						
							wprotoRegisterTinyMCEFormats();
						
							tinyMCE.activeEditor.formatter.remove('whole');
							tinyMCE.activeEditor.formatter.remove('half');
							tinyMCE.activeEditor.formatter.remove('one-third');
							tinyMCE.activeEditor.formatter.remove('one-quarter');
							tinyMCE.activeEditor.formatter.remove('three-quarters');
							tinyMCE.activeEditor.formatter.remove('one-fifth');
							tinyMCE.activeEditor.formatter.remove('one-sixth');
							tinyMCE.activeEditor.formatter.remove('two-fifths');
							tinyMCE.activeEditor.formatter.remove('three-fifths');
							tinyMCE.activeEditor.formatter.remove('four-fifths');
							tinyMCE.activeEditor.formatter.remove('golden-small');
							tinyMCE.activeEditor.formatter.remove('golden-large');
							
							tinyMCE.activeEditor.formatter.toggle('two-thirds');
					}
				},
				{
					text: '3/4',
					onclick: function() {
						
						
							wprotoRegisterTinyMCEFormats();
						
							tinyMCE.activeEditor.formatter.remove('whole');
							tinyMCE.activeEditor.formatter.remove('half');
							tinyMCE.activeEditor.formatter.remove('one-third');
							tinyMCE.activeEditor.formatter.remove('two-thirds');
							tinyMCE.activeEditor.formatter.remove('one-quarter');
							tinyMCE.activeEditor.formatter.remove('one-fifth');
							tinyMCE.activeEditor.formatter.remove('one-sixth');
							tinyMCE.activeEditor.formatter.remove('two-fifths');
							tinyMCE.activeEditor.formatter.remove('three-fifths');
							tinyMCE.activeEditor.formatter.remove('four-fifths');
							tinyMCE.activeEditor.formatter.remove('golden-small');
							tinyMCE.activeEditor.formatter.remove('golden-large');
							
							tinyMCE.activeEditor.formatter.toggle('three-quarters');
					}
				},
				{
					text: '1/5',
					onclick: function() {
						
						
							wprotoRegisterTinyMCEFormats();
						
							tinyMCE.activeEditor.formatter.remove('whole');
							tinyMCE.activeEditor.formatter.remove('half');
							tinyMCE.activeEditor.formatter.remove('one-third');
							tinyMCE.activeEditor.formatter.remove('two-thirds');
							tinyMCE.activeEditor.formatter.remove('one-quarter');
							tinyMCE.activeEditor.formatter.remove('three-quarters');
							tinyMCE.activeEditor.formatter.remove('one-sixth');
							tinyMCE.activeEditor.formatter.remove('two-fifths');
							tinyMCE.activeEditor.formatter.remove('three-fifths');
							tinyMCE.activeEditor.formatter.remove('four-fifths');
							tinyMCE.activeEditor.formatter.remove('golden-small');
							tinyMCE.activeEditor.formatter.remove('golden-large');
							
							tinyMCE.activeEditor.formatter.toggle('one-fifth');
					}
				},
				{
					text: '1/6',
					onclick: function() {
						
						
							wprotoRegisterTinyMCEFormats();
						
							tinyMCE.activeEditor.formatter.remove('whole');
							tinyMCE.activeEditor.formatter.remove('half');
							tinyMCE.activeEditor.formatter.remove('one-third');
							tinyMCE.activeEditor.formatter.remove('two-thirds');
							tinyMCE.activeEditor.formatter.remove('one-quarter');
							tinyMCE.activeEditor.formatter.remove('three-quarters');
							tinyMCE.activeEditor.formatter.remove('one-fifth');
							tinyMCE.activeEditor.formatter.remove('two-fifths');
							tinyMCE.activeEditor.formatter.remove('three-fifths');
							tinyMCE.activeEditor.formatter.remove('four-fifths');
							tinyMCE.activeEditor.formatter.remove('golden-small');
							tinyMCE.activeEditor.formatter.remove('golden-large');
							
							tinyMCE.activeEditor.formatter.toggle('one-sixth');
					}
				},
				{
					text: '2/5',
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
							tinyMCE.activeEditor.formatter.remove('three-fifths');
							tinyMCE.activeEditor.formatter.remove('four-fifths');
							tinyMCE.activeEditor.formatter.remove('golden-small');
							tinyMCE.activeEditor.formatter.remove('golden-large');
							
							tinyMCE.activeEditor.formatter.toggle('two-fifths');
					}
				},
				{
					text: '3/5',
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
							tinyMCE.activeEditor.formatter.remove('four-fifths');
							tinyMCE.activeEditor.formatter.remove('golden-small');
							tinyMCE.activeEditor.formatter.remove('golden-large');
							
							tinyMCE.activeEditor.formatter.toggle('three-fifths');
					}
				},
				{
					text: '4/5',
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
							tinyMCE.activeEditor.formatter.remove('golden-small');
							tinyMCE.activeEditor.formatter.remove('golden-large');
							
							tinyMCE.activeEditor.formatter.toggle('four-fifths');
					}
				},
				{
					text: wprotoVars.strGoldenLarge,
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
							tinyMCE.activeEditor.formatter.remove('golden-small');
							
							tinyMCE.activeEditor.formatter.toggle('golden-large');
					}
				},
				{
					text: wprotoVars.strGoldenSmall,
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
							
							tinyMCE.activeEditor.formatter.toggle('golden-small');
					}
				},
				{
					text: wprotoVars.strRemove,
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
				}
			]
		});
	});
	
	
	var defaultEditor = $('#content');
	if( defaultEditor.length && window.tinymce ) {
		
		setTimeout("try{tinymce.get('content').focus()}catch(e){}", 1000);

	}
	
});