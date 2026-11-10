from datetime import date


class Persona:
    """Clase base. De aqui heredan Paciente y Medico."""

    def __init__(self, identificacion, nombres, annio_nac, mes_nac, dia_nac,
                 genero, direccion, codigo_postal):
        self.identificacion = identificacion
        self.nombres = nombres
        # Si la fecha no existe (por ejemplo 31 de febrero) date() lanza ValueError
        date(annio_nac, mes_nac, dia_nac)
        self.annio_nac = annio_nac
        self.mes_nac = mes_nac
        self.dia_nac = dia_nac
        self.genero = genero
        self.direccion = direccion
        self.codigo_postal = codigo_postal

    @property
    def identificacion(self):
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor):
        valor = str(valor).strip()
        if not valor:
            raise ValueError("La identificacion no puede estar vacia")
        self._identificacion = valor

    @property
    def genero(self):
        return self._genero

    @genero.setter
    def genero(self, valor):
        valor = str(valor).strip().upper()
        if valor not in ("M", "F"):
            raise ValueError("El genero debe ser M o F")
        self._genero = valor

    def calcular_edad(self):
        hoy = date.today()
        edad = hoy.year - self.annio_nac
        # Si todavia no ha cumplido este anio, se le resta uno
        if (hoy.month, hoy.day) < (self.mes_nac, self.dia_nac):
            edad -= 1
        return edad

    def es_mayor_edad(self):
        return self.calcular_edad() >= 18

    def cantidad_citas(self):
        # Cada subclase sabe como contar sus citas
        raise NotImplementedError("Debe implementarla la subclase")

    def __str__(self):
        return f"{self.identificacion} - {self.nombres}"
