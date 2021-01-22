import os
from django.contrib.messages import constants as messages



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^tl()34n(74#+)7m76z-n9#0isg)li+bbhu1edum*8&wfoq543'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Overriding message tag 
MESSAGE_TAGS = {
    messages.ERROR : 'danger',
    }
# overriding ends her

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # For using django forms
    'crispy_forms',
    # Django template Math FIlter
    'mathfilters',

    # REST API libraries
    'rest_framework',
     'rest_framework.authtoken',
     'django_rest_passwordreset',
    #'knox',

    # WebApp Apps
    'homeApp',
    'accounts',
    'travelagency',
    'qna',
    'touring',
    'traveller',

    # API Apps
    'api.home',
    'api.accountsAPI',
    'api.tours',
    'api.travelagencyAPI',
    'api.travellerAPI',

]
CRISPY_TEMPLATE_PACK = 'bootstrap4'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'travmaks.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

AUTH_USER_MODEL = 'accounts.User'
WSGI_APPLICATION = 'travmaks.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'iycvP8wTqP',
        'USER':'iycvP8wTqP',
        'PASSWORD':'7qghTb2EZz',
        'HOST':'remotemysql.com',
        'PORT':'3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 2
}

# Static
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR,'designs')

# Media File
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# TRAVMAKS Production mail 
'''
DEFAULT_FROM_EMAIL = 'travmaks-admin@travmaks.in'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Example for using Zoho Mail as email sending backend
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST = 'smtp.zoho.in'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'travmaks-admin@travmaks.in'
EMAIL_HOST_PASSWORD = 'iamtravmaks07!'
'''
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
MAILER_EMAIL_BACKEND = EMAIL_BACKEND
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT=587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'makscub3e@gmail.com'
EMAIL_HOST_PASSWORD = 'Weareteammaks07!'