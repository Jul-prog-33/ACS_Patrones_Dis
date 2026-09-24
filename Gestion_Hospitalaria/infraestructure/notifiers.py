from business_domain.notifications import NotificacionObserver


class Email(NotificacionObserver):
    def __init__(self, email_direccion: str):
        self.email_direccion = email_direccion

    def update(self, event: str, data: dict) -> None:
        print(f"[Email a {self.email_direccion}] Evento: {event} - {data}")


class SMS_notificacion(NotificacionObserver):
    def __init__(self, numero_celular: str):
        self.numero_celular = numero_celular

    def update(self, event: str, data: dict) -> None:
        print(f"[SMS a {self.numero_celular}] Evento: {event} - {data}")