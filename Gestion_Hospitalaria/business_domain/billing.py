from abc import ABC, abstractmethod

class BillingStrategy(ABC):
    @abstractmethod
    def calcular_total(self, monto_base: float, datos_paciente: dict) -> float:
        pass


class Seguro(BillingStrategy):
    def __init__(self, porcentage_cobertura: float):
        self.porcentage_cobertura = porcentage_cobertura

    def calcular_total(self, monto_base: float, datos_paciente: dict) -> float:
        return monto_base * (1 - self.porcentage_cobertura)


class Privado(BillingStrategy):
    def __init__(self, recargo: float):
        self.recargo = recargo

    def calcular_total(self, monto_base: float, datos_paciente: dict) -> float:
        return monto_base + self.recargo


class Acuerdo_Facturacion(BillingStrategy):
    def __init__(self, acuerdo_descuento: float):
        self.acuerdo_descuento = acuerdo_descuento

    def calcular_total(self, monto_base: float, datos_paciente: dict) -> float:
        return monto_base - self.acuerdo_descuento