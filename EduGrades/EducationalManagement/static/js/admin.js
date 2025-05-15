/**
 * Admin-specific functionality for EduGrade system
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize users table functionality
    initUsersTable();
    
    // Initialize user form validation
    initUserForm();
    
    // Initialize reports page functionality
    initReportsPage();
    
    // Initialize dashboard charts
    initDashboardCharts();
});

/**
 * Initialize users table functionality (filtering, sorting, etc.)
 */
function initUsersTable() {
    const usersTable = document.getElementById('users-table');
    if (!usersTable) return;
    
    // Search functionality
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', filterUsers);
    }
    
    // Role filter functionality
    const roleFilter = document.getElementById('roleFilter');
    if (roleFilter) {
        roleFilter.addEventListener('change', filterUsers);
    }
    
    // Delete confirmation
    const deleteButtons = document.querySelectorAll('[data-delete-user]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const userId = this.getAttribute('data-delete-user');
            const userName = this.getAttribute('data-user-name');
            
            if (!confirm(`¿Estás seguro de que deseas eliminar al usuario "${userName}"? Esta acción no se puede deshacer.`)) {
                event.preventDefault();
            }
        });
    });
    
    // Pagination functionality
    const prevPageBtn = document.getElementById('prevPage');
    const nextPageBtn = document.getElementById('nextPage');
    
    if (prevPageBtn && nextPageBtn) {
        prevPageBtn.addEventListener('click', function() {
            const currentPage = parseInt(document.getElementById('currentPage').textContent);
            if (currentPage > 1) {
                changePage(currentPage - 1);
            }
        });
        
        nextPageBtn.addEventListener('click', function() {
            const currentPage = parseInt(document.getElementById('currentPage').textContent);
            const totalPages = parseInt(document.getElementById('totalPages').textContent);
            
            if (currentPage < totalPages) {
                changePage(currentPage + 1);
            }
        });
    }
    
    // Update user count on load
    updateUserCount();
}

/**
 * Filter users based on search input and role filter
 */
function filterUsers() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const roleFilter = document.getElementById('roleFilter').value;
    const tableRows = document.querySelectorAll('#users-table tbody tr');
    
    let visibleCount = 0;
    
    tableRows.forEach(row => {
        // Get user data from row
        const username = row.querySelector('td:nth-child(4)').textContent.toLowerCase();
        const name = row.querySelector('td:nth-child(2)').textContent.toLowerCase() + ' ' + 
                    row.querySelector('td:nth-child(3)').textContent.toLowerCase();
        const email = row.querySelector('td:nth-child(5)').textContent.toLowerCase();
        const role = row.querySelector('td:nth-child(6)').textContent.trim().toLowerCase();
        
        // Check if matches search term and role filter
        const matchesSearch = username.includes(searchTerm) || 
                             name.includes(searchTerm) || 
                             email.includes(searchTerm);
        
        const matchesRole = roleFilter === 'all' || 
                          (roleFilter === 'admin' && role.includes('admin')) || 
                          (roleFilter === 'teacher' && role.includes('profesor')) || 
                          (roleFilter === 'student' && role.includes('estudiante'));
        
        // Show/hide row based on filters
        if (matchesSearch && matchesRole) {
            row.style.display = '';
            visibleCount++;
        } else {
            row.style.display = 'none';
        }
    });
    
    // Update user count
    const userCount = document.getElementById('userCount');
    if (userCount) {
        userCount.textContent = visibleCount;
    }
    
    // Update pagination buttons
    updatePagination(visibleCount);
}

/**
 * Update user count
 */
function updateUserCount() {
    const tableRows = document.querySelectorAll('#users-table tbody tr');
    const visibleRows = Array.from(tableRows).filter(row => row.style.display !== 'none');
    
    const userCount = document.getElementById('userCount');
    if (userCount) {
        userCount.textContent = visibleRows.length;
    }
}

/**
 * Change page in pagination
 * @param {number} pageNumber - The page number to change to
 */
function changePage(pageNumber) {
    // Update current page display
    document.getElementById('currentPage').textContent = pageNumber;
    
    // Get visible rows
    const tableRows = document.querySelectorAll('#users-table tbody tr');
    const visibleRows = Array.from(tableRows).filter(row => row.style.display !== 'none');
    
    // Items per page
    const itemsPerPage = 10;
    
    // Calculate start and end index
    const startIndex = (pageNumber - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    
    // Show/hide rows based on pagination
    visibleRows.forEach((row, index) => {
        if (index >= startIndex && index < endIndex) {
            row.classList.remove('hidden');
        } else {
            row.classList.add('hidden');
        }
    });
    
    // Update pagination buttons
    updatePaginationButtons(pageNumber, Math.ceil(visibleRows.length / itemsPerPage));
}

/**
 * Update pagination based on visible rows count
 * @param {number} visibleCount - The number of visible rows
 */
function updatePagination(visibleCount) {
    const itemsPerPage = 10;
    const totalPages = Math.ceil(visibleCount / itemsPerPage);
    
    // Update total pages display
    document.getElementById('totalPages').textContent = totalPages;
    
    // Reset to first page when filtering
    document.getElementById('currentPage').textContent = 1;
    
    // Update pagination buttons
    updatePaginationButtons(1, totalPages);
}

/**
 * Update pagination buttons state
 * @param {number} currentPage - The current page number
 * @param {number} totalPages - The total number of pages
 */
function updatePaginationButtons(currentPage, totalPages) {
    const prevPageBtn = document.getElementById('prevPage');
    const nextPageBtn = document.getElementById('nextPage');
    
    // Disable/enable previous page button
    if (currentPage <= 1) {
        prevPageBtn.disabled = true;
        prevPageBtn.classList.add('opacity-50', 'cursor-not-allowed');
    } else {
        prevPageBtn.disabled = false;
        prevPageBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    }
    
    // Disable/enable next page button
    if (currentPage >= totalPages) {
        nextPageBtn.disabled = true;
        nextPageBtn.classList.add('opacity-50', 'cursor-not-allowed');
    } else {
        nextPageBtn.disabled = false;
        nextPageBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    }
}

/**
 * Initialize user form validation
 */
function initUserForm() {
    const userForm = document.getElementById('userForm');
    if (!userForm) return;
    
    userForm.addEventListener('submit', function(event) {
        // Prevent default form submission
        event.preventDefault();
        
        // Get form inputs
        const username = document.getElementById('username');
        const email = document.getElementById('email');
        const firstName = document.getElementById('first_name');
        const lastName = document.getElementById('last_name');
        const role = document.getElementById('role');
        
        // Reset previous error messages
        clearFormErrors();
        
        // Validate form
        let isValid = true;
        
        if (!username.value.trim()) {
            showFormError('username', 'El nombre de usuario es requerido');
            isValid = false;
        } else if (username.value.trim().length < 3) {
            showFormError('username', 'El nombre de usuario debe tener al menos 3 caracteres');
            isValid = false;
        }
        
        if (!email.value.trim()) {
            showFormError('email', 'El correo electrónico es requerido');
            isValid = false;
        } else if (!isValidEmail(email.value.trim())) {
            showFormError('email', 'Ingrese un correo electrónico válido');
            isValid = false;
        }
        
        if (!firstName.value.trim()) {
            showFormError('first_name', 'El nombre es requerido');
            isValid = false;
        }
        
        if (!lastName.value.trim()) {
            showFormError('last_name', 'El apellido es requerido');
            isValid = false;
        }
        
        if (!role.value) {
            showFormError('role', 'Seleccione un rol');
            isValid = false;
        }
        
        // If form is valid, submit it
        if (isValid) {
            userForm.submit();
        }
    });
}

/**
 * Show error message for a form field
 * @param {string} fieldId - The ID of the field
 * @param {string} message - The error message
 */
function showFormError(fieldId, message) {
    const field = document.getElementById(fieldId);
    const errorElement = document.getElementById(`${fieldId}Error`);
    
    // Add error class to field
    field.classList.add('border-red-500');
    
    // Display error message
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.classList.remove('hidden');
    }
}

/**
 * Clear all error messages in the form
 */
function clearFormErrors() {
    // Remove error class from all inputs
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.classList.remove('border-red-500');
    });
    
    // Hide all error messages
    const errorMessages = document.querySelectorAll('[id$="Error"]');
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
 * Initialize reports page functionality
 */
function initReportsPage() {
    const reportsPage = document.getElementById('reports-container');
    if (!reportsPage) return;
    
    // Initialize filter functionality
    initReportFilters();
    
    // Initialize export functionality
    initReportExport();
    
    // Initialize refresh button
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            window.location.reload();
        });
    }
    
    // Initialize report type selector
    const reportType = document.getElementById('reportType');
    if (reportType) {
        reportType.addEventListener('change', function() {
            // In a full implementation, this would call an API to load different report data
            // For now, just show a notification
            showNotification('Cambiando al reporte: ' + reportType.options[reportType.selectedIndex].text, 'info');
        });
    }
}

/**
 * Initialize report filters
 */
function initReportFilters() {
    const searchInput = document.getElementById('searchInput');
    const dateFrom = document.getElementById('dateFrom');
    const dateTo = document.getElementById('dateTo');
    const actionFilter = document.getElementById('actionFilter');
    const resetFilters = document.getElementById('resetFilters');
    
    // If any of these filters exists, initialize them
    if (searchInput || dateFrom || dateTo || actionFilter) {
        // Function to apply filters (would be connected to an API in a real implementation)
        const applyFilters = () => {
            // In a real implementation, this would make an API call
            // For now, just show a notification with the filter values
            const filters = {
                search: searchInput ? searchInput.value : '',
                dateFrom: dateFrom ? dateFrom.value : '',
                dateTo: dateTo ? dateTo.value : '',
                action: actionFilter ? actionFilter.value : ''
            };
            
            console.log('Applying filters:', filters);
            showNotification('Filtros aplicados', 'success');
        };
        
        // Add event listeners
        if (searchInput) {
            searchInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    applyFilters();
                }
            });
        }
        
        if (dateFrom) dateFrom.addEventListener('change', applyFilters);
        if (dateTo) dateTo.addEventListener('change', applyFilters);
        if (actionFilter) actionFilter.addEventListener('change', applyFilters);
        
        // Reset filters button
        if (resetFilters) {
            resetFilters.addEventListener('click', function() {
                if (searchInput) searchInput.value = '';
                if (dateFrom) dateFrom.value = '';
                if (dateTo) dateTo.value = '';
                if (actionFilter) actionFilter.value = '';
                
                applyFilters();
            });
        }
    }
}

/**
 * Initialize report export functionality
 */
function initReportExport() {
    const exportDropdownBtn = document.getElementById('exportDropdownBtn');
    const exportDropdown = document.getElementById('exportDropdown');
    const exportPdfBtn = document.getElementById('exportPdfBtn');
    const exportCsvBtn = document.getElementById('exportCsvBtn');
    
    // Toggle export dropdown
    if (exportDropdownBtn && exportDropdown) {
        exportDropdownBtn.addEventListener('click', function() {
            exportDropdown.classList.toggle('hidden');
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(event) {
            if (!exportDropdownBtn.contains(event.target) && !exportDropdown.contains(event.target)) {
                exportDropdown.classList.add('hidden');
            }
        });
    }
    
    // Export to PDF
    if (exportPdfBtn) {
        exportPdfBtn.addEventListener('click', function() {
            // This would be connected to a PDF generation library in a real implementation
            showNotification('Exportando a PDF...', 'info');
            
            // Simulate PDF generation delay
            setTimeout(() => {
                showNotification('El informe ha sido exportado a PDF correctamente', 'success');
            }, 1500);
        });
    }
    
    // Export to CSV
    if (exportCsvBtn) {
        exportCsvBtn.addEventListener('click', function() {
            // This would be connected to a CSV generation library in a real implementation
            showNotification('Exportando a CSV...', 'info');
            
            // Simulate CSV generation delay
            setTimeout(() => {
                showNotification('El informe ha sido exportado a CSV correctamente', 'success');
            }, 1000);
        });
    }
}

/**
 * Initialize dashboard charts
 */
function initDashboardCharts() {
    const userDistributionChart = document.getElementById('userDistributionChart');
    if (!userDistributionChart) return;
    
    // Get chart data from data attributes
    const adminCount = parseInt(userDistributionChart.getAttribute('data-admin-count') || 0);
    const teacherCount = parseInt(userDistributionChart.getAttribute('data-teacher-count') || 0);
    const studentCount = parseInt(userDistributionChart.getAttribute('data-student-count') || 0);
    
    // Create user distribution chart
    new Chart(userDistributionChart.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: ['Administradores', 'Profesores', 'Estudiantes'],
            datasets: [{
                data: [adminCount, teacherCount, studentCount],
                backgroundColor: [
                    'rgba(220, 38, 38, 0.7)',  // Red for admins
                    'rgba(59, 130, 246, 0.7)', // Blue for teachers
                    'rgba(234, 179, 8, 0.7)',  // Yellow for students
                ],
                borderColor: [
                    'rgba(220, 38, 38, 1)',
                    'rgba(59, 130, 246, 1)',
                    'rgba(234, 179, 8, 1)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        usePointStyle: true,
                        padding: 20,
                        font: {
                            size: 12
                        }
                    }
                }
            }
        }
    });
}
