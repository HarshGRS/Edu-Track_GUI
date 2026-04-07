// Dashboard specific JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard
    initializeDashboard();
});

function initializeDashboard() {
    // Add event listeners for modal buttons
    setupModalListeners();

    // Initialize form validations
    setupFormValidations();

    // Add search functionality
    setupSearchFunctionality();
}

function setupModalListeners() {
    // Add student modal
    const addBtn = document.querySelector('[onclick="openAddModal()"]');
    if (addBtn) {
        addBtn.addEventListener('click', () => openModal('addModal'));
    }

    // Close modal buttons
    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', function() {
            const modalId = this.closest('.modal').id;
            closeModal(modalId);
        });
    });

    // Close modal on outside click
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal(this.id);
            }
        });
    });
}

function setupFormValidations() {
    // Add student form validation
    const addForm = document.querySelector('#addModal form');
    if (addForm) {
        addForm.addEventListener('submit', function(e) {
            if (!validateStudentForm(this)) {
                e.preventDefault();
                return false;
            }
        });
    }

    // Edit student form validation
    const editForm = document.querySelector('#editModal form');
    if (editForm) {
        editForm.addEventListener('submit', function(e) {
            if (!validateStudentForm(this)) {
                e.preventDefault();
                return false;
            }
        });
    }
}

function validateStudentForm(form) {
    const roll = form.querySelector('[name="roll"]');
    const name = form.querySelector('[name="name"]');
    const sub1 = form.querySelector('[name="sub1"]');
    const sub2 = form.querySelector('[name="sub2"]');
    const sub3 = form.querySelector('[name="sub3"]');

    // Clear previous errors
    clearFormErrors(form);

    let isValid = true;

    // Validate roll number
    if (!roll.value || roll.value < 1) {
        showFieldError(roll, 'Roll number must be a positive number');
        isValid = false;
    }

    // Validate name
    if (!name.value.trim()) {
        showFieldError(name, 'Name is required');
        isValid = false;
    } else if (name.value.trim().length < 2) {
        showFieldError(name, 'Name must be at least 2 characters');
        isValid = false;
    }

    // Validate marks
    [sub1, sub2, sub3].forEach((field, index) => {
        const value = parseInt(field.value);
        if (isNaN(value) || value < 0 || value > 100) {
            showFieldError(field, `Subject ${index + 1} marks must be between 0 and 100`);
            isValid = false;
        }
    });

    return isValid;
}

function showFieldError(field, message) {
    field.style.borderColor = '#ef4444';

    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    errorDiv.style.color = '#ef4444';
    errorDiv.style.fontSize = '0.8rem';
    errorDiv.style.marginTop = '5px';

    field.parentNode.appendChild(errorDiv);

    // Remove error styling on input
    field.addEventListener('input', function() {
        this.style.borderColor = '#3b82f6';
        const error = this.parentNode.querySelector('.field-error');
        if (error) error.remove();
    });
}

function clearFormErrors(form) {
    form.querySelectorAll('.field-error').forEach(error => error.remove());
    form.querySelectorAll('input').forEach(input => {
        input.style.borderColor = '#e2e8f0';
    });
}

function setupSearchFunctionality() {
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.placeholder = 'Search students...';
    searchInput.className = 'search-input';

    const tableHeader = document.querySelector('.table-header');
    if (tableHeader) {
        tableHeader.appendChild(searchInput);

        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = document.querySelectorAll('.data-table tbody tr');

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    }
}

// Modal functions (global scope for onclick handlers)
function openAddModal() {
    openModal('addModal');
}

function openEditModal(roll, name, sub1, sub2, sub3) {
    // Populate edit form
    document.getElementById('edit_roll').value = roll;
    document.getElementById('edit_name').value = name;
    document.getElementById('edit_sub1').value = sub1;
    document.getElementById('edit_sub2').value = sub2;
    document.getElementById('edit_sub3').value = sub3;

    // Set form action
    const editForm = document.getElementById('editForm');
    editForm.action = `/update_student/${roll}`;

    openModal('editModal');
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// Add search input styles
const searchStyle = document.createElement('style');
searchStyle.textContent = `
    .search-input {
        margin-left: auto;
        padding: 8px 12px;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        font-size: 0.9rem;
        width: 250px;
        transition: border-color 0.3s ease;
    }

    .search-input:focus {
        outline: none;
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }

    .table-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    @media (max-width: 768px) {
        .search-input {
            width: 150px;
            margin-left: 10px;
        }
    }
`;
document.head.appendChild(searchStyle);