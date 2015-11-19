Tenemos que añadir la librería nosetest dentro de la carpeta de SMM para que travis no de el error de

$ smm/nosetests --with-gae --gae-lib-root ../google_appengine
/home/travis/build.sh: line 45: smm/nosetests: No such file or directory
The command "smm/nosetests --with-gae --gae-lib-root ../google_appengine" exited with 127.

Y otras dos más, para que el entorno en travis esté listo:
#dependencias requeridas:
install:
  - sudo pip install nosegae
  - sudo pip install webtest
  - sudo pip install MySQL-python
