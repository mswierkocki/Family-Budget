# flake8: noqa

from .base import *  
from decouple import config
APP_ENV = config('APP_ENV', default="dev", cast=str)
if APP_ENV == 'prod':
    from .prod import *  
elif APP_ENV == 'heroku':
    from .heroku import * 
else:
    from .dev import *
