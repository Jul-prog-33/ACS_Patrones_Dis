"""
server.py - lado servidor de la arquitectura cliente-servidor.

Expone via HTTP (Flask) las operaciones sobre reservas. Este archivo NO
contiene logica de negocio: solo traduce peticiones HTTP en llamadas al
dominio (ReservationBuilder, Reservation, ReservationRepository) y
traduce las respuestas o errores del dominio de vuelta a JSON. Toda la
inteligencia (Builder, Strategy, State, Observer) vive en las carpetas
que ya construimos; aqui solo se orquesta.
"""

from __future__ import annotations

from flask import Flask, jsonify, request
from flask_cors import CORS

from .builder.reservation_builder import ReservationBuilder
from .domain.passenger import Passenger
from .domain.flight import Flight
from .domain.seat import Seat
from .domain.payment import Payment
from .observer.email_notifier import EmailNotifier
from .observer.sms_notifier import SMSNotifier
from .observer.app_notifier import AppNotifier
from .repository import ReservationRepository, ReservationNotFoundError
from .state.reservation_state import InvalidTransitionError

app = Flask(__name__)
CORS(app)  # el cliente web corre en otro origen (otro puerto/archivo)

repository = ReservationRepository()

NOTIFIER_CLASSES = {
    "email": EmailNotifier,
    "sms": SMSNotifier,
    "app": AppNotifier,
}


@app.errorhandler(ReservationNotFoundError)
def handle_not_found(error: ReservationNotFoundError):
    return jsonify({"error": str(error)}), 404


@app.errorhandler(InvalidTransitionError)
def handle_invalid_transition(error: InvalidTransitionError):
    return jsonify({"error": str(error)}), 400


def _serialize(reservation_id: str, reservation) -> dict:
    return {"id": reservation_id, **reservation.to_dict()}


@app.route("/reservations", methods=["POST"])
def create_reservation():
    data = request.get_json(force=True)

    builder = (
        ReservationBuilder()
        .set_passenger(Passenger.from_dict(data["passenger"]))
        .set_flight(Flight.from_dict(data["flight"]))
        .set_seat(Seat.from_dict(data["seat"]))
        .set_base_price(data["base_price"])
        .set_preference(data.get("preferences", ""))
    )

    for service in data.get("additional_services", []):
        builder.add_service(service)

    if data.get("payment") is not None:
        builder.set_payment(Payment.from_dict(data["payment"]))

    reservation = builder.build()
    reservation_id = repository.add(reservation)

    return jsonify(_serialize(reservation_id, reservation)), 201


@app.route("/reservations", methods=["GET"])
def list_reservations():
    reservations = repository.list_all()
    return jsonify([
        _serialize(reservation_id, reservation)
        for reservation_id, reservation in reservations.items()
    ])


@app.route("/reservations/<reservation_id>", methods=["GET"])
def get_reservation(reservation_id: str):
    reservation = repository.get(reservation_id)
    return jsonify(_serialize(reservation_id, reservation))


@app.route("/reservations/<reservation_id>/price", methods=["GET"])
def get_price(reservation_id: str):
    reservation = repository.get(reservation_id)
    return jsonify({"price": reservation.calculate_price()})


@app.route("/reservations/<reservation_id>/confirm", methods=["POST"])
def confirm_reservation(reservation_id: str):
    reservation = repository.get(reservation_id)
    reservation.confirm()
    return jsonify(_serialize(reservation_id, reservation))


@app.route("/reservations/<reservation_id>/cancel", methods=["POST"])
def cancel_reservation(reservation_id: str):
    reservation = repository.get(reservation_id)
    reservation.cancel()
    return jsonify(_serialize(reservation_id, reservation))


@app.route("/reservations/<reservation_id>/modify", methods=["POST"])
def modify_reservation(reservation_id: str):
    reservation = repository.get(reservation_id)
    reservation.modify()
    return jsonify(_serialize(reservation_id, reservation))


@app.route("/reservations/<reservation_id>/checkin", methods=["POST"])
def checkin_reservation(reservation_id: str):
    reservation = repository.get(reservation_id)
    reservation.check_in()
    return jsonify(_serialize(reservation_id, reservation))


@app.route("/reservations/<reservation_id>/board", methods=["POST"])
def board_reservation(reservation_id: str):
    reservation = repository.get(reservation_id)
    reservation.board()
    return jsonify(_serialize(reservation_id, reservation))


@app.route("/reservations/<reservation_id>/observers", methods=["POST"])
def add_observer(reservation_id: str):
    reservation = repository.get(reservation_id)
    data = request.get_json(force=True)
    channel = data.get("channel")

    notifier_class = NOTIFIER_CLASSES.get(channel)
    if notifier_class is None:
        return jsonify({
            "error": f"Canal '{channel}' invalido. Use uno de: {list(NOTIFIER_CLASSES)}"
        }), 400

    reservation.add_observer(notifier_class())
    return jsonify({"message": f"Observador '{channel}' suscrito a la reserva."}), 201


if __name__ == "__main__":
    app.run(debug=True, port=5000)