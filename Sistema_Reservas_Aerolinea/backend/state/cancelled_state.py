"""
CancelledState - implementacion concreta de ReservationState.

Representa una reserva cancelada. Es un estado terminal: no sobreescribe
ningun metodo, por lo que confirm(), cancel(), modify(), check_in() y
board() quedan todos rechazados por el comportamiento por defecto de
ReservationState.

Una reserva cancelada no puede volver a confirmarse, ni generar cargos
adicionales, simplemente reintentando alguna operacion sobre ella.
"""

from __future__ import annotations

from .reservation_state import ReservationState


class CancelledState(ReservationState):
    """Reserva cancelada: estado terminal, ninguna operacion esta permitida."""