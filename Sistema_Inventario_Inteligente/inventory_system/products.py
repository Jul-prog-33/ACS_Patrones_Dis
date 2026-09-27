"""
Jerarquia de productos (clase abstracta + subclases concretas).

Product es una CLASE ABSTRACTA: tiene estado y comportamiento concreto
(__init__, __repr__) pero deja category() sin implementar para que cada
subclase la complete. No es una interfaz porque no es puro contrato: ya
trae atributos reales inicializados.
"""

from abc import ABC, abstractmethod


class Product(ABC):
    """Clase base de todos los productos del inventario."""

    def __init__(self, sku: str, name: str, stock: int, price: float):
        self.sku = sku
        self.name = name
        self.stock = stock
        self.price = price

    @abstractmethod
    def category(self) -> str:
        ...

    def __repr__(self):
        return f"<{self.category()} sku={self.sku} name={self.name} stock={self.stock}>"


class ElectronicProduct(Product):
    def __init__(self, sku, name, stock, price, warranty_months: int = 12):
        super().__init__(sku, name, stock, price)
        self.warranty_months = warranty_months

    def category(self) -> str:
        return "Electronica"


class FoodProduct(Product):
    def __init__(self, sku, name, stock, price, expiration_date: str):
        super().__init__(sku, name, stock, price)
        self.expiration_date = expiration_date  # perecedero

    def category(self) -> str:
        return "Alimento"


class ClothingProduct(Product):
    def __init__(self, sku, name, stock, price, size: str):
        super().__init__(sku, name, stock, price)
        self.size = size

    def category(self) -> str:
        return "Ropa"
