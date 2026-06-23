// Sidebar toggle responsive (hamburger menu)
document.addEventListener('DOMContentLoaded', function () {
    var sidebar = document.getElementById('sidebar');
    var overlay = document.getElementById('sidebarOverlay');
    var hamburger = document.getElementById('hamburgerBtn');
    var closeBtn = document.getElementById('sidebarClose');

    if (sidebar && overlay && hamburger) {
        function openSidebar() {
            sidebar.classList.add('active');
            overlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function closeSidebar() {
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
            document.body.style.overflow = '';
        }

        hamburger.addEventListener('click', openSidebar);
        overlay.addEventListener('click', closeSidebar);
        if (closeBtn) closeBtn.addEventListener('click', closeSidebar);

        // Cerrar con tecla Escape
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && sidebar.classList.contains('active')) {
                closeSidebar();
            }
        });
    }
});

// Obtener token CSRF para fetch
function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
            return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : '';
}

// Headers por defecto para fetch
function getHeaders(extra = {}) {
    return {
        'X-Requested-With': 'XMLHttpRequest',
        ...extra
    };
}
