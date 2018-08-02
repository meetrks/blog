from .base import *

DEBUG = False

ALLOWED_HOSTS = []

SECRET_KEY = os.environ.get('SECRET_KEY', '$c6wtefwk+awg8wdb$0zq6$6cc8u740xr#%)*@1hnj4pm3@e0z')

CORS_ORIGIN_ALLOW_ALL = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', "blog"),
        'USER': os.environ.get('USER_NAME', "blog"),
        'PASSWORD': os.environ.get('PASSWORD', "blog"),
        'HOST': os.environ.get('HOST_NAME', "localhost"),
        'PORT': os.environ.get('PORT', "3306"),
    }
}
