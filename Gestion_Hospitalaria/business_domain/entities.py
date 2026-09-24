from abc import ABC, abstractmethod


class Person(ABC):
    def __init__(self, id: str, name: str, role: str):
        self.id = id
        self.name = name
        self.role = role

    @abstractmethod
    def get_info(self) -> str:
        pass


class Doctor(Person):

    def __init__(self, id: str, name: str, especialidad: str):
        super().__init__(id, name, role="doctor")
        self.especialidad = especialidad

    def get_info(self) -> str:
        return f"Doctor {self.name} - Especialidad: {self.especialidad}"


class Paciente(Person):

    def __init__(self, id: str, name: str, tipo_enfermedad: str):
        super().__init__(id, name, role="paciente")
        self.tipo_enfermedad = tipo_enfermedad
        self.historia_clinica = []

    def get_info(self) -> str:
        return f"Paciente {self.name} - Condición: {self.tipo_enfermedad}"


class Administrador(Person):

    def __init__(self, id: str, name: str, area_administrativa: str):
        super().__init__(id, name, role="administrador")
        self.area_administrativa = area_administrativa

    def get_info(self) -> str:
        return f"Administrador {self.name} - Área: {self.area_administrativa}"