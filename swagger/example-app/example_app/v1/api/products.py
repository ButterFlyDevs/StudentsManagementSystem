# -*- coding: utf-8 -*-
from flask import request, g

from . import Resource
from .. import schemas


class Products(Resource):

    def get(self):
        print g.args

        return [], 200, None