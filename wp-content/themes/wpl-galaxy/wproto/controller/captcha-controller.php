<?php
/**
 * Captcha controller
 * based on MathCaptcha http://www.dfactory.eu/plugins/math-captcha/
 **/
class wpl_galaxy_wp_captcha_controller extends wpl_galaxy_wp_base_controller {
	
	private $time = 3600;
	private $crypt_key = 'f*DwUtJOXSZwlghZwn}3VS';	
	public $session_id = '';
	
	public function __construct() {

		add_action( 'after_setup_theme', array( $this, 'init_session'), 1);
		add_filter( 'preprocess_comment', array( $this, 'add_comment_with_captcha'));
		
		add_action( 'wp_ajax_wproto_check_captcha_answer', array( $this, 'ajax_check_captcha_answer' ) );
		add_action( 'wp_ajax_nopriv_wproto_check_captcha_answer', array( $this, 'ajax_check_captcha_answer' ) );
		
	}
	
	
	/**
	 * Init math captcha session
	 **/
	function init_session() {

		if( isset( $_COOKIE['wproto_captcha_session_id'])) {
			$this->session_id = $_COOKIE['wproto_captcha_session_id'];
		} else {
			$this->session_id = substr( md5( wp_generate_password( 128, TRUE, TRUE ) . time() ), 16 );
		}
		
		@setcookie( 'wproto_captcha_session_id', $this->session_id, current_time('timestamp', TRUE) + $this->time, COOKIEPATH, COOKIE_DOMAIN);
			
	}
	
	/**
	 * Generates captcha
	 **/ 
	public function generate_captcha_phrase() {
		global $wproto;
		
		// generate inique form ID
		$captcha_id = substr( md5( wp_generate_password( 30, TRUE, TRUE ) . time() ), 8, 8 );
		
		$ops = array(
			'plus' => '+',
			'minus' => '-',
			'multiply' => '&#215;',
			'division' => '&#247;',
		);

		$operations = array();
		$input = '<input type="hidden" class="wproto-captcha-input-id" name="wproto_captcha_id" value="' . $captcha_id . '" />
		<input type="text" size="2" class="wproto-captcha-input" name="wproto-captcha-value" value="" />';

		//available operations
		$captcha_diff = $this->get_option( 'captcha_difficult' );
		$operations = $captcha_diff == NULL ? array('minus') : $captcha_diff;

		//available groups
		$groups = array('numbers');

		//number of groups
		$ao = count($groups);

		//operation
		$rnd_op = $operations[mt_rand(0, count($operations) - 1)];
		$number[3] = $ops[$rnd_op];

		//place where to put empty input
		$rnd_input = mt_rand(0, 2);

		switch($rnd_op)
		{
			case 'plus':
				if($rnd_input === 0)
				{
					$number[0] = mt_rand(1, 10);
					$number[1] = mt_rand(1, 89);
				}
				elseif($rnd_input === 1)
				{
					$number[0] = mt_rand(1, 89);
					$number[1] = mt_rand(1, 10);
				}
				elseif($rnd_input === 2)
				{
					$number[0] = mt_rand(1, 9);
					$number[1] = mt_rand(1, 10 - $number[0]);
				}

				$number[2] = $number[0] + $number[1];
				break;

			case 'minus':
				if($rnd_input === 0)
				{
					$number[0] = mt_rand(2, 10);
					$number[1] = mt_rand(1, $number[0] - 1);
				}
				elseif($rnd_input === 1)
				{
					$number[0] = mt_rand(11, 99);
					$number[1] = mt_rand(1, 10);
				}
				elseif($rnd_input === 2)
				{
					$number[0] = mt_rand(11, 99);
					$number[1] = mt_rand($number[0] - 10, $number[0] - 1);
				}

				$number[2] = $number[0] - $number[1];
				break;

			case 'multiply':
				if($rnd_input === 0)
				{
					$number[0] = mt_rand(1, 10);
					$number[1] = mt_rand(1, 9);
				}
				elseif($rnd_input === 1)
				{
					$number[0] = mt_rand(1, 9);
					$number[1] = mt_rand(1, 10);
				}
				elseif($rnd_input === 2)
				{
					$number[0] = mt_rand(1, 10);
					$number[1] = ($number[0] > 5 ? 1 : ($number[0] === 4 && $number[0] === 5 ? mt_rand(1, 2) : ($number[0] === 3 ? mt_rand(1, 3) : ($number[0] === 2 ? mt_rand(1, 5) : mt_rand(1, 10)))));
				}

				$number[2] = $number[0] * $number[1];
				break;

			case 'division':
				if($rnd_input === 0)
				{
					$divide = array(2 => array(1, 2), 3 => array(1, 3), 4 => array(1, 2, 4), 5 => array(1, 5), 6 => array(1, 2, 3, 6), 7 => array(1, 7), 8 => array(1, 2, 4, 8), 9 => array(1, 3, 9), 10 => array(1, 2, 5, 10));
					$number[0] = mt_rand(2, 10);
					$number[1] = $divide[$number[0]][mt_rand(0, count($divide[$number[0]]) - 1)];
				}
				elseif($rnd_input === 1)
				{
					$divide = array(1 => 99, 2 => 49, 3 => 33, 4 => 24, 5 => 19, 6 => 16, 7 => 14, 8 => 12, 9 => 11, 10 => 9);
					$number[1] = mt_rand(1, 10);
					$number[0] = $number[1] * mt_rand(1, $divide[$number[1]]);
				}
				elseif($rnd_input === 2)
				{
					$divide = array(1 => 99, 2 => 49, 3 => 33, 4 => 24, 5 => 19, 6 => 16, 7 => 14, 8 => 12, 9 => 11, 10 => 9);
					$number[2] = mt_rand(1, 10);
					$number[0] = $number[2] * mt_rand(1, $divide[$number[2]]);
					$number[1] = (int)($number[0] / $number[2]);
				}

				if(!isset($number[2]))
				{
					$number[2] = (int)($number[0] / $number[1]);
				}
				break;
		}

		//words
		if($ao === 1 && $groups[0] === 'words')
		{
			if($rnd_input === 0)
			{
				$number[1] = $this->numberToWords($number[1]);
				$number[2] = $this->numberToWords($number[2]);
			}
			elseif($rnd_input === 1)
			{
				$number[0] = $this->numberToWords($number[0]);
				$number[2] = $this->numberToWords($number[2]);
			}
			elseif($rnd_input === 2)
			{
				$number[0] = $this->numberToWords($number[0]);
				$number[1] = $this->numberToWords($number[1]);
			}
		}
		//numbers and words
		elseif($ao === 2)
		{
			if($rnd_input === 0)
			{
				if(mt_rand(1, 2) === 2)
				{
					$number[1] = $this->numberToWords($number[1]);
					$number[2] = $this->numberToWords($number[2]);
				}
				else
					$number[$tmp = mt_rand(1, 2)] = $this->numberToWords($number[$tmp]);
			}
			elseif($rnd_input === 1)
			{
				if(mt_rand(1, 2) === 2)
				{
					$number[0] = $this->numberToWords($number[0]);
					$number[2] = $this->numberToWords($number[2]);
				}
				else
					$number[$tmp = array_rand(array(0 => 0, 2 => 2), 1)] = $this->numberToWords($number[$tmp]);
			}
			elseif($rnd_input === 2)
			{
				if(mt_rand(1, 2) === 2)
				{
					$number[0] = $this->numberToWords($number[0]);
					$number[1] = $this->numberToWords($number[1]);
				}
				else
					$number[$tmp = mt_rand(0, 1)] = $this->numberToWords($number[$tmp]);
			}
		}

		//position of empty input
		if($rnd_input === 0)
			$return = $input.' '.$number[3].' '.$this->encode_operation($number[1]).' = '.$this->encode_operation($number[2]);
		elseif($rnd_input === 1)
			$return = $this->encode_operation($number[0]).' '.$number[3].' '.$input.' = '.$this->encode_operation($number[2]);
		elseif($rnd_input === 2)
			$return = $this->encode_operation($number[0]).' '.$number[3].' '.$this->encode_operation($number[1]).' = '.$input;

		set_transient( 'wprc_' . $this->session_id . '_' . $captcha_id, sha1( $this->crypt_key . $number[$rnd_input] . $this->session_id, FALSE), $this->time );
		echo $return;
	}
	
	/**
	 * Encodes chars
	*/
	private function encode_operation( $string ) {
		$chars = str_split( $string );
		$seed = mt_rand( 0, (int)abs( crc32( $string) / strlen( $string)));

		foreach($chars as $key => $char)
		{
			$ord = ord($char);

			//ignore non-ascii chars
			if($ord < 128)
			{
				//pseudo "random function"
				$r = ($seed * (1 + $key)) % 100;

				if($r > 60 && $char !== '@') {} // plain character (not encoded), if not @-sign
				elseif($r < 45) $chars[$key] = '&#x'.dechex($ord).';'; //hexadecimal
				else $chars[$key] = '&#'.$ord.';'; //decimal (ascii)
			}
		}

		return implode('', $chars);
	}


	/**
	 * Converts numbers to words
	 **/
	private function numberToWords( $number ){
		$words = array(
			1 => __( 'one', 'wproto'),
			2 => __( 'two', 'wproto'),
			3 => __( 'three', 'wproto'),
			4 => __( 'four', 'wproto'),
			5 => __( 'five', 'wproto'),
			6 => __( 'six', 'wproto'),
			7 => __( 'seven', 'wproto'),
			8 => __( 'eight', 'wproto'),
			9 => __( 'nine', 'wproto'),
			10 => __( 'ten', 'wproto'),
			11 => __( 'eleven', 'wproto'),
			12 => __( 'twelve', 'wproto'),
			13 => __( 'thirteen', 'wproto'),
			14 => __( 'fourteen', 'wproto'),
			15 => __( 'fifteen', 'wproto'),
			16 => __( 'sixteen', 'wproto'),
			17 => __( 'seventeen', 'wproto'),
			18 => __( 'eighteen', 'wproto'),
			19 => __( 'nineteen', 'wproto'),
			20 => __( 'twenty', 'wproto'),
			30 => __( 'thirty', 'wproto'),
			40 => __( 'forty', 'wproto'),
			50 => __( 'fifty', 'wproto'),
			60 => __( 'sixty', 'wproto'),
			70 => __( 'seventy', 'wproto'),
			80 => __( 'eighty', 'wproto'),
			90 => __( 'ninety', 'wproto')
		);

		if( isset( $words[$number]))
			return $words[$number];
		else
		{
			$reverse = FALSE;

			switch( get_bloginfo('language') )
			{
				case 'de-DE':
					$spacer = 'und';
					$reverse = TRUE;
					break;

				case 'nl-NL':
					$spacer = 'en';
					$reverse = TRUE;
					break;

				case 'pl-PL':
					$spacer = ' ';
					break;

				case 'en-EN':
				default:
					$spacer = '-';
			}

			$first = (int)(substr($number, 0, 1) * 10);
			$second = (int)substr($number, -1);

			return ($reverse === FALSE ? $words[$first].$spacer.$words[$second] : $words[$second].$spacer.$words[$first]);
		}
	}
	
	/**
	 * Check for captcha at comments
	 **/
	function add_comment_with_captcha( $comment ) {
		global $wproto;

		$captcha_enabled = $this->get_option( 'enable_at_comments' );
		$hide_from_logged = $this->get_option( 'hide_from_logged' );
		
		if( ((is_user_logged_in() && $hide_from_logged != 'yes') || !is_user_logged_in()) && $captcha_enabled == 'yes' ):
		
			if( isset( $_POST['wproto-captcha-value'] ) && ( !is_admin() || DOING_AJAX ) && ( $comment['comment_type'] === '' || $comment['comment_type'] === 'comment' ) ) {
			
				if( $_POST['wproto-captcha-value'] !== '') {
															
					if( $this->session_id !== '' && get_transient( 'wprc_' . $this->session_id . '_' . $_POST['wproto_captcha_id'] ) !== FALSE) {
					
						if( $this->validate_captcha_answer( $_POST['wproto-captcha-value'], $_POST['wproto_captcha_id'] ) )
							return $comment;
						else
							wp_die( __('Invalid captcha value.', 'wproto') );
					}
					else
						wp_die( __('Captcha time expired.', 'wproto') );
				}
				else
					wp_die( __('Please enter captcha value.', 'wproto') );
			}
			else
				return $comment;
		
		else:
			return $comment;
		endif;
		
	}
	
	/**
	 * Validate captcha answer
	 **/
	function validate_captcha_answer( $answer, $captcha_id ) {		
		return strcmp( get_transient( 'wprc_' . $this->session_id . '_' . $captcha_id ), sha1( $this->crypt_key . $answer . $this->session_id, FALSE )) === 0;
	}
	
	/**
	 * Check captcha answer via AJAX
	 **/
	function ajax_check_captcha_answer() {
		echo $this->validate_captcha_answer( $_POST['answer'], $_POST['wproto_captcha_id'] ) ? 'ok' : 'false';
		die;
	}
	
}