# -*- coding: utf-8 -*-
from google.appengine.ext import ndb

class modeloPersona(ndb.Model):

    nombre = ndb.StringProperty()
    apellidos = ndb.StringProperty()
    dni = ndb.StringProperty()
    tlf = ndb.StringProperty()
