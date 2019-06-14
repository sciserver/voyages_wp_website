<?php
/*
Plugin Name: Equation Editor
Plugin URI: https://wordpress.org/plugins/equation-editor/
Description: Adds equation editor to wordpress TinyMCE editor.
Author: modalweb
Version: 1.5
Author URI: https://profiles.wordpress.org/modalweb
*/
if(!class_exists('mw_equation_editor')) {
	class mw_equation_editor {
		var $option;
		var $settings;
	    public function  __construct() {
              add_filter('mce_buttons', array($this, 'equation_add_button'), 0);
              add_filter('mce_external_plugins', array($this, "equation_editor_register"));
              add_action('admin_menu', array(&$this, 'mw_equation_menu_page'));
              $this->option = 'mw_equation_editor';
              $this->settings = get_option($this->option);
              register_activation_hook(__FILE__, array(&$this, 'mw_equation_install'));
        }
        public function mw_equation_install() {
                           $settings = array(
                                             'enable_eq_editor' => '1',
                                             'select_eq_editor' => 'wiris',
                                             );
                    if(!$this->settings['enable_eq_editor']) {
                        update_option($this->option, $settings);
                    }
        }
        public function mw_equation_menu_page() {
             add_menu_page(
            __( 'Equation Editor', 'equation-editor' ),
            __( 'Equation Editor', 'equation-editor' ),
               'manage_options',
            'mw_equation_editor',
            array(&$this, 'mw_equation_editor_method'),
            'dashicons-editor-underline'
            );
        }
        public function equation_add_button($buttons)
        {
          if(isset($this->settings['enable_eq_editor']) && $this->settings['enable_eq_editor'] == '1') {
            if($this->settings['select_eq_editor'] == 'latex') {
              array_push($buttons, "separator", "equation");
            } else if($this->settings['select_eq_editor'] == 'wiris') {
              array_push($buttons, 'separator', 'tiny_mce_wiris_formulaEditor', 'tiny_mce_wiris_formulaEditorChemistry');
            } else if($this->settings['select_eq_editor'] == 'both') {
                array_push($buttons, "separator", "equation");
                array_push($buttons, 'separator', 'tiny_mce_wiris_formulaEditor', 'tiny_mce_wiris_formulaEditorChemistry');
            }
            return $buttons;
          }
        }

        public function equation_editor_register($plugin_array)
        {
          if(isset($this->settings['enable_eq_editor']) && $this->settings['enable_eq_editor'] == '1') {
            if($this->settings['select_eq_editor'] == 'latex') {
                $plugin_array['equation'] = plugins_url('js/eq_editor.js', __FILE__);
            } else if($this->settings['select_eq_editor'] == 'wiris') {
               $plugin_array['tiny_mce_wiris'] = plugins_url('tiny_mce_wiris/editor_plugin.js', __FILE__);
            } else if($this->settings['select_eq_editor'] == 'both') {
                $plugin_array['equation'] = plugins_url('js/eq_editor.js', __FILE__);
                $plugin_array['tiny_mce_wiris'] = plugins_url('tiny_mce_wiris/editor_plugin.js', __FILE__);
            }
          }
            return $plugin_array;
        }
        public function mw_equation_editor_method() {
            if(is_admin() && current_user_can('manage_options')) {
                require_once('admin/mw_equation_editor.php');
            }
        }
        public function save() {
          if(isset($_POST['submit']) && wp_verify_nonce( $_POST['mw_equation_editor_nonce'], 'mw_equation_editor_action' )):
          $set = update_option( $this->option, $_POST );
          if($set){ $this->f('?page=mw_equation_editor&s=y'); } else { $this->f('?page=mw_equation_editor&s=n');}
          endif;
        }
        public function f($url) {
            echo '<script>';
            echo 'window.location.href="'.$url.'"';
            echo '</script>';
        }

    }
new mw_equation_editor;
}