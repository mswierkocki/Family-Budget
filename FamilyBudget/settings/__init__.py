#import os
#os.environ['APP_ENV']
from .base import *
from decouple import config
APP_ENV = config('APP_ENV',default="dev",cast=str)
if APP_ENV == 'prod':
   from .prod import *
else:
   from .dev import *