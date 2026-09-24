from abc import ABC, abstractmethod


class Servicios_Seguros(ABC):
    @abstractmethod
    def enviar_reclamo(self, dato_reclamo: dict) -> str:
        pass

    @abstractmethod
    def verificar_cobertura(self, patient_id: str) -> bool:
        pass