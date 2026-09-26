import os
import time
from business_domain.factories import DoctorFactory, PacienteFactory, AdministradorFactory
from business_domain.notifications import ExpedienteClinico
from business_domain.billing import Seguro, Privado, Acuerdo_Facturacion
from infraestructure.repositorio_pacientes_ccon import Repositorio_pacientes
from infraestructure.external_insurance_api import ExternalInsuranceAPI
from infraestructure.insurance_adapter import InsuranceAdapter
from infraestructure.notifiers import Email, SMS_notificacion
from config.hospital_config import HospitalConfig
from facade.hospital_facade import HospitalFacade


def pedir_id() -> str:
    while True:
        valor = input("CC,TI,PEP,DNI: ").strip()
        if valor.isdigit() and 6 <= len(valor) <= 10:
            return valor
        print("DNI inválido. Debe ser numérico y tener entre 6 y 10 dígitos.")


def pedir_texto(mensaje: str) -> str:
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("Este campo no puede estar vacío.")


def pedir_monto() -> float:
    while True:
        valor = input("Monto de la consulta: ").strip()
        if not valor:
            print("Debes ingresar un monto.")
            continue
        try:
            monto = float(valor)
        except ValueError:
            print("Debe ingresar un número válido.")
            continue
        if monto <= 0:
            print("El monto debe ser mayor a cero.")
            continue
        return monto


def registrar_persona(facades: dict):
    print("\n" \
    "           1. Doctor " \
    "           2. Paciente" \
    "           3. Administrador")

    opcion = input("Rol a registrar: ").strip()
    match opcion:
        case "1":
            data = {
                "id": pedir_id(),
                "name": pedir_texto("Nombre: "),
                "especialidad": pedir_texto("Especialidad: ")
            }
            persona_id = facades["doctor"].registrar_paciente(data)
        case "2":
            data = {
                "id": pedir_id(),
                "name": pedir_texto("Nombre: "),
                "tipo_enfermedad": pedir_texto("Tipo de enfermedad: ")
            }
            persona_id = facades["paciente"].registrar_paciente(data)
        case "3":
            data = {
                "id": pedir_id(),
                "name": pedir_texto("Nombre: "),
                "area_administrativa": pedir_texto("Área administrativa: ")
            }
            persona_id = facades["administrador"].registrar_paciente(data)
        case _:
            print("Opción inválida.")
            return

    print(f"Registrado con ID: {persona_id}")


def subir_historia(facade: HospitalFacade):
    paciente_id = pedir_id()
    diagnostico = pedir_texto("Diagnóstico: ")
    try:
        facade.subir_historia(paciente_id, {"diagnostico": diagnostico})
        print("Historia clínica actualizada.")
    except ValueError as e:
        print(f"Error: {e}")


def facturar(facade: HospitalFacade):
    paciente_id = pedir_id()
    monto = pedir_monto()

    print("\n " \
    "       1. Seguro"\
    "       2. Privado"\
    "       3. Acuerdo institucional")
    opcion = input("Tipo de facturación: ").strip()

    match opcion:
        case "1":
            porcentaje = float(input("Porcentaje de cobertura (0.0 a 1.0): "))
            metodo = Seguro(porcentaje)
        case "2":
            recargo = float(input("Recargo: "))
            metodo = Privado(recargo)
        case "3":
            descuento = float(input("Descuento por acuerdo: "))
            metodo = Acuerdo_Facturacion(descuento)
        case _:
            print("Opción inválida.")
            return
    try:
        total = facade.facturacion(paciente_id, monto, metodo)
        print(f"Total a pagar: {total}")
    except ValueError as e:
        print(f"Error: {e}")


def verificar_seguro(facade: HospitalFacade):
    paciente_id = pedir_id()
    try:
        cubierto = facade.verificar_seguro(paciente_id)
        print(f"¿Tiene cobertura?: {cubierto}")
    except ValueError as e:
        print(f"Error: {e}")

def ver_historia(facade: HospitalFacade):
    paciente_id = pedir_id()
    try:
        historia = facade.ver_historia(paciente_id)
        if not historia:
            print("Este paciente no tiene historia clínica registrada.")
        else:
            print(f"\nHistoria clínica de {paciente_id}:")
            for i, registro in enumerate(historia, start=1):
                print(f"  {i}. {registro}")
    except ValueError as e:
        print(f"Error: {e}")

def agendar_cita(facade: HospitalFacade):
    paciente_id = pedir_id()
    doctor_id = pedir_id()
    fecha = pedir_texto("Fecha (AAAA-MM-DD): ")
    hora = pedir_texto("Hora (HH:MM): ")

    cita_id = facade.agendar_cita({
        "paciente_id": paciente_id,
        "doctor_id": doctor_id,
        "fecha": fecha,
        "hora": hora
    })
    print(f"Cita agendada con ID: {cita_id}")


def envrecor_medicamento(facade: HospitalFacade):
    paciente_id = pedir_id()
    medicamento = pedir_texto("Medicamento: ")
    facade.envrecor_medicamento(paciente_id, medicamento)
    print("Recordatorio enviado.")


def alerta_emergencia(facade: HospitalFacade):
    paciente_id = pedir_id()
    mensaje = pedir_texto("Mensaje de emergencia: ")
    facade.alerta_emergencia(paciente_id, mensaje)
    print("Alerta de emergencia enviada.")

def main():
    config = HospitalConfig.get_instancia()
    config.instituto_nombre = "Hospital San Jorge"
    config.horario_atencion = "Consulta Externa: 7:00 A.M. - 5:00 P.M." + "\n" + "Urgencias: 24 horas"
    config.politicas = {
        "notificaciones_habilitadas": True,
        "tratamiento_de_datos": True,
        "consulta_particular": True
    }

    repositorio = Repositorio_pacientes()
    expediente = ExpedienteClinico()
    expediente.agregar(Email("juliangarcia112220@gmail.com"))
    expediente.agregar(SMS_notificacion("3147038966"))

    api_externa = ExternalInsuranceAPI("api-key_salomon")
    adapter_seguro = InsuranceAdapter(api_externa)

    facade_doctor = HospitalFacade(
        fabrica_personas=DoctorFactory(),
        repositorio_pacientes=repositorio,
        expediente_clinico=expediente,
        servicio_seguro=adapter_seguro
    )
    facade_paciente = HospitalFacade(
        fabrica_personas=PacienteFactory(),
        repositorio_pacientes=repositorio,
        expediente_clinico=expediente,
        servicio_seguro=adapter_seguro
    )
    facade_admin = HospitalFacade(
        fabrica_personas=AdministradorFactory(),
        repositorio_pacientes=repositorio,
        expediente_clinico=expediente,
        servicio_seguro=adapter_seguro
    )

    facades = {
        "doctor": facade_doctor,
        "paciente": facade_paciente,
        "administrador": facade_admin
    }

    while True:
        print(f"Bienvenido a {config.instituto_nombre}")
        print(f"Horario de atención: {config.horario_atencion}\n")
        print("""Hospital San Jorge:
            1. Registrar persona
            2. Subir historia clínica
            3. Facturar
            4. Verificar seguro
            5. Ver historia clínica
            6. Agendar cita
            7. Enviar recordatorio de medicamento
            8. Emitir alerta de emergencia
            9. Salir""")
        opcion = input("Seleccione una opción: ").strip()

        match opcion:
            case "1":
                registrar_persona(facades)
                time.sleep(3)
                os.system("cls")
            case "2":
                subir_historia(facade_paciente)
                time.sleep(3)
                os.system("cls")
            case "3":
                facturar(facade_paciente)
                time.sleep(3)
                os.system("cls")
            case "4":
                verificar_seguro(facade_paciente)
                time.sleep(3)
                os.system("cls")
            case "5":
                ver_historia(facade_paciente)
                time.sleep(3)
                os.system("cls")
            case "6":
                agendar_cita(facade_paciente)
                time.sleep(3)
                os.system("cls")
            case "7":
                envrecor_medicamento(facade_paciente)
                time.sleep(3)
                os.system("cls")
            case "8":
                alerta_emergencia(facade_paciente)
                time.sleep(3)
                os.system("cls")
            case "9":
                print("Saliendo del sistema.")
                break
            case _:
                print("Opción inválida.")


if __name__ == "__main__":
    main()