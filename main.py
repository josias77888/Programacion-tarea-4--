# Archivo     : main.py
# Proyecto    : Software FJ
# Descripcion : Simulacion de 20 operaciones del sistema (validas e invalidas).
#               El programa nunca se detiene: cada error se controla y se registra en el log.

from sistema_logs import SistemaLogs                          # Parte 4: configura el archivo de logs
from gestor_general import GestorGeneral                      # Parte 4: administra clientes, servicios y reservas
from cliente import Cliente                                   # Parte 1: clientes validados
from servicio import ReservaSala, AlquilerEquipo, Asesoria    # Parte 2: servicios especializados
from excepciones import ErrorSoftwareFJ                       # Parte 1: excepcion base del sistema


def ejecutar(logs, numero, descripcion, funcion):
    """Ejecuta una operacion y evita que cualquier error detenga el programa."""
    print(f"\n--- Operacion {numero}: {descripcion} ---")
    logs.info(f"Operacion {numero}: {descripcion}")           # Se deja constancia en el log
    try:
        resultado = funcion()                                 # Se intenta la operacion
    except ErrorSoftwareFJ as error:                          # Errores controlados del sistema
        print(f"[ERROR CONTROLADO] {type(error).__name__}: {error}")
        if error.__cause__ is not None:                       # Encadenamiento de excepciones
            print(f"   Causa original: {type(error.__cause__).__name__}: {error.__cause__}")
        logs.error(f"Operacion {numero} fallo de forma controlada: {error}")
    except Exception as error:                                # Cualquier error inesperado
        print(f"[ERROR INESPERADO] {type(error).__name__}: {error}")
        logs.error(f"Operacion {numero} con error inesperado: {error}")
    else:                                                     # Solo si no hubo error
        print(f"[OK] {resultado}")
        logs.info(f"Operacion {numero} completada correctamente.")
    finally:                                                  # Se ejecuta siempre
        logs.info(f"Fin de la operacion {numero}.")


def main():
    logs = SistemaLogs()                                      # Se activa el archivo logs/sistema.log
    gestor = GestorGeneral()                                  # Listas internas, sin base de datos
    ctx = {}                                                  # Guarda los objetos creados en la simulacion
    print("=== SIMULACION DEL SISTEMA SOFTWARE FJ ===")

    # ---------------- CLIENTES ----------------
    def op1():
        ctx["ana"] = Cliente.crear_seguro(1, "Ana Pérez", "ana@correo.com", "3001234567")
        gestor.registrar_cliente(ctx["ana"])
        return ctx["ana"].describir()
    ejecutar(logs, 1, "Registrar cliente valido", op1)

    def op2():
        cliente = Cliente(2, "Luis Gómez", "correo-malo", "3009876543")   # lanza DatoInvalidoError
        return gestor.registrar_cliente(cliente)
    ejecutar(logs, 2, "Registrar cliente con correo invalido", op2)

    def op3():
        cliente = Cliente(3, 123, "numero@correo.com", "3001112233")      # nombre no es texto
        return gestor.registrar_cliente(cliente)
    ejecutar(logs, 3, "Registrar cliente con nombre numerico", op3)

    def op4():
        cliente = Cliente(4, "Marta Ruiz", "marta@correo.com", "abc")     # telefono no numerico
        return gestor.registrar_cliente(cliente)
    ejecutar(logs, 4, "Registrar cliente con telefono no numerico", op4)

    def op5():
        ctx["carlos"] = Cliente.crear_seguro(5, "Carlos Díaz", "carlos@correo.com", "3104445566")
        gestor.registrar_cliente(ctx["carlos"])
        return ctx["carlos"].describir()
    ejecutar(logs, 5, "Registrar segundo cliente valido", op5)

    ejecutar(logs, 6, "Registrar un cliente duplicado",
             lambda: gestor.registrar_cliente(ctx["ana"]))

    # ---------------- SERVICIOS ----------------
    def op7():
        ctx["sala"] = ReservaSala.crear_seguro(1, "Sala de juntas", 50000, 10)
        gestor.registrar_servicio(ctx["sala"])
        return ctx["sala"].describir()
    ejecutar(logs, 7, "Crear servicio valido: sala", op7)

    def op8():
        servicio = AlquilerEquipo(2, "Portátil Dell", -8000, "Portátil", 20000)   # tarifa negativa
        return gestor.registrar_servicio(servicio)
    ejecutar(logs, 8, "Crear servicio con tarifa negativa", op8)

    def op9():
        ctx["equipo"] = AlquilerEquipo.crear_seguro(3, "Proyector HD", 8000, "Proyector", 20000)
        gestor.registrar_servicio(ctx["equipo"])
        return ctx["equipo"].describir()
    ejecutar(logs, 9, "Crear servicio valido: alquiler de equipo", op9)

    def op10():
        ctx["asesoria"] = Asesoria.crear_seguro(4, "Asesoría Python", 60000, "Programación", "experto")
        gestor.registrar_servicio(ctx["asesoria"])
        return ctx["asesoria"].describir()
    ejecutar(logs, 10, "Crear servicio valido: asesoria", op10)

    # ---------------- RESERVAS ----------------
    def op11():
        ctx["r1"] = gestor.crear_reserva(ctx["ana"], ctx["sala"], 3)
        gestor.confirmar_reserva(ctx["r1"].id_reserva)
        costo = gestor.procesar_reserva(ctx["r1"].id_reserva, 0.19, 0.10)
        return f"{ctx['r1']} (IVA 19% y descuento 10% aplicados)"
    ejecutar(logs, 11, "Reserva exitosa (crear, confirmar y procesar)", op11)

    ejecutar(logs, 12, "Reserva con duracion invalida",
             lambda: gestor.crear_reserva(ctx["ana"], ctx["sala"], -5))

    sin_registrar = Cliente.crear_seguro(9, "Pedro Rojas", "pedro@correo.com", "3201112233")
    ejecutar(logs, 13, "Reserva de un cliente no registrado",
             lambda: gestor.crear_reserva(sin_registrar, ctx["sala"], 2))

    ejecutar(logs, 14, "Confirmar una reserva que no existe",
             lambda: gestor.confirmar_reserva("RES-9999"))

    def op15():
        ctx["r2"] = gestor.crear_reserva(ctx["carlos"], ctx["equipo"], 5)
        gestor.cancelar_reserva(ctx["r2"].id_reserva, "El cliente ya no lo necesita")
        return f"{ctx['r2']}"
    ejecutar(logs, 15, "Crear y cancelar una reserva", op15)

    ejecutar(logs, 16, "Confirmar una reserva ya cancelada",
             lambda: gestor.confirmar_reserva(ctx["r2"].id_reserva))

    def op17():
        ctx["r3"] = gestor.crear_reserva(ctx["ana"], ctx["asesoria"], 10)
        gestor.confirmar_reserva(ctx["r3"].id_reserva)
        return gestor.procesar_reserva(ctx["r3"].id_reserva)  # 10 h supera el maximo de una asesoria
    ejecutar(logs, 17, "Calculo inconsistente: asesoria de 10 horas", op17)

    def op18():
        ctx["r4"] = gestor.crear_reserva(ctx["carlos"], ctx["equipo"], 2)
        gestor.confirmar_reserva(ctx["r4"].id_reserva)
        ctx["equipo"].marcar_no_disponible()                  # El equipo sale de servicio
        return gestor.procesar_reserva(ctx["r4"].id_reserva)
    ejecutar(logs, 18, "Procesar con servicio no disponible", op18)

    # ---------------- METODOS SOBRECARGADOS ----------------
    def op19():
        sala = ctx["sala"]
        return (f"Sala 2 h -> sin extras: ${sala.calcular_costo(2):,.0f} | "
                f"con impuesto: ${sala.calcular_costo_con_impuesto(2, 0.19):,.0f} | "
                f"con descuento: ${sala.calcular_costo_con_descuento(2, 0.10):,.0f} | "
                f"ambos: ${sala.cotizar(2, 0.19, 0.10):,.0f}")
    ejecutar(logs, 19, "Costos con metodos sobrecargados", op19)

    # ---------------- RESUMEN ----------------
    def op20():
        resumen = gestor.generar_resumen()
        print("   Reservas registradas:")
        for reserva in gestor.consultar_reservas():
            print(f"   - {reserva}")
        return resumen
    ejecutar(logs, 20, "Resumen general del sistema", op20)

    print("\n=== SIMULACION FINALIZADA: el programa no se detuvo ===")
    print("Revisa los eventos y errores en el archivo: logs/sistema.log")


if __name__ == "__main__":
    main()
