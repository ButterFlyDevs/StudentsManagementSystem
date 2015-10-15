# -*- coding: utf-8 -*-
from webtest import TestApp
import unittest
import main

app = TestApp(main.application)

'''
Cada una de las clases será un test que tendrá que pasar la ejecución.
Ejecución:
> nosetests --with-gae --gae-lib-root ../google_appengine
(Siempre que estemos dentro del directorio de la app)

Más información en: https://github.com/Trii/NoseGAE

Simplificado:

> ./runTest.sh

'''

class HelloWorldTest(unittest.TestCase):
    def test_index(self):
        """Tests that the index page for the application

        The page should be served as: Content-Type: text/plain
        The body content should contain the string: Hello world!
        """
        response = app.get('/hello')
        self.assertEqual(response.content_type, 'text/plain')
        self.assertIn('Hello Testing World!', response.body)
