"""
BoardedState - implementacion concreta de ReservationState.

Representa una reserva cuyo pasajero ya abordo el vuelo. Es un estado
terminal del flujo normal: no sobreescribe ningun metodo, por lo que
confirm(), cancel(), modify(), check_in() y board() quedan todos
rechazados por el comportamiento por defecto de ReservationState.

No tiene sentido, por ejemplo, cancelar o modificar una reserva cuyo
pasajero ya esta en el avion.
"""

from __future__ import annotations

from .reservation_state import ReservationState


class BoardedState(ReservationState):
    """Reserva abordada: estado terminal, ninguna operacion esta permitida."""