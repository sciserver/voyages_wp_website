=== Compilebin ===
Contributors: rahburma
Tags: compiler, code snippet, syntax highlighter, syntax highlight, embed code snippets, code, highlight, syntax, online compiler, snippet, code editor, compiler plugin
Plugin URI: https://www.compilebin.com
Requires at least: 3.1
Tested up to: 4.9.4
Stable tag: 1.4.1
Requires PHP: 5.2.4
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.txt

An online compiler plugin which comprises of code editor and live compiler along with syntax highlighter.

== Description ==
This is a syntax highlighter plugin which also acts as an interface to the online compiler api service on cloud provided by https://www.compilebin.com. It interacts with cloud service via rest APIs i.e, submit the code and get the output. Users need to signup and get an api key which is to be updated in the plugin to use the service. Plugin contains a link for signing up for the service. There is no security concern on the web server as the task of code execution is offloaded to the cloud service. The plugin uses the following open source libraries :
1) Code prettify for syntax highlighting
2) Ace code editor
Please visit https://www.compilebin.com for more information about the service.
Note that this plugin can also be used purely as a syntax highlighter only by hiding the run button on your code snippets. This mode of usage is free of any charges. Run button will not be visible on public view.
Please report issues to support@compilebin.com
This plugin is actively maintained and we will fix the reported issues as soon as possible.

== Installation ==
1. Upload the plugin to the '/wp-content/plugins/' directory, or install the plugin through the WordPress plugins screen directly.
2. Activate the plugin through the 'Plugins' screen in WordPress.
3. Use 'Insert code' button  to launch code editor and signup on https://www.compilebin.com to get your API key.
4. You don't need any key in case you are using only syntax highlighting feature and do not want users to execute code on your website.

== Screenshots ==
1. /assets/screenshot-1.png - Editor to write, save and execute code.
2. /assets/screenshot-2.png - Insert code button on the admin page.
3. /assets/screenshot-3.png - Dialog box to update API key.
4. /assets/screenshot-4.png - Dialog box to set preferences.
5. /assets/screenshot-5.png - Web design code editor.

== Changelog ==
1.4.1
Dark theme for code snippets in public view.
Feature to enable pop up of dialog box to edit saved code with double click instead of single click.
Performance improvement.

1.3.11
Support for fullscreen code editor in public view.
Copy button to copy the code to clipboard in public view.

1.3.10
Support for highlighting selected portion of web design code in public view.
UI improvement

1.3.8
Support for highlighting selected portion of code in public view.

1.3.7
Introduced support for displaying line numbers in syntax highlighted code

1.3.6
Fixed display issue in firefox

1.3.5
Performance improvements

1.3.3
Support for syntax highlighting of languages for which compilation feature is not available.
Bug fixes.

1.3.1
UI enhancement.

1.2.4
Fixed display issue for web design code snippets.

1.2.3
Resolved notices thrown in wp_debug mode.

1.2.1
Bug Fixes.

1.2.0
Custom settings inroduced to set preferences like hiding run button, default editor, default theme and programming language.

1.1.0
Support for front-end web design code execution i.e html, css and javascript

1.0.0
First Release.
