DIAS = ("Lun", "Mar", "Mie", "Jue", "Vie", "Sab")


class Horario:
    def __init__(self, dia, hora, medico, disponibilidad=True):
        if dia not in DIAS:
            raise ValueError(f"El dia debe ser uno de {DIAS}")
        if not 6 <= hora <= 18:
            raise ValueError("La hora debe estar entre 6 y 18")
        self.dia = dia
        self.hora = hora
        self.medico = medico
        self.disponibilidad = disponibilidad

    def __str__(self):
        estado = "libre" if self.disponibilidad else "ocupado"
        return f"{self.dia} {self.hora}:00 ({estado})"
