(function () {
	'use strict';

	var MAX_IMAGES = 10;

	function initFormImages() {
		var input = document.getElementById('shm_images');
		var preview = document.getElementById('shm_images_preview');
		var countEl = document.getElementById('shm_images_count');
		if (!input) {
			return;
		}

		input.addEventListener('change', function () {
			var files = input.files;
			if (files.length > MAX_IMAGES) {
				alert('You can upload a maximum of ' + MAX_IMAGES + ' images.');
				input.value = '';
				if (preview) {
					preview.innerHTML = '';
				}
				if (countEl) {
					countEl.textContent = '';
				}
				return;
			}

			if (countEl) {
				countEl.textContent =
					files.length === 0
						? ''
						: files.length + ' / ' + MAX_IMAGES + ' selected';
			}

			if (!preview) {
				return;
			}
			preview.innerHTML = '';
			Array.prototype.forEach.call(files, function (file) {
				if (!file.type.match(/^image\//)) {
					return;
				}
				var img = document.createElement('img');
				img.className = 'shm-preview-thumb';
				img.alt = '';
				preview.appendChild(img);
				var reader = new FileReader();
				reader.onload = function (e) {
					img.src = e.target.result;
				};
				reader.readAsDataURL(file);
			});
		});
	}

	function initCarousels() {
		document.querySelectorAll('.shm-carousel').forEach(function (root) {
			var track = root.querySelector('.shm-carousel__track');
			var slides = root.querySelectorAll('.shm-carousel__slide');
			var dotsWrap = root.querySelector('.shm-carousel__dots');
			var counter = root.querySelector('.shm-carousel__counter');
			var prevBtn = root.querySelector('.shm-carousel__prev');
			var nextBtn = root.querySelector('.shm-carousel__next');

			if (!track || slides.length === 0) {
				return;
			}

			var index = 0;
			var total = slides.length;

			function goTo(i) {
				index = (i + total) % total;
				track.style.transform = 'translateX(-' + index * 100 + '%)';
				if (dotsWrap) {
					dotsWrap.querySelectorAll('.shm-carousel__dot').forEach(function (dot, di) {
						dot.classList.toggle('is-active', di === index);
					});
				}
				if (counter) {
					counter.textContent = index + 1 + ' / ' + total;
				}
			}

			if (dotsWrap && total > 1) {
				for (var d = 0; d < total; d++) {
					var dot = document.createElement('button');
					dot.type = 'button';
					dot.className = 'shm-carousel__dot' + (d === 0 ? ' is-active' : '');
					dot.setAttribute('aria-label', 'Image ' + (d + 1));
					(function (di) {
						dot.addEventListener('click', function () {
							goTo(di);
						});
					})(d);
					dotsWrap.appendChild(dot);
				}
			}

			if (prevBtn) {
				prevBtn.addEventListener('click', function () {
					goTo(index - 1);
				});
			}
			if (nextBtn) {
				nextBtn.addEventListener('click', function () {
					goTo(index + 1);
				});
			}

			var startX = 0;
			var startY = 0;
			var dragging = false;

			root.addEventListener(
				'touchstart',
				function (e) {
					if (total <= 1) {
						return;
					}
					startX = e.touches[0].clientX;
					startY = e.touches[0].clientY;
					dragging = true;
				},
				{ passive: true }
			);

			root.addEventListener(
				'touchend',
				function (e) {
					if (!dragging || total <= 1) {
						return;
					}
					dragging = false;
					var endX = e.changedTouches[0].clientX;
					var endY = e.changedTouches[0].clientY;
					var diffX = endX - startX;
					var diffY = endY - startY;
					if (Math.abs(diffX) < 40 || Math.abs(diffY) > Math.abs(diffX)) {
						return;
					}
					if (diffX < 0) {
						goTo(index + 1);
					} else {
						goTo(index - 1);
					}
				},
				{ passive: true }
			);

			/* Mouse drag for desktop */
			var mouseDown = false;
			root.addEventListener('mousedown', function (e) {
				if (total <= 1) {
					return;
				}
				mouseDown = true;
				startX = e.clientX;
			});
			root.addEventListener('mouseup', function (e) {
				if (!mouseDown || total <= 1) {
					return;
				}
				mouseDown = false;
				var diffX = e.clientX - startX;
				if (Math.abs(diffX) < 50) {
					return;
				}
				if (diffX < 0) {
					goTo(index + 1);
				} else {
					goTo(index - 1);
				}
			});
			root.addEventListener('mouseleave', function () {
				mouseDown = false;
			});
		});
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', function () {
			initFormImages();
			initCarousels();
		});
	} else {
		initFormImages();
		initCarousels();
	}
})();
