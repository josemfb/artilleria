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