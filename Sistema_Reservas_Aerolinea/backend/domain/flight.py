"""
Flight - clase de dominio.

Representa el vuelo que esta siendo reservado. Al igual que Passenger,
no participa en ningun patron de diseno; es un objeto de datos simple
que Reservation referencia como atributo.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Flight:
    """Datos basicos del vuelo asociado a una reserva."""

    flight_number: str
    origin: str
    destination: str
    departure: str  # ISO 8601, ej: "2026-10-15T08:30:00"
    arrival: str     # ISO 8601, ej: "2026-10-15T11:45:00"

    def to_dict(self) -> dict:
        """Serializa el vuelo para enviarlo como JSON desde la API."""
        return {
            "flight_number": self.flight_number,
            "origin": self.origin,
            "destination": self.destination,
            "departure": self.departure,
            "arrival": self.arrival,
        }

    @staticmethod
    def from_dict(data: dict) -> "Flight":
        """Reconstruye un Flight a partir de un diccionario (payload JSON)."""
        return Flight(
            flight_number=data["flight_number"],
            origin=data["origin"],
            destination=data["destination"],
            departure=data["departure"],
            arrival=data["arrival"],
        )