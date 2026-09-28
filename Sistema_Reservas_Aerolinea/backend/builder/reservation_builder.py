"""
ReservationBuilder - patron Builder.

Permite construir una Reservation paso a paso, evitando un constructor
telescopico con muchos parametros. Cada set_*() devuelve self (interfaz
fluida, encadenable), y build() valida que los datos minimos existan
antes de devolver el objeto Reservation ya armado y consistente.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..domain.passenger import Passenger
from ..domain.flight import Flight
from ..domain.seat import Seat
from ..domain.payment import Payment
from ..domain.reservation import Reservation
from ..state.pending_state import PendingState
from ..strategy.economy_pricing import EconomyPricing
from ..strategy.premium_pricing import PremiumPricing
from ..strategy.first_class_pricing import FirstClassPricing

if TYPE_CHECKING:
    from ..strategy.pricing_strategy import PricingStrategy


class ReservationBuilder:
    """Ensambla una Reservation paso a paso."""

    def __init__(self) -> None:
        self._passenger: Passenger | None = None
        self._flight: Flight | None = None
        self._seat: Seat | None = None
        self._base_price: float | None = None
        self._additional_services: list[str] = []
        self._preferences: str = ""
        self._payment: Payment | None = None
        self._pricing_strategy: PricingStrategy | None = None

    def set_passenger(self, passenger: Passenger) -> ReservationBuilder:
        self._passenger = passenger
        return self

    def set_flight(self, flight: Flight) -> ReservationBuilder:
        self._flight = flight
        return self

    def set_seat(self, seat: Seat) -> ReservationBuilder:
        self._seat = seat
        return self

    def set_base_price(self, base_price: float) -> ReservationBuilder:
        self._base_price = base_price
        return self

    def add_service(self, service: str) -> ReservationBuilder:
        self._additional_services.append(service)
        return self

    def set_preference(self, preference: str) -> ReservationBuilder:
        self._preferences = preference
        return self

    def set_payment(self, payment: Payment) -> ReservationBuilder:
        self._payment = payment
        return self

    def set_pricing_strategy(self, strategy: PricingStrategy) -> ReservationBuilder:
        """Opcional: si no se llama, build() elige la estrategia segun la clase del asiento."""
        self._pricing_strategy = strategy
        return self

    def build(self) -> Reservation:
        """Valida los datos obligatorios y devuelve la Reservation ya lista."""
        if self._passenger is None:
            raise ValueError("La reserva necesita un pasajero (set_passenger).")
        if self._flight is None:
            raise ValueError("La reserva necesita un vuelo (set_flight).")
        if self._seat is None:
            raise ValueError("La reserva necesita un asiento (set_seat).")
        if self._base_price is None:
            raise ValueError("La reserva necesita un precio base (set_base_price).")

        pricing_strategy = self._pricing_strategy or self._default_strategy_for_seat()

        return Reservation(
            passenger=self._passenger,
            flight=self._flight,
            seat=self._seat,
            base_price=self._base_price,
            pricing_strategy=pricing_strategy,
            state=PendingState(),  # toda reserva nueva nace en estado pendiente
            additional_services=list(self._additional_services),
            preferences=self._preferences,
            payment=self._payment,
        )

    def _default_strategy_for_seat(self) -> PricingStrategy:
        """Si no se fijo una estrategia explicita, se elige segun el tipo de asiento."""
        mapping = {
            "economy": EconomyPricing(),
            "premium": PremiumPricing(),
            "first": FirstClassPricing(),
        }
        return mapping.get(self._seat.class_type, EconomyPricing())