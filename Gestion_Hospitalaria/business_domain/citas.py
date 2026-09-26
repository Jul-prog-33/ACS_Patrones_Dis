class Cita:
    def __init__(self, id: str, paciente_id: str, doctor_id: str, fecha: str, hora: str):
        self.id = id
        self.paciente_id = paciente_id
        self.doctor_id = doctor_id
        self.fecha = fecha
        self.hora = hora