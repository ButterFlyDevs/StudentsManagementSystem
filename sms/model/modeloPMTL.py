# -*- coding: utf-8 -*-
from model.modeloPersona import modeloPersona
from google.appengine.ext import ndb

class modeloPMDTL(modeloPersona):

    profesion = ndb.StringProperty()
    estudios = ndb.StringProperty()
    condicionCivil = ndb.StringProperty()
