"""
PricingStrategy - interfaz del patron Strategy.

Define el contrato que debe cumplir cualquier algoritmo de calculo de
precio. Reservation nunca sabe COMO se calcula el precio; solo sabe que
tiene un pricing_strategy y le delega calculate_price(). Esto permite
agregar nuevas estrategias (por ejemplo BusinessPricing) sin tocar
Reservation ni las estrategias ya existentes.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..domain.reservation import Reservation


class PricingStrategy(ABC):
    """Contrato comun para todas las estrategias de calculo de precio."""

    @abstractmethod
    def calculate_price(self, reservation: Reservation) -> float:
        """Calcula el precio final de la reserva dada."""
        raise NotImplementedError