from persona import Persona

TIPOS_MEDICO = ("Titular", "Interino", "Sustituto")


class Medico(Persona):
    def __init__(self, identificacion, nombres, annio_nac, mes_nac, dia_nac,
                 genero, direccion, codigo_postal, tipo_medico, especialidad,
                 sueldo):
        super().__init__(identificacion, nombres, annio_nac, mes_nac, dia_nac,
                         genero, direccion, codigo_postal)
        if tipo_medico not in TIPOS_MEDICO:
            raise ValueError(f"El tipo debe ser uno de {TIPOS_MEDICO}")
        self.tipo_medico = tipo_medico
        self.especialidad = especialidad
        self.sueldo = sueldo
        self.citas = []
        self.horarios = []

    def calcular_sueldo_annio(self):
        return self.sueldo * 12

    def cantidad_citas(self):
        return len(self.citas)

    def verificar_disponibilidad(self, dia, hora):
        """Devuelve los horarios libres que coinciden con el dia y la hora."""
        return [h for h in self.horarios
                if h.dia == dia and h.hora == hora and h.disponibilidad]
