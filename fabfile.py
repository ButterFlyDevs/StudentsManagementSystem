from fabric import *

def info_servidor():
    run ('uname -s')

def pararTodo():
    run ('kill -9 $(pidof python google_appengine)')
