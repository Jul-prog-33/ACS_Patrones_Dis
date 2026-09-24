class ExternalInsuranceAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def verificacion(self, seguro_id: str) -> dict:
        return {"seguro_id": seguro_id, "cubierto": True}

    def enviar_peticion(self, payload: dict) -> dict:
        return {"status": "aceptado", "payload": payload}