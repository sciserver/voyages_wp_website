<?php
class compilebinAdmin {

   private $plugin_name;
   private $plugin_version;

   public function __construct() {
      $this->plugin_name = "code-editor-and-compiler";
      $this->plugin_version = "1.4.1";
      //add_action('admin_head', array($this, 'cdbx_add_insert_code_button'));   
      add_action('admin_init', array($this, 'additional_plugin_check'));   
      add_action('admin_notices', array($this, 'plugin_activation'));
      add_action('deactivated_plugin', array($this, 'plugin_deactivation'));   
      add_action('admin_enqueue_scripts', array(&$this, 'enqueueScripts'));
      add_action('admin_enqueue_scripts', array(&$this, 'enqueueStyles'));
      add_action('media_buttons', array(&$this, 'insertCodeButton'));
      add_action('wp_ajax_editor_modal', array(&$this, 'loadEditorModal'));
      add_action('wp_ajax_editor_modal_web', array(&$this, 'loadEditorModalWeb'));   
      add_action('wp_ajax_compile', array(&$this, 'compileCode'));
      add_action('wp_ajax_runhtmlcode', array(&$this, 'runHtmlCode'));
      add_action('wp_ajax_save_key', array(&$this, 'saveAPIKey'));
      add_action('wp_ajax_save_editor_preference', array(&$this, 'saveEditorPreference'));
      add_action('wp_ajax_get_editor_preference', array(&$this, 'getEditorPreference'));   
      add_action('wp_ajax_save_lang_preference', array(&$this, 'saveLangPreference'));
      add_action('wp_ajax_get_lang_preference', array(&$this, 'getLangPreference'));   
      add_action('wp_ajax_save_run_btn_status', array(&$this, 'saveRunBtnStatus'));
      add_action('wp_ajax_get_run_btn_status', array(&$this, 'getRunBtnStatus'));
      add_action('wp_ajax_save_global_setting', array(&$this, 'saveGlobalSetting'));
      add_action('wp_ajax_get_global_setting', array(&$this, 'getGlobalSetting'));
      add_action('wp_ajax_get_public_setting', array(&$this, 'getPublicSetting'));
      add_action('wp_ajax_get_tmce_click_setting', array(&$this, 'getTMCEClickSetting'));   
      add_action('wp_ajax_nopriv_editor_modal', array(&$this, 'loadEditorModalPublic'));
      add_action('wp_ajax_nopriv_editor_modal_web', array(&$this, 'loadEditorModalPublicWeb'));   
      add_action('wp_ajax_nopriv_compile', array(&$this, 'compileCode'));
      add_action('wp_ajax_nopriv_runhtmlcode', array(&$this, 'runHtmlCode'));
      add_action('wp_ajax_nopriv_get_run_btn_status', array(&$this, 'getRunBtnStatus'));
      add_action('wp_ajax_nopriv_get_public_setting', array(&$this, 'getPublicSetting')); 
   }
    
   public function plugin_activation() {
       if (is_plugin_active('crayon-syntax-highlighter/crayon_wp.class.php')) {
           $html = '<div class="updated notice is-dismissible">
                       <p>Compilebin is not compatible with crayon syntax highlighter. So, crayon is <strong>deactivated</strong> and all previous code snippets added with crayon will be syntax highlighted by compilebin.</p>
                    </div>';
           deactivate_plugins('crayon-syntax-highlighter/crayon_wp.class.php');
           echo $html;   
       }
       if (is_plugin_active('wp-syntaxhighlighter/wp-syntaxhighlighter.php')) {
           $html = '<div class="updated notice is-dismissible">
                       <p>Compilebin is not compatible with WP Syntax Highlighter. So, WP Syntax Highlighter is <strong>deactivated</strong> and all previous code snippets added with WP Syntax Highlighter will be syntax highlighted by compilebin.</p>
                    </div>';
           deactivate_plugins('wp-syntaxhighlighter/wp-syntaxhighlighter.php');
           echo $html;   
       }
   }
    
   public function additional_plugin_check() {
       if (is_plugin_active('syntaxhighlighter/syntaxhighlighter.php')) {
           if (get_option('compilebinActivated') == 'Plugin-Slug') {
               delete_option('compilebinActivated');
               $html = '<div class="updated notice is-dismissible">
                           <p>Existing code snippets which are using <i>Syntax Highlighter Evolved</i> plugin will now be syntax highlighted using <i>Compilebin</i>. Please do <b>NOT</b> deactivate <i>Syntax Highlighter Evolved</i> plugin.</p>
                        </div>';
               echo $html;
           }
       }
   }    
    
   public function plugin_deactivation() {
       //echo 'plugin deactivated';
   }    

   public function enqueueScripts() {
      wp_enqueue_script('jquery-ui-dialog');
      wp_enqueue_script('ace', plugins_url() . '/' . $this->plugin_name . '/ace-builds-master/src-noconflict/ace.js', array('jquery'), $this->plugin_version, false);
      wp_enqueue_script('include-js', plugins_url() . '/' . $this->plugin_name . '/common/js/include.js', array('jquery'), $this->plugin_version, false);
      wp_enqueue_script('editor-handler', plugin_dir_url( __FILE__ ) . 'js/editor-handler.js', array('jquery'), $this->plugin_version, false);
      wp_localize_script('editor-handler', 'cdbx_ajax_script', array('ajaxurl' => admin_url('admin-ajax.php')));
   }

   public function enqueueStyles() {
      wp_enqueue_style('wp-jquery-ui-dialog');
      wp_enqueue_style('editor-style', plugins_url() . '/' . $this->plugin_name .  '/common/css/editor-style.css', array(), $this->plugin_version, 'all');
   }
    
   public function cdbx_add_insert_code_button() {
      global $typenow;
      if (!current_user_can('edit_posts') && !current_user_can('edit_pages')) return;
      if (!in_array($typenow, array('post', 'page'))) return;
      if (get_user_option('rich_editing') == 'true') {
         add_filter('mce_external_plugins', array($this, 'cdbx_add_tinymce_plugin'));
         add_filter('mce_buttons', array($this, 'cdbx_register_insert_code_button'));
      }
   }
    
   public function cdbx_add_tinymce_plugin($plugin_array) {
      $plugin_array['cdbx_insert_code_button'] = plugin_dir_url( __FILE__ ) . 'js/editor-handler.js';
      return $plugin_array;
   }
    
   public function cdbx_register_insert_code_button($buttons) {
      array_push($buttons, "cdbx_insert_code_button");
      return $buttons;
   }

   public function insertCodeButton() {
      echo '<a href="#" id="cdbx-insert-code" class="button"><span class="dashicons dashicons-editor-code" style="margin-top:0.2em"></span>&nbsp;Insert Code</a>';
   }
  
   public function compileCode() {
      $key = null;
      if (false === ($key = get_transient('api_key'))) {
        $key = get_option('api_key');
        set_transient('api_key', $key, YEAR_IN_SECONDS);
      }
      
      $postData = array(
        'language' => $_POST['language'],
        'code' => stripslashes($_POST['code']),
        'stdin' => stripslashes($_POST['stdin']),
        'cmdlineargs' => stripslashes($_POST['cmdlineargs']),
        'fileName' => stripslashes($_POST['fileName']),
        'key' => $key
      );
     
      $url = stripslashes($_POST['url']);
      $response = wp_remote_post($url, array(
	      'body' => $postData,
          'timeout' => 20
        )
      );

      //print_r($response);   

      echo $response['body'];
      wp_die();
   }
    
   public function runHtmlCode() {
      $key = null;
      if (false === ($key = get_transient('api_key'))) {
        $key = get_option('api_key');
        set_transient('api_key', $key, YEAR_IN_SECONDS);
      }
      
      $postData = array(
        'html' => stripslashes($_POST['html']),
        'css' => stripslashes($_POST['css']),
        'js' => stripslashes($_POST['js']),
        'externalCss' => stripslashes($_POST['externalCss']),
        'externalJs' => stripslashes($_POST['externalJs']),
        'key' => $key
      );
     
      $url = stripslashes($_POST['url']);
      $response = wp_remote_post($url, array(
	      'body' => $postData,
          'timeout' => 20
        )
      );

      echo $response['body'];
      wp_die();
   }    
  
   public function saveAPIKey() {
      $key = trim($_POST['key']);
      delete_option('api_key');
      delete_transient('api_key');
      $status = add_option('api_key', $key, '', 'no');
      if ($status) {
        echo "<b>API key saved successfully.</b><br><br>";
      } else {
        echo "<b>Failed to save API key. Please try again.</b><br><br>";
      }
      wp_die();
   }
    
   private function saveRunBtnStatusInternal() {
      $run_btn_status = $_POST['run_btn_status'];
      delete_option('run_btn_status');
      delete_transient('run_btn_status');
      $status = add_option('run_btn_status', $run_btn_status, '', 'no');
      return $status;
   }

   public function saveRunBtnStatus() {
      $status = $this->saveRunBtnStatusInternal();
      if ($status) {
        echo "Run button status saved successfully.";
      } else {
        echo "Error setting run button status preference. Please try again.";
      }
      wp_die();
   }
    
   private function getRunBtnStatusInternal() {
      $run_btn_status = null;
      if (false === ($run_btn_status = get_transient('run_btn_status'))) {
        $run_btn_status = get_option('run_btn_status');
        set_transient('run_btn_status', $run_btn_status, YEAR_IN_SECONDS);
      }
      return $run_btn_status;   
   }

   public function getRunBtnStatus() {
      $run_btn_status = $this->getRunBtnStatusInternal();
      echo $run_btn_status;
      wp_die();
   }
    
   private function saveCopyBtnStatusInternal() {
      $copy_btn_status = $_POST['copy_btn_status'];
      delete_option('copy_btn_status');
      delete_transient('copy_btn_status');
      $status = add_option('copy_btn_status', $copy_btn_status, '', 'no');
      return $status;
   }

   public function saveCopyBtnStatus() {
      $status = $this->saveCopyBtnStatusInternal();
      if ($status) {
        echo "Copy button status saved successfully.";
      } else {
        echo "Error setting copy button status preference. Please try again.";
      }
      wp_die();
   }    
    
   private function getCopyBtnStatusInternal() {
      $copy_btn_status = null;
      if (false === ($copy_btn_status = get_transient('copy_btn_status'))) {
        $copy_btn_status = get_option('copy_btn_status');
        set_transient('copy_btn_status', $copy_btn_status, YEAR_IN_SECONDS);
      }
      return $copy_btn_status;
   }

   public function getCopyBtnStatus() {
      $copy_btn_status = $this->getCopyBtnStatusInternal();
      echo $copy_btn_status;
      wp_die();
   }    
    
   private function saveEditorPreferenceInternal() {
      $editor_type = $_POST['editor_type'];
      delete_option('editor_type');
      delete_transient('editor_type');
      $status = add_option('editor_type', $editor_type, '', 'no');
      return $status;
   }    
    
   public function saveEditorPreference() {
      $status = $this->saveEditorPreferenceInternal();
      if ($status) {
        echo "Editor preference saved successfully.";
      } else {
        echo "Error setting editor preference. Please try again.";
      }
      wp_die();
   }
    
   public function getEditorPreferenceInternal() {
      $editor_type = null;
      if (false === ($editor_type = get_transient('editor_type'))) {
        $editor_type = get_option('editor_type');
        set_transient('editor_type', $editor_type, YEAR_IN_SECONDS);
      }
      return $editor_type;   
   }    
    
   public function getEditorPreference() {
      $editor_type = $this->getEditorPreferenceInternal();
      echo $editor_type;
      wp_die();
   }
   
   public function saveLangPreferenceInternal() {
      $lang = $_POST['lang'];
      delete_option('lang');
      delete_transient('lang');
      $status = add_option('lang', $lang, '', 'no');
      return $status;
   } 
       
   private function saveLangPreference() {
      $status = saveLangPreferenceInternal();
      if ($status) {
        echo "Language preference saved successfully.";
      } else {
        echo "Error setting language preference. Please try again.";
      }
      wp_die();
   } 
       
   private function getLangPreferenceInternal() {
      $lang_type = null;
      if (false === ($lang_type = get_transient('lang'))) {
        $lang_type = get_option('lang');
        set_transient('lang', $lang_type, YEAR_IN_SECONDS);
      }
      return $lang_type;   
   }
    
   public function getLangPreference() {
      $lang_type = $this->getLangPreferenceInternal();
      echo $lang_type;
      wp_die();
   }
    
   public function saveThemePreferenceInternal() {
      $theme = $_POST['theme'];
      delete_option('theme');
      delete_transient('theme');
      $status = add_option('theme', $theme, '', 'no');
      return $status;
   } 
       
   private function saveThemePreference() {
      $status = saveThemePreferenceInternal();
      if ($status) {
        echo "Theme preference saved successfully.";
      } else {
        echo "Error setting theme preference. Please try again.";
      }
      wp_die();
   }    
    
   private function getThemePreferenceInternal() {
      $theme_type = null;
      if (false === ($theme_type = get_transient('theme'))) {
        $theme_type = get_option('theme');
        set_transient('theme', $theme_type, YEAR_IN_SECONDS);
      }
      return $theme_type; 
   }
    
   public function getThemePreference() {
      $theme_type = $this->getThemePreferenceInternal();
      echo $theme_type;
      wp_die();
   }
    
   public function saveLinenumPreferenceInternal() {
      $linenum = $_POST['linenum_status'];
      delete_option('linenum_status');
      delete_transient('linenum_status');
      $status = add_option('linenum_status', $linenum, '', 'no');
      return $status;
   } 
       
   private function saveLinenumPreference() {
      $status = saveLinenumPreferenceInternal();
      if ($status) {
        echo "Line number preference saved successfully.";
      } else {
        echo "Error setting line number preference. Please try again.";
      }
      wp_die();
   }    
    
   private function getLinenumPreferenceInternal() {
      $linenum_status = null;
      if (false === ($linenum_status = get_transient('linenum_status'))) {
        $linenum_status = get_option('linenum_status');
        set_transient('linenum_status', $linenum_status, YEAR_IN_SECONDS);
      }
      return $linenum_status; 
   }
    
   public function getLinenumPreference() {
      $linenum_status = $this->getLinenumPreferenceInternal();
      echo $linenum_status;
      wp_die();
   }
    
   private function saveFullscreenStatusInternal() {
      $fullscreen_status = $_POST['fullscreen_status'];
      delete_option('fullscreen_status');
      delete_transient('fullscreen_status');
      $status = add_option('fullscreen_status', $fullscreen_status, '', 'no');
      return $status;
   }

   public function saveFullscreenStatus() {
      $status = $this->saveFullscreenStatusInternal();
      if ($status) {
        echo "Fullscreen status saved successfully.";
      } else {
        echo "Error setting fullscreen status preference. Please try again.";
      }
      wp_die();
   }    
    
   private function getFullscreenStatusInternal() {
      $fullscreen_status = null;
      if (false === ($fullscreen_status = get_transient('fullscreen_status'))) {
        $fullscreen_status = get_option('fullscreen_status');
        set_transient('fullscreen_status', $fullscreen_status, YEAR_IN_SECONDS);
      }
      return $fullscreen_status;
   }

   public function getFullscreenStatus() {
      $fullscreen_status = $this->getFullscreenStatusInternal();
      echo $fullscreen_status;
      wp_die();
   }
    
   /********************** Dark Theme Status *********************************/
    
   private function saveDarkThemeStatusInternal() {
      $darktheme_status = $_POST['darktheme_status'];
      delete_option('darktheme_status');
      delete_transient('darktheme_status');
      $status = add_option('darktheme_status', $darktheme_status, '', 'no');
      return $status;
   }

   public function saveDarkThemeStatus() {
      $status = $this->saveDarkThemeStatusInternal();
      if ($status) {
        echo "Dark theme status saved successfully.";
      } else {
        echo "Error setting Dark theme status preference. Please try again.";
      }
      wp_die();
   }    
    
   private function getDarkThemeStatusInternal() {
      $darktheme_status = null;
      if (false === ($darktheme_status = get_transient('darktheme_status'))) {
        $darktheme_status = get_option('darktheme_status');
        set_transient('darktheme_status', $darktheme_status, YEAR_IN_SECONDS);
      }
      return $darktheme_status;
   }

   public function getDarkThemeStatus() {
      $darktheme_status = $this->getDarkThemeStatusInternal();
      echo $darktheme_status;
      wp_die();
   }
    
   /***************************************************************************/
    
   /********************** Editor double click status *****************************/
    
   private function saveTMCEDoubleClickStatusInternal() {
      $doubleclick_status = $_POST['doubleclick_status'];
      delete_option('doubleclick_status');
      delete_transient('doubleclick_status');
      $status = add_option('doubleclick_status', $doubleclick_status, '', 'no');
      return $status;
   }

   public function saveTMCEDoubleClickStatus() {
      $status = $this->saveTMCEDoubleClickStatusInternal();
      if ($status) {
        echo "Double click status saved successfully.";
      } else {
        echo "Error setting Double click status preference. Please try again.";
      }
      wp_die();
   }    
    
   private function getTMCEDoubleClickStatusInternal() {
      $doubleclick_status = null;
      if (false === ($doubleclick_status = get_transient('doubleclick_status'))) {
        $doubleclick_status = get_option('doubleclick_status');
        set_transient('doubleclick_status', $doubleclick_status, YEAR_IN_SECONDS);
      }
      return $doubleclick_status;
   }

   public function getTMCEDoubleClickStatus() {
      $doubleclick_status = $this->getTMCEDoubleClickStatusInternal();
      echo $doubleclick_status;
      wp_die();
   }
    
   public function getTMCEClickSetting() {
      $settingObj = array (
         'doubleClickStatus' => $this->getTMCEDoubleClickStatusInternal() 
      );
      echo json_encode($settingObj);
      wp_die();   
   }    

   /*******************************************************************************/     
    
   public function getGlobalSetting() {
      $settingObj = array (
         'runBtnStatus' => $this->getRunBtnStatusInternal(),
         'copyBtnStatus' => $this->getCopyBtnStatusInternal(),  
         'editorPref' => $this->getEditorPreferenceInternal(),
         'langPref' => $this->getLangPreferenceInternal(),
         'themePref' => $this->getThemePreferenceInternal(),
         'linenumStatus' => $this->getLinenumPreferenceInternal(),
         'fullscreenStatus' => $this->getFullscreenStatusInternal(),
         'darkThemeStatus' => $this->getDarkThemeStatusInternal(),
         'doubleClickStatus' => $this->getTMCEDoubleClickStatusInternal() 
      );
      echo json_encode($settingObj);
      wp_die();   
   }
    
   public function saveGlobalSetting() {
      $statusRunBtn = $this->saveRunBtnStatusInternal();
      $statusCopyBtn = $this->saveCopyBtnStatusInternal();   
      $statusEditorPref = $this->saveEditorPreferenceInternal();
      $statusLangPref = $this->saveLangPreferenceInternal();
      $statusThemePref = $this->saveThemePreferenceInternal();
      $statusLinenumPref = $this->saveLinenumPreferenceInternal();
      $statusFullscreen = $this->saveFullscreenStatusInternal();
      $statusDarkTheme = $this->saveDarkThemeStatusInternal();
      $statusDoubleClick = $this->saveTMCEDoubleClickStatusInternal();     
      if (!$statusRunBtn || !$statusCopyBtn || !$statusEditorPref || !$statusLangPref || !$statusThemePref || !$statusLinenumPref || !$statusFullscreen || !$statusDarkTheme || !$statusDoubleClick) {
         echo "<b>Error saving your preferences. Please try again.</b><br><br>";      
      } else {
         echo "<b>Your preferences saved successfully.</b><br><br>";  
      }
      wp_die();
   }
    
   public function getPublicSetting() {
      $settingObj = array (
         'runBtnStatus' => $this->getRunBtnStatusInternal(),
         'copyBtnStatus' => $this->getCopyBtnStatusInternal(),
         'themePref' => $this->getThemePreferenceInternal(),
         'linenumStatus' => $this->getLinenumPreferenceInternal(),
         'fullscreenStatus' => $this->getFullscreenStatusInternal(),
         'darkthemeStatus' => $this->getDarkThemeStatusInternal()  
      );
      echo json_encode($settingObj);
      wp_die();   
   }    
     
   public function loadEditorModal() {
      $div_content = null;
      if ($_POST['caller'] == 'admin') {
        $div_content = $this->getModalContent();
      } else {
        $div_content = $this->getModalContentPublic();
      }

      echo $div_content;
      wp_die();
   }
    
   public function loadEditorModalWeb() {
      $div_content = null;
      if ($_POST['caller'] == 'admin') {
        $div_content = $this->getModalContentWeb();
      } else {
        $div_content = $this->getModalContentPublicWeb();
      }

      echo $div_content;
      wp_die();
   }    
  
   public function loadEditorModalPublic() {
      echo $this->getModalContentPublic();
      wp_die();
   }
    
   public function loadEditorModalPublicWeb() {
      echo $this->getModalContentPublicWeb();
      wp_die();
   }    
   
   private function getModalContent() {
      $div_content = 
          '<div style="width:100%;margin-top:-10px;"><ul class="cdbx-tabs" style="float:right">
		     <li id="cdbx-tab-standard" class="cdbx-tab-link current" data-tab="cdbx-tab-1">Standard</li>
		     <li id="cdbx-tab-web-design" class="cdbx-tab-link" data-tab="cdbx-tab-2">Web Design</li>
		   </ul></div>
           <ul class="cdbx-tabs-web">
		       <li class="cdbx-tab-link current" data-tab="cdbx-tab-html">Html</li>
		       <li class="cdbx-tab-link" data-tab="cdbx-tab-css">CSS</li>
               <li class="cdbx-tab-link" data-tab="cdbx-tab-js">Javascript</li>
		   </ul>
           <div class="cdbx-tabs-placeholder">
           <br><br>
           </div>
           <div id="cdbx-tab-1" class="cdbx-tab-content current">
              <div id="cdbx-editor-dialog">
              <div class="cdbx-editor-div">
                <div class="cdbx-editor-div-left">
                  <div id="cdbx-compilebin-editor" class="cdbx-editor"></div>
                </div>
                <div class="cdbx-editor-div-right">
                  <div>
                    <button type="button" id="cdbx-save-code" class="button button-primary">
                      <span class="" aria-hidden="true" style="margin-top:0.2em"></span> <b>Save</b>
                    </button>        
                    <button type="button" id="cdbx-ace-theme-xcode" class="button button-default cdbx-ace-theme" title="Light theme">
                      <span class="dashicons dashicons-visibility" aria-hidden="true" style="margin-top:0.2em"></span>
                    </button>
                    <button type="button" id="cdbx-ace-theme-monokai" class="button button-default cdbx-ace-theme" title="Dark (monokai) theme">
                      <span class="dashicons dashicons-art" aria-hidden="true" style="margin-top:0.2em"></span>
                    </button>
                    <button type="button" id="cdbx-ace-theme-cobalt" class="button button-default cdbx-ace-theme" title="Dark (cobalt) theme">
                      <span class="dashicons dashicons-image-filter" aria-hidden="true" style="margin-top:0.2em"></span>
                    </button>
                    <button type="button" id="cdbx-ace-font-zoomin" class="button button-default">
                      <span class="dashicons dashicons-plus" aria-hidden="true" style="margin-top:0.2em"></span>
                    </button>
                    <button type="button" id="cdbx-ace-font-zoomout" class="button button-default">
                      <span class="dashicons dashicons-minus" aria-hidden="true" style="margin-top:0.2em"></span>
                    </button>          

                    <button type="button" id="cdbx-delete-code" class="button button-default">
                      <span class="dashicons dashicons-trash" aria-hidden="true" style="margin-top:0.2em"></span>
                    </button>
                    <button type="button" id="cdbx-run-code" class="button button-primary" style="float:right;width:5em;">
                      <span class="" aria-hidden="true"></span> <b>Run</b>
                    </button>      
                   </div>
                   <div class="cdbx-div-right-2">
                     <select name="cdbx-lang" id="cdbx-lang" style="margin-top:-0.1em"></select>
                     <input id="cdbx-filename" class="cdbx-textbox" placeholder="Filename" style=""></input><span id="cdbx-filename-ext"></span>
                     <button type="button" id="cdbx-setting" class="button button-default" style="float:right" title="Enter your API key for code execution">
                       <span class="dashicons dashicons-admin-network" aria-hidden="true" style="margin-top:0.2em"></span>
                     </button>
                     <button type="button" id="cdbx-global-setting" class="button button-default" style="float:right;margin-right:0.2em;" title="Global settings that apply to all code snippets">
                       <span class="dashicons dashicons-admin-generic" aria-hidden="true" style="margin-top:0.2em"></span>
                     </button>
                   </div>
                   <div id="cdbx-div-output" style="width:98%">
                     Output Appears Here ...
                   </div>
                   <div style="width:100%">
                     <textarea id="cdbx-stdin" class="cdbx-textarea-input" rows="4" cols="200" placeholder="Stdin (One input element per line)"></textarea>
                     <textarea id="cdbx-cmdline" class="cdbx-textarea-input" rows="1" placeholder="Cmd Line Args"></textarea>
                   </div>
                </div>
              </div>
            </div>
           </div>
           <div id="cdbx-tab-2" class="cdbx-tab-content">
             <!--<ul class="cdbx-tabs-web">
		       <li class="cdbx-tab-link current" data-tab="cdbx-tab-html">Html</li>
		       <li class="cdbx-tab-link" data-tab="cdbx-tab-css">CSS</li>
               <li class="cdbx-tab-link" data-tab="cdbx-tab-js">Javascript</li>
		     </ul> -->
             <div class="cdbx-editor-div-left">
                 <div id="cdbx-tab-html" class="cdbx-tab-content-web current">
                   <div class="cdbx-editor-div">
                       <div id="cdbx-compilebin-editor-html" class="cdbx-editor"></div>
                   </div>     
                 </div>
                 <div id="cdbx-tab-css" class="cdbx-tab-content-web">
                   <div class="cdbx-editor-div">
                       <div id="cdbx-compilebin-editor-css" class="cdbx-editor"></div>
                   </div>
                 </div>
                 <div id="cdbx-tab-js" class="cdbx-tab-content-web">
                   <div class="cdbx-editor-div">
                       <div id="cdbx-compilebin-editor-js" class="cdbx-editor"></div>
                   </div>
                 </div>
              </div>
              <div class="cdbx-editor-div-right">
                   <div>
                       <button type="button" id="cdbx-save-code-web" class="button button-primary">
                          <span class="" aria-hidden="true" style="margin-top:0.2em"></span> <b>Save</b>
                        </button>        
                        <button type="button" id="cdbx-ace-theme-xcode-web" class="button button-default cdbx-ace-theme-web" title="Light theme">
                          <span class="dashicons dashicons-visibility" aria-hidden="true" style="margin-top:0.2em"></span>
                        </button>
                        <button type="button" id="cdbx-ace-theme-monokai-web" class="button button-default cdbx-ace-theme-web" title="Dark (monokai) theme">
                          <span class="dashicons dashicons-art" aria-hidden="true" style="margin-top:0.2em"></span>
                        </button>
                        <button type="button" id="cdbx-ace-theme-cobalt-web" class="button button-default cdbx-ace-theme-web" title="Dark (cobalt) theme">
                          <span class="dashicons dashicons-image-filter" aria-hidden="true" style="margin-top:0.2em"></span>
                        </button>
                        <button type="button" id="cdbx-ace-font-zoomin-web" class="button button-default">
                          <span class="dashicons dashicons-plus" aria-hidden="true" style="margin-top:0.2em"></span>
                        </button>
                        <button type="button" id="cdbx-ace-font-zoomout-web" class="button button-default">
                          <span class="dashicons dashicons-minus" aria-hidden="true" style="margin-top:0.2em"></span>
                        </button>          

                        <button type="button" id="cdbx-delete-code-web" class="button button-default">
                          <span class="dashicons dashicons-trash" aria-hidden="true" style="margin-top:0.2em"></span>
                        </button>
                        <button type="button" id="cdbx-run-code-web" class="button button-primary" style="float:right;width:5em;">
                          <span class="" aria-hidden="true"></span> <b>Run</b>
                        </button>
                    </div>
                    <div class="cdbx-div-right-2">
                     <a id="cdbx-output-web-link" class="button button-default disabled" style="width:5em;text-align:center;" target="_blank" href="" title="a unique link gets generated everytime code is executed">Link</a>
                     <button type="button" id="cdbx-setting" class="button button-default" style="float:right" title="Enter your API key for code execution">
                       <span class="dashicons dashicons-admin-network" aria-hidden="true" style="margin-top:0.2em"></span>
                     </button>
                     <button type="button" id="cdbx-global-setting" class="button button-default" style="float:right;margin-right:0.2em;" title="Global settings that apply to all code snippets">
                       <span class="dashicons dashicons-admin-generic" aria-hidden="true" style="margin-top:0.2em"></span>
                     </button>
                    </div>
                    <div id="cdbx-div-output-web" style="width:100%">
                        Output Appears Here ...
                    </div>
                 </div>
           </div>';
       
      return $div_content;   
   }


   private function getModalContentPublicWeb() {
      $div_content = 
            '<div id="cdbx-editor-dialog">
              <ul class="cdbx-tabs-web" style="text-align:left">
		       <li class="cdbx-tab-link current" data-tab="cdbx-tab-html">Html</li>
		       <li class="cdbx-tab-link" data-tab="cdbx-tab-css">CSS</li>
               <li class="cdbx-tab-link" data-tab="cdbx-tab-js">Javascript</li>
		     </ul>
             <div class="cdbx-editor-div-left" style="margin-top:5px;">
                 <div id="cdbx-tab-html" class="cdbx-tab-content-web current">
                   <div class="cdbx-editor-div">
                       <div id="cdbx-compilebin-editor-html" class="cdbx-editor"></div>
                   </div>     
                 </div>
                 <div id="cdbx-tab-css" class="cdbx-tab-content-web">
                   <div class="cdbx-editor-div">
                       <div id="cdbx-compilebin-editor-css" class="cdbx-editor"></div>
                   </div>
                 </div>
                 <div id="cdbx-tab-js" class="cdbx-tab-content-web">
                   <div class="cdbx-editor-div">
                       <div id="cdbx-compilebin-editor-js" class="cdbx-editor"></div>
                   </div>
                 </div>
              </div>
              <div class="cdbx-editor-div-right" style="margin-top:5px;">
                   <div>
                        <a id="cdbx-output-web-link" class="cdbx-btn-1 disabled" target="_blank" href="" title="a unique link gets generated everytime code is executed">Link</a>
                        <button type="button" id="cdbx-ace-theme-xcode-web" class="cdbx-btn-1 cdbx-ace-theme-web" title="Light theme">
                          <span class="dashicons dashicons-visibility" aria-hidden="true"></span>
                        </button>
                        <button type="button" id="cdbx-ace-theme-monokai-web" class="cdbx-btn-1 cdbx-ace-theme-web" title="Dark (monokai) theme">
                          <span class="dashicons dashicons-art" aria-hidden="true"></span>
                        </button>
                        <button type="button" id="cdbx-ace-theme-cobalt-web" class="cdbx-btn-1 cdbx-ace-theme-web" title="Dark (cobalt) theme">
                          <span class="dashicons dashicons-image-filter" aria-hidden="true"></span>
                        </button>
                        <button type="button" id="cdbx-ace-font-zoomin-web" class="cdbx-btn-1">
                          <span class="dashicons dashicons-plus" aria-hidden="true"></span>
                        </button>
                        <button type="button" id="cdbx-ace-font-zoomout-web" class="cdbx-btn-1">
                          <span class="dashicons dashicons-minus" aria-hidden="true"></span>
                        </button>          

                        <button type="button" id="cdbx-run-code-web" class="cdbx-btn-1" style="float:right">
                          <span class="" aria-hidden="true"></span> <b>Run</b>
                        </button>
                    </div>
                    <br><br>
                    <div id="cdbx-div-output-web" style="float:left;width:100%;text-align:left;margin-top:27px;font-size:13px;">
                        Output Appears Here ...
                    </div>
                 </div>
            </div>';

       return $div_content;
   }
    
   private function getModalContentPublic() {
      $div_content = 
            '<div id="cdbx-editor-dialog">
              <div class="cdbx-editor-div">
                <div class="cdbx-editor-div-left">
                  <div id="cdbx-compilebin-editor" class="cdbx-editor"></div>
                </div>
                <div class="cdbx-editor-div-right">
                  <div style="width:100%;float:left"> 
                    <button type="" id="cdbx-ace-theme-xcode" class="cdbx-btn-1 cdbx-ace-theme" title="Light theme">
                      <span class="dashicons dashicons-visibility" aria-hidden="true"></span>
                    </button>
                    <button type="button" id="cdbx-ace-theme-monokai" class="cdbx-btn-1 cdbx-ace-theme" title="Dark (monokai) theme">
                      <span class="dashicons dashicons-art" aria-hidden="true"></span>
                    </button>
                    <button type="button" id="cdbx-ace-theme-cobalt" class="cdbx-btn-1 cdbx-ace-theme" title="Dark (cobalt) theme">
                      <span class="dashicons dashicons-image-filter" aria-hidden="true"></span>
                    </button>
                    <button type="button" id="cdbx-ace-font-zoomin" class="cdbx-btn-1">
                      <span class="dashicons dashicons-plus" aria-hidden="true"></span>
                    </button>
                    <button type="button" id="cdbx-ace-font-zoomout" class="cdbx-btn-1">
                      <span class="dashicons dashicons-minus" aria-hidden="true"></span>
                    </button>
                    <button type="button" id="cdbx-run-code" class="cdbx-btn-1" style="float:right;">
                      <span class="" aria-hidden="true"></span><b>Run</b></span>
                    </button>    
                  </div>
                  <div class="cdbx-div-right-2" style="width:100%;">
                    <input id="cdbx-filename" class="cdbx-textbox" style="margin-top:5px;float:left;font-size:13px;" placeholder="Filename"></input><span id="cdbx-filename-ext" style="float:left;margin-top:5px;"></span>
                    <!--<button type="button" id="cdbx-code-help" class="cdbx-btn-1" style="float:right">
                      <span class="dashicons dashicons-editor-help" aria-hidden="true"></span>
                    </button>-->  
                  </div>
                  <div id="cdbx-div-output" style="float:left;width:100%;text-align:left">
                    Output Appears Here ...
                  </div>
                  <div style="width:100%">
                    <textarea id="cdbx-stdin" class="cdbx-textarea-input" style="font-size:13px;" rows="4" cols="200" placeholder="Stdin (One input element per line)"></textarea>
                    <textarea id="cdbx-cmdline" class="cdbx-textarea-input" style="font-size:13px;" rows="1" placeholder="Cmd Line Args"></textarea>
                  </div>
                </div>
              </div>
            </div>';

       return $div_content;
   }    
  
}
?>
