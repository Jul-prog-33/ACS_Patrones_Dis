"""
Payment - clase de dominio.

Representa el pago asociado a una reserva. Como se discutio en el diseno,
el ejercicio no pide un patron especifico para Payment, asi que se deja
como una clase de datos simple, sin logica de patrones.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Payment:
    """Datos basicos del pago asociado a una reserva."""

    payment_id: str
    amount: float
    date: str    # ISO 8601, ej: "2026-09-27T14:00:00"
    method: str  # "credit_card" | "debit_card" | "transfer" | etc.
    status: str = "pending"  # "pending" | "completed" | "refunded"

    def to_dict(self) -> dict:
        """Serializa el pago para enviarlo como JSON desde la API."""
        return {
            "payment_id": self.payment_id,
            "amount": self.amount,
            "date": self.date,
            "method": self.method,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: dict) -> "Payment":
        """Reconstruye un Payment a partir de un diccionario (payload JSON)."""
        return Payment(
            payment_id=data["payment_id"],
            amount=data["amount"],
            date=data["date"],
            method=data["method"],
            status=data.get("status", "pending"),
        )