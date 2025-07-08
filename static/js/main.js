/**
 * Main JavaScript file for Sudeesh Sathya Portfolio
 */



document.addEventListener('DOMContentLoaded', function () {
    // Mobile Navigation Toggle
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

    // Close mobile menu when clicking on a nav item
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function () {
            hamburger.classList.remove('active');
            leftNavLinks.classList.remove('active');
            rightNavLinks.classList.remove('active');
        });
    });

    // Highlight active nav item based on scroll position
    const sections = document.querySelectorAll('section[id]');

    function highlightNavItem() {
        const scrollY = window.pageYOffset;

        sections.forEach(current => {
            const sectionHeight = current.offsetHeight;
            const sectionTop = current.offsetTop - 100;
            const sectionId = current.getAttribute('id');

            if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                document.querySelector('.nav-links a[href*=' + sectionId + ']').classList.add('active');
            } else {
                document.querySelector('.nav-links a[href*=' + sectionId + ']').classList.remove('active');
            }
        });
    }

    // Add scroll event listener for nav highlighting
    window.addEventListener('scroll', highlightNavItem);

    // Dynamic navbar behavior
    const header = document.querySelector('header');
    let lastScrollY = window.scrollY;
    let scrollingTimeout;

    function handleNavbarVisibility() {
        const currentScrollY = window.scrollY;

        // At the top of the page
        if (currentScrollY <= 10) {
            header.classList.remove('scrolled');
            header.classList.remove('hidden');
        }
        // Scrolling down - hide navbar
        else if (currentScrollY > lastScrollY) {
            header.classList.add('scrolled');
            header.classList.add('hidden');
        }
        // Scrolling up - show navbar with black background
        else {
            header.classList.add('scrolled');
            header.classList.remove('hidden');
        }

        lastScrollY = currentScrollY;
    }

    // Throttle scroll events for better performance
    window.addEventListener('scroll', function () {
        if (!scrollingTimeout) {
            scrollingTimeout = setTimeout(function () {
                handleNavbarVisibility();
                scrollingTimeout = null;
            }, 10);
        }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 70,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Modal functionality for clickable images
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    const modalTitle = document.getElementById('modalTitle');
    const modalClose = document.querySelector('.modal-close');
    const clickableImages = document.querySelectorAll('.clickable-image');

    // Open modal when clicking on an image
    clickableImages.forEach(image => {
        image.addEventListener('click', function () {
            const imageSrc = this.getAttribute('data-modal-image');
            const imageTitle = this.getAttribute('data-modal-title');

            modalImage.src = imageSrc;
            modalTitle.textContent = imageTitle;

            modal.style.display = 'block';
            setTimeout(() => {
                modal.classList.add('show');
            }, 10);

            // Prevent scrolling on body when modal is open
            document.body.style.overflow = 'hidden';
        });
    });

    // Close modal when clicking on the close button
    modalClose.addEventListener('click', closeModal);

    // Close modal when clicking outside the modal content
    modal.addEventListener('click', function (e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Close modal when pressing Escape key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.style.display === 'block') {
            closeModal();
        }
    });

    function closeModal() {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.style.display = 'none';
            // Re-enable scrolling on body
            document.body.style.overflow = 'auto';
        }, 300);
    }

    // Form validation for contact form
    const contactForm = document.querySelector('.contact-form form');

    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const nameInput = document.getElementById('name');
            const emailInput = document.getElementById('email');
            const messageInput = document.getElementById('message');

            let isValid = true;

            // Simple validation
            if (nameInput.value.trim() === '') {
                isValid = false;
                showError(nameInput, 'Name is required');
            } else {
                removeError(nameInput);
            }

            if (emailInput.value.trim() === '') {
                isValid = false;
                showError(emailInput, 'Email is required');
            } else if (!isValidEmail(emailInput.value)) {
                isValid = false;
                showError(emailInput, 'Please enter a valid email');
            } else {
                removeError(emailInput);
            }

            if (messageInput.value.trim() === '') {
                isValid = false;
                showError(messageInput, 'Message is required');
            } else {
                removeError(messageInput);
            }

            if (isValid) {
                // In a real Django app, this would submit the form
                // For this template, we'll just show a success message
                showSuccess(contactForm);
            }
        });
    }

    // Helper functions for form validation
    function showError(input, message) {
        const formGroup = input.parentElement;
        const errorElement = formGroup.querySelector('.error-message') || document.createElement('div');

        errorElement.className = 'error-message';
        errorElement.textContent = message;

        if (!formGroup.querySelector('.error-message')) {
            formGroup.appendChild(errorElement);
        }

        input.classList.add('error');
    }

    function removeError(input) {
        const formGroup = input.parentElement;
        const errorElement = formGroup.querySelector('.error-message');

        if (errorElement) {
            formGroup.removeChild(errorElement);
        }

        input.classList.remove('error');
    }

    function isValidEmail(email) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }

    function showSuccess(form) {
        // Hide the form
        form.style.display = 'none';

        // Create success message
        const successMessage = document.createElement('div');
        successMessage.className = 'success-message';
        successMessage.innerHTML = `
            <i class="fas fa-check-circle"></i>
            <h3>Message Sent!</h3>
            <p>Thank you for reaching out. I'll get back to you soon.</p>
        `;

        // Add success message to the form's parent
        form.parentElement.appendChild(successMessage);
    }
});


document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('subscription-modal');
    const closeBtn = document.querySelector('.close-btn');
    const sessionKey = 'subscriptionModalShown';

    if (!sessionStorage.getItem(sessionKey)) {
        setTimeout(() => {
            modal.style.display = 'flex';
            sessionStorage.setItem(sessionKey, 'true');
        }, 1500);
    }

    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Shared handler for both forms
    const handleSubscribe = (formId, messageId) => {
        const form = document.getElementById(formId);
        const message = document.getElementById(messageId);

        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const email = form.querySelector('input[name="email"]').value;
            const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

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
                message.textContent = data.message;
                message.style.color = data.success ? 'green' : 'red';
                if (data.success) form.reset();
            })
            .catch(() => {
                message.textContent = 'Something went wrong.';
                message.style.color = 'red';
            });
        });
    };

    handleSubscribe('modal-subscribe-form', 'modal-subscribe-message');
    handleSubscribe('footer-subscribe-form', 'footer-subscribe-message');
});


