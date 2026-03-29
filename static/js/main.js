// InvenLogic Pro - Main JavaScript

// ============= VALIDATION FUNCTIONS =============

// Validate email format
function validateEmail(email) {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailPattern.test(email);
}

// Validate phone number (exactly 10 digits)
function validatePhone(phone) {
    const phoneClean = phone.replace(/[\s\-\(\)]/g, '');
    return /^\d{10}$/.test(phoneClean);
}

// Validate password (must contain special character)
function validatePassword(password) {
    if (password.length < 8) return false;
    const specialChars = /[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/;~`]/;
    return specialChars.test(password);
}

// Validate name (no numbers allowed)
function validateName(name) {
    if (!name || name.trim().length < 2) return false;
    return !/\d/.test(name);
}

// Show validation error
function showError(input, message) {
    input.style.borderColor = '#ef4444';
    let errorDiv = input.nextElementSibling;
    if (!errorDiv || !errorDiv.classList.contains('error-message')) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.style.color = '#ef4444';
        errorDiv.style.fontSize = '0.875rem';
        errorDiv.style.marginTop = '0.25rem';
        input.parentNode.insertBefore(errorDiv, input.nextSibling);
    }
    errorDiv.textContent = message;
}

// Clear validation error
function clearError(input) {
    input.style.borderColor = '#e2e8f0';
    const errorDiv = input.nextElementSibling;
    if (errorDiv && errorDiv.classList.contains('error-message')) {
        errorDiv.remove();
    }
}

// Real-time validation setup
function setupValidation() {
    // Email validation
    document.querySelectorAll('input[type="email"]').forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value && !validateEmail(this.value)) {
                showError(this, 'Invalid email format. Email must contain @ and a valid domain');
            } else {
                clearError(this);
            }
        });
        input.addEventListener('input', function() {
            if (this.value && validateEmail(this.value)) {
                clearError(this);
            }
        });
    });

    // Phone validation
    document.querySelectorAll('input[name="phone"]').forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value && !validatePhone(this.value)) {
                showError(this, 'Phone number must be exactly 10 digits');
            } else {
                clearError(this);
            }
        });
        input.addEventListener('input', function() {
            if (this.value && validatePhone(this.value)) {
                clearError(this);
            }
        });
    });

    // Password validation
    document.querySelectorAll('input[type="password"][name="password"], input[type="password"][name="new_password"]').forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value && !validatePassword(this.value)) {
                showError(this, 'Password must be at least 8 characters and contain a special character');
            } else {
                clearError(this);
            }
        });
        input.addEventListener('input', function() {
            if (this.value && validatePassword(this.value)) {
                clearError(this);
            }
        });
    });

    // Name validation (username, buyer_name, supplier_name, contact_person)
    document.querySelectorAll('input[name="username"], input[name="buyer_name"], input[name="supplier_name"], input[name="contact_person"]').forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value && !validateName(this.value)) {
                const fieldName = this.name.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
                showError(this, `${fieldName} cannot contain numbers and must be at least 2 characters`);
            } else {
                clearError(this);
            }
        });
        input.addEventListener('input', function() {
            if (this.value && validateName(this.value)) {
                clearError(this);
            }
        });
    });
}

// Form submission validation
function validateFormOnSubmit(form) {
    let isValid = true;

    // Validate all email fields
    form.querySelectorAll('input[type="email"]').forEach(input => {
        if (input.value && !validateEmail(input.value)) {
            showError(input, 'Invalid email format. Email must contain @ and a valid domain');
            isValid = false;
        }
    });

    // Validate all phone fields
    form.querySelectorAll('input[name="phone"]').forEach(input => {
        if (input.value && !validatePhone(input.value)) {
            showError(input, 'Phone number must be exactly 10 digits');
            isValid = false;
        }
    });

    // Validate all password fields
    form.querySelectorAll('input[type="password"][name="password"], input[type="password"][name="new_password"]').forEach(input => {
        if (input.value && !validatePassword(input.value)) {
            showError(input, 'Password must be at least 8 characters and contain a special character');
            isValid = false;
        }
    });

    // Validate all name fields
    form.querySelectorAll('input[name="username"], input[name="buyer_name"], input[name="supplier_name"], input[name="contact_person"]').forEach(input => {
        if (input.value && !validateName(input.value)) {
            const fieldName = input.name.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
            showError(input, `${fieldName} cannot contain numbers and must be at least 2 characters`);
            isValid = false;
        }
    });

    // Validate password confirmation
    const password = form.querySelector('input[name="password"]');
    const confirmPassword = form.querySelector('input[name="confirm_password"]');
    if (password && confirmPassword && password.value !== confirmPassword.value) {
        showError(confirmPassword, 'Passwords do not match');
        isValid = false;
    }

    return isValid;
}

// Auto-hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    // Setup real-time validation
    setupValidation();

    // Add form submission validation
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateFormOnSubmit(this)) {
                e.preventDefault();
                // Scroll to first error
                const firstError = this.querySelector('.error-message');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    });
});


