# core/settings.py
import environ
import os
from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Variables de entorno ──────────────────────────────────────────────────
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY  = env('SECRET_KEY', default='dev-key-insegura-solo-para-desarrollo')
DEBUG       = env('DEBUG', default=True)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['.onrender.com', 'localhost', '127.0.0.1'])

# ── Apps instaladas ───────────────────────────────────────────────────────
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # Terceros
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',              # ← nuevo (nombre de app es django_filters)
    'whitenoise.runserver_nostatic',
    'anymail',                     # ← W17: correo con SendGrid
    # Apps del ERP
    'clientes',
    'proveedores',
    'productos',
    'ventas',
    'reportes',
    'configuracion',
    'catalogo',                    # ← nuevo
    'core',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'core.urls'

# ── Templates ─────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Context processor del carrito — W13
                'catalogo.context_processors.carrito_info',
            ],
        },
    },
]

# ── Base de datos ─────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ── Internacionalización ──────────────────────────────────────────────────
LANGUAGE_CODE = 'es-mx'
TIME_ZONE     = 'America/Mexico_City'
USE_I18N      = True
USE_TZ        = True

# ── Archivos estáticos ────────────────────────────────────────────────────
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']  # fuentes adicionales
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ── Archivos media ────────────────────────────────────────────────────────
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ── Autenticación ─────────────────────────────────────────────────────────
LOGIN_URL           = '/accounts/login/'
LOGIN_REDIRECT_URL  = '/productos/'
LOGOUT_REDIRECT_URL = '/'

# ── DRF ──────────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',   # para el navegador
        'rest_framework.authentication.TokenAuthentication',     # para clientes externos
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── STRIPE (Pasarela de pago) ──────────────────────────────────────────────
STRIPE_SECRET_KEY      = env('STRIPE_SECRET_KEY',      default='sk_test_placeholder')
STRIPE_PUBLISHABLE_KEY = env('STRIPE_PUBLISHABLE_KEY', default='pk_test_placeholder')
STRIPE_WEBHOOK_SECRET  = env('STRIPE_WEBHOOK_SECRET',  default='whsec_placeholder')

# ── JAZZMIN — Personalización del admin con Fable 5 AzulERP ───────────────
JAZZMIN_SETTINGS = {
    # Identidad
    'site_title':       '🎃 Mi ERP 🎃',
    'site_header':      'Gestión Empresarial🧑‍💻',
    'site_brand':       '🏢 Mi ERP 🎃',
    'welcome_sign':     'Inventario, ventas y clientes💯',
    'copyright':        'Victor Emanuel Estrada Villagomez,TSU en Programación🕷️',

    # Icono del sitio (usar emoji como fallback)
    'site_icon':        None,
    'site_logo':        None,    # ruta a logo en static/ (agregar en W11+)

    # Búsqueda global en el admin
    'search_model':     ['clientes.Cliente', 'productos.Producto'],

    # Menú superior (top navigation)
    'topmenu_links': [
        {'name': 'Inicio ERP',   'url': '/', 'new_window': False},
        {'name': 'Productos',    'url': '/productos/'},
        {'name': 'Clientes',     'url': '/clientes/'},
        {'name': 'Ventas',       'url': '/ventas/'},
    ],

    # Menú de usuario (avatar)
    'usermenu_links': [
        {'name': 'Ver ERP', 'url': '/', 'new_window': False},
    ],

    # Menú lateral: orden de apps y modelos
    'order_with_respect_to': [
        'clientes', 'proveedores', 'productos',
        'ventas', 'configuracion', 'auth',
    ],

    # Iconos de Font Awesome para cada modelo
    'icons': {
        'auth':                       'fas fa-users-cog',
        'auth.user':                  'fas fa-user',
        'auth.Group':                 'fas fa-users',
        'clientes.Cliente':           'fas fa-user-tie',
        'proveedores.Proveedor':      'fas fa-truck',
        'productos.Categoria':        'fas fa-tags',
        'productos.Producto':         'fas fa-box',
        'ventas.Venta':               'fas fa-file-invoice-dollar',
        'ventas.DetalleVenta':        'fas fa-list',
        'ventas.Pedido':              'fas fa-shopping-cart',
        'configuracion.ConfiguracionERP': 'fas fa-cogs',
    },
    'default_icon_parents': 'fas fa-folder',
    'default_icon_children': 'fas fa-circle',

    # Apariencia
    'related_modal_active':     True,
    'custom_css':               'erp_custom.css',   # archivo en static/
    'show_sidebar':             True,
    'navigation_expanded':      True,
    'hide_apps':                [],
    'hide_models':              [],

    # UI tweaks
    'changeform_format':        'horizontal_tabs',
    'language_chooser':         False,
}

JAZZMIN_UI_TWEAKS = {
    'navbar_small_text':         False,
    'footer_small_text':         False,
    'body_small_text':           False,
    'brand_small_text':          False,
    'brand_colour':              'navbar-orange',
    'accent':                    'accent-orange',
    'navbar':                    'navbar-gray-dark navbar-dark',
    'no_navbar_border':          False,
    'navbar_fixed':              True,
    'layout_boxed':              False,
    'footer_fixed':              False,
    'sidebar_fixed':             True,
    'sidebar':                   'sidebar-dark-orange',
    'sidebar_nav_small_text':    False,
    'sidebar_disable_expand':    False,
    'sidebar_nav_child_indent':  True,
    'sidebar_nav_compact_style': False,
    'sidebar_nav_legacy_style':  False,
    'sidebar_nav_flat_style':    False,
    'theme':                     'cyborg',
    'default_theme_mode':        'dark',
    'button_classes': {
        'primary':   'btn-primary',
        'secondary': 'btn-secondary',
        'info':      'btn-info',
        'warning':   'btn-warning',
        'danger':    'btn-danger',
        'success':   'btn-success',
    },
}

# ── DJANGO SITES (requerido por allauth) ──────────────────────────────────
SITE_ID = 1

# ── AUTHENTICATION BACKENDS ───────────────────────────────────────────────
AUTHENTICATION_BACKENDS = [
    # Backend estándar de Django (username + password en admin)
    'django.contrib.auth.backends.ModelBackend',
    # Backend de allauth (permite login por email también)
    'allauth.account.auth_backends.AuthenticationBackend',
]

# ── ALLAUTH: configuración para desarrollo académico ──────────────────────
ACCOUNT_LOGIN_METHODS          = {'username'}   # login por username
ACCOUNT_EMAIL_REQUIRED         = False          # no obligar correo
ACCOUNT_EMAIL_VERIFICATION     = 'none'         # no enviar email de verificación
ACCOUNT_LOGOUT_ON_GET          = True           # logout sin confirmar (dev)
ACCOUNT_SESSION_REMEMBER       = True           # recordar sesión

LOGOUT_REDIRECT_URL = '/'

# ── CELERY — Cola de tareas asíncronas ────────────────────────────────────
# Broker: Redis almacena los mensajes de las tareas pendientes
CELERY_BROKER_URL = env('REDIS_URL', default='redis://localhost:6379/0')

# Backend: Redis almacena los resultados de las tareas (opcional)
CELERY_RESULT_BACKEND = env('REDIS_URL', default='redis://localhost:6379/0')

# Formato de serialización (JSON es seguro y portable)
CELERY_ACCEPT_CONTENT    = ['json']
CELERY_TASK_SERIALIZER   = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Zona horaria (heredar de Django)
CELERY_TIMEZONE = TIME_ZONE   # 'America/Mexico_City'

# Reintentos automáticos ante fallos de conexión al broker
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Tiempo máximo que puede correr una tarea antes de ser terminada (segundos)
CELERY_TASK_SOFT_TIME_LIMIT = 300   # 5 minutos
CELERY_TASK_TIME_LIMIT       = 360  # 6 minutos (hard limit)

# Prefijo para las colas (útil si se comparte Redis entre proyectos)
CELERY_TASK_DEFAULT_QUEUE = 'erp_django'

# Modo "eager": las tareas se ejecutan al instante dentro de la misma
# página, sin worker ni Redis. Se controla con variables de entorno:
#   - En local (con worker real): no pongas nada → queda en False.
#   - En Render (sin worker):     CELERY_ALWAYS_EAGER=True en Environment.
# EAGER_PROPAGATES=True hace que los errores (por ejemplo de SendGrid)
# SÍ se vean en los Logs en vez de perderse en silencio.
# En tests se sigue pudiendo usar @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
CELERY_TASK_ALWAYS_EAGER     = env.bool('CELERY_ALWAYS_EAGER', default=False)
CELERY_TASK_EAGER_PROPAGATES = env.bool('CELERY_EAGER_PROPAGATES', default=True)

# ── CORREO ELECTRÓNICO (W17: SendGrid vía django-anymail) ─────────────────
# API key de SendGrid (viene del archivo .env, nunca se escribe aquí)
SENDGRID_API_KEY = env('SENDGRID_API_KEY', default='')

# Backend de correo:
#   - Si hay SENDGRID_API_KEY en el .env  → correo REAL con SendGrid.
#   - Si no hay API key                   → imprime el correo en la terminal.
#   - Si defines EMAIL_BACKEND en el .env → se respeta lo que pongas.
# (Los tests usan su propio backend en memoria, nunca envían correos reales.)
EMAIL_BACKEND = env(
    'EMAIL_BACKEND',
    default=(
        'anymail.backends.sendgrid.EmailBackend'
        if SENDGRID_API_KEY
        else 'django.core.mail.backends.console.EmailBackend'
    ),
)

# Remitente: debe ser el correo verificado como Sender en SendGrid
DEFAULT_FROM_EMAIL = env(
    'DEFAULT_FROM_EMAIL',
    default='ERP Django <noreply@erp-django.com>'
)

EMAIL_SUBJECT_PREFIX = '[ERP Django] '

# Administrador que recibe las alertas de stock y el reporte diario
# (las tareas leen settings.ADMINS[0])
ADMIN_EMAIL = env('ADMIN_EMAIL', default='admin@erp-django.com')
ADMINS = [
    ('Admin ERP', ADMIN_EMAIL),
]

# Token secreto para que un cron externo (cron-job.org) pueda disparar
# el reporte diario sin Celery. Si está vacío, la vista rechaza todo.
CRON_TOKEN = env('CRON_TOKEN', default='')

# django-anymail (SendGrid)
ANYMAIL = {
    'SENDGRID_API_KEY': SENDGRID_API_KEY,
}

# URL pública del sitio (la usan los enlaces de los correos de W17).
# En Render sale sola de RENDER_EXTERNAL_URL; en local cae a localhost.
SITE_URL = env(
    'SITE_URL',
    default=env('RENDER_EXTERNAL_URL', default='http://localhost:8000')
).rstrip('/')

# Ruta de la tienda a la que lleva el botón del correo de confirmación.
# Cámbiala si tu catálogo vive en otra ruta (por ejemplo '/catalogo/').
TIENDA_PATH = env('TIENDA_PATH', default='/')

# ── CELERY BEAT — Tareas programadas (W18) ────────────────────────────────
CELERY_BEAT_SCHEDULE = {

    # Verificar stock bajo cada hora
    'verificar-stock-bajo-cada-hora': {
        'task':     'ventas.verificar_stock_bajo',
        'schedule': timedelta(hours=1),
        'args':     (5,),   # umbral = 5 unidades
        'options':  {'queue': 'erp_django'},
    },

    # Reporte de ventas diario (hora México, formato 24 h).
    # La hora se cambia con REPORTE_HORA y REPORTE_MINUTO en el .env
    # (o en Environment de Render). Si no existen: 8:00 AM.
    'reporte-ventas-diario-8am': {
        'task':     'ventas.reporte_ventas_diario',
        'schedule': crontab(
            hour=env.int('REPORTE_HORA', default=8),
            minute=env.int('REPORTE_MINUTO', default=0),
        ),
        'options':  {'queue': 'erp_django'},
    },

}

# Necesario para que Beat use la zona horaria de Django (no UTC)
CELERY_BEAT_TIMEZONE = TIME_ZONE   # 'America/Mexico_City'