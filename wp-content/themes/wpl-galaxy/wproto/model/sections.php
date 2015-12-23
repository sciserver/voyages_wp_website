<?php
	/**
   * Sections model
   **/
	class wpl_galaxy_wp_sections extends wpl_galaxy_wp_database {                     

		/**
		 * Delete a section
		 * @param int
		 **/
		function delete( $section_id ) {
			
			$table = $this->tables['sections'];
			
			return $this->wpdb->delete( $table, array( 'ID' => $section_id, 'status' => 'default' ) );
			
		}
		
		/**
		 * Get a sections by ids
		 * @param array
		 **/
		function get( $ids = array() ) {
			
			if( count( $ids ) <= 0 ) return false;

			$table = $this->tables['sections'];
			
			return $this->wpdb->get_results(' 
				SELECT * 
				FROM ' . $table . '
				WHERE ID IN (' . implode( ',', $ids ) . ') 
				ORDER BY FIELD(ID, ' . implode( ',', $ids ) . ')
			');
			
		}
		
		/**
		 * Get single section with unserialized data
		 **/
		function get_single( $id ) {
			
			$table = $this->tables['sections'];
			
			$return = array();
			
			$section = $this->wpdb->get_row(' 
				SELECT * 
				FROM ' . $table . '
				WHERE ID = ' . absint( $id ) . '
			');
			
			$return['wproto_section_content'] = array(
				'title' => $section->title,
				'subtitle' => $section->subtitle,
				'before_text' => $section->before_text,
				'after_text' => $section->after_text,
				'status' => $section->status,
				'type' => $section->type
			);
			$return['wproto_section_data'] = @unserialize( $section->data );
			
			return $return;
		}
		
		/**
		 * Add new section
		 * @param array
		 **/	
		function add( $data ) {
			
			$table = $this->tables['sections'];
			
			$this->wpdb->insert( 
				$table, 
				$data 
			);
			
			return $this->wpdb->insert_id;
		}
		
		/**
		 * Update section settings
		 * @param array
		 **/	
		function update( $data ) {
			
			$table = $this->tables['sections'];
			$id = isset( $data['ID'] ) ? absint( $data['ID'] ) : 0;
			
			$this->wpdb->update( 
				$table, 
				array( 
					'title' => $data['title'],
					'subtitle' => $data['subtitle'],
					'before_text' => $data['before_text'],
					'after_text' => $data['after_text'],
					'data' => $data['data'],
				), 
				array( 'ID' => $id ) 
			);
			
		}

	}