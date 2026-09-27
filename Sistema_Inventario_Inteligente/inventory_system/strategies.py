"""
Patron STRATEGY -> ReorderStrategy y sus variantes

Encapsula los distintos algoritmos de calculo de cantidad a reordenar,
permitiendo cambiar el criterio activo en tiempo de ejecucion sin tocar
InventoryFacade ni el resto del dominio.
"""

from abc import ABC, abstractmethod

from .products import Product


class ReorderStrategy(ABC):
    @abstractmethod
    def calculate_reorder_quantity(self, product: Product) -> int:
        ...


class FixedReorderStrategy(ReorderStrategy):
    """Reorden por una cantidad fija predefinida."""

    def __init__(self, fixed_quantity: int = 50):
        self.fixed_quantity = fixed_quantity

    def calculate_reorder_quantity(self, product: Product) -> int:
        return self.fixed_quantity


class DemandBasedReorderStrategy(ReorderStrategy):
    """Reorden basado en la demanda historica promedio."""

    def __init__(self, avg_daily_demand: float, days_of_coverage: int = 15):
        self.avg_daily_demand = avg_daily_demand
        self.days_of_coverage = days_of_coverage

    def calculate_reorder_quantity(self, product: Product) -> int:
        return int(self.avg_daily_demand * self.days_of_coverage)


class SeasonalReorderStrategy(ReorderStrategy):
    """Reorden ajustado por un multiplicador estacional (ej. diciembre)."""

    def __init__(self, base_quantity: int, seasonal_multiplier: float = 1.0):
        self.base_quantity = base_quantity
        self.seasonal_multiplier = seasonal_multiplier

    def calculate_reorder_quantity(self, product: Product) -> int:
        return int(self.base_quantity * self.seasonal_multiplier)
