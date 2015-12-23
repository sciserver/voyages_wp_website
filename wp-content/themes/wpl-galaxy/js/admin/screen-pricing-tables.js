jQuery.noConflict()( function($){
	"use strict";

	var wprotoScreenPricingTables = {
	
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
			
			if( $('#wproto-pricing-table-editor').length ) {
		
				$('#wproto-pricing-table-editor tbody').sortable({
					update : function() {
						self.updatePricingTable();
					},
					items: "tr:not(.system-item)"
				});
		
			}
			
		},
		/**
			Set page events
		**/
		events: function() {
			
			var self = this;
			
			// delete feature button
			$( document ).on('click', '.wproto-delete-feature', function() {
		
				$(this).parents('tr').fadeOut( 500, function() { $(this).remove() });
				self.updatePricingTable();
				return false;
			});
			
			// delete package
			$( document ).on( 'click', '.wproto-delete-package', function() {
		
				var table = $('#wproto-pricing-table-editor');
				var index = table.find('tfoot th').index( $(this).parents('th') );
		
				table.find('thead, tfoot').find('tr th:eq(' + index + ')').fadeOut( 500, function() { $(this).remove() });
				table.find('tbody tr').each( function() {
					$(this).find('td:eq(' + index + ')').fadeOut( 500, function() { $(this).remove() })
				});
				self.updatePricingTable();
				return false;
			});
	
			// make package featured
			$( document ).on('click', '.wproto-make-featured-price', function() {
				$('.wproto-make-featured-price').removeClass('button-primary');
				$('.wproto-make-featured-price input').removeAttr('checked');
				$(this).addClass('button-primary');
				$(this).find('input').attr('checked', 'checked');
				return false;
			});
			
			// add package
			$('.wproto-add-pricing-package').click( function() {
		
				var table = $('#wproto-pricing-table-editor');
		
				$( '<th class="package-title"><input name="pt[packages][names][0][]" type="text" value="' + wprotoVars.strPackageName + '" /></th>' ).insertBefore( table.find('thead th:last') );
				$( '<th class="center"><a href="javascript:;" class="wproto-delete-package button"><i class="fa fa-times"></i></a> <a href="javascript:;" class="wproto-make-featured-price button"><i class="fa fa-star"></i><input type="radio" name="pt[pricing_table][featured]" value="0" /></a></th>' ).insertBefore( table.find('tfoot th:last') );
				table.find('tbody tr.system-item').each( function() {

					var html;
		
					if( $(this).hasClass('item-price') ) {
						html = '<td><input name="pt[features][price][0][]" type="text" value="" /></td>';	
						$(html).insertBefore( $(this).find('td:last') );
					}
			
					if( $(this).hasClass('item-details') ) {
						html = '<td><input name="pt[features][details][0][]" type="text" value="" /></td>';	
						$(html).insertBefore( $(this).find('td:last') );				
					}
			
					if( $(this).hasClass('item-button') ) {
						html = '<td><input name="pt[features][button_text][0][]" type="text" value="" /><br /><input name="pt[features][button_url][0][]" type="text" value="" /></td>';	
						$(html).insertBefore( $(this).find('td:last') );
					}

				});
				table.find('tbody tr.custom-item').each( function() {
					var html = '<td><input name="pt[features][user_features_values][0][]" type="text" value="' + wprotoVars.strValue + '" /></td>';	
					$(html).insertBefore( $(this).find('td:last') );
				});
		
				self.updatePricingTable();
				return false;
			});
	
			// add feature
			$('.wproto-add-pricing-feature').click( function() {
		
				var table = $('#wproto-pricing-table-editor');
				var pLen = table.find('thead th').length - 2; 
				var fLen = $('tr.custom-item').length;
				var html = '<tr style="display: none" class="move custom-item"><td class="ex description"><a href="javascript:;" class="button wproto-delete-feature"><i class="fa fa-times"></i></a> <input name="pt[features][user_features_names][' + fLen + '][]" type="text" value="' + wprotoVars.strYourFeature + '" /></td>';
		
				if( pLen > 0 ) {
					for( var i=0; i<pLen; i++ ) {
						html = html + '<td><input name="pt[features][user_features_values][0][]" type="text" value="' + wprotoVars.strValue + '" /></td>';
					}
				}
						
				html = html + '<td class="ex center"><img width="16" height="16" src="' + wprotoVars.moveImgSrc + '" alt="" /></td></tr>';
				table.append( html );
				table.find('tbody tr:last').fadeIn(500, function() {
					self.updatePricingTable();
				});
		
				return false;
			});
			
		},
		
		/**************************************************************************************************************************
			Class methods
		**************************************************************************************************************************/
		updatePricingTable: function() {
	
			var table = $('#wproto-pricing-table-editor');
	
			table.find('thead th').not('.ex').each( function( index ) {
				$(this).find('input').attr('name', 'pt[packages][names][' + index + ']');
			});
	
			table.find('tbody tr').each( function() {
		
				$(this).find('td').not('.ex').each( function( index ) {
			
					var i = index;
			
					$(this).find('input').each( function() {
			
						var currName = $(this).attr('name');
			
						var pattern = /\[[0-9]+\]/i;
						var newName = currName.replace( pattern, '[' + i + ']');
		
						$(this).attr('name', newName);
			
					});
			
				});
		
			});
	
			table.find('tfoot th').not('.ex').each( function( index ) {
				$(this).find('input').attr('name', 'pt[pricing_table][featured]').val( index );
			});
	
		}
	}
	
	wprotoScreenPricingTables.initialize();
	
});