import webapp2






class infoProfesor(webapp2.RequestHandler):
    '''
    Devuelve todos los datos de un profesor.
    '''
    def get(self, keywords):
         dni=keywords
         print dni
         #params = extract_params()
         #print params
         self.response.write("profesor x con datos y z")




app = webapp2.WSGIApplication([
    ('/infoProfesor/([^/]+)/?', infoProfesor)
], debug=True)
