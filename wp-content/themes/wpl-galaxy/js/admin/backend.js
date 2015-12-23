jQuery.noConflict()( function($){
	"use strict";

	var wprotoMedia;

	var wprotoBackend = {
	
		/**
			Constructor
		**/
		initialize: function() {

			this.build();
			this.events();

		},
		/**
			Build page elements
		**/
		build: function() {

			var self = this;
			
			/**
				Check for retina displays
			**/
			if( document.cookie.indexOf('device_pixel_ratio') == -1 && 'devicePixelRatio' in window && window.devicePixelRatio == 2 ){

				var date = new Date();
				date.setTime( date.getTime() + 3600000 );

				document.cookie = 'device_pixel_ratio=' + window.devicePixelRatio + ';' +  ' expires=' + date.toUTCString() +'; path=/';
				//if cookies are not blocked, reload the page
				if(document.cookie.indexOf('device_pixel_ratio') != -1) {
					window.location.reload();
				}
 			}
 			
			/**
				Datepicker
			**/
			$('#wproto-opening-date-picker').datepicker( { dateFormat: $('#wproto-opening-date-picker').data('date-format') } );
 			
			/**
				Set ajax loader after "filter" button
			**/
			$('#wproto-list-posts-loader').insertAfter('#post-query-submit');
			
			/**
				Set up sortables
			**/
			$( "#wproto-metabox-content" ).sortable({
				placeholder: "ui-state-highlight"
			});
			
			// Fades
			$( '.fade' ).fadeOut( 1500 );
			
			/**
				Color picker
			**/
			$('.wp-color-picker-field').wpColorPicker();
			
			/**
				Select to image picker
			**/
			if( $('.wproto-select-to-picker').length ) {
				$('.wproto-select-to-picker').imagepicker();
			}	
			
			wprotoSetupTooltips();			
			
		},
		/**
			Set page events
		**/
		events: function() {
			
			var self = this;
			
			/*/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
			One Image Picker
			/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////*/
	
			$( document ).on( 'click', '.wproto-image-selector', function() {
		
				var targetImage = $(this).attr('data-src-target');
				var targetInput = $(this).attr('data-url-target');
				var targetInputURL = $(this).attr('data-url-input');
		
				wprotoMedia = wp.media.frames.wprotoMedia = wp.media({
					className: 'media-frame wproto-media-frame',
					frame: 'select',
					multiple: false,
					title: wprotoVars.strSelectImage,
					library: {
						type: 'image'
					},
					button: {
						text: wprotoVars.strSelect
					}
				});
		
				wprotoMedia.on('select', function(){
					var media_attachment = wprotoMedia.state().get('selection').first().toJSON();
			
					if( targetImage != '' ) {
						$( targetImage ).attr( 'src', media_attachment.url );
					}
					if( targetInput != '' ) {
						$( targetInput ).val( media_attachment.id );
					}
					if( targetInputURL ) {
						
						$( targetInputURL ).val( media_attachment.url );
					}

				});
		
				wprotoMedia.open();
		
				return false;
			});
	
			$( document ).on( 'click', '.wproto-image-remover', function(){
		
				var targetImage = $(this).attr('data-src-target');
				var targetInput = $(this).attr('data-url-target');
				var defaultImage = $(this).attr('data-default-img');
				var targetInputURL = $(this).attr('data-url-input');
		
				$( targetImage ).attr( 'src', defaultImage );
				$( targetInput ).val( '0' );
				$( targetInputURL ).val('');
		
				return false;
			});
	
			/*/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
				Video Grabber
			/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////*/
	
			$('#wproto-example-video-link').click( function() {
				$('#wproto-video-link-input').val( $( this).text());
				return false;
			});
	
			$( '#wproto-grab-video').bind('click', function() {
        
				var link = $('#wproto-video-link-input');
				var result_div = $('#wproto-video-table');
        
				result_div.html('').hide();
        
				if( $.trim( link.val()) == '') {
					link.focus();
					return false;
				}
        
				result_div.html( wprotoVars.adminBigLoaderImageTransp ).show();
        
				$.post( ajaxurl, { 'action' : 'wproto_ajax_grab_video', 'link' : link.val() },
					function( response){
						result_div.html( response);
						wprotoSetTooltips( $('a#wproto-use-video-title'), 'left left', 'right right', 'left', '10px 0' );
					}
				);
		
				return false;

			});
	
			$( document ).on( 'click', '#wproto-use-video-title', function() {
				var title = $(this).text();
				$('input#title').val( title ).focus();
				return false;
			});
	
			$( document ).on( 'click', '.wproto-container-size-links a', function() {
        
				var size = $( this).text();
				var size_array = size.split('x'); 
        
				$( '#wproto-video-container-width').val( size_array[0]);
				$( '#wproto-video-container-height').val( size_array[1]);
        
				return false;
			});
		
			/*/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
				Image chooser
			/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////*/
	
			$('#wproto-img-picker-add-images').click( function() {
		
				if ( wprotoMedia ) {
					wprotoMedia.open();
					return;
				}
		
				wprotoMedia = wp.media.frames.wprotoMedia = wp.media({
					className: 'media-frame wproto-media-frame',
					frame: 'select',
					multiple: true,
					title: wprotoVars.strAttachImages,
					library: {
						type: 'image'
					},
					button: {
						text: wprotoVars.strInsertAttachedImages
					}
				});
		
				wprotoMedia.on('select', function(){
					//var media_attachment = wprotoMedia.state().get('selection').first().toJSON();
					var media_attachments = wprotoMedia.state().get('selection').toJSON();
					var already_attached = [];
			
					$('input.wproto-attached-image-item-id').each( function() {
						already_attached.push( $(this).val() );
					});
			
					var loader = $('#wproto-list-attached-images-loader');
			
					if( media_attachments.length > 0 ) {
			
						$.ajax({
							url: ajaxurl,
							type: "post",
							dataType: "json",
							data: {
								'action' : 'wproto_ajax_get_html_for_attached_images',
								'images' : media_attachments,
								'already_attached' : already_attached
							},
							beforeSend: function() {
								loader.show();
							},
							success: function( response ) {
								loader.hide();
								$('#wproto_meta_attached_images #wproto-metabox-content').append( response.html );
						
								self.countAttachedImages();
						
							},
							error: function() {
								loader.hide();		
								wprotoAlertServerResponseError();
							},
							ajaxError: function() {
								loader.hide();			
								wprotoAlertAjaxError();
							}
						});
				
					}

				});
		
				wprotoMedia.open();
		
				return false;
			});
	
			$('#wproto-attached-images a.view-button').click( function() {
		
				var view = $(this).hasClass('view-table') ? 'display-table' : 'display-thumbs';
		
				$('#wproto-metabox-footer li').removeClass('current');
				$(this).parent().addClass('current');
		
				$('#wproto_meta_attached_images').removeClass('display-table display-thumbs').addClass( view );
		
				return false;
			});
		
			$( document ).on( 'click', 'a.wproto-attached-image-delete', function() {
		
				$(this).parent().fadeOut(500, function() {
					$(this).remove();
					self.countAttachedImages();
				});
		
				return false;
			});
	
			$( document ).on( 'click', 'a.wproto-attached-image-edit', function() {
		
				var id = $(this).attr('data-id');
				tb_show( '', wprotoVars.adminURL + 'media.php?attachment_id=' + id + '&action=edit&wproto_admin_noheader&TB_iframe=1');
		
				return false;
			});
	
			/*/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
				Change post status ('Sticky' / 'Featured') by click
			/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////*/
	
			$('a.wproto_change_post_status').click( function() {
		
				var loader = $('#wproto-list-posts-loader');
				var prevValue = $(this).attr('data-value');
				var postStatus = $(this).hasClass('wproto_change_sticky') ? 'sticky' : 'featured';
				var statusImage = $(this).find('img');
				var postId = $(this).attr('data-post-id');
				var link = $(this);
			
				$.ajax({
					url: ajaxurl,
					type: "post",
					dataType: "json",
					data: {
						'action' : 'wproto_ajax_change_post_status',
						'post_status' : postStatus,
						'post_id' : postId
					},
					beforeSend: function() {
						loader.show();
					},
					success: function( response ) {
						loader.hide();
				
						if( prevValue == 'true' ) {
							statusImage.attr( 'src', wprotoVars.adminIconFalse );
					
							if( postStatus == 'sticky' ) {
								$('tr#post-' + postId).find('.post-state').hide();
							}
					
							link.attr('data-value', 'false');
						} else {
							statusImage.attr( 'src', wprotoVars.adminIconTrue );
							link.attr('data-value', 'true');
					
							if( postStatus == 'sticky' ) {
						
								if( $('tr#post-' + postId + ' span.post-state').length ) {
									$('tr#post-' + postId).find('.post-state').show();
								} else {
									$('<span class="post-state"> - ' + wprotoVars.strSticky + '</span>').insertAfter( 'tr#post-' + postId + ' a.row-title' );
								}
						
							}
	
						}
				
					},
					error: function() {
						loader.hide();		
						wprotoAlertServerResponseError();
					},
					ajaxError: function() {
						loader.hide();			
						wprotoAlertAjaxError();
					}
				});
		
				return false;
			});
	
			/*/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
				Icon picker
			/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////*/
		
			/**
				Icon picker filters
			**/
			$( document ).on('change', '#icon-picker-filter', function() {
							
				var val = $(this).val();
				
				switch( val ) {
					default:
					case('all'):
						$('.font-awesome-icon-list, .icomoon-icon-list').show();
					break;
					case('font-awesome'):
						$('.font-awesome-icon-list').show();
						$('.icomoon-icon-list').hide();
					break;
					case('icomoon'):
						$('.font-awesome-icon-list').hide();
						$('.icomoon-icon-list').show();
					break;
				}
							
				return false;
			});
			
			$( document ).on('keyup', '#icon-picker-text-filter', function() {
				var val = $(this).val();
				
				$("#icon-picker-icons i").hide();
				
				$("#icon-picker-icons i:regex(class, .*" + val + ".*)").show();
				return false;
			});
		
			/**
				Choose an icon clicked
			**/
			$( document ).on('click', 'a.wproto-icon-chooser', function() {
				var iconHolder = $(this).parent().find('i.wproto-icon-holder');
				var iconInput = $(this).parent().find('input.wproto-icon-holder-input');
				var linkChooser = $(this);
				var selectedIcon = '';
				var library = 'font-awesome';
		
				$('<div id="wproto-icon-picker-dialog" title="' + wprotoVars.strIconPicker + '"></div>').appendTo('body').hide();
				var dialog = $('#wproto-icon-picker-dialog');
		
				$.ajax({
					url: ajaxurl,
					type: "post",
					dataType: "json",
					data: {
						'action' : 'wproto_ajax_show_icon_picker_form'
					},
					beforeSend: function() {
						dialog.html( wprotoVars.adminBigLoaderImage );
				
						dialog.dialog({
							modal: true,
      				height: 450,
      				width: 700,
							buttons: {
								Ok: function() {

									selectedIcon = $('#icon-picker-icons i.selected' );
									library = selectedIcon.data('library');
									var selectedIconName = selectedIcon.attr('data-name');
									iconHolder.attr( 'class', '').addClass('wproto-icon-holder fa-4x' + ' ' + selectedIconName + ' ' + library );
									
									iconInput.val( selectedIconName + ' ' + library );
									linkChooser.text( wprotoVars.strChange );
									$( this ).dialog( "close" );
								},
								Cancel: function() {
									$( this ).dialog( "close" );
								},
								'Remove Icon': function() {
									iconHolder.attr( 'class', '').addClass('wproto-icon-holder icon-2x' ).attr( 'data-name', '' );
									iconInput.val('');
									linkChooser.text( wprotoVars.strSelectIcon );
									$( this ).dialog( "close" );
								}
							}
						});
				
					},
					success: function( response ) {
						dialog.html( response.html );
						var selected = iconHolder.attr('data-name');
						if( selected != '' ) {
							$('#icon-picker-icons i.' + selected ).addClass('selected');
						}
				
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
		
				return false;
			});
	
			/**
				Select an icon
			**/
			$( document ).on('click', '#icon-picker-icons i.wproto-icon-picker-icon', function() {
				$('#icon-picker-icons i').removeClass('selected');
				$(this).addClass('selected');
				return false;
			});
			
			/**
				On / off checkboxes
			**/
			$( document ).on('click', ".cb-enable", function(){
				var parent = $(this).parents('.switch');
				$('.cb-disable',parent).removeClass('selected');
				$(this).addClass('selected');
				$('input[type=hidden]',parent).val('yes').change();
			});
			$( document).on('click', ".cb-disable", function(){
				var parent = $(this).parents('.switch');
				$('.cb-enable',parent).removeClass('selected');
				$(this).addClass('selected');
				$('input[type=hidden]',parent).val('no').change();
			});
			
			/**
				Toggle elements
			**/
			$('input[data-toggle-element]').change( function() {
				var child = $( $(this).data('toggle-element') );
				$(this).val() == 'yes' ? child.show() : child.hide();
				return false;
			});
			
			/**
				Hide installation message box
			**/
			$('#wproto-hide-demo-data-message').click( function() {
		
				var msg = $(this).parent().parent();
				var loader = $('#wproto-dismiss-demodata-loader');
		
				loader.show();
		
				$.post( ajaxurl, { 'action' : 'wproto_dismiss_demo_data_notice' },
					function( response){
						loader.hide();
						msg.fadeOut(800).remove();
					}
				);
		
				return false;
			});
			
			/**
				Scroll infobox
			**/
	
			var infobox = $( '#wproto-info-box');
			var infoboxWidth = infobox.width();
			var infoboxOffset = infobox.offset();
	
			if( infobox.length ) {
		
				$( window).scroll( function () { 

					var scrollTop = $( window).scrollTop();

					if( scrollTop > infoboxOffset.top ) {
						if( infobox.hasClass('scroll') == false ) {
							infobox.addClass( 'scroll').width( infoboxWidth );
						}
			
					} else {
						infobox.removeClass( 'scroll');
					}
	
				});
				
			}
			
			/**
				Turn OFF infobox
			**/
			$('#wproto-turnoff-infobox').click( function() {
		
				var loader = $('#wproto-hide-infobix-loader');
				loader.show();
		
				$.post( ajaxurl, { 'action' : 'wproto_ajax_hide_infobox' },
					function( response){
						loader.hide();
						$('#wproto-screen-right').remove();
						$('#wproto-screen-cols, #wproto-screen-left').removeAttr('id');
						$('#wproto-hide-infobox-input').attr('checked', 'checked').change();
				
						var cParent = $('#wproto-hide-infobox-input').parent();
						cParent.find('.cb-disable').removeClass('selected');
						cParent.find('.cb-enable').addClass('selected');
				
					}
				);
		
				return false;
			});
			
			/**
				Toggles
			**/
			$( document ).on( 'click', 'a.wproto-toggle-form-block', function() {
		
				$(this).parent().next('.wproto-form-table').stop().fadeToggle();
				$(this).next('i').toggleClass('icon-angle-right').toggleClass('icon-angle-down');
		
				return false;
			});
			
			/**
				Set up $ UI Dialogs
			**/
			$( "#dialog" ).dialog({
      		height: 340,
      		width: 400,
      		modal: true,
						buttons: {
        		"Delete all items": function() {
          		$( this ).dialog( "close" );
        		},
        		Cancel: function() {
          		$( this ).dialog( "close" );
        		}
      		}
 			});
			
			// Tabs 
			$( document ).on( 'click', '.wproto-nav-tab-wrapper a', function() {
		
				$( 'div.wproto_tab' ).hide();
				$( $( this ).attr( 'href' ) ).show();
				$( '.wproto-nav-tab-wrapper a' ).removeClass( 'nav-tab-active' );

				$( this ).addClass( 'nav-tab-active' );
		
				$('input[name=wproto_tab]').val( $(this).attr('data-tab-name') );

				window.location.hash = '';
				return false;
			});

			// Tabs hashchange
			if ( "onhashchange" in window ) {
				var hash = window.location.hash;

				var tab = $( hash );
				var tabLinks = $( '.wproto-nav-tab-wrapper a' );

				if( tab.length ) {

					tabLinks.each( function() {
						if( $( this).attr( 'href' ) == hash) {
							tabLinks.removeClass( 'nav-tab-active' );
							$( this).addClass( 'nav-tab-active' );
						}
					});

					$( '.wproto_tab' ).hide();
					tab.show();
				}
		
			}
			
			// Wproto Toggles editor buttons
			$('.wproto-toggles-tabs-title, wproto-toggles-tabs-content').keyup(function() {
				$(this).val($(this).val().replace(/[|]/g, ""));
			});
			
			$( document ).on( 'click', '#wproto-toggles-tabs-items .controls .add, #wproto-progress-items .controls .add', function() {
				var parent = $(this).parent().parent();
				var element = parent.clone(true);
								
				element.find('input[type=text], textarea').val('');
				element.find('input[type=number]').val(1);
				element.insertAfter( parent );
				wprotoSetupTogglesTabsItems();
				return false;
			});
	
			$( document ).on( 'click', '#wproto-toggles-tabs-items .controls .remove, #wproto-progress-items .controls .remove', function() {
				$(this).parent().parent().remove();
				wprotoSetupTogglesTabsItems();
				return false;
			});
			
		},
		
		/**************************************************************************************************************************
			Class methods
		**************************************************************************************************************************/
		
		countAttachedImages: function() {
			var items = jQuery('#wproto-metabox-content .wproto-attached-image-item').length;
	
			var holder = jQuery('#wproto-attached-images-count');
	
			if( items <= 0 ) {
				holder.html( wprotoVars.strNoImagesSelected );
			} else if( items == 1 ) {
				holder.html( wprotoVars.strOneImagesSelected );
			} else {
				holder.html( items + ' ' + wprotoVars.strImagesSelected );
			}
	
		}
		
	}
	
	wprotoBackend.initialize();
	
});