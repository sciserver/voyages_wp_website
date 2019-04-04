<?php
class compilebinPublic {

   private $plugin_name;
   private $plugin_version;

   public function __construct() {
      $this->plugin_name = "code-editor-and-compiler";
      $this->plugin_version = "1.4.1";
      add_action('wp_enqueue_scripts', array(&$this, 'enqueueScripts'));
      add_action('wp_enqueue_scripts', array(&$this, 'enqueueStyles'));
   }
    
   private function getDarkThemeStatus() {
      $darktheme_status = null;
      if (false === ($darktheme_status = get_transient('darktheme_status'))) {
        $darktheme_status = get_option('darktheme_status');
        set_transient('darktheme_status', $darktheme_status, YEAR_IN_SECONDS);
      }
      if ($darktheme_status == null || strlen($darktheme_status) == 0) {
        $darktheme_status = 0;  
      }   
      return $darktheme_status;
   }    

   public function enqueueScripts() {   
      wp_enqueue_script('jquery-ui-dialog');
      wp_enqueue_script('ace-js', plugins_url() . '/' . $this->plugin_name . '/ace-builds-master/src-noconflict/ace.js', array('jquery'), $this->plugin_version, false);  
      wp_enqueue_script('include-js', plugins_url() . '/' . $this->plugin_name . '/common/js/include.js', array('jquery'), $this->plugin_version, false);
      wp_enqueue_script('editor-handler-public', plugin_dir_url( __FILE__ ) . 'js/editor-handler-public.js', array( 'jquery' ), $this->plugin_version, false);
      wp_localize_script('editor-handler-public', 'cdbx_ajax_script', array('ajaxurl' => admin_url('admin-ajax.php')));
      if ($this->getDarkThemeStatus() == 0) {
        wp_enqueue_script('code-prettify-js-1', plugins_url() . '/' . $this->plugin_name . '/code-prettify-master/loader/run_prettify.js?callback=cdbx_publicInit', array('jquery'), $this->plugin_version, false);
      } else {  
        wp_enqueue_script('code-prettify-js-2', plugins_url() . '/' . $this->plugin_name . '/code-prettify-master/loader/run_prettify.js?skin=desert&callback=cdbx_publicInit', array('jquery'), $this->plugin_version, false);  
      }
      //wp_enqueue_script('code-prettify-js-1', plugins_url() . '/' . $this->plugin_name . '/code-prettify-master/loader/run_prettify.js', array('jquery'), $this->plugin_version, false);    
   }

   public function enqueueStyles() {
      wp_enqueue_style('wp-jquery-ui-dialog');
      wp_enqueue_style('editor-style', plugins_url() . '/' . $this->plugin_name .  '/common/css/editor-style.css', array(), $this->plugin_version, 'all');   
   }
  
}
?>
