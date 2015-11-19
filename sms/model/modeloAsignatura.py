# -*- coding: utf-8 -*-
from google.appengine.ext import ndb

class modeloAsignatura(ndb.Model):

    nombre = ndb.StringProperty()
    curso = ndb.StringProperty()
