

class CA_simple:
    def __init__(self, fechaHora,uniforme,rnj,rj,falta,idAlumno,idProfesor,idClase,id_asignatura,key):
        self.fechaHora = fechaHora
        self.uniforme=uniforme
        self.retraso_no_justificado=rnj
        self.retraso_justificado = rj,
        self.falta = falta
        self.idAlumno=idAlumno
        self.idProfesor=idProfesor
        self.idClase=idClase
        self.id_asignatura=id_asignatura
        self.keyNDB = key


class CA_complejo(CA_simple):
    def __init__ (self, fecha,uniforme,rnj,rj,falta,idAlumno,idProfesor,idClase,id_asignatura, nombreAlumno,nombreProfesor,nombreClase,nombreAsignatura):
        CA_simple.__init__(fecha,uniforme,rnj,rj,falta,idAlumno,idProfesor,idClase,id_asignatura)
        self.nombreAlumno = nombreAlumno
        self.nombreProfesor=nombreProfesor
        self.nombreClase=nombreClase
        self.nombreAsignatura=nombreAsignatura

class RCA_simple:
    def __init__(self, listaIdCA,fechaHora,idProfesor,idClase,idAsignatura,key):
        self.listaIdCA=listaIdCA
        self.fechaHora=fechaHora
        self.idProfesor=idProfesor
        self.idClase=idClase
        self.idAsignatura=idAsignatura
        self.keyNDB = key

class RCA_complejo(RCA_simple):
    def __init__ (self, listaIdCA,fechaHora,idProfesor,idClase,idAsignatura,nombreProfesor,nombreClase,nombreAsignatura):
        RCA_simple.__init__(listaIdCA,fechaHora,idProfesor,idClase,idAsignatura)
        self.nombreProfesor=nombreProfesor
        self.nombreClase=nombreClase
        self.nombreAsignatura=nombreAsignatura
