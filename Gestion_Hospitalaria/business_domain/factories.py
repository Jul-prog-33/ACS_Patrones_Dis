from abc import ABC, abstractmethod
from business_domain.entities import Person, Doctor, Paciente, Administrador


class PersonFactory(ABC):
    @abstractmethod
    def crear_persona(self, datos: dict) -> Person:
        pass


class DoctorFactory(PersonFactory):
    def crear_persona(self, datos: dict) -> Person:
        return Doctor(datos["id"], datos["name"], datos["especialidad"])


class PacienteFactory(PersonFactory):
    def crear_persona(self, datos: dict) -> Person:
        return Paciente(datos["id"], datos["name"], datos["tipo_enfermedad"])


class AdministradorFactory(PersonFactory):
    def crear_persona(self, datos: dict) -> Person:
        return Administrador(datos["id"], datos["name"], datos["area_administrativa"])