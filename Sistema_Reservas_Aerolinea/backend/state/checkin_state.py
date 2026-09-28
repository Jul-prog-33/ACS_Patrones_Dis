"""
CheckInState - implementacion concreta de ReservationState.

Representa una reserva a la que ya se le realizo el check-in. Permite
abordar o cancelar (por ejemplo, ante una emergencia de ultima hora).
confirm() y modify() quedan rechazados por el comportamiento por
defecto: los datos de la reserva ya no deberian cambiar en esta etapa.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .reservation_state import ReservationState
from .boarded_state import BoardedState
from .cancelled_state import CancelledState

if TYPE_CHECKING:
    from ..domain.reservation import Reservation


class CheckInState(ReservationState):
    """Reserva con check-in realizado: puede abordar o cancelarse."""

    def board(self, reservation: Reservation) -> None:
        reservation.change_state(BoardedState())

    def cancel(self, reservation: Reservation) -> None:
        reservation.change_state(CancelledState())