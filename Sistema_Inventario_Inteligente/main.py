"""
Sistema de Inventario Inteligente - Menu interactivo por consola.

Ejecutar con:  python main.py   (o  py main.py  en Windows)
(parado en la carpeta que CONTIENE la carpeta inventory_system/)
"""

import sys

# Arregla textos con tildes/enies que se ven mal en algunas consolas de Windows.
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from inventory_system.config import InventoryConfig
from inventory_system.facade import InventoryFacade
from inventory_system.observers import EmailAlert, InventoryManager, SMSAlert
from inventory_system.repository import InMemoryProductRepository
from inventory_system.strategies import (
    DemandBasedReorderStrategy,
    FixedReorderStrategy,
    SeasonalReorderStrategy,
)
from inventory_system.suppliers import ExternalSupplierAPI, SupplierAdapter


# ---------------------------------------------------------------------------
# Helpers de entrada (validan lo que escribe el usuario)
# ---------------------------------------------------------------------------

def pedir_texto(mensaje: str) -> str:
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("Este campo no puede estar vacio.")


def pedir_entero(mensaje: str, minimo: int = 0) -> int:
    while True:
        valor = input(mensaje).strip()
        try:
            numero = int(valor)
        except ValueError:
            print("Debes ingresar un numero entero.")
            continue
        if numero < minimo:
            print(f"El valor debe ser mayor o igual a {minimo}.")
            continue
        return numero


def pedir_decimal(mensaje: str, minimo: float = 0.0) -> float:
    while True:
        valor = input(mensaje).strip()
        try:
            numero = float(valor)
        except ValueError:
            print("Debes ingresar un numero valido.")
            continue
        if numero < minimo:
            print(f"El valor debe ser mayor o igual a {minimo}.")
            continue
        return numero


def encabezado(texto: str) -> None:
    linea = "=" * 60
    print(f"\n{linea}")
    print(f" {texto}")
    print(linea)


# ---------------------------------------------------------------------------
# Acciones del menu
# ---------------------------------------------------------------------------

def registrar_producto(inventory: InventoryFacade) -> None:
    encabezado("Registrar producto (Factory Method)")
    print("Categorias disponibles: electronica, alimento, ropa")
    tipo = pedir_texto("Categoria: ").lower()

    sku = pedir_texto("SKU: ")
    nombre = pedir_texto("Nombre: ")
    stock = pedir_entero("Stock inicial: ")
    precio = pedir_decimal("Precio: ")

    datos = dict(sku=sku, name=nombre, stock=stock, price=precio)

    if tipo == "electronica":
        datos["warranty_months"] = pedir_entero("Meses de garantia: ")
    elif tipo == "alimento":
        datos["expiration_date"] = pedir_texto("Fecha de vencimiento (AAAA-MM-DD): ")
    elif tipo == "ropa":
        datos["size"] = pedir_texto("Talla: ")
    else:
        print(f"Categoria '{tipo}' no reconocida. No se registro el producto.")
        return

    try:
        producto = inventory.register_product(tipo, **datos)
        print(f"\n[OK] Producto registrado: {producto.sku} - {producto.name} "
              f"({producto.category()}) - stock: {producto.stock}")
    except ValueError as e:
        print(f"Error: {e}")


def ver_productos(inventory: InventoryFacade) -> None:
    encabezado("Productos en inventario")
    productos = inventory._repository.get_all()
    if not productos:
        print("No hay productos registrados todavia.")
        return
    print(f"{'SKU':<8}{'Nombre':<25}{'Categoria':<14}{'Stock':<8}{'Precio'}")
    print("-" * 65)
    for p in productos:
        print(f"{p.sku:<8}{p.name:<25}{p.category():<14}{p.stock:<8}{p.price}")


def monitorear_inventario(inventory: InventoryFacade) -> None:
    encabezado("Monitoreo de inventario (Observer)")
    bajos = inventory.monitor_inventory()
    if bajos:
        print(f"\nProductos con stock bajo: {len(bajos)}")
        for p in bajos:
            print(f"  -> {p.sku} - {p.name} (stock actual: {p.stock})")
    else:
        print("Todos los productos tienen stock suficiente.")


def cambiar_estrategia(inventory: InventoryFacade) -> None:
    encabezado("Cambiar estrategia de reposicion (Strategy)")
    print("1. Fija (cantidad constante)")
    print("2. Por demanda historica")
    print("3. Estacional")
    opcion = pedir_texto("Elige una opcion: ")

    if opcion == "1":
        cantidad = pedir_entero("Cantidad fija a reordenar: ", minimo=1)
        inventory.set_reorder_strategy(FixedReorderStrategy(fixed_quantity=cantidad))
        print("Estrategia activa: Fija")
    elif opcion == "2":
        demanda = pedir_decimal("Demanda diaria promedio: ", minimo=0.1)
        dias = pedir_entero("Dias de cobertura: ", minimo=1)
        inventory.set_reorder_strategy(
            DemandBasedReorderStrategy(avg_daily_demand=demanda, days_of_coverage=dias)
        )
        print("Estrategia activa: Por demanda historica")
    elif opcion == "3":
        base = pedir_entero("Cantidad base: ", minimo=1)
        multiplicador = pedir_decimal("Multiplicador estacional (ej. 1.5): ", minimo=0.1)
        inventory.set_reorder_strategy(
            SeasonalReorderStrategy(base_quantity=base, seasonal_multiplier=multiplicador)
        )
        print("Estrategia activa: Estacional")
    else:
        print("Opcion invalida.")


def reabastecer_producto(inventory: InventoryFacade) -> None:
    encabezado("Reabastecer un producto (Strategy + Adapter)")
    sku = pedir_texto("SKU del producto a reabastecer: ")
    try:
        orden = inventory.trigger_reorder(sku)
        print(f"\n[OK] Orden generada -> proveedor: {orden['supplier']}, "
              f"cantidad: {orden['quantity']}, ETA: {orden['eta_days']} dias")
    except KeyError as e:
        print(f"Error: {e}")


def reabastecer_automatico(inventory: InventoryFacade) -> None:
    encabezado("Reabastecimiento automatico (Observer + Strategy + Adapter)")
    ordenes = inventory.auto_replenish_low_stock()
    if not ordenes:
        print("No hay productos con stock bajo, no se genero ninguna orden.")
        return
    print(f"\n{'SKU':<8}{'Proveedor':<28}{'Cantidad':<12}{'ETA (dias)'}")
    print("-" * 60)
    for orden in ordenes:
        print(f"{orden['sku']:<8}{orden['supplier']:<28}{orden['quantity']:<12}{orden['eta_days']}")


def cambiar_umbral(inventory: InventoryFacade) -> None:
    encabezado("Configurar umbral minimo de stock (Singleton)")
    nuevo_umbral = pedir_entero("Nuevo umbral minimo: ", minimo=0)
    inventory.configure_threshold(nuevo_umbral)
    print(f"Umbral actualizado a {nuevo_umbral} unidades.")


def mostrar_menu() -> None:
    encabezado("SISTEMA DE INVENTARIO INTELIGENTE")
    print("1. Registrar producto")
    print("2. Ver todos los productos")
    print("3. Monitorear inventario (alertas de stock bajo)")
    print("4. Cambiar estrategia de reposicion")
    print("5. Reabastecer un producto especifico")
    print("6. Reabastecimiento automatico (todos los de stock bajo)")
    print("7. Configurar umbral minimo de stock")
    print("0. Salir")


def cargar_datos_demo(inventory: InventoryFacade) -> None:
    """Deja el inventario con datos de ejemplo, para no empezar vacio."""
    inventory.register_product(
        "electronica", sku="E001", name="Audifonos Bluetooth", stock=5, price=120000,
        warranty_months=12,
    )
    inventory.register_product(
        "alimento", sku="A001", name="Arroz 1kg", stock=25, price=4500,
        expiration_date="2026-12-01",
    )
    inventory.register_product(
        "ropa", sku="R001", name="Camiseta Talla M", stock=3, price=35000, size="M",
    )


def main():
    # --- Singleton: configuracion global ---
    config = InventoryConfig.get_instance()
    config.set_min_stock_threshold(10)

    # --- Repository, Observer manager, Adapter y Strategy ---
    repository = InMemoryProductRepository()

    manager = InventoryManager()
    manager.attach(EmailAlert())
    manager.attach(SMSAlert())

    external_api = ExternalSupplierAPI()
    supplier = SupplierAdapter(external_api, vendor_name="ProveedorNacional S.A.S")

    strategy = FixedReorderStrategy(fixed_quantity=50)

    # --- Facade: unico punto de entrada ---
    inventory = InventoryFacade(
        repository=repository,
        manager=manager,
        supplier=supplier,
        default_strategy=strategy,
    )

    cargar_datos_demo(inventory)
    print("Se cargaron 3 productos de ejemplo para que puedas probar el sistema.")

    acciones = {
        "1": registrar_producto,
        "2": ver_productos,
        "3": monitorear_inventario,
        "4": cambiar_estrategia,
        "5": reabastecer_producto,
        "6": reabastecer_automatico,
        "7": cambiar_umbral,
    }

    while True:
        mostrar_menu()
        opcion = input("\nElige una opcion: ").strip()

        if opcion == "0":
            print("\nSaliendo del sistema. Hasta luego.")
            break

        accion = acciones.get(opcion)
        if accion is None:
            print("Opcion invalida, intenta de nuevo.")
            continue

        accion(inventory)


if __name__ == "__main__":
    main()
