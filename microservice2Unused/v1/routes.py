# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###

from .api.products import Products
from .api.profesores import Profesores


routes = [
    dict(resource=Products, urls=['/products'], endpoint='products'),
    dict(resource=Profesores, urls=['/profesores'], endpoint='profesores'),
]