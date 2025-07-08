// multi-step-form.js

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

    // Step tracking
    let currentStepIndex = 0;
    const totalSteps = steps.length - 1;

    function initForm() {
        updateProgressBar();
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

        fetch('/contact/', {
            method: 'POST',
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showStep(4);
                    setTimeout(() => {
                        showStep(0);
                        nameInput.value = '';
                        emailInput.value = '';
                        messageInput.value = '';
                        submitBtn.disabled = false;
                        submitBtn.textContent = 'Submit';
                    }, 5000);
                } else {
                    alert(data.message || 'Submission failed.');
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Submit';
                }
            })
            .catch(error => {
                console.error('Submission error:', error);
                alert('An error occurred. Please try again later.');
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit';
            });
    }

    function addEventListeners() {
        startBtn.addEventListener('click', () => showStep(1));

        nameNextBtn.addEventListener('click', () => {
            if (nameInput.value.trim() !== '') nextStep();
            else nameInput.focus();
        });

        emailNextBtn.addEventListener('click', () => {
            if (emailInput.value.trim() && isValidEmail(emailInput.value)) {
                nextStep();
            } else {
                emailInput.focus();
            }
        });

        submitBtn.addEventListener('click', () => {
            if (messageInput.value.trim() !== '') {
                submitForm();
            } else {
                messageInput.focus();
            }
        });

        navUp.addEventListener('click', prevStep);
        navDown.addEventListener('click', nextStep);

        // Keyboard navigation
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                if (currentStepIndex === 0) startBtn.click();
                else if (currentStepIndex === 1 && document.activeElement === nameInput) nameNextBtn.click();
                else if (currentStepIndex === 2 && document.activeElement === emailInput) emailNextBtn.click();
                e.preventDefault();
            }

            if (!['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
                if (e.key === 'ArrowUp') {
                    prevStep();
                    e.preventDefault();
                } else if (e.key === 'ArrowDown') {
                    nextStep();
                    e.preventDefault();
                }
            }
        });

        nameInput.addEventListener('keydown', e => {
            if (e.key === 'Enter') {
                nameNextBtn.click();
                e.preventDefault();
            }
        });

        emailInput.addEventListener('keydown', e => {
            if (e.key === 'Enter') {
                emailNextBtn.click();
                e.preventDefault();
            }
        });

        messageInput.addEventListener('keydown', e => {
            if (e.key === 'Enter' && !e.shiftKey) {
                submitBtn.click();
                e.preventDefault();
            }
        });
    }

    initForm();
});
