"""
api_client.py - unica parte del cliente que sabe hablar HTTP.

El menu de consola (main.py) nunca usa requests directamente: solo llama
a los metodos de ReservationApiClient. Asi, si manana cambia la URL, el
formato o el protocolo, solo se toca este archivo. Igual que server.py no
contiene logica de negocio, este archivo no contiene logica de interfaz.
"""

from __future__ import annotations

import requests

BASE_URL = "http://127.0.0.1:5000"


class ApiError(Exception):
    """Error al comunicarse con el servidor o respuesta de error del mismo."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class ReservationApiClient:
    """Traduce llamadas de Python a peticiones HTTP hacia el servidor."""

    def __init__(self, base_url: str = BASE_URL, timeout: float = 5.0) -> None:
        self.base_url = base_url
        self.timeout = timeout

    # ---------- Reservas ----------
    def create_reservation(self, data: dict) -> dict:
        return self._request("POST", "/reservations", json=data)

    def list_reservations(self) -> list[dict]:
        return self._request("GET", "/reservations")

    def get_reservation(self, reservation_id: str) -> dict:
        return self._request("GET", f"/reservations/{reservation_id}")

    def get_price(self, reservation_id: str) -> float:
        return self._request("GET", f"/reservations/{reservation_id}/price")["price"]

    # ---------- Operaciones del ciclo de vida (State) ----------
    def confirm(self, reservation_id: str) -> dict:
        return self._request("POST", f"/reservations/{reservation_id}/confirm")

    def cancel(self, reservation_id: str) -> dict:
        return self._request("POST", f"/reservations/{reservation_id}/cancel")

    def modify(self, reservation_id: str) -> dict:
        return self._request("POST", f"/reservations/{reservation_id}/modify")

    def check_in(self, reservation_id: str) -> dict:
        return self._request("POST", f"/reservations/{reservation_id}/checkin")

    def board(self, reservation_id: str) -> dict:
        return self._request("POST", f"/reservations/{reservation_id}/board")

    # ---------- Notificaciones (Observer) ----------
    def add_observer(self, reservation_id: str, channel: str) -> dict:
        return self._request(
            "POST",
            f"/reservations/{reservation_id}/observers",
            json={"channel": channel},
        )

    # ---------- Infraestructura interna ----------
    def _request(self, method: str, path: str, json: dict | None = None):
        try:
            response = requests.request(
                method, f"{self.base_url}{path}", json=json, timeout=self.timeout
            )
        except requests.exceptions.ConnectionError:
            raise ApiError(
                "No se pudo conectar con el servidor. "
                "¿Está corriendo 'python -m backend.server' en otra terminal?"
            ) from None
        except requests.exceptions.Timeout:
            raise ApiError("El servidor tardó demasiado en responder.") from None

        try:
            body = response.json()
        except ValueError:
            body = {}

        if not response.ok:
            message = (
                body.get("error") if isinstance(body, dict) else None
            ) or f"Error HTTP {response.status_code}"
            raise ApiError(message, response.status_code)

        return body