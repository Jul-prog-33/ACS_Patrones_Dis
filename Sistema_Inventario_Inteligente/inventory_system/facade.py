"""
Patron FACADE -> InventoryFacade

Punto de entrada unico que oculta la complejidad de coordinar
ProductFactory, IProductRepository, InventoryManager (Observer),
ReorderStrategy (Strategy) y ISupplierService (Adapter). Los equipos de
operacion/desarrollo solo necesitan conocer esta clase.
"""

from typing import List

from .config import InventoryConfig
from .factory import ProductFactory
from .observers import InventoryManager
from .products import Product
from .repository import IProductRepository
from .strategies import ReorderStrategy
from .suppliers import ISupplierService


class InventoryFacade:
    def __init__(
        self,
        repository: IProductRepository,
        manager: InventoryManager,
        supplier: ISupplierService,
        default_strategy: ReorderStrategy,
    ):
        self._repository = repository
        self._manager = manager
        self._supplier = supplier
        self._strategy = default_strategy
        self._config = InventoryConfig.get_instance()

    def set_reorder_strategy(self, strategy: ReorderStrategy) -> None:
        """Permite cambiar la estrategia de reabastecimiento en tiempo real."""
        self._strategy = strategy

    def configure_threshold(self, min_stock: int) -> None:
        self._config.set_min_stock_threshold(min_stock)

    def register_product(self, product_type: str, **kwargs) -> Product:
        product = ProductFactory.create_product(product_type, **kwargs)
        self._repository.add(product)
        return product

    def monitor_inventory(self) -> List[Product]:
        """Revisa todos los productos y dispara alertas (Observer) si aplica."""
        low_stock_products = []
        for product in self._repository.get_all():
            if self._manager.check_stock(product):
                low_stock_products.append(product)
        return low_stock_products

    def trigger_reorder(self, sku: str) -> dict:
        """Calcula cantidad (Strategy) y coloca la orden (Adapter)."""
        product = self._repository.get(sku)
        if product is None:
            raise KeyError(f"Producto {sku} no encontrado")

        quantity = self._strategy.calculate_reorder_quantity(product)
        order_result = self._supplier.place_order(sku, quantity)

        product.stock += quantity
        self._repository.update(product)
        return order_result

    def auto_replenish_low_stock(self) -> List[dict]:
        """Flujo completo: monitorea, y reordena automaticamente lo que este bajo."""
        results = []
        for product in self.monitor_inventory():
            results.append(self.trigger_reorder(product.sku))
        return results
