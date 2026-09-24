from business_domain.factories import DoctorFactory, PacienteFactory, AdministradorFactory
from business_domain.notifications import ExpedienteClinico
from business_domain.billing import Seguro, Privado, Acuerdo_Facturacion
from infraestructure.repositorio_pacientes_ccon import Repositorio_pacientes
from infraestructure.external_insurance_api import ExternalInsuranceAPI
from infraestructure.insurance_adapter import InsuranceAdapter
from infraestructure.notifiers import Email, SMS_notificacion
from config.hospital_config import HospitalConfig
from facade.hospital_facade import HospitalFacade


def main():
    config = HospitalConfig.get_instancia()
    config.instituto_nombre = "Hospital San Jorge"
    config.horario_atencion = "24 horas"
    config.politicas = {"alertas_habilitadas": True, "tratamiento de datos": True, "consulta particular": True}

    repositorio = Repositorio_pacientes()
    expediente = ExpedienteClinico()
    expediente.agregar(Email("juliangarcia112220@gmail.com"))
    expediente.agregar(SMS_notificacion("3147038966"))

    api_externa = ExternalInsuranceAPI("api-key_salomon")
    adapter_seguro = InsuranceAdapter(api_externa)

    fabrica_paciente = PacienteFactory()

    facade = HospitalFacade(
        fabrica_personas=fabrica_paciente,
        repositorio_pacientes=repositorio,
        expediente_clinico=expediente,
        servicio_seguro=adapter_seguro
    )

    paciente_id = facade.registrar_paciente({
        "id": "1104680251",
        "name": "Julian Valencia",
        "tipo_enfermedad": "Gripe de Hombre", 
    })
    print("Paciente registrado con ID:", paciente_id)

    facade.subir_historia(paciente_id, {"diagnostico": "Reposo por 15 días"})

    total_seguro = facade.facturacion(paciente_id, 100, Seguro(0.20))
    print("Total con seguro:", total_seguro)

    total_privado = facade.facturacion(paciente_id, 100, Privado(15))
    print("Total privado:", total_privado)

    cubierto = facade.verificar_seguro(paciente_id)
    print("¿Tiene cobertura?:", cubierto)


if __name__ == "__main__":
    main()