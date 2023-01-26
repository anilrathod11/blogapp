from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# print ("base dir path", BASE_DIR)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v=q&&gvczxzk4^ro3^sc9o@4csfjo6)2_+v4(&qm^(!$pzr7b@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# LOGIN_REDIRECT_URL = "blog/list"
# ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'
LOGIN_URL = 'two_factor:login'

# Application definition
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'oauth2_provider',
    'social_django',
    'drf_social_oauth2',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    "corsheaders",
    'drf_yasg',
    'blogs',
    'user_app',
    'rest_framework',
    'rest_framework.authtoken',
    'django_celery_results',
    'django_celery_beat',
    'storages',
    'sub_plan_app',
    # 2FA
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',
]
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_otp.middleware.OTPMiddleware',
]

SITE_ID = 1
ROOT_URLCONF = 'my_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'django.template.context_processors.request',
            ],
        },
    },
]


WSGI_APPLICATION = 'my_blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog_management',
        'USER': 'root',
        'PASSWORD': 'Rathod@11',
        'HOST':'localhost',
        'PORT':'3306',
        'TIME_ZONE': 'Asia/Kolkata',
    }
}
AUTH_USER_MODEL = "user_app.CustomeUser" 

# CORS configuration
# Access_Control_Allow_Origin = ["*"]
CSRF_TRUSTED_ORIGINS = ['https://accounts.google.com/o/oauth2/v2/auth/identifier?client_id=840708859618-rm4fvhibo0dk7j8elukp00qp9uqqp52q.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Faccounts%2Fgoogle%2Flogin%2Fcallback%2F&scope=profile%20email&response_type=code&state=B74KqXCUsZqu&access_type=online&code_challenge_method=S256&code_challenge=HVh0Ll6_ARF8UMXaVPxFcoPBK46Oa6Ah22-8rjf2CJg&service=lso&o2v=2&flowName=GeneralOAuthFlow']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = [
'accept',
'accept-encoding',
'authorization',
'content-type',
'dnt',
'origin',
'user-agent',
'x-csrftoken',
'x-requested-with',
"ngrok-skip-browser-warning",
]


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIM_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# print(datetime.datetime.now())

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'  
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')  
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'media'),
]
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'drf_social_oauth2.authentication.SocialAuthentication',
    ],
}
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}

# CELERY SETTINGS
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_RESULT_BACKEND = 'django-db'

#CELERY BEAT
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
DJANGO_CELERY_BEAT_TZ_AWARE = False

# SMTP Settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER ='anil.pune11@gmail.com'
EMAIL_HOST_PASSWORD = "acqbpttqdyzqkfgj"
DEFAULT_FROM_EMAIL = 'Celery <anil.pune11@gmail.com>'


# AWS services conf
# DEFAULT_FILE_STORAGE = "django_s3_storage.storage.S3Storage",
# STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"

# S3 bucket configuration
# AWS_ACCESS_KEY_ID = ""
# AWS_SECRET_ACCESS_KEY = ""
# AWS_S3_BUCKET_NAME = ""

# stripe configuration

# STRIPE_PUBLISHABLE_KEY = 'pk_test_51MPQOQSEibFHYgaHC6CUkgNkPjlJFZNDjzqbTv5bvaDRIpl52vHF0d6m1iJuwykCp5A6e4iy3uLSXfTrog0K7d8j00ACE08Tfe'
# STRIPE_SECRET_KEY = 'sk_test_51MPQOQSEibFHYgaHJ5sq1lfdCzuaCIfBdnTndNQGeqbMDPWNsu1BsrVXlL6snHilMRYikF7auakNwt55doXWocXv00HhTqoMvM'
# STRIPE_PRICE_ID = 'price_1MPQd9SEibFHYgaHQRgLL2G6'


# 840708859618-rm4fvhibo0dk7j8elukp00qp9uqqp52q.apps.googleusercontent.com
# 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