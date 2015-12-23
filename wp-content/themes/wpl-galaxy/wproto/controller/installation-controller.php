<?php
/**
 * Installation Controller
 **/
class wpl_galaxy_wp_installation_controller extends wpl_galaxy_wp_admin_controller {
	/**
	 * Below ALL add_action() and add_filter() hooks that
	 * get served by the methods of this controller
	 **/
	function __construct() {
		// Security: Admin only
		if ( is_admin() ) {
			add_action( 'init', array( $this, 'check_first_activation'));
			//add_action( 'after_switch_theme', array( $this, 'activation_hook' ));
			add_action( 'switch_theme', array( $this, 'deactivation_hook' ));	
			add_action( 'wp_ajax_wproto_install_sample_data', array( $this, 'ajax_install_sample_data' ) );
		}
	}

	/**
	 * Check for first activation
	 **/
	function check_first_activation() {
		global $pagenow;
		// first theme activation fix
		if ( isset( $_GET['activated'] ) && $pagenow == 'themes.php' ) {
			$this->activation_hook();
		}
	}

	/**
	 * install hook
	 **/
	function activation_hook() {
		global $wp_version;
		
		if( version_compare( PHP_VERSION, '5.3.0', '<' ) ) {
			wp_die( sprintf( __( 'Cannot install the theme. PHP version > 5.3.0 is required. Your PHP version: %s', 'wproto' ), PHP_VERSION ) );
		}
		
		if( version_compare( $wp_version, '3.6', '<' ) ) {
			wp_die( sprintf( __( 'Cannot activate the theme. WordPress version > 3.6 is required. Your WordPress version: %s', 'wproto' ), $wp_version ) );
		}
		
		$this->model->installation->install();		
		
		flush_rewrite_rules( true );
		wp_cache_flush();
		
	}		
	
	/**
	 * deactivation hook
	 **/
	function deactivation_hook() {
		$this->model->installation->uninstall();
		
		flush_rewrite_rules( true );
		
	}
	
	/**
	 * Install sample data
	 **/
	function ajax_install_sample_data() {
		global $wpl_galaxy_wp;
		
		@set_time_limit(300000);
		
		/**
		 * Insert sample images
		 **/
		
		require_once( ABSPATH . 'wp-admin/includes/image.php' );
		
		$wp_upload_dir = wp_upload_dir();
		
		$sample_images = array(
			WPROTO_THEME_DIR . '/images/admin/sample-1.jpg',
			WPROTO_THEME_DIR . '/images/admin/sample-2.jpg',
			WPROTO_THEME_DIR . '/images/admin/sample-3.jpg'
		); 
		
		$sample_images_ids = array();
		
		foreach( $sample_images as $k=>$image ) {
			
			$moved_file = $wp_upload_dir['path'] . "/wpl-sample-" . uniqid() . '.jpg';
			
			if ( copy( $image, $moved_file ) ) {
				
				$wp_filetype = wp_check_filetype(basename( $moved_file ), null );
				
				$attach_id = wp_insert_attachment( array(
     			'guid' => $wp_upload_dir['url'] . '/' . basename( $moved_file ), 
     			'post_mime_type' => $wp_filetype['type'],
     			'post_title' => preg_replace( '/\.[^.]+$/', '', basename( $moved_file ) ),
     			'post_content' => '',
     			'post_status' => 'inherit'
				), $moved_file );
				
				$sample_images_ids[] = $attach_id;
				
				$attach_data = wp_generate_attachment_metadata( $attach_id, $moved_file );
  			wp_update_attachment_metadata( $attach_id, $attach_data );
				
			}
			
		}
		
		/**
		 * Insert sample blog posts
		 **/
		$sample_posts = array(
			'titles' => array(
				'Aliquam tincidunt lacus tellus',
				'Some another post',
				'Pellentesque habitant morbi tristique',
				'Lorem ipsum dolor',
				'Nunc vitae turpis dignissim ante dictum eleifend',
				'Praesent nec tincidunt lacus',
				'Suspendisse dapibus lacus',
				'Aenean sed fringilla libero',
				'There are many kinds of variations of passages',
				'Plane fly high over the ground',
				'Quisque tincidunt eu ante',
				'The generated Lorem Ipsum is therefore always',
				'Lorem ipsum dolor sit amet',
				'Many kinds of variations of passages'
			),
			'content' => array(
				'<p>There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don\'t look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn\'t anything embarrassing hidden in the middle of text.</p><p>All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable.</p><p>The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc. There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don\'t look even slightly believable.</p>',
				'<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p>',
				'<p>Phasellus quam ligula, feugiat in dignissim at, porttitor et sapien. Duis porttitor orci at libero egestas, vel viverra urna ullamcorper. Ut malesuada, felis sed interdum suscipit, metus neque vehicula nisi, quis sagittis purus dolor bibendum est. Nullam mollis eu urna quis eleifend. Ut ullamcorper risus non tellus consectetur auctor sed in nisl. Morbi nec purus vehicula, pellentesque elit condimentum, egestas lacus. Nullam mi est, imperdiet sed elit nec, hendrerit feugiat ligula. Nunc ac leo porttitor, lobortis nisi quis, eleifend libero. Curabitur vulputate a nunc vel volutpat. Proin gravida arcu odio, eget lacinia odio gravida non. Aliquam erat volutpat. Mauris non interdum felis. Morbi sodales felis quam, sed tristique ante blandit sit amet. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.</p>',
				'<p>Pellentesque ligula lacus, tempor eget tincidunt ut, hendrerit et mauris. Sed venenatis dolor a mollis facilisis. Pellentesque porttitor turpis at nisl tempus ultrices. Integer tincidunt varius felis, nec elementum arcu facilisis sit amet. Morbi semper augue nec turpis fringilla auctor. Fusce felis purus, dapibus in tincidunt id, aliquet pulvinar nunc. Morbi lobortis, nunc a tempus posuere, lacus augue eleifend nulla, quis tempor dolor orci id metus. Nam auctor feugiat mi eget malesuada. Praesent consequat orci odio, eu lacinia risus tincidunt vitae. Ut aliquet eu ligula in molestie.</p>',
				'<p>Nunc in est aliquet, faucibus erat sed, pellentesque quam. Sed fringilla pellentesque purus, tristique tincidunt justo semper vel. Donec eu metus posuere, interdum nisi ac, tincidunt lacus. Duis nisi diam, ullamcorper quis elementum quis, posuere fermentum tellus. Nulla pretium leo vitae urna consectetur, sed interdum diam consectetur. Curabitur neque est, commodo a est id, aliquam dictum felis. Suspendisse arcu velit, imperdiet in diam eget, pellentesque semper purus. Nulla eleifend risus dignissim malesuada gravida.</p><p>Pellentesque ligula lacus, tempor eget tincidunt ut, hendrerit et mauris. Sed venenatis dolor a mollis facilisis. Pellentesque porttitor turpis at nisl tempus ultrices. Integer tincidunt varius felis, nec elementum arcu facilisis sit amet. Morbi semper augue nec turpis fringilla auctor. Fusce felis purus, dapibus in tincidunt id, aliquet pulvinar nunc. Morbi lobortis, nunc a tempus posuere, lacus augue eleifend nulla, quis tempor dolor orci id metus. Nam auctor feugiat mi eget malesuada. Praesent consequat orci odio, eu lacinia risus tincidunt vitae. Ut aliquet eu ligula in molestie.</p>',
				'<p>Nulla scelerisque, ligula quis eleifend faucibus, quam purus bibendum elit, eu condimentum libero quam sit amet magna. Nunc malesuada elit eget ipsum auctor elementum. Aliquam euismod dignissim arcu, et tempus ligula mollis vel. Cras consectetur vitae sem at vulputate. Nunc viverra mi massa, in rhoncus tortor auctor eu. Fusce eget lorem iaculis dolor suscipit luctus eget vitae ipsum. Suspendisse placerat, est fermentum venenatis dignissim, magna nibh vestibulum eros, a egestas neque enim a dolor. Pellentesque at eleifend ligula. Integer eget urna pretium, commodo nunc nec, pulvinar tortor. Phasellus vel mattis quam. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras luctus varius libero, dapibus luctus tortor bibendum eu. Cras quis accumsan lorem. Donec non erat at sapien congue egestas.</p>',
				'<p>Sed sollicitudin vitae massa a aliquet. Vestibulum consectetur quam ornare odio iaculis, in lobortis mauris ullamcorper. Praesent blandit eros et nisi fermentum pretium. Morbi turpis metus, faucibus vitae dapibus id, tempus vel diam. In rhoncus libero ut tellus ultrices, eget luctus mi tincidunt. Etiam magna dui, accumsan pretium nunc eget, facilisis luctus odio. Etiam eget lectus eget libero gravida vestibulum. Sed sagittis gravida lorem ut ullamcorper. Etiam gravida mauris at bibendum faucibus. Curabitur tempor vel est non aliquam. Proin non nunc lobortis, tristique massa sed, pharetra urna. Donec rhoncus orci nulla, et faucibus mauris commodo ut. Suspendisse risus mauris, posuere a est eget, ultrices ultrices metus. Duis purus sapien, molestie in mi vel, fermentum congue nulla.</p>',
				'<p>There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don\'t look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn\'t anything embarrassing hidden in the middle of text.</p><p>All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable.</p><p>The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc. There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don\'t look even slightly believable.</p>',
				'<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p>',
				'<p>Phasellus quam ligula, feugiat in dignissim at, porttitor et sapien. Duis porttitor orci at libero egestas, vel viverra urna ullamcorper. Ut malesuada, felis sed interdum suscipit, metus neque vehicula nisi, quis sagittis purus dolor bibendum est. Nullam mollis eu urna quis eleifend. Ut ullamcorper risus non tellus consectetur auctor sed in nisl. Morbi nec purus vehicula, pellentesque elit condimentum, egestas lacus. Nullam mi est, imperdiet sed elit nec, hendrerit feugiat ligula. Nunc ac leo porttitor, lobortis nisi quis, eleifend libero. Curabitur vulputate a nunc vel volutpat. Proin gravida arcu odio, eget lacinia odio gravida non. Aliquam erat volutpat. Mauris non interdum felis. Morbi sodales felis quam, sed tristique ante blandit sit amet. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.</p>',
				'<p>Pellentesque ligula lacus, tempor eget tincidunt ut, hendrerit et mauris. Sed venenatis dolor a mollis facilisis. Pellentesque porttitor turpis at nisl tempus ultrices. Integer tincidunt varius felis, nec elementum arcu facilisis sit amet. Morbi semper augue nec turpis fringilla auctor. Fusce felis purus, dapibus in tincidunt id, aliquet pulvinar nunc. Morbi lobortis, nunc a tempus posuere, lacus augue eleifend nulla, quis tempor dolor orci id metus. Nam auctor feugiat mi eget malesuada. Praesent consequat orci odio, eu lacinia risus tincidunt vitae. Ut aliquet eu ligula in molestie.</p>',
				'<p>Nunc in est aliquet, faucibus erat sed, pellentesque quam. Sed fringilla pellentesque purus, tristique tincidunt justo semper vel. Donec eu metus posuere, interdum nisi ac, tincidunt lacus. Duis nisi diam, ullamcorper quis elementum quis, posuere fermentum tellus. Nulla pretium leo vitae urna consectetur, sed interdum diam consectetur. Curabitur neque est, commodo a est id, aliquam dictum felis. Suspendisse arcu velit, imperdiet in diam eget, pellentesque semper purus. Nulla eleifend risus dignissim malesuada gravida.</p><p>Pellentesque ligula lacus, tempor eget tincidunt ut, hendrerit et mauris. Sed venenatis dolor a mollis facilisis. Pellentesque porttitor turpis at nisl tempus ultrices. Integer tincidunt varius felis, nec elementum arcu facilisis sit amet. Morbi semper augue nec turpis fringilla auctor. Fusce felis purus, dapibus in tincidunt id, aliquet pulvinar nunc. Morbi lobortis, nunc a tempus posuere, lacus augue eleifend nulla, quis tempor dolor orci id metus. Nam auctor feugiat mi eget malesuada. Praesent consequat orci odio, eu lacinia risus tincidunt vitae. Ut aliquet eu ligula in molestie.</p>',
				'<p>Nulla scelerisque, ligula quis eleifend faucibus, quam purus bibendum elit, eu condimentum libero quam sit amet magna. Nunc malesuada elit eget ipsum auctor elementum. Aliquam euismod dignissim arcu, et tempus ligula mollis vel. Cras consectetur vitae sem at vulputate. Nunc viverra mi massa, in rhoncus tortor auctor eu. Fusce eget lorem iaculis dolor suscipit luctus eget vitae ipsum. Suspendisse placerat, est fermentum venenatis dignissim, magna nibh vestibulum eros, a egestas neque enim a dolor. Pellentesque at eleifend ligula. Integer eget urna pretium, commodo nunc nec, pulvinar tortor. Phasellus vel mattis quam. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras luctus varius libero, dapibus luctus tortor bibendum eu. Cras quis accumsan lorem. Donec non erat at sapien congue egestas.</p>',
				'<p>Sed sollicitudin vitae massa a aliquet. Vestibulum consectetur quam ornare odio iaculis, in lobortis mauris ullamcorper. Praesent blandit eros et nisi fermentum pretium. Morbi turpis metus, faucibus vitae dapibus id, tempus vel diam. In rhoncus libero ut tellus ultrices, eget luctus mi tincidunt. Etiam magna dui, accumsan pretium nunc eget, facilisis luctus odio. Etiam eget lectus eget libero gravida vestibulum. Sed sagittis gravida lorem ut ullamcorper. Etiam gravida mauris at bibendum faucibus. Curabitur tempor vel est non aliquam. Proin non nunc lobortis, tristique massa sed, pharetra urna. Donec rhoncus orci nulla, et faucibus mauris commodo ut. Suspendisse risus mauris, posuere a est eget, ultrices ultrices metus. Duis purus sapien, molestie in mi vel, fermentum congue nulla.</p>'
			)
		);
		
		for( $i=0; $i<count( $sample_posts['titles'] ); $i++ ) {
			
			$post_data = array(
				'post_title'    => $sample_posts['titles'][$i],
				'post_content'  => $sample_posts['content'][$i],
				'post_status'   => 'publish',
				'post_type'			=> 'post'
			);
			
			$post_id = wp_insert_post( $post_data );
			
			set_post_thumbnail( $post_id, $sample_images_ids[ rand( 0, count( $sample_images_ids ) - 1)] );
			
		}
		
		/**
		 * Insert sample video posts
		 **/
		$sample_videos = array(
			'titles' => array(
				'The Galaxy',
				'All Alone in the Night &ndash; Time-lapse footage of the Earth as seen from the ISS',
				'Earths motion around the Sun, not as simple as I thought',
				'Stunning Timelapse of Earth from the International Space Station',
				'Planet Earth',
				'A Space Journey',
				'Earth from Space. Videos and Photos of Planet Earth in Space',
				'What is Space?',
				'National Geographic &ndash; Monster Black Holes',
				'The Largest Black Holes in the Universe',
				'Universe: Journey from Earth to the Edge of the Cosmos',
				'Vivamus adipiscing malesuada imperdiet'
			),
			'content' => array(
				'<p>There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don\'t look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn\'t anything embarrassing hidden in the middle of text.</p><p>All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable.</p><p>The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc. There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don\'t look even slightly believable.</p>',
				'<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p>',
				'<p>Phasellus quam ligula, feugiat in dignissim at, porttitor et sapien. Duis porttitor orci at libero egestas, vel viverra urna ullamcorper. Ut malesuada, felis sed interdum suscipit, metus neque vehicula nisi, quis sagittis purus dolor bibendum est. Nullam mollis eu urna quis eleifend. Ut ullamcorper risus non tellus consectetur auctor sed in nisl. Morbi nec purus vehicula, pellentesque elit condimentum, egestas lacus. Nullam mi est, imperdiet sed elit nec, hendrerit feugiat ligula. Nunc ac leo porttitor, lobortis nisi quis, eleifend libero. Curabitur vulputate a nunc vel volutpat. Proin gravida arcu odio, eget lacinia odio gravida non. Aliquam erat volutpat. Mauris non interdum felis. Morbi sodales felis quam, sed tristique ante blandit sit amet. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.</p>',
				'<p>Pellentesque ligula lacus, tempor eget tincidunt ut, hendrerit et mauris. Sed venenatis dolor a mollis facilisis. Pellentesque porttitor turpis at nisl tempus ultrices. Integer tincidunt varius felis, nec elementum arcu facilisis sit amet. Morbi semper augue nec turpis fringilla auctor. Fusce felis purus, dapibus in tincidunt id, aliquet pulvinar nunc. Morbi lobortis, nunc a tempus posuere, lacus augue eleifend nulla, quis tempor dolor orci id metus. Nam auctor feugiat mi eget malesuada. Praesent consequat orci odio, eu lacinia risus tincidunt vitae. Ut aliquet eu ligula in molestie.</p>',
				'<p>Nunc in est aliquet, faucibus erat sed, pellentesque quam. Sed fringilla pellentesque purus, tristique tincidunt justo semper vel. Donec eu metus posuere, interdum nisi ac, tincidunt lacus. Duis nisi diam, ullamcorper quis elementum quis, posuere fermentum tellus. Nulla pretium leo vitae urna consectetur, sed interdum diam consectetur. Curabitur neque est, commodo a est id, aliquam dictum felis. Suspendisse arcu velit, imperdiet in diam eget, pellentesque semper purus. Nulla eleifend risus dignissim malesuada gravida.</p><p>Pellentesque ligula lacus, tempor eget tincidunt ut, hendrerit et mauris. Sed venenatis dolor a mollis facilisis. Pellentesque porttitor turpis at nisl tempus ultrices. Integer tincidunt varius felis, nec elementum arcu facilisis sit amet. Morbi semper augue nec turpis fringilla auctor. Fusce felis purus, dapibus in tincidunt id, aliquet pulvinar nunc. Morbi lobortis, nunc a tempus posuere, lacus augue eleifend nulla, quis tempor dolor orci id metus. Nam auctor feugiat mi eget malesuada. Praesent consequat orci odio, eu lacinia risus tincidunt vitae. Ut aliquet eu ligula in molestie.</p>',
				'<p>Nulla scelerisque, ligula quis eleifend faucibus, quam purus bibendum elit, eu condimentum libero quam sit amet magna. Nunc malesuada elit eget ipsum auctor elementum. Aliquam euismod dignissim arcu, et tempus ligula mollis vel. Cras consectetur vitae sem at vulputate. Nunc viverra mi massa, in rhoncus tortor auctor eu. Fusce eget lorem iaculis dolor suscipit luctus eget vitae ipsum. Suspendisse placerat, est fermentum venenatis dignissim, magna nibh vestibulum eros, a egestas neque enim a dolor. Pellentesque at eleifend ligula. Integer eget urna pretium, commodo nunc nec, pulvinar tortor. Phasellus vel mattis quam. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras luctus varius libero, dapibus luctus tortor bibendum eu. Cras quis accumsan lorem. Donec non erat at sapien congue egestas.</p>',
				'<p>Sed sollicitudin vitae massa a aliquet. Vestibulum consectetur quam ornare odio iaculis, in lobortis mauris ullamcorper. Praesent blandit eros et nisi fermentum pretium. Morbi turpis metus, faucibus vitae dapibus id, tempus vel diam. In rhoncus libero ut tellus ultrices, eget luctus mi tincidunt. Etiam magna dui, accumsan pretium nunc eget, facilisis luctus odio. Etiam eget lectus eget libero gravida vestibulum. Sed sagittis gravida lorem ut ullamcorper. Etiam gravida mauris at bibendum faucibus. Curabitur tempor vel est non aliquam. Proin non nunc lobortis, tristique massa sed, pharetra urna. Donec rhoncus orci nulla, et faucibus mauris commodo ut. Suspendisse risus mauris, posuere a est eget, ultrices ultrices metus. Duis purus sapien, molestie in mi vel, fermentum congue nulla.</p>',
				'<p>There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don\'t look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn\'t anything embarrassing hidden in the middle of text.</p><p>All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable.</p><p>The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc. There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don\'t look even slightly believable.</p>',
				'<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p>',
				'<p>Phasellus quam ligula, feugiat in dignissim at, porttitor et sapien. Duis porttitor orci at libero egestas, vel viverra urna ullamcorper. Ut malesuada, felis sed interdum suscipit, metus neque vehicula nisi, quis sagittis purus dolor bibendum est. Nullam mollis eu urna quis eleifend. Ut ullamcorper risus non tellus consectetur auctor sed in nisl. Morbi nec purus vehicula, pellentesque elit condimentum, egestas lacus. Nullam mi est, imperdiet sed elit nec, hendrerit feugiat ligula. Nunc ac leo porttitor, lobortis nisi quis, eleifend libero. Curabitur vulputate a nunc vel volutpat. Proin gravida arcu odio, eget lacinia odio gravida non. Aliquam erat volutpat. Mauris non interdum felis. Morbi sodales felis quam, sed tristique ante blandit sit amet. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.</p>',
				'<p>Pellentesque ligula lacus, tempor eget tincidunt ut, hendrerit et mauris. Sed venenatis dolor a mollis facilisis. Pellentesque porttitor turpis at nisl tempus ultrices. Integer tincidunt varius felis, nec elementum arcu facilisis sit amet. Morbi semper augue nec turpis fringilla auctor. Fusce felis purus, dapibus in tincidunt id, aliquet pulvinar nunc. Morbi lobortis, nunc a tempus posuere, lacus augue eleifend nulla, quis tempor dolor orci id metus. Nam auctor feugiat mi eget malesuada. Praesent consequat orci odio, eu lacinia risus tincidunt vitae. Ut aliquet eu ligula in molestie.</p>',
				'<p>Nunc in est aliquet, faucibus erat sed, pellentesque quam. Sed fringilla pellentesque purus, tristique tincidunt justo semper vel. Donec eu metus posuere, interdum nisi ac, tincidunt lacus. Duis nisi diam, ullamcorper quis elementum quis, posuere fermentum tellus. Nulla pretium leo vitae urna consectetur, sed interdum diam consectetur. Curabitur neque est, commodo a est id, aliquam dictum felis. Suspendisse arcu velit, imperdiet in diam eget, pellentesque semper purus. Nulla eleifend risus dignissim malesuada gravida.</p><p>Pellentesque ligula lacus, tempor eget tincidunt ut, hendrerit et mauris. Sed venenatis dolor a mollis facilisis. Pellentesque porttitor turpis at nisl tempus ultrices. Integer tincidunt varius felis, nec elementum arcu facilisis sit amet. Morbi semper augue nec turpis fringilla auctor. Fusce felis purus, dapibus in tincidunt id, aliquet pulvinar nunc. Morbi lobortis, nunc a tempus posuere, lacus augue eleifend nulla, quis tempor dolor orci id metus. Nam auctor feugiat mi eget malesuada. Praesent consequat orci odio, eu lacinia risus tincidunt vitae. Ut aliquet eu ligula in molestie.</p>'
			),
			'custom_fields' => array(
				array(
					'video_width' => '640',
					'video_height' => '480',
					'player_code' => 'http://player.vimeo.com/video/19940361',
					'thumbnail_small' => 'http://b.vimeocdn.com/ts/126/981/126981413_100.jpg',
					'thumbnail_medium' => 'http://b.vimeocdn.com/ts/126/981/126981413_200.jpg',
					'thumbnail_big' => 'http://b.vimeocdn.com/ts/126/981/126981413_640.jpg',
					'title' => 'Galaxy',
					'type' => 'vimeo'
				),
				array(
					'video_width' => '640',
					'video_height' => '480',
					'player_code' => 'http://www.youtube.com/embed/FG0fTKAqZ5g',
					'thumbnail_small' => 'http://i1.ytimg.com/vi/FG0fTKAqZ5g/1.jpg',
					'thumbnail_medium' => 'http://i1.ytimg.com/vi/FG0fTKAqZ5g/0.jpg',
					'thumbnail_big' => 'http://i1.ytimg.com/vi/FG0fTKAqZ5g/0.jpg',
					'title' => 'Galaxy',
					'type' => 'youtube'
				),
				array(
					'video_width' => '640',
					'video_height' => '480',
					'player_code' => 'http://www.youtube.com/embed/82p-DYgGFjI',
					'thumbnail_small' => 'http://i1.ytimg.com/vi/82p-DYgGFjI/1.jpg',
					'thumbnail_medium' => 'http://i1.ytimg.com/vi/82p-DYgGFjI/0.jpg',
					'thumbnail_big' => 'http://i1.ytimg.com/vi/82p-DYgGFjI/0.jpg',
					'title' => 'Earths motion around the Sun, not as simple as I thought',
					'type' => 'youtube'
				),
				array(
					'video_width' => '640',
					'video_height' => '480',
					'player_code' => 'http://www.youtube.com/embed/GPj8D5KaPVU',
					'thumbnail_small' => 'http://i1.ytimg.com/vi/GPj8D5KaPVU/1.jpg',
					'thumbnail_medium' => 'http://i1.ytimg.com/vi/GPj8D5KaPVU/0.jpg',
					'thumbnail_big' => 'http://i1.ytimg.com/vi/GPj8D5KaPVU/0.jpg',
					'title' => 'Stunning Timelapse of Earth from the International Space Station',
					'type' => 'youtube'
				),
				array(
					'video_width' => '640',
					'video_height' => '480',
					'player_code' => 'http://www.youtube.com/embed/6v2L2UGZJAM',
					'thumbnail_small' => 'http://i1.ytimg.com/vi/6v2L2UGZJAM/1.jpg',
					'thumbnail_medium' => 'http://i1.ytimg.com/vi/6v2L2UGZJAM/0.jpg',
					'thumbnail_big' => 'http://i1.ytimg.com/vi/6v2L2UGZJAM/0.jpg',
					'title' => 'Planet Earth: Amazing nature scenery (1080p HD)',
					'type' => 'youtube'
				),
				array(
					'video_width' => '640',
					'video_height' => '480',
					'player_code' => 'http://www.youtube.com/embed/Un5SEJ8MyPc',
					'thumbnail_small' => 'http://i1.ytimg.com/vi/Un5SEJ8MyPc/1.jpg',
					'thumbnail_medium' => 'http://i1.ytimg.com/vi/Un5SEJ8MyPc/0.jpg',
					'thumbnail_big' => 'http://i1.ytimg.com/vi/Un5SEJ8MyPc/0.jpg',
					'title' => 'A Space Journey (HD)',
					'type' => 'youtube'
				),
				array(
					'video_width' => '640',
					'video_height' => '480',
					'player_code' => 'http://www.youtube.com/embed/MGRY-yFxZus',
					'thumbnail_small' => 'http://i1.ytimg.com/vi/MGRY-yFxZus/1.jpg',
					'thumbnail_medium' => 'http://i1.ytimg.com/vi/MGRY-yFxZus/0.jpg',
					'thumbnail_big' => 'http://i1.ytimg.com/vi/MGRY-yFxZus/0.jpg',
					'title' => 'Earth from Space. Videos and Photos of Planet Earth in Space',
					'type' => 'youtube'
				),
				array(
					'video_width' => '640',
					'video_height' => '480',
					'player_code' => 'http://www.youtube.com/embed/5iZ1-csQFUA',
					'thumbnail_small' => 'http://i1.ytimg.com/vi/5iZ1-csQFUA/1.jpg',
					'thumbnail_medium' => 'http://i1.ytimg.com/vi/5iZ1-csQFUA/0.jpg',
					'thumbnail_big' => 'http://i1.ytimg.com/vi/5iZ1-csQFUA/0.jpg',
					'title' => '1. What is Space?',
					'type' => 'youtube'
				),
				array(
					'video_width' => '640',
					'video_height' => '480',
					'player_code' => 'http://www.youtube.com/embed/MlsljXCFcRc',
					'thumbnail_small' => 'http://i1.ytimg.com/vi/MlsljXCFcRc/1.jpg',
					'thumbnail_medium' => 'http://i1.ytimg.com/vi/MlsljXCFcRc/0.jpg',
					'thumbnail_big' => 'http://i1.ytimg.com/vi/MlsljXCFcRc/0.jpg',
					'title' => 'National Geographic - Monster Black Holes',
					'type' => 'youtube'
				),
				array(
					'video_width' => '640',
					'video_height' => '480',
					'player_code' => 'http://www.youtube.com/embed/xp-8HysWkxw',
					'thumbnail_small' => 'http://i1.ytimg.com/vi/xp-8HysWkxw/1.jpg',
					'thumbnail_medium' => 'http://i1.ytimg.com/vi/xp-8HysWkxw/0.jpg',
					'thumbnail_big' => 'http://i1.ytimg.com/vi/xp-8HysWkxw/0.jpg',
					'title' => 'The Largest Black Holes in the Universe',
					'type' => 'youtube'
				),
				array(
					'video_width' => '640',
					'video_height' => '480',
					'player_code' => 'http://www.youtube.com/embed/EIxAPFYDsnQ',
					'thumbnail_small' => 'http://i1.ytimg.com/vi/EIxAPFYDsnQ/1.jpg',
					'thumbnail_medium' => 'http://i1.ytimg.com/vi/EIxAPFYDsnQ/0.jpg',
					'thumbnail_big' => 'http://i1.ytimg.com/vi/EIxAPFYDsnQ/0.jpg',
					'title' => 'Universe: Journey from Earth to the Edge of the Cosmos',
					'type' => 'youtube'
				),
				array(
					'video_width' => '640',
					'video_height' => '480',
					'player_code' => 'http://www.youtube.com/embed/7loDuK4kZwU',
					'thumbnail_small' => 'http://i1.ytimg.com/vi/7loDuK4kZwU/1.jpg',
					'thumbnail_medium' => 'http://i1.ytimg.com/vi/7loDuK4kZwU/0.jpg',
					'thumbnail_big' => 'http://i1.ytimg.com/vi/7loDuK4kZwU/0.jpg',
					'title' => 'BEAUTIFUL SPACE VIDEO - An Unforgettable Trip',
					'type' => 'youtube'
				)
			)
		);
		
		for( $i=0; $i<count( $sample_videos['titles'] ); $i++ ) {
			
			$post_data = array(
				'post_title'    => $sample_videos['titles'][$i],
				'post_content'  => $sample_videos['content'][$i],
				'post_status'   => 'publish',
				'post_type'			=> 'wproto_video'
			);
			
			$post_id = wp_insert_post( $post_data );
			
			// insert custom fields
			foreach( $sample_videos['custom_fields'][$i] as $k=>$v ) {
				update_post_meta( $post_id, $k, $v );
			}
			
		}
		
		/**
		 * Insert sample photoalbums posts
		 **/
		$sample_photoalbums = array(
			'titles' => array(
				'Lorem ipsum dolor',
				'Nunc feugiat, lectus eget vestibulum',
				'Vivamus adipiscing malesuada',
				'Pellentesque risus nisi, vestibulum',
				'Morbi felis diam, ullamcorper sit amet',
				'Donec quis feugiat nisi. Mauris ut pellentesque tellus',
				'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
				'Morbi felis diam, ullamcorper sit amet massa non',
				'Sed vel dolor pulvinar, viverra',
				'Vivamus adipiscing malesuada imperdiet',
				'Plane fly high over the ground and seas',
				'Plane fly high over the ground and seas',
				'Lorem ipsum dolor sit amet, consectetur adipiscing elit'
			),
			'content' => array(
				'<p>There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don\'t look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn\'t anything embarrassing hidden in the middle of text.</p><p>All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable.</p><p>The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc. There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don\'t look even slightly believable.</p>',
				'<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p>',
				'<p>Phasellus quam ligula, feugiat in dignissim at, porttitor et sapien. Duis porttitor orci at libero egestas, vel viverra urna ullamcorper. Ut malesuada, felis sed interdum suscipit, metus neque vehicula nisi, quis sagittis purus dolor bibendum est. Nullam mollis eu urna quis eleifend. Ut ullamcorper risus non tellus consectetur auctor sed in nisl. Morbi nec purus vehicula, pellentesque elit condimentum, egestas lacus. Nullam mi est, imperdiet sed elit nec, hendrerit feugiat ligula. Nunc ac leo porttitor, lobortis nisi quis, eleifend libero. Curabitur vulputate a nunc vel volutpat. Proin gravida arcu odio, eget lacinia odio gravida non. Aliquam erat volutpat. Mauris non interdum felis. Morbi sodales felis quam, sed tristique ante blandit sit amet. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.</p>',
				'<p>Pellentesque ligula lacus, tempor eget tincidunt ut, hendrerit et mauris. Sed venenatis dolor a mollis facilisis. Pellentesque porttitor turpis at nisl tempus ultrices. Integer tincidunt varius felis, nec elementum arcu facilisis sit amet. Morbi semper augue nec turpis fringilla auctor. Fusce felis purus, dapibus in tincidunt id, aliquet pulvinar nunc. Morbi lobortis, nunc a tempus posuere, lacus augue eleifend nulla, quis tempor dolor orci id metus. Nam auctor feugiat mi eget malesuada. Praesent consequat orci odio, eu lacinia risus tincidunt vitae. Ut aliquet eu ligula in molestie.</p>',
				'<p>Nunc in est aliquet, faucibus erat sed, pellentesque quam. Sed fringilla pellentesque purus, tristique tincidunt justo semper vel. Donec eu metus posuere, interdum nisi ac, tincidunt lacus. Duis nisi diam, ullamcorper quis elementum quis, posuere fermentum tellus. Nulla pretium leo vitae urna consectetur, sed interdum diam consectetur. Curabitur neque est, commodo a est id, aliquam dictum felis. Suspendisse arcu velit, imperdiet in diam eget, pellentesque semper purus. Nulla eleifend risus dignissim malesuada gravida.</p><p>Pellentesque ligula lacus, tempor eget tincidunt ut, hendrerit et mauris. Sed venenatis dolor a mollis facilisis. Pellentesque porttitor turpis at nisl tempus ultrices. Integer tincidunt varius felis, nec elementum arcu facilisis sit amet. Morbi semper augue nec turpis fringilla auctor. Fusce felis purus, dapibus in tincidunt id, aliquet pulvinar nunc. Morbi lobortis, nunc a tempus posuere, lacus augue eleifend nulla, quis tempor dolor orci id metus. Nam auctor feugiat mi eget malesuada. Praesent consequat orci odio, eu lacinia risus tincidunt vitae. Ut aliquet eu ligula in molestie.</p>',
				'<p>Nulla scelerisque, ligula quis eleifend faucibus, quam purus bibendum elit, eu condimentum libero quam sit amet magna. Nunc malesuada elit eget ipsum auctor elementum. Aliquam euismod dignissim arcu, et tempus ligula mollis vel. Cras consectetur vitae sem at vulputate. Nunc viverra mi massa, in rhoncus tortor auctor eu. Fusce eget lorem iaculis dolor suscipit luctus eget vitae ipsum. Suspendisse placerat, est fermentum venenatis dignissim, magna nibh vestibulum eros, a egestas neque enim a dolor. Pellentesque at eleifend ligula. Integer eget urna pretium, commodo nunc nec, pulvinar tortor. Phasellus vel mattis quam. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras luctus varius libero, dapibus luctus tortor bibendum eu. Cras quis accumsan lorem. Donec non erat at sapien congue egestas.</p>',
				'<p>Sed sollicitudin vitae massa a aliquet. Vestibulum consectetur quam ornare odio iaculis, in lobortis mauris ullamcorper. Praesent blandit eros et nisi fermentum pretium. Morbi turpis metus, faucibus vitae dapibus id, tempus vel diam. In rhoncus libero ut tellus ultrices, eget luctus mi tincidunt. Etiam magna dui, accumsan pretium nunc eget, facilisis luctus odio. Etiam eget lectus eget libero gravida vestibulum. Sed sagittis gravida lorem ut ullamcorper. Etiam gravida mauris at bibendum faucibus. Curabitur tempor vel est non aliquam. Proin non nunc lobortis, tristique massa sed, pharetra urna. Donec rhoncus orci nulla, et faucibus mauris commodo ut. Suspendisse risus mauris, posuere a est eget, ultrices ultrices metus. Duis purus sapien, molestie in mi vel, fermentum congue nulla.</p>',
				'<p>There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don\'t look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn\'t anything embarrassing hidden in the middle of text.</p><p>All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable.</p><p>The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc. There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don\'t look even slightly believable.</p>',
				'<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p>',
				'<p>Phasellus quam ligula, feugiat in dignissim at, porttitor et sapien. Duis porttitor orci at libero egestas, vel viverra urna ullamcorper. Ut malesuada, felis sed interdum suscipit, metus neque vehicula nisi, quis sagittis purus dolor bibendum est. Nullam mollis eu urna quis eleifend. Ut ullamcorper risus non tellus consectetur auctor sed in nisl. Morbi nec purus vehicula, pellentesque elit condimentum, egestas lacus. Nullam mi est, imperdiet sed elit nec, hendrerit feugiat ligula. Nunc ac leo porttitor, lobortis nisi quis, eleifend libero. Curabitur vulputate a nunc vel volutpat. Proin gravida arcu odio, eget lacinia odio gravida non. Aliquam erat volutpat. Mauris non interdum felis. Morbi sodales felis quam, sed tristique ante blandit sit amet. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.</p>',
				'<p>Pellentesque ligula lacus, tempor eget tincidunt ut, hendrerit et mauris. Sed venenatis dolor a mollis facilisis. Pellentesque porttitor turpis at nisl tempus ultrices. Integer tincidunt varius felis, nec elementum arcu facilisis sit amet. Morbi semper augue nec turpis fringilla auctor. Fusce felis purus, dapibus in tincidunt id, aliquet pulvinar nunc. Morbi lobortis, nunc a tempus posuere, lacus augue eleifend nulla, quis tempor dolor orci id metus. Nam auctor feugiat mi eget malesuada. Praesent consequat orci odio, eu lacinia risus tincidunt vitae. Ut aliquet eu ligula in molestie.</p>',
				'<p>Nunc in est aliquet, faucibus erat sed, pellentesque quam. Sed fringilla pellentesque purus, tristique tincidunt justo semper vel. Donec eu metus posuere, interdum nisi ac, tincidunt lacus. Duis nisi diam, ullamcorper quis elementum quis, posuere fermentum tellus. Nulla pretium leo vitae urna consectetur, sed interdum diam consectetur. Curabitur neque est, commodo a est id, aliquam dictum felis. Suspendisse arcu velit, imperdiet in diam eget, pellentesque semper purus. Nulla eleifend risus dignissim malesuada gravida.</p><p>Pellentesque ligula lacus, tempor eget tincidunt ut, hendrerit et mauris. Sed venenatis dolor a mollis facilisis. Pellentesque porttitor turpis at nisl tempus ultrices. Integer tincidunt varius felis, nec elementum arcu facilisis sit amet. Morbi semper augue nec turpis fringilla auctor. Fusce felis purus, dapibus in tincidunt id, aliquet pulvinar nunc. Morbi lobortis, nunc a tempus posuere, lacus augue eleifend nulla, quis tempor dolor orci id metus. Nam auctor feugiat mi eget malesuada. Praesent consequat orci odio, eu lacinia risus tincidunt vitae. Ut aliquet eu ligula in molestie.</p>',
				'<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p>',
			)
		);
		
		for( $i=0; $i<count( $sample_photoalbums['titles'] ); $i++ ) {
			
			$post_data = array(
				'post_title'    => $sample_photoalbums['titles'][$i],
				'post_content'  => $sample_photoalbums['content'][$i],
				'post_status'   => 'publish',
				'post_type'			=> 'wproto_photoalbums'
			);
			
			$post_id = wp_insert_post( $post_data );
			
			set_post_thumbnail( $post_id, $sample_images_ids[ rand( 0, count( $sample_images_ids ) - 1)] );
			
			// insert custom fields
			update_post_meta( $post_id, 'wproto_attached_images', $sample_images_ids );
			
		}
		
		/**
		 * Insert sample portfolio posts
		 **/
		$sample_portfolio = array(
			'titles' => array(
				'Lorem ipsum dolor',
				'Nunc feugiat, lectus eget vestibulum',
				'Vivamus adipiscing malesuada',
				'Pellentesque risus nisi, vestibulum',
				'Morbi felis diam, ullamcorper sit amet',
				'Donec quis feugiat nisi. Mauris ut pellentesque tellus',
				'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
				'Morbi felis diam, ullamcorper sit amet massa non',
				'Sed vel dolor pulvinar, viverra',
				'Vivamus adipiscing malesuada imperdiet',
				'Plane fly high over the ground and seas',
				'Plane fly high over the ground and seas',
				'Lorem ipsum dolor sit amet, consectetur adipiscing elit'
			),
			'content' => array(
				'<p>There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don\'t look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn\'t anything embarrassing hidden in the middle of text.</p><p>All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable.</p><p>The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc. There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don\'t look even slightly believable.</p>',
				'<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p>',
				'<p>Phasellus quam ligula, feugiat in dignissim at, porttitor et sapien. Duis porttitor orci at libero egestas, vel viverra urna ullamcorper. Ut malesuada, felis sed interdum suscipit, metus neque vehicula nisi, quis sagittis purus dolor bibendum est. Nullam mollis eu urna quis eleifend. Ut ullamcorper risus non tellus consectetur auctor sed in nisl. Morbi nec purus vehicula, pellentesque elit condimentum, egestas lacus. Nullam mi est, imperdiet sed elit nec, hendrerit feugiat ligula. Nunc ac leo porttitor, lobortis nisi quis, eleifend libero. Curabitur vulputate a nunc vel volutpat. Proin gravida arcu odio, eget lacinia odio gravida non. Aliquam erat volutpat. Mauris non interdum felis. Morbi sodales felis quam, sed tristique ante blandit sit amet. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.</p>',
				'<p>Pellentesque ligula lacus, tempor eget tincidunt ut, hendrerit et mauris. Sed venenatis dolor a mollis facilisis. Pellentesque porttitor turpis at nisl tempus ultrices. Integer tincidunt varius felis, nec elementum arcu facilisis sit amet. Morbi semper augue nec turpis fringilla auctor. Fusce felis purus, dapibus in tincidunt id, aliquet pulvinar nunc. Morbi lobortis, nunc a tempus posuere, lacus augue eleifend nulla, quis tempor dolor orci id metus. Nam auctor feugiat mi eget malesuada. Praesent consequat orci odio, eu lacinia risus tincidunt vitae. Ut aliquet eu ligula in molestie.</p>',
				'<p>Nunc in est aliquet, faucibus erat sed, pellentesque quam. Sed fringilla pellentesque purus, tristique tincidunt justo semper vel. Donec eu metus posuere, interdum nisi ac, tincidunt lacus. Duis nisi diam, ullamcorper quis elementum quis, posuere fermentum tellus. Nulla pretium leo vitae urna consectetur, sed interdum diam consectetur. Curabitur neque est, commodo a est id, aliquam dictum felis. Suspendisse arcu velit, imperdiet in diam eget, pellentesque semper purus. Nulla eleifend risus dignissim malesuada gravida.</p><p>Pellentesque ligula lacus, tempor eget tincidunt ut, hendrerit et mauris. Sed venenatis dolor a mollis facilisis. Pellentesque porttitor turpis at nisl tempus ultrices. Integer tincidunt varius felis, nec elementum arcu facilisis sit amet. Morbi semper augue nec turpis fringilla auctor. Fusce felis purus, dapibus in tincidunt id, aliquet pulvinar nunc. Morbi lobortis, nunc a tempus posuere, lacus augue eleifend nulla, quis tempor dolor orci id metus. Nam auctor feugiat mi eget malesuada. Praesent consequat orci odio, eu lacinia risus tincidunt vitae. Ut aliquet eu ligula in molestie.</p>',
				'<p>Nulla scelerisque, ligula quis eleifend faucibus, quam purus bibendum elit, eu condimentum libero quam sit amet magna. Nunc malesuada elit eget ipsum auctor elementum. Aliquam euismod dignissim arcu, et tempus ligula mollis vel. Cras consectetur vitae sem at vulputate. Nunc viverra mi massa, in rhoncus tortor auctor eu. Fusce eget lorem iaculis dolor suscipit luctus eget vitae ipsum. Suspendisse placerat, est fermentum venenatis dignissim, magna nibh vestibulum eros, a egestas neque enim a dolor. Pellentesque at eleifend ligula. Integer eget urna pretium, commodo nunc nec, pulvinar tortor. Phasellus vel mattis quam. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras luctus varius libero, dapibus luctus tortor bibendum eu. Cras quis accumsan lorem. Donec non erat at sapien congue egestas.</p>',
				'<p>Sed sollicitudin vitae massa a aliquet. Vestibulum consectetur quam ornare odio iaculis, in lobortis mauris ullamcorper. Praesent blandit eros et nisi fermentum pretium. Morbi turpis metus, faucibus vitae dapibus id, tempus vel diam. In rhoncus libero ut tellus ultrices, eget luctus mi tincidunt. Etiam magna dui, accumsan pretium nunc eget, facilisis luctus odio. Etiam eget lectus eget libero gravida vestibulum. Sed sagittis gravida lorem ut ullamcorper. Etiam gravida mauris at bibendum faucibus. Curabitur tempor vel est non aliquam. Proin non nunc lobortis, tristique massa sed, pharetra urna. Donec rhoncus orci nulla, et faucibus mauris commodo ut. Suspendisse risus mauris, posuere a est eget, ultrices ultrices metus. Duis purus sapien, molestie in mi vel, fermentum congue nulla.</p>',
				'<p>There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don\'t look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn\'t anything embarrassing hidden in the middle of text.</p><p>All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable.</p><p>The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc. There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don\'t look even slightly believable.</p>',
				'<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p>',
				'<p>Phasellus quam ligula, feugiat in dignissim at, porttitor et sapien. Duis porttitor orci at libero egestas, vel viverra urna ullamcorper. Ut malesuada, felis sed interdum suscipit, metus neque vehicula nisi, quis sagittis purus dolor bibendum est. Nullam mollis eu urna quis eleifend. Ut ullamcorper risus non tellus consectetur auctor sed in nisl. Morbi nec purus vehicula, pellentesque elit condimentum, egestas lacus. Nullam mi est, imperdiet sed elit nec, hendrerit feugiat ligula. Nunc ac leo porttitor, lobortis nisi quis, eleifend libero. Curabitur vulputate a nunc vel volutpat. Proin gravida arcu odio, eget lacinia odio gravida non. Aliquam erat volutpat. Mauris non interdum felis. Morbi sodales felis quam, sed tristique ante blandit sit amet. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.</p>',
				'<p>Pellentesque ligula lacus, tempor eget tincidunt ut, hendrerit et mauris. Sed venenatis dolor a mollis facilisis. Pellentesque porttitor turpis at nisl tempus ultrices. Integer tincidunt varius felis, nec elementum arcu facilisis sit amet. Morbi semper augue nec turpis fringilla auctor. Fusce felis purus, dapibus in tincidunt id, aliquet pulvinar nunc. Morbi lobortis, nunc a tempus posuere, lacus augue eleifend nulla, quis tempor dolor orci id metus. Nam auctor feugiat mi eget malesuada. Praesent consequat orci odio, eu lacinia risus tincidunt vitae. Ut aliquet eu ligula in molestie.</p>',
				'<p>Nunc in est aliquet, faucibus erat sed, pellentesque quam. Sed fringilla pellentesque purus, tristique tincidunt justo semper vel. Donec eu metus posuere, interdum nisi ac, tincidunt lacus. Duis nisi diam, ullamcorper quis elementum quis, posuere fermentum tellus. Nulla pretium leo vitae urna consectetur, sed interdum diam consectetur. Curabitur neque est, commodo a est id, aliquam dictum felis. Suspendisse arcu velit, imperdiet in diam eget, pellentesque semper purus. Nulla eleifend risus dignissim malesuada gravida.</p><p>Pellentesque ligula lacus, tempor eget tincidunt ut, hendrerit et mauris. Sed venenatis dolor a mollis facilisis. Pellentesque porttitor turpis at nisl tempus ultrices. Integer tincidunt varius felis, nec elementum arcu facilisis sit amet. Morbi semper augue nec turpis fringilla auctor. Fusce felis purus, dapibus in tincidunt id, aliquet pulvinar nunc. Morbi lobortis, nunc a tempus posuere, lacus augue eleifend nulla, quis tempor dolor orci id metus. Nam auctor feugiat mi eget malesuada. Praesent consequat orci odio, eu lacinia risus tincidunt vitae. Ut aliquet eu ligula in molestie.</p>',
				'<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p>',
			)
		);
		
		for( $i=0; $i<count( $sample_portfolio['titles'] ); $i++ ) {
			
			$post_data = array(
				'post_title'    => $sample_portfolio['titles'][$i],
				'post_content'  => $sample_portfolio['content'][$i],
				'post_status'   => 'publish',
				'post_type'			=> 'wproto_portfolio'
			);
			
			$post_id = wp_insert_post( $post_data );
			
			set_post_thumbnail( $post_id, $sample_images_ids[ rand( 0, count( $sample_images_ids ) - 1)] );
			
			// insert custom fields
			update_post_meta( $post_id, 'wproto_attached_images', $sample_images_ids );
			
		}
		
		/**
		 * Insert sample catalog posts
		 **/
		$sample_catalog = array(
			'titles' => array(
				'Samsung Galaxy Note 3 HD 32Gb',
				'Smartphone Galaxy HD 3',
				'Samsung TV LED Galaxy Note 3',
				'Samsung Galaxy Note 3 HD 32Gb',
				'Samsung Galaxy S4 HD proffesional edition',
				'GoldStar Note 3',
				'Samsung Galaxy Tab 3',
				'Samsung Galaxy S4 Mini',
				'Samsung Galaxy Note 10',
				'Samsung TV LED Galaxy Note 3',
				'Samsung Galaxy Note 3 HD 32Gb',
				'Samsung Galaxy S4 HD proffesional edition',
				'Galaxy Note'
			),
			'content' => array(
				'<p>In magna tellus, fermentum ac lorem quis, dictum consequat libero. Morbi molestie eleifend est, quis pulvinar libero. Proin laoreet lorem nec nunc pretium eleifend. Curabitur suscipit porttitor turpis quis commodo. Integer pharetra interdum libero. Morbi mollis in enim at dapibus. Morbi tristique augue diam, rhoncus posuere leo semper eu. Aenean ultricies viverra consectetur. Sed congue dolor a orci facilisis venenatis. Proin convallis sollicitudin aliquam. Pellentesque a odio aliquet, molestie massa vitae, lobortis erat.</p>',
				'<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris at porta metus. Nunc faucibus arcu ac metus fringilla rhoncus et vitae ante. Nunc fermentum magna et dictum placerat. Curabitur ut tincidunt nulla. Nunc eu felis eros. Fusce accumsan lobortis nisl, vitae pretium enim aliquam eget. Duis iaculis euismod nunc, ac elementum libero accumsan vitae. Praesent semper metus sit amet augue consectetur tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent interdum ac magna vitae rhoncus.</p>',
				'<p>In magna tellus, fermentum ac lorem quis, dictum consequat libero. Morbi molestie eleifend est, quis pulvinar libero. Proin laoreet lorem nec nunc pretium eleifend. Curabitur suscipit porttitor turpis quis commodo. Integer pharetra interdum libero. Morbi mollis in enim at dapibus. Morbi tristique augue diam, rhoncus posuere leo semper eu. Aenean ultricies viverra consectetur. Sed congue dolor a orci facilisis venenatis. Proin convallis sollicitudin aliquam. Pellentesque a odio aliquet, molestie massa vitae, lobortis erat.</p>',
				'<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris at porta metus. Nunc faucibus arcu ac metus fringilla rhoncus et vitae ante. Nunc fermentum magna et dictum placerat. Curabitur ut tincidunt nulla. Nunc eu felis eros. Fusce accumsan lobortis nisl, vitae pretium enim aliquam eget. Duis iaculis euismod nunc, ac elementum libero accumsan vitae. Praesent semper metus sit amet augue consectetur tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent interdum ac magna vitae rhoncus.</p>',
				'<p>In magna tellus, fermentum ac lorem quis, dictum consequat libero. Morbi molestie eleifend est, quis pulvinar libero. Proin laoreet lorem nec nunc pretium eleifend. Curabitur suscipit porttitor turpis quis commodo. Integer pharetra interdum libero. Morbi mollis in enim at dapibus. Morbi tristique augue diam, rhoncus posuere leo semper eu. Aenean ultricies viverra consectetur. Sed congue dolor a orci facilisis venenatis. Proin convallis sollicitudin aliquam. Pellentesque a odio aliquet, molestie massa vitae, lobortis erat.</p>',
				'<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris at porta metus. Nunc faucibus arcu ac metus fringilla rhoncus et vitae ante. Nunc fermentum magna et dictum placerat. Curabitur ut tincidunt nulla. Nunc eu felis eros. Fusce accumsan lobortis nisl, vitae pretium enim aliquam eget. Duis iaculis euismod nunc, ac elementum libero accumsan vitae. Praesent semper metus sit amet augue consectetur tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent interdum ac magna vitae rhoncus.</p>',
				'<p>In magna tellus, fermentum ac lorem quis, dictum consequat libero. Morbi molestie eleifend est, quis pulvinar libero. Proin laoreet lorem nec nunc pretium eleifend. Curabitur suscipit porttitor turpis quis commodo. Integer pharetra interdum libero. Morbi mollis in enim at dapibus. Morbi tristique augue diam, rhoncus posuere leo semper eu. Aenean ultricies viverra consectetur. Sed congue dolor a orci facilisis venenatis. Proin convallis sollicitudin aliquam. Pellentesque a odio aliquet, molestie massa vitae, lobortis erat.</p>',
				'<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris at porta metus. Nunc faucibus arcu ac metus fringilla rhoncus et vitae ante. Nunc fermentum magna et dictum placerat. Curabitur ut tincidunt nulla. Nunc eu felis eros. Fusce accumsan lobortis nisl, vitae pretium enim aliquam eget. Duis iaculis euismod nunc, ac elementum libero accumsan vitae. Praesent semper metus sit amet augue consectetur tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent interdum ac magna vitae rhoncus.</p>',
				'<p>In magna tellus, fermentum ac lorem quis, dictum consequat libero. Morbi molestie eleifend est, quis pulvinar libero. Proin laoreet lorem nec nunc pretium eleifend. Curabitur suscipit porttitor turpis quis commodo. Integer pharetra interdum libero. Morbi mollis in enim at dapibus. Morbi tristique augue diam, rhoncus posuere leo semper eu. Aenean ultricies viverra consectetur. Sed congue dolor a orci facilisis venenatis. Proin convallis sollicitudin aliquam. Pellentesque a odio aliquet, molestie massa vitae, lobortis erat.</p>',
				'<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris at porta metus. Nunc faucibus arcu ac metus fringilla rhoncus et vitae ante. Nunc fermentum magna et dictum placerat. Curabitur ut tincidunt nulla. Nunc eu felis eros. Fusce accumsan lobortis nisl, vitae pretium enim aliquam eget. Duis iaculis euismod nunc, ac elementum libero accumsan vitae. Praesent semper metus sit amet augue consectetur tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent interdum ac magna vitae rhoncus.</p>',
				'<p>In magna tellus, fermentum ac lorem quis, dictum consequat libero. Morbi molestie eleifend est, quis pulvinar libero. Proin laoreet lorem nec nunc pretium eleifend. Curabitur suscipit porttitor turpis quis commodo. Integer pharetra interdum libero. Morbi mollis in enim at dapibus. Morbi tristique augue diam, rhoncus posuere leo semper eu. Aenean ultricies viverra consectetur. Sed congue dolor a orci facilisis venenatis. Proin convallis sollicitudin aliquam. Pellentesque a odio aliquet, molestie massa vitae, lobortis erat.</p>',
				'<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris at porta metus. Nunc faucibus arcu ac metus fringilla rhoncus et vitae ante. Nunc fermentum magna et dictum placerat. Curabitur ut tincidunt nulla. Nunc eu felis eros. Fusce accumsan lobortis nisl, vitae pretium enim aliquam eget. Duis iaculis euismod nunc, ac elementum libero accumsan vitae. Praesent semper metus sit amet augue consectetur tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent interdum ac magna vitae rhoncus.</p>',
				'<p>In magna tellus, fermentum ac lorem quis, dictum consequat libero. Morbi molestie eleifend est, quis pulvinar libero. Proin laoreet lorem nec nunc pretium eleifend. Curabitur suscipit porttitor turpis quis commodo. Integer pharetra interdum libero. Morbi mollis in enim at dapibus. Morbi tristique augue diam, rhoncus posuere leo semper eu. Aenean ultricies viverra consectetur. Sed congue dolor a orci facilisis venenatis. Proin convallis sollicitudin aliquam. Pellentesque a odio aliquet, molestie massa vitae, lobortis erat.</p>'
			),
			'custom_fields' => array(
				array(
					'overview_text' => '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris at porta metus. Nunc faucibus arcu ac metus fringilla rhoncus et vitae ante. Nunc fermentum magna et dictum placerat. Curabitur ut tincidunt nulla. Nunc eu felis eros. Fusce accumsan lobortis nisl, vitae pretium enim aliquam eget. Duis iaculis euismod nunc, ac elementum libero accumsan vitae. Praesent semper metus sit amet augue consectetur tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent interdum ac magna vitae rhoncus.</p><p>In magna tellus, fermentum ac lorem quis, dictum consequat libero. Morbi molestie eleifend est, quis pulvinar libero. Proin laoreet lorem nec nunc pretium eleifend. Curabitur suscipit porttitor turpis quis commodo. Integer pharetra interdum libero. Morbi mollis in enim at dapibus. Morbi tristique augue diam, rhoncus posuere leo semper eu. Aenean ultricies viverra consectetur. Sed congue dolor a orci facilisis venenatis. Proin convallis sollicitudin aliquam. Pellentesque a odio aliquet, molestie massa vitae, lobortis erat.</p>',
					'price' => '1299',
					'old_price' => '1350',
					'sku' => '12345',
					'link_to_buy' => 'http://themeforest.net/user/wplab/portfolio',
					'badge' => 'onsale'
				),
				array(
					'overview_text' => '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris at porta metus. Nunc faucibus arcu ac metus fringilla rhoncus et vitae ante. Nunc fermentum magna et dictum placerat. Curabitur ut tincidunt nulla. Nunc eu felis eros. Fusce accumsan lobortis nisl, vitae pretium enim aliquam eget. Duis iaculis euismod nunc, ac elementum libero accumsan vitae. Praesent semper metus sit amet augue consectetur tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent interdum ac magna vitae rhoncus.</p><p>In magna tellus, fermentum ac lorem quis, dictum consequat libero. Morbi molestie eleifend est, quis pulvinar libero. Proin laoreet lorem nec nunc pretium eleifend. Curabitur suscipit porttitor turpis quis commodo. Integer pharetra interdum libero. Morbi mollis in enim at dapibus. Morbi tristique augue diam, rhoncus posuere leo semper eu. Aenean ultricies viverra consectetur. Sed congue dolor a orci facilisis venenatis. Proin convallis sollicitudin aliquam. Pellentesque a odio aliquet, molestie massa vitae, lobortis erat.</p>',
					'price' => '477',
					'old_price' => '1200',
					'sku' => '13457',
					'link_to_buy' => 'http://themeforest.net/user/wplab/portfolio',
					'badge' => 'best_price'
				),
				array(
					'overview_text' => '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris at porta metus. Nunc faucibus arcu ac metus fringilla rhoncus et vitae ante. Nunc fermentum magna et dictum placerat. Curabitur ut tincidunt nulla. Nunc eu felis eros. Fusce accumsan lobortis nisl, vitae pretium enim aliquam eget. Duis iaculis euismod nunc, ac elementum libero accumsan vitae. Praesent semper metus sit amet augue consectetur tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent interdum ac magna vitae rhoncus.</p><p>In magna tellus, fermentum ac lorem quis, dictum consequat libero. Morbi molestie eleifend est, quis pulvinar libero. Proin laoreet lorem nec nunc pretium eleifend. Curabitur suscipit porttitor turpis quis commodo. Integer pharetra interdum libero. Morbi mollis in enim at dapibus. Morbi tristique augue diam, rhoncus posuere leo semper eu. Aenean ultricies viverra consectetur. Sed congue dolor a orci facilisis venenatis. Proin convallis sollicitudin aliquam. Pellentesque a odio aliquet, molestie massa vitae, lobortis erat.</p>',
					'price' => '354',
					'old_price' => '800',
					'sku' => '45178',
					'link_to_buy' => 'http://themeforest.net/user/wplab/portfolio',
					'badge' => ''
				),
				array(
					'overview_text' => '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris at porta metus. Nunc faucibus arcu ac metus fringilla rhoncus et vitae ante. Nunc fermentum magna et dictum placerat. Curabitur ut tincidunt nulla. Nunc eu felis eros. Fusce accumsan lobortis nisl, vitae pretium enim aliquam eget. Duis iaculis euismod nunc, ac elementum libero accumsan vitae. Praesent semper metus sit amet augue consectetur tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent interdum ac magna vitae rhoncus.</p><p>In magna tellus, fermentum ac lorem quis, dictum consequat libero. Morbi molestie eleifend est, quis pulvinar libero. Proin laoreet lorem nec nunc pretium eleifend. Curabitur suscipit porttitor turpis quis commodo. Integer pharetra interdum libero. Morbi mollis in enim at dapibus. Morbi tristique augue diam, rhoncus posuere leo semper eu. Aenean ultricies viverra consectetur. Sed congue dolor a orci facilisis venenatis. Proin convallis sollicitudin aliquam. Pellentesque a odio aliquet, molestie massa vitae, lobortis erat.</p>',
					'price' => '1299',
					'old_price' => '1350',
					'sku' => '12345',
					'link_to_buy' => 'http://themeforest.net/user/wplab/portfolio',
					'badge' => 'onsale'
				),
				array(
					'overview_text' => '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris at porta metus. Nunc faucibus arcu ac metus fringilla rhoncus et vitae ante. Nunc fermentum magna et dictum placerat. Curabitur ut tincidunt nulla. Nunc eu felis eros. Fusce accumsan lobortis nisl, vitae pretium enim aliquam eget. Duis iaculis euismod nunc, ac elementum libero accumsan vitae. Praesent semper metus sit amet augue consectetur tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent interdum ac magna vitae rhoncus.</p><p>In magna tellus, fermentum ac lorem quis, dictum consequat libero. Morbi molestie eleifend est, quis pulvinar libero. Proin laoreet lorem nec nunc pretium eleifend. Curabitur suscipit porttitor turpis quis commodo. Integer pharetra interdum libero. Morbi mollis in enim at dapibus. Morbi tristique augue diam, rhoncus posuere leo semper eu. Aenean ultricies viverra consectetur. Sed congue dolor a orci facilisis venenatis. Proin convallis sollicitudin aliquam. Pellentesque a odio aliquet, molestie massa vitae, lobortis erat.</p>',
					'price' => '477',
					'old_price' => '1200',
					'sku' => '13457',
					'link_to_buy' => 'http://themeforest.net/user/wplab/portfolio',
					'badge' => 'best_price'
				),
				array(
					'overview_text' => '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris at porta metus. Nunc faucibus arcu ac metus fringilla rhoncus et vitae ante. Nunc fermentum magna et dictum placerat. Curabitur ut tincidunt nulla. Nunc eu felis eros. Fusce accumsan lobortis nisl, vitae pretium enim aliquam eget. Duis iaculis euismod nunc, ac elementum libero accumsan vitae. Praesent semper metus sit amet augue consectetur tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent interdum ac magna vitae rhoncus.</p><p>In magna tellus, fermentum ac lorem quis, dictum consequat libero. Morbi molestie eleifend est, quis pulvinar libero. Proin laoreet lorem nec nunc pretium eleifend. Curabitur suscipit porttitor turpis quis commodo. Integer pharetra interdum libero. Morbi mollis in enim at dapibus. Morbi tristique augue diam, rhoncus posuere leo semper eu. Aenean ultricies viverra consectetur. Sed congue dolor a orci facilisis venenatis. Proin convallis sollicitudin aliquam. Pellentesque a odio aliquet, molestie massa vitae, lobortis erat.</p>',
					'price' => '354',
					'old_price' => '800',
					'sku' => '45178',
					'link_to_buy' => 'http://themeforest.net/user/wplab/portfolio',
					'badge' => ''
				),
				array(
					'overview_text' => '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris at porta metus. Nunc faucibus arcu ac metus fringilla rhoncus et vitae ante. Nunc fermentum magna et dictum placerat. Curabitur ut tincidunt nulla. Nunc eu felis eros. Fusce accumsan lobortis nisl, vitae pretium enim aliquam eget. Duis iaculis euismod nunc, ac elementum libero accumsan vitae. Praesent semper metus sit amet augue consectetur tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent interdum ac magna vitae rhoncus.</p><p>In magna tellus, fermentum ac lorem quis, dictum consequat libero. Morbi molestie eleifend est, quis pulvinar libero. Proin laoreet lorem nec nunc pretium eleifend. Curabitur suscipit porttitor turpis quis commodo. Integer pharetra interdum libero. Morbi mollis in enim at dapibus. Morbi tristique augue diam, rhoncus posuere leo semper eu. Aenean ultricies viverra consectetur. Sed congue dolor a orci facilisis venenatis. Proin convallis sollicitudin aliquam. Pellentesque a odio aliquet, molestie massa vitae, lobortis erat.</p>',
					'price' => '1299',
					'old_price' => '1350',
					'sku' => '12345',
					'link_to_buy' => 'http://themeforest.net/user/wplab/portfolio',
					'badge' => 'onsale'
				),
				array(
					'overview_text' => '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris at porta metus. Nunc faucibus arcu ac metus fringilla rhoncus et vitae ante. Nunc fermentum magna et dictum placerat. Curabitur ut tincidunt nulla. Nunc eu felis eros. Fusce accumsan lobortis nisl, vitae pretium enim aliquam eget. Duis iaculis euismod nunc, ac elementum libero accumsan vitae. Praesent semper metus sit amet augue consectetur tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent interdum ac magna vitae rhoncus.</p><p>In magna tellus, fermentum ac lorem quis, dictum consequat libero. Morbi molestie eleifend est, quis pulvinar libero. Proin laoreet lorem nec nunc pretium eleifend. Curabitur suscipit porttitor turpis quis commodo. Integer pharetra interdum libero. Morbi mollis in enim at dapibus. Morbi tristique augue diam, rhoncus posuere leo semper eu. Aenean ultricies viverra consectetur. Sed congue dolor a orci facilisis venenatis. Proin convallis sollicitudin aliquam. Pellentesque a odio aliquet, molestie massa vitae, lobortis erat.</p>',
					'price' => '477',
					'old_price' => '1200',
					'sku' => '13457',
					'link_to_buy' => 'http://themeforest.net/user/wplab/portfolio',
					'badge' => 'best_price'
				),
				array(
					'overview_text' => '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris at porta metus. Nunc faucibus arcu ac metus fringilla rhoncus et vitae ante. Nunc fermentum magna et dictum placerat. Curabitur ut tincidunt nulla. Nunc eu felis eros. Fusce accumsan lobortis nisl, vitae pretium enim aliquam eget. Duis iaculis euismod nunc, ac elementum libero accumsan vitae. Praesent semper metus sit amet augue consectetur tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent interdum ac magna vitae rhoncus.</p><p>In magna tellus, fermentum ac lorem quis, dictum consequat libero. Morbi molestie eleifend est, quis pulvinar libero. Proin laoreet lorem nec nunc pretium eleifend. Curabitur suscipit porttitor turpis quis commodo. Integer pharetra interdum libero. Morbi mollis in enim at dapibus. Morbi tristique augue diam, rhoncus posuere leo semper eu. Aenean ultricies viverra consectetur. Sed congue dolor a orci facilisis venenatis. Proin convallis sollicitudin aliquam. Pellentesque a odio aliquet, molestie massa vitae, lobortis erat.</p>',
					'price' => '354',
					'old_price' => '800',
					'sku' => '45178',
					'link_to_buy' => 'http://themeforest.net/user/wplab/portfolio',
					'badge' => ''
				),
				array(
					'overview_text' => '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris at porta metus. Nunc faucibus arcu ac metus fringilla rhoncus et vitae ante. Nunc fermentum magna et dictum placerat. Curabitur ut tincidunt nulla. Nunc eu felis eros. Fusce accumsan lobortis nisl, vitae pretium enim aliquam eget. Duis iaculis euismod nunc, ac elementum libero accumsan vitae. Praesent semper metus sit amet augue consectetur tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent interdum ac magna vitae rhoncus.</p><p>In magna tellus, fermentum ac lorem quis, dictum consequat libero. Morbi molestie eleifend est, quis pulvinar libero. Proin laoreet lorem nec nunc pretium eleifend. Curabitur suscipit porttitor turpis quis commodo. Integer pharetra interdum libero. Morbi mollis in enim at dapibus. Morbi tristique augue diam, rhoncus posuere leo semper eu. Aenean ultricies viverra consectetur. Sed congue dolor a orci facilisis venenatis. Proin convallis sollicitudin aliquam. Pellentesque a odio aliquet, molestie massa vitae, lobortis erat.</p>',
					'price' => '1299',
					'old_price' => '1350',
					'sku' => '12345',
					'link_to_buy' => 'http://themeforest.net/user/wplab/portfolio',
					'badge' => 'onsale'
				),
				array(
					'overview_text' => '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris at porta metus. Nunc faucibus arcu ac metus fringilla rhoncus et vitae ante. Nunc fermentum magna et dictum placerat. Curabitur ut tincidunt nulla. Nunc eu felis eros. Fusce accumsan lobortis nisl, vitae pretium enim aliquam eget. Duis iaculis euismod nunc, ac elementum libero accumsan vitae. Praesent semper metus sit amet augue consectetur tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent interdum ac magna vitae rhoncus.</p><p>In magna tellus, fermentum ac lorem quis, dictum consequat libero. Morbi molestie eleifend est, quis pulvinar libero. Proin laoreet lorem nec nunc pretium eleifend. Curabitur suscipit porttitor turpis quis commodo. Integer pharetra interdum libero. Morbi mollis in enim at dapibus. Morbi tristique augue diam, rhoncus posuere leo semper eu. Aenean ultricies viverra consectetur. Sed congue dolor a orci facilisis venenatis. Proin convallis sollicitudin aliquam. Pellentesque a odio aliquet, molestie massa vitae, lobortis erat.</p>',
					'price' => '477',
					'old_price' => '1200',
					'sku' => '13457',
					'link_to_buy' => 'http://themeforest.net/user/wplab/portfolio',
					'badge' => 'best_price'
				),
				array(
					'overview_text' => '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris at porta metus. Nunc faucibus arcu ac metus fringilla rhoncus et vitae ante. Nunc fermentum magna et dictum placerat. Curabitur ut tincidunt nulla. Nunc eu felis eros. Fusce accumsan lobortis nisl, vitae pretium enim aliquam eget. Duis iaculis euismod nunc, ac elementum libero accumsan vitae. Praesent semper metus sit amet augue consectetur tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent interdum ac magna vitae rhoncus.</p><p>In magna tellus, fermentum ac lorem quis, dictum consequat libero. Morbi molestie eleifend est, quis pulvinar libero. Proin laoreet lorem nec nunc pretium eleifend. Curabitur suscipit porttitor turpis quis commodo. Integer pharetra interdum libero. Morbi mollis in enim at dapibus. Morbi tristique augue diam, rhoncus posuere leo semper eu. Aenean ultricies viverra consectetur. Sed congue dolor a orci facilisis venenatis. Proin convallis sollicitudin aliquam. Pellentesque a odio aliquet, molestie massa vitae, lobortis erat.</p>',
					'price' => '354',
					'old_price' => '800',
					'sku' => '45178',
					'link_to_buy' => 'http://themeforest.net/user/wplab/portfolio',
					'badge' => ''
				),
				array(
					'overview_text' => '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ullamcorper, libero ac lobortis mollis, ipsum nunc convallis lacus, non adipiscing dolor ante vitae turpis. Etiam venenatis at massa sed scelerisque. Etiam scelerisque ipsum felis, ut semper velit lacinia eget. Praesent eget urna ut metus fermentum consequat. Vestibulum auctor ante a sem lacinia congue. Ut elementum enim non diam cursus tincidunt. Nulla fermentum dui augue, egestas sollicitudin nibh hendrerit ac. Donec condimentum dapibus dolor id consequat. Morbi mauris dolor, egestas eget porta at, accumsan quis arcu. Praesent nunc mauris, fermentum ac sem quis, auctor volutpat elit. Suspendisse pellentesque leo non turpis luctus malesuada. Nulla rutrum vulputate dictum. Mauris porta nisi mauris. Nullam et vehicula dui, id condimentum ante.</p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris at porta metus. Nunc faucibus arcu ac metus fringilla rhoncus et vitae ante. Nunc fermentum magna et dictum placerat. Curabitur ut tincidunt nulla. Nunc eu felis eros. Fusce accumsan lobortis nisl, vitae pretium enim aliquam eget. Duis iaculis euismod nunc, ac elementum libero accumsan vitae. Praesent semper metus sit amet augue consectetur tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent interdum ac magna vitae rhoncus.</p><p>In magna tellus, fermentum ac lorem quis, dictum consequat libero. Morbi molestie eleifend est, quis pulvinar libero. Proin laoreet lorem nec nunc pretium eleifend. Curabitur suscipit porttitor turpis quis commodo. Integer pharetra interdum libero. Morbi mollis in enim at dapibus. Morbi tristique augue diam, rhoncus posuere leo semper eu. Aenean ultricies viverra consectetur. Sed congue dolor a orci facilisis venenatis. Proin convallis sollicitudin aliquam. Pellentesque a odio aliquet, molestie massa vitae, lobortis erat.</p>',
					'price' => '477',
					'old_price' => '1200',
					'sku' => '13457',
					'link_to_buy' => 'http://themeforest.net/user/wplab/portfolio',
					'badge' => 'best_price'
				)
			)
		);
		
		for( $i=0; $i<count( $sample_catalog['titles'] ); $i++ ) {
			
			$post_data = array(
				'post_title'    => $sample_catalog['titles'][$i],
				'post_content'  => $sample_catalog['content'][$i],
				'post_status'   => 'publish',
				'post_type'			=> 'wproto_catalog'
			);
			
			$post_id = wp_insert_post( $post_data );
			
			set_post_thumbnail( $post_id, $sample_images_ids[ rand( 0, count( $sample_images_ids ) - 1)] );
			
			// insert custom fields
			update_post_meta( $post_id, 'wproto_attached_images', $sample_images_ids );
			
		}
		
		/**
		 * Insert sample partners
		 **/
		$sample_partners = array(
			'titles' => array(
				'Design Service',
				'Rocket Science',
				'Abstract',
				'Bio Design',
				'Grunge Shield',
				'The Human'
			)
		);
		
		for( $i=0; $i<count( $sample_partners['titles'] ); $i++ ) {
			
			$post_data = array(
				'post_title'    => $sample_partners['titles'][$i],
				'post_content'  => '',
				'post_status'   => 'publish',
				'post_type'			=> 'wproto_partners'
			);
			
			$post_id = wp_insert_post( $post_data );

			set_post_thumbnail( $post_id, $sample_images_ids[ rand( 0, count( $sample_images_ids ) - 1)] );
			
		}
		
		/**
		 * Insert sample team members
		 **/
		$sample_team_members = array(
			'titles' => array(
				'Lian Road',
				'Albert Mushino',
				'John Doe',
				'John Robertson'
			),
			'content' => array(
				'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin eu suscipit tortor. Aenean lobortis commodo augue vitae iaculis.',
				'Mauris nunc risus, aliquam nec est vel, tempus pellentesque quam.',
				'Phasellus consectetur lacus id tristique tincidunt. Donec venenatis fermentum diam.',
				'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin eu suscipit tortor. Aenean lobortis commodo augue vitae iaculis.'
			),
			'custom_fields' => array(
				array(
					'age' => 35,
					'position' => 'CEO',
					'twitter_url' => 'http://twitter.com',
					'facebook_url' => 'http://facebook.com',
					'linkedin_url' => 'http://linkedin.com'
				),
				array(
					'age' => 25,
					'position' => 'Designer',
					'twitter_url' => 'http://twitter.com',
					'facebook_url' => 'http://facebook.com',
					'linkedin_url' => 'http://linkedin.com'
				),
				array(
					'age' => 27,
					'position' => 'Programmer',
					'twitter_url' => 'http://twitter.com',
					'facebook_url' => 'http://facebook.com',
					'linkedin_url' => 'http://linkedin.com'
				),
				array(
					'age' => 22,
					'position' => 'Developer',
					'twitter_url' => 'http://twitter.com',
					'facebook_url' => 'http://facebook.com',
					'linkedin_url' => 'http://linkedin.com'
				),
			)
		);
		
		for( $i=0; $i<count( $sample_team_members['titles'] ); $i++ ) {
			
			$post_data = array(
				'post_title'    => $sample_team_members['titles'][$i],
				'post_content'  => $sample_team_members['content'][$i],
				'post_status'   => 'publish',
				'post_type'			=> 'wproto_team'
			);
			
			$post_id = wp_insert_post( $post_data );

			set_post_thumbnail( $post_id, $sample_images_ids[ rand( 0, count( $sample_images_ids ) - 1)] );
			
			// insert custom fields
			foreach( $sample_team_members['custom_fields'][$i] as $k=>$v ) {
				update_post_meta( $post_id, $k, $v );
			}
			
		}
		
		/**
		 * Insert sample benefits
		 **/
		$sample_benefits = array(
			'titles' => array(
				'HQ HTML5 & CSS3',
				'Responsive design',
				'Clean Code',
				'New UI ideas'
			),
			'content' => array(
				'HTML are many variations of passages in Lorem Ipsum available, but the majority have suffered alteration.',
				'Design are many variations of passages in Lorem Ipsum available, but the majority have suffered alteration.',
				'Code are many variations of passages Lorem Ipsum available, but the majority have suffered alteration.',
				'There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration.'
			),
			'custom_fields' => array(
				array(
					'wproto_benefit_style' => 'icon',
					'wproto_benefit_icon_name' => 'fa-clock-o fa'
				),
				array(
					'wproto_benefit_style' => 'icon',
					'wproto_benefit_icon_name' => 'fa-star fa'
				),
				array(
					'wproto_benefit_style' => 'icon',
					'wproto_benefit_icon_name' => 'fa-html5 fa'
				),
				array(
					'wproto_benefit_style' => 'icon',
					'wproto_benefit_icon_name' => 'fa-lightbulb-o fa'
				),
			)
		);
		
		for( $i=0; $i<count( $sample_benefits['titles'] ); $i++ ) {
			
			$post_data = array(
				'post_title'    => $sample_benefits['titles'][$i],
				'post_content'  => $sample_benefits['content'][$i],
				'post_status'   => 'publish',
				'post_type'			=> 'wproto_benefits'
			);
			
			$post_id = wp_insert_post( $post_data );

			set_post_thumbnail( $post_id, $sample_images_ids[ rand( 0, count( $sample_images_ids ) - 1)] );
			
			// insert custom fields
			foreach( $sample_benefits['custom_fields'][$i] as $k=>$v ) {
				update_post_meta( $post_id, $k, $v );
			}
			
		}
		
		/**
		 * Insert sample testimonials
		 **/
		$sample_testimonials = array(
			'titles' => array(
				'Elvis Moore',
				'Marina Doe',
				'John Doe'
			),
			'content' => array(
				'There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration. Design many variations of passages of Lorem Ipsum available, but the majority have suffered alteration.',
				'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In ornare felis nunc, id porttitor dui blandit in. Etiam bibendum nibh sed lectus fermentum, id molestie ipsum facilisis. Nulla dignissim sapien eget massa mattis, nec porta dolor hendrerit.',
				'There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration. Design many variations of passages of Lorem Ipsum available, but the majority have suffered alteration.'
			),
			'custom_fields' => array(
				array(
					'position' => 'senior designer'
				),
				array(
					'position' => 'web developer'
				),
				array(
					'position' => 'CEO'
				)
			)
		);
		
		for( $i=0; $i<count( $sample_testimonials['titles'] ); $i++ ) {
			
			$post_data = array(
				'post_title'    => $sample_testimonials['titles'][$i],
				'post_content'  => $sample_testimonials['content'][$i],
				'post_status'   => 'publish',
				'post_type'			=> 'wproto_testimonials'
			);
			
			$post_id = wp_insert_post( $post_data );

			set_post_thumbnail( $post_id, $sample_images_ids[ rand( 0, count( $sample_images_ids ) - 1)] );
			
			// insert custom fields
			foreach( $sample_testimonials['custom_fields'][$i] as $k=>$v ) {
				update_post_meta( $post_id, $k, $v );
			}
			
		}
		
		/**
		 * Insert sample pages
		 **/
		
		/*****************************************************************************************************************
			Contacts page
		*****************************************************************************************************************/
		
		$page_data = array(
			'post_title'    => 'Example - Contact Page',
			'post_content'  => '',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		$custom_fields = array(
			'wproto_tpl_contact_email_to' => 'fakeemail@mailinator.com',
			'wproto_tpl_contact_success_text' => 'Message was sent! Thank you!',
			'wproto_tpl_contact_address' => '90210 Surgery Center, North Roxbury Drive, Beverly Hills, CA, United States',
			'wproto_tpl_contact_phone' => '+3 8 032 654 321 98',
			'wproto_tpl_contact_fax' => '+3 8 032 654 321 98',
			'wproto_tpl_contact_display_captcha' => 'yes',
			'wproto_tpl_contact_display_social' => 'no',
			'wproto_page_sidebar' => 'none',
			'wproto_tpl_contact_google_img' => WPROTO_THEME_URL . '/images/logo.png'
		);
		
		foreach( $custom_fields as $cf_k => $cf_v ) {
			update_post_meta( $page_id, $cf_k, $cf_v );
		}

		update_post_meta( $page_id, '_wp_page_template', 'page-tpl-contacts.php' );

		/*****************************************************************************************************************
			Blog - timeline page
		*****************************************************************************************************************/
		
		$page_data = array(
			'post_title'    => 'Example - Blog Timeline',
			'post_content'  => '',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		$custom_fields = array(
			'wproto_page_sidebar' => 'none',
			'wproto_content_layout' => 'timeline',
			'wproto_content_layout_display_page_text' => 'hide',
			'wproto_content_layout_posts_per_page' => 8,
			'wproto_content_pagination' => 'yes',
			'wproto_content_pagination_style' => 'ajax',
			'wproto_content_display_posts_type' => 'all',
			'wproto_content_display_posts_order' => 'date',
			'wproto_content_display_posts_sort' => 'DESC'
		);
		
		foreach( $custom_fields as $cf_k => $cf_v ) {
			update_post_meta( $page_id, $cf_k, $cf_v );
		}
		update_post_meta( $page_id, '_wp_page_template', 'page-tpl-blog.php' );
		
		/*****************************************************************************************************************
			Blog - Four Columns page
		*****************************************************************************************************************/
		
		$page_data = array(
			'post_title'    => 'Example - Blog Four Columns',
			'post_content'  => '',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		$custom_fields = array(
			'wproto_content_layout' => 'four_columns',
			'wproto_content_layout_display_page_text' => 'hide',
			'wproto_content_layout_posts_per_page' => 8,
			'wproto_content_pagination' => 'yes',
			'wproto_content_pagination_style' => 'ajax',
			'wproto_content_display_posts_type' => 'all',
			'wproto_content_display_posts_order' => 'date',
			'wproto_content_display_posts_sort' => 'DESC'
		);
		
		foreach( $custom_fields as $cf_k => $cf_v ) {
			update_post_meta( $page_id, $cf_k, $cf_v );
		}
		update_post_meta( $page_id, '_wp_page_template', 'page-tpl-blog.php' );
		
		/*****************************************************************************************************************
			Portfolio Hexagon
		*****************************************************************************************************************/
		
		$page_data = array(
			'post_title'    => 'Example - Portfolio Hexagon',
			'post_content'  => '',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		$custom_fields = array(
			'wproto_content_layout' => 'hexagon',
			'wproto_content_layout_display_page_text' => 'hide',
			'wproto_content_layout_posts_per_page' => 11,
			'wproto_content_layout_filters' => 'yes'
		);
		
		foreach( $custom_fields as $cf_k => $cf_v ) {
			update_post_meta( $page_id, $cf_k, $cf_v );
		}
		update_post_meta( $page_id, '_wp_page_template', 'page-tpl-portfolio.php' );
		
		/*****************************************************************************************************************
			Videos - Masonry Layout
		*****************************************************************************************************************/
		
		$page_data = array(
			'post_title'    => 'Example - Videos Masonry',
			'post_content'  => '',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		$custom_fields = array(
			'wproto_content_layout' => 'masonry',
			'wproto_content_layout_display_page_text' => 'hide',
			'wproto_content_layout_posts_per_page' => 10,
			'wproto_content_pagination' => 'yes',
			'wproto_content_pagination_style' => 'numeric',
			'wproto_content_display_posts_type' => 'all'
		);
		
		foreach( $custom_fields as $cf_k => $cf_v ) {
			update_post_meta( $page_id, $cf_k, $cf_v );
		}
		update_post_meta( $page_id, '_wp_page_template', 'page-tpl-videos.php' );
		
		/*****************************************************************************************************************
			Photoalbums - One Column Grid
		*****************************************************************************************************************/
		
		$page_data = array(
			'post_title'    => 'Example - Photoalbums One Column Grid',
			'post_content'  => '',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		$custom_fields = array(
			'wproto_content_layout' => 'one_column_grid',
			'wproto_content_layout_display_page_text' => 'hide',
			'wproto_content_layout_posts_per_page' => 10,
			'wproto_content_pagination' => 'yes',
			'wproto_content_pagination_style' => 'numeric',
			'wproto_content_display_posts_type' => 'all'
		);
		
		foreach( $custom_fields as $cf_k => $cf_v ) {
			update_post_meta( $page_id, $cf_k, $cf_v );
		}
		update_post_meta( $page_id, '_wp_page_template', 'page-tpl-photoalbums.php' );
		
		/*****************************************************************************************************************
			Catalog - Three Columns
		*****************************************************************************************************************/
		
		$page_data = array(
			'post_title'    => 'Example - Catalog Three Columns',
			'post_content'  => '',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		$custom_fields = array(
			'wproto_content_layout' => 'three_columns',
			'wproto_content_layout_display_page_text' => 'hide',
			'wproto_content_layout_posts_per_page' => 6,
			'wproto_content_pagination' => 'yes',
			'wproto_content_pagination_style' => 'ajax',
			'wproto_content_display_posts_type' => 'all'
		);
		
		foreach( $custom_fields as $cf_k => $cf_v ) {
			update_post_meta( $page_id, $cf_k, $cf_v );
		}
		update_post_meta( $page_id, '_wp_page_template', 'page-tpl-catalog.php' );
		
		/*****************************************************************************************************************
			Grid and typography
		*****************************************************************************************************************/
		$page_data = array(
			'post_title'    => 'Example - Grid and Text Layout',
			'post_content'  => '<div class="unit half"><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eleifend leo cursus, dapibus sapien at, tincidunt tortor. Suspendisse varius convallis magna id varius. Proin vitae eros at metus adipiscing tempor. Vivamus interdum dictum dui, ut convallis metus tincidunt quis. Quisque in aliquam erat. Sed laoreet eros quis molestie blandit. Ut quis justo sit amet urna mollis feugiat ut sed erat. Suspendisse tincidunt est eu porta tincidunt. Nam id odio in nulla placerat molestie. Mauris leo tortor, scelerisque et lacus id, eleifend fermentum velit. Aliquam vitae dolor vehicula, consectetur justo ac, blandit nisl. In hac habitasse platea dictumst. Donec sagittis libero ante, a ornare metus consequat at.</p></div>
<div class="unit half"><p>Donec a elementum leo. Vestibulum libero lorem, molestie posuere placerat sed, dapibus id leo. Sed in leo vulputate, hendrerit risus sed, pretium lorem. Nunc sodales arcu non diam laoreet, vitae adipiscing odio commodo. Sed suscipit nisl sed ipsum dapibus, sed tristique orci commodo. Praesent fringilla rutrum libero, porta fermentum est vestibulum non. Morbi dictum adipiscing malesuada. Nunc eros mi, imperdiet quis sodales eget, facilisis et nisi.</p></div>
<div class="unit one-third"><p>Nunc sodales arcu non diam laoreet, vitae adipiscing odio commodo. Sed suscipit nisl sed ipsum dapibus, sed tristique orci commodo. Praesent fringilla rutrum libero, porta fermentum est vestibulum non. Morbi dictum adipiscing malesuada. Nunc eros mi, imperdiet quis sodales eget, facilisis et nisi.</p></div>
<div class="unit one-third"><p>Nunc sodales arcu non diam laoreet, vitae adipiscing odio commodo. Sed suscipit nisl sed ipsum dapibus, sed tristique orci commodo. Praesent fringilla rutrum libero, porta fermentum est vestibulum non. Morbi dictum adipiscing malesuada. Nunc eros mi, imperdiet quis sodales eget, facilisis et nisi.</p></div>
<div class="unit one-third"><p>Nunc sodales arcu non diam laoreet, vitae adipiscing odio commodo. Sed suscipit nisl sed ipsum dapibus, sed tristique orci commodo. Praesent fringilla rutrum libero, porta fermentum est vestibulum non. Morbi dictum adipiscing malesuada. Nunc eros mi, imperdiet quis sodales eget, facilisis et nisi.</p></div>',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		/*****************************************************************************************************************
			Shortcodes - Audio
		*****************************************************************************************************************/
		$page_data = array(
			'post_title'    => 'Example - Audio Shortcode',
			'post_content'  => '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce auctor nisl ut mauris viverra vestibulum. Aenean felis ipsum, eleifend a interdum et, accumsan nec diam. Maecenas tempor arcu lorem, bibendum posuere eros tempor quis. Nulla sodales suscipit ante, sit amet condimentum neque egestas vitae. Maecenas ac tellus at eros dapibus blandit ac in orci. Proin diam augue, porttitor in nisi nec, rutrum venenatis metus. Fusce justo metus, molestie ac nulla quis, condimentum tincidunt erat. Cras at lobortis ipsum. Aenean lorem nisl, porta a diam vel, tincidunt suscipit odio. Aenean euismod varius purus sed ultricies. Pellentesque non eleifend mauris. Aliquam eleifend bibendum tellus, ac bibendum felis mollis nec. Fusce ac quam cursus nibh tincidunt consequat et et dui. Nunc imperdiet leo vel nisi feugiat pharetra. Sed ullamcorper velit sapien, quis dictum lorem elementum non.</p>

[audio src="http://themes.wplab.pro/galaxy/wp-content/uploads/sites/3/2013/12/originaldixielandjazzbandwithalbernard-stlouisblues.mp3"]',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		/*****************************************************************************************************************
			Shortcodes - Benefits
		*****************************************************************************************************************/
		$page_data = array(
			'post_title'    => 'Example - Benefits Shortcode',
			'post_content'  => '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus faucibus quis purus sed euismod. Nunc sit amet diam eget odio dapibus semper. Morbi in ullamcorper felis. Duis euismod nisi id porttitor pharetra. Aenean rutrum ultrices turpis eu varius. Mauris enim erat, placerat at adipiscing ut, elementum non mauris. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.</p>

[wproto_benefits show="all" cols="4" title="Our Benefits" limit="4" orderby="random" sort="ASC"]

<p>Curabitur vitae sapien rutrum, sodales ipsum a, ultricies nulla. Nunc porttitor pellentesque sem, sit amet adipiscing dui imperdiet non. Fusce fringilla vel nibh vitae accumsan. Cras ut diam interdum, euismod lacus vel, aliquam nisi.</p>',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		/*****************************************************************************************************************
			Shortcodes - Buttons
		*****************************************************************************************************************/
		$page_data = array(
			'post_title'    => 'Example - Button Shortcode',
			'post_content'  => '<div class="unit one-third">
<h4>Blue Small Button</h4>
<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam convallis nisl vitae turpis lobortis viverra. Phasellus massa mauris, dignissim et erat et, laoreet iaculis sapien.</p>

[wproto_button text="Blue button text" size="small" color="blue" link="http://themeforest.net/user/wplab/portfolio" new_window="yes"]

</div>
<div class="unit one-third">
<h4>Red Small Button</h4>
<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam convallis nisl vitae turpis lobortis viverra. Phasellus massa mauris, dignissim et erat et, laoreet iaculis sapien.</p>

[wproto_button text="Red button text" size="small" color="red" link="http://themeforest.net/user/wplab/portfolio" new_window="yes"]

</div>
<div class="unit one-third">
<h4>Green Small Button</h4>
<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam convallis nisl vitae turpis lobortis viverra. Phasellus massa mauris, dignissim et erat et, laoreet iaculis sapien.</p>

[wproto_button text="Green button text" size="small" color="green" link="http://themeforest.net/user/wplab/portfolio" new_window="yes"]

</div>',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		/*****************************************************************************************************************
			Shortcodes - Call to action
		*****************************************************************************************************************/
		$page_data = array(
			'post_title'    => 'Example - Call to action Shortcode',
			'post_content'  => '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam convallis nisl vitae turpis lobortis viverra. Phasellus massa mauris, dignissim et erat et, laoreet iaculis sapien. Etiam venenatis erat a augue laoreet, sed sodales orci fermentum. Vivamus ut dui egestas, suscipit risus sed, placerat leo. Maecenas leo diam, viverra in augue sed, tincidunt semper justo. Sed consectetur lobortis leo, vitae facilisis est posuere nec. Maecenas mi tortor, bibendum sed vestibulum id, lacinia pulvinar sem. In consequat non turpis eu ullamcorper. Aliquam id ante sit amet enim consectetur sagittis. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec dictum rhoncus rutrum. Fusce laoreet hendrerit felis, et laoreet augue feugiat at. Mauris cursus velit dui, a mollis eros viverra sit amet. Duis ut tempor arcu, ac aliquam metus. Ut dignissim ultricies lacus, id consequat turpis commodo id.</p>

[wproto_call_to_action button_text="Action button" button_color="#3492d1" button_text_color="#FFFFFF" title="Call to action block" title_color="#3c4247" text_content="Choose any colors you want. Aliquam id ante sit amet enim consectetur sagittis. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec dictum rhoncus rutrum. Fusce laoreet hendrerit felis, et laoreet augue feugiat at. Mauris cursus velit dui, a mollis eros viverra sit amet. Duis ut tempor arcu, ac aliquam metus. Ut dignissim ultricies lacus, id consequat turpis commodo id." content_color="#777f8a" show_button="yes" link="http://themeforest.net/user/wplab/portfolio" button_size="small" new_window="yes" icon="fa fa-bell-o" icon_color="#3492d1" border_color="#e6e6e6" background="#fafafa"]',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		/*****************************************************************************************************************
			Shortcodes - Catalog
		*****************************************************************************************************************/
		$page_data = array(
			'post_title'    => 'Example - Catalog items Shortcode',
			'post_content'  => '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse lacinia ante urna, vitae tempus lacus gravida sit amet. Nam ullamcorper sed elit ut hendrerit. Phasellus interdum consequat leo. Integer dignissim, sem nec semper faucibus, erat dolor egestas dui, in egestas magna erat lacinia lectus. Nulla eget cursus ipsum. Pellentesque ac accumsan libero. Curabitur varius dictum neque blandit commodo. Etiam porta adipiscing condimentum. Phasellus mauris elit, facilisis quis hendrerit id, varius fringilla leo. Nunc ac ligula pellentesque, tempor ligula id, sodales est. Duis fermentum nunc eu porta pellentesque. Duis blandit gravida aliquet. Nulla facilisi. Pellentesque vestibulum turpis metus, et posuere metus hendrerit at. Vivamus eget ipsum auctor, pharetra justo vel, vestibulum urna.</p>

[wproto_catalog cols="4" show="all" title="Catalog Items Shortcode Example" limit="8" orderby="rand" sort="ASC"]',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		/*****************************************************************************************************************
			Shortcodes - Partners
		*****************************************************************************************************************/
		$page_data = array(
			'post_title'    => 'Example - Our Clients Shortcode',
			'post_content'  => '<div class="unit whole">

<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus faucibus quis purus sed euismod. Nunc sit amet diam eget odio dapibus semper. Morbi in ullamcorper felis. Duis euismod nisi id porttitor pharetra. Aenean rutrum ultrices turpis eu varius. Mauris enim erat, placerat at adipiscing ut, elementum non mauris. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.</p>

</div>
<div class="unit two-fifths">

[wproto_clients_partners show="all" title="Our Clients" limit="7" orderby="random" sort="ASC"]

</div>
<div class="unit three-fifths">

<p>Curabitur vitae sapien rutrum, sodales ipsum a, ultricies nulla. Nunc porttitor pellentesque sem, sit amet adipiscing dui imperdiet non. Fusce fringilla vel nibh vitae accumsan. Cras ut diam interdum, euismod lacus vel, aliquam nisi. Phasellus quis mauris et quam vulputate sagittis sit amet non nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Maecenas blandit, nibh ut imperdiet rutrum, dui magna condimentum ligula, quis iaculis velit eros ac magna. Pellentesque ligula ante, convallis semper varius vel, placerat eget nunc. Nullam dapibus pharetra felis hendrerit feugiat. Curabitur volutpat eros a nisi blandit, vel adipiscing risus iaculis. Integer pretium feugiat commodo. Pellentesque magna ligula, lobortis non orci quis, eleifend elementum dui.</p>

</div>',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		/*****************************************************************************************************************
			Shortcodes - Contact Form
		*****************************************************************************************************************/
		$page_data = array(
			'post_title'    => 'Example - Contact Form Shortcode',
			'post_content'  => '<div class="unit whole">

<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam convallis nisl vitae turpis lobortis viverra. Phasellus massa mauris, dignissim et erat et, laoreet iaculis sapien. Etiam venenatis erat a augue laoreet, sed sodales orci fermentum. Vivamus ut dui egestas, suscipit risus sed, placerat leo. Maecenas leo diam, viverra in augue sed, tincidunt semper justo. Sed consectetur lobortis leo, vitae facilisis est posuere nec. Maecenas mi tortor, bibendum sed vestibulum id, lacinia pulvinar sem. In consequat non turpis eu ullamcorper. Aliquam id ante sit amet enim consectetur sagittis. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec dictum rhoncus rutrum. Fusce laoreet hendrerit felis, et laoreet augue feugiat at. Mauris cursus velit dui, a mollis eros viverra sit amet. Duis ut tempor arcu, ac aliquam metus. Ut dignissim ultricies lacus, id consequat turpis commodo id.</p>

</div>
<div class="unit half">
<h4>Lorem ipsum dolor</h4>
<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam convallis nisl vitae turpis lobortis viverra. Phasellus massa mauris, dignissim et erat et, laoreet iaculis sapien. Etiam venenatis erat a augue laoreet, sed sodales orci fermentum. Vivamus ut dui egestas, suscipit risus sed, placerat leo. Maecenas leo diam, viverra in augue sed, tincidunt semper justo. Sed consectetur lobortis leo, vitae facilisis est posuere nec. Maecenas mi tortor, bibendum sed vestibulum id, lacinia pulvinar sem. In consequat non turpis eu ullamcorper. Aliquam id ante sit amet enim consectetur sagittis. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec dictum rhoncus rutrum. Fusce laoreet hendrerit felis, et laoreet augue feugiat at. Mauris cursus velit dui, a mollis eros viverra sit amet. Duis ut tempor arcu, ac aliquam metus. Ut dignissim ultricies lacus, id consequat turpis commodo id.</p>

<p>Ut mattis tellus in libero rhoncus, pellentesque fringilla elit mollis. Sed est nunc, ultrices at fermentum vitae, condimentum a enim. In vitae dolor nibh. Maecenas tincidunt urna non dolor tristique blandit. Aenean nec arcu neque. Fusce ac lectus eget velit porttitor malesuada. Curabitur vehicula vestibulum turpis, quis fermentum sem facilisis non.</p>

</div>
<div class="unit half">

[wproto_contact_form form_id="52d2f1e30a46b" to="fakeemail@mailinator.com" subject="Test Email" title="Contact Form Shortcode" text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam convallis nisl vitae turpis lobortis viverra. Phasellus massa mauris, dignissim et erat et, laoreet iaculis sapien. Etiam venenatis erat a augue laoreet, sed sodales orci fermentum. Vivamus ut dui egestas, suscipit risus sed, placerat leo." captcha="yes"]

</div>
<div class="unit whole">

<p>Vivamus nec risus ac eros bibendum porta. Nulla pretium lobortis neque, id hendrerit tellus interdum in. Etiam congue eu nibh quis vestibulum. Aliquam luctus purus et velit porta commodo. Integer gravida eros non tortor gravida, at faucibus turpis mollis. Nam non venenatis eros. Vestibulum fringilla convallis condimentum. Sed placerat tellus vel felis malesuada rhoncus. Nulla dapibus sem id augue aliquet, id lacinia massa facilisis. Vestibulum sit amet elit et massa elementum fermentum nec non ipsum. Aliquam laoreet sodales orci eget egestas.</p>

</div>',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		/*****************************************************************************************************************
			Shortcodes - Divider
		*****************************************************************************************************************/
		$page_data = array(
			'post_title'    => 'Example - Divider Shortcode',
			'post_content'  => '<h4>Narrow Style</h4>
<p>Faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies ipsum velit ante sit amet imperdiet, felis enim. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit, a faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit.</p>

[wproto_divider style="narrow"]

<p>Faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies ipsum velit ante sit amet imperdiet, felis enim. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit, a faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit.</p>

[wproto_divider style="narrow"]

<p>Faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies ipsum velit ante sit amet imperdiet, felis enim. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit, a faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit.</p>
<h4>Wide Style</h4>
<p>Faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies ipsum velit ante sit amet imperdiet, felis enim. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit, a faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit.</p>

[wproto_divider style="wide"]

<p>Faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies ipsum velit ante sit amet imperdiet, felis enim. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit, a faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit.</p>

[wproto_divider style="wide"]

<p>Faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies ipsum velit ante sit amet imperdiet, felis enim. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit, a faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit.</p>
<h4>Gap</h4>
<p>Faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies ipsum velit ante sit amet imperdiet, felis enim. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit, a faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit.</p>

[wproto_divider style="gap"]

<p>Faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies ipsum velit ante sit amet imperdiet, felis enim. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit, a faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit.</p>

[wproto_divider style="gap"]

<p>Faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies ipsum velit ante sit amet imperdiet, felis enim. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit, a faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit.</p>
<h4>Double Gap</h4>
<p>Faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies ipsum velit ante sit amet imperdiet, felis enim. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit, a faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit.</p>

[wproto_divider style="double-gap"]

<p>Faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies ipsum velit ante sit amet imperdiet, felis enim. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit, a faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit.</p>

[wproto_divider style="double-gap"]

<p>Faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies ipsum velit ante sit amet imperdiet, felis enim. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit, a faucibus purus. Quisque dignissim, ante sit amet imperdiet ultricies. Dignissim, ante sit amet imperdiet ultricies, felis enim luctus leo, et cursus leo libero in nisi. Donec sit amet ipsum velit.</p>',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		/*****************************************************************************************************************
			Shortcodes - Google Map
		*****************************************************************************************************************/
		$page_data = array(
			'post_title'    => 'Example - Google Map Shortcode',
			'post_content'  => '<p>Quisque non libero aliquam, sollicitudin ante sed, ultricies orci. Cras vehicula, tortor ac laoreet molestie, diam risus lobortis nunc, vitae blandit tortor ipsum in lorem. Nullam imperdiet egestas sem, nec vulputate justo elementum nec. Maecenas ut sapien dui. Nam sit amet malesuada nunc, eget dignissim nulla. Nunc tincidunt ac dolor at commodo. Vivamus scelerisque ullamcorper arcu.</p>

<p>Vivamus nec risus ac eros bibendum porta. Nulla pretium lobortis neque, id hendrerit tellus interdum in. Etiam congue eu nibh quis vestibulum. Aliquam luctus purus et velit porta commodo. Integer gravida eros non tortor gravida, at faucibus turpis mollis. Nam non venenatis eros. Vestibulum fringilla convallis condimentum. Sed placerat tellus vel felis malesuada rhoncus. Nulla dapibus sem id augue aliquet, id lacinia massa facilisis. Vestibulum sit amet elit et massa elementum fermentum nec non ipsum. Aliquam laoreet sodales orci eget egestas.</p>

[wproto_map address="1332 Ocean Park Blvd, Santa Monica, CA 90405"]',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		/*****************************************************************************************************************
			Shortcodes - Highlighted text
		*****************************************************************************************************************/
		$page_data = array(
			'post_title'    => 'Example - Highlighted Text',
			'post_content'  => 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam convallis nisl vitae turpis lobortis viverra. [wproto_highlight color="#dd3333" content="Some highlighted text. Choose any color you want."] Phasellus massa mauris, dignissim et erat et, laoreet iaculis sapien. Etiam venenatis erat a augue laoreet, sed sodales orci fermentum. Vivamus ut dui egestas, suscipit risus sed, placerat leo. Maecenas leo diam, viverra in augue sed, tincidunt semper justo. Sed consectetur lobortis leo, vitae facilisis est posuere nec. Maecenas mi tortor, bibendum sed vestibulum id, lacinia pulvinar sem. In consequat non turpis eu ullamcorper. Aliquam id ante sit amet enim consectetur sagittis. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec dictum rhoncus rutrum. Fusce laoreet hendrerit felis, et laoreet augue feugiat at. Mauris cursus velit dui, a mollis eros viverra sit amet. Duis ut tempor arcu, ac aliquam metus. Ut dignissim ultricies lacus, id consequat turpis commodo id.',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		/*****************************************************************************************************************
			Shortcodes - Progress Bars
		*****************************************************************************************************************/
		$page_data = array(
			'post_title'    => 'Example - Progress Bars',
			'post_content'  => '<div class="unit half">

<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam convallis nisl vitae turpis lobortis viverra. Phasellus massa mauris, dignissim et erat et, laoreet iaculis sapien. Etiam venenatis erat a augue laoreet, sed sodales orci fermentum. Vivamus ut dui egestas, suscipit risus sed, placerat leo. Maecenas leo diam, viverra in augue sed, tincidunt semper justo. Sed consectetur lobortis leo, vitae facilisis est posuere nec. Maecenas mi tortor, bibendum sed vestibulum id, lacinia pulvinar sem. In consequat non turpis eu ullamcorper. Aliquam id ante sit amet enim consectetur sagittis. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec dictum rhoncus rutrum. Fusce laoreet hendrerit felis, et laoreet augue feugiat at. Mauris cursus velit dui, a mollis eros viverra sit amet. Duis ut tempor arcu, ac aliquam metus. Ut dignissim ultricies lacus, id consequat turpis commodo id.</p>

</div>
<div class="unit half">

<p>Sed est nunc, ultrices at fermentum vitae, condimentum a enim. In vitae dolor nibh. Maecenas tincidunt urna non dolor tristique blandit.</p>

[wproto_progress titles="Photography|Web design|Print design|Identity|SEO and PHP code" values="85|94|67|58|95"]

</div>',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		/*****************************************************************************************************************
			Shortcodes - Tabs
		*****************************************************************************************************************/
		$page_data = array(
			'post_title'    => 'Example - Tabs Shortcode',
			'post_content'  => '<div class="unit whole">

<p>Cras sed dictum felis. Aliquam vitae est luctus, facilisis tellus quis, eleifend turpis. Cras suscipit interdum condimentum. Sed vitae aliquet justo, vitae scelerisque nulla. In hendrerit, ante nec aliquet pulvinar, nibh lectus congue sem, sit amet dictum nibh neque nec elit. Mauris at augue a diam gravida interdum. Quisque volutpat justo massa, vel semper massa pellentesque sit amet. Etiam porta mi et ullamcorper ultricies. Donec aliquam massa nec rutrum dictum. Sed hendrerit faucibus sapien, eget laoreet lorem interdum rhoncus. Sed sagittis risus non elit commodo fringilla. Nunc sollicitudin nibh euismod viverra blandit. Aliquam erat volutpat.</p>

</div>
<div class="unit whole">[wproto_tabs][tab title="Seo and code"]There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour. If you are going to use a passage of Lorem Ipsum, you need to be sure there isnt anything embarrassing.All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words. Combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable.[/tab][tab title="Web design"]The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc. There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which dont look even slightly believable.It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc. There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which dont look even slightly believable.[/tab][tab title="Print"]Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus rutrum odio a mi interdum luctus. Mauris laoreet sapien sit amet tellus molestie, vitae porta quam dictum. Praesent in rhoncus tortor. Praesent suscipit felis ut tincidunt cursus. Ut id nisi ac erat consectetur tincidunt. Nunc posuere justo non consectetur faucibus.Aliquam id libero nec sapien dictum ornare. Donec in nisl ac nisl molestie pulvinar nec ultricies metus. In varius lorem sem, id tempor eros fringilla et. Vivamus sodales nisl libero, et blandit metus commodo in. Nulla et placerat urna, ac scelerisque ligula.[/tab][/wproto_tabs]</div>',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		/*****************************************************************************************************************
			Shortcodes - Team Shortcode
		*****************************************************************************************************************/
		$page_data = array(
			'post_title'    => 'Example - Team Shortcode',
			'post_content'  => '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce fringilla, enim vitae malesuada convallis, velit tortor sodales neque, nec lobortis risus neque et tellus. Fusce diam nisl, volutpat sit amet fringilla vel, tempor vel mi. Maecenas lobortis dui et consectetur pulvinar. Nulla at vestibulum mauris. Integer ut erat lorem. Nulla vestibulum porttitor mi nec dignissim. Donec euismod arcu id venenatis hendrerit.</p>

[wproto_team cols="4" show="all" title="Our Team" limit="8" orderby="rand" sort="ASC"]',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		/*****************************************************************************************************************
			Shortcodes - Testimonials Shortcode
		*****************************************************************************************************************/
		$page_data = array(
			'post_title'    => 'Example - Testimonials Shortcode',
			'post_content'  => '<div class="unit whole">
<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce fringilla, enim vitae malesuada convallis, velit tortor sodales neque, nec lobortis risus neque et tellus. Fusce diam nisl, volutpat sit amet fringilla vel, tempor vel mi. Maecenas lobortis dui et consectetur pulvinar. Nulla at vestibulum mauris. Integer ut erat lorem. Nulla vestibulum porttitor mi nec dignissim. Donec euismod arcu id venenatis hendrerit. Sed nec risus laoreet, semper quam at, consectetur dolor. Nunc eget lobortis purus. Donec cursus leo eget sem aliquam, eget scelerisque magna condimentum. Nulla mattis magna et augue fringilla blandit. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris convallis fringilla magna. Pellentesque vel erat nisi. Vivamus dui arcu, sagittis consectetur aliquet eu, posuere at orci. Nulla consequat faucibus eros quis porttitor.</p>
</div>
<div class="unit two-thirds">
<p>Duis molestie venenatis tempus. Aliquam hendrerit metus eget tellus sagittis ultricies. Quisque posuere sagittis ligula, sed lobortis mi commodo eu. Sed eu porta velit, ac ullamcorper odio. Vivamus eget ornare metus. Morbi fermentum, purus in lacinia aliquam, dui velit lobortis leo, eget egestas sapien risus at nisi. Vivamus at tellus accumsan, accumsan purus sit amet, semper dui. Cras et ante ut odio tempor ultricies. Nunc consequat vehicula lorem, nec auctor felis blandit sit amet. Nullam consectetur dolor et libero bibendum, vel faucibus nisi tempor. Nunc tristique sed velit molestie dictum. Interdum et malesuada fames ac ante ipsum primis in faucibus. Phasellus ac varius est, nec adipiscing enim. In non vulputate tortor.</p>
<p>Aliquam varius posuere risus ut aliquam. Vestibulum ipsum arcu, semper nec imperdiet dapibus, rhoncus et eros. Nullam eget magna lectus. Donec viverra ultricies imperdiet. Vestibulum dictum, sem a consectetur facilisis, augue nunc consectetur lorem, vel posuere felis urna ut lorem. Morbi vulputate leo a lacus interdum, at semper augue dignissim. Etiam mollis sem sit amet quam viverra laoreet. Vivamus magna lectus, consectetur in elit sit amet, vehicula venenatis lorem. Donec porta elit at dui ultrices rutrum. Etiam euismod a orci eget dignissim. In id ultrices sapien, ut laoreet neque. Cras at massa sit amet sem scelerisque pharetra a quis mauris. Aliquam at nisl non justo eleifend tempor ut a risus.</p>
</div>
<div class="unit one-third">
[wproto_testimonials show="all" title="Testimonials Shortcode" limit="5" orderby="random" sort="ASC"]
</div>',
			'post_status'   => 'publish',
			'post_type'			=> 'page'
		);
		
		$page_id = wp_insert_post( $page_data );
		
		die;
	}

}