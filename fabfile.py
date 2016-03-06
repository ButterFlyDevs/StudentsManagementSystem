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


def instalarDependencias():


def obtenerLineasProyecto():


def subirGAE():


def actualizarProyecto():

def borrarProyecto():

def test_APIBD():
