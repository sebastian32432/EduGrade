/**
 * Auth-related functionality for EduGrade system
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize login form validation
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        initLoginForm(loginForm);
    }
    
    // Initialize registration form validation
    const registrationForm = document.getElementById('registration-form');
    if (registrationForm) {
        initRegistrationForm(registrationForm);
    }
    
    // Setup toggle between login and registration forms if both exist on the page
    const loginTab = document.getElementById('login-tab');
    const registerTab = document.getElementById('register-tab');
    
    if (loginTab && registerTab) {
        setupFormToggle(loginTab, registerTab);
    }
});

/**
 * Initialize login form validation and submission
 * @param {HTMLElement} form - The login form element
 */
function initLoginForm(form) {
    form.addEventListener('submit', function(event) {
        // Prevent default form submission
        event.preventDefault();
        
        // Get form inputs
        const username = form.querySelector('#username');
        const password = form.querySelector('#password');
        
        // Reset previous error messages
        clearErrors(form);
        
        // Validate form
        let isValid = true;
        
        if (!username.value.trim()) {
            showError(username, 'El nombre de usuario es requerido');
            isValid = false;
        }
        
        if (!password.value) {
            showError(password, 'La contraseña es requerida');
            isValid = false;
        }
        
        // If form is valid, submit it
        if (isValid) {
            form.submit();
        }
    });
}

/**
 * Initialize registration form validation and submission
 * @param {HTMLElement} form - The registration form element
 */
function initRegistrationForm(form) {
    form.addEventListener('submit', function(event) {
        // Prevent default form submission
        event.preventDefault();
        
        // Get form inputs
        const username = form.querySelector('#username');
        const email = form.querySelector('#email');
        const firstName = form.querySelector('#first_name');
        const lastName = form.querySelector('#last_name');
        const password = form.querySelector('#password');
        const confirmPassword = form.querySelector('#password_confirm');
        
        // Reset previous error messages
        clearErrors(form);
        
        // Validate form
        let isValid = true;
        
        if (!username.value.trim()) {
            showError(username, 'El nombre de usuario es requerido');
            isValid = false;
        } else if (username.value.trim().length < 3) {
            showError(username, 'El nombre de usuario debe tener al menos 3 caracteres');
            isValid = false;
        }
        
        if (!email.value.trim()) {
            showError(email, 'El correo electrónico es requerido');
            isValid = false;
        } else if (!isValidEmail(email.value.trim())) {
            showError(email, 'Ingrese un correo electrónico válido');
            isValid = false;
        }
        
        if (!firstName.value.trim()) {
            showError(firstName, 'El nombre es requerido');
            isValid = false;
        }
        
        if (!lastName.value.trim()) {
            showError(lastName, 'El apellido es requerido');
            isValid = false;
        }
        
        if (!password.value) {
            showError(password, 'La contraseña es requerida');
            isValid = false;
        } else if (password.value.length < 6) {
            showError(password, 'La contraseña debe tener al menos 6 caracteres');
            isValid = false;
        }
        
        if (password.value !== confirmPassword.value) {
            showError(confirmPassword, 'Las contraseñas no coinciden');
            isValid = false;
        }
        
        // If form is valid, submit it
        if (isValid) {
            form.submit();
        }
    });
}

/**
 * Setup toggle between login and registration forms
 * @param {HTMLElement} loginTab - The login tab element
 * @param {HTMLElement} registerTab - The registration tab element
 */
function setupFormToggle(loginTab, registerTab) {
    const loginForm = document.getElementById('login-form');
    const registrationForm = document.getElementById('registration-form');
    
    loginTab.addEventListener('click', function() {
        // Make login form active
        loginTab.classList.add('bg-white', 'dark:bg-gray-800', 'border-primary-500', 'dark:border-primary-400');
        registerTab.classList.remove('bg-white', 'dark:bg-gray-800', 'border-primary-500', 'dark:border-primary-400');
        
        loginForm.classList.remove('hidden');
        registrationForm.classList.add('hidden');
    });
    
    registerTab.addEventListener('click', function() {
        // Make registration form active
        registerTab.classList.add('bg-white', 'dark:bg-gray-800', 'border-primary-500', 'dark:border-primary-400');
        loginTab.classList.remove('bg-white', 'dark:bg-gray-800', 'border-primary-500', 'dark:border-primary-400');
        
        registrationForm.classList.remove('hidden');
        loginForm.classList.add('hidden');
    });
}

/**
 * Show error message for an input
 * @param {HTMLElement} input - The input element
 * @param {string} message - The error message
 */
function showError(input, message) {
    const formGroup = input.closest('.form-group');
    const errorElement = formGroup.querySelector('.error-message');
    
    // Add error class to input
    input.classList.add('border-red-500', 'dark:border-red-500');
    
    // Create error message element if it doesn't exist
    if (!errorElement) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'text-red-500 text-sm mt-1 error-message';
        errorDiv.textContent = message;
        formGroup.appendChild(errorDiv);
    } else {
        errorElement.textContent = message;
        errorElement.classList.remove('hidden');
    }
}

/**
 * Clear all error messages in a form
 * @param {HTMLElement} form - The form element
 */
function clearErrors(form) {
    // Remove error class from all inputs
    const inputs = form.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.classList.remove('border-red-500', 'dark:border-red-500');
    });
    
    // Hide all error messages
    const errorMessages = form.querySelectorAll('.error-message');
    errorMessages.forEach(errorMessage => {
        errorMessage.textContent = '';
        errorMessage.classList.add('hidden');
    });
}

/**
 * Validate email format
 * @param {string} email - The email to validate
 * @returns {boolean} Whether the email is valid
 */
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Redirect to appropriate dashboard based on user role
 */
function redirectBasedOnRole() {
    // Get user role from the hidden input
    const roleInput = document.getElementById('user-role');
    if (!roleInput) return;
    
    const role = roleInput.value;
    
    // Redirect based on role
    if (role === 'admin') {
        window.location.href = '/admin/dashboard';
    } else if (role === 'teacher') {
        window.location.href = '/teacher/dashboard';
    } else if (role === 'student') {
        window.location.href = '/student/dashboard';
    }
}
