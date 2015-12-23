<?php
/**
 * Do stuff common to all model classes
 * that extend this database class
 **/
class wpl_galaxy_wp_database {
	/**
	 * Class vars
	 **/
	protected $wpdb = null;
	protected $model = null;

	/**
	 * Make Wordpress dbase object and other
	 * models available to all model classes.
	 * Also, define database tables.
	 **/
	function __construct() {
		global $wpdb;
		$this->wpdb = $wpdb;

		$this->tables = array(
			'layerslider' => $this->wpdb->prefix . "layerslider",
			'sections' => $this->wpdb->prefix . "wpl_gwp_sections"
		);
	}

	/**
	 * Inject all models into all other models
	 * to make them callable from there
	 **/
	function inject_application_classes($model) {
		$this->model = $model;
	}
}
