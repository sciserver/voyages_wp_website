jQuery(function($) {

    $(document).ready(function () {

        var cdbx_editorNode = null;
        var cdbx_curtooltip = null;
        var cdbx_editor_fullscreen = false;
        var cdbx_themeId = 0;
        var cdbx_show_copy_btn = false;
        var cdbx_show_linenums = false;
        
        var cdbx_reverseId = function(str) {
            return str.split('').reverse().join('');
        };
        
        // Get current editor theme and run button settings
        var cdbx_publicSetting = {
           action: 'get_public_setting' 
        };
        
        var cdbx_isCrayonHighlighterPresent = function(elem) {
           if (elem.className.substr(0, CDBX_CRAYON_DETECT_STRING.length) == CDBX_CRAYON_DETECT_STRING) {
               return true;
           }
           return false;
        };
        
        var cdbx_isWPSyntaxHighlighterPresent = function(elem) {
           if (elem.className.substr(0, CDBX_WP_SYNTAX_HIGHLIGHTER_DETECT_STRING.length) == CDBX_WP_SYNTAX_HIGHLIGHTER_DETECT_STRING) {
               return true;
           }
           return false;
        };
        
        var cdbx_isCompilebinPresent = function (elem) {
           var classTok = elem.className.split(' ');    
           if (classTok[0] == 'prettyprint' || classTok[0] == 'cdbxweb') {
               return true;
           }
           return false;    
        };
        
        var cdbx_lineHighlight = function (cdbx_codeElem) {
            var elem = document.getElementById(cdbx_codeElem.id);
            var className = cdbx_codeElem.getAttribute('class');
            var classTok = className.split(' ');
            if (classTok[0] != 'prettyprint' && classTok[0] != 'cdbxweb') return;
            var highlightedLines = '';
            if (elem && elem.dataset && elem.dataset.highlight) {
                highlightedLines = elem.dataset.highlight;
            }
            if (highlightedLines.length == 0) return;
            var myCodeStr = cdbx_codeElem.innerHTML;
            var codeLineArray = myCodeStr.split('\n');
            var newCodeStr = '';
            var highlightArray = highlightedLines.split(',');
            for (var i = 0; i < highlightArray.length; i++) {
                var lineRange = highlightArray[i].split('-');
                var start = parseInt(lineRange[0]);
                var end = parseInt(lineRange[1]);
                /*for (var j = start - 1; j < end; j++) {
                    if (cdbx_themeId == 0) {    
                       codeLineArray[j] = '<code style="background-color:rgba(240, 240, 240, 1);">' + codeLineArray[j] + '</code>';
                    } else {
                       codeLineArray[j] = '<code style="background-color:#2F4F4F;">' + codeLineArray[j] + '</code>';
                    }
                }*/
                if (cdbx_themeId == 0) {
                   codeLineArray[start-1] = '<code style="background-color:rgba(240, 240, 240, 1);">' + codeLineArray[start-1];
                   codeLineArray[end-1] = codeLineArray[end-1] + '</code>'; 
                } else {
                   codeLineArray[start-1] = '<code style="background-color:#2F4F4F;">' + codeLineArray[start-1];
                   codeLineArray[end-1] = codeLineArray[end-1] + '</code>';   
                }
            }
            for (var i = 0; i < codeLineArray.length; i++) {
                newCodeStr += codeLineArray[i] + '\n';
            }
            cdbx_codeElem.innerHTML = newCodeStr;
        };
        
        var cdbx_preProcess = function() {
            var cdbx_preElems = document.getElementsByTagName("PRE");
            for (var i = 0; i < cdbx_preElems.length; i++) {
                //cdbx_lineHighlight(cdbx_preElems[i]);
                //if (cdbx_isCrayonHighlighterPresent(cdbx_preElems[i]) || cdbx_isWPSyntaxHighlighterPresent(cdbx_preElems[i])) {
                if (!cdbx_isCompilebinPresent(cdbx_preElems[i])) {
                    //cdbx_preElems[i].classList.add('prettyprint');
                    cdbx_preElems[i].className = 'prettyprint';
                }
            }
        };

        cdbx_preProcess();
        
        var cdbx_showLineNums = function (cdbx_preElem) {
            var preContent = cdbx_preElem.innerHTML;
            var codeLine = new Array();
            var newContent = '';
            codeLine = preContent.split('\n');
            for (var j = 0; j < codeLine.length; j++) {
                newContent = newContent + '<cdbx-code>' + codeLine[j] + '</>';
                if (j != codeLine.length) {
                    newContent += '\n';
                }
            }
            cdbx_preElem.innerHTML = newContent;    
        };
        
        var cdbx_showCopyButton = function (cdbx_preElem) {
            var preContent = cdbx_preElem.innerHTML;
            if (cdbx_preElem.id.length > 0) {
                var copyButton = '<span class="cdbx-tooltip" style="float:right;"><input id="copy' + cdbx_preElem.id + '" class="cdbx-tooltip cdbx-btn-copy" style="background-color: #ffffff; margin-bottom: 0; color: #008b8b; border: 1px solid rgba(231, 231, 230, 1); border-radius: 10px; font-size: 13px; height: 30px; min-width: 60px; max-width: 150px; padding: 4px; font-weight: normal; outline: none;float:right;margin-right:3px;" type="button" value="Copy" />' + 
                '<input type="text" class="cdbx-tooltiptext" id="cdbx-copytooltip-' + cdbx_preElem.id + '" value="Copy to clipboard" style="color:#000080;border:1px solid #ddd" /></span>';
                cdbx_preElem.innerHTML = preContent.trim() + copyButton;
            }
                
        };
        
        var modifyCodeSnippets = function () {
            var cdbx_preElems = document.getElementsByTagName("PRE");
            for (var i = 0; i < cdbx_preElems.length; i++) {
                if (cdbx_themeId == 0) {
                    cdbx_preElems[i].setAttribute("style", "padding: 10px; border: 1px solid rgba(231, 231, 230, 1); border-radius: 10px; background-color: #fff; font-size: 13px;");   
                } else {
                    cdbx_preElems[i].setAttribute("style", "padding: 10px; border: 1px solid rgba(231, 231, 230, 1); border-radius: 10px; background-color: #333; font-size: 13px;");
                }
                if (cdbx_show_copy_btn) {
                    cdbx_showCopyButton(cdbx_preElems[i]);
                }
                if (cdbx_show_linenums) {
                    cdbx_showLineNums(cdbx_preElems[i]);
                }
                cdbx_lineHighlight(cdbx_preElems[i]);
            }
        };
        
        window.exports = { 
           cdbx_publicInit: function () {
               $.ajax({
                url: cdbx_ajax_script.ajaxurl,
                type : 'POST',
                async : 'false',
                data : cdbx_publicSetting,
                success: function(data, textStatus, jqXHR) {
                   var setObj = $.parseJSON(data);    
                   if (setObj.darkthemeStatus.length == 0) {
                      // darktheme status not found, display default theme   
                   } else {
                      if (parseInt(setObj.darkthemeStatus) == 1) {
                         cdbx_themeId = 1;
                      } else {
                      }
                   }    
                   if (setObj.runBtnStatus.length == 0) {
                      // run_btn_status not found
                      $(CDBX_BTN_MAIN).css('display', 'block');
                   } else {
                      if (parseInt(setObj.runBtnStatus) == 1) {
                          $(CDBX_BTN_MAIN).css('display', 'block'); 
                      }
                   }
                   if (setObj.copyBtnStatus.length == 0) {
                      // copy_btn_status not found
                      cdbx_show_copy_btn = true;   
                   } else {
                      if (parseInt(setObj.copyBtnStatus) == 1) {
                         cdbx_show_copy_btn = true;  
                      }
                   }
                   if (setObj.fullscreenStatus.length == 0) {
                      // fullscreen status not found
                      cdbx_editor_fullscreen = true;
                   } else {
                      if (parseInt(setObj.fullscreenStatus) == 1) {
                         cdbx_editor_fullscreen = true;
                      }
                   }        
                   if (setObj.themePref.length > 0) {
                      switch (parseInt(setObj.themePref)) {
                         case CDBX_THEME_XCODE : cdbx_curTheme = cdbx_curThemePref = CDBX_ACE_THEME_XCODE; break;
                         case CDBX_THEME_MONOKAI : cdbx_curTheme = cdbx_curThemePref = CDBX_ACE_THEME_MONOKAI; break;
                         case CDBX_THEME_COBALT : cdbx_curTheme = cdbx_curThemePref = CDBX_ACE_THEME_COBALT;
                         default : break;
                      } 
                   }
                   if (setObj.linenumStatus.length == 0) {
                      // linenum status not found, display line numbers by default
                      cdbx_show_linenums = true;   
                   } else {
                      if (parseInt(setObj.linenumStatus) == 1) {
                         cdbx_show_linenums = true;  
                      } 
                   }    
                   modifyCodeSnippets();       
                }              
              });
           }
        };
        
        var cdbx_setTheme = function() {
           cdbx_editor.setTheme(cdbx_curTheme);
        };
        
        var cdbx_setThemeWeb = function() {
           cdbx_editor_html.setTheme(cdbx_curTheme);
           cdbx_editor_css.setTheme(cdbx_curTheme);
           cdbx_editor_js.setTheme(cdbx_curTheme);
        };
        
        var cdbx_reverseId = function(str) {
           return str.split('').reverse().join('');
        };

        var cdbx_setMode = function() {
           cdbx_editor.getSession().setMode(cdbx_languages[cdbx_curLangId].mode);
           $(CDBX_FILENAME_EXT).text(cdbx_languages[cdbx_curLangId].ext);
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
           $('ul.cdbx-tabs-web li').click(function() {
               var tab_id = $(this).attr('data-tab');

		       $('ul.cdbx-tabs-web li').removeClass('current');
		       $('.cdbx-tab-content-web').removeClass('current');

		       $(this).addClass('current');
		       $("#" + tab_id).addClass('current');
	       });                         
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

        var initEditorDialog = function() {
            $(CDBX_EDITOR_DIALOG).dialog({
                title: 'Code Editor and Compiler',
                /*dialogClass: 'wp-dialog', */
                autoOpen: false,
                draggable: false,
                width: CDBX_EDITOR_DIALOG_WIDTH,
                modal: true,
                resizable: false,
                closeOnEscape: true,
                position: {
                  my: 'center',
                  at: 'center',
                  of: window
                },
                open: function () {
                  $(CDBX_FILENAME).val(cdbx_progName);
                  if (!cdbx_editor_fullscreen) {
                    $(CDBX_FULLSCREEN).css('display', 'none');
                  }    
                  $('.ui-widget-overlay').bind(CDBX_EVENT_CLICK, function() {
                    $(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_CLOSE);
                  })
                },
                create: function () {
                  $('.ui-dialog-titlebar-close').addClass('ui-button');
                }
            });
        };

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

        $(CDBX_TRY_CODE).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            if (document.getElementById('cdbx-hidden-content') == null) {
              $("<div/>").attr('id', 'cdbx-hidden-content').appendTo('body');
              $(CDBX_HIDDEN_CONTENT).css('display', 'none');
            }
            var elemId = this.id;
            var elem = document.getElementById(elemId);
            var codeElem = elem.dataset.code;
            var code = document.getElementById(codeElem).innerHTML;
            $(CDBX_HIDDEN_CONTENT).html(code);
            code = $(CDBX_HIDDEN_CONTENT).text();
            cdbx_curLangId = elem.dataset.lang;
            cdbx_progName = elem.dataset.filename;
          
            var data = getCodeEditorData();
            if (document.getElementById('cdbx-editor-dialog') == null) {
                $("<div/>").attr('id', 'cdbx-editor-dialog').appendTo('body');
                $(CDBX_EDITOR_DIALOG).css('display', 'none');
            }
            $(CDBX_EDITOR_DIALOG).html(data);
            initEditorDialog();
            cdbx_editor = ace.edit(CDBX_ELEM_COMPILEBIN_EDITOR);
            cdbx_setMode();
            cdbx_setTheme();
            cdbx_editor.setValue(code);
            cdbx_editor.clearSelection();
            cdbx_cleanUpEditorDiv();
            $(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_OPEN);
            
            /************************ Deprecated Code ***********************************/
            /*var data = {
			   action: 'editor_modal',
               caller: 'front_end'    
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
                 cdbx_setMode();
                 cdbx_setTheme();
                 cdbx_editor.setValue(code);
                 cdbx_editor.clearSelection();
                 cdbx_cleanUpEditorDiv();
                 $(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_OPEN);
               }        
           }); */
           /***************************************************************************/    
            
        });
        
        $(CDBX_TRY_CODE_WEB).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
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
            
            var elemId = this.id;
            var htmlCode = '';
            var cssCode = '';
            var jsCode = '';
            var htmlElemDiv = document.getElementById(cdbx_reverseId(elemId) + 'html');
            var cssElemDiv = document.getElementById(cdbx_reverseId(elemId) + 'css');
            var jsElemDiv = document.getElementById(cdbx_reverseId(elemId) + 'js');
            if (htmlElemDiv) htmlCode = htmlElemDiv.innerHTML;
            if (cssElemDiv) cssCode = cssElemDiv.innerHTML;
            if (jsElemDiv) jsCode = jsElemDiv.innerHTML;

            $(CDBX_HIDDEN_CONTENT_HTML).html(htmlCode);
            $(CDBX_HIDDEN_CONTENT_CSS).html(cssCode);
            $(CDBX_HIDDEN_CONTENT_JS).html(jsCode);
            
            htmlCode = $(CDBX_HIDDEN_CONTENT_HTML).text();
            cssCode = $(CDBX_HIDDEN_CONTENT_CSS).text();
            jsCode = $(CDBX_HIDDEN_CONTENT_JS).text();
            
            var data = getWebCodeEditorData();
            if (document.getElementById('cdbx-editor-dialog') == null) {
                $("<div/>").attr('id', 'cdbx-editor-dialog').appendTo('body');
                $(CDBX_EDITOR_DIALOG).css('display', 'none');
            }

            $(CDBX_EDITOR_DIALOG).html(data);
            initEditorDialog();
            cdbx_editor_html = ace.edit(CDBX_ELEM_COMPILEBIN_EDITOR_HTML);
            cdbx_editor_css = ace.edit(CDBX_ELEM_COMPILEBIN_EDITOR_CSS);
            cdbx_editor_js = ace.edit(CDBX_ELEM_COMPILEBIN_EDITOR_JS);   
                 
            cdbx_setThemeWeb();   
                   
            cdbx_editor_html.setValue(htmlCode);
            cdbx_editor_css.setValue(cssCode);
            cdbx_editor_js.setValue(jsCode);   
                   
            cdbx_editor_html.clearSelection();
            cdbx_editor_css.clearSelection();
            cdbx_editor_js.clearSelection();   

            cdbx_setModeWeb();
            activateTabs();
            
            if (this.dataset.lang) {
                switch (this.dataset.lang) {
                    case 'html' : $("[data-tab=cdbx-tab-html]").click(); break;
                    case 'css'  : $("[data-tab=cdbx-tab-css]").click();  break;
                    case 'js'   : $("[data-tab=cdbx-tab-js]").click();   break;    
                }   
            }
            
            $(CDBX_TABS_WEB).css('display', 'block');   
            $(CDBX_OUTPUT_WEB_LINK).addClass('disabled').removeAttr("href");   
            $(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_OPEN);

          
            /************************************* Deprecated Code ***************************/
            /*var data = {
			   action: 'editor_modal_web',
               caller: 'front_end'    
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
                 cdbx_editor_css = ace.edit(CDBX_ELEM_COMPILEBIN_EDITOR_CSS);
                 cdbx_editor_js = ace.edit(CDBX_ELEM_COMPILEBIN_EDITOR_JS);   
                   
                 //cdbx_editor_html.setTheme(CDBX_ACE_THEME_XCODE);
                 //cdbx_editor_css.setTheme(CDBX_ACE_THEME_XCODE);
                 //cdbx_editor_js.setTheme(CDBX_ACE_THEME_XCODE);
                 cdbx_setThemeWeb();   
                   
                 cdbx_editor_html.setValue(htmlCode);
                 cdbx_editor_css.setValue(cssCode);
                 cdbx_editor_js.setValue(jsCode);   
                   
                 cdbx_editor_html.clearSelection();
                 cdbx_editor_css.clearSelection();
                 cdbx_editor_js.clearSelection();   

                 cdbx_setModeWeb();
                 activateTabs();
                 $(CDBX_TABS_WEB).css('display', 'block');   
                 $(CDBX_OUTPUT_WEB_LINK).addClass('disabled').removeAttr("href");   
                 $(CDBX_EDITOR_DIALOG).dialog(CDBX_EVENT_OPEN);
               }        
           }); */
           /*****************************************************************************************/    
        });
        
        $(CDBX_BTN_COPY).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            if (document.getElementById('cdbx-hidden-content') == null) {
              $('<div/>').attr('id', 'cdbx-hidden-content').appendTo('body');
              $(CDBX_HIDDEN_CONTENT).css('display', 'none');
            }
            var elemId = this.id.substring(4);
            var elem = document.getElementById(elemId);
            var code = elem.innerHTML;
            $(CDBX_HIDDEN_CONTENT).html(code);
            code = $(CDBX_HIDDEN_CONTENT).text();
            
            if (document.getElementById('cdbx-hidden-textarea') == null) {
              $('<textarea>').attr('id', 'cdbx-hidden-textarea').appendTo('body');
            } else {
              $('#cdbx-hidden-textarea').css('display', 'block');
            }
            
            $('#cdbx-hidden-textarea').val(elem.textContent);
            $('#cdbx-hidden-textarea').select();
            document.execCommand('copy');
            $('#cdbx-hidden-textarea').css('display', 'none');
            cdbx_curtooltip = document.getElementById("cdbx-copytooltip-" + elemId);
            cdbx_curtooltip.value = 'Code copied';
        });
        
        $(CDBX_BTN_COPY).live('mouseout', function() {
            if (cdbx_curtooltip) {
               cdbx_curtooltip.value = 'Copy to clipboard';   
            }
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

        $(CDBX_CODE_HELP).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            $(CDBX_CODE_HELP_DIALOG).dialog(CDBX_EVENT_OPEN);
        });
        
        $(CDBX_FULLSCREEN).live(CDBX_EVENT_CLICK, function (e) {
            e.preventDefault();
            cdbx_fullscreen();
        });

        var cdbx_fullscreen = function () {
            var element = document.getElementById(CDBX_ELEM_EDITOR_DIALOG);
            var full_screen_element = document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement || null;
            if (full_screen_element == null) {
               if (element.requestFullscreen) {
                   element.requestFullscreen();
               } else if(element.mozRequestFullScreen) {
                   element.mozRequestFullScreen();
               } else if(element.webkitRequestFullscreen) {
                   element.webkitRequestFullscreen();
               } else if(element.msRequestFullscreen) {
                   element.msRequestFullscreen();
               }
            } else {
               if (document.exitFullscreen)
		          document.exitFullscreen();
	           else if (document.mozCancelFullScreen)
		          document.mozCancelFullScreen();
	           else if (document.webkitExitFullscreen)
		          document.webkitExitFullscreen();
	           else if (document.msExitFullscreen)
		          document.msExitFullscreen(); 
            }
        };
        
        var getCodeEditorData = function() {
          var div_content = 
            '<div id="cdbx-editor-dialog"> \
              <div class="cdbx-editor-div"> \
                <div class="cdbx-editor-div-left"> \
                  <div id="cdbx-compilebin-editor" class="cdbx-editor"></div> \
                </div> \
                <div class="cdbx-editor-div-right" style="background-color:#FFFFFF"> \
                  <div style="width:100%;float:left"> \
                    <button type="" id="cdbx-fullscreen" class="cdbx-btn-1" title="Full screen"> \
                      <span class="dashicons dashicons-editor-expand" aria-hidden="true"></span> \
                    </button> \
                    <button type="" id="cdbx-ace-theme-xcode" class="cdbx-btn-1 cdbx-ace-theme" title="Light theme"> \
                      <span class="dashicons dashicons-visibility" aria-hidden="true"></span> \
                    </button> \
                    <button type="button" id="cdbx-ace-theme-monokai" class="cdbx-btn-1 cdbx-ace-theme" title="Dark (monokai) theme"> \
                      <span class="dashicons dashicons-art" aria-hidden="true"></span> \
                    </button> \
                    <button type="button" id="cdbx-ace-theme-cobalt" class="cdbx-btn-1 cdbx-ace-theme" title="Dark (cobalt) theme"> \
                      <span class="dashicons dashicons-image-filter" aria-hidden="true"></span> \
                    </button> \
                    <button type="button" id="cdbx-ace-font-zoomin" class="cdbx-btn-1"> \
                      <span class="dashicons dashicons-plus" aria-hidden="true"></span> \
                    </button> \
                    <button type="button" id="cdbx-ace-font-zoomout" class="cdbx-btn-1"> \
                      <span class="dashicons dashicons-minus" aria-hidden="true"></span> \
                    </button> \
                    <button type="button" id="cdbx-run-code" class="cdbx-btn-1" style="float:right;"> \
                      <span class="" aria-hidden="true"></span><b>Run</b></span> \
                    </button> \
                  </div> \
                  <div class="cdbx-div-right-2" style="width:100%;"> \
                    <input id="cdbx-filename" class="cdbx-textbox" style="margin-top:5px;float:left;font-size:13px;" placeholder="Filename"></input><span id="cdbx-filename-ext" style="float:left;margin-top:5px;"></span> \
                    <!--<button type="button" id="cdbx-code-help" class="cdbx-btn-1" style="float:right"> \
                      <span class="dashicons dashicons-editor-help" aria-hidden="true"></span> \
                    </button>--> \
                  </div> \
                  <div id="cdbx-div-output" style="float:left;width:100%;text-align:left"> \
                    Output Appears Here ... \
                  </div> \
                  <div style="width:100%"> \
                    <textarea id="cdbx-stdin" class="cdbx-textarea-input" style="font-size:13px;" rows="4" cols="200" placeholder="Stdin (One input element per line)"></textarea> \
                    <textarea id="cdbx-cmdline" class="cdbx-textarea-input" style="font-size:13px;" rows="1" placeholder="Cmd Line Args"></textarea> \
                  </div> \
                </div> \
              </div> \
            </div>';

            return div_content;  
        };
        
        var getWebCodeEditorData = function () {
            var div_content =
            '<div id="cdbx-editor-dialog"> \
              <ul class="cdbx-tabs-web" style="text-align:left;background:#FFFFFF"> \
		       <li id="cdbx-tab-web-html" class="cdbx-tab-link current" data-tab="cdbx-tab-html">Html</li> \
		       <li id="cdbx-tab-web-css" class="cdbx-tab-link" data-tab="cdbx-tab-css">CSS</li> \
               <li id="cdbx-tab-web-js" class="cdbx-tab-link" data-tab="cdbx-tab-js">Javascript</li> \
		      </ul> \
             <div class="cdbx-editor-div-left" style="margin-top:5px;"> \
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
              <div class="cdbx-editor-div-right" style="margin-top:5px;background-color:#FFFFFF"> \
                   <div> \
                        <button type="" id="cdbx-fullscreen" class="cdbx-btn-1" title="Full screen"> \
                          <span class="dashicons dashicons-editor-expand" aria-hidden="true"></span> \
                        </button> \
                        <a id="cdbx-output-web-link" class="cdbx-btn-1 disabled" target="_blank" href="" title="a unique link gets generated everytime code is executed">Link</a> \
                        <button type="button" id="cdbx-ace-theme-xcode-web" class="cdbx-btn-1 cdbx-ace-theme-web" title="Light theme"> \
                          <span class="dashicons dashicons-visibility" aria-hidden="true"></span> \
                        </button> \
                        <button type="button" id="cdbx-ace-theme-monokai-web" class="cdbx-btn-1 cdbx-ace-theme-web" title="Dark (monokai) theme"> \
                          <span class="dashicons dashicons-art" aria-hidden="true"></span> \
                        </button> \
                        <button type="button" id="cdbx-ace-theme-cobalt-web" class="cdbx-btn-1 cdbx-ace-theme-web" title="Dark (cobalt) theme"> \
                          <span class="dashicons dashicons-image-filter" aria-hidden="true"></span> \
                        </button> \
                        <button type="button" id="cdbx-ace-font-zoomin-web" class="cdbx-btn-1"> \
                          <span class="dashicons dashicons-plus" aria-hidden="true"></span> \
                        </button> \
                        <button type="button" id="cdbx-ace-font-zoomout-web" class="cdbx-btn-1"> \
                          <span class="dashicons dashicons-minus" aria-hidden="true"></span> \
                        </button> \
                        \
                        <button type="button" id="cdbx-run-code-web" class="cdbx-btn-1" style="float:right"> \
                          <span class="" aria-hidden="true"></span> <b>Run</b> \
                        </button> \
                    </div> \
                    <br><br> \
                    <div id="cdbx-div-output-web" style="float:left;width:100%;text-align:left;margin-top:27px;font-size:13px;"> \
                        Output Appears Here ... \
                    </div> \
                    <div style="width:100%;"> \
                    <textarea class="cdbx-textarea-input" style="border:1px solid #FFFFFF;resize:none;" rows="0" cols="200"></textarea> \
                  </div> \
                 </div> \
            </div>';

            return div_content;
        };

    });
});
