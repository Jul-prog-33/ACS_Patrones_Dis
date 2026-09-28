"""
ConfirmedState - implementacion concreta de ReservationState.

Representa una reserva ya confirmada por el pasajero. Permite cancelar,
pasar a check-in o modificarla. confirm() queda rechazado por el
comportamiento por defecto: no tiene sentido confirmar una reserva que
ya esta confirmada.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .reservation_state import ReservationState
from .checkin_state import CheckInState
from .cancelled_state import CancelledState

if TYPE_CHECKING:
    from ..domain.reservation import Reservation


class ConfirmedState(ReservationState):
    """Reserva confirmada: puede cancelarse, pasar a check-in o modificarse."""

    def cancel(self, reservation: Reservation) -> None:
        reservation.change_state(CancelledState())

    def check_in(self, reservation: Reservation) -> None:
        reservation.change_state(CheckInState())

    def modify(self, reservation: Reservation) -> None:
        reservation.notify_observers("Reserva confirmada modificada")