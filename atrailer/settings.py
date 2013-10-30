# -*- coding: utf-8 -*-
import os


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Vasiliy Bolshakov', 'va.bolshakov@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'atrailer.ru.sqlite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

APPEND_SLASH = False

USE_I18N = True
USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

FILEBROWSER_DIRECTORY = ''

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates/static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'qtxw9=oj2xnd&amp;!c%4d%s_!hl#(_ep=f@#j(ypwvwfg3=ehf61e'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'atrailer.urls'

WSGI_APPLICATION = 'atrailer.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = [
    'grappelli',
    'filebrowser',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',
    'sitetree',
    ]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "atrailer.apps.customshop.context_processors.forms",
    "atrailer.apps.customshop.context_processors.categories",
    "atrailer.apps.callback.context_processors.forms",
]

TINYMCE_JS_URL = STATIC_URL + \
                 'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

from atrailer.local_settings import *

INSTALLED_APPS = INSTALLED_APPS + [
    # external apps
    'sorl.thumbnail',
    'polymorphic',
    'shop',
    'south',
    'tinymce',
    'treeadmin',
    'shop_categories',
    'django_extensions',
    # internal apps
    'atrailer.apps.common',
    'atrailer.apps.customshop',
    'atrailer.apps.customshop.categories',
    'atrailer.apps.customshop.address',
    'atrailer.apps.articles',
    'atrailer.apps.banners',
    'atrailer.apps.callback',
]

SHOP_SHIPPING_BACKENDS = [
    'atrailer.apps.customshop.shipping.backends.pickup.PickupShipping',
    'atrailer.apps.customshop.shipping.backends.delivery_in_moscow.DeliveryInMoscowShipping',
    ]
SHOP_PAYMENT_BACKENDS = [
    'atrailer.apps.customshop.payments.backends.pay_with_cash.PayWithCashBackend'
]

SHOP_ADDRESS_MODEL = 'atrailer.apps.customshop.address.models.Address'
#    SHOP_PRODUCT_MODEL = ('atrailer.apps.customshop.base_models.CustomProduct', 'shop')
SHOP_CATEGORIES_CATEGORY_MODEL = 'atrailer.apps.customshop.categories.models.Category'

ALLOWED_HOSTS = [
    'atrailer.ru',
    'atrailer.ru.',
    'localhost'
]

if DEBUG:
    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
    #    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
    )
    MIDDLEWARE_CLASSES = (
        ('debug_toolbar.middleware.DebugToolbarMiddleware',)
        + MIDDLEWARE_CLASSES)

    INTERNAL_IPS = ('127.0.0.1',)
    DEBUG_TOOLBAR_CONFIG = dict(
        INTERCEPT_REDIRECTS = False
    )
    INSTALLED_APPS += ['debug_toolbar',]

    # STATICFILES_DIRS = LocalSettings.STATICFILES_DIRS +\
    #                    (os.path.join(LocalSettings.PROJECT_ROOT, 'media'),)
else:
    FILES_URL = 'http://atrailer.ru'
    # MEDIA_URL = FILES_URL + LocalSettings.MEDIA_URL
    STATIC_URL = FILES_URL + STATIC_URL

    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader',
         TEMPLATE_LOADERS),
    )
