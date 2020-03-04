import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEPLOY_DIR = os.path.dirname(BASE_DIR)

DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bootstrap4',
    'ordered_model',
    'sorl.thumbnail',
    'django_filters',
    'django_cbrf',

    'catalog',
    'home',
    'users',
    'cart',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'isletworkshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'isletworkshop.wsgi.application'

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
AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = [
    'users.backends.EmailBackend',
]
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

TIME_ZONE = 'UTC'
USE_TZ = True

LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Русский'),
]
USE_I18N = True
USE_L10N = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(DEPLOY_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_files'), ]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(DEPLOY_DIR, 'media')

THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
THUMBNAIL_REDIS_DB = 0
THUMBNAIL_REDIS_HOST = '127.0.0.1'
THUMBNAIL_REDIS_PORT = 6379

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'

CART_SESSION_KEY = '_cart'

BOOTSTRAP4 = {
    'css_url': {
        'href': os.path.join(STATIC_URL, 'css/bootstrap.min.css'),
    },
    'theme_url': None,
    'javascript_url': {
        'url': os.path.join(STATIC_URL, 'js/bootstrap.bundle.min.js'),
    },
    'include_jquery': 'full',
    'jquery_url': {
        'url': os.path.join(STATIC_URL, 'js/jquery.min.js'),
    },
}
