from abc import ABC, abstractmethod

class NotificacionObserver(ABC):
    @abstractmethod
    def update(self, event: str, data: dict) -> None:
        pass


class ExpedienteClinico:
    def __init__(self):
        self.observadores = []

    def agregar(self, obs: NotificacionObserver) -> None:
        self.observadores.append(obs)

    def remover(self, obs: NotificacionObserver) -> None:
        self.observadores.remove(obs)

    def notificar(self, event: str, data: dict) -> None:
        for obs in self.observadores:
            obs.update(event, data)