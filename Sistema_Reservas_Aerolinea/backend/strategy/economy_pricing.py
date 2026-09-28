"""
EconomyPricing - implementacion concreta de PricingStrategy.

Aplica las reglas de tarifa de clase economica: el precio base sin
recargo por clase, mas un cargo fijo por cada servicio adicional
contratado (equipaje extra, comida, etc.).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .pricing_strategy import PricingStrategy

if TYPE_CHECKING:
    from ..domain.reservation import Reservation

SERVICE_FEE = 15.0  # cargo fijo por cada servicio adicional


class EconomyPricing(PricingStrategy):
    """Precio = precio base + cargo fijo por cada servicio adicional."""

    def calculate_price(self, reservation: Reservation) -> float:
        services_cost = len(reservation.additional_services) * SERVICE_FEE
        return reservation.base_price + services_cost