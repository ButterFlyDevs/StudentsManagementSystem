from fabric import *

#Fihcero fabric. Se definen todos los métodos que se usarán con fabric
#
#   Uso en terminal: fab <orden>
#
#
#

#Definir la info del servidor
def info_servidor():
    run ('uname -s')

#Se cierra todo proceso que esté corriendo  con Python (nos interesa por que google appengine corre con él)
def pararTodo():
    run ('kill -9 $(pidof python)')

def lanzarTodo():

def lanzarServicioBD():

def lanzarServicioControlEstdiantes():

    pass
def instalarDependencias():

    pass
def obtenerLineasProyecto():

    pass
def subirGAE():

    pass
def actualizarProyecto():

    pass
def borrarProyecto():

    pass
def test_APIBD():

    pass
