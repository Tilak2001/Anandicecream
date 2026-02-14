// Cart Management System

// Get cart from localStorage
function getCart() {
    const cart = localStorage.getItem('anandIceCreamCart');
    return cart ? JSON.parse(cart) : [];
}

// Save cart to localStorage
function saveCart(cart) {
    localStorage.setItem('anandIceCreamCart', JSON.stringify(cart));
    updateCartCount();
}

// Update cart count in navbar
function updateCartCount() {
    const cart = getCart();
    const cartCount = document.getElementById('cartCount');
    if (cartCount) {
        cartCount.textContent = cart.length;
    }
}

// Display cart items
function displayCart() {
    const cart = getCart();
    const container = document.getElementById('cartItemsContainer');
    const summary = document.getElementById('cartSummary');

    if (cart.length === 0) {
        container.innerHTML = `
            <div class="empty-cart">
                <div class="empty-cart-icon">🛒</div>
                <h2>Your cart is empty</h2>
                <p>Add some delicious ice cream to get started!</p>
                <a href="index.html" class="continue-shopping">Continue Shopping</a>
            </div>
        `;
        summary.style.display = 'none';
    } else {
        // Display cart items
        let itemsHTML = '<div class="cart-items">';
        let total = 0;

        cart.forEach((item, index) => {
            total += item.price;
            const sizeOrQuantity = item.quantity
                ? `Quantity: ${item.quantity}`
                : `Size: ${item.size}`;

            itemsHTML += `
                <div class="cart-item">
                    <div class="item-info">
                        <div class="item-icon">🍦</div>
                        <div class="item-details">
                            <div class="item-name">${item.product}</div>
                            <div class="item-flavor">Flavor: ${item.flavor}</div>
                            <div class="item-size">${sizeOrQuantity}</div>
                        </div>
                    </div>
                    <div class="item-price">₹${item.price}</div>
                    <button class="remove-btn" onclick="removeFromCart(${index})">Remove</button>
                </div>
            `;
        });

        itemsHTML += '</div>';
        container.innerHTML = itemsHTML;

        // Update summary
        document.getElementById('subtotal').textContent = '₹' + total;
        document.getElementById('total').textContent = '₹' + total;
        summary.style.display = 'block';
    }
}

// Remove item from cart
function removeFromCart(index) {
    const cart = getCart();
    cart.splice(index, 1);
    saveCart(cart);
    displayCart();
}

// Checkout function - opens the checkout modal
function checkout() {
    const cart = getCart();
    if (cart.length === 0) {
        alert('Your cart is empty!');
        return;
    }

    // Show checkout modal
    const modal = document.getElementById('checkoutModal');
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

// Close checkout modal
function closeCheckoutModal() {
    const modal = document.getElementById('checkoutModal');
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';

    // Reset form
    document.getElementById('checkoutForm').reset();
}

// Submit order function - now redirects to payment page
async function submitOrder(event) {
    event.preventDefault();

    const cart = getCart();
    const total = cart.reduce((sum, item) => sum + item.price, 0);

    // Collect form data
    const orderData = {
        customerInfo: {
            fullName: document.getElementById('fullName').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            deliveryAddress: document.getElementById('address').value,
            pincode: document.getElementById('pincode').value,
            alternatePhone: document.getElementById('alternatePhone').value || null
        },
        items: cart,
        totalAmount: total,
        orderDate: new Date().toISOString(),
        status: 'pending'
    };

    // Save order data to localStorage for payment page
    localStorage.setItem('pendingOrder', JSON.stringify(orderData));

    // Redirect to payment page
    window.location.href = 'payment.html';
}

// Initialize cart on page load
document.addEventListener('DOMContentLoaded', function () {
    updateCartCount();

    // Only display cart if we're on the cart page
    if (document.getElementById('cartItemsContainer')) {
        displayCart();
    }
});
