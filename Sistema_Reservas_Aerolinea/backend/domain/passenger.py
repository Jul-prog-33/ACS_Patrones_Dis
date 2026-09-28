"""
Passenger - clase de dominio.

Representa al pasajero que realiza una reserva. No participa directamente
en ningun patron de diseno (Builder, Strategy, State u Observer); es un
objeto de datos simple que Reservation referencia como atributo.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Passenger:
    """Datos basicos del pasajero asociado a una reserva."""

    id: str
    name: str
    email: str
    phone: str

    def to_dict(self) -> dict:
        """Serializa el pasajero para enviarlo como JSON desde la API."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
        }

    @staticmethod
    def from_dict(data: dict) -> "Passenger":
        """Reconstruye un Passenger a partir de un diccionario (payload JSON)."""
        return Passenger(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
        )