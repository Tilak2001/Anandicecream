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
let quantity = 1;
const unitPrice = 30;
let currentPrice = 30;

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

// Increase quantity
function increaseQuantity() {
    const input = document.getElementById('quantity');
    quantity = (parseInt(input.value) || 1) + 1;
    input.value = quantity;
    updatePrice();
}

// Decrease quantity
function decreaseQuantity() {
    const input = document.getElementById('quantity');
    quantity = Math.max(1, (parseInt(input.value) || 1) - 1);
    input.value = quantity;
    updatePrice();
}

// Live input handler for Kulfi quantity
function onKulfiQtyInput(input) {
    const val = parseInt(input.value);
    if (!isNaN(val) && val >= 1) {
        quantity = val;
        updatePrice();
    }
}

// Update price based on quantity
function updatePrice() {
    currentPrice = unitPrice * quantity;
    document.getElementById('totalPrice').textContent = '₹' + currentPrice;
}

// Add to cart
function addToCart() {
    const btn = document.querySelector('.add-to-cart-btn');

    // Create cart item object
    const cartItem = {
        product: 'Kulfi',
        flavor: selectedFlavor,
        quantity: quantity,
        unitPrice: unitPrice,
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

// Add click events + modal backdrop listeners inside DOMContentLoaded
document.addEventListener('DOMContentLoaded', function () {
    // Update cart count on page load
    updateCartCountDisplay();

    // Kulfi card click
    const kulfiCard = document.querySelector('.ice-cream-card:first-child');
    if (kulfiCard) {
        kulfiCard.addEventListener('click', openKulfiPage);
    }

    // Close modals when clicking outside
    const kulfiModal = document.getElementById('kulfiModal');
    if (kulfiModal) {
        kulfiModal.addEventListener('click', function (e) {
            if (e.target === this) closeProductPage();
        });
    }

    const cupModal = document.getElementById('cupModal');
    if (cupModal) {
        cupModal.addEventListener('click', function (e) {
            if (e.target === this) closeCupPage();
        });
    }
});

// ========================
// Cup Ice Cream Modal
// ========================
let selectedCupFlavor = 'Vanilla';
let cupQuantity = 1;
const cupUnitPrice = 10;
let cupCurrentPrice = 10;

function openCupPage() {
    document.getElementById('cupModal').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeCupPage() {
    document.getElementById('cupModal').classList.remove('active');
    document.body.style.overflow = 'auto';
}

function selectCupFlavor(element, flavor) {
    document.querySelectorAll('#cupFlavorGrid .flavor-option').forEach(opt => {
        opt.classList.remove('selected');
    });
    element.classList.add('selected');
    selectedCupFlavor = flavor;
}

function increaseCupQuantity() {
    const input = document.getElementById('cupQuantity');
    cupQuantity = (parseInt(input.value) || 1) + 1;
    input.value = cupQuantity;
    updateCupPrice();
}

function decreaseCupQuantity() {
    const input = document.getElementById('cupQuantity');
    cupQuantity = Math.max(1, (parseInt(input.value) || 1) - 1);
    input.value = cupQuantity;
    updateCupPrice();
}

// Live input handler for Cup quantity
function onCupQtyInput(input) {
    const val = parseInt(input.value);
    if (!isNaN(val) && val >= 1) {
        cupQuantity = val;
        updateCupPrice();
    }
}

function updateCupPrice() {
    cupCurrentPrice = cupUnitPrice * cupQuantity;
    document.getElementById('cupTotalPrice').textContent = '₹' + cupCurrentPrice;
}

function addCupToCart() {
    const btn = document.getElementById('cupCartBtn');
    const cartItem = {
        product: 'Cup Ice Cream',
        flavor: selectedCupFlavor,
        quantity: cupQuantity,
        unitPrice: cupUnitPrice,
        price: cupCurrentPrice
    };

    let cart = localStorage.getItem('anandIceCreamCart');
    cart = cart ? JSON.parse(cart) : [];
    cart.push(cartItem);
    localStorage.setItem('anandIceCreamCart', JSON.stringify(cart));

    updateCartCountDisplay();

    btn.classList.add('added');
    btn.innerHTML = '✓ Added to Cart!';
    setTimeout(() => {
        btn.classList.remove('added');
        btn.innerHTML = '🛒 Add to Cart';
    }, 2000);
}

// ========================
// Gadbad Modal
// ========================
let selectedGadbadFlavor = 'Mini Gudbud';
let gadbadUnitPrice = 20;
let gadbadQuantity = 1;
let gadbadCurrentPrice = 20;

function openGadbadPage() {
    document.getElementById('gadbadModal').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeGadbadPage() {
    document.getElementById('gadbadModal').classList.remove('active');
    document.body.style.overflow = 'auto';
}

function selectGadbadFlavor(element, flavor, price) {
    document.querySelectorAll('#gadbadFlavorGrid .flavor-option').forEach(opt => {
        opt.classList.remove('selected');
    });
    element.classList.add('selected');
    selectedGadbadFlavor = flavor;
    gadbadUnitPrice = price;
    updateGadbadPrice();
}

function increaseGadbadQuantity() {
    const input = document.getElementById('gadbadQuantity');
    gadbadQuantity = (parseInt(input.value) || 1) + 1;
    input.value = gadbadQuantity;
    updateGadbadPrice();
}

function decreaseGadbadQuantity() {
    const input = document.getElementById('gadbadQuantity');
    gadbadQuantity = Math.max(1, (parseInt(input.value) || 1) - 1);
    input.value = gadbadQuantity;
    updateGadbadPrice();
}

function onGadbadQtyInput(input) {
    const val = parseInt(input.value);
    if (!isNaN(val) && val >= 1) {
        gadbadQuantity = val;
        updateGadbadPrice();
    }
}

function updateGadbadPrice() {
    gadbadCurrentPrice = gadbadUnitPrice * gadbadQuantity;
    document.getElementById('gadbadTotalPrice').textContent = 'Rs.' + gadbadCurrentPrice;
}

function addGadbadToCart() {
    const btn = document.getElementById('gadbadCartBtn');
    const cartItem = {
        product: 'Gadbad',
        flavor: selectedGadbadFlavor,
        quantity: gadbadQuantity,
        unitPrice: gadbadUnitPrice,
        price: gadbadCurrentPrice
    };

    let cart = localStorage.getItem('anandIceCreamCart');
    cart = cart ? JSON.parse(cart) : [];
    cart.push(cartItem);
    localStorage.setItem('anandIceCreamCart', JSON.stringify(cart));

    updateCartCountDisplay();

    btn.classList.add('added');
    btn.textContent = 'Added to Cart!';
    setTimeout(() => {
        btn.classList.remove('added');
        btn.textContent = 'Add to Cart';
    }, 2000);
}

// Wire Gadbad backdrop click
document.addEventListener('DOMContentLoaded', function () {
    const gadbadModal = document.getElementById('gadbadModal');
    if (gadbadModal) {
        gadbadModal.addEventListener('click', function (e) {
            if (e.target === this) closeGadbadPage();
        });
    }
});

// ========================
// Dolly Modal
// ========================
let selectedDollyFlavor = 'Mango';
let dollyUnitPrice = 20;
let dollyQuantity = 1;
let dollyCurrentPrice = 20;

function openDollyPage() {
    document.getElementById('dollyModal').classList.add('active');
    document.body.style.overflow = 'hidden';
}
function closeDollyPage() {
    document.getElementById('dollyModal').classList.remove('active');
    document.body.style.overflow = 'auto';
}
function selectDollyFlavor(el, flavor, price) {
    document.querySelectorAll('#dollyFlavorGrid .flavor-option').forEach(o => o.classList.remove('selected'));
    el.classList.add('selected');
    selectedDollyFlavor = flavor; dollyUnitPrice = price; updateDollyPrice();
}
function increaseDollyQty() {
    const inp = document.getElementById('dollyQuantity');
    dollyQuantity = (parseInt(inp.value) || 1) + 1; inp.value = dollyQuantity; updateDollyPrice();
}
function decreaseDollyQty() {
    const inp = document.getElementById('dollyQuantity');
    dollyQuantity = Math.max(1, (parseInt(inp.value) || 1) - 1); inp.value = dollyQuantity; updateDollyPrice();
}
function onDollyQtyInput(inp) {
    const v = parseInt(inp.value); if (!isNaN(v) && v >= 1) { dollyQuantity = v; updateDollyPrice(); }
}
function updateDollyPrice() {
    dollyCurrentPrice = dollyUnitPrice * dollyQuantity;
    document.getElementById('dollyTotalPrice').textContent = 'Rs.' + dollyCurrentPrice;
}
function addDollyToCart() {
    const btn = document.getElementById('dollyCartBtn');
    let cart = JSON.parse(localStorage.getItem('anandIceCreamCart') || '[]');
    cart.push({ product: 'Dolly', flavor: selectedDollyFlavor, quantity: dollyQuantity, unitPrice: dollyUnitPrice, price: dollyCurrentPrice });
    localStorage.setItem('anandIceCreamCart', JSON.stringify(cart));
    updateCartCountDisplay();
    btn.textContent = 'Added!';
    setTimeout(() => { btn.textContent = 'Add to Cart'; }, 2000);
}

// ========================
// Cone Modal
// ========================
let selectedConeFlavor = 'Butterscotch';
let coneUnitPrice = 40;
let coneQuantity = 1;
let coneCurrentPrice = 40;

function openConePage() {
    document.getElementById('coneModal').classList.add('active');
    document.body.style.overflow = 'hidden';
}
function closeConePage() {
    document.getElementById('coneModal').classList.remove('active');
    document.body.style.overflow = 'auto';
}
function selectConeFlavor(el, flavor, price) {
    document.querySelectorAll('#coneFlavorGrid .flavor-option').forEach(o => o.classList.remove('selected'));
    el.classList.add('selected');
    selectedConeFlavor = flavor; coneUnitPrice = price; updateConePrice();
}
function increaseConeQty() {
    const inp = document.getElementById('coneQuantity');
    coneQuantity = (parseInt(inp.value) || 1) + 1; inp.value = coneQuantity; updateConePrice();
}
function decreaseConeQty() {
    const inp = document.getElementById('coneQuantity');
    coneQuantity = Math.max(1, (parseInt(inp.value) || 1) - 1); inp.value = coneQuantity; updateConePrice();
}
function onConeQtyInput(inp) {
    const v = parseInt(inp.value); if (!isNaN(v) && v >= 1) { coneQuantity = v; updateConePrice(); }
}
function updateConePrice() {
    coneCurrentPrice = coneUnitPrice * coneQuantity;
    document.getElementById('coneTotalPrice').textContent = 'Rs.' + coneCurrentPrice;
}
function addConeToCart() {
    const btn = document.getElementById('coneCartBtn');
    let cart = JSON.parse(localStorage.getItem('anandIceCreamCart') || '[]');
    cart.push({ product: 'Cone', flavor: selectedConeFlavor, quantity: coneQuantity, unitPrice: coneUnitPrice, price: coneCurrentPrice });
    localStorage.setItem('anandIceCreamCart', JSON.stringify(cart));
    updateCartCountDisplay();
    btn.textContent = 'Added!';
    setTimeout(() => { btn.textContent = 'Add to Cart'; }, 2000);
}

// ========================
// Scoop Ice Cream Modal
// ========================
let selectedScoopFlavor = 'Sithapal';
let scoopUnitPrice = 20;
let scoopQuantity = 1;
let scoopCurrentPrice = 20;

function openScoopPage() {
    document.getElementById('scoopModal').classList.add('active');
    document.body.style.overflow = 'hidden';
}
function closeScoopPage() {
    document.getElementById('scoopModal').classList.remove('active');
    document.body.style.overflow = 'auto';
}
function selectScoopFlavor(el, flavor, price) {
    document.querySelectorAll('#scoopFlavorGrid .flavor-option').forEach(o => o.classList.remove('selected'));
    el.classList.add('selected');
    selectedScoopFlavor = flavor; scoopUnitPrice = price; updateScoopPrice();
}
function increaseScoopQty() {
    const inp = document.getElementById('scoopQuantity');
    scoopQuantity = (parseInt(inp.value) || 1) + 1; inp.value = scoopQuantity; updateScoopPrice();
}
function decreaseScoopQty() {
    const inp = document.getElementById('scoopQuantity');
    scoopQuantity = Math.max(1, (parseInt(inp.value) || 1) - 1); inp.value = scoopQuantity; updateScoopPrice();
}
function onScoopQtyInput(inp) {
    const v = parseInt(inp.value); if (!isNaN(v) && v >= 1) { scoopQuantity = v; updateScoopPrice(); }
}
function updateScoopPrice() {
    scoopCurrentPrice = scoopUnitPrice * scoopQuantity;
    document.getElementById('scoopTotalPrice').textContent = 'Rs.' + scoopCurrentPrice;
}
function addScoopToCart() {
    const btn = document.getElementById('scoopCartBtn');
    let cart = JSON.parse(localStorage.getItem('anandIceCreamCart') || '[]');
    cart.push({ product: 'Scoop Ice Cream', flavor: selectedScoopFlavor, quantity: scoopQuantity, unitPrice: scoopUnitPrice, price: scoopCurrentPrice });
    localStorage.setItem('anandIceCreamCart', JSON.stringify(cart));
    updateCartCountDisplay();
    btn.textContent = 'Added!';
    setTimeout(() => { btn.textContent = 'Add to Cart'; }, 2000);
}

// Wire backdrop click for Dolly, Cone, Scoop modals
document.addEventListener('DOMContentLoaded', function () {
    ['dollyModal', 'coneModal', 'scoopModal'].forEach(function (id) {
        const m = document.getElementById(id);
        if (m) m.addEventListener('click', function (e) { if (e.target === this) this.classList.remove('active'); document.body.style.overflow = 'auto'; });
    });
});

// ========================
// Chocbar Modal
// ========================
let selectedChocbarSize = 'Chocobar';
let chocbarUnitPrice = 20;
let chocbarQuantity = 1;
let chocbarCurrentPrice = 20;

function openChocbarPage() {
    document.getElementById('chocbarModal').classList.add('active');
    document.body.style.overflow = 'hidden';
}
function closeChocbarPage() {
    document.getElementById('chocbarModal').classList.remove('active');
    document.body.style.overflow = 'auto';
}
function selectChocbarSize(el, size, price) {
    document.querySelectorAll('#chocbarFlavorGrid .flavor-option').forEach(o => o.classList.remove('selected'));
    el.classList.add('selected');
    selectedChocbarSize = size; chocbarUnitPrice = price; updateChocbarPrice();
}
function increaseChocbarQty() {
    const inp = document.getElementById('chocbarQuantity');
    chocbarQuantity = (parseInt(inp.value) || 1) + 1; inp.value = chocbarQuantity; updateChocbarPrice();
}
function decreaseChocbarQty() {
    const inp = document.getElementById('chocbarQuantity');
    chocbarQuantity = Math.max(1, (parseInt(inp.value) || 1) - 1); inp.value = chocbarQuantity; updateChocbarPrice();
}
function onChocbarQtyInput(inp) {
    const v = parseInt(inp.value); if (!isNaN(v) && v >= 1) { chocbarQuantity = v; updateChocbarPrice(); }
}
function updateChocbarPrice() {
    chocbarCurrentPrice = chocbarUnitPrice * chocbarQuantity;
    document.getElementById('chocbarTotalPrice').textContent = 'Rs.' + chocbarCurrentPrice;
}
function addChocbarToCart() {
    const btn = document.getElementById('chocbarCartBtn');
    let cart = JSON.parse(localStorage.getItem('anandIceCreamCart') || '[]');
    cart.push({ product: 'Chocbar', flavor: selectedChocbarSize, quantity: chocbarQuantity, unitPrice: chocbarUnitPrice, price: chocbarCurrentPrice });
    localStorage.setItem('anandIceCreamCart', JSON.stringify(cart));
    updateCartCountDisplay();
    btn.textContent = 'Added!';
    setTimeout(() => { btn.textContent = 'Add to Cart'; }, 2000);
}

// ========================
// Family Pack Modal
// ========================
let selectedFamilySize = 'Half Liter';
let familyUnitPrice = 120;
let familyQuantity = 1;
let familyCurrentPrice = 120;

function openFamilyPage() {
    document.getElementById('familyModal').classList.add('active');
    document.body.style.overflow = 'hidden';
}
function closeFamilyPage() {
    document.getElementById('familyModal').classList.remove('active');
    document.body.style.overflow = 'auto';
}
function selectFamilySize(el, size, price) {
    document.querySelectorAll('#familyFlavorGrid .flavor-option').forEach(o => o.classList.remove('selected'));
    el.classList.add('selected');
    selectedFamilySize = size; familyUnitPrice = price; updateFamilyPrice();
}
function increaseFamilyQty() {
    const inp = document.getElementById('familyQuantity');
    familyQuantity = (parseInt(inp.value) || 1) + 1; inp.value = familyQuantity; updateFamilyPrice();
}
function decreaseFamilyQty() {
    const inp = document.getElementById('familyQuantity');
    familyQuantity = Math.max(1, (parseInt(inp.value) || 1) - 1); inp.value = familyQuantity; updateFamilyPrice();
}
function onFamilyQtyInput(inp) {
    const v = parseInt(inp.value); if (!isNaN(v) && v >= 1) { familyQuantity = v; updateFamilyPrice(); }
}
function updateFamilyPrice() {
    familyCurrentPrice = familyUnitPrice * familyQuantity;
    document.getElementById('familyTotalPrice').textContent = 'Rs.' + familyCurrentPrice;
}
function addFamilyToCart() {
    const btn = document.getElementById('familyCartBtn');
    let cart = JSON.parse(localStorage.getItem('anandIceCreamCart') || '[]');
    cart.push({ product: 'Family Pack', flavor: selectedFamilySize, quantity: familyQuantity, unitPrice: familyUnitPrice, price: familyCurrentPrice });
    localStorage.setItem('anandIceCreamCart', JSON.stringify(cart));
    updateCartCountDisplay();
    btn.textContent = 'Added!';
    setTimeout(() => { btn.textContent = 'Add to Cart'; }, 2000);
}

// Wire backdrop click for Chocbar and Family modals
document.addEventListener('DOMContentLoaded', function () {
    ['chocbarModal', 'familyModal'].forEach(function (id) {
        const m = document.getElementById(id);
        if (m) m.addEventListener('click', function (e) {
            if (e.target === this) { this.classList.remove('active'); document.body.style.overflow = 'auto'; }
        });
    });
});
