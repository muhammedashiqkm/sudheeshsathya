// contact-form.js - Complete with Inline Email Validation on "OK"

document.addEventListener('DOMContentLoaded', function () {
    // Form elements
    const steps = document.querySelectorAll('.message-step');
    const progressBar = document.getElementById('form-progress-bar');
    const navUp = document.getElementById('nav-up');
    const navDown = document.getElementById('nav-down');

    // Buttons
    const startBtn = document.getElementById('btn-start');
    const nameNextBtn = document.getElementById('btn-name-next');
    const emailNextBtn = document.getElementById('btn-email-next');
    const submitBtn = document.getElementById('btn-submit');

    // Input fields
    const nameInput = document.getElementById('input-name');
    const emailInput = document.getElementById('input-email');
    const messageInput = document.getElementById('input-message');

    // Error element (will be created)
    let emailError = null;

    // Step tracking
    let currentStepIndex = 0;
    const totalSteps = steps.length - 1;

    function initForm() {
        updateProgressBar();
        createEmailErrorElement();
        addEventListeners();
    }

    function updateProgressBar() {
        const progress = (currentStepIndex / totalSteps) * 100;
        progressBar.style.width = `${progress}%`;
    }

    function showStep(index) {
        steps.forEach(step => step.classList.remove('active'));
        steps[index].classList.add('active');
        currentStepIndex = index;
        updateProgressBar();
        focusInput(index);
        updateNavButtons();
    }

    function focusInput(index) {
        setTimeout(() => {
            if (index === 1) nameInput.focus();
            else if (index === 2) emailInput.focus();
            else if (index === 3) messageInput.focus();
        }, 300);
    }

    function updateNavButtons() {
        if (currentStepIndex === 0 || currentStepIndex === 4) {
            navUp.style.display = 'none';
            navDown.style.display = 'none';
            return;
        }
        navUp.style.display = currentStepIndex > 1 ? 'flex' : 'none';
        navDown.style.display = currentStepIndex < 3 ? 'flex' : 'none';
    }

    function nextStep() {
        if (currentStepIndex < totalSteps) {
            showStep(currentStepIndex + 1);
        }
    }

    function prevStep() {
        if (currentStepIndex > 0) {
            showStep(currentStepIndex - 1);
        }
    }

    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // === CREATE EMAIL ERROR MESSAGE ELEMENT ===
    function createEmailErrorElement() {
        const emailStep = document.getElementById('step-email');
        emailError = document.createElement('div');
        emailError.className = 'error-message';
        emailError.style.cssText = `
            color: var(--danger-color);
            font-size: 0.85rem;
            margin-top: 8px;
            opacity: 0;
            transition: opacity 0.3s ease;
            min-height: 20px;
            font-style: italic;
        `;
        emailStep.querySelector('.message-action').appendChild(emailError);
    }

    // === SHOW / HIDE ERROR ===
    function showEmailError(message) {
        emailError.textContent = message;
        emailError.style.opacity = '1';
    }

    function hideEmailError() {
        emailError.style.opacity = '0';
        setTimeout(() => {
            emailError.textContent = '';
        }, 300);
    }

    // === SUBMIT FORM ===
    function submitForm() {
        const name = nameInput.value.trim();
        const email = emailInput.value.trim();
        const message = messageInput.value.trim();

        if (!name || !email || !message) {
            alert('Please fill in all required fields.');
            return;
        }

        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';

        const formData = new FormData();
        formData.append('name', name);
        formData.append('email', email);
        formData.append('message', message);
        const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
        formData.append('csrfmiddlewaretoken', csrfToken);

        fetch('/contact/', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showStep(4);
                setTimeout(() => {
                    resetForm();
                }, 4000);
            } else {
                alert(data.message || 'Failed to send message.');
                resetSubmitButton();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Network error. Please try again.');
            resetSubmitButton();
        });
    }

    function resetForm() {
        showStep(0);
        nameInput.value = '';
        emailInput.value = '';
        messageInput.value = '';
        hideEmailError();
        resetSubmitButton();
    }

    function resetSubmitButton() {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit';
    }

    // === EVENT LISTENERS ===
    function addEventListeners() {
        startBtn.addEventListener('click', () => showStep(1));

        nameNextBtn.addEventListener('click', () => {
            if (nameInput.value.trim()) {
                nextStep();
            } else {
                nameInput.focus();
            }
        });

        // EMAIL VALIDATION ON "OK" CLICK
        emailNextBtn.addEventListener('click', () => {
            const email = emailInput.value.trim();

            if (!email) {
                showEmailError('Email is required.');
                emailInput.focus();
                return;
            }
            if (!isValidEmail(email)) {
                showEmailError('Please enter a valid email address.');
                emailInput.focus();
                return;
            }

            hideEmailError();
            nextStep();
        });

        submitBtn.addEventListener('click', submitForm);

        navUp.addEventListener('click', prevStep);
        navDown.addEventListener('click', nextStep);

        // === KEYBOARD NAVIGATION ===
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                if (currentStepIndex === 0) startBtn.click();
                else if (currentStepIndex === 1 && document.activeElement === nameInput) nameNextBtn.click();
                else if (currentStepIndex === 2 && document.activeElement === emailInput) emailNextBtn.click();
            }

            if (!['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
                if (e.key === 'ArrowUp') { prevStep(); e.preventDefault(); }
                if (e.key === 'ArrowDown') { nextStep(); e.preventDefault(); }
            }
        });

        nameInput.addEventListener('keydown', e => {
            if (e.key === 'Enter') { e.preventDefault(); nameNextBtn.click(); }
        });

        emailInput.addEventListener('keydown', e => {
            if (e.key === 'Enter') { e.preventDefault(); emailNextBtn.click(); }
        });

        messageInput.addEventListener('keydown', e => {
            if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); submitBtn.click(); }
        });
    }

    // Initialize
    initForm();
});