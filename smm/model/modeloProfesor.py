# -*- coding: utf-8 -*-
from model.modeloPersona import modeloPersona
from google.appengine.ext import ndb

class modeloProfesor(modeloPersona):

    grupo = ndb.StringProperty()
    curso = ndb.StringProperty()
    asignatura = ndb.StringProperty()

    alias = ndb.StringProperty()
    password = ndb.StringProperty()
