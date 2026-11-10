import os
from persona import Persona


class Paciente(Persona):
    """Paciente del centro de salud.

    Cada paciente se guarda como una linea en Paciente.txt, con los campos
    separados por punto y coma. La identificacion funciona como llave unica.
    """

    ARCHIVO = "Paciente.txt"
    SEPARADOR = ";"
    CAMPOS = ("identificacion", "nombres", "annio_nac", "mes_nac", "dia_nac",
              "genero", "direccion", "codigo_postal", "estrato", "ciudad",
              "telefono", "medico_id")

    def __init__(self, identificacion, nombres, annio_nac, mes_nac, dia_nac,
                 genero, direccion, codigo_postal, estrato, telefono,
                 ciudad="Giron", medico=None):
        super().__init__(identificacion, nombres, annio_nac, mes_nac, dia_nac,
                         genero, direccion, codigo_postal)
        self.estrato = estrato
        self.ciudad = ciudad
        self.telefono = telefono
        self.citas = []
        self.medico = medico
        self._medico_id = ""

    @property
    def estrato(self):
        return self._estrato

    @estrato.setter
    def estrato(self, valor):
        valor = int(valor)
        if not 1 <= valor <= 6:
            raise ValueError("El estrato debe estar entre 1 y 6")
        self._estrato = valor

    @property
    def medico_id(self):
        # Si hay un objeto Medico se usa su identificacion; si el paciente
        # viene del archivo, solo tenemos el id guardado
        if self.medico is not None:
            return self.medico.identificacion
        return self._medico_id

    def asignar_medico(self, medico):
        self.medico = medico
        self._medico_id = medico.identificacion

    # ---------- metodos del diagrama ----------

    def cantidad_citas(self):
        return len(self.citas)

    def cantidad_citas_por_mes(self):
        """Devuelve un diccionario {mes: cantidad}."""
        conteo = {}
        for cita in self.citas:
            conteo[cita.fecha.month] = conteo.get(cita.fecha.month, 0) + 1
        return dict(sorted(conteo.items()))

    def cantidad_citas_por_esp(self):
        """Devuelve un diccionario {especialidad: cantidad}."""
        conteo = {}
        for cita in self.citas:
            esp = cita.medico.especialidad
            conteo[esp] = conteo.get(esp, 0) + 1
        return conteo

    # ---------- manejo del archivo Paciente.txt ----------

    @staticmethod
    def _limpiar(texto):
        # Un ; o un salto de linea dentro de un dato dañaria el formato
        return str(texto).replace(";", ",").replace("\n", " ").strip()

    def _a_linea(self):
        valores = (self.identificacion, self.nombres, self.annio_nac,
                   self.mes_nac, self.dia_nac, self.genero, self.direccion,
                   self.codigo_postal, self.estrato, self.ciudad,
                   self.telefono, self.medico_id)
        return self.SEPARADOR.join(self._limpiar(v) for v in valores)

    @classmethod
    def _desde_linea(cls, linea):
        partes = linea.rstrip("\n").split(cls.SEPARADOR)
        if len(partes) != len(cls.CAMPOS):
            raise ValueError("La linea no tiene el numero de campos esperado")
        d = dict(zip(cls.CAMPOS, partes))
        paciente = cls(d["identificacion"], d["nombres"], int(d["annio_nac"]),
                       int(d["mes_nac"]), int(d["dia_nac"]), d["genero"],
                       d["direccion"], d["codigo_postal"], d["estrato"],
                       d["telefono"], ciudad=d["ciudad"])
        paciente._medico_id = d["medico_id"]
        return paciente

    @classmethod
    def cargar_todos(cls, ruta=None):
        """Lee el archivo y devuelve la lista de pacientes.

        Si el archivo todavia no existe devuelve una lista vacia. Las lineas
        dañadas se saltan y se avisa por pantalla.
        """
        ruta = ruta or cls.ARCHIVO
        pacientes = []
        if not os.path.exists(ruta):
            return pacientes
        with open(ruta, "r", encoding="utf-8") as archivo:
            for numero, linea in enumerate(archivo, start=1):
                if not linea.strip():
                    continue
                try:
                    pacientes.append(cls._desde_linea(linea))
                except (ValueError, TypeError) as error:
                    print(f"Linea {numero} ignorada en {ruta}: {error}")
        return pacientes

    @classmethod
    def buscar(cls, identificacion, ruta=None):
        identificacion = str(identificacion).strip()
        for paciente in cls.cargar_todos(ruta):
            if paciente.identificacion == identificacion:
                return paciente
        return None

    @classmethod
    def _escribir_todos(cls, pacientes, ruta):
        with open(ruta, "w", encoding="utf-8") as archivo:
            for p in pacientes:
                archivo.write(p._a_linea() + "\n")

    def guardar(self, ruta=None):
        """Agrega el paciente al final del archivo. No permite repetidos."""
        ruta = ruta or self.ARCHIVO
        if Paciente.buscar(self.identificacion, ruta) is not None:
            raise ValueError(
                f"Ya existe un paciente con identificacion {self.identificacion}")
        with open(ruta, "a", encoding="utf-8") as archivo:
            archivo.write(self._a_linea() + "\n")

    def actualizar(self, ruta=None):
        """Reemplaza en el archivo la linea de este paciente."""
        ruta = ruta or self.ARCHIVO
        pacientes = Paciente.cargar_todos(ruta)
        for i, p in enumerate(pacientes):
            if p.identificacion == self.identificacion:
                pacientes[i] = self
                Paciente._escribir_todos(pacientes, ruta)
                return
        raise ValueError(f"No existe el paciente {self.identificacion}")

    @classmethod
    def eliminar(cls, identificacion, ruta=None):
        """Borra al paciente del archivo. Devuelve True si lo encontro."""
        ruta = ruta or cls.ARCHIVO
        identificacion = str(identificacion).strip()
        pacientes = cls.cargar_todos(ruta)
        restantes = [p for p in pacientes if p.identificacion != identificacion]
        if len(restantes) == len(pacientes):
            return False
        cls._escribir_todos(restantes, ruta)
        return True

    def __str__(self):
        return (f"{self.identificacion} | {self.nombres} | "
                f"{self.calcular_edad()} annos | estrato {self.estrato} | "
                f"{self.ciudad} | tel. {self.telefono}")
