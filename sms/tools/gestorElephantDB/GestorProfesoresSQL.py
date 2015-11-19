# -*- coding: utf-8 -*-
#import MySQLdb
from Profesor import *
from Alumno import *
from Asignatura import *
import os
import psycopg2
import urlparse
import clavesElephantSQL

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(clavesElephantSQL.DATABASE_URL)
conn = psycopg2.connect(database=url.path[1:],
  user=url.username,
  password=url.password,
  host=url.hostname,
  port=url.port
)
