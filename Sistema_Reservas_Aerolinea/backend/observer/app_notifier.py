"""
AppNotifier - implementacion concreta de ReservationObserver.

Notifica los eventos de una Reservation mediante la aplicacion movil
(push notification). Igual que EmailNotifier y SMSNotifier, deja un
punto unico (_send) donde conectar un proveedor real (Firebase Cloud
Messaging, APNs, etc.) sin tocar el resto del sistema.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .reservation_observer import ReservationObserver

if TYPE_CHECKING:
    from ..domain.reservation import Reservation


class AppNotifier(ReservationObserver):
    """Envia una notificacion push a la aplicacion movil ante cada evento."""

    def update(self, event: str, reservation: Reservation) -> None:
        destinatario = reservation.passenger.id
        mensaje = f"[Push a usuario {destinatario}] {event}"
        self._send(destinatario, mensaje)

    def _send(self, destinatario: str, mensaje: str) -> None:
        # Punto unico de integracion con un proveedor push real
        # (Firebase Cloud Messaging, APNs, etc.). Por ahora solo se
        # imprime en consola.
        print(mensaje)