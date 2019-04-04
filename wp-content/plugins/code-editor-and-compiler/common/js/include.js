var cdbx_compilebinLinkCompile = 'https://www.compilebin.com/compile';
var cdbx_compilebinLinkTest = 'https://www.compilebin.com/test';
var cdbx_compilebinLinkWebDesign = 'https://www.compilebin.com/webdesign';

var cdbx_progName = 'Filename';
var cdbx_default_output = "Output appears here ...";
var cdbx_output_status_progress = '<b>Processing ...</b>';
var cdbx_output_status_fail = '<b>Processing Failure .....</b>';

var cdbx_key_save_progress = '<b>Saving API key.</b><br><br>';
var cdbx_key_save_fail = '<b>Failed to save API key.</b><br><br>';
var cdbx_key_empty = '<b>Please enter a valid key.</b><br><br>';

var cdbx_global_setting_save_progress = '<b>Saving your preferences.</b><br><br>';
var cdbx_global_setting_save_fail = '<b>Failed to save your preferences.</b><br><br>';

var CDBX_INSERT_CODE      = '#cdbx-insert-code';
var CDBX_SAVE_CODE        = '#cdbx-save-code';
var CDBX_DELETE_CODE      = '#cdbx-delete-code';
var CDBX_FILENAME         = '#cdbx-filename';
var CDBX_FILENAME_EXT     = '#cdbx-filename-ext';
var CDBX_DIV_OUTPUT       = '#cdbx-div-output';
var CDBX_STDIN            = '#cdbx-stdin';
var CDBX_CMDLINE          = '#cdbx-cmdline';
var CDBX_EDITOR_DIALOG    = '#cdbx-editor-dialog';
var CDBX_LANG             = '#cdbx-lang';
var CDBX_PREF_LANG        = '#cdbx-pref-lang';
var CDBX_PREF_EDITOR      = '#cdbx-pref-editor';
var CDBX_CODE_HELP        = '#cdbx-code-help';
var CDBX_SETTING          = '#cdbx-setting';
var CDBX_GLOBAL_SETTING   = '#cdbx-global-setting';
var CDBX_CODE_HELP_DIALOG = '#cdbx-code-help-dialog';
var CDBX_SETTING_DIALOG   = '#cdbx-setting-dialog';
var CDBX_GLOBAL_SETTING_DIALOG = '#cdbx-global-setting-dialog';
var CDBX_HIDDEN_CONTENT   = '#cdbx-hidden-content';
var CDBX_RUN_CODE         = '#cdbx-run-code';
var CDBX_RUN_CODE_WEB     = '#cdbx-run-code-web';
var CDBX_ACE_FONT_ZOOMOUT = '#cdbx-ace-font-zoomout';
var CDBX_ACE_FONT_ZOOMIN  = '#cdbx-ace-font-zoomin';
var CDBX_SAVE_KEY         = '#cdbx-save-key';
var CDBX_API_KEY          = '#cdbx-api-key';
var CDBX_API_KEY_SAVE_MSG = '#cdbx-api-key-save-msg';
var CDBX_RUN_BTN_STATUS   = '#cdbx-run-btn-status';
var CDBX_COPY_BTN_STATUS  = '#cdbx-copy-btn-status';
var CDBX_FULLSCREEN_STATUS = '#cdbx-fullscreen-status';
var CDBX_LINENUM_STATUS   = '#cdbx-linenum-status';
var CDBX_DARKTHEME_STATUS = '#cdbx-darktheme-status';
var CDBX_TMCE_DOUBLE_CLICK_STATUS = '#cdbx-tmce-doubleclick-status';
var CDBX_SAVE_GLOBAL_SETTING = '#cdbx-save-global-setting';
var CDBX_GLOBAL_SETTING_SAVE_MSG = '#cdbx-global-setting-save-msg';
var CDBX_GLOBAL_SETTING_CLOSE = '#cdbx-global-setting-close';
var CDBX_SAVE_KEY_CLOSE = '#cdbx-save-key-close';

var CDBX_ACE_THEME_CLASS     = '.cdbx-ace-theme';
var CDBX_ACE_THEME_CLASS_WEB = '.cdbx-ace-theme-web';
var CDBX_TRY_CODE            = '.cdbx-try-code';
var CDBX_TRY_CODE_WEB        = '.cdbx-try-code-web';
var CDBX_BTN_MAIN            = '.cdbx-btn-main';
var CDBX_BTN_COPY            = '.cdbx-btn-copy';

var CDBX_ELEM_EDITOR_DIALOG     = 'cdbx-editor-dialog';
var CDBX_ELEM_COMPILEBIN_EDITOR = 'cdbx-compilebin-editor';
var CDBX_ELEM_HIDDEN_CONTENT    = 'cdbx-hidden-content';
var CDBX_ELEM_DIV_OUTPUT        = 'cdbx-div-output';
var CDBX_OUTPUT_WEB_LINK        = '#cdbx-output-web-link';

var CDBX_SAVE_CODE_WEB        = '#cdbx-save-code-web';
var CDBX_DELETE_CODE_WEB      = '#cdbx-delete-code-web';
var CDBX_DIV_OUTPUT_WEB       = '#cdbx-div-output-web'; 
var CDBX_ACE_FONT_ZOOMOUT_WEB = '#cdbx-ace-font-zoomout-web';
var CDBX_ACE_FONT_ZOOMIN_WEB  = '#cdbx-ace-font-zoomin-web';

var CDBX_ELEM_COMPILEBIN_EDITOR_HTML = 'cdbx-compilebin-editor-html';
var CDBX_ELEM_COMPILEBIN_EDITOR_CSS  = 'cdbx-compilebin-editor-css';
var CDBX_ELEM_COMPILEBIN_EDITOR_JS   = 'cdbx-compilebin-editor-js';
var CDBX_ELEM_DIV_OUTPUT_WEB         = 'cdbx-div-output';

var CDBX_HIDDEN_CONTENT_HTML = '#cdbx-hidden-content-html';
var CDBX_HIDDEN_CONTENT_CSS  = '#cdbx-hidden-content-css';
var CDBX_HIDDEN_CONTENT_JS   = '#cdbx-hidden-content-js';

var CDBX_ELEM_HIDDEN_CONTENT_HTML = 'cdbx-hidden-content-html';
var CDBX_ELEM_HIDDEN_CONTENT_CSS  = 'cdbx-hidden-content-css';
var CDBX_ELEM_HIDDEN_CONTENT_JS   = 'cdbx-hidden-content-js';

var CDBX_EDITOR_DIALOG_WIDTH           = '90%';
var CDBX_CODE_HELP_DIALOG_WIDTH        = '70%';
var CDBX_SETTING_DIALOG_WIDTH          = '40%';
var CDBX_GLOBAL_SETTING_DIALOG_WIDTH   = '70%';

var CDBX_ACE_THEME_XCODE      = 'ace/theme/xcode';
var CDBX_ACE_THEME_MONOKAI    = 'ace/theme/monokai';
var CDBX_ACE_THEME_COBALT     = 'ace/theme/cobalt';

var CDBX_ACE_THEME_XCODE_ID   = 'cdbx-ace-theme-xcode';
var CDBX_ACE_THEME_MONOKAI_ID = 'cdbx-ace-theme-monokai';
var CDBX_ACE_THEME_COBALT_ID  = 'cdbx-ace-theme-cobalt';

var CDBX_ACE_THEME_XCODE_ID_WEB   = 'cdbx-ace-theme-xcode-web';
var CDBX_ACE_THEME_MONOKAI_ID_WEB = 'cdbx-ace-theme-monokai-web';
var CDBX_ACE_THEME_COBALT_ID_WEB  = 'cdbx-ace-theme-cobalt-web';

var CDBX_TAB_STANDARD  = '#cdbx-tab-standard';
var CDBX_TAB_WEBDESIGN = '#cdbx-tab-web-design';

var CDBX_TABS_WEB = '.cdbx-tabs-web';
var CDBX_TABS_PLACEHOLDER = '.cdbx-tabs-placeholder';

var CDBX_PREF_EDITOR = '#cdbx-pref-editor';
var CDBX_PREF_LANG   = '#cdbx-pref-lang';
var CDBX_PREF_THEME  = '#cdbx-pref-theme';

var CDBX_CODE_LINES_HIGHLIGHT      = '#cdbx-code-lines-highlight';
var CDBX_CODE_LINES_HIGHLIGHT_AREA = '#cdbx-code-lines-highlight-area';
var CDBX_LINES_HIGHLIGHTED         = '#cdbx-lines-highlighted';
var CDBX_LINES_HIGHLIGHTED_HIDDEN  = '#cdbx-lines-highlighted-hidden';
var CDBX_LINES_HIGHLIGHT_NOW       = '#cdbx-lines-highlight-now';
var CDBX_SELECT_LINES              = '#cdbx-select-lines';
var CDBX_REMOVE_HIGHLIGHT_LINES    = '.cdbx-remove-highlight-lines';

var CDBX_CODE_LINES_HIGHLIGHT_WEB      = '#cdbx-code-lines-highlight-web';

var CDBX_CODE_LINES_HIGHLIGHT_AREA_HTML = '#cdbx-code-lines-highlight-area-html';
var CDBX_LINES_HIGHLIGHTED_HTML         = '#cdbx-lines-highlighted-html';
var CDBX_LINES_HIGHLIGHTED_HIDDEN_HTML  = '#cdbx-lines-highlighted-hidden-html';
var CDBX_LINES_HIGHLIGHT_NOW_HTML       = '#cdbx-lines-highlight-now-html';
var CDBX_SELECT_LINES_HTML              = '#cdbx-select-lines-html';
var CDBX_REMOVE_HIGHLIGHT_LINES_HTML    = '.cdbx-remove-highlight-lines-html';

var CDBX_CODE_LINES_HIGHLIGHT_AREA_CSS = '#cdbx-code-lines-highlight-area-css';
var CDBX_LINES_HIGHLIGHTED_CSS         = '#cdbx-lines-highlighted-css';
var CDBX_LINES_HIGHLIGHTED_HIDDEN_CSS  = '#cdbx-lines-highlighted-hidden-css';
var CDBX_LINES_HIGHLIGHT_NOW_CSS       = '#cdbx-lines-highlight-now-css';
var CDBX_SELECT_LINES_CSS              = '#cdbx-select-lines-css';
var CDBX_REMOVE_HIGHLIGHT_LINES_CSS    = '.cdbx-remove-highlight-lines-css';

var CDBX_CODE_LINES_HIGHLIGHT_AREA_JS = '#cdbx-code-lines-highlight-area-js';
var CDBX_LINES_HIGHLIGHTED_JS         = '#cdbx-lines-highlighted-js';
var CDBX_LINES_HIGHLIGHTED_HIDDEN_JS  = '#cdbx-lines-highlighted-hidden-js';
var CDBX_LINES_HIGHLIGHT_NOW_JS       = '#cdbx-lines-highlight-now-js';
var CDBX_SELECT_LINES_JS              = '#cdbx-select-lines-js';
var CDBX_REMOVE_HIGHLIGHT_LINES_JS    = '.cdbx-remove-highlight-lines-js';

var CDBX_TAB_WEB_HTML  = '#cdbx-tab-web-html';
var CDBX_TAB_WEB_CSS   = '#cdbx-tab-web-css';
var CDBX_TAB_WEB_JS    = '#cdbx-tab-web-js';

var CDBX_FULLSCREEN            = '#cdbx-fullscreen';
var CDBX_FULLSCREEN_STATUS     = '#cdbx-fullscreen-status';
var CDBX_FULLSCREEN_STATUS_DIV = '#cdbx-fullscreen-status-div';

var cdbx_languages = [
    { id: 0,     name: 'C',           mode: 'ace/mode/c_cpp',      ext: '.c'     },
    { id: 1,     name: 'C++',         mode: 'ace/mode/c_cpp',      ext: '.cpp'   },
    { id: 2,     name: 'Java',        mode: 'ace/mode/java',       ext: '.java'  },
    { id: 3,     name: 'Python2.7',   mode: 'ace/mode/python',     ext: '.py'    },
    { id: 4,     name: 'Python3',     mode: 'ace/mode/python',     ext: '.py'    },
    { id: 5,     name: 'Perl',        mode: 'ace/mode/perl',       ext: '.pl'    },
    { id: 6,     name: 'Ruby',        mode: 'ace/mode/ruby',       ext: '.rb'    },
    { id: 7,     name: 'Clojure',     mode: 'ace/mode/clojure',    ext: '.clj'   },
    { id: 8,     name: 'Elixir',      mode: 'ace/mode/elixir',     ext: '.ex'    },
    { id: 9,     name: 'C#',          mode: 'ace/mode/csharp',     ext: '.cs'    },
    { id: 10,    name: 'Erlang',      mode: 'ace/mode/erlang',     ext: '.erl'   },
    { id: 11,    name: 'Scala',       mode: 'ace/mode/scala',      ext: '.scala' },
    { id: 12,    name: 'Go',          mode: 'ace/mode/golang',     ext: '.go'    },
    { id: 13,    name: 'Objective-C', mode: 'ace/mode/objectivec', ext: '.m'     },
    { id: 14,    name: 'VB.Net',      mode: 'ace/mode/vbscript',   ext: '.vb'    },
    { id: 15,    name: 'Swift3',      mode: 'ace/mode/objectivec', ext: '.swift' },
    { id: 9999,  name: 'Default',     mode: 'ace/mode/c_cpp',      ext: ''       }
];

var cdbx_languages_web = [
    { id: 0,  name: 'Html',       mode: 'ace/mode/html',       ext: 'html'},
    { id: 1,  name: 'Css',        mode: 'ace/mode/css',        ext: 'css'},
    { id: 2,  name: 'Javascript', mode: 'ace/mode/javascript', ext: 'js'}
];

var cdbx_editor_type = [
    { id: 0,  name: 'Standard' },
    { id: 1,  name: 'Web Design' }
];

var cdbx_editor_theme = [
    { id: 0,  name: 'Light' },
    { id: 1,  name: 'Dark (Monokai)' },
    { id: 2,  name: 'Dark (Cobalt)' }
];

var CDBX_EVENT_OPEN  = 'open';
var CDBX_EVENT_CLOSE = 'close';
var CDBX_EVENT_CLICK = 'click';
var CDBX_EVENT_TMCE_CLICK = 'click'; 

var CDBX_EDITOR_STANDARD = 0;
var CDBX_EDITOR_WEBDESIGN = 1;

var CDBX_THEME_XCODE   = 0;
var CDBX_THEME_MONOKAI = 1;
var CDBX_THEME_COBALT  = 2;

var cdbx_editor = null;
var cdbx_editor_html = null;
var cdbx_editor_css = null;
var cdbx_editor_js = null;
var cdbx_defaultMode = 'ace/mode/c_cpp';
var cdbx_defLangId = cdbx_languages[cdbx_languages.length - 1].id;
var cdbx_curLangId = cdbx_defLangId;
var cdbx_curLangIdPref = cdbx_defLangId;
var cdbx_curEditorId = 0;
var cdbx_curEditorIdPref = 0;
var cdbx_run_btn_status = 1;
var cdbx_linenum_status = 1;
var cdbx_copy_btn_status = 1;
var cdbx_fullscreen_status = 1;
var cdbx_darktheme_status = 0;
var cdbx_tmce_double_click_status = 0;
var cdbx_linesHighlight = null;
var cdbx_linesHighlightHtml = null;
var cdbx_linesHighlightCss = null;
var cdbx_linesHighlightJs = null;
var cdbx_curThemePrefId = CDBX_THEME_XCODE;
var cdbx_curThemeId = CDBX_THEME_XCODE;
var cdbx_curThemePref = CDBX_ACE_THEME_XCODE;
var cdbx_curTheme = CDBX_ACE_THEME_XCODE;

var CDBX_TAB_HTML_ID = 0;
var CDBX_TAB_CSS_ID  = 1;
var CDBX_TAB_JS_ID   = 2;

var cdbx_active_tab_web = CDBX_TAB_HTML_ID;
var cdbx_highlight_area_active = false;

var CDBX_CRAYON_DETECT_STRING = "lang:";
var CDBX_WP_SYNTAX_HIGHLIGHTER_DETECT_STRING = "brush:";
