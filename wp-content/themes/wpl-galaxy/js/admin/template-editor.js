jQuery.noConflict()( function($){
	"use strict";

	var wprotoTemplateEditor = {
		
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

			this.checkHexagonTpl();
			this.handleTemplate();
			
			
			if( $('#wproto-tabbed').length ) {
				wprotoEnableTabOnTextarea('wproto-tabbed');
			}
			
		},
		/**
			Set page events
		**/
		events: function() {
			
			var self = this;
			
			$('#page_template').change( function() {
				self.handleTemplate();
			});
			
			/**
				Add new section
			**/
			$('#wproto-lb-add-new-section a.icon, #wproto-lb-add-new-section .add-section-menu > a').click( function(){
				
				var parent = $('#wproto-lb-add-new-section');
				
				parent.find('.add-section-menu > a i').toggleClass('fa-chevron-down fa-chevron-up');
				
				parent.find('.add-section-menu ul').fadeToggle('fast');
				
				return false;
			});
			
			$('.wproto-add-section-links a').click( function() {
				
				var section = $(this).data('section');
				
				//$('#wproto-lb-add-new-section a.icon').addClass('fa-spin');
				
				$('#wproto-lb-add-new-section .add-section-menu ul').fadeOut('fast');
				
				$('#wproto-lb-add-new-section .add-section-menu > a i').toggleClass('fa-chevron-down fa-chevron-up');
				
				tb_show( '', ajaxurl + '?action=wproto_ajax_add_edit_section&subaction=add&type=' + section + '&wproto_admin_noheader&TB_iframe=1');
				
				wprotoFullWidthThickbox();
				
				return false;
			});
			
			/**
				Edit section
			**/
			$('#wproto_tpl_page_custom_layout_builder .sections').on( 'click', 'a.edit-section', function() {
				
				var parent = $(this).parents('.wproto_section');
				var section = parent.data('section-type');
				var id = parent.find('input[type=hidden]').val();
				
				tb_show( '', ajaxurl + '?action=wproto_ajax_add_edit_section&subaction=edit&id=' + id + '&type=' + section + '&wproto_admin_noheader&TB_iframe=1');
				
				wprotoFullWidthThickbox();
				
				return false;
			});
			
			/**
				Sortable sections
			**/
			$('#wproto_tpl_page_custom_layout_builder .sections').sortable({
     		placeholder: "ui-state-highlight"
    	}).disableSelection();
			
			/**
				Delete section
			**/
			$('#wproto_tpl_page_custom_layout_builder').on('click', 'a.delete-section', function() {
				
				var block = $(this).parent();
				var section_id = $(this).parent().find('input[type=hidden]').val();
				
				block.fadeOut( 500, function() {
					block.remove();
				});
				
				$.ajax({
					url: ajaxurl,
					type: "post",
					dataType: "json",
					data: {
						'action' : 'wproto_ajax_delete_section',
						'section_id' : section_id
					},
					beforeSend: function() {

					},
					success: function( response ) {
						
					},
					error: function() {	
						wprotoAlertServerResponseError();
					},
					ajaxError: function() {		
						wprotoAlertAjaxError();
					}
				});
				
				return false;
			});
			
			/**
				Page redirect metabox
			**/
			if( $('div#wproto-redirect-form').length ) {
		
				$('.wproto_redirect_type-input').change( function() {
			
					var val = $(this).val();
			
					if( val == 'page' ) {
						$('#wproto-redirect-form-choose-page').show();
						$('#wproto-redirect-form-choose-url').hide();
					}
			
					if( val == 'url' ) {
						$('#wproto-redirect-form-choose-page').hide();
						$('#wproto-redirect-form-choose-url').show();
					}
				
					return false;
				});
		
			}
			
			/**
				Layout switcher
			**/
			$( document ).on( 'click', '.wproto-content-layout-type a', function(){
				$(this).parent().parent().find('li').removeClass('selected');
				$(this).parent().addClass('selected');
				
				self.checkHexagonTpl();
		
				var layout = $(this).parent().data('layout');
				
				layout == 'hexagon' ? $('#wproto-layout-filters-tr').show() : $('#wproto-layout-filters-tr').hide();
				
				$('input#wproto-content-layout-input').val( layout );
		
				return false;
			});
			
			/**
				Hexagon filters
			**/
			$('#wproto-layout-filters-tr input[type=hidden]').change( function() {
				self.checkHexagonTpl();
			});
			
			/**
				Post categories controls
			**/
			$( document ).on( 'click', '.wproto-display-posts-controls a.button', function(){
		
				var val = $(this).data('display-posts');
				var table = $(this).parents('table');
				var parentTr = $(this).parent().parent();
				var tr = table.find('tr.wproto-display-posts-control-block');
				var selectAllNone = table.find('.wproto-display-posts-controls span.alignright');
				if( $('#page_template').length ) {
					var template = $('#page_template').val();
					var taxList = tr.find('div[data-tpl="' + template + '"]');
				} else {
					var taxList = $('.wproto-posts-categories-chooser-content');
				}

				parentTr.find('input.wproto-display-posts-categories-input').val( val );
		
				$(this).parent().find('a.button').removeClass('button-primary');
				$(this).addClass('button-primary');
		
				switch( val ) {
					case('all'):
						selectAllNone.hide();
						tr.hide();
						tr.find('.wproto-posts-categories-chooser-content').hide();
					break;
					case('only'):
					case('all_except'):
						tr.stop().fadeIn( function() {
							selectAllNone.show();
						});
						tr.find('.wproto-posts-categories-chooser-content').hide();
						taxList.show();
					break;
				}
		
				return false;
			});
			
			// select a category
			$('.wproto-posts-categories-chooser-content a').click( function() {
				$(this).toggleClass('selected');
				var input = $(this).find('input');
				input.attr("checked", !input.attr("checked"));
			});
			
			$( document ).on( 'click', '.wproto-display-posts-controls span.alignright a', function(){
		
				var items = $(this).parents('table').find('.wproto-posts-categories-chooser-content:visible a');
				var action = $(this).hasClass('select-all') ? 'select-all' : 'select-none';
		
				items.each( function() {
			
					if( action == 'select-all' && $(this).hasClass('selected') == false ) {
						$(this).click();
					} else if( action == 'select-none' && $(this).hasClass('selected') == true ) {
						$(this).click();
					}
				
				});
		
		
				return false;
			});
				
			/**
				Sidebar switcher
			**/
			$( document ).on( 'click', '.wproto-sidebars-layouts a', function(){
				$(this).parent().parent().find('li').removeClass('selected');
				$(this).parent().addClass('selected');
		
				var sidebar = $(this).parent().attr('data-sidebar');
				var hidden = $(this).parent().parent().parent().find('.wproto-layout-type-hide-if-no-sidebar');
		
				$('input#wproto-layout-type-input').val( sidebar );
		
				sidebar == 'none' ? hidden.hide() : hidden.show();
		
				return false;
			});
			
			/**
				Media template autocomplete
			**/
			if( $( "#wproto_media_tpl_post_title" ).length ) {
				
				$( "#wproto_media_tpl_post_title" ).autocomplete({
      		//source: ajaxurl + '?action=wproto_autocomplete_posts&post_type=' + $('#wproto_media_tpl_display_type').val(),
      		source: function( request, response ) {
      			
						$.ajax({
          		url: ajaxurl + '?action=wproto_autocomplete_posts',
            	dataType: "json",
          		data: {
            		term : request.term,
            		post_type : $('#wproto_media_tpl_display_type').val()
          		},
          		success: function(data) {
            		response(data);
          		}
        		});
      			
      		},
      		minLength: 2,
      		focus: function( event, ui ) {
						$( "#wproto_media_tpl_post_title" ).val( ui.item.title );
						$( '#wproto_media_tpl_post_id').val( ui.item.value );
      			return false;
     			},
      		select: function( event, ui ) {
						$( "#wproto_media_tpl_post_title" ).val( ui.item.title );
						$( '#wproto_media_tpl_post_id').val( ui.item.value );
						return false;
      		}
    		});
    		
    		$('#wproto_media_tpl_post_id').change( function() {
    			
    			var val = $(this).val();
    			
    			if( $.trim( val ) == '' ) {
    				$( '#wproto_media_tpl_post_id').val( '' );
    			}
    			
    		});
    		
    		$('#wproto_media_tpl_display_type').change( function() {
					$( "#wproto_media_tpl_post_title" ).val( '' );
					$( '#wproto_media_tpl_post_id').val( '' );
    			return false;
    		});
				
			}
			
		},
		/***************************************************************************************************************************
			Class methods
		***************************************************************************************************************************/
		handleTemplate: function() {
			
			if( $('#page_template').length ) {
			
				var template = $('#page_template').val();
			
				$('#adv-settings').find('label[for=wproto_sidebar_settings-hide], label[for=wproto_slider_settings-hide], label[for=wproto_post_appearance_settings-hide], label[for=wproto_tpl_page_contacts-hide], label[for=wproto_tpl_page_layout-hide], label[for=wproto_tpl_page_media_layout-hide], label[for=wproto_tpl_page_custom_layout_builder-hide], label[for=wproto_redirect-hide]').remove();
			
				$('.wproto-display-posts-controls a[data-display-posts=all]').click();

				$('#wproto-product-view-tr, .wproto-posts-categories-chooser-content').hide();
				$('#postdivrich, #commentstatusdiv, .wproto-content-layout-type, .wproto-posts-categories-chooser-content[data-tpl="' + template + '"]').show();
				$('.wproto-content-layout-type a.one-column-list').click();
				$('#wproto_tpl_one_page_template').hide();
			
				switch( template ) {
					default:
					case 'default':
						$('#wproto_sidebar_settings, #wproto_slider_settings, #wproto_post_appearance_settings').show();
						$('#wproto_tpl_page_contacts, #wproto_tpl_page_layout, #wproto_tpl_page_media_layout, #wproto_tpl_page_custom_layout_builder').hide();
					break;
					case 'page-tpl-home-custom.php':
						$('#postdivrich, #commentstatusdiv, #wproto_sidebar_settings, #wproto_slider_settings, #wproto_post_appearance_settings, #wproto_tpl_page_contacts, #wproto_tpl_page_layout, #wproto_tpl_page_media_layout').hide();
						$('#wproto_tpl_page_custom_layout_builder').show();
					break;
					case 'page-tpl-blog.php':
					case 'page-tpl-portfolio.php':
					case 'page-tpl-photoalbums.php':
					case 'page-tpl-catalog.php':
					case 'page-tpl-videos.php':
						$('#wproto_tpl_page_contacts, #wproto_tpl_page_media_layout, #wproto_tpl_page_custom_layout_builder').hide();
						$('#wproto_sidebar_settings, #wproto_slider_settings, #wproto_post_appearance_settings, #wproto_tpl_page_layout').show();
					break;
					case 'page-tpl-media.php':
						$('#postdivrich, #commentstatusdiv, #wproto_post_appearance_settings, #wproto_tpl_page_layout, #wproto_slider_settings, #wproto_sidebar_settings, #wproto_tpl_page_contacts, #wproto_tpl_page_custom_layout_builder').hide();
						$('#wproto_tpl_page_media_layout').show();
					break;
					case 'page-tpl-contacts.php':
						$('#wproto_slider_settings, #wproto_tpl_page_layout, #wproto_post_appearance_settings, #wproto_tpl_page_media_layout, #wproto_tpl_page_custom_layout_builder').hide();
						$('#wproto_tpl_page_contacts, #wproto_sidebar_settings').show();
					break;
					case 'page-tpl-shop.php':
				
						$('.wproto-content-layout-type').hide();
						$('#wproto-product-view-tr').show();
				
						$('#wproto_tpl_page_contacts, #wproto_tpl_page_media_layout, #wproto_tpl_page_custom_layout_builder').hide();
						$('#wproto_sidebar_settings, #wproto_slider_settings, #wproto_post_appearance_settings, #wproto_tpl_page_layout').show();
					break;
					case 'page-tpl-one-page.php':
						$('#postdivrich, #commentstatusdiv, #wproto_sidebar_settings, #wproto_slider_settings, #wproto_post_appearance_settings, #wproto_tpl_page_contacts, #wproto_tpl_page_layout, #wproto_tpl_page_media_layout').hide();
						$('#wproto_tpl_page_custom_layout_builder, #wproto_tpl_one_page_template').show();
					break;
				}
			}
		},
		checkHexagonTpl: function() {
			
			var currentLayout = $('.wproto-content-layout-type li.selected').data('layout');
			
			// items
			var sidebarSettings = $('#wproto_sidebar_settings');
			
			if( currentLayout == 'hexagon' ) {
				$('#wproto_tpl_page_layout #wproto-layout-type-input').val('none');
				sidebarSettings.hide();
				$('#wproto_tpl_page_layout .wproto-sidebars-layouts li').removeClass('selected');
				$('#wproto_tpl_page_layout .wproto-sidebars-layouts li:last').addClass('selected');
			} else {
				sidebarSettings.show();
			}
			
			// check dependencies
			var displayFilters = $('#wproto_tpl_page_layout #wproto-layout-filters-tr input[type=hidden]').val();
			
			if( currentLayout == 'hexagon' && displayFilters == 'yes' ) {
				$('#wproto_tpl_page_layout tr.no-hexagon-with-filters').hide();
			} else {
				$('#wproto_tpl_page_layout #wproto-ls-sort-tr, #wproto_tpl_page_layout #wproto-ls-order-tr, #wproto_tpl_page_layout #wproto-ls-display-from-cats-tr, #wproto_tpl_page_layout #wproto-pagination-show-hide').show();
				
				if( $('#wproto_tpl_page_layout #wproto-ls-display-from-cats-tr .wproto-display-posts-categories-input').val() == 'all' ) {
					$('#wproto_tpl_page_layout .wproto-display-posts-control-block, #wproto_tpl_page_layout .wproto-display-posts-controls .alignright').hide();
				} else {
					$('#wproto_tpl_page_layout .wproto-display-posts-control-block, #wproto_tpl_page_layout .wproto-display-posts-controls .alignright').show();
				}
				
				if( $('#wproto_tpl_page_layout #wproto-pagination-show-hide input[type=hidden]').val() == 'yes' ) {
					$('#wproto_tpl_page_layout .wproto-pagination-settings').show();
				} else {
					$('#wproto_tpl_page_layout .wproto-pagination-settings').hide();
				}
				
			}
			
		}
		
	}
	
	wprotoTemplateEditor.initialize();
	
});