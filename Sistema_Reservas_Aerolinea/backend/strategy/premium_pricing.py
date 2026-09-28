"""
PremiumPricing - implementacion concreta de PricingStrategy.

Aplica las reglas de tarifa de clase premium: un recargo sobre el
precio base, mas el mismo cargo fijo por servicio adicional que
EconomyPricing.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .pricing_strategy import PricingStrategy

if TYPE_CHECKING:
    from ..domain.reservation import Reservation

SERVICE_FEE = 15.0       # cargo fijo por cada servicio adicional
PREMIUM_MULTIPLIER = 1.4  # 40% de recargo sobre el precio base


class PremiumPricing(PricingStrategy):
    """Precio = (precio base * 1.4) + cargo fijo por cada servicio adicional."""

    def calculate_price(self, reservation: Reservation) -> float:
        services_cost = len(reservation.additional_services) * SERVICE_FEE
        return (reservation.base_price * PREMIUM_MULTIPLIER) + services_cost