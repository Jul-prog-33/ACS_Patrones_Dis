"""
Reservation - clase de dominio central.

Es la unica clase que conoce a los cuatro patrones:
- Builder    (ReservationBuilder) la construye paso a paso.
- Strategy   (PricingStrategy)    calcula su precio.
- State      (ReservationState)   controla que operaciones son validas.
- Observer   (ReservationObserver) recibe notificaciones de sus cambios.

Reservation nunca usa if/elif para decidir su comportamiento segun el
estado: siempre delega en self.state, que es quien realmente sabe que
esta permitido en cada momento del ciclo de vida.
"""

from __future__ import annotations
from dataclasses import dataclass, field

from .passenger import Passenger
from .flight import Flight
from .seat import Seat
from .payment import Payment

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Solo se importan para el chequeo de tipos: evita import circular,
    # porque estas clases (a su vez) reciben un Reservation como parametro.
    from ..state.reservation_state import ReservationState
    from ..strategy.pricing_strategy import PricingStrategy
    from ..observer.reservation_observer import ReservationObserver


@dataclass
class Reservation:
    """Representa una reserva concreta realizada por un pasajero."""

    passenger: Passenger
    flight: Flight
    seat: Seat
    base_price: float
    pricing_strategy: PricingStrategy
    state: ReservationState
    additional_services: list[str] = field(default_factory=list)
    preferences: str = ""
    payment: Payment | None = None
    observers: list[ReservationObserver] = field(default_factory=list)

    # ---------- State: la reserva delega, nunca decide con if/elif ----------
    def confirm(self) -> None:
        self.state.confirm(self)

    def cancel(self) -> None:
        self.state.cancel(self)

    def modify(self) -> None:
        self.state.modify(self)

    def check_in(self) -> None:
        self.state.check_in(self)

    def board(self) -> None:
        self.state.board(self)

    def change_state(self, new_state: ReservationState) -> None:
        """Llamado por las propias clases State para hacer la transicion."""
        old_state = type(self.state).__name__
        self.state = new_state
        self.notify_observers(
            f"Estado cambiado de {old_state} a {type(new_state).__name__}"
        )

    # ---------- Strategy ----------
    def calculate_price(self) -> float:
        return self.pricing_strategy.calculate_price(self)

    # ---------- Observer ----------
    def add_observer(self, observer: ReservationObserver) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: ReservationObserver) -> None:
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, event: str) -> None:
        for observer in self.observers:
            observer.update(event, self)

    # ---------- Serializacion para la API ----------
    def to_dict(self) -> dict:
        return {
            "passenger": self.passenger.to_dict(),
            "flight": self.flight.to_dict(),
            "seat": self.seat.to_dict(),
            "base_price": self.base_price,
            "additional_services": self.additional_services,
            "preferences": self.preferences,
            "payment": self.payment.to_dict() if self.payment else None,
            "state": type(self.state).__name__,
            "pricing_strategy": type(self.pricing_strategy).__name__,
            "current_price": self.calculate_price(),
        }