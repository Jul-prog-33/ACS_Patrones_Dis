from abc import ABC, abstractmethod
from typing import Optional
from business_domain.entities import Person


class Repositorio_Pacientes(ABC):
    @abstractmethod
    def guardar(self, paciente: Person) -> None:
        pass

    @abstractmethod
    def obtener_por_id(self, id: str) -> Optional[Person]:
        pass

    @abstractmethod
    def actualizar(self, paciente: Person) -> None:
        pass

    @abstractmethod
    def eliminar(self, id: str) -> None:
        pass