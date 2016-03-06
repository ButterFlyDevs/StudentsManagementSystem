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
    run ('./run')
def lanzarServicioBD():
    run ('google_appengine/dev_appserver.py --port=8001 --admin_port=8082 SMS-Back-End/microservicio1/microservicio1.yaml')
def lanzarServicioControlEstdiantes():
    run ('google_appengine/dev_appserver.py --port=8001 --admin_port=8082 SMS-Back-End/microservicio1/microservicio2.yaml')

def instalarDependenciasServicioBD():
    run ('sudo pip install -r SMS-Back-End/microservicio1/requirements.txt')
def instalarDependenciasServicioControlEstudiantes():
    run ('sudo pip install -r SMS-Back-End/microservicio2/requirements.txt')
def instalarTodasDependencias():
    run ('sudo ')
     run ('sudo pip install -r SMS-Back-End/microservicio1/requirements.txt')
     run ('sudo pip install -r SMS-Back-End/microservicio2/requirements.txt')

def obtenerLineasProyecto():
    run('echo \"Para contar las lineas del proyecto\"')
    wc -l `find SMS-Front-End``find SMS-Back-End`
def subirGAE():
    run ('google_appengine/appcfg.py -A studentsmanagementsystem-1124 update sms/')
def actualizarProyecto():
    run ('git pull')
def borrarProyecto():
    run ('rm -rf ./*')
def test_APIBD():
    run ('python SMS-Back-End/microservicio1/APIDB/testUnitario.py')
