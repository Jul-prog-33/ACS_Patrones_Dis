"""
Patron ADAPTER -> SupplierAdapter envuelve ExternalSupplierAPI

Adapta la interfaz heterogenea de un proveedor externo (que no podemos
modificar) a la interfaz uniforme ISupplierService que el resto del
sistema conoce. Cambiar de proveedor o agregar uno nuevo solo implica un
nuevo Adapter, sin tocar InventoryFacade ni el resto del dominio.
"""

from abc import ABC, abstractmethod


class ExternalSupplierAPI:
    """API externa de un proveedor real, con una interfaz propia que NO
    podemos modificar (llega "de fabrica" asi)."""

    def send_purchase_request(self, product_code: str, units: int, vendor_ref: str) -> dict:
        return {
            "status": "OK",
            "vendor_ref": vendor_ref,
            "product_code": product_code,
            "units_confirmed": units,
            "eta_days": 5,
        }


class ISupplierService(ABC):
    """Interfaz uniforme que el motor de inventario espera consumir."""

    @abstractmethod
    def place_order(self, sku: str, quantity: int) -> dict:
        ...


class SupplierAdapter(ISupplierService):
    def __init__(self, external_api: ExternalSupplierAPI, vendor_name: str):
        self._api = external_api
        self._vendor_name = vendor_name

    def place_order(self, sku: str, quantity: int) -> dict:
        raw_response = self._api.send_purchase_request(
            product_code=sku,
            units=quantity,
            vendor_ref=self._vendor_name,
        )
        return {
            "supplier": self._vendor_name,
            "sku": sku,
            "quantity": raw_response["units_confirmed"],
            "eta_days": raw_response["eta_days"],
        }
