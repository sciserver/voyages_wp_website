jQuery(function($) {

    var cdbx_confirm_delete_msg = "Do you want to delete this code ?";
    var CDBX_EVENT_EDITOR_INIT = 'tinymce-editor-init';
    var CDBX_PRETTYPRINT_CLASS = "prettyprint";
    var CDBX_WEBDESIGN_CLASS = 'cdbxweb prettyprint';
    var cdbx_tmce_click_status_changed = false;

    var cdbx_uniqueId = function() {
       return (new Date().valueOf() + Math.random()).toString();
    };

    var cdbx_reverseId = function(str) {
       return str.split('').reverse().join('');
    };
    
    var cdbx_showDummyDialog = function () {
       if (document.getElementById('cdbx-dummy-dialog') == null) {
          $("<div/>").attr('id', 'cdbx-dummy-dialog').appendTo('body');
          $("#cdbx-dummy-dialog").css('display', 'none');
       }      

       $("#cdbx-dummy-dialog").dialog ({
          title: 'Loading Editor ...',
          dialogClass: 'wp-dialog',
          width: '20%',
          draggable: false,
          modal: true,
          resizable: false,
          closeOnEscape: true,
          position: {
             my: 'center',
             at: 'center',
             of:  window
          },
          open: function () {
             var data = '<p style="text-align:center"><img src="/wp-content/plugins/code-editor-and-compiler/assets/spinner.gif" alt="Loading" width="200" height="100"></p>';  
             $("#cdbx-dummy-dialog").html(data);
             $(".ui-dialog-titlebar-close").hide();  
          }
        });
    };
        
    var cdbx_closeDummyDialog = function () {
        $("#cdbx-dummy-dialog").dialog(CDBX_EVENT_CLOSE);
    };

    $(document).ready(function () {

        var cdbx_editorNode = null;
        var cdbx_editorNode_web = null;
        var cdbx_editorNode_html = null;
        var cdbx_editorNode_css = null;
        var cdbx_editorNode_js = null;
        var pref_loaded = false;
        
        /*if (typeof tinymce != 'undefined') {
           tinymce.PluginManager.add('cdbx_insert_code_button', function( editor, url ) {  
             editor.addButton( 'cdbx_insert_code_button', {
               title: 'Insert Code',
               icon: 'wp_code',
               onclick: function() {
                 $(CDBX_INSERT_CODE).click();   
               }
             });
           });
        }*/

        var cdbx_setMode = function() {
           if (cdbx_curLangId == cdbx_defLangId) {
              cdbx_editor.getSession().setMode(cdbx_defaultMode); 
           } else {
              cdbx_editor.getSession().setMode(cdbx_languages[cdbx_curLangId].mode);
              $(CDBX_FILENAME_EXT).text(cdbx_languages[cdbx_curLangId].ext);   
           }
        };
        
        var cdbx_setTheme = function() {
           cdbx_editor.setTheme(cdbx_curTheme);
           cdbx_editor_html.setTheme(cdbx_curTheme);
           cdbx_editor_css.setTheme(cdbx_curTheme);
           cdbx_editor_js.setTheme(cdbx_curTheme);
        };
        
        var cdbx_setModeWeb = function() {
           cdbx_editor_html.getSession().setMode(cdbx_languages_web[0].mode);
           cdbx_editor_css.getSession().setMode(cdbx_languages_web[1].mode);
           cdbx_editor_js.getSession().setMode(cdbx_languages_web[2].mode);    
        };

        var cdbx_zoomOut = function() {
           var f_size = parseInt(cdbx_editor.getFontSize());
           f_size = f_size - 1;
           cdbx_editor.setFontSize(f_size);
        };

        var cdbx_zoomIn = function() {
           var f_size = cdbx_editor.getFontSize();
           f_size = f_size + 1;
           cdbx_editor.setFontSize(f_size);
        };
        
        var cdbx_zoomOut_web = function() {
           var f_size = parseInt(cdbx_editor_html.getFontSize());
           f_size = f_size - 1;
           cdbx_editor_html.setFontSize(f_size);
           cdbx_editor_css.setFontSize(f_size);
           cdbx_editor_js.setFontSize(f_size);    
        };

        var cdbx_zoomIn_web = function() {
           var f_size = cdbx_editor_html.getFontSize();
           f_size = f_size + 1;
           cdbx_editor_html.setFontSize(f_size);
           cdbx_editor_css.setFontSize(f_size);
           cdbx_editor_js.setFontSize(f_size);    
        };

        var cdbx_cleanUpEditorDiv = function () {
           $(CDBX_DIV_OUTPUT).html(cdbx_default_output);
        };
        
        var activateTabs = function () {
           $('ul.cdbx-tabs li').click(function() {
               var tab_id = $(this).attr('data-tab');

		       $('ul.cdbx-tabs li').removeClass('current');
		       $('.cdbx-tab-content').removeClass('current');

		       $(this).addClass('current');
		       $("#" + tab_id).addClass('current');
	       });
                  
           $('ul.cdbx-tabs-web li').click(function() {
               var tab_id = $(this).attr('data-tab');

		       $('ul.cdbx-tabs-web li').removeClass('current');
		       $('.cdbx-tab-content-web').removeClass('current');

		       $(this).addClass('current');
		       $("#" + tab_id).addClass('current');
	       });                         
        };
        
        var cdbx_updateDOM = function () {
          if (cdbx_curLangId == cdbx_defLangId || cdbx_run_btn_status == 0) {
             $(CDBX_FILENAME).hide();
             $(CDBX_FILENAME_EXT).hide(); 
             $(CDBX_RUN_CODE).prop("disabled", true);
             $(CDBX_STDIN).hide();
             $(CDBX_CMDLINE).hide();
              
             var cdbx_info_html = 'Syntax Highlighter Mode <br>';
             var cdbx_info_html_web = 'Syntax Highlighter Mode <br>';  

             if (cdbx_curLangId == cdbx_defLangId) {
                cdbx_info_html += '<p style="color:#696969"><label style="color:#008B8B">Default programming language is selected.</label><br> Code that you write in any language will only be syntax highlighted in public view. Select a specific language from the drop down menu to run your code.</p>';
             }

             if (cdbx_run_btn_status == 0) {
                /* run button needs to be hidden in web design editor also */
                $(CDBX_RUN_CODE_WEB).prop("disabled", true);
                //$(CDBX_OUTPUT_WEB_LINK).hide();
                cdbx_info_html_web += '<p style="color:#696969"><label style="color:#008B8B">Code execution is disabled.</label><br> Please enable it from <a href="" id="cdbx-global-setting">global settings</a></p>';
                cdbx_info_html += '<p style="color:#696969"><label style="color:#008B8B">Code execution is disabled.</label><br> Please enable it from <a href="" id="cdbx-global-setting">global settings</a></p>'; 
                $(CDBX_DIV_OUTPUT_WEB).html(cdbx_info_html_web); 
             } else {
                $(CDBX_RUN_CODE_WEB).prop("disabled", false);
                $(CDBX_DIV_OUTPUT_WEB).html(cdbx_default_output); 
             }

             $(CDBX_DIV_OUTPUT).html(cdbx_info_html);  
              
          } else {
             $(CDBX_FILENAME).show();
             $(CDBX_FILENAME_EXT).show();  
             $(CDBX_RUN_CODE).prop("disabled", false);
             $(CDBX_STDIN).show();
             $(CDBX_CMDLINE).show();
             $(CDBX_DIV_OUTPUT).html(cdbx_default_output);
              
             $(CDBX_RUN_CODE_WEB).prop("disabled", false);
             $(CDBX_DIV_OUTPUT_WEB).html(cdbx_default_output); 
             //$(CDBX_OUTPUT_WEB_LINK).show(); 
          }
        };


        var cdbx_executeHtmlCode = function(html, css, js, externalCss, externalJs, output_div) {
          	var cdbx_json = {
               action: 'runhtmlcode',
               html : html,
               css : css,
               js : js,
               externalJs : externalJs,
               externalCss : externalCss,    
               url : cdbx_compilebinLinkWebDesign
            };
  
          	$.ajax({
               url : cdbx_ajax_script.ajaxurl,
               type : 'POST',
               async : 'false',
               data : cdbx_json,
               beforeSend: function() {
                  $(CDBX_DIV_OUTPUT_WEB).html(cdbx_output_status_progress);
                  $(CDBX_OUTPUT_WEB_LINK).addClass('disabled').removeAttr("href");  
               },
               success: function(data, textStatus, jqXHR) {
          		  var output = JSON.parse(data);
                  //$(CDBX_OUTPUT_WEB_LINK).attr("href", output.url);
                  var my_iframe = '<iframe class="cdbx-web-output-frame" sandbox="allow-scripts allow-modals" src="' +
                                  output.url + '" allowfullscreen></iframe>';
                  $(CDBX_DIV_OUTPUT_WEB).html(my_iframe);
                  $(CDBX_OUTPUT_WEB_LINK).removeClass('disabled').prop("href", output.url);   
               },
               error: function(jqXHR, textStatus, errorThrown) {
                  $(CDBX_DIV_OUTPUT_WEB).html(cdbx_output_status_fail);
               }
            });
        };
        
        var cdbx_executeCode = function(code, output_div, input, args) {
          	var cdbx_json = {
               action: 'compile',
               language : cdbx_curLangId,
               code : code,
               stdin : input,
               cmdlineargs : args,
          	   fileName : cdbx_progName,
               url : cdbx_compilebinLinkCompile
            };
  
          	$.ajax({
               url : cdbx_ajax_script.ajaxurl,
               type : 'POST',
               async : 'false',
               data : cdbx_json,
               beforeSend: function() {
                  $(CDBX_DIV_OUTPUT).html(cdbx_output_status_progress);
               },
               success: function(data, textStatus, jqXHR) {
          		  var output = JSON.parse(data).output.replace(/\n/g, '<br />');
                  $(CDBX_DIV_OUTPUT).html(output); 
               },
               error: function(jqXHR, textStatus, errorThrown) {
                  $(CDBX_DIV_OUTPUT).html(cdbx_output_status_fail);
               }
            });
        };

        var initEditorDialog = function () {
          $(CDBX_EDITOR_DIALOG).dialog({
            title: 'Code Editor and Compiler',
            dialogClass: 'wp-dialog',
            autoOpen: false,
            draggable: false,
            width: CDBX_EDITOR_DIALOG_WIDTH,
            modal: true,
            resizable: false,
            closeOnEscape: true,
            position: {
              my: 'center',
              at: 'center',
              of:  window
            },
            open: function () {
              cdbx_editor = ace.edit(CDBX_ELEM_COMPILEBIN_EDITOR);
              cdbx_setMode();
              //cdbx_editor.setTheme(CDBX_ACE_THEME_XCODE);
              cdbx_editor.clearSelection();
              cdbx_cleanUpEditorDiv();
              var options = $(CDBX_LANG);
              $.each(cdbx_languages, function(key, val) {
                options.append(new Option(val.name, val.id));
              });
              $(CDBX_LANG).val(cdbx_curLangId);
              cdbx_updateDOM();    
              $(CDBX_FILENAME).val(cdbx_progName);
              if (cdbx_editorNode == null) {
                 $(CDBX_DELETE_CODE).prop("disabled", true);
                 $(CDBX_DELETE_CODE_WEB).prop("disabled", true);
              }
                
              cdbx_editor_html = ace.edit(CDBX_ELEM_COMPILEBIN_EDITOR_HTML);
              //cdbx_editor_html.setTheme(CDBX_ACE_THEME_XCODE);
              cdbx_editor_html.clearSelection();
                
              cdbx_editor_css = ace.edit(CDBX_ELEM_COMPILEBIN_EDITOR_CSS);
              //cdbx_editor_css.setTheme(CDBX_ACE_THEME_XCODE);
              cdbx_editor_css.clearSelection();

              cdbx_editor_js = ace.edit(CDBX_ELEM_COMPILEBIN_EDITOR_JS);
              //cdbx_editor_js.setTheme(CDBX_ACE_THEME_XCODE);
              cdbx_editor_js.clearSelection(); 
                
              if (cdbx_linesHighlight) cdbx_appendHighlightedLines();    
              cdbx_editor.getSession().selection.on('changeSelection', function(e) {
                 var selectionRange = cdbx_editor.getSelectionRange();
                 var startLine = parseInt(selectionRange.start.row) + 1;
                 var endLine = parseInt(selectionRange.end.row) + 1;
                 //var content = cdbx_editor.session.getTextRange(selectionRange);
                 //console.log(startLine + ',' + endLine);
                 $(CDBX_LINES_HIGHLIGHT_NOW).html(startLine + '-' + endLine);
                 $(CDBX_SELECT_LINES).css('display', 'inline');  
              });
                
              if (cdbx_linesHighlightHtml) cdbx_appendHighlightedLinesHtml();    
              cdbx_editor_html.getSession().selection.on('changeSelection', function(e) {
                 var selectionRange = cdbx_editor_html.getSelectionRange();
                 var startLine = parseInt(selectionRange.start.row) + 1;
                 var endLine = parseInt(selectionRange.end.row) + 1;
                 $(CDBX_LINES_HIGHLIGHT_NOW_HTML).html(startLine + '-' + endLine);
                 $(CDBX_SELECT_LINES_HTML).css('display', 'inline');  
              });
                
              if (cdbx_linesHighlightCss) cdbx_appendHighlightedLinesCss();    
              cdbx_editor_css.getSession().selection.on('changeSelection', function(e) {
                 var selectionRange = cdbx_editor_css.getSelectionRange();
                 var startLine = parseInt(selectionRange.start.row) + 1;
                 var endLine = parseInt(selectionRange.end.row) + 1;
                 $(CDBX_LINES_HIGHLIGHT_NOW_CSS).html(startLine + '-' + endLine);
                 $(CDBX_SELECT_LINES_CSS).css('display', 'inline');  
              });
                
              if (cdbx_linesHighlightJs) cdbx_appendHighlightedLinesJs();    
              cdbx_editor_js.getSession().selection.on('changeSelection', function(e) {
                 var selectionRange = cdbx_editor_js.getSelectionRange();
                 var startLine = parseInt(selectionRange.start.row) + 1;
                 var endLine = parseInt(selectionRange.end.row) + 1;
                 $(CDBX_LINES_HIGHLIGHT_NOW_JS).html(startLine + '-' + endLine);
                 $(CDBX_SELECT_LINES_JS).css('display', 'inline');  
              });    
                
              cdbx_setModeWeb(); 
              cdbx_setTheme();
              $('.ui-widget-overlay').bind(CDBX_EVENT_CLICK, function(){
                $(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_CLOSE);
              });
            },
            create: function () {
              $('.ui-dialog-titlebar-close').addClass('ui-button');
            }
          });
        };
        

        $(CDBX_INSERT_CODE).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            
            var data = getEditorModalData();
            if (document.getElementById('cdbx-editor-dialog') == null) {
                  $("<div/>").attr('id', 'cdbx-editor-dialog').appendTo('body');
                  $(CDBX_EDITOR_DIALOG).css('display', 'none');
                }
                $(CDBX_EDITOR_DIALOG).html(data);
                //initEditorDialog();
                cdbx_editorNode = null;
                activateTabs();

                if (!pref_loaded) {
                    // Get current editor and language settings
                    cdbx_showDummyDialog();
                    var prefData = {
                       action: 'get_global_setting',
                       caller: 'admin'
                    };
                    $.ajax({
                       url: cdbx_ajax_script.ajaxurl,
                       type : 'POST',
                       async : 'false',
                       data : prefData,
                       success: function(data, textStatus, jqXHR) {
                          var setObj = $.parseJSON(data);
                          if (setObj.runBtnStatus.length > 0) {
                             cdbx_run_btn_status = parseInt(setObj.runBtnStatus); 
                          }
                          if (setObj.copyBtnStatus.length > 0) {
                             cdbx_copy_btn_status = parseInt(setObj.copyBtnStatus); 
                          } 
                          if (setObj.linenumStatus.length > 0) {
                             cdbx_linenum_status = parseInt(setObj.linenumStatus); 
                          }
                          if (setObj.fullscreenStatus.length > 0) {
                             cdbx_fullscreen_status = parseInt(setObj.fullscreenStatus); 
                          }
                          if (setObj.darkThemeStatus.length > 0) {
                             cdbx_darktheme_status = parseInt(setObj.darkThemeStatus); 
                          }
                          if (setObj.doubleClickStatus.length > 0) {
                             cdbx_tmce_double_click_status = parseInt(setObj.doubleClickStatus);  
                             /*if (cdbx_tmce_double_click_status == 1) {
                                 CDBX_EVENT_TMCE_CLICK = 'dblclick';
                             }*/  
                          }   
                          if (setObj.editorPref.length > 0) {
                             if (setObj.editorPref == CDBX_EDITOR_WEBDESIGN) {
                                $("[data-tab=cdbx-tab-2]").click();
                             }
                             cdbx_curEditorId = cdbx_curEditorIdPref = parseInt(setObj.editorPref);
                          }

                          if (setObj.langPref.length > 0) {  
                             cdbx_curLangId = parseInt(setObj.langPref);
                             cdbx_curLangIdPref = parseInt(setObj.langPref);
                          }
                          if (setObj.themePref.length > 0) {
                             cdbx_curThemeId = cdbx_curThemePrefId = parseInt(setObj.themePref);   
                             switch (parseInt(setObj.themePref)) {
                                 case CDBX_THEME_XCODE : cdbx_curTheme = cdbx_curThemePref = CDBX_ACE_THEME_XCODE; break;
                                 case CDBX_THEME_MONOKAI : cdbx_curTheme = cdbx_curThemePref = CDBX_ACE_THEME_MONOKAI; break;
                                 case CDBX_THEME_COBALT : cdbx_curTheme = cdbx_curThemePref = CDBX_ACE_THEME_COBALT;
                                 default : break;
                             }
                          }
                          initEditorDialog();
                          cdbx_linesHighlight = cdbx_linesHighlightHtml = cdbx_linesHighlightCss = cdbx_linesHighlightJs = null;
                          $(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_OPEN);
                          pref_loaded = true;
                          cdbx_closeDummyDialog();  
                       }
                    });
                } else {
                    cdbx_curLangId = cdbx_curLangIdPref;
                    if (cdbx_curEditorId == CDBX_EDITOR_WEBDESIGN) {
                        $("[data-tab=cdbx-tab-2]").click(); 
                    }
                    initEditorDialog();
                    cdbx_linesHighlight = cdbx_linesHighlightHtml = cdbx_linesHighlightCss = cdbx_linesHighlightJs = null;
                    $(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_OPEN);
                }
                
            /**************************** Deprecated Code ******************************/
            /*var data = {
			   action: 'editor_modal',
               caller: 'admin'   
		    };
            $.ajax({
              url: cdbx_ajax_script.ajaxurl,
              type : 'POST',
              async : 'false',
              data : data,
              success: function(data, textStatus, jqXHR) {
                if (document.getElementById('cdbx-editor-dialog') == null) {
                  $("<div/>").attr('id', 'cdbx-editor-dialog').appendTo('body');
                  $(CDBX_EDITOR_DIALOG).css('display', 'none');
                }
                $(CDBX_EDITOR_DIALOG).html(data);
                //initEditorDialog();
                cdbx_editorNode = null;
                activateTabs();  
                
                // Get current editor and language settings
                var prefData = {
                   action: 'get_global_setting',
                   caller: 'admin'
                };

                $.ajax({
                   url: cdbx_ajax_script.ajaxurl,
                   type : 'POST',
                   async : 'false',
                   data : prefData,
                   success: function(data, textStatus, jqXHR) {
                      var setObj = $.parseJSON(data);
                      if (setObj.runBtnStatus.length > 0) {
                         cdbx_run_btn_status = parseInt(setObj.runBtnStatus); 
                      }
                      if (setObj.editorPref.length > 0) {
                         if (setObj.editorPref == CDBX_EDITOR_WEBDESIGN) {
                            $("[data-tab=cdbx-tab-2]").click(); 
                         }
                         cdbx_curEditorIdPref = parseInt(setObj.editorPref);
                      }
  
                      if (setObj.langPref.length > 0) {  
                         cdbx_curLangId = parseInt(setObj.langPref);
                         cdbx_curLangIdPref = parseInt(setObj.langPref);
                      }
                      if (setObj.themePref.length > 0) {
                         cdbx_curThemeId = cdbx_curThemePrefId = parseInt(setObj.themePref);   
                         switch (parseInt(setObj.themePref)) {
                             case CDBX_THEME_XCODE : cdbx_curTheme = cdbx_curThemePref = CDBX_ACE_THEME_XCODE; break;
                             case CDBX_THEME_MONOKAI : cdbx_curTheme = cdbx_curThemePref = CDBX_ACE_THEME_MONOKAI; break;
                             case CDBX_THEME_COBALT : cdbx_curTheme = cdbx_curThemePref = CDBX_ACE_THEME_COBALT;
                             default : break;
                         }
                      }
                      initEditorDialog();
                      $(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_OPEN);
                   }
                });
                  
                //$(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_OPEN);
              }
            }); */
            /******************************************************************************/
        });

        $(CDBX_SAVE_CODE).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            if (cdbx_editorNode != null) {
               cdbx_editorNode.remove();
               cdbx_editorNode = null;
            }
            var code = cdbx_editor.getSession().getValue();
            if (document.getElementById('cdbx-hidden-content') == null) {
              $("<div/>").attr('id', 'cdbx-hidden-content').appendTo('body');
              $(CDBX_HIDDEN_CONTENT).css('display', 'none');
            }
            $(CDBX_HIDDEN_CONTENT).text(code);
            code = document.getElementById(CDBX_ELEM_HIDDEN_CONTENT).innerHTML;
            var pre_id = cdbx_uniqueId();
            var input_id = cdbx_reverseId(pre_id);
            var lang_id = cdbx_curLangId.toString();
            var file_name = $(CDBX_FILENAME).val();
            var highlight = cdbx_linesHighlight ? cdbx_linesHighlight : '';
            
            var prefix = '<pre id="' + pre_id + '"' + 'data-highlight="' + highlight + '"' + ' class="prettyprint" style="padding:10px;border:1px solid rgba(231, 231, 230, 1);border-radius:10px;overflow:auto;background-color:#FFFFFF;font-size:13px;">';
            
            var suffix = '';
            if (lang_id == cdbx_defLangId) {
               suffix = '<input id="' + input_id + '"' +
                         'class="cdbx-try-code cdbx-btn-main-def"' +
                         'style="background-color:#FFFFFF;margin-bottom:0;color:#008B8B;border: 1px solid rgba(231, 231, 230, 1); border-radius: 10px;font-size:13px;height:30px;min-width:60px;max-width:150px;padding:4px;font-weight:normal;outline:none;display:none;float:right;"' +
                         'type="" value="Run" data-code="' + pre_id + '"' +
                         'data-highlight="' + highlight + '"' +
                         'data-lang="' + lang_id + '"' + 'data-filename="' + file_name + '" /><br></pre><br>';
            } else {
               suffix = '<input id="' + input_id + '"' +
                         'class="cdbx-try-code cdbx-btn-main"' +
                         'style="background-color:#FFFFFF;margin-bottom:0;color:#008B8B;border: 1px solid rgba(231, 231, 230, 1); border-radius: 10px;font-size:13px;height:30px;min-width:60px;max-width:150px;padding:4px;font-weight:normal;outline:none;display:none;float:right;"' +
                         'type="button" value="Run" data-code="' + pre_id + '"' +
                         'data-highlight="' + highlight + '"' +
                         'data-lang="' + lang_id + '"' + 'data-filename="' + file_name + '" /><br></pre><br>';    
            }

            wp.media.editor.insert(prefix + code + suffix);
            $(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_CLOSE);
        });
        
        $(CDBX_SAVE_CODE_WEB).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            if (cdbx_editorNode_html != null) {
               cdbx_editorNode_html.remove();
               cdbx_editorNode_html = null;
            }
            if (cdbx_editorNode_css != null) {
               cdbx_editorNode_css.remove();
               cdbx_editorNode_css = null;
            }
            if (cdbx_editorNode_js != null) {
               cdbx_editorNode_js.remove();
               cdbx_editorNode_js = null;
            }
            if (cdbx_editorNode_web != null) {
               cdbx_editorNode_web.remove();
               cdbx_editorNode_web = null;
            }  
            
            var code_html = cdbx_editor_html.getSession().getValue();
            var code_css = cdbx_editor_css.getSession().getValue();
            var code_js = cdbx_editor_js.getSession().getValue();
            
            if (document.getElementById('cdbx-hidden-content-html') == null) {
              $("<div/>").attr('id', 'cdbx-hidden-content-html').appendTo('body');
              $(CDBX_HIDDEN_CONTENT_HTML).css('display', 'none');
            }
            
            if (document.getElementById('cdbx-hidden-content-css') == null) {
              $("<div/>").attr('id', 'cdbx-hidden-content-css').appendTo('body');
              $(CDBX_HIDDEN_CONTENT_CSS).css('display', 'none');
            }
            
            if (document.getElementById('cdbx-hidden-content-js') == null) {
              $("<div/>").attr('id', 'cdbx-hidden-content-js').appendTo('body');
              $(CDBX_HIDDEN_CONTENT_JS).css('display', 'none');
            }
            
            $(CDBX_HIDDEN_CONTENT_HTML).text(code_html);
            $(CDBX_HIDDEN_CONTENT_CSS).text(code_css);
            $(CDBX_HIDDEN_CONTENT_JS).text(code_js);
            
            code_html = document.getElementById(CDBX_ELEM_HIDDEN_CONTENT_HTML).innerHTML;
            code_css = document.getElementById(CDBX_ELEM_HIDDEN_CONTENT_CSS).innerHTML;
            code_js = document.getElementById(CDBX_ELEM_HIDDEN_CONTENT_JS).innerHTML;
            
            var pre_id = cdbx_uniqueId();
            var input_id = cdbx_reverseId(pre_id);
            
            var pre_id_html = pre_id + 'html';
            var pre_id_css = pre_id + 'css';
            var pre_id_js = pre_id + 'js';
            
            var highlightHtml = cdbx_linesHighlightHtml ? cdbx_linesHighlightHtml : '';
            var highlightCss = cdbx_linesHighlightCss ? cdbx_linesHighlightCss : '';
            var highlightJs = cdbx_linesHighlightJs ? cdbx_linesHighlightJs : '';
            
            var prefix = '<div id="' + pre_id + '"' + ' class="cdbxweb prettyprint">';
            var suffix = '</div>';
            
            var html_suffix = '<input id="' + input_id + '"' +
                         'class="cdbx-try-code-web cdbx-btn-main"' +
                         'style="background-color:#FFFFFF;margin-bottom:0;color:#008B8B;border: 1px solid rgba(231, 231, 230, 1); border-radius: 10px;font-size:13px;height:30px;min-width:110px;max-width:220px;padding:4px;font-weight:normal;outline:none;display:none;float:right;"' +
                         'type="button" value="Run HTML" data-lang="html" data-code="' + pre_id + '"' +
                         '" /></pre>';
            
            var css_suffix = '<input id="' + input_id + '"' +
                         'class="cdbx-try-code-web cdbx-btn-main"' +
                         'type="button" value="Run CSS" data-lang="css" data-code="' + pre_id + '"' +
                         'style="background-color:#FFFFFF;margin-bottom:0;color:#008B8B;border: 1px solid rgba(231, 231, 230, 1); border-radius: 10px;font-size:13px;height:30px;min-width:110px;max-width:220px;padding:4px;font-weight:normal;outline:none;display:none;float:right;"' +
                         '" /></pre>';
            
            var js_suffix = '<input id="' + input_id + '"' +
                         'class="cdbx-try-code-web cdbx-btn-main"' +
                         'type="button" value="Run Javascript" data-lang="js" data-code="' + pre_id + '"' +
                         'style="background-color:#FFFFFF;margin-bottom:0;color:#008B8B;border: 1px solid rgba(231, 231, 230, 1); border-radius: 10px;font-size:13px;height:30px;min-width:110px;max-width:220px;padding:4px;font-weight:normal;outline:none;display:none;float:right;"' +
                         '" /></pre>';

            var html_code_prefix = '<pre id="' + pre_id_html + '"' + 'data-lang="html" data-highlight="' + highlightHtml + '"' + ' class="cdbxweb prettyprint" style="padding:10px;overflow:auto;border:1px solid rgba(231, 231, 230, 1);border-radius:10px;margin-bottom:5px;background-color:#FFFFFF;font-size:13px;">';
            var html_code_div = html_code_prefix + code_html + html_suffix;
            
            var css_code_prefix = '<pre id="' + pre_id_css + '"' + 'data-lang="css" data-highlight="' + highlightCss + '"' + ' class="cdbxweb prettyprint" style="padding:10px;overflow:auto;border:1px solid rgba(231, 231, 230, 1);border-radius:10px;margin-bottom:5px;background-color:#FFFFFF;font-size:13px;">';
            var css_code_div = css_code_prefix + code_css + css_suffix;
            
            var js_code_prefix = '<pre id="' + pre_id_js + '"' + 'data-lang="js" data-highlight="' + highlightJs + '"' + ' class="cdbxweb prettyprint" style="padding:10px;overflow:auto;border:1px solid rgba(231, 231, 230, 1);border-radius:10px;margin-bottom:5px;background-color:#FFFFFF;font-size:13px;">';
            var js_code_div = js_code_prefix + code_js + js_suffix;
            
            var code_web = prefix;
            if (code_html.length > 0) {
              code_web += html_code_div;    
            }
            if (code_css.length > 0) {
              code_web += css_code_div;   
            }
            if (code_js.length > 0) {
              code_web += js_code_div;    
            }
            code_web += suffix;
            
            wp.media.editor.insert(code_web);
            $(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_CLOSE);

        });

        $(CDBX_DELETE_CODE).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            if (confirm(cdbx_confirm_delete_msg)) {
               if (cdbx_editorNode != null) {
                  cdbx_editorNode.remove();
                  cdbx_editorNode = null;
               }
               $(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_CLOSE);
            }
        });
        
        $(CDBX_DELETE_CODE_WEB).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            if (confirm(cdbx_confirm_delete_msg)) {    
               if (cdbx_editorNode_html != null) {
                  cdbx_editorNode_html.remove();
                  cdbx_editorNode_html = null;
               }
               if (cdbx_editorNode_css != null) {
                  cdbx_editorNode_css.remove();
                  cdbx_editorNode_css = null;
               }
               if (cdbx_editorNode_js != null) {
                  cdbx_editorNode_js.remove();
                  cdbx_editorNode_js = null;
               }
               if (cdbx_editorNode_web != null) {
                  cdbx_editorNode_web.remove();
                  cdbx_editorNode_web = null;
               }    
               $(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_CLOSE);
            }
        });

        $(CDBX_RUN_CODE).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            var code = cdbx_editor.getSession().getValue();
	        var output_div = document.getElementById(CDBX_ELEM_DIV_OUTPUT);
	        var stdin = $(CDBX_STDIN).val();
	        var cmdline = $(CDBX_CMDLINE).val();
            var cdbx_fileName = $(CDBX_FILENAME).val();
            if (cdbx_fileName.length > 0) {
               cdbx_progName = cdbx_fileName;
            }
	        cdbx_executeCode(code, output_div, stdin, cmdline);
        });
        
        $(CDBX_RUN_CODE_WEB).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            var html = cdbx_editor_html.getSession().getValue();
            var css = cdbx_editor_css.getSession().getValue();
            var js = cdbx_editor_js.getSession().getValue();
            var externalCss = '';
            var externalJs = '';
	        var output_div = document.getElementById(CDBX_ELEM_DIV_OUTPUT);
	        cdbx_executeHtmlCode(html, css, js, externalCss, externalJs, output_div);
        });
        
        $(CDBX_OUTPUT_WEB_LINK).live(CDBX_EVENT_CLICK, function (e) {
            if ($(this).attr('href') == "") {
               e.preventDefault();
            }
        });

        $(CDBX_LANG).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            cdbx_curLangId = $(this).find('option:selected').val();
            cdbx_setMode();
            cdbx_updateDOM();
        });

        $(CDBX_ACE_THEME_CLASS).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            if (e.currentTarget.id == CDBX_ACE_THEME_XCODE_ID) {
              cdbx_editor.setTheme(CDBX_ACE_THEME_XCODE);
            } else if (e.currentTarget.id == CDBX_ACE_THEME_MONOKAI_ID) {
              cdbx_editor.setTheme(CDBX_ACE_THEME_MONOKAI);
            } else if (e.currentTarget.id == CDBX_ACE_THEME_COBALT_ID) {
              cdbx_editor.setTheme(CDBX_ACE_THEME_COBALT);
            }
        });
        
        $(CDBX_ACE_THEME_CLASS_WEB).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            if (e.currentTarget.id == CDBX_ACE_THEME_XCODE_ID_WEB) {
              cdbx_editor_html.setTheme(CDBX_ACE_THEME_XCODE);
              cdbx_editor_css.setTheme(CDBX_ACE_THEME_XCODE);
              cdbx_editor_js.setTheme(CDBX_ACE_THEME_XCODE);    
            } else if (e.currentTarget.id == CDBX_ACE_THEME_MONOKAI_ID_WEB) {
              cdbx_editor_html.setTheme(CDBX_ACE_THEME_MONOKAI);
              cdbx_editor_css.setTheme(CDBX_ACE_THEME_MONOKAI);
              cdbx_editor_js.setTheme(CDBX_ACE_THEME_MONOKAI);    
            } else if (e.currentTarget.id == CDBX_ACE_THEME_COBALT_ID_WEB) {
              cdbx_editor_html.setTheme(CDBX_ACE_THEME_COBALT);
              cdbx_editor_css.setTheme(CDBX_ACE_THEME_COBALT);
              cdbx_editor_js.setTheme(CDBX_ACE_THEME_COBALT);    
            }
        });

        $(CDBX_ACE_FONT_ZOOMOUT).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            cdbx_zoomOut();
        });

        $(CDBX_ACE_FONT_ZOOMIN).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            cdbx_zoomIn();
        });
        
        $(CDBX_ACE_FONT_ZOOMOUT_WEB).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            cdbx_zoomOut_web();
        });

        $(CDBX_ACE_FONT_ZOOMIN_WEB).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            cdbx_zoomIn_web();
        });

        /*$(CDBX_CODE_HELP).on(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            $(CDBX_CODE_HELP_DIALOG).dialog(CDBX_EVENT_OPEN);
        });*/
      
        var initSettingDialog = function() {
          $(CDBX_SETTING_DIALOG).dialog({
            title: 'API KEY',
            dialogClass: 'wp-dialog',
            autoOpen: false,
            draggable: false,
            width: CDBX_SETTING_DIALOG_WIDTH,
            modal: true,
            resizable: false,
            closeOnEscape: true,
            position: {
              my: 'center',
              at: 'center',
              of:  window
            },
            open: function () {
              $('.ui-widget-overlay').bind(CDBX_EVENT_CLICK, function() {
                $(CDBX_SETTING_DIALOG).dialog(CDBX_EVENT_CLOSE);
              })
            },
            create: function () {
              $('.ui-dialog-titlebar-close').addClass('ui-button');
            }
          });  
        };
      
        $(CDBX_SETTING).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            if (document.getElementById('cdbx-setting-dialog') == null) {
              $("<div/>").attr('id', 'cdbx-setting-dialog').appendTo('body');
              $(CDBX_SETTING_DIALOG).css('display', 'none');
            }
            var data = '<div class="cdbx-dialog-box">' +
                       '<div id="cdbx-api-key-save-msg" style="color:#000080"></div>' +
                       '<span class="cdbx-label-text">Enter your secret API Key</span><br><br>' +
                       '<input id="cdbx-api-key" class="cdbx-textbox-key" placeholder="Your key"><br><br>' +
                       '<button type="button" id="cdbx-save-key" class="button button-primary"><b>Save Now</b></button>' +
                       '<button type="button" id="cdbx-save-key-close" class="button button-info" style="margin-left:0.2em"><b>Cancel</b></button><br><br>' +
                       'Don\'t have API key ? &nbsp;&nbsp;<a target="_blank" href="https://www.compilebin.com/authentication/signup">Sign Up</a> &nbsp;&nbsp;now to get one.' +
                       '</div>'
                       ;
            $(CDBX_SETTING_DIALOG).html(data);
            initSettingDialog();
            $(CDBX_SETTING_DIALOG).dialog(CDBX_EVENT_OPEN);
        });
        
        $(CDBX_SAVE_KEY_CLOSE).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            $(CDBX_SETTING_DIALOG).dialog(CDBX_EVENT_CLOSE); 
        });
      
        $(CDBX_SAVE_KEY).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            var cdbx_json = {
               action : 'save_key',
               key : $(CDBX_API_KEY).val()
            };
            if (cdbx_json.key.length == 0) {
              $(CDBX_API_KEY_SAVE_MSG).html(cdbx_key_empty);
              return false;
            }
          	$.ajax({
               url : cdbx_ajax_script.ajaxurl,
               type : 'POST',
               async : 'false',
               data : cdbx_json,
               beforeSend: function() {
                  $(CDBX_API_KEY_SAVE_MSG).html(cdbx_key_save_progress);
               },
               success: function(data, textStatus, jqXHR) {
                  $(CDBX_API_KEY_SAVE_MSG).html(data);
                  $(CDBX_API_KEY).val('');
               },
               error: function(jqXHR, textStatus, errorThrown) {
                  $(CDBX_API_KEY_SAVE_MSG).html(cdbx_key_save_fail);
               }
            });
        });
        
        var initGlobalSettingDialog = function() {
          $(CDBX_GLOBAL_SETTING_DIALOG).dialog({
            title: 'GLOBAL SETTINGS',
            dialogClass: 'wp-dialog',
            autoOpen: false,
            draggable: false,
            width: CDBX_GLOBAL_SETTING_DIALOG_WIDTH,
            modal: true,
            resizable: false,
            closeOnEscape: true,
            position: {
              my: 'center',
              at: 'center',
              of:  window
            },
            open: function () {
              $('.ui-widget-overlay').bind(CDBX_EVENT_CLICK, function() {  
                $(CDBX_GLOBAL_SETTING_DIALOG).dialog(CDBX_EVENT_CLOSE);
                if (cdbx_tmce_click_status_changed) {
                  location.reload(true);    
                }  
              })
            },
            create: function () {
              $('.ui-dialog-titlebar-close').addClass('ui-button');
              $('.ui-dialog-titlebar-close').click(function(e) {
                 e.preventDefault();
                 if (cdbx_tmce_click_status_changed) {
                   location.reload(true);    
                 }  
              });
            }
          });  
        };
        
        $(CDBX_GLOBAL_SETTING_CLOSE).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            $(CDBX_GLOBAL_SETTING_DIALOG).dialog(CDBX_EVENT_CLOSE);
            if (cdbx_tmce_click_status_changed) {
              location.reload(true);    
            }
        });
        
        $(CDBX_SAVE_GLOBAL_SETTING).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();

            var cdbx_json = {
               action: 'save_global_setting',
               run_btn_status: $(CDBX_RUN_BTN_STATUS).is(":checked") ? 0 : 1,
               fullscreen_status: $(CDBX_FULLSCREEN_STATUS).is(":checked") ? 1 : 0,
               copy_btn_status: $(CDBX_COPY_BTN_STATUS).is(":checked") ? 1 : 0,
               editor_type: $(CDBX_PREF_EDITOR).find('option:selected').val(),
               lang: $(CDBX_PREF_LANG).find('option:selected').val(),
               theme: $(CDBX_PREF_THEME).find('option:selected').val(),
               linenum_status: $(CDBX_LINENUM_STATUS).is(":checked") ? 1 : 0,
               darktheme_status: $(CDBX_DARKTHEME_STATUS).is(":checked") ? 1 : 0,
               doubleclick_status: $(CDBX_TMCE_DOUBLE_CLICK_STATUS).is(":checked") ? 1 : 0    
            };
  
          	$.ajax({
               url : cdbx_ajax_script.ajaxurl,
               type : 'POST',
               async : 'false',
               data : cdbx_json,
               beforeSend: function() {
                   $(CDBX_GLOBAL_SETTING_SAVE_MSG).html(cdbx_global_setting_save_progress);
               },
               success: function(data, textStatus, jqXHR) {
          		   $(CDBX_GLOBAL_SETTING_SAVE_MSG).html(data);
                   cdbx_curLangId = cdbx_json.lang;
                   cdbx_curLangIdPref = cdbx_json.lang;
                   cdbx_setMode();
                   $(CDBX_LANG).val(cdbx_curLangId);
                   if (cdbx_json.editor_type == CDBX_EDITOR_STANDARD) {
                       cdbx_curEditorId = cdbx_curEditorIdPref = CDBX_EDITOR_STANDARD;
                       $("[data-tab=cdbx-tab-1]").click();
                   } else {
                       cdbx_curEditorId = cdbx_curEditorIdPref = CDBX_EDITOR_WEBDESIGN;
                       $("[data-tab=cdbx-tab-2]").click();
                   }
                   cdbx_curThemeId = cdbx_json.theme;
                   cdbx_curThemePrefId = cdbx_json.theme;
                   switch (parseInt(cdbx_curThemeId)) {
                      case CDBX_THEME_XCODE : cdbx_curTheme = cdbx_curThemePref = CDBX_ACE_THEME_XCODE; break;
                      case CDBX_THEME_MONOKAI : cdbx_curTheme = cdbx_curThemePref = CDBX_ACE_THEME_MONOKAI; break;
                      case CDBX_THEME_COBALT : cdbx_curTheme = cdbx_curThemePref = CDBX_ACE_THEME_COBALT;
                      default : break;
                   }
                   cdbx_setTheme();
                   cdbx_run_btn_status = cdbx_json.run_btn_status;
                   cdbx_linenum_status = cdbx_json.linenum_status;
                   cdbx_copy_btn_status = cdbx_json.copy_btn_status;
                   cdbx_fullscreen_status = cdbx_json.fullscreen_status;
                   cdbx_darktheme_status = cdbx_json.darktheme_status;
                   if (cdbx_tmce_double_click_status != parseInt(cdbx_json.doubleclick_status)) {
                       cdbx_tmce_click_status_changed = true;
                   }
                   cdbx_tmce_double_click_status = cdbx_json.doubleclick_status;
                   /*if (parseInt(cdbx_tmce_double_click_status) == 1) {
                       CDBX_EVENT_TMCE_CLICK = 'dblclick';
                   }*/
                   cdbx_updateDOM();
               },
               error: function(jqXHR, textStatus, errorThrown) {
                   $(CDBX_GLOBAL_SETTING_SAVE_MSG).html(cdbx_global_setting_save_fail);
               }
            });
        });
        
        $(CDBX_GLOBAL_SETTING).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            if (document.getElementById('cdbx-global-setting-dialog') == null) {
              $("<div/>").attr('id', 'cdbx-global-setting-dialog').appendTo('body');
              $(CDBX_GLOBAL_SETTING_DIALOG).css('display', 'none');
            }
            var data = '<p class="cdbx-info-text" style="margin-top:-0.5em;">These settings apply to all code snippets on your website.</p>' +
                       '<div class="cdbx-dialog-box">' +
                       '<div id="cdbx-global-setting-save-msg" style="color:#000080"></div>' +
                       '<input type="checkbox" id="cdbx-run-btn-status">&nbsp;&nbsp;<span class="cdbx-label-text">Disable code execution</span>&nbsp&nbsp&nbsp&nbsp<span class="cdbx-info-text-1">Syntax highlighter mode only. Run button will not be visible in code snippets.</span><br><br>' +
                       '<div id="cdbx-fullscreen-status-div"><input type="checkbox" id="cdbx-fullscreen-status">&nbsp;&nbsp;<span class="cdbx-label-text">Enable code editor fullscreen</span>&nbsp&nbsp&nbsp&nbsp<span class="cdbx-info-text-1">Editor in public view can be made fullscreen on click of a button.</span><br><br></div>' +
                       '<input type="checkbox" id="cdbx-copy-btn-status">&nbsp;&nbsp;<span class="cdbx-label-text">Show Copy button</span>&nbsp&nbsp&nbsp&nbsp<span class="cdbx-info-text-1">Copy code to clipboard in public view.</span><br><br>' +
                       '<input type="checkbox" id="cdbx-linenum-status">&nbsp;&nbsp;<span class="cdbx-label-text">Show line numbers</span>&nbsp&nbsp&nbsp&nbsp<span class="cdbx-info-text-1">Display line numbers in syntax highlighted code.</span><br><br>' +
                       '<input type="checkbox" id="cdbx-darktheme-status">&nbsp;&nbsp;<span class="cdbx-label-text">Enable Dark Theme</span>&nbsp&nbsp&nbsp&nbsp<span class="cdbx-info-text-1">Dark theme for all code anippets in public view.</span><br><br>' +
                       '<span class="cdbx-label-text">Preferred Editor</span> &nbsp;&nbsp;<select name="cdbx-pref-editor" id="cdbx-pref-editor" style=""></select>&nbsp&nbsp&nbsp&nbsp<span class="cdbx-info-text-1">Default code editor.</span><br><br>' +
                       '<span class="cdbx-label-text">Preferred Language</span> &nbsp;&nbsp;<select name="cdbx-pref-lang" id="cdbx-pref-lang" style=""></select>&nbsp&nbsp&nbsp&nbsp<span class="cdbx-info-text-1">Default programming language.</span><br><br>' +
                       '<span class="cdbx-label-text">Preferred Editor Theme</span> &nbsp;&nbsp;<select name="cdbx-pref-theme" id="cdbx-pref-theme" style=""></select>&nbsp&nbsp&nbsp&nbsp<span class="cdbx-info-text-1">Default editor theme applicable to both admin and public views.</span><br><br>' +
                       '<input type="checkbox" id="cdbx-tmce-doubleclick-status">&nbsp;&nbsp;<span class="cdbx-label-text">Double click to edit saved code.</span>&nbsp&nbsp&nbsp&nbsp<span class="cdbx-info-text-1">Pop up dialog to edit saved code with double click instead of single click in admin view.</span>' +
                       '<br><br><br>' +
                       '<button type="button" id="cdbx-save-global-setting" class="button button-primary"><b>Save Now</b></button>&nbsp;&nbsp;' +
                       '<button type="button" id="cdbx-global-setting-close" class="button button-info"><b>Cancel</b></button>' +
                       '</div>'
                       ;
            
            $(CDBX_GLOBAL_SETTING_DIALOG).html(data);
            
            var optionsEditor = $(CDBX_PREF_EDITOR);
              $.each(cdbx_editor_type, function(key, val) {
                optionsEditor.append(new Option(val.name, val.id));
              });
            $(CDBX_PREF_EDITOR).val(cdbx_curEditorIdPref);
            
            var optionsLang = $(CDBX_PREF_LANG);
              $.each(cdbx_languages, function(key, val) {
                optionsLang.append(new Option(val.name, val.id));
              });
            $(CDBX_PREF_LANG).val(cdbx_curLangIdPref);
            
            var optionsTheme = $(CDBX_PREF_THEME);
              $.each(cdbx_editor_theme, function(key, val) {
                optionsTheme.append(new Option(val.name, val.id));
              });
            $(CDBX_PREF_THEME).val(cdbx_curThemePrefId);
            
            if (!cdbx_run_btn_status) {
                // enable the checkbox to hide run button
                $(CDBX_RUN_BTN_STATUS).prop('checked', true);
                $(CDBX_FULLSCREEN_STATUS_DIV).css('display', 'none');
            }
            
            if (cdbx_copy_btn_status) {
                // enable the checkbox to show copy button
                $(CDBX_COPY_BTN_STATUS).prop('checked', true); 
            }
            
            if (cdbx_fullscreen_status) {
                // enable the checkbox for fullscreen editor
                $(CDBX_FULLSCREEN_STATUS).prop('checked', true);
            }
            
            if (cdbx_linenum_status) {
                // enable the checkbox to display line numbers
                $(CDBX_LINENUM_STATUS).prop('checked', true);  
            }
            
            if (cdbx_darktheme_status) {
                // enable the checkbox for darktheme
                $(CDBX_DARKTHEME_STATUS).prop('checked', true);
            }
            
            if (cdbx_tmce_double_click_status) {
                $(CDBX_TMCE_DOUBLE_CLICK_STATUS).prop('checked', true);
            }
            
            initGlobalSettingDialog();
            $(CDBX_GLOBAL_SETTING_DIALOG).dialog(CDBX_EVENT_OPEN);
        });
        
        $(CDBX_RUN_BTN_STATUS).live(CDBX_EVENT_CLICK, function (e) {
            var run_btn_status = $(CDBX_RUN_BTN_STATUS).is(":checked") ? 0 : 1;
            if (!run_btn_status) {
                $(CDBX_FULLSCREEN_STATUS_DIV).css('display', 'none');
            } else {
                $(CDBX_FULLSCREEN_STATUS_DIV).css('display', 'block');
            }
        });
        
        $(CDBX_TAB_STANDARD).live(CDBX_EVENT_CLICK, function (e) {
            $(CDBX_TABS_WEB).css('display', 'none');
            $(CDBX_TABS_PLACEHOLDER).css('display', 'block');
        });
        
        $(CDBX_TAB_WEBDESIGN).live(CDBX_EVENT_CLICK, function (e) {
            $(CDBX_TABS_WEB).css('display', 'block');
            $(CDBX_TABS_PLACEHOLDER).css('display', 'none');
        });
        
        $(CDBX_TAB_WEB_HTML).live(CDBX_EVENT_CLICK, function (e) {
            cdbx_active_tab_web = CDBX_TAB_HTML_ID;
            cdbx_updateHighlightArea();
        });
        
        $(CDBX_TAB_WEB_CSS).live(CDBX_EVENT_CLICK, function (e) {
            cdbx_active_tab_web = CDBX_TAB_CSS_ID;
            cdbx_updateHighlightArea();
        });
        
        $(CDBX_TAB_WEB_JS).live(CDBX_EVENT_CLICK, function (e) {
            cdbx_active_tab_web = CDBX_TAB_JS_ID;
            cdbx_updateHighlightArea();
        });
        
        $(CDBX_CODE_LINES_HIGHLIGHT).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            if ($(CDBX_CODE_LINES_HIGHLIGHT_AREA).css('display') == 'block') {
                $(CDBX_CODE_LINES_HIGHLIGHT_AREA).css('display', 'none');
            } else {
                $(CDBX_CODE_LINES_HIGHLIGHT_AREA).css('display', 'block');
            }
        });
        
        $(CDBX_CODE_LINES_HIGHLIGHT_WEB).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            if (cdbx_highlight_area_active) {
                $(CDBX_CODE_LINES_HIGHLIGHT_AREA_HTML).css('display', 'none');
                $(CDBX_CODE_LINES_HIGHLIGHT_AREA_CSS).css('display', 'none');
                $(CDBX_CODE_LINES_HIGHLIGHT_AREA_JS).css('display', 'none');
                cdbx_highlight_area_active = false;
            } else {
                cdbx_highlight_area_active = true;
                cdbx_updateHighlightArea();
            }
            /*if ($(CDBX_CODE_LINES_HIGHLIGHT_AREA_HTML).css('display') == 'block') {
                $(CDBX_CODE_LINES_HIGHLIGHT_AREA_HTML).css('display', 'none');
                $(CDBX_CODE_LINES_HIGHLIGHT_AREA_CSS).css('display', 'none');
                $(CDBX_CODE_LINES_HIGHLIGHT_AREA_JS).css('display', 'none');
            } else {
                $(CDBX_CODE_LINES_HIGHLIGHT_AREA_HTML).css('display', 'block');
                $(CDBX_CODE_LINES_HIGHLIGHT_AREA_CSS).css('display', 'block');
                $(CDBX_CODE_LINES_HIGHLIGHT_AREA_JS).css('display', 'block');
            } */
        });
        
        var cdbx_updateHighlightArea = function () {
            if (cdbx_highlight_area_active) {
                $(CDBX_CODE_LINES_HIGHLIGHT_AREA_HTML).css('display', 'none');
                $(CDBX_CODE_LINES_HIGHLIGHT_AREA_CSS).css('display', 'none');
                $(CDBX_CODE_LINES_HIGHLIGHT_AREA_JS).css('display', 'none');
                switch (cdbx_active_tab_web) {
                    case CDBX_TAB_HTML_ID : $(CDBX_CODE_LINES_HIGHLIGHT_AREA_HTML).css('display', 'block'); break;
                    case CDBX_TAB_CSS_ID  : $(CDBX_CODE_LINES_HIGHLIGHT_AREA_CSS).css('display', 'block');  break;
                    case CDBX_TAB_JS_ID   : $(CDBX_CODE_LINES_HIGHLIGHT_AREA_JS).css('display', 'block');   break;    
                };    
            }
        };
        
        $(CDBX_SELECT_LINES).live(CDBX_EVENT_CLICK, function (e) {
            var selectedLines = $(CDBX_LINES_HIGHLIGHT_NOW).text();
            if (cdbx_linesHighlight) {
                if (!cdbx_detectDuplicateOverlapHighlight(selectedLines)) {
                    cdbx_linesHighlight += ',' + selectedLines;
                }
            } else {
                cdbx_linesHighlight = selectedLines;
            }
            
            cdbx_appendHighlightedLines();
            cdbx_editor.clearSelection();
        });
        
        $(CDBX_REMOVE_HIGHLIGHT_LINES).live(CDBX_EVENT_CLICK, function (e) {
            var idx = parseInt($(this).attr('id').split('@')[1]);
            var linesGroup = cdbx_linesHighlight.split(',');
            linesGroup.splice(idx, 1);
            var linestr = '';
            for (var i = 0; i < linesGroup.length; i++) {
                linestr += linesGroup[i];
                if (i != linesGroup.length - 1) {
                    linestr += ',';
                }
            }
            cdbx_linesHighlight = linestr;
            cdbx_appendHighlightedLines();
        });
        
        var cdbx_appendHighlightedLines = function () {
            $(CDBX_LINES_HIGHLIGHTED_HIDDEN).html(cdbx_linesHighlight);
            if (!cdbx_linesHighlight  || cdbx_linesHighlight.length == 0) {
                $(CDBX_LINES_HIGHLIGHTED).html(cdbx_linesHighlight);
                return;
            }
            var linesGroup = cdbx_linesHighlight.split(',');
            var currentHighlights = '';
            for (var i = 0; i < linesGroup.length; i++) {
                currentHighlights +=
                    '<span> \
                        <a id="cdbx_remove_highlight@' + i + '" class="cdbx-remove-highlight-lines" style="cursor:pointer;" title="Remove highlight"> \
                            <span class="dashicons dashicons-no"></span> ' + '<span style="margin-top:0.5em">' + linesGroup[i] + '</span>' + 
                        '</button> \
                    </span>';
                currentHighlights += '&nbsp;&nbsp;&nbsp;';
            }
            $(CDBX_LINES_HIGHLIGHTED).html(currentHighlights);
        };
        
        var cdbx_detectDuplicateOverlapHighlight = function (selectedLines) {
            var linesGroup = cdbx_linesHighlight.split(',');
            for (var i = 0; i < linesGroup.length; i++) {
                if (selectedLines == linesGroup[i]) {
                    alert('Duplicate highlight range !!!');
                    return true;
                }
            }
            return false;
        };
        
        $(CDBX_SELECT_LINES_HTML).live(CDBX_EVENT_CLICK, function (e) {
            var selectedLines = $(CDBX_LINES_HIGHLIGHT_NOW_HTML).text();
            if (cdbx_linesHighlightHtml) {
                if (!cdbx_detectDuplicateOverlapHighlightWeb(selectedLines, cdbx_linesHighlightHtml)) {
                    cdbx_linesHighlightHtml += ',' + selectedLines;
                }
            } else {
                cdbx_linesHighlightHtml = selectedLines;
            }
            
            cdbx_appendHighlightedLinesHtml();
            cdbx_editor_html.clearSelection();
        });
        
        $(CDBX_SELECT_LINES_CSS).live(CDBX_EVENT_CLICK, function (e) {
            var selectedLines = $(CDBX_LINES_HIGHLIGHT_NOW_CSS).text();
            if (cdbx_linesHighlightCss) {
                if (!cdbx_detectDuplicateOverlapHighlightWeb(selectedLines, cdbx_linesHighlightCss)) {
                    cdbx_linesHighlightCss += ',' + selectedLines;
                }
            } else {
                cdbx_linesHighlightCss = selectedLines;
            }
            
            cdbx_appendHighlightedLinesCss();
            cdbx_editor_css.clearSelection();
        });
        
        $(CDBX_SELECT_LINES_JS).live(CDBX_EVENT_CLICK, function (e) {
            var selectedLines = $(CDBX_LINES_HIGHLIGHT_NOW_JS).text();
            if (cdbx_linesHighlightJs) {
                if (!cdbx_detectDuplicateOverlapHighlightWeb(selectedLines, cdbx_linesHighlightJs)) {
                    cdbx_linesHighlightJs += ',' + selectedLines;
                }
            } else {
                cdbx_linesHighlightJs = selectedLines;
            }
            
            cdbx_appendHighlightedLinesJs();
            cdbx_editor_js.clearSelection();
        });
        
        $(CDBX_REMOVE_HIGHLIGHT_LINES_HTML).live(CDBX_EVENT_CLICK, function (e) {
            var idx = parseInt($(this).attr('id').split('@')[1]);
            var linesGroup = cdbx_linesHighlightHtml.split(',');
            linesGroup.splice(idx, 1);
            var linestr = '';
            for (var i = 0; i < linesGroup.length; i++) {
                linestr += linesGroup[i];
                if (i != linesGroup.length - 1) {
                    linestr += ',';
                }
            }
            cdbx_linesHighlightHtml = linestr;
            cdbx_appendHighlightedLinesHtml();
        });
        
        $(CDBX_REMOVE_HIGHLIGHT_LINES_CSS).live(CDBX_EVENT_CLICK, function (e) {
            var idx = parseInt($(this).attr('id').split('@')[1]);
            var linesGroup = cdbx_linesHighlightCss.split(',');
            linesGroup.splice(idx, 1);
            var linestr = '';
            for (var i = 0; i < linesGroup.length; i++) {
                linestr += linesGroup[i];
                if (i != linesGroup.length - 1) {
                    linestr += ',';
                }
            }
            cdbx_linesHighlightCss = linestr;
            cdbx_appendHighlightedLinesCss();
        });
        
        $(CDBX_REMOVE_HIGHLIGHT_LINES_JS).live(CDBX_EVENT_CLICK, function (e) {
            var idx = parseInt($(this).attr('id').split('@')[1]);
            var linesGroup = cdbx_linesHighlightJs.split(',');
            linesGroup.splice(idx, 1);
            var linestr = '';
            for (var i = 0; i < linesGroup.length; i++) {
                linestr += linesGroup[i];
                if (i != linesGroup.length - 1) {
                    linestr += ',';
                }
            }
            cdbx_linesHighlightJs = linestr;
            cdbx_appendHighlightedLinesJs();
        });
        
        var cdbx_appendHighlightedLinesHtml = function () {
            $(CDBX_LINES_HIGHLIGHTED_HIDDEN_HTML).html(cdbx_linesHighlightHtml);
            if (!cdbx_linesHighlightHtml  || cdbx_linesHighlightHtml.length == 0) {
                $(CDBX_LINES_HIGHLIGHTED_HTML).html(cdbx_linesHighlightHtml);
                return;
            }
            var linesGroup = cdbx_linesHighlightHtml.split(',');
            var currentHighlights = '';
            for (var i = 0; i < linesGroup.length; i++) {
                currentHighlights +=
                    '<span> \
                        <a id="cdbx-remove-highlight-html@' + i + '" class="cdbx-remove-highlight-lines-html" style="cursor:pointer;" title="Remove highlight"> \
                            <span class="dashicons dashicons-no"></span> ' + '<span style="margin-top:0.5em">' + linesGroup[i] + '</span>' + 
                        '</button> \
                    </span>';
                currentHighlights += '&nbsp;&nbsp;&nbsp;';
            }
            $(CDBX_LINES_HIGHLIGHTED_HTML).html(currentHighlights);
        };
        
        var cdbx_appendHighlightedLinesCss = function () {
            $(CDBX_LINES_HIGHLIGHTED_HIDDEN_CSS).html(cdbx_linesHighlightCss);
            if (!cdbx_linesHighlightCss || cdbx_linesHighlightCss.length == 0) {
                $(CDBX_LINES_HIGHLIGHTED_CSS).html(cdbx_linesHighlightCss);
                return;
            }
            var linesGroup = cdbx_linesHighlightCss.split(',');
            var currentHighlights = '';
            for (var i = 0; i < linesGroup.length; i++) {
                currentHighlights +=
                    '<span> \
                        <a id="cdbx-remove-highlight-css@' + i + '" class="cdbx-remove-highlight-lines-css" style="cursor:pointer;" title="Remove highlight"> \
                            <span class="dashicons dashicons-no"></span> ' + '<span style="margin-top:0.5em">' + linesGroup[i] + '</span>' + 
                        '</button> \
                    </span>';
                currentHighlights += '&nbsp;&nbsp;&nbsp;';
            }
            $(CDBX_LINES_HIGHLIGHTED_CSS).html(currentHighlights);
        };
        
        var cdbx_appendHighlightedLinesJs = function () {
            $(CDBX_LINES_HIGHLIGHTED_HIDDEN_JS).html(cdbx_linesHighlightJs);
            if (!cdbx_linesHighlightJs || cdbx_linesHighlightJs.length == 0) {
                $(CDBX_LINES_HIGHLIGHTED_JS).html(cdbx_linesHighlightJs);
                return;
            }
            var linesGroup = cdbx_linesHighlightJs.split(',');
            var currentHighlights = '';
            for (var i = 0; i < linesGroup.length; i++) {
                currentHighlights +=
                    '<span> \
                        <a id="cdbx-remove-highlight-js@' + i + '" class="cdbx-remove-highlight-lines-js" style="cursor:pointer;" title="Remove highlight"> \
                            <span class="dashicons dashicons-no"></span> ' + '<span style="margin-top:0.5em">' + linesGroup[i] + '</span>' + 
                        '</button> \
                    </span>';
                currentHighlights += '&nbsp;&nbsp;&nbsp;';
            }
            $(CDBX_LINES_HIGHLIGHTED_JS).html(currentHighlights);
        };
        
        var cdbx_detectDuplicateOverlapHighlightWeb = function (selectedLines, highlightLines) {
            var linesGroup = highlightLines.split(',');
            for (var i = 0; i < linesGroup.length; i++) {
                if (selectedLines == linesGroup[i]) {
                    alert('Duplicate highlight range !!!');
                    return true;
                }
            }
            return false;
        };
        
        $(document).live(CDBX_EVENT_EDITOR_INIT, function( event, editor ) {
            setTimeout(function () {
              var doubleClickData = {
                 action: 'get_tmce_click_setting',
                 caller: 'admin'
              };
              $.ajax({
                 url: cdbx_ajax_script.ajaxurl,
                 type : 'POST',
                 async : 'false',
                 data : doubleClickData,
                 success: function(data, textStatus, jqXHR) {
                    var setObj = $.parseJSON(data); 
                    if (setObj.doubleClickStatus.length > 0) {
                        cdbx_tmce_double_click_status = parseInt(setObj.doubleClickStatus);
                        if (cdbx_tmce_double_click_status == 1) {
                            CDBX_EVENT_TMCE_CLICK = 'dblclick';
                        }
                    }
                    initActiveEditorEventHandler(); 
                 }
              });
                
              var initActiveEditorEventHandler = function() {
                  tinymce.activeEditor.on(CDBX_EVENT_TMCE_CLICK, function(ed, e) {
                     cdbx_editorNode = tinymce.activeEditor.selection.getNode();
                     if (cdbx_editorNode.className == CDBX_PRETTYPRINT_CLASS) {
                        var elemContent = cdbx_editorNode.innerHTML;
                        if (document.getElementById('cdbx-hidden-content') == null) {
                          $("<div/>").attr('id', 'cdbx-hidden-content').appendTo('body');
                          $(CDBX_HIDDEN_CONTENT).css('display', 'none');
                        }
                        $(CDBX_HIDDEN_CONTENT).html(elemContent);
                        var code = $(CDBX_HIDDEN_CONTENT).text();
                        var run_btn_id = cdbx_reverseId(cdbx_editorNode.id);
                        var run_btn_elem = document.getElementById(run_btn_id);
                        cdbx_curLangId = run_btn_elem.dataset.lang;
                        cdbx_progName = run_btn_elem.dataset.filename;
                        cdbx_linesHighlight = null; 
                        if (run_btn_elem.dataset.highlight && run_btn_elem.dataset.highlight.length > 0) {
                           cdbx_linesHighlight = run_btn_elem.dataset.highlight;    
                        }

                        var postLoadSetup = function () {
                            cdbx_editor = ace.edit(CDBX_ELEM_COMPILEBIN_EDITOR);
                            cdbx_cleanUpEditorDiv();
                            cdbx_editor.setValue(code);
                            cdbx_setMode();
                            cdbx_editor.clearSelection();
                            $(CDBX_DELETE_CODE).prop("disabled", false);
                            activateTabs();
                        };

                        var data = getEditorModalData();
                        if (document.getElementById('cdbx-editor-dialog') == null) {
                            $("<div/>").attr('id', 'cdbx-editor-dialog').appendTo('body');
                            $(CDBX_EDITOR_DIALOG).css('display', 'none');
                        }
                        $(CDBX_EDITOR_DIALOG).html(data);

                        if (!pref_loaded) {
                            cdbx_showDummyDialog();
                            // Get current editor and language settings
                            var prefData = {
                                action: 'get_global_setting',
                                caller: 'admin'
                            };
                            $.ajax({
                                url: cdbx_ajax_script.ajaxurl,
                                type : 'POST',
                                async : 'false',
                                data : prefData,
                                success: function(data, textStatus, jqXHR) {
                                    var setObj = $.parseJSON(data);
                                    if (setObj.runBtnStatus.length > 0) {
                                        cdbx_run_btn_status = parseInt(setObj.runBtnStatus); 
                                    }
                                    if (setObj.linenumStatus.length > 0) {
                                        cdbx_linenum_status = parseInt(setObj.linenumStatus); 
                                    }
                                    if (setObj.copyBtnStatus.length > 0) {
                                        cdbx_copy_btn_status = parseInt(setObj.copyBtnStatus); 
                                    }
                                    if (setObj.fullscreenStatus.length > 0) {
                                        cdbx_fullscreen_status = parseInt(setObj.fullscreenStatus); 
                                    }
                                    if (setObj.darkThemeStatus.length > 0) {
                                        cdbx_darktheme_status = parseInt(setObj.darkThemeStatus); 
                                    }
                                    if (setObj.doubleClickStatus.length > 0) {
                                        cdbx_tmce_double_click_status = parseInt(setObj.doubleClickStatus);
                                        /*if (cdbx_tmce_double_click_status == 1) {
                                            CDBX_EVENT_TMCE_CLICK = 'dblclick';
                                        }*/
                                    }
                                    if (setObj.editorPref.length > 0) {
                                        /*if (setObj.editorPref == CDBX_EDITOR_WEBDESIGN) {
                                            $("[data-tab=cdbx-tab-2]").click(); 
                                        }*/
                                        cdbx_curEditorId = cdbx_curEditorIdPref = parseInt(setObj.editorPref);
                                    }

                                    if (setObj.langPref.length > 0) {  
                                        //cdbx_curLangId = parseInt(setObj.langPref);
                                        cdbx_curLangIdPref = parseInt(setObj.langPref);
                                    }
                                    if (setObj.themePref.length > 0) {
                                        cdbx_curThemeId = cdbx_curThemePrefId = parseInt(setObj.themePref);   
                                        switch (parseInt(setObj.themePref)) {
                                            case CDBX_THEME_XCODE : cdbx_curTheme = cdbx_curThemePref = CDBX_ACE_THEME_XCODE; break;
                                            case CDBX_THEME_MONOKAI : cdbx_curTheme = cdbx_curThemePref = CDBX_ACE_THEME_MONOKAI; break;
                                            case CDBX_THEME_COBALT : cdbx_curTheme = cdbx_curThemePref = CDBX_ACE_THEME_COBALT;
                                            default : break;
                                        }
                                    }
                                    initEditorDialog();
                                    postLoadSetup();
                                    $(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_OPEN);
                                    pref_loaded = true;
                                    cdbx_closeDummyDialog();
                                }
                            });
                        } else {
                            initEditorDialog();
                            postLoadSetup();
                            $(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_OPEN);
                        }

                        /**************************** Deprecated Code **************************/ 
                        /*initEditorDialog();
                        cdbx_editor = ace.edit(CDBX_ELEM_COMPILEBIN_EDITOR);
                        cdbx_cleanUpEditorDiv();
                        cdbx_editor.setValue(code);
                        cdbx_setMode();
                        cdbx_editor.clearSelection();
                        $(CDBX_DELETE_CODE).prop("disabled", false);
                        activateTabs();  
                        $(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_OPEN); */
                        /***********************************************************************/ 

                        /**************************** Deprecated Code **************************/ 
                        /*var data = {
                          action: 'editor_modal',
                          caller: 'admin'    
                        };
                        $.ajax({
                          url: cdbx_ajax_script.ajaxurl,
                          type : 'POST',
                          async : 'false',
                          data : data,
                          success: function(data, textStatus, jqXHR) {
                            if (document.getElementById('cdbx-editor-dialog') == null) {
                              $("<div/>").attr('id', 'cdbx-editor-dialog').appendTo('body');
                              $(CDBX_EDITOR_DIALOG).css('display', 'none');
                            }
                            $(CDBX_EDITOR_DIALOG).html(data);
                            initEditorDialog();
                            cdbx_editor = ace.edit(CDBX_ELEM_COMPILEBIN_EDITOR);
                            cdbx_cleanUpEditorDiv();
                            cdbx_editor.setValue(code);
                            cdbx_setMode();
                            cdbx_editor.clearSelection();
                            $(CDBX_DELETE_CODE).prop("disabled", false);
                            activateTabs();  
                            $(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_OPEN);
                          }
                        }); */
                        /**************************************************************************/ 
                     } else if (cdbx_editorNode.className == CDBX_WEBDESIGN_CLASS) {
                        var editorNodeId = cdbx_editorNode.id;
                        var editorNodeIdCommon = null; 
                        var editorNodeIdHtml = null;
                        var editorNodeIdCss = null;
                        var editorNodeIdJs = null;

                        if (editorNodeId.substring(editorNodeId.length - 4, editorNodeId.length) == 'html') {
                          editorNodeIdCommon = editorNodeId.substring(0, editorNodeId.length - 4);       
                        } else if (editorNodeId.substring(editorNodeId.length - 3, editorNodeId.length) == 'css') {
                          editorNodeIdCommon = editorNodeId.substring(0, editorNodeId.length - 3);;
                        } else if (editorNodeId.substring(editorNodeId.length - 2, editorNodeId.length) == 'js') {
                          editorNodeIdCommon = editorNodeId.substring(0, editorNodeId.length - 2);
                        } else {
                          return;
                        }

                        editorNodeIdHtml = editorNodeIdCommon + 'html';
                        editorNodeIdCss = editorNodeIdCommon + 'css';
                        editorNodeIdJs = editorNodeIdCommon + 'js';

                        cdbx_editorNode_web = tinymce.activeEditor.dom.get(editorNodeIdCommon); 
                        cdbx_editorNode_html = tinymce.activeEditor.dom.get(editorNodeIdHtml);
                        cdbx_editorNode_css = tinymce.activeEditor.dom.get(editorNodeIdCss);
                        cdbx_editorNode_js = tinymce.activeEditor.dom.get(editorNodeIdJs);  

                        var elemContentHtml = cdbx_editorNode_html ? cdbx_editorNode_html.innerHTML : '';
                        var elemContentCss = cdbx_editorNode_css ? cdbx_editorNode_css.innerHTML : '';
                        var elemContentJs = cdbx_editorNode_js ? cdbx_editorNode_js.innerHTML : '';

                        if (document.getElementById('cdbx-hidden-content-html') == null) {
                          $("<div/>").attr('id', 'cdbx-hidden-content-html').appendTo('body');
                          $(CDBX_HIDDEN_CONTENT_HTML).css('display', 'none');
                        }
                        $(CDBX_HIDDEN_CONTENT_HTML).html(elemContentHtml);

                        if (document.getElementById('cdbx-hidden-content-css') == null) {
                          $("<div/>").attr('id', 'cdbx-hidden-content-css').appendTo('body');
                          $(CDBX_HIDDEN_CONTENT_CSS).css('display', 'none');
                        }
                        $(CDBX_HIDDEN_CONTENT_CSS).html(elemContentCss);

                        if (document.getElementById('cdbx-hidden-content-js') == null) {
                          $("<div/>").attr('id', 'cdbx-hidden-content-js').appendTo('body');
                          $(CDBX_HIDDEN_CONTENT_JS).css('display', 'none');
                        }
                        $(CDBX_HIDDEN_CONTENT_JS).html(elemContentJs);

                        var htmlCode = $(CDBX_HIDDEN_CONTENT_HTML).text();
                        var cssCode = $(CDBX_HIDDEN_CONTENT_CSS).text();
                        var jsCode = $(CDBX_HIDDEN_CONTENT_JS).text();

                        cdbx_linesHighlightHtml = null; 
                        if (cdbx_editorNode_html && cdbx_editorNode_html.dataset.highlight && cdbx_editorNode_html.dataset.highlight.length > 0) {
                            cdbx_linesHighlightHtml = cdbx_editorNode_html.dataset.highlight;    
                        }    

                        cdbx_linesHighlightCss = null; 
                        if (cdbx_editorNode_css && cdbx_editorNode_css.dataset.highlight && cdbx_editorNode_css.dataset.highlight.length > 0) {
                            cdbx_linesHighlightCss = cdbx_editorNode_css.dataset.highlight;    
                        }  

                        cdbx_linesHighlightJs = null; 
                        if (cdbx_editorNode_js && cdbx_editorNode_js.dataset.highlight && cdbx_editorNode_js.dataset.highlight.length > 0) {
                            cdbx_linesHighlightJs = cdbx_editorNode_js.dataset.highlight;    
                        }

                        var postLoadSetupWeb = function () {
                            cdbx_editor_html = ace.edit(CDBX_ELEM_COMPILEBIN_EDITOR_HTML);
                            cdbx_editor_html.setValue(htmlCode);
                            cdbx_editor_html.clearSelection();

                            cdbx_editor_css = ace.edit(CDBX_ELEM_COMPILEBIN_EDITOR_CSS);
                            cdbx_editor_css.setValue(cssCode);
                            cdbx_editor_css.clearSelection();

                            cdbx_editor_js = ace.edit(CDBX_ELEM_COMPILEBIN_EDITOR_JS);
                            cdbx_editor_js.setValue(jsCode);
                            cdbx_editor_js.clearSelection();

                            cdbx_setModeWeb();

                            $(CDBX_DELETE_CODE_WEB).prop("disabled", false);
                            activateTabs();
                            $("[data-tab=cdbx-tab-2]").click();

                            if (cdbx_editorNode.dataset.lang) {
                                switch (cdbx_editorNode.dataset.lang) {
                                    case 'html' : $("[data-tab=cdbx-tab-html]").click(); break;
                                    case 'css'  : $("[data-tab=cdbx-tab-css]").click();  break;
                                    case 'js'   : $("[data-tab=cdbx-tab-js]").click();   break;    
                                }   
                            }
                        }; 

                        var data = getEditorModalData();
                        if (document.getElementById('cdbx-editor-dialog') == null) {
                            $("<div/>").attr('id', 'cdbx-editor-dialog').appendTo('body');
                            $(CDBX_EDITOR_DIALOG).css('display', 'none');
                        }
                        $(CDBX_EDITOR_DIALOG).html(data);

                        if (!pref_loaded) {
                            cdbx_showDummyDialog();
                            // Get current editor and language settings
                            var prefData = {
                                action: 'get_global_setting',
                                caller: 'admin'
                            };
                            $.ajax({
                                url: cdbx_ajax_script.ajaxurl,
                                type : 'POST',
                                async : 'false',
                                data : prefData,
                                success: function(data, textStatus, jqXHR) {
                                    var setObj = $.parseJSON(data);
                                    if (setObj.runBtnStatus.length > 0) {
                                        cdbx_run_btn_status = parseInt(setObj.runBtnStatus); 
                                    }
                                    if (setObj.linenumStatus.length > 0) {
                                        cdbx_linenum_status = parseInt(setObj.linenumStatus); 
                                    }
                                    if (setObj.copyBtnStatus.length > 0) {
                                        cdbx_copy_btn_status = parseInt(setObj.copyBtnStatus); 
                                    }
                                    if (setObj.fullscreenStatus.length > 0) {
                                        cdbx_fullscreen_status = parseInt(setObj.fullscreenStatus); 
                                    }
                                    if (setObj.darkThemeStatus.length > 0) {
                                        cdbx_darktheme_status = parseInt(setObj.darkThemeStatus); 
                                    }
                                    if (setObj.doubleClickStatus.length > 0) {
                                        cdbx_tmce_double_click_status = parseInt(setObj.doubleClickStatus);
                                        /*if (cdbx_tmce_double_click_status == 1) {
                                            CDBX_EVENT_TMCE_CLICK = 'dblclick';
                                        }*/
                                    }
                                    if (setObj.editorPref.length > 0) {
                                        /*if (setObj.editorPref == CDBX_EDITOR_WEBDESIGN) {
                                            $("[data-tab=cdbx-tab-2]").click(); 
                                        }*/
                                        cdbx_curEditorId = cdbx_curEditorIdPref = parseInt(setObj.editorPref);
                                    }

                                    if (setObj.langPref.length > 0) {  
                                        //cdbx_curLangId = parseInt(setObj.langPref);
                                        cdbx_curLangIdPref = parseInt(setObj.langPref);
                                    }
                                    if (setObj.themePref.length > 0) {
                                        cdbx_curThemeId = cdbx_curThemePrefId = parseInt(setObj.themePref);   
                                        switch (parseInt(setObj.themePref)) {
                                            case CDBX_THEME_XCODE : cdbx_curTheme = cdbx_curThemePref = CDBX_ACE_THEME_XCODE; break;
                                            case CDBX_THEME_MONOKAI : cdbx_curTheme = cdbx_curThemePref = CDBX_ACE_THEME_MONOKAI; break;
                                            case CDBX_THEME_COBALT : cdbx_curTheme = cdbx_curThemePref = CDBX_ACE_THEME_COBALT;
                                            default : break;
                                        }
                                    }
                                    initEditorDialog();
                                    postLoadSetupWeb();
                                    $(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_OPEN);
                                    pref_loaded = true;
                                    cdbx_closeDummyDialog();
                                }
                            });
                        } else {
                            initEditorDialog();
                            postLoadSetupWeb();
                            $(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_OPEN);
                        } 

                        /****************************** Deprecated Code *****************/ 
                        /*initEditorDialog();  
                        postLoadSetupWeb();
                        $(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_OPEN); */ 
                        /****************************************************************/ 

                        /************************************* Deprecated Code *********************/ 
                        /*var data = {
                          action: 'editor_modal',
                          caller: 'admin'    
                        };
                        $.ajax({
                          url: cdbx_ajax_script.ajaxurl,
                          type : 'POST',
                          async : 'false',
                          data : data,
                          success: function(data, textStatus, jqXHR) {
                            if (document.getElementById('cdbx-editor-dialog') == null) {
                              $("<div/>").attr('id', 'cdbx-editor-dialog').appendTo('body');
                              $(CDBX_EDITOR_DIALOG).css('display', 'none');
                            }
                            $(CDBX_EDITOR_DIALOG).html(data);
                            initEditorDialog();

                            cdbx_editor_html = ace.edit(CDBX_ELEM_COMPILEBIN_EDITOR_HTML);
                            cdbx_editor_html.setValue(htmlCode);
                            cdbx_editor_html.clearSelection();

                            cdbx_editor_css = ace.edit(CDBX_ELEM_COMPILEBIN_EDITOR_CSS);
                            cdbx_editor_css.setValue(cssCode);
                            cdbx_editor_css.clearSelection();

                            cdbx_editor_js = ace.edit(CDBX_ELEM_COMPILEBIN_EDITOR_JS);
                            cdbx_editor_js.setValue(jsCode);
                            cdbx_editor_js.clearSelection();

                            cdbx_setModeWeb();

                            $(CDBX_DELETE_CODE_WEB).prop("disabled", false);
                            activateTabs();
                            $("[data-tab=cdbx-tab-2]").click();
                            $(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_OPEN);
                          }
                        }); */
                        /******************************************************************************/ 

                     }
                  });
              }
            }, 1000);
        });

    });
    
    var getEditorModalData = function () {
        var div_content = 
          '<div style="width:100%;margin-top:-10px;"> \
           <ul class="cdbx-tabs" style="float:right"> \
		     <li id="cdbx-tab-standard" class="cdbx-tab-link current" data-tab="cdbx-tab-1">Standard</li> \
		     <li id="cdbx-tab-web-design" class="cdbx-tab-link" data-tab="cdbx-tab-2">Web Design</li> \
		   </ul>\
           </div> \
           <ul class="cdbx-tabs-web"> \
		       <li id="cdbx-tab-web-html" class="cdbx-tab-link current" data-tab="cdbx-tab-html">Html</li> \
		       <li id="cdbx-tab-web-css" class="cdbx-tab-link" data-tab="cdbx-tab-css">CSS</li> \
               <li id="cdbx-tab-web-js" class="cdbx-tab-link" data-tab="cdbx-tab-js">Javascript</li> \
		   </ul> \
           <div class="cdbx-tabs-placeholder"> \
           <br><br> \
           </div> \
           <div id="cdbx-tab-1" class="cdbx-tab-content current"> \
              <div id="cdbx-editor-dialog"> \
              <div class="cdbx-editor-div"> \
                <div class="cdbx-editor-div-left"> \
                  <div id="cdbx-compilebin-editor" class="cdbx-editor"></div> \
                </div> \
                <div class="cdbx-editor-div-right"> \
                  <div> \
                    <button type="button" id="cdbx-save-code" class="button button-primary"> \
                      <span class="" aria-hidden="true" style="margin-top:0.2em"></span> <b>Save</b> \
                    </button> \
                    <button type="button" id="cdbx-ace-theme-xcode" class="button button-default cdbx-ace-theme" title="Light theme"> \
                      <span class="dashicons dashicons-visibility" aria-hidden="true" style="margin-top:0.2em"></span> \
                    </button> \
                    <button type="button" id="cdbx-ace-theme-monokai" class="button button-default cdbx-ace-theme" title="Dark (monokai) theme"> \
                      <span class="dashicons dashicons-art" aria-hidden="true" style="margin-top:0.2em"></span> \
                    </button> \
                    <button type="button" id="cdbx-ace-theme-cobalt" class="button button-default cdbx-ace-theme" title="Dark (cobalt) theme"> \
                      <span class="dashicons dashicons-image-filter" aria-hidden="true" style="margin-top:0.2em"></span> \
                    </button> \
                    <button type="button" id="cdbx-ace-font-zoomin" class="button button-default"> \
                      <span class="dashicons dashicons-plus" aria-hidden="true" style="margin-top:0.2em"></span> \
                    </button> \
                    <button type="button" id="cdbx-ace-font-zoomout" class="button button-default"> \
                      <span class="dashicons dashicons-minus" aria-hidden="true" style="margin-top:0.2em"></span> \
                    </button> \
                    \
                    <button type="button" id="cdbx-delete-code" class="button button-default"> \
                      <span class="dashicons dashicons-trash" aria-hidden="true" style="margin-top:0.2em"></span> \
                    </button> \
                    <button type="button" id="cdbx-run-code" class="button button-primary" style="float:right;width:5em;"> \
                      <span class="" aria-hidden="true"></span> <b>Run</b> \
                    </button> \
                   </div> \
                   <div class="cdbx-div-right-2"> \
                     <select name="cdbx-lang" id="cdbx-lang" style="margin-top:-0.1em"></select> \
                     <input id="cdbx-filename" class="cdbx-textbox" placeholder="Filename" style=""></input><span id="cdbx-filename-ext"></span> \
                     <button type="button" id="cdbx-setting" class="button button-default" style="float:right" title="Enter your API key for code execution"> \
                       <span class="dashicons dashicons-admin-network" aria-hidden="true" style="margin-top:0.2em"></span> \
                     </button> \
                     <button type="button" id="cdbx-global-setting" class="button button-default" style="float:right;margin-right:0.2em;" title="Global settings that apply to all code snippets"> \
                       <span class="dashicons dashicons-admin-generic" aria-hidden="true" style="margin-top:0.2em"></span> \
                     </button> \
                   </div> \
                   <div> \
                     <p><a id="cdbx-code-lines-highlight" style="cursor:pointer" title="Selected lines will be highlighted with different background color in public view"><u>Highlight lines</u></a></p> \
                     <div id="cdbx-code-lines-highlight-area" style="display:none;border:1px solid #ddd;padding:0.5em"> \
                        <div id="cdbx-lines-highlighted-hidden" style="display:none"></div> \
                        <div id="cdbx-lines-highlighted"></div> \
                        <p style="font-size:0.8em;color:#008B8B">Select lines to be highlighted in the editor</p> \
                        <span id="cdbx-lines-highlight-now"></span>&nbsp;&nbsp; \
                        <span> \
                           <button type="button" id="cdbx-select-lines" style="cursor:pointer;display:none;"> \
                              <span class="dashicons dashicons-yes"></span> \
                           </button> \
                        </span> \
                     </div> \
                   </div> \
                   <div id="cdbx-div-output" style="width:98%"> \
                     Output Appears Here ... \
                   </div> \
                   <div style="width:100%"> \
                     <textarea id="cdbx-stdin" class="cdbx-textarea-input" rows="4" cols="200" placeholder="Stdin (One input element per line)"></textarea> \
                     <textarea id="cdbx-cmdline" class="cdbx-textarea-input" rows="1" placeholder="Cmd Line Args"></textarea> \
                   </div> \
                </div> \
              </div> \
            </div> \
           </div> \
           <div id="cdbx-tab-2" class="cdbx-tab-content"> \
             <!--<ul class="cdbx-tabs-web"> \
		       <li class="cdbx-tab-link current" data-tab="cdbx-tab-html">Html</li> \
		       <li class="cdbx-tab-link" data-tab="cdbx-tab-css">CSS</li> \
               <li class="cdbx-tab-link" data-tab="cdbx-tab-js">Javascript</li> \
		     </ul> --> \
             <div class="cdbx-editor-div-left"> \
                 <div id="cdbx-tab-html" class="cdbx-tab-content-web current"> \
                   <div class="cdbx-editor-div"> \
                       <div id="cdbx-compilebin-editor-html" class="cdbx-editor"></div> \
                   </div> \
                 </div> \
                 <div id="cdbx-tab-css" class="cdbx-tab-content-web"> \
                   <div class="cdbx-editor-div"> \
                       <div id="cdbx-compilebin-editor-css" class="cdbx-editor"></div> \
                   </div> \
                 </div> \
                 <div id="cdbx-tab-js" class="cdbx-tab-content-web"> \
                   <div class="cdbx-editor-div"> \
                       <div id="cdbx-compilebin-editor-js" class="cdbx-editor"></div> \
                   </div> \
                 </div> \
              </div> \
              <div class="cdbx-editor-div-right"> \
                   <div> \
                       <button type="button" id="cdbx-save-code-web" class="button button-primary"> \
                          <span class="" aria-hidden="true" style="margin-top:0.2em"></span> <b>Save</b> \
                        </button> \
                        <button type="button" id="cdbx-ace-theme-xcode-web" class="button button-default cdbx-ace-theme-web" title="Light theme"> \
                          <span class="dashicons dashicons-visibility" aria-hidden="true" style="margin-top:0.2em"></span> \
                        </button> \
                        <button type="button" id="cdbx-ace-theme-monokai-web" class="button button-default cdbx-ace-theme-web" title="Dark (monokai) theme"> \
                          <span class="dashicons dashicons-art" aria-hidden="true" style="margin-top:0.2em"></span> \
                        </button> \
                        <button type="button" id="cdbx-ace-theme-cobalt-web" class="button button-default cdbx-ace-theme-web" title="Dark (cobalt) theme"> \
                          <span class="dashicons dashicons-image-filter" aria-hidden="true" style="margin-top:0.2em"></span> \
                        </button> \
                        <button type="button" id="cdbx-ace-font-zoomin-web" class="button button-default"> \
                          <span class="dashicons dashicons-plus" aria-hidden="true" style="margin-top:0.2em"></span> \
                        </button> \
                        <button type="button" id="cdbx-ace-font-zoomout-web" class="button button-default"> \
                          <span class="dashicons dashicons-minus" aria-hidden="true" style="margin-top:0.2em"></span> \
                        </button> \
                        <button type="button" id="cdbx-delete-code-web" class="button button-default"> \
                          <span class="dashicons dashicons-trash" aria-hidden="true" style="margin-top:0.2em"></span> \
                        </button> \
                        <button type="button" id="cdbx-run-code-web" class="button button-primary" style="float:right;width:5em;"> \
                          <span class="" aria-hidden="true"></span> <b>Run</b> \
                        </button> \
                    </div> \
                    <div class="cdbx-div-right-2"> \
                     <a id="cdbx-output-web-link" class="button button-default disabled" style="width:5em;text-align:center;" target="_blank" href="" title="a unique link gets generated everytime code is executed">Link</a> \
                     <button type="button" id="cdbx-setting" class="button button-default" style="float:right" title="Enter your API key for code execution"> \
                       <span class="dashicons dashicons-admin-network" aria-hidden="true" style="margin-top:0.2em"> \</span> \
                     </button> \
                     <button type="button" id="cdbx-global-setting" class="button button-default" style="float:right;margin-right:0.2em;" title="Global settings that apply to all code snippets"> \
                       <span class="dashicons dashicons-admin-generic" aria-hidden="true" style="margin-top:0.2em"> \</span> \
                     </button> \
                    </div> \
                    <div> \
                     <p><a id="cdbx-code-lines-highlight-web" style="cursor:pointer" title="Selected lines will be highlighted with different background color in public view"><u>Highlight lines</u></a></p> \
                     <div id="cdbx-code-lines-highlight-area-html" style="display:none;border:1px solid #ddd;padding:0.5em"> \
                        <div id="cdbx-lines-highlighted-hidden-html" style="display:none"></div> \
                        <div id="cdbx-lines-highlighted-html"></div> \
                        <p style="font-size:0.8em;color:#008B8B">Select lines to be highlighted in the editor</p> \
                        <span id="cdbx-lines-highlight-now-html"></span>&nbsp;&nbsp; \
                        <span> \
                           <button type="button" id="cdbx-select-lines-html" style="cursor:pointer;display:none;"> \
                              <span class="dashicons dashicons-yes"></span> \
                           </button> \
                        </span> \
                     </div> \
                     <div id="cdbx-code-lines-highlight-area-css" style="display:none;border:1px solid #ddd;padding:0.5em"> \
                        <div id="cdbx-lines-highlighted-hidden-css" style="display:none"></div> \
                        <div id="cdbx-lines-highlighted-css"></div> \
                        <p style="font-size:0.8em;color:#008B8B">Select lines to be highlighted in the editor</p> \
                        <span id="cdbx-lines-highlight-now-css"></span>&nbsp;&nbsp; \
                        <span> \
                           <button type="button" id="cdbx-select-lines-css" style="cursor:pointer;display:none;"> \
                              <span class="dashicons dashicons-yes"></span> \
                           </button> \
                        </span> \
                     </div> \
                     <div id="cdbx-code-lines-highlight-area-js" style="display:none;border:1px solid #ddd;padding:0.5em"> \
                        <div id="cdbx-lines-highlighted-hidden-js" style="display:none"></div> \
                        <div id="cdbx-lines-highlighted-js"></div> \
                        <p style="font-size:0.8em;color:#008B8B">Select lines to be highlighted in the editor</p> \
                        <span id="cdbx-lines-highlight-now-js"></span>&nbsp;&nbsp; \
                        <span> \
                           <button type="button" id="cdbx-select-lines-js" style="cursor:pointer;display:none;"> \
                              <span class="dashicons dashicons-yes"></span> \
                           </button> \
                        </span> \
                     </div> \
                    </div> \
                    <div id="cdbx-div-output-web" style="width:98%"> \
                        Output Appears Here ... \
                    </div> \
                 </div> \
           </div>';
       
        return div_content;
    };
    
});
