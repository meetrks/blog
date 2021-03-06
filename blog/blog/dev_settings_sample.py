from .base import *

DEBUG = True

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
