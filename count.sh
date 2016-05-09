#!/bin/bash

#Contamos las lineas del mServicio apigateway
APIG_lines="$(wc -l SMS-Back-End/apigateway/*.py SMS-Back-End/apigateway/*.txt SMS-Back-End/apigateway/*yaml | grep 'total' | cut -d' ' -f3)"

git checkout gh-pages

echo $APIG_lines >> lines.txt

git commit -am "Prueba de escritura"

git checkout master
