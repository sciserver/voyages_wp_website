<?php
	// do not show comments for password-protected posts and pages
	if ( post_password_required()): return; endif;
	global $wpl_galaxy_wp;
?>

<div id="comments" data-appear-animation="fadeIn">

<?php if( is_page() && !comments_open()): ?>

	<!-- Show nothing ... -->

<?php elseif( is_singular()): ?>

	<?php if( have_comments()): ?>

		<h3><?php printf( _n( '<span>1</span> comment', '<span>%1$s</span> comments', get_comments_number(), 'wproto' ), number_format_i18n( get_comments_number())); ?>:</h3>

		<?php if ( have_comments()) : ?>
        
		<ol class="comment-list">
			<?php wp_list_comments( array( 'format' => 'html5', 'style' => 'ol', 'callback' => 'wproto_comments_callback' )); ?>
		</ol>
        
		<?php if ( get_comment_pages_count() > 1 && get_option( 'page_comments')): // are there comments to navigate through ?>
		<div class="comments-pagination">
			<?php paginate_comments_links( array('prev_text' => '&laquo;', 'next_text' => '&raquo;') ); ?>
			<div class="clear"></div>
		</div>
		<?php endif; // check for comment navigation ?>

	<?php endif; ?>

<?php endif; ?>

<div id="respond" data-appear-animation="fadeIn">

	<h3 id="reply-title"><?php comment_form_title( __( 'Leave a Comment', 'wproto'), __( 'Leave a Comment to %s', 'wproto') ); ?></h3>
	<small class="cancel-reply"><?php cancel_comment_reply_link(); ?></small>
    
	<?php if( comments_open()): ?>

		<?php if ( get_option( 'comment_registration') && !$user_ID ): ?>
		
		<?php get_template_part( 'part', 'oauth' ); ?>
		
		<?php else: ?>

			<form action="<?php echo home_url('/wp-comments-post.php'); ?>" method="post" id="commentform">
			<?php if ( $user_ID): ?>
		<?php else: ?>

			<?php get_template_part( 'part', 'oauth' ) ?>
			
			<div class="wrapper-block ib half comment-form-author">
				<label class="label" for="author"><?php _e( 'Name', 'wproto'); ?> <span class="required">*</span></label>
				<div class="input">
					<input class="text" id="author" name="author" type="text" value="" size="30" />
				</div>
				<div class="clear"></div>
			</div>

			<div class="wrapper-block ib half comment-form-email">
				<label class="label" for="email"><?php _e( 'Email', 'wproto'); ?> <span class="required">*</span></label>
				<div class="input">
					<input class="text" id="email" name="email" type="text" value="" size="30" />
				</div>
			</div>
            
		<?php endif; ?>

			<div class="wrapper-block comment-form-comment">
				<label class="label" for="comment"><?php _e( 'Comment', 'wproto'); ?> <span class="required">*</span></label>
				<div class="input">
					<textarea class="textarea" id="comment" name="comment" cols="45" rows="8"></textarea>
				</div>
				<div class="clear"></div>
			</div>
			
			<?php
				$captcha_enabled = $wpl_galaxy_wp->get_option( 'enable_at_comments' );
				$hide_from_logged = $wpl_galaxy_wp->get_option( 'hide_from_logged' );
				
				if( ((is_user_logged_in() && $hide_from_logged != 'yes') || !is_user_logged_in()) && $captcha_enabled == 'yes' ):
			?>
			<div class="wrapper-block comment-form-comment">
				<label class="label" for="captcha"><?php _e( 'Captcha', 'wproto'); ?> <span class="required">*</span></label>
				<?php $wpl_galaxy_wp->controller->captcha->generate_captcha_phrase(); ?>
				<div class="clear"></div>
			</div>
			<?php
				endif;																
			?>

			<div class="wrapper-block form-submit">
				<?php comment_id_fields(); ?>
				<input name="submit" type="submit" class="btn" id="submit" value="<?php _e( 'Post Comment', 'wproto'); ?>" />	
				
			</div>
            
			<?php do_action( 'comment_form', $post->ID); ?>

	</form>
        
	<?php endif; ?>
    
	<?php else: ?>
    
		<p class="comments-closed"><?php _e( 'Comments are closed.', 'wproto'); ?></p>
    
	<?php endif; ?>
	
</div>

<?php endif; ?>

</div>

<?php
/**
	* Comments callback function
 **/
function wproto_comments_callback( $comment, $args, $depth) {
	global $wpl_galaxy_wp;
	$GLOBALS['comment'] = $comment;
    
	switch ( $comment->comment_type ) :
		case '':
	?>
		<li <?php comment_class(); ?> id="comment-<?php comment_ID(); ?>">
			<div class="comment-inside" id="comment-content-<?php comment_ID(); ?>">
			
				<div class="comment-avatar">
					<div><?php $avatar_size = wpl_galaxy_wp_utils::is_retina() ? 140 : 70; echo get_avatar( $comment, $avatar_size ); ?></div>
				</div>
			
				<div class="comment-data">
					<span class="author">
						<?php echo get_comment_author_link(); ?>
					</span>
					<span class="time">
						<span><?php echo get_comment_date( $wpl_galaxy_wp->get_option('date_format') ); ?></span>
					</span>

				</div>
            
				<div class="comment-content">
					<?php comment_text(); ?>
				</div>
				
				<div class="comment-reply">
					<?php comment_reply_link( array_merge( $args, array( 'add_below' => 'comment-content', 'reply_text' => __( 'Reply', 'wproto' ) . ' <i class="arrow-keep-reading"></i>', 'depth' => $depth, 'max_depth' => $args['max_depth'] ) ), get_comment_ID(), get_the_ID() ); ?>  
					<?php wpl_galaxy_wp_front::likes( get_comment_ID(), 'comment' ); ?>
				</div>
				
			</div>

	<?php
		break;
			case 'pingback'  :
			case 'trackback' :
	?>
		<li class="post pingback">
			<div class="comment-data">
				<p><?php _e( 'Pingback', 'wproto' ); ?>: <?php comment_author_link(); ?></p>
			</div>
	<?php
		break;
	endswitch;
}