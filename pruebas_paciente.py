import os
import tempfile
import unittest
from datetime import date

from cita import Cita
from horario import Horario
from medico import Medico
from paciente import Paciente


def nuevo_paciente(identificacion="1098765432", nombres="Laura Gomez"):
    return Paciente(identificacion, nombres, 2000, 5, 17, "F",
                    "Calle 10 # 5-20", "681001", 3, "3101234567")


class PruebasPaciente(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.mkdtemp()
        self.ruta = os.path.join(carpeta, "Paciente.txt")

    def test_guardar_y_buscar(self):
        nuevo_paciente().guardar(self.ruta)
        encontrado = Paciente.buscar("1098765432", self.ruta)
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.nombres, "Laura Gomez")
        self.assertEqual(encontrado.ciudad, "Giron")
        self.assertEqual(encontrado.estrato, 3)

    def test_no_permite_repetidos(self):
        nuevo_paciente().guardar(self.ruta)
        with self.assertRaises(ValueError):
            nuevo_paciente().guardar(self.ruta)

    def test_archivo_inexistente_devuelve_lista_vacia(self):
        self.assertEqual(Paciente.cargar_todos(self.ruta), [])

    def test_varios_pacientes(self):
        nuevo_paciente("1", "Ana").guardar(self.ruta)
        nuevo_paciente("2", "Beto").guardar(self.ruta)
        nuevo_paciente("3", "Carla").guardar(self.ruta)
        self.assertEqual(len(Paciente.cargar_todos(self.ruta)), 3)

    def test_actualizar(self):
        paciente = nuevo_paciente()
        paciente.guardar(self.ruta)
        paciente.telefono = "3209998877"
        paciente.actualizar(self.ruta)
        self.assertEqual(Paciente.buscar("1098765432", self.ruta).telefono,
                         "3209998877")

    def test_eliminar(self):
        nuevo_paciente("1", "Ana").guardar(self.ruta)
        nuevo_paciente("2", "Beto").guardar(self.ruta)
        self.assertTrue(Paciente.eliminar("1", self.ruta))
        self.assertFalse(Paciente.eliminar("1", self.ruta))
        self.assertEqual(len(Paciente.cargar_todos(self.ruta)), 1)

    def test_punto_y_coma_no_rompe_el_formato(self):
        paciente = nuevo_paciente()
        paciente.direccion = "Calle 1; Barrio Centro"
        paciente.guardar(self.ruta)
        self.assertEqual(len(Paciente.cargar_todos(self.ruta)), 1)

    def test_linea_danada_se_ignora(self):
        nuevo_paciente().guardar(self.ruta)
        with open(self.ruta, "a", encoding="utf-8") as f:
            f.write("esto no es un paciente\n")
        self.assertEqual(len(Paciente.cargar_todos(self.ruta)), 1)

    def test_validaciones(self):
        with self.assertRaises(ValueError):
            Paciente("1", "X", 2000, 2, 31, "F", "d", "1", 3, "1")
        with self.assertRaises(ValueError):
            Paciente("1", "X", 2000, 1, 1, "Z", "d", "1", 3, "1")
        with self.assertRaises(ValueError):
            Paciente("1", "X", 2000, 1, 1, "F", "d", "1", 9, "1")

    def test_guarda_el_id_del_medico(self):
        medico = Medico("55", "Dr. Perez", 1980, 1, 1, "M", "d", "1",
                        "Titular", "Odontologia", 5000000)
        paciente = nuevo_paciente()
        paciente.asignar_medico(medico)
        paciente.guardar(self.ruta)
        self.assertEqual(Paciente.buscar("1098765432", self.ruta).medico_id,
                         "55")

    def test_conteo_de_citas(self):
        paciente = nuevo_paciente()
        general = Medico("1", "Dra. Rojas", 1975, 3, 3, "F", "d", "1",
                         "Titular", "Medicina general", 6000000)
        dentista = Medico("2", "Dr. Diaz", 1985, 8, 8, "M", "d", "1",
                          "Interino", "Odontologia", 5000000)
        Cita(general, paciente, fecha=date(2026, 3, 10))
        Cita(general, paciente, fecha=date(2026, 3, 25))
        Cita(dentista, paciente, fecha=date(2026, 7, 2), tipo="Odontologia")
        self.assertEqual(paciente.cantidad_citas(), 3)
        self.assertEqual(paciente.cantidad_citas_por_mes(), {3: 2, 7: 1})
        self.assertEqual(paciente.cantidad_citas_por_esp(),
                         {"Medicina general": 2, "Odontologia": 1})

    def test_edad_y_disponibilidad(self):
        self.assertGreaterEqual(nuevo_paciente().calcular_edad(), 0)
        self.assertTrue(nuevo_paciente().es_mayor_edad())
        medico = Medico("9", "Dr. Luna", 1970, 1, 1, "M", "d", "1",
                        "Sustituto", "Pediatria", 4000000)
        medico.horarios.append(Horario("Lun", 8, medico))
        self.assertEqual(len(medico.verificar_disponibilidad("Lun", 8)), 1)
        self.assertEqual(medico.verificar_disponibilidad("Mar", 8), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
