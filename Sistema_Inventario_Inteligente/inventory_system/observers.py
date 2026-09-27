"""
Patron OBSERVER -> InventoryManager (sujeto) + EmailAlert / SMSAlert (observadores)

Desacopla la logica de monitoreo de stock de los mecanismos de notificacion:
InventoryManager no sabe (ni le importa) quien esta escuchando, solo notifica
cuando el stock cae por debajo del umbral configurado.
"""

from abc import ABC, abstractmethod
from typing import List

from .config import InventoryConfig
from .products import Product


class StockObserver(ABC):
    @abstractmethod
    def update(self, product: Product) -> None:
        ...


class EmailAlert(StockObserver):
    def update(self, product: Product) -> None:
        print(f"[EMAIL] Alerta: '{product.name}' (sku={product.sku}) "
              f"tiene stock bajo ({product.stock} unidades). Se notifica a compras@empresa.com")


class SMSAlert(StockObserver):
    def update(self, product: Product) -> None:
        print(f"[SMS] Stock bajo de '{product.name}': {product.stock} unidades. "
              f"Enviado al responsable de bodega.")


class InventoryManager:
    """Sujeto (subject) del patron Observer."""

    def __init__(self):
        self._observers: List[StockObserver] = []
        self._config = InventoryConfig.get_instance()

    def attach(self, observer: StockObserver) -> None:
        self._observers.append(observer)

    def detach(self, observer: StockObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify(self, product: Product) -> None:
        for observer in self._observers:
            observer.update(product)

    def check_stock(self, product: Product) -> bool:
        """Retorna True si el stock esta por debajo del umbral y notifica."""
        if product.stock < self._config.min_stock_threshold:
            self._notify(product)
            return True
        return False
