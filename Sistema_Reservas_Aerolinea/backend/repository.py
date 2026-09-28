"""
ReservationRepository - almacenamiento en memoria de reservas.

Separa "donde vive la reserva" de "como se comporta la reserva": el
dominio (Reservation) no sabe si se guarda en memoria, en un archivo o
en una base de datos. Si mañana se cambia a una base de datos real,
solo se reescribe este archivo; ni domain/, ni builder/, ni server.py
se enteran del cambio.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .domain.reservation import Reservation


class ReservationNotFoundError(Exception):
    """Se lanza cuando se busca una reserva que no existe."""


class ReservationRepository:
    """Guarda las reservas en un diccionario en memoria, indexadas por id."""

    def __init__(self) -> None:
        self._reservations: dict[str, Reservation] = {}

    def add(self, reservation: Reservation) -> str:
        """Guarda una reserva nueva y devuelve el id generado."""
        reservation_id = str(uuid.uuid4())
        self._reservations[reservation_id] = reservation
        return reservation_id

    def get(self, reservation_id: str) -> Reservation:
        """Busca una reserva por id o lanza ReservationNotFoundError."""
        try:
            return self._reservations[reservation_id]
        except KeyError:
            raise ReservationNotFoundError(
                f"No existe una reserva con id {reservation_id}."
            ) from None

    def list_all(self) -> dict[str, Reservation]:
        """Devuelve una copia del diccionario completo de reservas."""
        return dict(self._reservations)