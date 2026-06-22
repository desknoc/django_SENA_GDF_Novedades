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
