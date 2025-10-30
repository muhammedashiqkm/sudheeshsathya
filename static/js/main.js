/**
 * Main JavaScript file for Sudeesh Sathya Portfolio
 *
 * Combines all event listeners for better organization and removes redundant code.
 */

document.addEventListener('DOMContentLoaded', function () {

    // =========================================================================
    // SECTION: GLOBAL SITE FEATURES
    // =========================================================================

    // --- Mobile Navigation Toggle ---
    const hamburger = document.getElementById('hamburger');
    const leftNavLinks = document.getElementById('leftNavLinks');
    const rightNavLinks = document.getElementById('rightNavLinks');

    if (hamburger) {
        hamburger.addEventListener('click', function () {
            hamburger.classList.toggle('active');
            leftNavLinks.classList.toggle('active');
            rightNavLinks.classList.toggle('active');
        });
    }

    // --- Close mobile menu when clicking a nav item ---
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function () {
            if (hamburger.classList.contains('active')) {
                hamburger.classList.remove('active');
                leftNavLinks.classList.remove('active');
                rightNavLinks.classList.remove('active');
            }
        });
    });

    // --- Highlight active nav item on scroll ---
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-links a');

    function highlightNavItem() {
        let currentSectionId = '';
        const scrollY = window.pageYOffset;

        sections.forEach(current => {
            const sectionHeight = current.offsetHeight;
            const sectionTop = current.offsetTop - 100;
            if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                currentSectionId = current.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            
            // --- THIS IS THE FIX ---
            // Only add 'active' if currentSectionId is NOT empty
            if (currentSectionId && link.getAttribute('href').includes(currentSectionId)) {
                link.classList.add('active');
            }
        });
    }
    window.addEventListener('scroll', highlightNavItem);


    // --- Dynamic navbar visibility on scroll ---
    const header = document.querySelector('header');
    let lastScrollY = window.scrollY;

    function handleNavbarVisibility() {
        const currentScrollY = window.scrollY;

        if (currentScrollY <= 10) {
            header.classList.remove('scrolled', 'hidden');
        } else if (currentScrollY > lastScrollY) {
            header.classList.add('scrolled', 'hidden');
        } else {
            header.classList.add('scrolled');
            header.classList.remove('hidden');
        }
        lastScrollY = currentScrollY;
    }
    window.addEventListener('scroll', handleNavbarVisibility, { passive: true });


    // --- Smooth scrolling for anchor links ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 70, // Adjust for fixed header
                    behavior: 'smooth'
                });
            }
        });
    });

    // =========================================================================
    // SECTION: SUBSCRIPTION MODAL & FORMS
    // =========================================================================

    // --- Subscription Modal Logic ---
    const subscriptionModal = document.getElementById('subscription-modal');
    const closeBtn = document.querySelector('.subscription-modal .close-btn');
    const sessionKey = 'subscriptionModalShown';

    // Show modal only once per session
    if (subscriptionModal && !sessionStorage.getItem(sessionKey)) {
        setTimeout(() => {
            subscriptionModal.style.display = 'flex';
            sessionStorage.setItem(sessionKey, 'true');
        }, 1500);
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            subscriptionModal.style.display = 'none';
        });
    }

    // --- Shared Subscription Form Handler ---
    // --- Shared Subscription Form Handler with Loading & Validation ---
const handleSubscribe = (formId, messageId) => {
    const form = document.getElementById(formId);
    const message = document.getElementById(messageId);
    const submitBtn = form.querySelector('button[type="submit"]');

    if (!form || !message || !submitBtn) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const emailInput = form.querySelector('input[name="email"]');
        const email = emailInput.value.trim();
        const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!email) {
            showMessage('Please enter your email.', false);
            emailInput.focus();
            return;
        }
        if (!emailRegex.test(email)) {
            showMessage('Please enter a valid email address.', false);
            emailInput.focus();
            return;
        }

        // Show loading
        submitBtn.disabled = true;
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Subscribe...';

        fetch('/subscribe/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
            },
            body: new URLSearchParams({ email })
        })
        .then(res => res.json())
        .then(data => {
            showMessage(data.message, data.success);
            if (data.success) {
                form.reset();
            }
        })
        .catch(() => {
            showMessage('An error occurred. Please try again.', false);
        })
        .finally(() => {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        });
    });

    function showMessage(text, isSuccess) {
        message.textContent = text;
        message.style.color = isSuccess ? 'var(--success-color)' : 'var(--danger-color)';
        message.style.opacity = '1';
        setTimeout(() => { message.style.opacity = '0'; }, 4000);
    }
};

// Initialize handlers
handleSubscribe('modal-subscribe-form', 'modal-subscribe-message');
handleSubscribe('footer-subscribe-form', 'footer-subscribe-message');

});