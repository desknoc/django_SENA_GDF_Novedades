// ========== TOGGLE PANEL ==========
const signUpBtn = document.getElementById('signUp');
const signInBtn = document.getElementById('signIn');
const container = document.getElementById('authContainer');

signUpBtn.addEventListener('click', () => {
    container.classList.add('right-panel-active');
});

signInBtn.addEventListener('click', () => {
    container.classList.remove('right-panel-active');
});

// ========== TOGGLE PASSWORD ==========
function togglePassRegistro(el) {
    const input = el.parentElement.querySelector('input');
    const icon = el.querySelector('ion-icon');
    if (input.type === 'password') {
        input.type = 'text';
        icon.setAttribute('name', 'eye-off-outline');
    } else {
        input.type = 'password';
        icon.setAttribute('name', 'eye-outline');
    }
}

// ========== LOGIN ==========
document.getElementById('formLogin').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(this);

    // Validar campos
    if (!formData.get('tipo_documento') || !formData.get('documento') || !formData.get('password')) {
        Swal.fire({
            icon: 'warning',
            title: 'Campos incompletos',
            text: 'Por favor, completa todos los campos.',
            confirmButtonColor: '#28a745'
        });
        return;
    }

    try {
        const response = await fetch('/usuarios/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const text = await response.text();

        if (text.includes('Inicio de sesión exitoso') || text.includes('success')) {
            Swal.fire({
                icon: 'success',
                title: '¡Inicio de sesión exitoso!',
                timer: 1500,
                showConfirmButton: false
            }).then(() => {
                window.location.href = '/novedades/';
            });
        } else if (text.includes('Credenciales inválidas')) {
            Swal.fire({
                icon: 'error',
                title: 'Credenciales inválidas',
                text: 'Verifica tu documento y contraseña.',
                confirmButtonColor: '#28a745'
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: text || 'Error del servidor. Intenta nuevamente.',
                confirmButtonColor: '#28a745'
            });
        }
    } catch (error) {
        console.error('Error en login:', error);
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Error de conexión. Por favor, intenta nuevamente.',
            confirmButtonColor: '#28a745'
        });
    }
});

// ========== REGISTRO ==========
document.getElementById('formRegistro').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(this);

    if (formData.get('password').length < 8) {
        Swal.fire({
            icon: 'warning',
            title: 'Contraseña muy corta',
            text: 'La contraseña debe tener al menos 8 caracteres.',
            confirmButtonColor: '#28a745'
        });
        return;
    }

    try {
        const response = await fetch('/usuarios/registro/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const text = await response.text();

        if (text.includes('registrado') || text.includes('exitosa')) {
            Swal.fire({
                icon: 'success',
                title: '¡Registro Exitoso!',
                text: 'Tu cuenta ha sido creada. Ahora puedes iniciar sesión.',
                confirmButtonColor: '#28a745'
            }).then(() => {
                container.classList.remove('right-panel-active');
                this.reset();
            });
        } else if (text.includes('ya existe')) {
            Swal.fire({
                icon: 'warning',
                title: 'Usuario existente',
                text: 'Ese documento ya está registrado.',
                confirmButtonColor: '#28a745'
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Error en el registro',
                text: text || 'No se pudo registrar el usuario.',
                confirmButtonColor: '#28a745'
            });
        }
    } catch (error) {
        console.error('Error en registro:', error);
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Error de conexión. Por favor, intenta nuevamente.',
            confirmButtonColor: '#28a745'
        });
    }
});
