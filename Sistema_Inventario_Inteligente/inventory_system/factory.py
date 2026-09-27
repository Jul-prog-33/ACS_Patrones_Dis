"""
Patron FACTORY METHOD -> ProductFactory

Centraliza la creacion de instancias de Product segun su tipo, encapsulando
la logica de instanciacion. Agregar una nueva categoria (ej. "congelado")
solo requiere una nueva subclase de Product y una entrada aqui; el codigo
cliente (InventoryFacade) no cambia.
"""

from .products import Product, ElectronicProduct, FoodProduct, ClothingProduct


class ProductFactory:
    _creators = {
        "electronica": ElectronicProduct,
        "alimento": FoodProduct,
        "ropa": ClothingProduct,
    }

    @classmethod
    def create_product(cls, product_type: str, **kwargs) -> Product:
        product_type = product_type.lower()
        creator = cls._creators.get(product_type)
        if creator is None:
            raise ValueError(f"Tipo de producto no soportado: {product_type}")
        return creator(**kwargs)

    @classmethod
    def register_type(cls, name: str, creator_cls) -> None:
        """Permite extender la fabrica en tiempo de ejecucion sin tocar esta clase."""
        cls._creators[name.lower()] = creator_cls
