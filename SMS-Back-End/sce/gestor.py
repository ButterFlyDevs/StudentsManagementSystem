from NDBlib import EstructurasNDB.ControlAsistencia
from NDBlib import EstructurasNDB.Resumen_ControlAsistencia
from NDBlib import EstructurasNDB.Alumnos_NombreID
from NDBlib import EstructurasNDB.Profesores_NombreID
from NDBlib import EstructurasNDB.Clases_NombreID
from NDBlib import EstructurasNDB.Asignaturas_NombreID
import Estructuras


class Gestor(self):

    @classmethod
    def obtenerALLCA():
        listaCA = []
        listaCA = ControlAsistencia.devolver_todo().fetch(100000)
        
    @classmethod
    def obtenerControlAsistencia(id):
        pass

    @classmethod
    def obtenerResumenControlAsistencia(idProfesor,idASignatura,idClase,fechaHora):
'''
Debe devolver también nombres (DEBE DEVOLVER UN RCA_complejo)
'''
        pass

    @classmethod
    def insertarControlAsistencia(fechaHora,uniforme,rnj,rj,falta,idAlumno,idProfesor,idClase,idASignatura):

        nuevoCA = ControlAsistencia(fecha_hora = fechaHora,uniforme = uniforme,retraso_no_justificado =rnj ,retraso_justificado =rj ,falta = falta,id_alumno = idAlumno, id_profesor = idProfesor,id_clase =idClase , id_asignatura =idAsignatura)
        nuevoCA_clave = nuevoCA.put()

    @classmethod
    def insertarResumenControlAsistencia(listaIdCA,fechaHora,idProfesor,idASignatura,idClase):
        pass

    @classmethod
    def obtenerNombreAlumnos(idAlumnos):
        pass

    @classmethod
    def obtenerNombreProfesores(idProfesor):
        pass

    @classmethod
    def obtenerNombreClases(idClase):
        pass

    @classmethod
    def obtenerNombreAsignaturas(idAsignatura):
        pass
