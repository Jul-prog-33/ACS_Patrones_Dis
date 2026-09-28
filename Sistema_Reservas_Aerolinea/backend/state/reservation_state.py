"""
ReservationState - base del patron State.

Define el comportamiento que depende del estado en el que se encuentre
una Reservation. Cada estado concreto (PendingState, ConfirmedState,
CancelledState, CheckInState, BoardedState) sobreescribe unicamente las
operaciones que tiene permitidas; el resto conserva el comportamiento
por defecto de esta clase, que rechaza la operacion con un mensaje claro.

Gracias a esto, Reservation nunca necesita un if/elif del tipo
"if self.status == 'pending': ..." para saber que esta permitido: toda
esa logica queda repartida entre las subclases de estado.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..domain.reservation import Reservation


class InvalidTransitionError(Exception):
    """Se lanza cuando se intenta una operacion no valida para el estado actual."""


class ReservationState:
    """Comportamiento por defecto: ninguna operacion esta permitida.

    No se declara como ABC con @abstractmethod a proposito: a diferencia
    de PricingStrategy (donde SIEMPRE hay que calcular un precio), aqui
    cada estado solo habilita un subconjunto de operaciones, asi que un
    rechazo por defecto evita repetir "raise" en cada subclase.
    """

    def confirm(self, reservation: Reservation) -> None:
        self._reject("confirmar")

    def cancel(self, reservation: Reservation) -> None:
        self._reject("cancelar")

    def modify(self, reservation: Reservation) -> None:
        self._reject("modificar")

    def check_in(self, reservation: Reservation) -> None:
        self._reject("hacer check-in de")

    def board(self, reservation: Reservation) -> None:
        self._reject("abordar")

    def _reject(self, action: str) -> None:
        raise InvalidTransitionError(
            f"No se puede {action} una reserva en estado {type(self).__name__}."
        )