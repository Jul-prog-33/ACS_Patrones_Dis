"""
Seat - clase de dominio.

Representa el asiento asignado al pasajero. El atributo class_type
(economy, premium, first) es relevante porque PricingStrategy lo usa
para decidir que estrategia de precio aplicar.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Seat:
    """Datos basicos del asiento asignado a una reserva."""

    number: str
    class_type: str  # "economy" | "premium" | "first"
    available: bool = True

    def to_dict(self) -> dict:
        """Serializa el asiento para enviarlo como JSON desde la API."""
        return {
            "number": self.number,
            "class_type": self.class_type,
            "available": self.available,
        }

    @staticmethod
    def from_dict(data: dict) -> "Seat":
        """Reconstruye un Seat a partir de un diccionario (payload JSON)."""
        return Seat(
            number=data["number"],
            class_type=data["class_type"],
            available=data.get("available", True),
        )