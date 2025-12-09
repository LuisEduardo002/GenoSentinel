import os
from decouple import config
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent





SECRET_KEY = 'django-insecure-bx8s!dnt!)&7h%%_!j=g@ftw_s(oa@p(jb$+0%4+3%o%o3vmk5'


DEBUG = False  # Set to True for local development

ALLOWED_HOSTS = ['*']  # Configure appropriately for production


# Aplicaciones instaladas

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

#Librerias externas
    'rest_framework',
    'drf_spectacular',
    'corsheaders',

#Aplicaciones 
    'apps.genes',
    'apps.variants',
    'apps.patient_reports',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'genomic_service.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'genomic_service.wsgi.application'


if DEBUG:
    db_host = '127.0.0.1'
    db_port = '3306'
else:
    db_host = config('DB_HOST', default='mysql')
    db_port = config('DB_PORT', default='3306')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME', default='genomica_db'),
        'USER': config('DB_USER', default='root'),
        'PASSWORD': config('DB_PASSWORD', default='hola1234'),
        'HOST': db_host,
        'PORT': db_port,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True




STATIC_URL = 'static/'



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Para el REST framework de Django
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# Para Spectacular Swagger
SPECTACULAR_SETTINGS = {
    'TITLE': 'Microservicio Genomica API',
    'DESCRIPTION': 'API para gestión de información genómica y variantes genéticas de pacientes oncológicos',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
}

# Configuraciones de CORS 
CORS_ALLOWED_ORIGINS = config(
    'CORS_ORIGINS',
    default='http://microservicio-auth:8080',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

CLINICAL_SERVICE_URL = config(
    'CLINICAL_SERVICE_URL', 
    default='http://microservicio-clinica:3001'
)

# URL del Microservicio de Autenticacion
GATEWAY_SERVICE_URL = config(
    'GATEWAY_SERVICE_URL', 
    default='http://microservicio-auth:8080'
)

# Timeout para llamadas HTTP entre microservicios
MICROSERVICE_REQUEST_TIMEOUT = config(
    'MICROSERVICE_REQUEST_TIMEOUT', 
    default=5, 
    cast=int
)