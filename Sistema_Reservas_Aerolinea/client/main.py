"""
main.py - menu de consola (interfaz del cliente).

Este archivo solo se ocupa de la interaccion con el usuario: pedir datos,
mostrar resultados y elegir que operacion ejecutar. No contiene reglas de
negocio (viven en el servidor, en los patrones) ni sabe nada de HTTP
(vive en api_client.py). Cada capa tiene una unica responsabilidad.

Ejecutar desde la raiz del proyecto, con el servidor ya corriendo:
    python -m client.main
"""

from __future__ import annotations

import re
import uuid
from datetime import datetime

from .api_client import ApiError, ReservationApiClient

SEAT_CLASSES = {"1": "economy", "2": "premium", "3": "first"}
PAYMENT_METHODS = {"1": "credit_card", "2": "debit_card", "3": "transfer"}
CHANNELS = {"1": "email", "2": "sms", "3": "app"}

MENU = """
==================== SISTEMA DE RESERVAS ====================
  1. Crear reserva (paso a paso)
  2. Crear reserva de ejemplo (rapido)
  3. Listar reservas
  4. Ver precio de una reserva
  5. Confirmar reserva
  6. Modificar reserva
  7. Hacer check-in
  8. Abordar
  9. Cancelar reserva
 10. Suscribir notificador (email / sms / app)
  0. Salir
=============================================================
"""


# ---------------------------------------------------------------- entrada
def ask(prompt: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default is not None else ""
    while True:
        value = input(f"{prompt}{suffix}: ").strip()
        if value:
            return value
        if default is not None:
            return default
        print("  Este campo es obligatorio.")


def parse_amount(raw: str) -> float:
    """Interpreta montos escritos en formato colombiano o internacional.

    200.000 -> 200000 | 1.200.000,50 -> 1200000.5 | 200,000 -> 200000
    250.50  -> 250.5  | 200,50 -> 200.5           | 200000  -> 200000
    """
    text = raw.strip().replace(" ", "")
    if re.fullmatch(r"\d{1,3}(\.\d{3})+(,\d+)?", text):    # puntos = miles
        text = text.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"\d{1,3}(,\d{3})+(\.\d+)?", text):  # comas = miles
        text = text.replace(",", "")
    else:
        text = text.replace(",", ".")
    return float(text)


def ask_float(prompt: str) -> float:
    while True:
        try:
            return parse_amount(ask(prompt))
        except ValueError:
            print("  Escribe un numero valido (ej: 200000 o 200.000).")


def ask_choice(prompt: str, options: dict[str, str]) -> str:
    listing = ", ".join(f"{key}={value}" for key, value in options.items())
    while True:
        key = input(f"{prompt} ({listing}): ").strip()
        if key in options:
            return options[key]
        print("  Opcion invalida.")


# ---------------------------------------------------------------- salida
def print_reservation(r: dict) -> None:
    passenger, flight, seat = r["passenger"], r["flight"], r["seat"]
    services = ", ".join(r["additional_services"]) or "ninguno"
    print(f"\n  Reserva {r['id'][:8]}")
    print(f"    Pasajero : {passenger['name']} ({passenger['email']})")
    print(f"    Vuelo    : {flight['flight_number']}  {flight['origin']} -> {flight['destination']}")
    print(f"    Asiento  : {seat['number']} ({seat['class_type']})")
    print(f"    Servicios: {services}")
    print(f"    Estado   : {r['state']}")
    print(f"    Estrategia de precio: {r['pricing_strategy']}")
    print(f"    Precio base: {r['base_price']:,.2f}  ->  Precio actual: {r['current_price']:,.2f}")


def choose_reservation(client: ReservationApiClient) -> str | None:
    """Muestra las reservas numeradas y devuelve el id de la elegida."""
    reservations = client.list_reservations()
    if not reservations:
        print("\n  No hay reservas todavia. Crea una primero (opcion 1 o 2).")
        return None
    print()
    for number, r in enumerate(reservations, start=1):
        print(f"  {number}. {r['id'][:8]} | {r['passenger']['name']} | "
              f"{r['flight']['flight_number']} | {r['state']}")
    while True:
        raw = input("Numero de reserva (Enter para volver): ").strip()
        if raw == "":
            return None
        if raw.isdigit() and 1 <= int(raw) <= len(reservations):
            return reservations[int(raw) - 1]["id"]
        print("  Numero invalido.")


# ---------------------------------------------------------------- acciones
def create_reservation(client: ReservationApiClient) -> None:
    print("\n-- Pasajero --")
    passenger = {
        "id": ask("Documento/ID"),
        "name": ask("Nombre"),
        "email": ask("Email"),
        "phone": ask("Telefono"),
    }
    print("\n-- Vuelo --")
    flight = {
        "flight_number": ask("Numero de vuelo"),
        "origin": ask("Origen"),
        "destination": ask("Destino"),
        "departure": ask("Salida (ISO)", "2026-10-15T08:30:00"),
        "arrival": ask("Llegada (ISO)", "2026-10-15T09:35:00"),
    }
    print("\n-- Asiento y precio --")
    seat = {
        "number": ask("Asiento (ej: 12A)"),
        "class_type": ask_choice("Clase", SEAT_CLASSES),
        "available": False,
    }
    base_price = ask_float("Precio base")
    raw_services = ask("Servicios adicionales separados por coma (Enter = ninguno)", "-")
    services = [] if raw_services == "-" else [s.strip() for s in raw_services.split(",") if s.strip()]
    preferences = ask("Preferencias (Enter = ninguna)", "")

    payment = None
    if ask("Registrar pago? (s/n)", "n").lower().startswith("s"):
        payment = {
            "payment_id": "PAY-" + uuid.uuid4().hex[:6].upper(),
            "amount": base_price,
            "date": datetime.now().isoformat(timespec="seconds"),
            "method": ask_choice("Metodo", PAYMENT_METHODS),
            "status": "pending",
        }

    result = client.create_reservation({
        "passenger": passenger,
        "flight": flight,
        "seat": seat,
        "base_price": base_price,
        "additional_services": services,
        "preferences": preferences,
        "payment": payment,
    })
    print("\n  Reserva creada correctamente.")
    print_reservation(result)


def create_sample_reservation(client: ReservationApiClient) -> None:
    result = client.create_reservation({
        "passenger": {"id": "P-001", "name": "Ana Torres",
                      "email": "ana@example.com", "phone": "+573001234567"},
        "flight": {"flight_number": "AV123", "origin": "BOG", "destination": "MDE",
                   "departure": "2026-10-15T08:30:00", "arrival": "2026-10-15T09:35:00"},
        "seat": {"number": "12A", "class_type": "premium", "available": False},
        "base_price": 200.0,
        "additional_services": ["equipaje extra", "comida"],
        "preferences": "ventana",
        "payment": None,
    })
    print("\n  Reserva de ejemplo creada.")
    print_reservation(result)


def list_reservations(client: ReservationApiClient) -> None:
    reservations = client.list_reservations()
    if not reservations:
        print("\n  No hay reservas todavia.")
        return
    for r in reservations:
        print_reservation(r)


def show_price(client: ReservationApiClient) -> None:
    reservation_id = choose_reservation(client)
    if reservation_id is not None:
        print(f"\n  Precio actual: {client.get_price(reservation_id):,.2f}")


def run_state_action(client: ReservationApiClient, verb: str, operation) -> None:
    reservation_id = choose_reservation(client)
    if reservation_id is None:
        return
    result = operation(client, reservation_id)
    print(f"\n  Reserva {verb} correctamente.")
    print_reservation(result)


def subscribe_observer(client: ReservationApiClient) -> None:
    reservation_id = choose_reservation(client)
    if reservation_id is None:
        return
    channel = ask_choice("Canal de notificacion", CHANNELS)
    print(f"\n  {client.add_observer(reservation_id, channel)['message']}")
    print("  (Los avisos apareceran en la terminal del SERVIDOR al cambiar el estado.)")


HANDLERS = {
    "1": create_reservation,
    "2": create_sample_reservation,
    "3": list_reservations,
    "4": show_price,
    "5": lambda c: run_state_action(c, "confirmada", ReservationApiClient.confirm),
    "6": lambda c: run_state_action(c, "modificada", ReservationApiClient.modify),
    "7": lambda c: run_state_action(c, "con check-in", ReservationApiClient.check_in),
    "8": lambda c: run_state_action(c, "abordada", ReservationApiClient.board),
    "9": lambda c: run_state_action(c, "cancelada", ReservationApiClient.cancel),
    "10": subscribe_observer,
}


def main() -> None:
    client = ReservationApiClient()
    while True:
        print(MENU)
        option = input("Elige una opcion: ").strip()
        if option == "0":
            print("Hasta luego.")
            break
        handler = HANDLERS.get(option)
        if handler is None:
            print("  Opcion invalida.")
            continue
        try:
            handler(client)
        except ApiError as error:
            print(f"\n  Error: {error}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nHasta luego.")