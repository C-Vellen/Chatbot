# package des settings :

# si bd mysql : décommenter les 2 lignes ci-dessous
import pymysql

pymysql.install_as_MySQLdb()


from .base import *

try:
    from .develop import *
except ModuleNotFoundError:
    pass

try:
    from .production import *
except ModuleNotFoundError:
    pass
