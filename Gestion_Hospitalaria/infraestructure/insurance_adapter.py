from interfaces.servicios_seguros import Servicios_Seguros
from infraestructure.external_insurance_api import ExternalInsuranceAPI


class InsuranceAdapter(Servicios_Seguros):
    def __init__(self, externa_api: ExternalInsuranceAPI):
        self.externa_api = externa_api

    def verificar_cobertura(self, patient_id: str) -> bool:
        resultado = self.externa_api.verificacion(patient_id)
        return resultado["cubierto"]

    def enviar_reclamo(self, dato_reclamo: dict) -> str:
        resultado = self.externa_api.enviar_peticion(dato_reclamo)
        return resultado["status"]