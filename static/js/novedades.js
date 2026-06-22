// ========== CONSTANTES ==========
const BASE_URL = '/novedades';

// ========== FUNCIONES AUXILIARES ==========
function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
            return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }
    return '';
}

function formatearFecha(fechaStr) {
    if (!fechaStr) return '';
    const fecha = new Date(fechaStr);
    if (isNaN(fecha.getTime())) return fechaStr;
    return fecha.toLocaleDateString('es-CO', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// ========== HOME: CARGAR NOVEDADES PÚBLICAS ==========
async function cargarNovedadesPublicas() {
    const container = document.getElementById('novedades-container');
    if (!container) return;

    try {
        const response = await fetch(`${BASE_URL}/`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const novedades = await response.json();

        document.getElementById('loading-spinner')?.remove();

        if (!novedades || novedades.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">
                        <ion-icon name="newspaper-outline"></ion-icon>
                    </div>
                    <h5 class="text-muted">No hay novedades publicadas aún</h5>
                </div>
            `;
            return;
        }

        let html = '<div style="display: flex; flex-wrap: wrap; gap: 1.5rem;">';
        for (const novedad of novedades) {
            const fecha = formatearFecha(novedad.fecha_publicacion || novedad.ultima_actualizacion);
            html += `
                <div style="flex: 0 0 calc(50% - 0.75rem); max-width: calc(50% - 0.75rem); box-sizing: border-box;">
                    <div class="card shadow-sm border-0 h-100">
                        <div class="card-header header-gradient d-flex justify-content-between align-items-center">
                            <h5 class="mb-0 text-truncate" style="color: white;">${escapeHtml(novedad.titulo)}</h5>
                            <span class="badge badge-categoria flex-shrink-0 ms-2">${escapeHtml(novedad.categoria)}</span>
                        </div>
                        ${novedad.imagen_url ? `
                            <div style="width: 100%; height: 200px; overflow: hidden; background: #e9ecef; display: flex; align-items: center; justify-content: center;">
                                <img src="data:image/jpeg;base64,${novedad.imagen_url}" alt="${escapeHtml(novedad.titulo)}"
                                     style="width: 100%; height: 100%; object-fit: cover;">
                            </div>
                        ` : `
                            <div style="width: 100%; height: 200px; background: #e9ecef; display: flex; align-items: center; justify-content: center; color: #6c757d; font-size: 3rem;">
                                <ion-icon name="newspaper-outline"></ion-icon>
                            </div>
                        `}
                        <div class="card-body d-flex flex-column">
                            <p class="text-muted flex-grow-1" style="margin-bottom: 1rem;">
                                ${escapeHtml(truncarTexto(novedad.contenido, 250))}
                            </p>
                            <div class="d-flex justify-content-between align-items-center">
                                <small class="text-muted">
                                    <ion-icon name="calendar-outline" style="vertical-align: middle; margin-right: 4px;"></ion-icon>
                                    ${fecha}
                                </small>
                                <a href="/novedades/detalle/${novedad.id}/" class="btn btn-outline-success btn-sm">
                                    <ion-icon name="eye-outline"></ion-icon> Ver más
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
        html += '</div>';
        container.innerHTML = html;

    } catch (error) {
        console.error('Error al cargar novedades:', error);
        document.getElementById('loading-spinner')?.remove();
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">
                    <ion-icon name="alert-circle-outline" style="color: #dc3545;"></ion-icon>
                </div>
                <h5 class="text-muted">Error al cargar las novedades</h5>
                <button class="btn btn-success mt-3" onclick="cargarNovedadesPublicas()">
                    <ion-icon name="refresh-outline"></ion-icon> Intentar de nuevo
                </button>
            </div>
        `;
    }
}

// ========== DETALLE ==========
async function cargarDetalleNovedad(id) {
    try {
        const response = await fetch(`${BASE_URL}/detallenovedad/${id}/`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });

        if (!response.ok) {
            window.location.href = '/404/';
            return;
        }

        const data = await response.json();

        document.getElementById('detalle-loading').style.display = 'none';
        document.getElementById('detalle-content').style.display = 'block';

        document.getElementById('detalle-titulo').textContent = data.titulo || '';
        document.getElementById('detalle-categoria').textContent = data.categoria || '';
        document.getElementById('detalle-contenido').textContent = data.contenido || '';
        document.getElementById('detalle-fecha').textContent = formatearFecha(data.ultima_actualizacion || data.fecha_publicacion);

        if (data.imagen_url) {
            const imgContainer = document.getElementById('detalle-imagen-container');
            const img = document.getElementById('detalle-imagen');
            img.src = `data:image/jpeg;base64,${data.imagen_url}`;
            imgContainer.style.display = 'block';
        }

        if (data.url_referencia) {
            const urlEl = document.getElementById('detalle-url');
            urlEl.href = data.url_referencia;
            urlEl.style.display = 'inline-flex';
        }

    } catch (error) {
        console.error('Error al cargar detalle:', error);
        document.getElementById('detalle-loading').innerHTML = `
            <div class="empty-state">
                <h5 class="text-muted">Error al cargar la novedad</h5>
                <button class="btn btn-success mt-3" onclick="location.reload()">
                    <ion-icon name="refresh-outline"></ion-icon> Reintentar
                </button>
            </div>
        `;
    }
}

// ========== ADMIN: LISTA NOVEDADES ==========
let novedadesCache = [];

async function cargarNovedadesAdmin() {
    const container = document.getElementById('admin-novedades-container');
    if (!container) return;

    try {
        const response = await fetch(`${BASE_URL}/`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        novedadesCache = await response.json();

        document.getElementById('admin-loading')?.remove();

        if (!novedadesCache || novedadesCache.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">
                        <ion-icon name="newspaper-outline"></ion-icon>
                    </div>
                    <h5 class="text-muted">No hay novedades publicadas aún</h5>
                    <a href="/novedades/admin/crear/" class="btn btn-success mt-3">
                        <ion-icon name="add-circle-outline"></ion-icon> Crear la primera publicación
                    </a>
                </div>
            `;
            return;
        }

        let html = '<div style="display: flex; flex-wrap: wrap; gap: 1.5rem;">';
        for (const novedad of novedadesCache) {
            const fecha = formatearFecha(novedad.fecha_publicacion || novedad.ultima_actualizacion);
            html += `
                <div style="flex: 0 0 calc(50% - 0.75rem); max-width: calc(50% - 0.75rem); box-sizing: border-box;">
                    <div class="card shadow-sm border-0 h-100">
                        <div class="card-header header-gradient d-flex justify-content-between align-items-center">
                            <h5 class="mb-0 text-truncate" style="color: white;">${escapeHtml(novedad.titulo)}</h5>
                            <span class="badge badge-categoria flex-shrink-0 ms-2">${escapeHtml(novedad.categoria)}</span>
                        </div>
                        ${novedad.imagen_url ? `
                            <div style="width: 100%; height: 200px; overflow: hidden; background: #e9ecef;">
                                <img src="data:image/jpeg;base64,${novedad.imagen_url}" alt="${escapeHtml(novedad.titulo)}"
                                     style="width: 100%; height: 100%; object-fit: cover;">
                            </div>
                        ` : `
                            <div style="width: 100%; height: 200px; background: #e9ecef; display: flex; align-items: center; justify-content: center; color: #6c757d; font-size: 3rem;">
                                <ion-icon name="newspaper-outline"></ion-icon>
                            </div>
                        `}
                        <div class="card-body d-flex flex-column">
                            <p class="text-muted flex-grow-1" style="margin-bottom: 1rem;">
                                ${escapeHtml(truncarTexto(novedad.contenido, 250))}
                            </p>
                            <div class="d-flex align-items-center text-muted mb-3">
                                <ion-icon name="calendar-outline" style="margin-right: 8px; color: #28a745;"></ion-icon>
                                <small>${fecha}</small>
                            </div>
                            <div style="display: flex; gap: 0.5rem;">
                                <button class="btn btn-outline-success btn-sm" style="flex: 1;" onclick="abrirModalEditar(${novedad.id})">
                                    <ion-icon name="create-outline"></ion-icon> Modificar
                                </button>
                                <button class="btn btn-outline-danger btn-sm" style="flex: 1;" onclick="confirmarEliminar(${novedad.id})">
                                    <ion-icon name="trash-outline"></ion-icon> Borrar
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
        html += '</div>';
        container.innerHTML = html;

    } catch (error) {
        console.error('Error:', error);
        document.getElementById('admin-loading')?.remove();
        container.innerHTML = `
            <div class="empty-state">
                <h5 class="text-muted">Error al cargar las novedades</h5>
                <button class="btn btn-success mt-3" onclick="cargarNovedadesAdmin()">
                    <ion-icon name="refresh-outline"></ion-icon> Reintentar
                </button>
            </div>
        `;
    }
}

// ========== ADMIN: ELIMINAR ==========
async function confirmarEliminar(id) {
    const novedad = novedadesCache.find(n => n.id === id);
    if (!novedad) return;

    const result = await Swal.fire({
        title: '¿Eliminar novedad?',
        html: `
            <p><strong>${escapeHtml(novedad.titulo)}</strong></p>
            <p style="font-size:0.9rem;color:#666;">${escapeHtml(truncarTexto(novedad.contenido, 150))}</p>
            <p style="font-size:1.1rem;color:#dc3545;"><strong>¡ESTA ACCIÓN NO PUEDE REVERTIRSE!</strong></p>
        `,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    });

    if (!result.isConfirmed) return;

    try {
        const formData = new FormData();
        formData.append('csrfmiddlewaretoken', getCSRFToken());

        const response = await fetch(`${BASE_URL}/eliminarnovedad/${id}/`, {
            method: 'POST',
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });

        const text = await response.text();
        const data = JSON.parse(text);

        if (data.mensaje || text.includes('eliminada')) {
            await Swal.fire({
                icon: 'success',
                title: 'Eliminada',
                text: 'La novedad se eliminó correctamente.',
                confirmButtonColor: '#28a745'
            });
            cargarNovedadesAdmin();
        } else {
            throw new Error(data.error || 'Error al eliminar');
        }
    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'No se pudo eliminar la novedad.',
            confirmButtonColor: '#28a745'
        });
    }
}

// ========== MODAL DE EDICIÓN ==========
function abrirModalEditar(id) {
    const novedad = novedadesCache.find(n => n.id === id);
    if (!novedad) return;

    document.getElementById('edit-id').value = novedad.id;
    document.getElementById('edit-titulo').value = novedad.titulo || '';
    document.getElementById('edit-contenido').value = novedad.contenido || '';
    document.getElementById('edit-categoria').value = novedad.categoria || '';
    document.getElementById('edit-url').value = novedad.url_referencia || '';

    const previewContainer = document.getElementById('edit-imagen-preview');
    const previewImg = document.getElementById('edit-img-preview');
    if (novedad.imagen_url) {
        previewImg.src = `data:image/jpeg;base64,${novedad.imagen_url}`;
        previewContainer.style.display = 'block';
    } else {
        previewContainer.style.display = 'none';
    }

    document.getElementById('modal-editar').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function cerrarModal() {
    document.getElementById('modal-editar').style.display = 'none';
    document.body.style.overflow = '';
}

function quitarImagenEditar() {
    document.getElementById('edit-imagen').value = '';
    document.getElementById('edit-imagen-preview').style.display = 'none';
    document.getElementById('edit-img-preview').src = '';
}

// Cerrar modal con Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') cerrarModal();
});

// Submit del modal de edición
document.getElementById('formEditar')?.addEventListener('submit', async function(e) {
    e.preventDefault();

    const id = document.getElementById('edit-id').value;
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', getCSRFToken());
    formData.append('titulo', document.getElementById('edit-titulo').value);
    formData.append('contenido', document.getElementById('edit-contenido').value);
    formData.append('categoria', document.getElementById('edit-categoria').value);
    formData.append('url_referencia', document.getElementById('edit-url').value);

    const imagenFile = document.getElementById('edit-imagen').files[0];
    if (imagenFile) {
        formData.append('imagen', imagenFile);
    }

    try {
        const response = await fetch(`${BASE_URL}/editar/${id}/`, {
            method: 'POST',
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });

        const text = await response.text();
        const data = JSON.parse(text);

        if (data.mensaje || text.includes('actualizada')) {
            await Swal.fire({
                icon: 'success',
                title: '¡Actualizada!',
                text: 'La novedad se actualizó correctamente.',
                confirmButtonColor: '#28a745'
            });
            cerrarModal();
            cargarNovedadesAdmin();
        } else {
            throw new Error(data.error || 'Error al actualizar');
        }
    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: error.message || 'No se pudo actualizar la novedad.',
            confirmButtonColor: '#28a745'
        });
    }
});

// ========== ADMIN: FORMULARIO CREAR/EDITAR ==========
function initFormNovedad() {
    const form = document.getElementById('formNovedad');
    if (!form) return;

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const btnSubmit = document.getElementById('btn-submit');
        const btnText = document.getElementById('btn-text');
        btnSubmit.disabled = true;
        btnText.textContent = 'Guardando...';

        const novedadId = document.getElementById('novedad-id')?.value;
        const formData = new FormData(this);

        try {
            let url, method;
            if (novedadId) {
                url = `${BASE_URL}/editar/${novedadId}/`;
            } else {
                url = `${BASE_URL}/crearnovedad/`;
            }

            const response = await fetch(url, {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });

            const text = await response.text();
            let data;
            try { data = JSON.parse(text); } catch { data = {}; }

            if (data.mensaje || text.includes('exitosamente') || text.includes('correctamente')) {
                await Swal.fire({
                    icon: 'success',
                    title: novedadId ? '¡Actualizada!' : '¡Publicada!',
                    text: `La novedad se ${novedadId ? 'actualizó' : 'creó'} correctamente.`,
                    confirmButtonColor: '#28a745'
                });
                window.location.href = '/novedades/admin/';
            } else {
                throw new Error(data.error || text || 'Error al guardar');
            }
        } catch (error) {
            console.error('Error:', error);
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: error.message || 'No se pudo guardar la novedad.',
                confirmButtonColor: '#28a745'
            });
        } finally {
            btnSubmit.disabled = false;
            btnText.textContent = novedadId ? 'Actualizar' : 'Publicar';
        }
    });
}

async function cargarFormEditar(id) {
    try {
        const response = await fetch(`${BASE_URL}/detallenovedad/${id}/`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const data = await response.json();

        document.getElementById('titulo').value = data.titulo || '';
        document.getElementById('contenido').value = data.contenido || '';
        document.getElementById('categoria').value = data.categoria || '';
        document.getElementById('url_referencia').value = data.url_referencia || '';

        if (data.imagen_url) {
            const previewContainer = document.getElementById('imagen-preview-container');
            const preview = document.getElementById('imagen-preview');
            preview.src = `data:image/jpeg;base64,${data.imagen_url}`;
            previewContainer.style.display = 'inline-block';
        }

        document.getElementById('btn-text').textContent = 'Actualizar';

    } catch (error) {
        console.error('Error al cargar datos para editar:', error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'No se pudo cargar la novedad para editar.',
            confirmButtonColor: '#28a745'
        });
    }
}

function quitarImagen() {
    document.getElementById('imagen').value = '';
    document.getElementById('imagen-preview-container').style.display = 'none';
}

// Preview de imagen al seleccionar archivo
document.addEventListener('change', function(e) {
    if (e.target.id === 'imagen' || e.target.id === 'edit-imagen') {
        const file = e.target.files[0];
        if (!file) return;

        if (file.size > 5 * 1024 * 1024) {
            Swal.fire({
                icon: 'error',
                title: 'Imagen muy grande',
                text: 'La imagen no puede superar los 5MB.',
                confirmButtonColor: '#28a745'
            });
            e.target.value = '';
            return;
        }

        if (!file.type.startsWith('image/')) {
            Swal.fire({
                icon: 'error',
                title: 'Formato inválido',
                text: 'Solo se permiten imágenes.',
                confirmButtonColor: '#28a745'
            });
            e.target.value = '';
            return;
        }

        const reader = new FileReader();
        reader.onload = function(ev) {
            const previewContainer = document.getElementById(
                e.target.id === 'imagen' ? 'imagen-preview-container' : 'edit-imagen-preview'
            );
            const preview = document.getElementById(
                e.target.id === 'imagen' ? 'imagen-preview' : 'edit-img-preview'
            );
            preview.src = ev.target.result;
            previewContainer.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});

// ========== FUNCIONES AUXILIARES ==========
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function truncarTexto(text, maxLength) {
    if (!text) return '';
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
}
