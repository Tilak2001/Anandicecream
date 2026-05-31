<?php
/**
 * Single listing layout (included from the_content filter).
 *
 * @var int    $post_id
 * @var string $description_html
 */

if (!defined('ABSPATH')) {
	exit;
}

$price  = get_post_meta($post_id, 'shm_price', true);
$loc    = get_post_meta($post_id, 'shm_location', true);
$phone  = get_post_meta($post_id, 'shm_contact', true);
$email  = get_post_meta($post_id, 'shm_email', true);
$posted = get_the_date('', $post_id);
$images = shm_get_listing_images($post_id);
$tel    = $phone ? preg_replace('/[^0-9+]/', '', $phone) : '';
?>
<article class="shm-detail">
	<?php if (!empty($images)) : ?>
		<div class="shm-carousel" role="region" aria-label="<?php esc_attr_e('Item photos', 'second-hand-marketplace'); ?>">
			<div class="shm-carousel__viewport">
				<div class="shm-carousel__track">
					<?php foreach ($images as $img) : ?>
						<div class="shm-carousel__slide">
							<img src="<?php echo esc_url($img['url']); ?>" alt="<?php echo esc_attr($img['alt']); ?>" loading="lazy" />
						</div>
					<?php endforeach; ?>
				</div>
				<?php if (count($images) > 1) : ?>
					<button type="button" class="shm-carousel__prev" aria-label="<?php esc_attr_e('Previous image', 'second-hand-marketplace'); ?>">‹</button>
					<button type="button" class="shm-carousel__next" aria-label="<?php esc_attr_e('Next image', 'second-hand-marketplace'); ?>">›</button>
					<span class="shm-carousel__counter">1 / <?php echo (int) count($images); ?></span>
				<?php endif; ?>
			</div>
			<?php if (count($images) > 1) : ?>
				<div class="shm-carousel__dots" aria-hidden="true"></div>
			<?php endif; ?>
			<?php if (count($images) > 1) : ?>
				<p class="shm-carousel__hint"><?php esc_html_e('Swipe left or right to see more photos', 'second-hand-marketplace'); ?></p>
			<?php endif; ?>
		</div>
	<?php else : ?>
		<div class="shm-detail__no-img">
			<span class="shm-detail__no-img-icon" aria-hidden="true">📷</span>
			<?php esc_html_e('No photos for this item', 'second-hand-marketplace'); ?>
		</div>
	<?php endif; ?>

	<div class="shm-detail__panel">
		<header class="shm-detail__header">
			<?php if ($price) : ?>
				<p class="shm-detail__price-tag"><?php echo esc_html($price); ?></p>
			<?php endif; ?>
		</header>

		<?php if ($loc) : ?>
			<div class="shm-detail__chip">
				<span class="shm-detail__chip-icon" aria-hidden="true">📍</span>
				<?php echo esc_html($loc); ?>
			</div>
		<?php endif; ?>

		<section class="shm-detail__section">
			<h3 class="shm-detail__section-title"><?php esc_html_e('Description', 'second-hand-marketplace'); ?></h3>
			<div class="shm-detail__desc">
				<?php echo $description_html; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
			</div>
		</section>

		<?php if ($email) : ?>
			<section class="shm-detail__section shm-detail__section--compact">
				<h3 class="shm-detail__section-title"><?php esc_html_e('Email', 'second-hand-marketplace'); ?></h3>
				<a class="shm-detail__email-link" href="<?php echo esc_url('mailto:' . $email); ?>"><?php echo esc_html($email); ?></a>
			</section>
		<?php endif; ?>

		<?php if ($posted) : ?>
			<p class="shm-detail__posted">
				<?php
				echo esc_html(
					sprintf(
						/* translators: %s: post date */
						__('Listed on %s', 'second-hand-marketplace'),
						$posted
					)
				);
				?>
			</p>
		<?php endif; ?>
	</div>

	<?php if ($phone) : ?>
		<a class="shm-detail__phone-bar" href="<?php echo esc_url('tel:' . $tel); ?>">
			<span class="shm-detail__phone-icon" aria-hidden="true">
				<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
					<path d="M6.62 10.79a15.05 15.05 0 006.59 6.59l2.2-2.2a1 1 0 011.01-.24 11.36 11.36 0 003.56.57 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1 11.36 11.36 0 00.57 3.56 1 1 0 01-.25 1.01l-2.2 2.22z" fill="currentColor"/>
				</svg>
			</span>
			<span class="shm-detail__phone-label"><?php esc_html_e('Call seller', 'second-hand-marketplace'); ?></span>
			<span class="shm-detail__phone-number"><?php echo esc_html($phone); ?></span>
		</a>
	<?php endif; ?>
</article>
