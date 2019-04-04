<?php

/**
 * @link              https://www.compilebin.com
 * @since             1.0.0
 * @package           compilebin
 *
 * @wordpress-plugin
 * Plugin Name:       Code Editor and Compiler
 * Plugin URI:        https://www.compilebin.com
 * Description:       Syntax highlighter and code compiler.
 * Version:           1.4.1
 * Author:            Compilebin
 * Author URI:        https://www.compilebin.com
 * License:           GPL-2.0+
 * License URI:       http://www.gnu.org/licenses/gpl-2.0.txt
 * Text Domain:       code-editor-and-compiler
 * Domain Path:       /languages
 */

 class compilebin {

    private $adminObj;
    private $publicObj;

    public function __construct() {
       $this->init();
       register_activation_hook(__FILE__, array($this, 'compilebin_activate'));    
    }
     
    public function compilebin_activate() {
        add_option('compilebinActivated', 'Plugin-Slug');
    } 

    public function init() {
       if (is_admin()) {
          require_once plugin_dir_path( __FILE__ ) . 'admin/compilebin-admin.php';
          $adminObj = new compilebinAdmin();
       } else {
          require_once plugin_dir_path( __FILE__ ) . 'public/compilebin-public.php';
          $publicObj = new compilebinPublic();
       }
    }

 };

 new compilebin;

?>
