"""
PendingState - implementacion concreta de ReservationState.

Representa una reserva recien creada, antes de ser confirmada. Es el
unico estado que permite tres operaciones: confirmar, cancelar o
modificar la reserva. check_in() y board() quedan rechazados por el
comportamiento por defecto de ReservationState.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .reservation_state import ReservationState
from .confirmed_state import ConfirmedState
from .cancelled_state import CancelledState

if TYPE_CHECKING:
    from ..domain.reservation import Reservation


class PendingState(ReservationState):
    """Reserva pendiente: puede confirmarse, cancelarse o modificarse."""

    def confirm(self, reservation: Reservation) -> None:
        reservation.change_state(ConfirmedState())

    def cancel(self, reservation: Reservation) -> None:
        reservation.change_state(CancelledState())

    def modify(self, reservation: Reservation) -> None:
        # Modificar no cambia el estado: sigue pendiente, solo se notifica.
        reservation.notify_observers("Reserva pendiente modificada")