/* ========================================================================
 * solarsystemsearch v1.0.0
 * ========================================================================
 *
 * What it does:
 * 		Creates a sql search form that submits the form's query to 
 *		casjobs rest spi.
 * 
 * Licensed under MIT 
 * ======================================================================== */
(function($) {
	'use strict';

	// PUBLIC CLASS DEFINITION
	// ================================

	var SSSWPDEBUG = true;
	
	var solarsystemsearch = {

		context: '#ssswp-container',
		
		levels: [
			'info',
			'warning',
			'danger',
		],
		
		targets: {
			mpcorb:{
				url:"https://skyserver.sdss.org/casjobs/RestAPI/contexts/mpcorb/query",
				ContentType:"application/json",
				type: "POST",
				data:{"Query":"","Accept":"application/xml"},
				success: function (data) {
					solarsystemsearch.showResults( data , false , true );
				},
				//,processData: false
			}
		},
		
	
		init: function(  ){
						
			var s=this;
			
			// get base url, query template, and which form we are dealing with.
			var webroot = $( solarsystemsearch.context ).data('ssswp-webroot');
			var basequery = $( solarsystemsearch.context ).data('ssswp-query');
			var which = $( solarsystemsearch.context ).data('ssswp-which');
			var target = solarsystemsearch.targets[which];
			var query = $('#ssswp-query').text();

			// Show the Search Page
			this.showForm( solarsystemsearch.context , false , true );
			this.showResults( '' , false , false );
			
			// Prevent form submitting/reloading page
			$( solarsystemsearch.context ).on( "submit" , "form#ssswp-form" , function( e ){ e.preventDefault(); });
			
			// Add (delegated) click event handlers to controls
			if ( which === 'mpcorb' ) {
				
				$( solarsystemsearch.context ).on( "change" , "#ssswp-num" , solarsystemsearch.doRegenerate );
				$( solarsystemsearch.context ).on( "change" , "#ssswp-coords" , solarsystemsearch.doRegenerate );
			}
			$( solarsystemsearch.context ).on( "click" , "#ssswp-submit" , { query: query , target:target , which:which } , solarsystemsearch.doSubmit );
			//$( solarsystemsearch.context ).on( "click" , "#ssswp-reset" , solarsystemsearch.doReset );
			//$( solarsystemsearch.context ).on( "click" , "#ssswp-syntax" , solarsystemsearch.doSyntax );
			
		},
		
		/**
		 * @summary Submits form data queries target 
		 * 
		 * @param Object e Event Object
		**/
		doSubmit: function( e ) {
			if (SSSWPDEBUG) { console.log('doSubmit'); }
			
			//if (SSSWPDEBUG) { console.log( e.data ); }
			
			var query = e.data.query;
			var target = e.data.target;
			var which = e.data.which;
			
			if ( which === 'mpcorb' ) {
				
				target.data = {"Query":query};
				//if (SSSWPDEBUG) { console.log( target ); }
				$.ajax( target );
				
			} else {
				
				//send query from form to skyserverws and listen for return
				var xhttp;
				xhttp = new XMLHttpRequest();
				xhttp.onreadystatechange = function() {
					if (this.readyState === 4 && this.status === 200) {
						var response = this.responseText;
						response = response.replace(/.*<body.*?>/i , "");
						response = response.replace(/<\/body.*/i , "");

						sqlsearchwp.showResults( response , false , true );
						sqlsearchwp.showForm( '' , true , false );
					}
				};
				xhttp.open("GET", query , true);
				xhttp.send();
			}
			
		},
		
		/**
		 * @summary Regenerates query in textarea
		 * 
		 * @param Object e Event Object
		**/
		doRegenerate: function( e ) {
			if (SSSWPDEBUG) { console.log('doRegenerate'); }
		},
		
		/**
		 * @summary Sends form data to skyserverws for syntax review
		 * 
		 * @param Object e Event Object
		**/
		doSyntax: function( e ) {
			if (SSSWPDEBUG) { console.log('doSyntax'); }
			// Get target db from form data
			var where = $( solarsystemsearch.context ).data('ssswp-where');
			var query = solarsystemsearch.wheres[where] +
				encodeURI( $( '#ssswp-query' ).val() ) +
				'&syntax=Syntax';
				
			//send query from form to skyserverws and listen for return
			var xhttp;
			xhttp = new XMLHttpRequest();
			xhttp.onreadystatechange = function() {
				if (this.readyState === 4 && this.status === 200) {
					var response = this.responseText;
					solarsystemsearch.showResults( response , false , true );
					//solarsystemsearch.showForm( '' , true , true );
				}
			};
			xhttp.open("GET", query , true);
			xhttp.send();
		},
		
		/**
		 * @summary Resets form data
		 * 
		 * @param Object e Event Object
		**/
		doReset: function( e ) {
			if (SSSWPDEBUG) { console.log('reset form'); }
			// Reset query - don't do this while testing...
			solarsystemsearch.showResults( '' , false , false );
			solarsystemsearch.showForm( solarsystemsearch.context , false , true );
		},
		
		doCollapse: function( toggle, container, show ) {
			$('.collapse').collapse();
			if ( show === true ) {
				$(container).collapse('show');
			} else {
				$(container).collapse('hide');
			}
			/*/
				$( container ).addClass('collapse in');
				$( container ).removeClass('in');
			/*/
		},
		
		/**
		 * @summary Appends or updates the displayed messages.
		 * 
		 * @param String $title Message Title
		 * @param String $msg Message text
		 * @param String $level One of info, warning, error
		 * @param Boolean $append Append or replace current message(s)
		**/
		showMessages: function( title , msg , level , append ) {
			var msgContainer = $( '.ssswp-messages' )[0];
			var msgWrapper = $( '.ssswp-messages-wrap' )[0];
			
			// Append or replace existing contents
			var message = ( append !== undefined && append ) ? $(msgContainer).html() : '' ;
			
			// Class for error level
			var msgLevel = ( ( level !== undefined ) && ( solarsystemsearch.levels.indexOf( level ) >= 0 ) ) ? 'alert-'+level : 'alert-primary' ;
			
			// Put Content in alert
			message += ( title !== undefined ) ? 
				'<h3 class="ssswp-msg-title ' + msgLevel + ' ">' + 
					'<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>' +
					title + '</h3>' : 
				'' ;
			message += ( msg !== undefined ) ? 
				'<div class="ssswp-msg-body ' + msgLevel + ' ">'+
					msg + '</div>' : 
				'' ;
			message = '<div class="alert ' + msgLevel + ' alert-dismissable ssswp-msg" role="alert">' + message + '</div>';
			$(msgContainer).html( message );
			
			// Hide if empty
			$( msgWrapper ).show();
			if ( $(msgContainer).html().length === 0 ) {
				$( msgWrapper ).hide();
			} 
		},
		
		showForm: function( context , append , show ) {
			var container = $( '#ssswp-form' );
			//var contents = ( append !== undefined && append ) ? $(container).html() : '' ;
			//var query = solarsystemsearch.query[ $( context ).data('ssswp-which') ];
			//$( '#ssswp-query' ).prop( 'value' , query );
			solarsystemsearch.doCollapse( '#ssswp-form-wrap>h2>a:[data-toggle]', container, show );
			
		},
		
		/**
		 * @summary Appends or updates the displayed Results.
		 * 
		 * @param String $results Results to display
		 * @param Boolean $append Append or replace current message(s)
		**/
		showResults: function( results , append , show ) {
			var container = $( '#ssswp-results' );

			var contents = ( append !== undefined && append ) ? $(container).html() : '' ;
			
			contents += ( results !== undefined ) ? '<pre>'+results+'</pre>' : '' ;
			$(container).html( contents );
			/*/
			if ( show ) {
				$( container ).addClass('collapse in');
			} else {
				$( container ).removeClass('in');
			}
			/*/
			solarsystemsearch.doCollapse( '#ssswp-results-wrap>h2>a:[data-toggle]', container, show );
		},
	};

	$(document).ready( function(  ) {
		if ( $( '#ssswp-container' ).length === 1 ) {
			solarsystemsearch.init(  );
		} else {
			if (SSSWPDEBUG) { console.log('Error running solarsystemsearch.js. Only one "#ssswp-container" expected, found'+ $( '#ssswp-container' ).length +'.');}
		}
	} );
	
})(jQuery);