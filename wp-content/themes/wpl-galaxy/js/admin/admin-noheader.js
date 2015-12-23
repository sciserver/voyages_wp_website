jQuery.noConflict()( function($){
	"use strict";
	
	$('#wpadminbar').remove();
	$('html, #wpcontent').attr('style', 'padding-top: 0 !important;');
	
});