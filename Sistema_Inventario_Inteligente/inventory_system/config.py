"""
Patron SINGLETON -> InventoryConfig

Garantiza una unica instancia de configuracion global para todo el sistema
(umbral de stock minimo, moneda, politicas, etc.). Todos los modulos
(productos, monitoreo, reabastecimiento) leen y escriben sobre la MISMA
instancia, evitando configuraciones inconsistentes entre modulos.
"""

from typing import Optional


class InventoryConfig:
    _instance: Optional["InventoryConfig"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.min_stock_threshold = 10
        self.currency = "COP"
        self._initialized = True

    @classmethod
    def get_instance(cls) -> "InventoryConfig":
        return cls()

    def set_min_stock_threshold(self, value: int) -> None:
        if value < 0:
            raise ValueError("El umbral no puede ser negativo")
        self.min_stock_threshold = value
