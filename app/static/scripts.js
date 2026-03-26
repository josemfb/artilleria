document.addEventListener('DOMContentLoaded', () => {
    const accordionHeaders = document.querySelectorAll('.accordion-header');

    accordionHeaders.forEach(button => {
        button.addEventListener('click', () => {
            accordionHeaders.forEach(otherButton => {
                if (otherButton !== button) {
                    otherButton.classList.remove('active');
                    otherButton.nextElementSibling.style.maxHeight = null;
                }
            });
            button.classList.toggle('active');
            const content = button.nextElementSibling;
            if (button.classList.contains('active')) {
                content.style.maxHeight = content.scrollHeight + "px";
            } else {
                content.style.maxHeight = null;
            }
        });
    });

    // Disable accordion headers if all content links are placeholders
    document.querySelectorAll('.accordion-item').forEach(item => {
        const header = item.querySelector('.accordion-header');
        const content = item.querySelector('.accordion-content');
        
        if (header && content) {
            const links = Array.from(content.querySelectorAll('a'));
            const allPlaceholders = links.every(link => link.getAttribute('href') === '#');
            if (links.length > 0 && allPlaceholders) {
                header.classList.add('disabled');
            }
        }
    });

    // User Menu Toggle
    const userMenuBtn = document.querySelector('.user-menu-toggle');
    const userDropdown = document.querySelector('.user-dropdown');

    if (userMenuBtn && userDropdown) {
        userMenuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            userDropdown.classList.toggle('show');
        });

        document.addEventListener('click', (e) => {
            if (!userMenuBtn.contains(e.target)) {
                userDropdown.classList.remove('show');
            }
        });
    }

    // Sidebar Toggle for Mobile
    const toggle = document.getElementById('navbar-brand-toggle');
    const sidebar = document.querySelector('.sidebar');
    if (toggle && sidebar) {
        toggle.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                sidebar.classList.toggle('show');
            }
        });
    }

    // Disable default action for placeholder links in sidebar
    document.querySelectorAll('.sidebar a[href="#"]').forEach(link => {
        link.addEventListener('click', (e) => e.preventDefault());
    });
});

// Tab switching function for volunteer details
function showTab(tabId) {
    // Hide all tab panes
    const tabPanes = document.querySelectorAll('.tab-pane');
    tabPanes.forEach(pane => {
        pane.classList.remove('active');
    });
    
    // Remove active class from all tab buttons
    const tabButtons = document.querySelectorAll('.service-tab');
    tabButtons.forEach(button => {
        button.classList.remove('active');
    });
    
    // Show the selected tab pane
    const selectedPane = document.getElementById(tabId);
    if (selectedPane) {
        selectedPane.classList.add('active');
    }
    
    // Add active class to the clicked tab button
    const clickedButton = document.querySelector(`[onclick="showTab('${tabId}')"]`);
    if (clickedButton) {
        clickedButton.classList.add('active');
    }
}

// Inline editing functions for volunteer personal data
function enablePersonalDataEdit() {
    // Hide display mode, show edit mode
    document.getElementById('personal-data-display').classList.add('hidden');
    document.getElementById('personal-data-edit').classList.remove('hidden');
    
    // Update tab actions to show save/cancel buttons
    const tabActions = document.getElementById('datos-tab-actions');
    tabActions.innerHTML = `
        <button type="submit" form="inline-edit-form" class="btn btn-success">Guardar cambios</button>
        <button class="btn btn-secondary" onclick="cancelPersonalDataEdit()">Cancelar</button>
    `;
    
    // Pre-populate form fields with current values from data attributes
    const form = document.getElementById('inline-edit-form');
    if (form) {
        const data = form.dataset;
        if (data.fechaNacimiento) document.getElementById('fecha_nacimiento').value = data.fechaNacimiento;
        if (data.ocupacion) document.getElementById('ocupacion').value = data.ocupacion;
        if (data.telefono) document.getElementById('telefono').value = data.telefono;
        if (data.email) document.getElementById('email').value = data.email;
        if (data.direccion) document.getElementById('direccion').value = data.direccion;
        if (data.fechaAlta) document.getElementById('fecha_alta').value = data.fechaAlta;
    }
}

function cancelPersonalDataEdit() {
    // Show display mode, hide edit mode
    document.getElementById('personal-data-display').classList.remove('hidden');
    document.getElementById('personal-data-edit').classList.add('hidden');
    
    // Restore original tab actions
    const tabActions = document.getElementById('datos-tab-actions');
    tabActions.innerHTML = `
        <button class="btn btn-primary" id="edit-personal-data-btn" onclick="enablePersonalDataEdit()">Editar datos personales</button>
        <button class="btn btn-primary" disabled>Editar altas anteriores</button>
    `;
}