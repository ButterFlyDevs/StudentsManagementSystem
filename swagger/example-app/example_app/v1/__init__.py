# -*- coding: utf-8 -*-
from flask import Blueprint
import flask_restful as restful

from .routes import routes
from .validators import security


@security.scopes_loader
def current_scopes():
    return []

bp = Blueprint('v1', __name__)
api = restful.Api(bp, catch_all_404s=True)

for route in routes:
    api.add_resource(route.pop('resource'), *route.pop('urls'), **route)