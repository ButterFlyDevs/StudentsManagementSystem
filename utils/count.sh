#!/bin/bash

#Copia del fichero que está en .git/hooks/post-commit para que se ejecute tras hacer un commit en la rama develop.

rama="$(git branch | sed -n '/\* /s///p')"
echo -e "RAMA actual" ${rama}

#Para evitar que un commit en cualquier otra rama ejecute el script
if [ "$rama" == "develop" ]
then
    #Leemos el número de commit
    COMMIT="$(git rev-list --count HEAD)"
    #Leemos la fecha
    FECHA="$(date +%Y-%m-%d)"

    #Nos movemos al microservicio sce
    cd SMS-Back-End/sce
    #Leemos todos los ficheros que están en seguimiento, quitamos aquellos con la extensión .png
    #después contamos las lineas de todos y cogemos del resultado la primera columna de la última linea,
    #que tiene el total de lineas.
    # git ls-files  | grep -v '\.png' | xargs wc -l | awk 'END{print $1}
    #Ejecutamos y guardamos en la variable
    LINES_SCE="$(git ls-files  | grep -v '\.png' | xargs wc -l | awk 'END{print $1}')"
    cd ../..

    #Nos movemos al microservicio sbd
    cd SMS-Back-End/sbd
    LINES_SBD="$(git ls-files  | grep -v '\.png' | xargs wc -l | awk 'END{print $1}')"
    cd ../..

    #Nos movemos al microservicio apigateway
    cd SMS-Back-End/apigateway
    LINES_APIG="$(git ls-files  | grep -v '\.png' | xargs wc -l | awk 'END{print $1}')"
    cd ../..

    #Nos movemos al front end (en este caso hay muchos directorios que omitir, de loskits js y css)
    cd SMS-Front-End
    LINES_UI="$(git ls-files  | grep -E -v '\.png|app/out|app/css|app/js|app/fonts' | xargs wc -l | awk 'END{print $1}')"
    cd ..

    #Mostramos el resumen:
    echo -e "Commit: " ${COMMIT}
    echo -e "Fecha: " ${FECHA}
    echo -e "Lineas UI: " ${LINES_UI}
    echo -e "Lineas SCE: " ${LINES_SCE}
    echo -e "Lineas SBD: " ${LINES_SBD}
    echo -e "Lineas APIG: " ${LINES_APIG}

    #Nos cambiamos de rama
    git checkout gh-pages


    puntoComa=';'
    lineaAEscribir=${COMMIT}${puntoComa}${FECHA}${puntoComa}${LINES_UI}${puntoComa}${LINES_APIG}${puntoComa}${LINES_SBD}${puntoComa}${LINES_SCE}
    echo ${lineaAEscribir}
    #ESCRITURA
    echo ${lineaAEscribir} >> lines.txt

    #Commit post ESCRITURA
    git commit -am "Mod lines.txt file for commit "${COMMIT}" ."

    echo -e "Contenido de lines.txt"
    cat lines.txt

    #Volvemos a la rama de desarrollo
    git checkout develop
fi
