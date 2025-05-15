/**
 * Main JavaScript file for EduGrade system
 * Contains common functionality used across multiple pages
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme toggle functionality
    initThemeToggle();
    
    // Initialize dropdown functionality
    initDropdowns();
    
    // Initialize mobile sidebar functionality
    initMobileSidebar();
    
    // Initialize flash message auto-dismiss
    initFlashMessages();
});

/**
 * Initialize theme toggle functionality
 * Switches between light and dark mode
 */
function initThemeToggle() {
    const themeToggleButtons = document.querySelectorAll('#theme-toggle');
    
    // Check for saved theme preference or use the system preference
    if (localStorage.getItem('color-theme') === 'dark' || 
        (!localStorage.getItem('color-theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
    
    // Add toggle event listeners if theme toggle buttons exist
    themeToggleButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            // Toggle theme
            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('color-theme', 'light');
            } else {
                document.documentElement.classList.add('dark');
                localStorage.setItem('color-theme', 'dark');
            }
        });
    });
}

/**
 * Initialize dropdown functionality
 * Used for user menu, notifications, etc.
 */
function initDropdowns() {
    // User menu dropdown
    const userMenuButton = document.getElementById('user-menu-button');
    const userMenu = document.getElementById('user-menu');
    
    if (userMenuButton && userMenu) {
        userMenuButton.addEventListener('click', function() {
            userMenu.classList.toggle('hidden');
            
            // If the menu has additional animation classes
            if (userMenu.classList.contains('opacity-0')) {
                userMenu.classList.toggle('opacity-0');
                userMenu.classList.toggle('scale-95');
            }
        });
    }
    
    // Notifications dropdown
    const notificationsBtn = document.getElementById('notifications-btn');
    const notificationsDropdown = document.getElementById('notifications-dropdown');
    
    if (notificationsBtn && notificationsDropdown) {
        notificationsBtn.addEventListener('click', function() {
            notificationsDropdown.classList.toggle('hidden');
        });
    }
    
    // Profile dropdown (used on profile page)
    const profileMenuBtn = document.getElementById('profile-menu-btn');
    const profileDropdown = document.getElementById('profile-dropdown');
    
    if (profileMenuBtn && profileDropdown) {
        profileMenuBtn.addEventListener('click', function() {
            profileDropdown.classList.toggle('hidden');
        });
    }
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(event) {
        // User menu
        if (userMenuButton && userMenu && !userMenu.classList.contains('hidden') && 
            !userMenuButton.contains(event.target) && 
            !userMenu.contains(event.target)) {
            userMenu.classList.add('hidden');
            
            // If the menu has additional animation classes
            if (userMenu.classList.contains('opacity-0') !== undefined) {
                userMenu.classList.add('opacity-0', 'scale-95');
            }
        }
        
        // Notifications dropdown
        if (notificationsBtn && notificationsDropdown && !notificationsDropdown.classList.contains('hidden') && 
            !notificationsBtn.contains(event.target) && 
            !notificationsDropdown.contains(event.target)) {
            notificationsDropdown.classList.add('hidden');
        }
        
        // Profile dropdown
        if (profileMenuBtn && profileDropdown && !profileDropdown.classList.contains('hidden') && 
            !profileMenuBtn.contains(event.target) && 
            !profileDropdown.contains(event.target)) {
            profileDropdown.classList.add('hidden');
        }
    });
}

/**
 * Initialize mobile sidebar functionality
 */
function initMobileSidebar() {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebar-overlay');
    
    if (sidebarToggle && sidebar && sidebarOverlay) {
        // Toggle sidebar function
        function toggleSidebar() {
            sidebar.classList.toggle('-translate-x-full');
            sidebarOverlay.classList.toggle('hidden');
        }
        
        // Add event listeners
        sidebarToggle.addEventListener('click', toggleSidebar);
        sidebarOverlay.addEventListener('click', toggleSidebar);
    }
}

/**
 * Initialize flash messages auto-dismiss functionality
 */
function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(function(message) {
        // Add close button functionality
        const closeBtn = message.querySelector('.close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                message.remove();
            });
        }
        
        // Auto-dismiss after 5 seconds
        setTimeout(function() {
            // Fade out
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 300); // Match transition duration
        }, 5000);
    });
}

/**
 * Format a date string to local format
 * @param {string} dateStr - The date string to format
 * @returns {string} Formatted date string
 */
function formatDate(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleDateString();
}

/**
 * Truncate text to specific length with ellipsis
 * @param {string} text - The text to truncate
 * @param {number} length - Max length before truncating
 * @returns {string} Truncated text
 */
function truncateText(text, length = 100) {
    if (!text) return '';
    if (text.length <= length) return text;
    return text.substring(0, length) + '...';
}

/**
 * Handle API error responses
 * @param {Response} response - The fetch API response
 * @throws {Error} Throws an error with the appropriate message
 */
async function handleApiError(response) {
    if (!response.ok) {
        let errorMessage = 'Error en la solicitud: ';
        try {
            const errorData = await response.json();
            errorMessage += errorData.message || response.statusText;
        } catch (e) {
            errorMessage += response.statusText;
        }
        throw new Error(errorMessage);
    }
    return response;
}

/**
 * Shows a notification/toast message
 * @param {string} message - The message to show
 * @param {string} type - The message type (success, error, info)
 */
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    
    // Set class based on type
    let bgColor = 'bg-blue-500';
    if (type === 'success') bgColor = 'bg-green-500';
    if (type === 'error') bgColor = 'bg-red-500';
    
    notification.className = `${bgColor} text-white px-4 py-3 rounded shadow-md mb-2 animate-fade-in flex items-center justify-between`;
    
    // Create message and close button
    notification.innerHTML = `
        <p>${message}</p>
        <button class="ml-4 text-white focus:outline-none">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Get or create notifications container
    let container = document.querySelector('.notifications-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'fixed top-4 right-4 z-50 w-full max-w-sm space-y-2';
        document.body.appendChild(container);
    }
    
    // Add notification to container
    container.appendChild(notification);
    
    // Add close button functionality
    const closeButton = notification.querySelector('button');
    closeButton.addEventListener('click', () => {
        notification.remove();
    });
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        notification.remove();
    }, 5000);
}
