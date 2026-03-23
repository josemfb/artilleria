document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.accordion-header').forEach(button => {
        button.addEventListener('click', () => {
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
});