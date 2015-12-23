( function( $ ) {

	// Update the site title in real time...
	wp.customize( 'blogname', function( value ) {
		value.bind( function( newval ) {
			$( '#text-logo .site-title' ).html( newval );
		} );
	} );
	
	//Update the site description in real time...
	wp.customize( 'blogdescription', function( value ) {
		value.bind( function( newval ) {
			$( '#text-logo .site-tagline' ).html( newval );
		} );
	} );
	
	// Color schemes
	wp.customize( 'wproto_color_scheme', function( value ) {
		
		value.bind( function( newval ) {
			
			$('#wproto-main-stylesheet').attr('href', wprotoCustomizer.themeURL + '/css/' + newval + '.css');
			
		} );
	} );
	
	// Boxed layout
	wp.customize( 'wproto_boxed_layout', function( value ) {
		
		value.bind( function( newval ) {
			
			newval == 'yes' ? $('body').addClass('boxed-layout') : $('body').removeClass('boxed-layout');
			
		} );
	} );
	
	// Mega menu style
	wp.customize( 'wproto_mega_menu_style', function( value ) {
		
		value.bind( function( newval ) {
			
			if( newval == 'relative' ) {
				$('li.mega-menu').each( function() {
					$(this).attr('style', 'position: relative !important');
				});
				$('.wproto-mega-menu-content').each( function() {
					$(this).attr('style', 'left: auto !important;');
				});
			} else {
				$('li.mega-menu').each( function() {
					$(this).attr('style', 'position: static !important');
				});
				$('.wproto-mega-menu-content').each( function() {
					$(this).attr('style', 'left: 0 !important;');
				});
			}
			
		} );
	} );
	
	// Custom background color
	wp.customize( 'wproto_bg_color', function( value ) {
		
		value.bind( function( newval ) {
			
			$( 'body' ).attr('style', 'background-color: ' + newval + ' !important' );
			
		} );
	} );
	
	// Boxed layout background image
	wp.customize( 'wproto_boxed_background', function( value ) {
		
		value.bind( function( newval ) {
			
			if( $( 'body' ).hasClass('boxed-layout') ) {
				$( 'body' ).removeClass('pattern-1 pattern-2 pattern-3 pattern-4 pattern-5 pattern-6 pattern-7 pattern-8 pattern-9 pattern-10').attr('style', 'background-image: url(' + newval + ') !important' );
			}
			
		} );
	} );
	
	wp.customize( 'wproto_boxed_background_position', function( value ) {
		
		value.bind( function( newval ) {
			
			if( $( 'body' ).hasClass('boxed-layout') ) {
				$( 'body' ).css('background-position', newval );
			}
			
		} );
	} );
	
	wp.customize( 'wproto_boxed_background_repeat', function( value ) {
		
		value.bind( function( newval ) {
			
			if( $( 'body' ).hasClass('boxed-layout') ) {
				$( 'body' ).css('background-repeat', newval );
			}
			
		} );
	} );
	
	wp.customize( 'wproto_boxed_background_fixed', function( value ) {
		
		value.bind( function( newval ) {
			
			if( $( 'body' ).hasClass('boxed-layout') ) {
				$( 'body' ).css('background-attachment', newval );
			}				
			
		} );
	} );
	
	// Boxed layout pattern
	wp.customize( 'wproto_boxed_pattern', function( value ) {
		
		value.bind( function( newval ) {
			
			$( 'body' ).css('background', '').removeClass('pattern-1 pattern-2 pattern-3 pattern-4 pattern-5 pattern-6 pattern-7 pattern-8 pattern-9 pattern-10').addClass( newval );
			
		} );
	} );
	
	// Header top menu
	wp.customize( 'wproto_header_top_menu', function( value ) {
		
		value.bind( function( newval ) {
			
			newval == 'no' ? $('body').addClass('no-top-menu') : $('body').removeClass('no-top-menu');
			
		} );
	} );
	
	// Custom header layout
	wp.customize( 'wproto_header_layout', function( value ) {
		
		value.bind( function( newval ) {
			
			$( 'body' ).removeClass('header-default header-default-centered header-big-background header-classic header-classic-centered header-full-width').addClass( newval );
			
		} );
	} );
	
	// Primary Font choosel
	wp.customize( 'wproto_primary_font', function( value ) {
		
		value.bind( function( newval ) {
			
			if( $('#font-' + newval ).length == 0 ) {
				$("head").append("<link id='font-" + newval + "' href='https://fonts.googleapis.com/css?family=" + newval + ":300,400,700' rel='stylesheet' type='text/css'>");
			}
			
			var secondaryFont = $( parent.document ).find('#customize-control-wproto_secondary_font select').val();
			
			less.modifyVars({
    		'@font_primary': newval,
    		'@font_secondary': secondaryFont
			});
			
		});
		
	});
	
	// Secondary Font choosel
	wp.customize( 'wproto_secondary_font', function( value ) {
		
		value.bind( function( newval ) {
			
			if( $('#font-' + newval ).length == 0 ) {
				$("head").append("<link id='font-" + newval + "' href='https://fonts.googleapis.com/css?family=" + newval + ":300,400,700' rel='stylesheet' type='text/css'>");
			}
			
			var primaryFont = $( parent.document ).find('#customize-control-wproto_primary_font select').val();
			
			less.modifyVars({
				'@font_primary': primaryFont,
    		'@font_secondary': newval
			});
			
		});
		
	});
	
} )( jQuery );