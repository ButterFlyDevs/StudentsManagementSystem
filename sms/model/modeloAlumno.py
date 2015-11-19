# -*- coding: utf-8 -*-
from model.modeloPersona import modeloPersona
from google.appengine.ext import ndb

class modeloAlumno(modeloPersona):

    grupo = ndb.StringProperty()
    curso = ndb.StringProperty()
