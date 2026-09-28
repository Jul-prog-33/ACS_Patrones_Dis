"""
ReservationObserver - interfaz del patron Observer.

Define el contrato que debe cumplir cualquier objeto que quiera enterarse
de los cambios de una Reservation (confirmacion, cancelacion, cambios de
estado en general). Reservation nunca sabe COMO se envia la notificacion
(correo, SMS, push); solo sabe que tiene una lista de observers y les
llama update() cuando ocurre un evento.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..domain.reservation import Reservation


class ReservationObserver(ABC):
    """Contrato comun para todos los canales de notificacion."""

    @abstractmethod
    def update(self, event: str, reservation: Reservation) -> None:
        """Se invoca cuando ocurre un evento relevante sobre la reserva."""
        raise NotImplementedError