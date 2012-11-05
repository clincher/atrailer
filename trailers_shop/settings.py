# -*- coding: utf-8 -*-
import os

from cbsettings import DjangoDefaults


class CommonSettings(DjangoDefaults):

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
            'NAME': 'database.sqlite',
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

    ROOT_URLCONF = 'trailers_shop.urls'

    WSGI_APPLICATION = 'trailers_shop.wsgi.application'

    TEMPLATE_DIRS = (
        os.path.join(PROJECT_ROOT, 'templates'),
    )

    INSTALLED_APPS = [
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
    ]

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


from local_settings import LocalSettings


class Settings(LocalSettings):

    INSTALLED_APPS = LocalSettings.INSTALLED_APPS + [
        # external apps
        'sorl.thumbnail',
        'polymorphic',
        'shop',
        'south',
        'sitetree',
        'tinymce',
        'treeadmin',
        'shop_categories',
        'django_extensions',
        # internal apps
        'trailers_shop.apps.common',
        'trailers_shop.apps.customshop',
        'trailers_shop.apps.customshop.address',
        'trailers_shop.apps.articles',
        'trailers_shop.apps.banners',
    ]

    SHOP_SHIPPING_BACKENDS = [
        'trailers_shop.apps.customshop.shipping.backends.pickup.PickupShipping',
        'trailers_shop.apps.customshop.shipping.backends.delivery_in_moscow.DeliveryInMoscowShipping',
        ]
    SHOP_PAYMENT_BACKENDS = [
        'trailers_shop.apps.customshop.payments.backends.pay_with_cash.PayWithCashBackend'
    ]

    SHOP_ADDRESS_MODEL = 'trailers_shop.apps.customshop.address.models.Address'
    SHOP_PRODUCT_MODEL = 'trailers_shop.apps.customshop.models.CustomProduct'
    SHOP_CATEGORIES_CATEGORY_MODEL = 'trailers_shop.apps.customshop.models.category.Category'

    if LocalSettings.DEBUG:
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
            + LocalSettings.MIDDLEWARE_CLASSES)

        INTERNAL_IPS = ('127.0.0.1',)
        DEBUG_TOOLBAR_CONFIG = dict(
            INTERCEPT_REDIRECTS = False
        )
        INSTALLED_APPS += ['debug_toolbar',]

        STATICFILES_DIRS = LocalSettings.STATICFILES_DIRS +\
                           (os.path.join(LocalSettings.PROJECT_ROOT, 'media'),)
    else:
        FILES_URL = 'http://files.savvatrailers_shop.com'
        MEDIA_URL = FILES_URL + LocalSettings.MEDIA_URL
        STATIC_URL = FILES_URL + LocalSettings.STATIC_URL

        TEMPLATE_LOADERS = (
            ('django.template.loaders.cached.Loader',
             LocalSettings.TEMPLATE_LOADERS),
        )
