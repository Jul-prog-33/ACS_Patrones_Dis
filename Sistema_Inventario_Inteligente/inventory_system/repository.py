"""
Patron REPOSITORY -> InMemoryProductRepository

Abstrae el acceso a los datos de productos detras de una interfaz CRUD
estable. Hoy vive en memoria; manana puede respaldarse en una base de
datos relacional o un ERP sin que InventoryFacade ni ningun otro modulo
cambien una sola linea.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from .products import Product


class IProductRepository(ABC):
    @abstractmethod
    def add(self, product: Product) -> None: ...

    @abstractmethod
    def get(self, sku: str) -> Optional[Product]: ...

    @abstractmethod
    def get_all(self) -> List[Product]: ...

    @abstractmethod
    def update(self, product: Product) -> None: ...

    @abstractmethod
    def delete(self, sku: str) -> None: ...


class InMemoryProductRepository(IProductRepository):
    def __init__(self):
        self._products: Dict[str, Product] = {}

    def add(self, product: Product) -> None:
        self._products[product.sku] = product

    def get(self, sku: str) -> Optional[Product]:
        return self._products.get(sku)

    def get_all(self) -> List[Product]:
        return list(self._products.values())

    def update(self, product: Product) -> None:
        if product.sku not in self._products:
            raise KeyError(f"Producto {product.sku} no existe")
        self._products[product.sku] = product

    def delete(self, sku: str) -> None:
        self._products.pop(sku, None)
