jQuery.noConflict()( function($){
	"use strict";

	var Core = {
	
		/**
			Constructor
		**/
		initialize: function() {

			this.build();
			this.events();

		},
		/**
			Build page elements, plugins init
		**/
		build: function() {
		
			var self = this;
		
			$('html').removeClass('no-js');
		
			if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
				$('html').addClass('mobile');
			}
			
			if (location.hash && $('.single-product').length ) {
				location.hash = '';
        window.scrollTo(0, 0);
        setTimeout(function() {
            window.scrollTo(0, 0);
        }, 1);
    	}
    	
    	if( $('body.page-template-page-tpl-one-page-php').length ) {

				$('body.page-template-page-tpl-one-page-php ul.menu').onePageNav({
					currentClass: 'current_page_item',
					changeHash: false,
 					scrollSpeed: 750,
  				scrollOffset: 85,
  				filter: ':not(.external)'
				});
				
				if( $(window).width() <= 767 ) {
					$('body.page-template-page-tpl-one-page-php .big-header-wrapper').removeClass('scrolled');
				} 
				
    	}
    	
    	$( window ).resize(function() {
				if( $(window).width() <= 767 ) {
					$('.big-header-wrapper').removeClass('scrolled');
				} else {
					$('body.page-template-page-tpl-one-page-php .big-header-wrapper').addClass('scrolled');
				}
   		});
		
			// table odd even
			$('.post #content table tr:odd').addClass('odd');
			$('.post #content table tr:even').addClass('even');
			
			$('.post-text').fitVids();
			
			// Menu Angles
			this.setupMenuAngles();
			
			// Custom inputs
			this.setupCustomInputs();
		
			// Setup page sliders
			this.setupSliders();
			
			this.setupTabs();
			
			// page loader progress bar
			$( document ).waitForImages( {
				finished: function() {
					self.setupSliders();
    		}
			});
			
			// Create toggles
			this.setupToggles();
		
			// Setup page carousels
			this.setupCarousels();
		
			// Setup another required plugins
			this.setupPlugins();
			
			// Setup homepage
			this.setupHomepages();
			
			if( $('#about-author-section .social-icons a').length == 0 ) {
				$('#about-author-section .social-icons').remove();
			}
		
		},
		/**
			Set page events
		**/
		events: function() {
		
			var self = this;
		
			// init CSS animations
			this.initAnimations();
		
			// page loader progress bar
			$( document ).waitForImages( {
				finished: function() {
					NProgress.done(true);
    		},
    		each: function() {
					NProgress.inc();
    		}
			});
		
			// Header menu scrolling
			this.navMenu();
		
			// Custom slider events
			this.sliderEvents();
			
			// Contact form submit
			this.bindContactForm();
			
			// Validate comments form
			this.validateCommentsForm();
			
			// Posts and comments likes
			this.bindLikes();
			
			// AJAX Pagination
			if( jQuery('#wproto-load-more-posts-link').length ) {
		
				jQuery('#wproto-load-more-posts-link').on( 'click', function() {
			
					var loader = jQuery(this).find('i');
			
					var max_pages = jQuery(this).data('max-pages');
			
					var current_page = jQuery(this).data('current-page');
					var next_page = jQuery(this).data('next-page');
					var post_type = jQuery(this).data('post-type');
					var taxonomy_name = jQuery(this).data('taxonomy-name');
					var taxonomy_term = jQuery(this).data('taxonomy-term');
					var loop_template = jQuery(this).data('loop-template');
					var search_string = jQuery(this).data('search-string');
					var posts_per_page = jQuery(this).data('posts_per_page');
					var display_type = jQuery(this).data('display-type');
					var current_author = jQuery(this).data('author');
			
					var link = jQuery(this);
			
					jQuery.ajax({
						url: wprotoEngineVars.ajaxurl,
						type: "POST",
						dataType : 'json',
						data: {
							'action' : 'wproto_ajax_pagination',
							'max_pages' : max_pages,
							'current_page' : current_page,
							'next_page' : next_page,
							'post_type' : post_type,
							'taxonomy_name' : taxonomy_name,
							'taxonomy_term' : taxonomy_term,
							'loop_template' : loop_template,
							'search_string' : search_string,
							'display_type' : display_type,
							'posts_per_page' : posts_per_page,
							'current_author' : current_author
						},
						beforeSend: function() {
							NProgress.start();
							loader.addClass('fa-spin');
						},
						success: function( response ) {
							loader.removeClass('fa-spin');
							NProgress.done(true);
										
							link.data( 'current-page', response.current_page );
							link.data( 'next-page', response.next_page );
					
							if( response.next_page > max_pages || response.hide_link == 'yes' ) {
								link.hide();
							}
					
							if( response.html ) {
								
								if( loop_template == 'masonry' ) {
										
									$('#ajax-pagination-response-container').append( response.html ).masonry('reloadItems').masonry({
										itemSelector: 'article.post',
										isAnimated: true,
										columnWidth: '.masonry-grid-sizer'
									});
									
									$('#ajax-pagination-response-container').waitForImages( {
										finished: function() {
											self.setupSliders();
											$('#ajax-pagination-response-container').masonry({
												itemSelector: 'article.post',
												isAnimated: true,
												columnWidth: '.masonry-grid-sizer'
											});
 										}
 									});

								} else {
									$('#ajax-pagination-response-container').append( response.html );
									self.setupSliders();
									self.setupTabs();
								}
								
								/*
								if ( History.enabled ) {
							
									if( wprotoEngineVars.isSearch == true ) {
										History.pushState( null, null, wprotoEngineVars.homeUrl + "?s=" + wprotoEngineVars.searchVar + '&paged=' + response.current_page );

									} else if( wprotoEngineVars.permalinksEnabled == false ) {
										var pattern = /&paged=[0-9]+\/?/i;
										var loc = window.location.toString();
										var newloc = loc.replace( pattern, '');
								
										History.pushState( null, null, newloc + '&paged=' + response.current_page );
									} else {
										var pattern = /\page\/[0-9]+\/?/i;
										var loc = window.location.toString();
										var newloc = loc.replace( pattern, '');
								
										History.pushState( null, null, newloc + "page/" + response.current_page + '/' );
									}
							
								}*/
						
							}

						},
						error: function() {
							loader.removeClass('fa-spin');
							NProgress.done(true);
							self.alertMessage( wprotoEngineVars.strServerResponseError );
						},
						ajaxError: function() {
							loader.removeClass('fa-spin');
							NProgress.done(true);
							self.alertMessage( wprotoEngineVars.strAJAXError );
						}
					});
			
					return false;
				});
		
			}
			
			/**
				Header AJAX cart
			**/
			$('header.small .my-cart').hover( function() {
				
				if( $('html').hasClass('mobile') || $(window).width() <= 767 ) {
					return false;
				}
				
				var link = $(this);
				
				if( link.hasClass('cart-opened') == false ) {
					
					link.addClass('cart-opened');
					$('#wproto-ajax-header-cart .ajax-loader').show();
					$('#wproto-ajax-header-cart .cart-content').html('').width('auto');
					$('#wproto-ajax-header-cart').fadeIn('fast');
				
					$.ajax({
						url: wprotoEngineVars.ajaxurl,
						type: "POST",
						data: {
							'action' : 'wproto_header_ajax_cart'
						},
						beforeSend: function() {
							NProgress.start();
						},
						success: function( html ) {
							NProgress.done(true);
							$('#wproto-ajax-header-cart .ajax-loader').hide();
							$('#wproto-ajax-header-cart .cart-content').animate({
								width: 294
							}, 500, function() {
								$(this).html( html );
							});
						
						},
						error: function() {
							NProgress.done(true);
						},
						ajaxError: function() {
							NProgress.done(true);
						}
					});
					
				}
				
			});
			
			$('#wproto-ajax-header-cart').hover( function() {
				
			}, function() {
				$(this).fadeOut('fast');
				$('header.small .my-cart').removeClass('cart-opened');
			});
			
			$('#wproto-close-ajax-cart').on( 'click', '#wproto-ajax-header-cart', function() {
				$('#wproto-ajax-header-cart').fadeOut('fast');
				$('header.small .my-cart').removeClass('cart-opened');
			});
			
			$(window).scroll(function(){
				$('#wproto-ajax-header-cart').fadeOut('fast');
				$('header.small .my-cart').removeClass('cart-opened');
			});
			
			// Google Map
			if( typeof( google ) != 'undefined' && jQuery('#google-map-contact').length ) {
				google.maps.event.addDomListener( window, "load", this.setupGoogleMap );
			}
		
			// top search form submit handler
			$('#top-search-form a, .search-form a.button').click( function() {
				$(this).parents('form').submit();
				return false;
			});
		
			/**
				Toggle mobile menu
			**/
			$('#phone-toggle-menu').click( function() {
				$('#header-menu').toggleClass('hide-on-phone').toggleClass('opened');
				return false;
			});
		
			// change shop view list/grid
			$('.change-shop-view').click( function() {
		
				var target = $('#shop-posts-list');
				var input = $(this).parents('.pull-right').find('input[type=hidden]');
		
				$('a.change-shop-view').removeClass('current');
		
				if( $(this).hasClass('view-grid') ) {
					target.removeClass('view-list').addClass('view-grid');
					input.val('grid');
				}
		
				if( $(this).hasClass('view-list') ) {
					target.removeClass('view-grid').addClass('view-list');
					input.val('list');
				}
		
				$(this).addClass('current');
		
				return false;
			});
		
			// toggle product categories
			$('.widget_product_categories i.toggle').click( function() {
		
				var parent = $(this).parents('.widget_product_categories');
				$(this).toggleClass('opened');
				$(this).parent().parent().find('ul:first').slideToggle( 400 );
		
				return false;
			});
			
			// home portfolio hover
			$('.portfolio-items .item').hover( function() {
				$(this).find('a.icon-zoom, a.icon-document').addClass('bounceIn animated');
			}, function() {
				$(this).find('a.icon-zoom, a.icon-document').removeClass('bounceIn animated');
			});
			
			// shipping address changed
			$('#ship_to_different_address').change( function() {
				var val = jQuery(this).attr('checked');
				var target = $('.shipping_address');
				val == 'checked' ? target.fadeIn() : target.fadeOut();
			});
			
			// shipping method change
			$('.payment_methods input[type=radio]').change( function() {
				$('div.payment_box').hide();
				$(this).parents('li').find('div.payment_box').fadeIn();
			});
			
			// videos play
			$('.video-link').magnificPopup({
				type: 'iframe',
				removalDelay: 100,
				mainClass: 'mfp-fade',
				zoom: {
					enabled: true,
					duration: 300
				},
				gallery: {
					enabled: true,
					navigateByImgClick: true
				}
			});
			
			// images lightbox
			$('.post-text a > img:not(.attachment-shop_thumbnail)').each( function() {
				$( this ).parent().magnificPopup({
					type: 'image',
					removalDelay: 100,
					mainClass: 'mfp-fade',
					zoom: {
						enabled: true,
						duration: 300
					}
				});
			});
			
			$('.small-image-link').click( function() {
				
				$('.woocommerce-main-image > img').attr('src', $(this).data('medium-src'));
				
				$('.woocommerce-main-image').attr('href', $(this).data('full-src'));
				
				return false;
			});
		
			/**
				Body parallax
			**/
			$('.parallax').each(function(){
				
				var sectionHeight = $(this).next('.parallax-content').height();
				$(this).height( sectionHeight + 'px' );
				
				var parallaxItem = $(this);
				$(window).scroll(function() {
					if( $(window).width() > 767 ) {
						var yPos = -( Math.floor($(window).scrollTop() / parallaxItem.data('parallax-speed')) ); 
						var coords = 'center '+ yPos + 'px';	
										
						parallaxItem.css({ backgroundPosition: coords });
					}
				});
			});
			
			$( window ).resize(function() {
				$('.parallax').each(function(){
					var sectionHeight = $(this).next('.parallax-content').height();
					$(this).height( sectionHeight + 'px' );
				});
			});
			
			/**
				IE8 Placeholders
			**/
			$('.ie8 input[placeholder], .ie8 textarea[placeholder]').each( function() {
				$(this).val( $(this).attr('placeholder') );
				
				$(this).focus( function() {
					if( this.value == $(this).attr('placeholder') ) this.value = '';
				});
				
				$(this).blur( function() {
					if( $.trim( $(this).val() ) == '' ) $(this).val( $(this).attr('placeholder') );
				});
				
			});
			
			/**
				Tap header menu
			**/
			$('.mobile #header-menu a.item').on('click', function() {
				var submenu = $(this).next('ul.sub-menu, .wproto-mega-menu-content');
				if( submenu.length ) {
					submenu.show();
					return false;
				}
			});
			
			/**
				Hexagon template filter
			**/
			$('.hexagon-filter-links li').click( function() {
				
				var tax_id = $(this).data('filter');
				var post_type = $(this).data('post-type');
				var taxonomy_name = $(this).data('tax-name');
				var responseContainer = $('#ajax-pagination-response-container');
				var paginationLink = $('#wproto-load-more-posts-link');
				var posts_per_page = paginationLink.data('posts_per_page');
				
				$('.hexagon-filter-links li').removeClass('current');
				$(this).addClass('current');
				
				$.ajax({
					url: wprotoEngineVars.ajaxurl,
					type: "POST",
					dataType : 'json',
					data: {
						'action' : 'wproto_ajax_filter_hexagon_posts',
						'term_id' : tax_id,
						'post_type' : post_type,
						'posts_per_page' : posts_per_page,
						'taxonomy_name' : taxonomy_name
					},
					beforeSend: function() {
						NProgress.start();
					},
					success: function( response ) {
						NProgress.done(true);
						
						if( response.html ) {
							responseContainer.html( response.html );
							paginationLink.data('display_type', 'category').data('max-pages', response.max_pages ).data('current-page', 1 ).data('next-page', 2 ).data('taxonomy-name', taxonomy_name ).data('taxonomy-term', tax_id );
							
							if( response.hide_link ) {
								paginationLink.hide();
							} else {
								paginationLink.show();
							}
							
							if( parseInt( tax_id ) == 0 ) {
								paginationLink.data('display_type', 'all').data('taxonomy-name', '' ).data('taxonomy-term', '' );
							}
							
						}
						
					},
					error: function() {
						NProgress.done(true);
						self.alertMessage( wprotoEngineVars.strServerResponseError );
					},
					ajaxError: function() {
						NProgress.done(true);
						self.alertMessage( wprotoEngineVars.strAJAXError );
					}
				});
				
				return false;
			});
			
			/**
				Homepage portfolio filter
			**/
			$('section.portfolio').each( function() {
				
				var responseContainer = $(this).find('.home-portfolio-items-container');
				
				$(this).find('.portfolio-categories a').click( function() {
					
					$(this).parents('.portfolio-categories').find('li').removeClass('current');
					jQuery(this).parent().addClass('current');
					
					var currentId = $(this).data('filter');
					
					jQuery.ajax({
						url: wprotoEngineVars.ajaxurl,
						type: "POST",
						dataType : 'json',
						data: {
							'action' : 'wproto_home_filter_portfolio_posts',
							'term_id' : currentId
						},
						beforeSend: function() {
							NProgress.start();
						},
						success: function( response ) {
							NProgress.done(true);
							
							if( response.html ) {
								responseContainer.html( response.html ).find('.portfolio-items').masonry({
									itemSelector: 'div.item',
									isAnimated: true,
									gutter: 6,
									columnWidth: 165
								});
								
								responseContainer.find('.portfolio-items').magnificPopup({
									type:'image',
									delegate: 'a.icon-zoom',
									removalDelay: 100,
									mainClass: 'mfp-fade',
									gallery: {
										enabled: true,
										navigateByImgClick: true
									}
								});
								
								responseContainer.waitForImages( {
									finished: function() {
										responseContainer.find('.portfolio-items').masonry({
											itemSelector: 'div.item',
											isAnimated: true,
											gutter: 6,
											columnWidth: 165
										});
									}
								});
							}
							
						},
						error: function() {
							NProgress.done(true);
							self.alertMessage( wprotoEngineVars.strServerResponseError );
						},
						ajaxError: function() {
							NProgress.done(true);
							self.alertMessage( wprotoEngineVars.strAJAXError );
						}
					});
					
					return false;
				});
				
			});
			
			/**
				Homepage portfolio load more posts button
			**/
			$( document ).on( 'click', '.section-portfolio-filter-load a.button', function() {
					
					var postsContainer = $(this).parents('.home-portfolio-items-container').find('.portfolio-items');
					var current_page = $(this).data('current-page');
					var max_pages = $(this).data('max-pages');
					var terms = $(this).data('taxonomy-term');
				
					var loader = jQuery(this).find('i');
					var link = jQuery(this);
					
					jQuery.ajax({
						url: wprotoEngineVars.ajaxurl,
						type: "POST",
						dataType : 'json',
						data: {
							'action' : 'wproto_home_load_portfolio_posts',
							'max_pages' : max_pages,
							'current_page' : current_page,
							'terms' : terms
						},
						beforeSend: function() {
							NProgress.start();
							loader.addClass('fa-spin');
						},
						success: function( response ) {
							
							loader.removeClass('fa-spin');
							NProgress.done(true);
										
							link.data( 'current-page', response.current_page );
					
							if( response.next_page > max_pages || response.hide_link == 'yes' ) {
								link.remove();
							}
							
							if( response.html ) {
								
								postsContainer.append( response.html ).masonry('reloadItems').masonry({
									itemSelector: 'div.item',
									isAnimated: true,
									gutter: 6,
									columnWidth: 165
								});
									
								postsContainer.waitForImages( {
									finished: function() {
										postsContainer.masonry({
											itemSelector: 'div.item',
											isAnimated: true,
											gutter: 6,
											columnWidth: 165
										});
									}
								});
								
							}
							
						},
						error: function() {
							loader.removeClass('fa-spin');
							NProgress.done(true);
							self.alertMessage( wprotoEngineVars.strServerResponseError );
						},
						ajaxError: function() {
							loader.removeClass('fa-spin');
							NProgress.done(true);
							self.alertMessage( wprotoEngineVars.strAJAXError );
						}
					});
					
					return false;
				
			});
			
			$('#sort-by').change( function() {
				$(this).parents('form').submit();
				return false;
			});
		
		},
	
		/**************************************************************************************************************************
			Class methods
		**************************************************************************************************************************/
		/**
			Google map
		**/
		setupGoogleMap: function() {
	
			var geocoder = new google.maps.Geocoder();
		
			var latlong;	
			
			var mapDiv = $('#google-map-contact');
			var settingsZoom = mapDiv.data('zoom');
			var settingsMapDraggable = mapDiv.data('draggable') == 'yes';
			var settingsMapZoomControls = mapDiv.data('zoom-controls') == 'yes';
			
			geocoder.geocode( { 'address': wprotoEngineVars.contact_address }, function(results, status) {
 				if (status == google.maps.GeocoderStatus.OK) {
 					latlong = results[0].geometry.location;

					var googleMapOptions = {
						zoom: settingsZoom,
						center: latlong,
						mapTypeId: google.maps.MapTypeId.ROADMAP,
						panControl: false,
						zoomControl: settingsMapZoomControls,
						scrollwheel: false,
						disableDoubleClickZoom: true,
						disableDefaultUI: true,
						draggable: settingsMapDraggable,
						scaleControl: false
					};

					var map = new google.maps.Map( document.getElementById('google-map-contact'), googleMapOptions );
		
					var image = new google.maps.MarkerImage(
		  			wprotoEngineVars.contact_map_pointer,
						new google.maps.Size(22,29),
						new google.maps.Point(0,0),
						new google.maps.Point(0,35)
					);

					var marker = new google.maps.Marker({
						draggable: false,
						raiseOnDrag: false,
						icon: image,
						map: map,
						position: latlong
					});
		
					var myInfoWindowOptions = {
						content: '<div class="info-window-content"><img width="130" src="' + wprotoEngineVars.contact_map_logo + '" alt="" /></div>',
						maxWidth: 150
					};

					var infoWindow = new google.maps.InfoWindow(myInfoWindowOptions);
		
					google.maps.event.addListener(marker, 'click', function() {
						infoWindow.open(map,marker);
					});
		
					google.maps.event.addListener(marker, 'click', function() {
						infoWindow.open(map,marker);
					});

					google.maps.event.addListener(marker, 'dragstart', function(){
						infoWindow.close();
					});

					infoWindow.open(map,marker);

				}
			});	
					
		},
		/**
			Contact form
		**/
		bindContactForm: function() {
			
			var self = this;
			
			$('.wproto-contact-form').each( function() {
				
				$(this).submit( function() {
				
					var form = $(this);
			
					var formId = $( this ).find( 'input[name=wproto_form_id]' );
					var fromWidget = $( this ).find( 'input[name=from_widget]' );
					var to = $( this ).find( 'input[name=to]' );
					var name = $( this ).find( 'input[name=name]' );
					var email = $( this ).find( 'input[name=email]' );
					var subject = $( this ).find( 'input[name=subject]' );
					var text = $( this ).find( 'textarea[name=message]' );
					var captcha = $( this ).find('input.wproto-captcha-input');
					var captcha_id = $( this ).find('input.wproto-captcha-input-id');
				
					if( ! captcha.next('.error').length && formId.val() == 'primary-contact-form' ) {
						form.find( '.unit-contacts' ).append( '<div class="error">' + wprotoEngineVars.strTypeCaptchaAnswer + '</div>' );
					}
				
					form.find('.error').hide();
				
					if( $.trim( name.val() ) == '' ) {
						name.focus();
						name.next('.error').show();
						return false;
					}
				
					if( jQuery.trim(email.val() ) == '' || !self.isValidEmailAddress( email.val() ) ) {
						email.focus();
						email.next('.error').show();
						return false;	
					}
				
					if( jQuery.trim( text.val() ) == '' ) {
						text.focus();
						text.next('.error').show();
						return false;
					}
				
					if( captcha.length && jQuery.trim( captcha.val() ) == '' ) {
						captcha.focus();
						captcha.next('.error').show();
					
						return false;	
					} else {
		
						jQuery.ajax({
							url: wprotoEngineVars.ajaxurl,
							type: "POST",
							dataType: "json",
							data: {
								'action' : 'wproto_send_contact_form',
								'to' : to.length ? to.val() : '',
								'from_widget' : fromWidget.length ? fromWidget.val() : '', 
								'post_id' : wprotoEngineVars.post_id,
								'form_id' : formId.length ? formId.val() : '',
								'name' : name.length ? name.val() : '',
								'email' : email.length ? email.val() : '',
								'subject' : subject.length ? subject.val() : '',
								'text' : text.length ? text.val() : '',
								'captcha_id' : captcha_id.length ? captcha_id.val() : '',
								'captcha_value' : captcha.length ? captcha.val() : ''
							},
							beforeSend: function() {
								NProgress.start();
							},
							success: function( result ) {
								NProgress.done(true);
						
								if( result.status == 'ok' ) {
									
									form.html( '<h2 class="message-send">' + wprotoEngineVars.messageWasSent + '</h2>' );
									
								} else {
								
									self.alertMessage( result.error_text );

								}
								
							},
							error: function() {
								NProgress.done(true);
								
								self.alertMessage( wprotoEngineVars.strServerResponseError );
								
							},
							ajaxError: function() {
								NProgress.done(true);
								
								self.alertMessage( wprotoEngineVars.strAJAXError );
								
							}
						});
			
					}
		
					return false;
				
				});
				
			});

		},
		/**
			Validate comments form
		**/
		validateCommentsForm: function() {
			
			var self = this;
			
			if( $('#commentform').length ) {
		
				$('#commentform').submit( function() {
					var author = $('#author');
					var comment = $('#comment');
					var email = $('#email');
					var captcha = $( this ).find('input.wproto-captcha-input');
			
					var errorCount = 0;
			
					var form = $(this);
			
					if( author.length && $.trim( author.val() ) == '' ) {
						author.focus();	
						errorCount++;		
						return false;	
					}

					if( email.length ) {
				
						var emailVal = email.val();
				
						if( $.trim(emailVal ) == '' || !self.isValidEmailAddress( email.val() ) ) {
					
							email.focus();
							errorCount++;
							return false;	
						}
					}
			
					if( $.trim( comment.val() ) == '' ) {
						comment.focus();
						errorCount++;
						return false;	
					}
			
					if( captcha.length && $.trim( captcha.val() ) == '' ) {
						captcha.focus();
						errorCount++;
						return false;	
					} else {

						if( captcha.length ) {
					
							var captcha_id = form.find('input.wproto-captcha-input-id');
							var answ = captcha.val();
					
							$.ajax({
								url: wprotoEngineVars.ajaxurl,
								type: "POST",
								data: {
									'action' : 'wproto_check_captcha_answer',
									'answer' : answ,
									'wproto_captcha_id' : captcha_id.val()
								},
								beforeSend: function() {
									NProgress.start();
								},
								success: function( result ) {
									if( result == 'ok' ) {
										$('#commentform').unbind( 'submit' );
										$('#commentform #submit').trigger('click');
									} else {
										NProgress.done(true);
										captcha.val('').focus();
									}
								},
								error: function() {
									NProgress.done(true);
									self.alertMessage( wprotoEngineVars.strServerResponseError );
								},
								ajaxError: function() {
									NProgress.done(true);
									self.alertMessage( wprotoEngineVars.strAJAXError );
								}
							});
				
							return false;
						} 
				
					}

				});
		
			}
			
		},
		/**
			Likes 
		**/
		bindLikes: function() {
			
			$('.wproto-like').click( function() {
		
				var postId = $(this).attr('data-id');
				var type = $(this).attr('data-type');
				var link = $(this);
				var params = {
					'action' : 'wproto_ajax_like',
					'post_id' : postId,
					'nonce' : wprotoEngineVars.ajaxNonce
				};
		
				if( type == 'comment' ) {
					params.comment_like = true;
					params.comment_id = postId;
				}
		
				if( type == 'post' ) {
					params.post_like = true;
					params.post_id = postId;
				}
		
				$.ajax({
					url: wprotoEngineVars.ajaxurl,
					type: "POST",
					data: params,
					beforeSend: function() {
						NProgress.start();
					},
					success: function( result ) {
						NProgress.done(true);
						var n = parseInt( result );
						if( n > 0 ) {
							link.find('span.views').text( n ).show();
							link.find('span.title').text( '' );
							link.find('span').unwrap();
							$('.tipsy:last').remove();
						}
					},
					error: function() {
						NProgress.done(true);
						self.alertMessage( wprotoEngineVars.strServerResponseError );
					},
					ajaxError: function() {
						NProgress.done(true);
						self.alertMessage( wprotoEngineVars.strAJAXError );
					}
				});
				return false;
			});
			
		},
		/**
			Setup menu angles
		**/
		setupMenuAngles: function() {
			
			if( $('#header-menu-ul').length ) {
				// first level
				$('#header-menu-ul > li').each( function() {
					
					var submenu = $(this).find('ul, .wproto-mega-menu-content');
					
					if( submenu.length ) {
						$(this).find('span.menu-text:first').append(' <i class="arrow-drop"></i>');
					}
					
				});
				// submenus
				$('#header-menu-ul > li > ul > li').each( function() {
					var submenu = $(this).find('ul');
					
					if( submenu.length ) {
						$(this).find('span.menu-text:first').append(' <i class="menu-angle"></i>');
					}
				});
			}
			
		},
		/**
			Custom page inputs
		**/
		setupCustomInputs: function() {
		
			// pretty checkboxes
			$('input[type=radio], input[type=checkbox]').each( function() {
				$(this).on('ifChecked', function(event){
					
					$(this).attr('checked', 'checked').change();
					
				}).on('ifUnchecked', function() {
					
					var name = $(this).attr('name');
					
					$(this).removeAttr('checked').change();
					
				}).iCheck({
  				labelHover: false,
  				cursor: true
				});
			});
			
		
			/**
				Select
			**/
			//$('select').fancySelect();
			
			var selects = $('select');
			if( selects.length ) {
				
				selects.each( function() {
					
					var id = $(this).attr('id');
					
					if( id != 'switcher-primary-font-selector' && id != 'switcher-secondary-font-selector' ) {
						/*
						$(this).selecter({
							customClass: "theme-select-input",
							cover: true //,
							//defaultLabel: "Select an item..."
						});
						*/
					}
					
				});
				
			}
		
		},
	
		/**
			Setup page sliders
		**/
		setupTabs: function() {
		
			/**
				Content slider
			**/
			$('.content-slider').liquidSlider({
				slideEaseFunction:'animate.css',
				animateIn:"fadeIn",
				animateOut:"fadeOut",
				dynamicArrows: false,
				autoHeight: true,
				slideEaseDuration:500,
				heightEaseDuration:500,
				includeTitle: false,
				autoSlide: false,
				panelTitleSelector: 'h2.title',
				callback: function() {
					var self = this;
			
					$(self).find('.panel').each(function() {
      			$(this).removeClass( 'animated ' + self.options.animateIn );
    			});
			
				}
			});
	
			$('.buy-together-slider').liquidSlider({
				slideEaseFunction:'animate.css',
				animateIn:"fadeIn",
				animateOut:"fadeOut",
				hideSideArrows: false,
				hideSideArrowsDuration: 0,
				slideEaseDuration:500,
				heightEaseDuration:500,
				dynamicTabs: false,
				dynamicArrows: true,
				autoSlide: false,
				callback: function() {
					var self = this;
			
					$(self).find('.panel').each(function() {
      			$(this).removeClass( 'animated ' + self.options.animateIn );
    			});
			
				}
			});
		},
		setupSliders: function() {
		
			// post gallery carousel
			$(".images-carousel, .post-slider-carousel").each( function() {
		
				$(this).bxSlider({
					controls: true,
					autoStart: false,
					minSlides: 2,
					nextSelector: $(this).parent().find(".post-slider-next"),
					prevSelector: $(this).parent().find(".post-slider-prev"),
					pagerSelector: $(this).parent().find(".post-slider-pagination"),
					touchEnabled: true,
					mode: 'fade'
				});
			
			});
	
			$('.widget-slider > .slides, .wproto-photoalbums-widget .slides').each( function() {
				$(this).bxSlider({
					controls: true,
					autoStart: false,
					minSlides: 2,
					pagerSelector: $(this).parent().find(".slider-pagination"),
					touchEnabled: true,
					mode: 'fade'
				});
			});
		
			// full screen portfolio
			if( $('.full-portfolio-slider').length ) {
				
				// load first slide
				$('.full-portfolio-slider img.lazy:first').each( function() {
					$(this).attr('src', $(this).data('src') );
					$('.full-portfolio-slider').removeClass('preload');
				});
				
				var pSlider = $('.full-portfolio-slider').bxSlider({
					mode: 'fade',
					onSlideBefore: function( slideElement, oldIndex, newIndex ){
						
						var lazy = slideElement.find("img.lazy")
						var load = lazy.attr("data-src");

						lazy.attr("src", load );
						
						/**
    				lazy.attr("src", load ).load(function(){
    					$('.bx-wrapper, .bx-viewport').height( lazy.height() );
    					//$('.portfolio-thumbnails').css('bottom', '0px');
    					//window.scrollTo(0, 0);
						});**/
 						
        	},
					controls: false,
					autoStart: false,
					minSlides: 1,
					adaptiveHeight: true,
					pagerCustom: $("#portfolio-pager .jTscroller"),
					touchEnabled: true
				});
			}
		
			//portfolio thumbnail scroller
			if( $("#portfolio-pager").length ) {
				
				var touchSlider = $("#portfolio-pager").find('.swiper-container').swiper({
					mode:'horizontal',
 					slidesPerView: 'auto',
  				calculateHeight: true,
  				autoResize: false
 				});
  				
				$("#portfolio-pager").find('.jTscrollerPrevButton').click( function() {
					touchSlider.swipePrev();
				});
				
				$("#portfolio-pager").find('.jTscrollerNextButton').click( function() {
					touchSlider.swipeNext();
				});
				
			}

		
		},
	
		/**
			Setup carousels
		**/
		setupCarousels: function() {
			
			var self = this;
		
			// related products and related posts carousel
			$('.related-posts > .items, .related-products > .items, .new-arrivals > .items, .best-sellers > .items').each( function() {
		
				var items = 4;
		
				if( $('body').hasClass('single-product') ) {
					items = $('.wproto-page-sidebar').length ? 4 : 5;
				}
				
		
				$(this).owlCarousel({
					items: items,
					autoPlay: false,
					navigation: false,
					pagination: true,
					responsive: true,
					itemsDesktopSmall: [1199,3],
					itemsTablet: [959,3],
					itemsTabletSmall: [767,3],
					itemsMobile: [480,1]
				});	
		
			});
			
			$('.hex-portfolio .items').each( function() {
		
				$(this).owlCarousel({
					items: 4,
					autoPlay: false,
					navigation: false,
					pagination: true,
					responsive: true,
					itemsDesktopSmall: [1199,3],
					itemsTablet: [959,2],
					itemsTabletSmall: [767,2],
					itemsMobile: [480,1]
				});	
		
			});
			
			// single shop products carousel
			$('.product-scroller .scroller').each( function() {
				$(this).bxSlider({
					controls: true,
					autoStart: false,
					slideWidth: 95,
					minSlides: 3,
					maxSlides: 3,
					adaptiveHeight: true,
					touchEnabled: true
				});
			});
		
			// page banners
			$('.page-banners-carousel > .items').each( function() {
		
				$(this).owlCarousel({
					items: 1,
					navigation: false,
					pagination: true,
					responsive: true,
					transitionStyle : "backSlide",
					itemsDesktopSmall: [1199,1],
					itemsTablet: [959,1],
					itemsTabletSmall: [767,1],
					itemsMobile: [480,1],
					afterInit: function( slider ) {
						self.runBannerAnimation( slider, 'show' );
					},
					afterMove: function( slider ) {
						self.runBannerAnimation( slider, 'show' );
					},
					beforeMove: function( slider ) {
						self.runBannerAnimation( slider, 'hide' );
					}
				});
		
			});
			
			// home slider
			$('.slider-carousel > .items').each( function() {
		
				$(this).owlCarousel({
					navigation: true,
					pagination: false,
					responsive: true,
					lazyLoad : true,
					lazyFollow : true,
					transitionStyle : "fade",
					singleItem: true,
					autoPlay: true,
					stopOnHover: true,
					afterInit: function( slider ) {
						self.runBannerAnimation( slider, 'show' );
					},
					afterMove: function( slider ) {
						self.runBannerAnimation( slider, 'show' );
					},
					beforeMove: function( slider ) {
						self.runBannerAnimation( slider, 'hide' );
					}
				});
		
			});
		
			// widget post carousel

			$('.widget.wproto-blog-posts-widget .items, .wproto-catalog-widget .items, .testimonials-holder .items, .wproto-testimonials-widget .items, .wproto-portfolio-widget .items, .wproto-logos-carousel-widget .items, .wproto-team-widget .items').each( function() {
		
				var self = $(this);
		
				$(this).owlCarousel({
					items: 1,
					navigation: true,
					pagination: false,
					responsive: true,
					transitionStyle : "fade",
					itemsDesktopSmall: [1199,1],
					itemsTablet: [959,1],
					itemsTabletSmall: [767,1],
					itemsMobile: [480,1],
					afterInit: function( slider ) {
				
						$(slider).find('.owl-external .prev').click( function() {
							self.trigger('owl.prev');
						});
						$(slider).find('.owl-external .next').click( function() {
							self.trigger('owl.next');
						});
					}
				});
		
			});
		
		},
	
		/**
			Setup required plugins
		**/
		setupPlugins: function() {
		
			/**
				Tipsy
			**/
			$('.show-tooltip, .wproto_tooltip').each( function() {
				var g = $(this).attr('data-tip-gravity');
				g = g == undefined ? 'n' : g;
				$(this).tipsy( { fade: true, gravity: g } );
			});
	
			// GoTop script
			if( $().UItoTop ) {
				$().UItoTop();
			}
		
			/**
				Lightbox
			**/
			$('.single-product .image-link, a.popup').each( function() {
				$(this).magnificPopup({
					type:'image',
					removalDelay: 100,
					mainClass: 'mfp-fade',
					zoom: {
						enabled: true,
						duration: 300,
						opener: function(element) {
							return element.find('img');
						}
					},
					gallery: {
						enabled: true,
						navigateByImgClick: true
					}
				});
			});
			$('.home-portfolio').each( function() {
				$(this).magnificPopup({
					type:'image',
					delegate: 'a.icon-zoom',
					removalDelay: 100,
					mainClass: 'mfp-fade',
					gallery: {
						enabled: true,
						navigateByImgClick: true
					}
				});
			});
			
			$('.wproto-photoalbums-widget, .widget-slider, .wproto-photos-widget').each( function() {
				$(this).magnificPopup({
					type:'image',
					delegate: 'a.lightbox',
					removalDelay: 100,
					mainClass: 'mfp-fade',
					zoom: {
						enabled: true,
						duration: 300,
						opener: function(element) {
							return element.find('img');
						}
					},
					gallery: {
						enabled: true,
						navigateByImgClick: true
					}
				});
			});
		
			// ui slider
			$('.slider-range').each( function() {
		
				var self = $(this);
		
				self.slider({
					range: true,
					min: 0,
					max: 3000,
					values: [ 500, 1200 ],
					slide: function( event, ui ) {
						self.parent().find('p.range span > span').html( "<strong>$" + ui.values[ 0 ] + "</strong> - <strong>$" + ui.values[ 1 ] + '</strong>' );
					}
				});
		
			});
		
			// masonry blog layout
			if( $('.template-masonry .posts').length ) {
		
				$('.template-masonry .posts').masonry({
					itemSelector: 'article.post',
					isAnimated: true,
					columnWidth: '.masonry-grid-sizer'
				});
				
				$( '.template-masonry .posts' ).waitForImages( {
					finished: function() {
						
						$('.template-masonry .posts').masonry({
							itemSelector: 'article.post',
							isAnimated: true,
							columnWidth: '.masonry-grid-sizer'
						});
    			}
   			} );
		
			}
		
		},
	
		/**
			Homepages init
		**/
		setupHomepages: function() {
			
			/**
				Home portfolio
			**/
			if( $('.home-portfolio').length ) {
				$('.home-portfolio').each( function() {
					
					$( this ).masonry({
						itemSelector: 'div.item',
						isAnimated: true,
						gutter: 6,
						columnWidth: 165
					});
					
				});
				
				$('.home-portfolio').waitForImages( {
					finished: function() {
						$('.home-portfolio').each( function() {
					
							$( this ).masonry({
								itemSelector: 'div.item',
								isAnimated: true,
								gutter: 6,
								columnWidth: 165
							});
					
						});
    			}
   			} );
				
			}
			
			/**
				Home testimonials
			**/
			var tCarousel = $('#testimonials-carousel');
			if( tCarousel.length ) {
				tCarousel.owlCarousel({
					items: 1,
					navigation: true,
					pagination: false,
					responsive: true,
					transitionStyle : "fade",
					itemsDesktopSmall: [1199,1],
					itemsTablet: [959,1],
					itemsTabletSmall: [767,1],
					itemsMobile: [480,1]
				});
			}
			
			/**
				Home products sub-carousel
			**/
			
			$('.additional-info .scroller').each( function() {
				$(this).bxSlider({
					controls: true,
					autoStart: false,
					slideWidth: 75,
					minSlides: 3,
					maxSlides: 3,
					adaptiveHeight: true,
					touchEnabled: true
				});
			});
			
			/**
				Home carousels
			**/
			// related products and related posts carousel
			if( $('.page-template-page-tpl-home-custom-php').length ) {
			
				$('.best-ratings > .items, .reviews > .items, .home-best-sellers > .items').each( function() {
		
					$(this).owlCarousel({
						items: 1,
						autoPlay: false,
						navigation: false,
						pagination: true,
						responsive: true,
						transitionStyle : "fade",
						itemsDesktopSmall: [1199,1],
						itemsTablet: [959,1],
						itemsTabletSmall: [767,1],
						itemsMobile: [480,1]
					});	
		
				});
				
			}
			
			/**
				Home blog posts scroller
			**/
			if( $('.blog-posts-home').length ) {
				
				var touchSliders = [];
				
				$('.blog-posts-home').each( function( i ) {
					
					touchSliders[i] = $( this ).find('.swiper-container').swiper({
    				mode:'horizontal',
    				slidesPerView: 'auto',
    				calculateHeight: true,
    				autoResize: false
  				});
  				
					$(this).find('.jTscrollerPrevButton').click( function() {
    				touchSliders[i].swipePrev();
					});
				
					$(this).find('.jTscrollerNextButton').click( function() {
    				touchSliders[i].swipeNext();
					});
					
				});
				
			}
			
		},
	
		/**
			Header menu scroll
		**/
		navMenu: function() {
			
			if( $('body').hasClass('no-scrolling-menu') ) {
				return false;
			}
			
			if( $('.big-header-wrapper').length && $('html').hasClass('mobile') == false && $('body').hasClass('page-template-page-tpl-one-page-php') == false ) {
				
				var menuTop = $('header.small');
				var el = $('.big-header-wrapper');
				var elpos_original = el.offset().top;
		
				$(window).scroll(function(){
					var elpos = el.offset().top;
 					var windowpos = $(window).scrollTop();
  				var finaldestination = windowpos;
  				var body = $('body');
  	
  				if( $(window).width() > 767 ) {
  					
  					if(windowpos<=elpos_original) {
   						finaldestination = elpos_original;
   						
     					el.removeClass('scrolled');
      				menuTop.removeClass('menu-scrolled');
      				body.removeClass('scrolling')
      				
  					} else {
  						
  						if( body.hasClass('scrolling') == false ) {
  							body.addClass('scrolling');
  						}
  						
  						if( el.hasClass('scrolled') == false ) {
  							el.addClass('scrolled');
  						}
  						
  						if( menuTop.hasClass('menu-scrolled') == false ) {
  							menuTop.addClass('menu-scrolled');
 							}
	   					
     					
 						}
  				} else {
 						el.removeClass('scrolled');
   					menuTop.removeClass('menu-scrolled');
  				}
				});
		
				$( window ).resize(function() {
					if( $(window).width() < 767 ) {
						$('header.small, .big-header-wrapper').removeClass('menu-scrolled scrolled');
					}
				});
				
			}

		},
	
		/**
			Custom slider events
		**/
		sliderEvents: function() {
		
			//portfolio thumbnail scroller
			$('.portfolio-full-slider .toggle-panel').click( function() {
				$(this).toggleClass('closed');
				$('.portfolio-thumbnails').toggleClass('closed');
				$('#portfolio-pager').fadeToggle();
				return false;
			});
		
		},
	
		/**
			Page toggles events
		**/
		setupToggles: function() {
			
			// Toggles		
			$('.toggle h4').click( function() {
		
				var top = $(this).parent().parent();
				var content = $(this).parent().find('.toggle-content');
				var icon = $(this).parent().find('i');
				var h = $(this);
		
				top.find('h4').removeClass('opened');

				if( content.is(':hidden') ) {
					top.find('.toggle-content').slideUp();
					top.find('i').removeClass('minus').addClass('plus');
					icon.removeClass('plus').addClass('minus');
					h.addClass('opened');
					content.slideDown();

				} else {
					icon.removeClass('minus').addClass('plus');
					content.slideUp();
				}
		
				return false;
			});
		},
	
		/**************************************************************************************************************************
			Utils
		**************************************************************************************************************************/
		/**
			Make alert
		**/
		alertMessage: function( text ) {
			
			vex.dialog.alert({
				message: text,
				className: 'vex-theme-default'
			});
		},
		/**
			Check email address
		**/
		isValidEmailAddress: function( emailAddress ) {
			var pattern = new RegExp(/^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i);
 			return pattern.test( emailAddress );
		},
		
		/**
			Show animations for elements
		**/
		initAnimations: function() {
	
			if( $("html").hasClass("mobile") ) {
				$('.progress-value .value').each( function() {
					$(this).css('width', $(this).data('width'));
				});
			}
	
			if( $("html").hasClass("oldie") || $("html").hasClass("mobile") ) {
				return false;
			}
	
			$("[data-appear-animation]").each(function() {

				var self = $(this);
		
				self.addClass("appear-animation");
		
					if( $(window).width() > 959 ) {
				
						self.appear(function() {
					
							var delay = (self.attr("data-appear-animation-delay") ? self.attr("data-appear-animation-delay") : 0);
					
							self.css("animation-delay", delay + "s");
					
							var animation = self.attr("data-appear-animation");
					
							self.addClass( animation );
					
							setTimeout(function() {
							
								if( animation == 'animateWidth' ) {
									self.css('width', self.attr("data-width"));
								}
						
								self.addClass("animated").addClass("animation-finished");
						
							}, delay);
					
						}, {accX: 0, accY: -50});
				
					} else {
				
						self.addClass("animated").addClass("animation-finished");
					
						self.css('width', self.attr("data-width"));
				
					}
			});
	
		},
	
		/**
			Run banner animation
		**/
		runBannerAnimation: function( slider, type ) {
		
			var elements = $( slider ).find('div.text:visible, div.second-text:visible, div.link:visible, .layer');
		
			elements.each( function() {
				$(this).addClass( $(this).data('animation-effect') ).css("animation-delay", $(this).data('animation-delay'));
			});
		
			if( type == 'show' ) {
				elements.css('opacity', 1).addClass('animated');
			}
		
			if( type == 'hide' ) {
				elements.css('opacity', 0).removeClass('animated');
			}
		
		}
	}

	Core.initialize();

});