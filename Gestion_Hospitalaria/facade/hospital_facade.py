from business_domain.factories import PersonFactory
from business_domain.notifications import ExpedienteClinico
from business_domain.billing import BillingStrategy
from interfaces.repositorio_pacientes import Repositorio_Pacientes
from interfaces.servicios_seguros import Servicios_Seguros
from business_domain.entities import Paciente
from config.hospital_config import HospitalConfig

class HospitalFacade:
    def __init__(self, fabrica_personas: PersonFactory,
                 repositorio_pacientes: Repositorio_Pacientes,
                 expediente_clinico: ExpedienteClinico,
                 servicio_seguro: Servicios_Seguros):
        self.fabrica_personas = fabrica_personas
        self.repositorio_pacientes = repositorio_pacientes
        self.expediente_clinico = expediente_clinico
        self.servicio_seguro = servicio_seguro

    def registrar_paciente(self, data: dict) -> str:
        paciente = self.fabrica_personas.crear_persona(data)
        self.repositorio_pacientes.guardar(paciente)
        return paciente.id

    def subir_historia(self, paciente_id: str, record: dict) -> None:
        paciente = self.repositorio_pacientes.obtener_por_id(paciente_id)
        if paciente is None or not isinstance(paciente, Paciente):
            raise ValueError(f"Paciente {paciente_id} no encontrado")

        paciente.historia_clinica.append(record)
        self.repositorio_pacientes.actualizar(paciente)

        config = HospitalConfig.get_instancia()
        if config.get_policy("notificaciones_habilitadas"):
            self.expediente_clinico.notificar("actualizacion_clinica", {
                "institucion": config.instituto_nombre,
                "paciente_id": paciente_id,
                "record": record
            })

    def facturacion(self, paciente_id: str, monto: float, metodo: BillingStrategy) -> float:
        paciente = self.repositorio_pacientes.obtener_por_id(paciente_id)
        return metodo.calcular_total(monto, {"paciente_id": paciente_id})

    def verificar_seguro(self, paciente_id: str) -> bool:
        return self.servicio_seguro.verificar_cobertura(paciente_id)