from typing import Optional
from interfaces.repositorio_pacientes import Repositorio_Pacientes
from business_domain.entities import Person


class Repositorio_pacientes(Repositorio_Pacientes):
    def __init__(self):
        self.storage = {}

    def guardar(self, paciente: Person) -> None:
        self.storage[paciente.id] = paciente

    def obtener_por_id(self, id: str) -> Optional[Person]:
        return self.storage.get(id)
    
    def actualizar(self, paciente: Person) -> None:
        self.storage[paciente.id] = paciente

    def eliminar(self, id: str) -> None:
        del self.storage[id]