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
    `;
}

// Alta Anterior management functions
function showAddAltaAnteriorForm() {
    const container = document.getElementById('alta-anterior-form-container');
    const content = document.getElementById('alta-anterior-form-content');
    const title = document.getElementById('alta-anterior-form-title');
    const tabActions = document.getElementById('datos-tab-actions');
    
    // Update title
    title.textContent = 'Añadir Alta Anterior';
    
    // Hide the tab actions buttons immediately
    if (tabActions) {
        tabActions.classList.add('hidden');
    }
    
    // Show the form container
    container.classList.remove('hidden');
    
    // Load the add form via HTMX
    const userId = window.location.pathname.split('/').pop();
    content.innerHTML = '<div class="text-center p-4"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';
    
    // Use fetch to load the form
    fetch(`/voluntarios/${userId}/altas-anteriores/add?htmx=1`)
        .then(response => response.text())
        .then(html => {
            // The response is now just the form HTML
            content.innerHTML = html;
        })
        .catch(error => {
            console.error('Error loading form:', error);
            content.innerHTML = '<div class="alert alert-danger">Error al cargar el formulario</div>';
        });
}

function editAltaAnterior(altaId) {
    const container = document.getElementById('alta-anterior-form-container');
    const content = document.getElementById('alta-anterior-form-content');
    const title = document.getElementById('alta-anterior-form-title');
    const tabActions = document.getElementById('datos-tab-actions');
    
    // Update title
    title.textContent = 'Editar Alta Anterior';
    
    // Hide the tab actions buttons immediately
    if (tabActions) {
        tabActions.classList.add('hidden');
    }
    
    // Show the form container
    container.classList.remove('hidden');
    
    // Load the edit form via HTMX
    content.innerHTML = '<div class="text-center p-4"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';
    
    // Use fetch to load the form
    fetch(`/voluntarios/altas-anteriores/edit/${altaId}?htmx=1`)
        .then(response => response.text())
        .then(html => {
            // The response is now just the form HTML
            content.innerHTML = html;
        })
        .catch(error => {
            console.error('Error loading form:', error);
            content.innerHTML = '<div class="alert alert-danger">Error al cargar el formulario</div>';
        });
}

function hideAltaAnteriorForm() {
    const container = document.getElementById('alta-anterior-form-container');
    const tabActions = document.getElementById('datos-tab-actions');
    
    // Hide the form container
    container.classList.add('hidden');
    
    // Show the tab actions buttons again
    if (tabActions) {
        tabActions.classList.remove('hidden');
    }
}

function deleteAltaAnterior(altaId) {
    if (confirm('¿Está seguro de eliminar esta alta anterior?')) {
        // Create a form element to submit via HTMX
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/voluntarios/altas-anteriores/delete/${altaId}`;
        form.setAttribute('hx-post', `/voluntarios/altas-anteriores/delete/${altaId}`);
        form.setAttribute('hx-target', '#datos-tab');
        form.setAttribute('hx-swap', 'innerHTML');
        
        // Add CSRF token if needed (assuming you're using Flask-WTF)
        const csrfToken = document.querySelector('input[name="csrf_token"]');
        if (csrfToken) {
            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrf_token';
            csrfInput.value = csrfToken.value;
            form.appendChild(csrfInput);
        }
        
        // Submit the form using HTMX
        document.body.appendChild(form);
        htmx.process(form);
        form.submit();
        
        // Clean up
        document.body.removeChild(form);
    }
}

// Inline editing functions for altas anteriores
function enableInlineEdit(altaId) {
    // Hide display values and show edit inputs
    const displayElements = document.querySelectorAll(`#alta-row-${altaId} .display-value`);
    const editElements = document.querySelectorAll(`#alta-row-${altaId} .edit-value`);
    
    displayElements.forEach(el => el.style.display = 'none');
    editElements.forEach(el => el.style.display = 'block');
    
    // Hide edit button and show save/cancel buttons
    document.getElementById(`edit-btn-${altaId}`).style.display = 'none';
    document.getElementById(`save-btn-${altaId}`).style.display = 'flex';
    document.getElementById(`cancel-btn-${altaId}`).style.display = 'flex';
    
    // Disable delete button during editing
    document.querySelector(`#alta-row-${altaId} .btn-outline-danger`).disabled = true;
}

function cancelInlineEdit(altaId) {
    // Hide edit inputs and show display values
    const displayElements = document.querySelectorAll(`#alta-row-${altaId} .display-value`);
    const editElements = document.querySelectorAll(`#alta-row-${altaId} .edit-value`);
    
    displayElements.forEach(el => el.style.display = 'block');
    editElements.forEach(el => el.style.display = 'none');
    
    // Show edit button and hide save/cancel buttons
    document.getElementById(`edit-btn-${altaId}`).style.display = 'block';
    document.getElementById(`save-btn-${altaId}`).style.display = 'none';
    document.getElementById(`cancel-btn-${altaId}`).style.display = 'none';
    
    // Enable delete button
    document.querySelector(`#alta-row-${altaId} .btn-outline-danger`).disabled = false;
}

function saveInlineEdit(altaId) {
    // Get the form data
    const data = {
        fecha_alta: document.getElementById(`edit-fecha_alta-${altaId}`).value,
        registro_general: document.getElementById(`edit-registro_general-${altaId}`).value,
        registro_quinta: document.getElementById(`edit-registro_quinta-${altaId}`).value,
        fecha_baja: document.getElementById(`edit-fecha_baja-${altaId}`).value,
        motivo_baja: document.getElementById(`edit-motivo_baja-${altaId}`).value
    };
    
    // Create and submit form via HTMX
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/voluntarios/altas-anteriores/edit/${altaId}`;
    form.setAttribute('hx-post', `/voluntarios/altas-anteriores/edit/${altaId}`);
    form.setAttribute('hx-target', '#datos-tab');
    form.setAttribute('hx-swap', 'innerHTML');
    
    // Add form fields
    Object.keys(data).forEach(key => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = key;
        input.value = data[key];
        form.appendChild(input);
    });
    
    // Add CSRF token if needed
    const csrfToken = document.querySelector('input[name="csrf_token"]');
    if (csrfToken) {
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrf_token';
        csrfInput.value = csrfToken.value;
        form.appendChild(csrfInput);
    }
    
    // Submit the form using HTMX
    document.body.appendChild(form);
    htmx.process(form);
    form.submit();
    
    // Clean up
    document.body.removeChild(form);
}