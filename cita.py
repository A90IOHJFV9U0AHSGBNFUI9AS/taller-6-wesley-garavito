from datetime import date, datetime

TIPOS_CITA = ("General", "Odontologia", "Especialista")


class Cita:
    def __init__(self, medico, paciente, fecha=None, hora=None,
                 tipo="General", num_consultorio="NA"):
        if tipo not in TIPOS_CITA:
            raise ValueError(f"El tipo debe ser uno de {TIPOS_CITA}")
        self.medico = medico
        self.paciente = paciente
        self.fecha = fecha or date.today()
        self.hora = hora or datetime.now().time()
        self.tipo = tipo
        self.num_consultorio = num_consultorio
        # La cita queda registrada en las dos listas
        medico.citas.append(self)
        paciente.citas.append(self)

    def consultar_medico(self):
        return self.medico

    def consultar_paciente(self):
        return self.paciente
