// Add active class to current nav item
const navLinks = document.querySelectorAll('.nav-menu a');

navLinks.forEach(link => {
    link.addEventListener('click', function (e) {
        navLinks.forEach(l => l.classList.remove('active'));
        this.classList.add('active');
    });
});

// Carousel functionality
let currentSlide = 0;
const wrapper = document.getElementById('carouselWrapper');
const dots = document.querySelectorAll('.dot');
const totalSlides = 2;

function updateCarousel() {
    wrapper.style.transform = `translateX(-${currentSlide * 100}%)`;

    // Update dots
    dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === currentSlide);
    });
}

function moveSlide(direction) {
    currentSlide += direction;

    if (currentSlide < 0) {
        currentSlide = totalSlides - 1;
    } else if (currentSlide >= totalSlides) {
        currentSlide = 0;
    }

    updateCarousel();
}

function goToSlide(slideIndex) {
    currentSlide = slideIndex;
    updateCarousel();
}

// Auto-rotate carousel every 5 seconds
setInterval(() => {
    moveSlide(1);
}, 5000);

// Product Page Functionality
let selectedFlavor = 'Badam';
let selectedSize = 'Small';
let currentPrice = 20;

// Open Kulfi product page
function openKulfiPage() {
    document.getElementById('kulfiModal').classList.add('active');
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
}

// Close product page
function closeProductPage() {
    document.getElementById('kulfiModal').classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Select flavor
function selectFlavor(element, flavor) {
    // Remove selected class from all flavor options
    document.querySelectorAll('.flavor-option').forEach(opt => {
        opt.classList.remove('selected');
    });
    // Add selected class to clicked option
    element.classList.add('selected');
    selectedFlavor = flavor;
}

// Select size and update price
function selectSize(element, size, price) {
    // Remove selected class from all size options
    document.querySelectorAll('.size-option').forEach(opt => {
        opt.classList.remove('selected');
    });
    // Add selected class to clicked option
    element.classList.add('selected');
    selectedSize = size;
    currentPrice = price;

    // Update price display
    document.getElementById('totalPrice').textContent = '₹' + price;
}

// Add to cart
function addToCart() {
    const btn = document.querySelector('.add-to-cart-btn');

    // Create cart item object
    const cartItem = {
        product: 'Kulfi',
        flavor: selectedFlavor,
        size: selectedSize,
        price: currentPrice
    };

    // Get existing cart from localStorage
    let cart = localStorage.getItem('anandIceCreamCart');
    cart = cart ? JSON.parse(cart) : [];

    // Add new item to cart
    cart.push(cartItem);

    // Save updated cart to localStorage
    localStorage.setItem('anandIceCreamCart', JSON.stringify(cart));

    // Update cart count in navbar
    updateCartCountDisplay();

    // Visual feedback
    btn.classList.add('added');
    btn.innerHTML = '✓ Added to Cart!';

    // Log to console
    console.log('Added to cart:', cartItem);
    console.log('Total items in cart:', cart.length);

    // Reset button after 2 seconds
    setTimeout(() => {
        btn.classList.remove('added');
        btn.innerHTML = '🛒 Add to Cart';
    }, 2000);
}

// Update cart count display
function updateCartCountDisplay() {
    const cart = localStorage.getItem('anandIceCreamCart');
    const cartArray = cart ? JSON.parse(cart) : [];
    const cartCount = document.getElementById('cartCount');
    if (cartCount) {
        cartCount.textContent = cartArray.length;
    }
}

// Add click event to Kulfi card
document.addEventListener('DOMContentLoaded', function () {
    // Update cart count on page load
    updateCartCountDisplay();

    const kulfiCard = document.querySelector('.ice-cream-card:first-child');
    if (kulfiCard) {
        kulfiCard.addEventListener('click', openKulfiPage);
    }
});

// Close modal when clicking outside the product page
document.getElementById('kulfiModal').addEventListener('click', function (e) {
    if (e.target === this) {
        closeProductPage();
    }
});
