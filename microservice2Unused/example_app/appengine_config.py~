# -*- coding: utf-8 -*-
from gaesessions import SessionMiddleware
def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app, cookie_key="djkdskdiehfivnskjdnkuwndiuskjsdkusknskuu")
    return app

from google.appengine.ext import vendor
#Para que entienda que las librerías de terceros debe buscarlas en la carpeta lib
vendor.add('lib')
