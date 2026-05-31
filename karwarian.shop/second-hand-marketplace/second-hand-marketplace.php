<?php
/**
 * Plugin Name: Second Hand Marketplace (OLX-style)
 * Description: Second-hand listings with moderation: submissions stay pending until an admin approves or rejects them.
 * Version: 1.3.0
 * Author: Cursor AI
 * Text Domain: second-hand-marketplace
 */

if (!defined('ABSPATH')) {
	exit;
}

define('SHM_VERSION', '1.3.0');
define('SHM_MAX_IMAGES', 10);
define('SHM_PATH', plugin_dir_path(__FILE__));
define('SHM_URL', plugin_dir_url(__FILE__));

register_activation_hook(__FILE__, 'shm_activate');
function shm_activate(): void {
	shm_register_post_type();
	flush_rewrite_rules();
	$existing = get_posts(
		array(
			'post_type'      => 'second_hand_item',
			'post_status'    => 'any',
			'posts_per_page' => 1,
			'fields'         => 'ids',
		)
	);
	if (!empty($existing)) {
		return;
	}
	$demos = array(
		array(
			'title'   => __('Sample: Office chair (used)', 'second-hand-marketplace'),
			'content' => __('Comfortable mesh chair. Minor wear on armrests. Pickup only.', 'second-hand-marketplace'),
			'price'   => '₹2,200',
			'loc'     => __('Indiranagar, Bengaluru', 'second-hand-marketplace'),
		),
		array(
			'title'   => __('Sample: Mountain bike 26"', 'second-hand-marketplace'),
			'content' => __('Single owner, serviced last month. Tyres in good condition.', 'second-hand-marketplace'),
			'price'   => '₹8,500',
			'loc'     => __('Koramangala, Bengaluru', 'second-hand-marketplace'),
		),
	);
	foreach ($demos as $row) {
		$pid = wp_insert_post(
			array(
				'post_title'   => $row['title'],
				'post_content' => $row['content'],
				'post_status'  => 'publish',
				'post_type'    => 'second_hand_item',
				'post_author'  => 1,
			),
			true
		);
		if (!is_wp_error($pid)) {
			update_post_meta($pid, 'shm_price', $row['price']);
			update_post_meta($pid, 'shm_location', $row['loc']);
		}
	}
}

/**
 * Load grid/form styles whenever shortcodes render (works in block themes too).
 */
function shm_enqueue_frontend_style(): void {
	wp_enqueue_style('shm-frontend', SHM_URL . 'assets/frontend.css', array(), SHM_VERSION);
}

function shm_enqueue_frontend_scripts(): void {
	wp_enqueue_script('shm-frontend', SHM_URL . 'assets/shm.js', array(), SHM_VERSION, true);
}

add_action('wp_enqueue_scripts', 'shm_enqueue_on_listing_pages');
function shm_enqueue_on_listing_pages(): void {
	global $post;
	if (is_singular('second_hand_item')) {
		shm_enqueue_frontend_style();
		shm_enqueue_frontend_scripts();
		return;
	}
	if ($post instanceof WP_Post && (has_shortcode($post->post_content, 'shm_sell_form') || has_shortcode($post->post_content, 'shm_listings'))) {
		shm_enqueue_frontend_style();
		if (has_shortcode($post->post_content, 'shm_sell_form')) {
			shm_enqueue_frontend_scripts();
		}
	}
}

/**
 * Status for new front-end submissions. Default pending (admin must approve).
 * Filter `shm_new_listing_post_status` to return `publish` for instant listing (not recommended).
 */
function shm_new_listing_status(): string {
	$status = apply_filters('shm_new_listing_post_status', 'pending');
	return in_array($status, array('publish', 'pending', 'draft'), true) ? $status : 'pending';
}

add_action('init', 'shm_register_post_type');
function shm_register_post_type(): void {
	register_post_type(
		'second_hand_item',
		array(
			'labels'              => array(
				'name'          => __('Second-hand items', 'second-hand-marketplace'),
				'singular_name' => __('Second-hand item', 'second-hand-marketplace'),
				'add_new_item'  => __('Add item', 'second-hand-marketplace'),
			),
			'public'              => true,
			'has_archive'         => true,
			'rewrite'             => array('slug' => 'second-hand'),
			'supports'            => array('title', 'editor', 'thumbnail', 'excerpt'),
			'menu_icon'           => 'dashicons-products',
			'show_in_rest'        => true,
			'capability_type'     => 'post',
			'map_meta_cap'        => true,
		)
	);
}

add_action('init', 'shm_register_meta');
function shm_register_meta(): void {
	register_post_meta(
		'second_hand_item',
		'shm_price',
		array(
			'type'              => 'string',
			'single'            => true,
			'show_in_rest'      => true,
			'sanitize_callback' => 'sanitize_text_field',
			'auth_callback'     => '__return_true',
		)
	);
	register_post_meta(
		'second_hand_item',
		'shm_contact',
		array(
			'type'              => 'string',
			'single'            => true,
			'show_in_rest'      => true,
			'sanitize_callback' => 'sanitize_text_field',
			'auth_callback'     => '__return_true',
		)
	);
	register_post_meta(
		'second_hand_item',
		'shm_location',
		array(
			'type'              => 'string',
			'single'            => true,
			'show_in_rest'      => true,
			'sanitize_callback' => 'sanitize_text_field',
			'auth_callback'     => '__return_true',
		)
	);
	register_post_meta(
		'second_hand_item',
		'shm_email',
		array(
			'type'              => 'string',
			'single'            => true,
			'show_in_rest'      => true,
			'sanitize_callback' => 'sanitize_email',
			'auth_callback'     => '__return_true',
		)
	);
	register_post_meta(
		'second_hand_item',
		'shm_gallery',
		array(
			'type'              => 'array',
			'single'            => true,
			'show_in_rest'      => array(
				'schema' => array(
					'type'  => 'array',
					'items' => array( 'type' => 'integer' ),
				),
			),
			'sanitize_callback' => 'shm_sanitize_gallery_meta',
			'auth_callback'     => '__return_true',
		)
	);
}

/**
 * @param mixed $value
 * @return int[]
 */
function shm_sanitize_gallery_meta($value): array {
	if (!is_array($value)) {
		return array();
	}
	$ids = array_map('absint', $value);
	$ids = array_values(array_filter($ids));
	return array_slice($ids, 0, SHM_MAX_IMAGES);
}

/**
 * Attachment IDs for listing carousel (gallery meta, else featured image).
 *
 * @return int[]
 */
function shm_get_listing_image_ids(int $post_id): array {
	$gallery = get_post_meta($post_id, 'shm_gallery', true);
	if (is_array($gallery) && !empty($gallery)) {
		$ids = array();
		foreach ($gallery as $id) {
			$id = (int) $id;
			if ($id > 0 && wp_attachment_is_image($id)) {
				$ids[] = $id;
			}
		}
		if (!empty($ids)) {
			return array_slice($ids, 0, SHM_MAX_IMAGES);
		}
	}
	$thumb = (int) get_post_thumbnail_id($post_id);
	return $thumb > 0 ? array( $thumb ) : array();
}

/**
 * @return array<int, array{url: string, alt: string, id: int}>
 */
function shm_get_listing_images(int $post_id): array {
	$out = array();
	foreach (shm_get_listing_image_ids($post_id) as $id) {
		$url = wp_get_attachment_image_url($id, 'large');
		if (!$url) {
			continue;
		}
		$out[] = array(
			'id'  => $id,
			'url' => $url,
			'alt' => (string) get_post_meta($id, '_wp_attachment_image_alt', true) ?: get_the_title($post_id),
		);
	}
	return $out;
}

function shm_save_listing_gallery(int $post_id, array $attachment_ids): void {
	$attachment_ids = shm_sanitize_gallery_meta($attachment_ids);
	if (empty($attachment_ids)) {
		delete_post_meta($post_id, 'shm_gallery');
		delete_post_thumbnail($post_id);
		return;
	}
	update_post_meta($post_id, 'shm_gallery', $attachment_ids);
	set_post_thumbnail($post_id, $attachment_ids[0]);
}

add_shortcode('shm_listings', 'shm_shortcode_listings');
/**
 * [shm_listings posts_per_page="12" columns="3"]
 */
function shm_shortcode_listings($atts): string {
	shm_enqueue_frontend_style();
	$atts = shortcode_atts(
		array(
			'posts_per_page' => 12,
			'columns'        => 3,
		),
		$atts,
		'shm_listings'
	);
	$cols = max(1, min(4, (int) $atts['columns']));
	$q     = new WP_Query(
		array(
			'post_type'      => 'second_hand_item',
			'post_status'    => 'publish',
			'posts_per_page' => (int) $atts['posts_per_page'],
		)
	);
	ob_start();
	echo '<div class="shm-grid shm-cols-' . esc_attr((string) $cols) . '">';
	if ($q->have_posts()) {
		while ($q->have_posts()) {
			$q->the_post();
			$price      = get_post_meta(get_the_ID(), 'shm_price', true);
			$loc        = get_post_meta(get_the_ID(), 'shm_location', true);
			$img_count  = count(shm_get_listing_image_ids(get_the_ID()));
			?>
			<article class="shm-card">
				<a href="<?php the_permalink(); ?>" class="shm-card__link">
					<div class="shm-card__thumb">
						<?php
						if (has_post_thumbnail()) {
							the_post_thumbnail('medium_large');
						} else {
							echo '<span class="shm-card__placeholder">' . esc_html__('No image', 'second-hand-marketplace') . '</span>';
						}
						if ($price) {
							echo '<span class="shm-card__badge">' . esc_html($price) . '</span>';
						}
						if ($img_count > 1) {
							echo '<span class="shm-card__photos">' . esc_html((string) $img_count) . ' ' . esc_html__('photos', 'second-hand-marketplace') . '</span>';
						}
						?>
					</div>
					<div class="shm-card__body">
						<h3 class="shm-card__title"><?php the_title(); ?></h3>
						<?php if ($loc) : ?>
							<p class="shm-card__loc"><?php echo esc_html($loc); ?></p>
						<?php endif; ?>
					</div>
				</a>
			</article>
			<?php
		}
		wp_reset_postdata();
	} else {
		echo '<p class="shm-empty">' . esc_html__('No items yet. Be the first to list one.', 'second-hand-marketplace') . '</p>';
	}
	echo '</div>';
	return (string) ob_get_clean();
}

add_shortcode('shm_sell_form', 'shm_shortcode_sell_form');
function shm_shortcode_sell_form(): string {
	shm_enqueue_frontend_style();
	if (!function_exists('wp_handle_upload')) {
		require_once ABSPATH . 'wp-admin/includes/file.php';
	}
	if (!function_exists('media_handle_upload')) {
		require_once ABSPATH . 'wp-admin/includes/image.php';
		require_once ABSPATH . 'wp-admin/includes/media.php';
	}

	$message = '';
	$error   = '';

	if (isset($_POST['shm_submit']) && isset($_POST['shm_nonce']) && wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['shm_nonce'])), 'shm_sell_form')) {
		$result = shm_process_listing_submission();
		if (is_wp_error($result)) {
			$error = $result->get_error_message();
		} else {
			$message = __('Thank you. Your listing was submitted and will appear on the site after an administrator approves it.', 'second-hand-marketplace');
		}
	}

	ob_start();
	?>
	<div class="shm-form-wrap">
		<?php if ($message) : ?>
			<p class="shm-notice shm-notice--success"><?php echo esc_html($message); ?></p>
		<?php endif; ?>
		<?php if ($error) : ?>
			<p class="shm-notice shm-notice--error"><?php echo esc_html($error); ?></p>
		<?php endif; ?>

		<div class="shm-form-card">
			<h2 class="shm-form-heading"><?php esc_html_e('Sell your item', 'second-hand-marketplace'); ?></h2>
			<p class="shm-form-sub"><?php esc_html_e('Fill in the details below. Your listing will be reviewed before it goes live.', 'second-hand-marketplace'); ?></p>

			<form method="post" enctype="multipart/form-data" class="shm-sell-form">
				<?php wp_nonce_field('shm_sell_form', 'shm_nonce'); ?>
				<p class="shm-field">
					<label for="shm_title"><?php esc_html_e('Item name', 'second-hand-marketplace'); ?> *</label>
					<input type="text" name="shm_title" id="shm_title" required maxlength="200" placeholder="<?php esc_attr_e('e.g. Tata Sierra 2012', 'second-hand-marketplace'); ?>"
						value="<?php echo isset($_POST['shm_title']) ? esc_attr(sanitize_text_field(wp_unslash($_POST['shm_title']))) : ''; ?>" />
				</p>
				<p class="shm-field">
					<label for="shm_description"><?php esc_html_e('Description', 'second-hand-marketplace'); ?> *</label>
					<textarea name="shm_description" id="shm_description" rows="6" required placeholder="<?php esc_attr_e('Condition, features, reason for selling…', 'second-hand-marketplace'); ?>"><?php echo isset($_POST['shm_description']) ? esc_textarea(wp_unslash($_POST['shm_description'])) : ''; ?></textarea>
				</p>
				<p class="shm-field">
					<label for="shm_price"><?php esc_html_e('Price', 'second-hand-marketplace'); ?></label>
					<input type="text" name="shm_price" id="shm_price" maxlength="100" placeholder="<?php esc_attr_e('e.g. ₹600000 or Free', 'second-hand-marketplace'); ?>"
						value="<?php echo isset($_POST['shm_price']) ? esc_attr(sanitize_text_field(wp_unslash($_POST['shm_price']))) : ''; ?>" />
				</p>
				<p class="shm-field">
					<label for="shm_location"><?php esc_html_e('City / area', 'second-hand-marketplace'); ?></label>
					<input type="text" name="shm_location" id="shm_location" maxlength="120" placeholder="<?php esc_attr_e('e.g. Karwar', 'second-hand-marketplace'); ?>"
						value="<?php echo isset($_POST['shm_location']) ? esc_attr(sanitize_text_field(wp_unslash($_POST['shm_location']))) : ''; ?>" />
				</p>
				<div class="shm-form-row">
					<p class="shm-field">
						<label for="shm_contact"><?php esc_html_e('Phone number', 'second-hand-marketplace'); ?></label>
						<input type="tel" name="shm_contact" id="shm_contact" maxlength="30" placeholder="<?php esc_attr_e('e.g. 7899273733', 'second-hand-marketplace'); ?>"
							value="<?php echo isset($_POST['shm_contact']) ? esc_attr(sanitize_text_field(wp_unslash($_POST['shm_contact']))) : ''; ?>" />
						<span class="shm-hint"><?php esc_html_e('Shown on the item page after approval', 'second-hand-marketplace'); ?></span>
					</p>
					<p class="shm-field">
						<label for="shm_email"><?php esc_html_e('Email', 'second-hand-marketplace'); ?></label>
						<input type="email" name="shm_email" id="shm_email" maxlength="120" placeholder="<?php esc_attr_e('you@example.com', 'second-hand-marketplace'); ?>"
							value="<?php echo isset($_POST['shm_email']) ? esc_attr(sanitize_email(wp_unslash($_POST['shm_email']))) : ''; ?>" />
					</p>
				</div>
				<p class="shm-field">
					<label for="shm_images"><?php esc_html_e('Photos', 'second-hand-marketplace'); ?></label>
					<div class="shm-file-wrap">
						<input type="file" name="shm_images[]" id="shm_images" accept="image/jpeg,image/png,image/webp,image/gif" multiple />
						<span class="shm-hint" id="shm_images_count"></span>
						<span class="shm-hint"><?php echo esc_html(sprintf(/* translators: %d: max images */ __('Add 1 to %d images. Buyers can swipe through them on your listing.', 'second-hand-marketplace'), SHM_MAX_IMAGES)); ?></span>
						<div id="shm_images_preview" class="shm-images-preview" aria-live="polite"></div>
					</div>
				</p>
				<p class="shm-field shm-field--hp" aria-hidden="true" style="position:absolute;left:-9999px;">
					<label for="shm_hp"><?php esc_html_e('Leave blank', 'second-hand-marketplace'); ?></label>
					<input type="text" name="shm_hp" id="shm_hp" tabindex="-1" autocomplete="off" />
				</p>
				<button type="submit" name="shm_submit" value="1" class="shm-submit"><?php esc_html_e('Submit for review', 'second-hand-marketplace'); ?></button>
			</form>
		</div>
	</div>
	<?php
	return (string) ob_get_clean();
}

/**
 * @return int|WP_Error
 */
function shm_process_listing_submission() {
	add_filter('user_has_cap', 'shm_grant_caps_for_guest_listing', 10, 4);
	try {
		if (!empty($_POST['shm_hp'])) {
			return new WP_Error('spam', __('Submission rejected.', 'second-hand-marketplace'));
		}

		$title = isset($_POST['shm_title']) ? sanitize_text_field(wp_unslash($_POST['shm_title'])) : '';
		$desc  = isset($_POST['shm_description']) ? wp_kses_post(wp_unslash($_POST['shm_description'])) : '';
		if ($title === '' || trim(wp_strip_all_tags($desc)) === '') {
			return new WP_Error('required', __('Please fill item name and description.', 'second-hand-marketplace'));
		}

		$author_id = (int) apply_filters('shm_listing_author_id', get_current_user_id() ?: 1);

		$post_id = wp_insert_post(
			array(
				'post_title'   => $title,
				'post_content' => $desc,
				'post_status'  => shm_new_listing_status(),
				'post_type'    => 'second_hand_item',
				'post_author'  => $author_id,
			),
			true
		);

		if (is_wp_error($post_id)) {
			return $post_id;
		}

		if (isset($_POST['shm_price'])) {
			update_post_meta($post_id, 'shm_price', sanitize_text_field(wp_unslash((string) $_POST['shm_price'])));
		}
		if (isset($_POST['shm_contact'])) {
			update_post_meta($post_id, 'shm_contact', sanitize_text_field(wp_unslash((string) $_POST['shm_contact'])));
		}
		if (isset($_POST['shm_email'])) {
			$email = sanitize_email(wp_unslash((string) $_POST['shm_email']));
			if ($email !== '') {
				update_post_meta($post_id, 'shm_email', $email);
			}
		}
		if (isset($_POST['shm_location'])) {
			update_post_meta($post_id, 'shm_location', sanitize_text_field(wp_unslash((string) $_POST['shm_location'])));
		}

		$uploaded = shm_process_listing_images_upload($post_id);
		if (is_wp_error($uploaded)) {
			return $uploaded;
		}

		return $post_id;
	} finally {
		remove_filter('user_has_cap', 'shm_grant_caps_for_guest_listing', 10);
	}
}

/**
 * Front-end submissions run without a logged-in user; media needs upload_files briefly.
 *
 * @param array<string, bool> $allcaps
 */
function shm_grant_caps_for_guest_listing($allcaps, $caps, $args, $user) {
	unset($caps, $args, $user);
	$allcaps['upload_files'] = true;
	$allcaps['edit_posts']   = true;
	return $allcaps;
}

/**
 * Normalize $_FILES field when input has multiple="multiple".
 *
 * @param array<string, mixed> $file_field
 * @return array<int, array<string, mixed>>
 */
function shm_normalize_uploaded_files(array $file_field): array {
	if (!isset($file_field['name']) || !is_array($file_field['name'])) {
		if (!empty($file_field['name'])) {
			return array( $file_field );
		}
		return array();
	}
	$files = array();
	foreach ($file_field['name'] as $i => $name) {
		if ($name === '' || $name === null) {
			continue;
		}
		$files[] = array(
			'name'     => $file_field['name'][ $i ],
			'type'     => $file_field['type'][ $i ] ?? '',
			'tmp_name' => $file_field['tmp_name'][ $i ] ?? '',
			'error'    => $file_field['error'][ $i ] ?? UPLOAD_ERR_NO_FILE,
			'size'     => $file_field['size'][ $i ] ?? 0,
		);
	}
	return $files;
}

/**
 * @return true|WP_Error
 */
function shm_process_listing_images_upload(int $post_id) {
	$files = array();
	if (!empty($_FILES['shm_images']['name'])) {
		$files = shm_normalize_uploaded_files($_FILES['shm_images']);
	} elseif (!empty($_FILES['shm_image']['name'])) {
		$files = shm_normalize_uploaded_files($_FILES['shm_image']);
	}
	if (empty($files)) {
		return true;
	}
	if (count($files) > SHM_MAX_IMAGES) {
		return new WP_Error(
			'too_many',
			sprintf(
				/* translators: %d: max images */
				__('You can upload at most %d images.', 'second-hand-marketplace'),
				SHM_MAX_IMAGES
			)
		);
	}

	$attachment_ids = array();
	foreach ($files as $file) {
		$aid = shm_upload_single_image($post_id, $file);
		if (is_wp_error($aid)) {
			continue;
		}
		$attachment_ids[] = (int) $aid;
	}

	if (empty($attachment_ids)) {
		return new WP_Error('upload', __('Could not upload images. Please use JPG, PNG or WebP.', 'second-hand-marketplace'));
	}

	shm_save_listing_gallery($post_id, $attachment_ids);
	return true;
}

/**
 * @param array<string, mixed> $file
 * @return int|WP_Error
 */
function shm_upload_single_image(int $post_id, array $file) {
	if (!function_exists('wp_handle_upload')) {
		require_once ABSPATH . 'wp-admin/includes/file.php';
	}
	if (!function_exists('wp_generate_attachment_metadata')) {
		require_once ABSPATH . 'wp-admin/includes/image.php';
	}

	if (!isset($file['error']) || UPLOAD_ERR_OK !== (int) $file['error']) {
		return new WP_Error('upload', __('Upload failed.', 'second-hand-marketplace'));
	}

	$check = wp_check_filetype_and_ext($file['tmp_name'], $file['name']);
	$mime  = isset($check['type']) ? (string) $check['type'] : '';
	if (empty($check['ext']) || strpos($mime, 'image/') !== 0) {
		return new WP_Error('type', __('Only image files are allowed.', 'second-hand-marketplace'));
	}

	$overrides = array('test_form' => false);
	$move      = wp_handle_upload($file, $overrides);
	if (isset($move['error'])) {
		return new WP_Error('upload', $move['error']);
	}

	$attachment = array(
		'post_mime_type' => $move['type'],
		'post_title'     => sanitize_file_name(basename($move['file'])),
		'post_content'   => '',
		'post_status'    => 'inherit',
		'post_parent'    => $post_id,
	);

	$attach_id = wp_insert_attachment($attachment, $move['file'], $post_id);
	if (is_wp_error($attach_id)) {
		return $attach_id;
	}

	$meta = wp_generate_attachment_metadata($attach_id, $move['file']);
	wp_update_attachment_metadata($attach_id, $meta);

	return (int) $attach_id;
}

add_filter('the_content', 'shm_render_single_listing', 5);
function shm_render_single_listing(string $content): string {
	if (!is_singular('second_hand_item') || !in_the_loop() || !is_main_query()) {
		return $content;
	}

	$post_id = get_the_ID();
	remove_filter('the_content', 'shm_render_single_listing', 5);
	$description_html = apply_filters('the_content', $content);
	add_filter('the_content', 'shm_render_single_listing', 5);

	shm_enqueue_frontend_scripts();

	ob_start();
	include SHM_PATH . 'templates/single-listing.php';
	return (string) ob_get_clean();
}

add_filter('post_thumbnail_html', 'shm_hide_theme_thumbnail_on_single', 99, 5);
function shm_hide_theme_thumbnail_on_single(string $html, $post_id, $thumb_id, $size, $attr): string {
	unset($thumb_id, $size, $attr);
	if (is_singular('second_hand_item') && (int) $post_id === get_queried_object_id()) {
		return '';
	}
	return $html;
}

/* ---------- Admin: approve / reject pending listings ---------- */

add_filter('post_row_actions', 'shm_listing_row_actions', 10, 2);
/**
 * @param array<string, string> $actions
 */
function shm_listing_row_actions(array $actions, WP_Post $post): array {
	if ($post->post_type !== 'second_hand_item' || $post->post_status !== 'pending') {
		return $actions;
	}
	$id = (int) $post->ID;

	if (current_user_can('publish_post', $id)) {
		$approve_url          = wp_nonce_url(
			admin_url('admin-post.php?action=shm_approve_listing&post=' . $id),
			'shm_approve_listing_' . $id
		);
		$actions['shm_approve'] = '<a href="' . esc_url($approve_url) . '">' . esc_html__('Approve', 'second-hand-marketplace') . '</a>';
	}

	if (current_user_can('delete_post', $id)) {
		$reject_url         = wp_nonce_url(
			admin_url('admin-post.php?action=shm_reject_listing&post=' . $id),
			'shm_reject_listing_' . $id
		);
		$confirm            = esc_js(__('Move this listing to the trash?', 'second-hand-marketplace'));
		$actions['shm_reject'] = '<a href="' . esc_url($reject_url) . '" class="shm-admin-reject" onclick="return confirm(\'' . $confirm . '\');">' . esc_html__('Reject', 'second-hand-marketplace') . '</a>';
	}

	return $actions;
}

add_action('admin_post_shm_approve_listing', 'shm_admin_post_approve_listing');
function shm_admin_post_approve_listing(): void {
	if (!is_user_logged_in()) {
		wp_die(esc_html__('You must be logged in.', 'second-hand-marketplace'));
	}
	$id = isset($_GET['post']) ? absint($_GET['post']) : 0;
	if (!$id || get_post_type($id) !== 'second_hand_item') {
		wp_die(esc_html__('Invalid listing.', 'second-hand-marketplace'));
	}
	if (!current_user_can('publish_post', $id)) {
		wp_die(esc_html__('Sorry, you are not allowed to approve this listing.', 'second-hand-marketplace'));
	}
	check_admin_referer('shm_approve_listing_' . $id);

	$post = get_post($id);
	if ($post && $post->post_status === 'pending') {
		wp_update_post(
			array(
				'ID'          => $id,
				'post_status' => 'publish',
			)
		);
	}

	wp_safe_redirect(
		add_query_arg(
			array(
				'post_type'    => 'second_hand_item',
				'shm_approved' => '1',
			),
			admin_url('edit.php')
		)
	);
	exit;
}

add_action('admin_post_shm_reject_listing', 'shm_admin_post_reject_listing');
function shm_admin_post_reject_listing(): void {
	if (!is_user_logged_in()) {
		wp_die(esc_html__('You must be logged in.', 'second-hand-marketplace'));
	}
	$id = isset($_GET['post']) ? absint($_GET['post']) : 0;
	if (!$id || get_post_type($id) !== 'second_hand_item') {
		wp_die(esc_html__('Invalid listing.', 'second-hand-marketplace'));
	}
	if (!current_user_can('delete_post', $id)) {
		wp_die(esc_html__('Sorry, you are not allowed to reject this listing.', 'second-hand-marketplace'));
	}
	check_admin_referer('shm_reject_listing_' . $id);

	$post = get_post($id);
	if ($post && $post->post_status === 'pending') {
		wp_trash_post($id);
	}

	wp_safe_redirect(
		add_query_arg(
			array(
				'post_type'   => 'second_hand_item',
				'shm_rejected' => '1',
			),
			admin_url('edit.php')
		)
	);
	exit;
}

add_action('admin_notices', 'shm_admin_listing_notices');
function shm_admin_listing_notices(): void {
	if (!is_admin()) {
		return;
	}
	$screen = function_exists('get_current_screen') ? get_current_screen() : null;
	if (!$screen || $screen->id !== 'edit-second_hand_item') {
		return;
	}

	if (isset($_GET['shm_approved']) && $_GET['shm_approved'] === '1') {
		echo '<div class="notice notice-success is-dismissible"><p>' . esc_html__('Listing approved. It is now visible on the website.', 'second-hand-marketplace') . '</p></div>';
	}
	if (isset($_GET['shm_rejected']) && $_GET['shm_rejected'] === '1') {
		echo '<div class="notice notice-warning is-dismissible"><p>' . esc_html__('Listing rejected (moved to Trash).', 'second-hand-marketplace') . '</p></div>';
	}

	$counts  = wp_count_posts('second_hand_item');
	$pending = isset($counts->pending) ? (int) $counts->pending : 0;
	if ($pending > 0) {
		echo '<div class="notice notice-info"><p>';
		echo esc_html(
			sprintf(
				/* translators: %d: number of pending listings */
				_n(
					'You have %d listing waiting for approval.',
					'You have %d listings waiting for approval.',
					$pending,
					'second-hand-marketplace'
				),
				$pending
			)
		);
		echo ' ';
		echo esc_html__('Use Approve or Reject under each pending item.', 'second-hand-marketplace');
		echo '</p></div>';
	}
}
