"""
SMSNotifier - implementacion concreta de ReservationObserver.

Notifica los eventos de una Reservation por SMS. Igual que EmailNotifier,
deja un punto unico (_send) donde conectar un proveedor real (Twilio,
etc.) sin tocar el resto del sistema.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .reservation_observer import ReservationObserver

if TYPE_CHECKING:
    from ..domain.reservation import Reservation


class SMSNotifier(ReservationObserver):
    """Envia una notificacion por SMS ante cada evento."""

    def update(self, event: str, reservation: Reservation) -> None:
        destinatario = reservation.passenger.phone
        mensaje = f"[SMS a {destinatario}] {event}"
        self._send(destinatario, mensaje)

    def _send(self, destinatario: str, mensaje: str) -> None:
        # Punto unico de integracion con un proveedor de SMS real
        # (Twilio, etc.). Por ahora solo se imprime en consola.
        print(mensaje)