# SENA GDF — Sistema de Gestión de Novedades

Plataforma web para la gestión de comunicados y novedades del **SENA — Grupo de Formación**. Permite a administradores crear, editar y eliminar novedades, y a aprendices visualizarlas.

---

## Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3 + Django 6.0 |
| Base de datos | MySQL |
| Frontend | HTML5 + CSS3 + Vanilla JavaScript |
| Estilos | Bootstrap 5.3.3 + CSS propio |
| Notificaciones | SweetAlert2 |
| Autenticación | Sistema propio con modelo `Usuario` personalizado |

---

## Arquitectura

### Monolito Django — MVT (Model-View-Template)

Es un **monolito Django clásico**. Sin DRF, sin microservicios, sin API Gateway. Dos apps dentro de un solo proyecto que se encargan de dominios distintos.

```
                    ┌─────────────────────────────┐
                    │     senagdf (config)         │
                    │  settings.py · urls.py       │
                    │  validators.py · asgi/wsgi   │
                    └──────┬──────────────────────┘
                           │ include()
              ┌────────────┼────────────┐
              ▼             ▼            │
   ┌─────────────────┐ ┌──────────────┐  │
   │   novedades      │ │  usuarios    │  │
   │   CRUD de        │ │  Auth +      │  │
   │   comunicados    │ │  Usuarios    │  │
   └────────┬─────────┘ └──────┬───────┘  │
            │                  │          │
            └──────────────────┼──────────┘
                               ▼
                    ┌─────────────────────┐
                    │     MySQL            │
                    │  novedades_*         │
                    │  usuarios_*          │
                    └─────────────────────┘
```

### Híbrido API + Server Render

El proyecto tiene **dos caras** conviviendo:

- **API endpoints** → devuelven JSON (`JsonResponse`), consumidos por el frontend JS via `fetch()` + `FormData`. Operaciones CRUD, login, registro.
- **Template views** → devuelven HTML renderizado (`render()`) para páginas completas. Home, detalle, formularios admin, login.

Las vistas están deliberadamente separadas en cada `views.py` con comentarios que marcan el límite.

### Modelado UML

Diagramas de clases, componentes y secuencia generados con PlantUML.

#### Diagrama de Clases — Modelo de Datos

![Diagrama de Clases](static/img/uml-classes.png)

<details>
<summary>Ver código fuente PlantUML</summary>

```plantuml
@startuml
skinparam backgroundColor #FEFEFE
skinparam class {
  BackgroundColor #F8F9FA
  BorderColor #2C3E50
  HeaderBackgroundColor #2C3E50
  HeaderFontColor white
  FontColor #2C3E50
}

package "senagdf (config)" {
  class validators {
    + {static} validar_documento(documento): bool
    + {static} validar_nombre(texto): bool
    + {static} validar_celular(celular): bool
    + {static} validar_correo(correo): bool
    + {static} validar_password(password): bool
  }
}

package "usuarios" {
  class UserManager {
    + create_user(documento, password, **extra_fields): Usuario
    + create_superuser(documento, password): Usuario
  }

  class Usuario {
    - primer_nombre: CharField
    - segundo_nombre: CharField (nullable)
    - primer_apellido: CharField
    - segundo_apellido: CharField (nullable)
    - tipo_documento: CharField [CC | TI]
    - documento: CharField {unique}
    - celular: CharField
    - grupo_formacion: IntegerField (nullable)
    - correo_electronico: CharField {unique}
    - rol: CharField [ADMIN | APRENDIZ]
    - tipo_apoyo: CharField
    - fecha_registro: DateField {auto}
    - ultima_actualizacion: DateField {auto}
    - is_active: BooleanField
    - is_staff: BooleanField
    + USERNAME_FIELD = "documento"
  }

  UserManager --> Usuario : crea >
}

package "novedades" {
  class Comunicado {
    - id: BigAutoField {PK}
    - titulo: CharField(200)
    - contenido: CharField(1000)
    - categoria: CharField(50)
    - imagen_url: TextField {base64}
    - url_referencia: CharField(500)
    - fecha_publicacion: DateField {auto_now_add}
    - ultima_actualizacion: DateField {auto_now}
  }
}

note top of Comunicado
  Almacena imágenes como
  texto base64 en lugar de
  archivos en disco.
end note

validators -r-> Usuario : <<validate>>
validators -r-> Comunicado : <<validate>>
@enduml
```

</details>

#### Diagrama de Componentes — Arquitectura en Capas

![Diagrama de Componentes](static/img/uml-components.png)

<details>
<summary>Ver código fuente PlantUML</summary>

```plantuml
@startuml
skinparam backgroundColor #FEFEFE
skinparam component {
  BackgroundColor #E8F4F8
  BorderColor #2980B9
  FontColor #2C3E50
}
skinparam database {
  BackgroundColor #F0F8F0
  BorderColor #27AE60
  FontColor #2C3E50
}

package "FRONTEND (Navegador)" {
  [Templates HTML\n(Django Template Language)] as TEMPLATES
  [CSS + Bootstrap 5.3.3] as CSS
  [Vanilla JS\n(auth.js · novedades.js · main.js)] as JS
  [SweetAlert2] as SWAL
  JS --> SWAL : notificaciones
}

package "BACKEND — django_SENA_GDF_Novedades" {
  [Root URL Dispatcher\nsenagdf/urls.py] as URLS

  package "senagdf" {
    [settings.py] as SETTINGS
    [validators.py] as VALIDATORS
  }

  package "usuarios" {
    [usuarios/views.py\nlogin · registro · logout] as U_VIEWS
    [usuarios/models.py\nUsuario + UserManager] as U_MODELS
    [usuarios/urls.py] as U_URLS
  }

  package "novedades" {
    [novedades/views.py\nHome · CRUD · Templates] as N_VIEWS
    [novedades/models.py\nComunicado] as N_MODELS
    [novedades/urls.py] as N_URLS
  }

  URLS --> U_URLS : include(/usuarios/)
  URLS --> N_URLS : include(/novedades/)
  U_URLS --> U_VIEWS
  N_URLS --> N_VIEWS
  U_VIEWS --> U_MODELS : ORM
  U_VIEWS --> VALIDATORS : validate
  N_VIEWS --> N_MODELS : ORM
  N_VIEWS --> VALIDATORS : validate
}

database "MySQL" {
  [tabla: usuarios_usuario]
  [tabla: novedades_comunicado]
  [tabla: auth_* (Django internas)]
}

U_MODELS --> MySQL : mysqlclient
N_MODELS --> MySQL : mysqlclient

JS --> URLS : fetch() + FormData\n(AJAX / JSON)
TEMPLATES --> N_VIEWS : GET render()
@enduml
```

</details>

#### Diagrama de Secuencia — Flujo: Crear Novedad

![Diagrama de Secuencia](static/img/uml-sequence.png)

<details>
<summary>Ver código fuente PlantUML</summary>

```plantuml
@startuml
skinparam backgroundColor #FEFEFE
skinparam sequence {
  ActorBorderColor #2C3E50
  ActorFontColor #2C3E50
  LifeLineBorderColor #3498DB
  LifeLineBackgroundColor #EAF2F8
  ParticipantBorderColor #3498DB
  ParticipantBackgroundColor #EAF2F8
  ParticipantFontColor #2C3E50
  ArrowColor #2C3E50
  NoteBorderColor #F39C12
  NoteBackgroundColor #FEF9E7
}

actor "Admin" as ADMIN
participant "Navegador\n(novedades.js)" as JS
participant "Django\n(novedades/views.py)" as DJANGO
participant "senagdf/validators.py" as VAL
database "MySQL" as DB

ADMIN -> JS: Llena formulario y\nhace clic en Guardar
activate JS

JS -> JS: Valida campos\nen frontend (opcional)
note right: Tamaño de imagen,\ncampos requeridos

JS -> DJANGO: POST /novedades/crearnovedad/\n(FormData con imagen)
activate DJANGO

DJANGO -> DJANGO: Verifica autenticación\ny rol == ADMIN
note right: request.user\n.is_authenticated\nrequest.user.rol

alt No autenticado o no ADMIN
  DJANGO --> JS: JsonResponse({error})
  JS --> ADMIN: SweetAlert error
  deactivate DJANGO
end

DJANGO -> DJANGO: Valida tamaño imagen\n(≤ 5MB)

alt Imagen muy pesada
  DJANGO --> JS: JsonResponse({error})
  JS --> ADMIN: SweetAlert error
end

DJANGO -> VAL: validar_magic_bytes()
activate VAL
VAL --> DJANGO: True / False
deactivate VAL

alt Magic bytes inválidos
  DJANGO --> JS: JsonResponse({error})
  JS --> ADMIN: SweetAlert error
end

DJANGO -> DJANGO: Convierte imagen\na base64

DJANGO -> DB: Comunicado.objects.create(\ntitulo, contenido,\ncategoria, imagen_url,\nurl_referencia)

alt OperationalError (MySQL)
  DB --> DJANGO: Error 1153
  DJANGO --> JS: JsonResponse({error})
  JS --> ADMIN: SweetAlert error
else Éxito
  DB --> DJANGO: objeto creado
  DJANGO --> JS: JsonResponse({mensaje})
  deactivate DJANGO
  JS --> ADMIN: SweetAlert\n"¡Novedad creada\nexitosamente!"
  deactivate JS
end
@enduml
```

</details>

---

## Patrones de Diseño

| Patrón | Dónde se usa |
|--------|-------------|
| **MVT (Model-View-Template)** | Todo el proyecto — patrón nativo de Django |
| **Custom User Manager** | `usuarios/models.py` — `UserManager` extiende `BaseUserManager`, autenticación por **documento** en vez de username |
| **Thin Model / Fat View** | Los models son pura definición de campos; toda la lógica de negocio (validaciones, permisos, transformación de imágenes) está en `views.py` |
| **AJAX / JSON API Pattern** | Frontend Vanilla JS ↔ Backend via `FormData` + `fetch()` + respuestas `JsonResponse` |
| **Validation Module** | `senagdf/validators.py` — funciones puras de regex (`validar_documento`, `validar_nombre`, etc.) reutilizadas desde las views |
| **Template Inheritance** | `base.html` → `home.html`, `detalle.html`, `form.html`, etc. via `{% extends %}` |
| **Route Segregation** | Cada app con su propio `urls.py`, importado via `include()` en el root |
| **Magic Bytes Validation** | `validar_magic_bytes()` en novedades — seguridad para verificar el tipo real de imagen (JPEG, PNG, GIF, WebP) antes de guardarla |

---

## Estructura del Proyecto

```
django_SENA_GDF_Novedades/
│
├── senagdf/                      # Configuración del proyecto
│   ├── settings.py               # Config global, DB, apps instaladas
│   ├── urls.py                   # Root URL dispatcher
│   ├── validators.py             # Validaciones compartidas (regex)
│   ├── asgi.py / wsgi.py         # Entry points de despliegue
│   └── __init__.py
│
├── novedades/                    # App de comunicados
│   ├── models.py                 # Modelo Comunicado
│   ├── views.py                  # CRUD lógico + vistas de templates
│   ├── urls.py                   # Rutas de la app
│   ├── admin.py / tests.py       # Admin y tests
│   └── migrations/               # Migraciones de DB
│
├── usuarios/                     # App de autenticación
│   ├── models.py                 # Modelo Usuario + UserManager
│   ├── views.py                  # Login, registro, logout
│   ├── urls.py                   # Rutas de la app
│   ├── admin.py / tests.py
│   └── migrations/
│
├── templates/                    # Templates HTML
│   ├── base.html                 # Layout base (header + sidebars)
│   ├── error404.html             # Página 404
│   ├── auth/
│   │   └── login.html            # Login / Registro
│   ├── includes/
│   │   ├── header.html           # Header reutilizable
│   │   ├── sidebar_admin.html    # Sidebar para administradores
│   │   └── sidebar_aprendiz.html # Sidebar para aprendices
│   └── novedades/
│       ├── home.html             # Home con listado de novedades
│       ├── detalle.html          # Detalle de una novedad
│       └── admin/
│           ├── lista.html        # Listado admin (CRUD)
│           └── form.html         # Formulario crear/editar
│
├── static/                       # Archivos estáticos
│   ├── css/
│   │   ├── bootstrap.min.css     # Bootstrap 5.3.3 local
│   │   ├── auth.css              # Estilos login
│   │   ├── header.css            # Estilos header
│   │   ├── sidebar.css           # Estilos sidebar
│   │   ├── novedades.css         # Estilos novedades
│   │   └── error404.css          # Estilos 404
│   ├── js/
│   │   ├── bootstrap.bundle.min.js
│   │   ├── auth.js               # Lógica login/registro
│   │   ├── novedades.js          # Lógica CRUD novedades
│   │   └── main.js               # Lógica general
│   └── img/
│
├── .env                          # Variables de entorno (NO COMMITEAR)
├── .gitignore
├── manage.py                     # Entry point de Django
└── README.md
```

---

## Funcionalidades

### Roles
- **ADMIN** — CRUD completo de novedades, gestión de usuarios
- **APRENDIZ** — Visualización de novedades publicadas

### Autenticación
- Login y registro con validación en frontend + backend
- Usuario personalizado por **documento** (no username)
- Validación de contraseña mínima (8 caracteres)
- Validación de formato con regex (documento, nombre, celular, correo)
- Protección CSRF en peticiones AJAX

### Novedades (Comunicados)
- Crear, editar, eliminar y ver detalle
- Imágenes en base64 con validación de:
  - **Tamaño máximo**: 5MB
  - **Magic bytes**: solo JPEG, PNG, GIF, WebP
- Categorización de novedades
- Fecha de publicación y última actualización automáticas

### Frontend
- Diseño responsive con sidebar overlay en mobile
- Bootstrap 5.3.3 (CDN + respaldo local)
- SweetAlert2 para todas las notificaciones
- Header con información del usuario autenticado

---

## Setup Local

```bash
# 1. Clonar el repo
git clone <repo-url>
cd django_SENA_GDF_Novedades

# 2. Crear y activar entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1    # Windows
# source venv/bin/activate     # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
# Copiar .env.example a .env y completar con tus datos
# DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

# 5. Ejecutar migraciones
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Iniciar servidor
python manage.py runserver
```

> **Nota:** Asegurate de tener MySQL corriendo en el puerto configurado antes de ejecutar migraciones.

---

## Endpoints

### API (JSON)

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/usuarios/` | Iniciar sesión |
| POST | `/usuarios/registro/` | Registrarse |
| GET | `/usuarios/cerrarSesion/` | Cerrar sesión |
| GET | `/novedades/` | Listar novedades (JSON) |
| POST | `/novedades/crearnovedad/` | Crear novedad |
| POST | `/novedades/editar/<id>/` | Editar novedad |
| POST | `/novedades/eliminarnovedad/<id>/` | Eliminar novedad |
| GET | `/novedades/detallenovedad/<id>/` | Detalle de novedad (JSON) |

### Templates (HTML)

| Ruta | Descripción |
|------|-------------|
| `/usuarios/login/` | Login / Registro |
| `/novedades/` | Home |
| `/novedades/detalle/<id>/` | Detalle de novedad |
| `/novedades/admin/` | Admin: listado |
| `/novedades/admin/crear/` | Admin: crear novedad |
| `/novedades/admin/editar/<id>/` | Admin: editar novedad |

---

## Licencia

Proyecto académico — SENA
