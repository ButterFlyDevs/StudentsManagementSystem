from NDBlib import EstructurasNDB.ControlAsistencia
import Estructuras


class Gestor(self):

    @classmethod
    def obtenerControlAsistencia(id):
        pass

    @classmethod
    def obtenerResumenControlAsistencia(idProfesor,idASignatura,idClase,fechaHora):
        pass

    @classmethod
    def insertarControlAsistencia(fechaHora,uniforme,rnj,rj,falta,idAlumno,idProfesor,idClase,idASignatura):
        pass

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
