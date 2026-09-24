class HospitalConfig:
    _instancia = None

    def __init__(self):
        self.instituto_nombre = ""
        self.horario_atencion = ""
        self.politicas = {}

    @staticmethod
    def get_instancia():
        if HospitalConfig._instancia is None:
            HospitalConfig._instancia = HospitalConfig()
        return HospitalConfig._instancia

    def get_policy(self, key: str):
        return self.politicas.get(key)