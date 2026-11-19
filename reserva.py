# Archivo     : reserva.py
# Proyecto    : Software FJ
# Descripcion : Clase Reserva que integra cliente, servicio, duracion y estado.

import logging                                   # Para registrar eventos y errores en el log
from datetime import datetime                    # Para manejar fechas de la reserva
from excepciones import (                        # Excepciones personalizadas del proyecto
    ReservaError,
    DatosInvalidosError,
    OperacionNoPermitidaError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
)

logger = logging.getLogger("SoftwareFJ")         # Mismo logger que usa el resto del proyecto


class Reserva:
    """
    Representa una reserva hecha por un cliente sobre un servicio de Software FJ.
    Estados: PENDIENTE, CONFIRMADA, CANCELADA, PROCESADA y FALLIDA.
    """

    ESTADO_PENDIENTE = "PENDIENTE"
    ESTADO_CONFIRMADA = "CONFIRMADA"
    ESTADO_CANCELADA = "CANCELADA"
    ESTADO_PROCESADA = "PROCESADA"
    ESTADO_FALLIDA = "FALLIDA"

    _contador_id = 0                             # Contador compartido para generar los ids

    def __init__(self, cliente, servicio, duracion_horas, fecha_reserva=None):
        # Se validan los datos antes de crear la reserva
        try:
            if cliente is None:
                raise DatosInvalidosError("El cliente no puede ser None.")
            if servicio is None:
                raise DatosInvalidosError("El servicio no puede ser None.")
            if not isinstance(duracion_horas, (int, float)) or isinstance(duracion_horas, bool):
                raise DatosInvalidosError("La duracion debe ser numerica.")
            if duracion_horas <= 0:
                raise DatosInvalidosError("La duracion debe ser mayor a cero.")
            if fecha_reserva is not None and not isinstance(fecha_reserva, datetime):
                raise DatosInvalidosError("fecha_reserva debe ser datetime.")
        except DatosInvalidosError as e:
            logger.error("No se pudo crear la reserva: %s", e)
            # Encadenamiento: se conserva la causa original con 'from e'
            raise DatosInvalidosError(f"No se pudo crear la reserva: {e}") from e

        Reserva._contador_id += 1
        self.__id_reserva = f"RES-{Reserva._contador_id:04d}"   # Atributos privados
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion_horas = float(duracion_horas)
        self.__fecha_reserva = fecha_reserva if fecha_reserva else datetime.now()
        self.__estado = Reserva.ESTADO_PENDIENTE
        self.__costo_total = 0.0
        self.__observaciones = "Reserva creada en estado PENDIENTE."
        logger.info("Reserva %s creada en estado PENDIENTE.", self.__id_reserva)

    # Propiedades de solo lectura
    @property
    def id_reserva(self): return self.__id_reserva

    @property
    def cliente(self): return self.__cliente

    @property
    def servicio(self): return self.__servicio

    @property
    def duracion_horas(self): return self.__duracion_horas

    @property
    def fecha_reserva(self): return self.__fecha_reserva

    @property
    def estado(self): return self.__estado

    @property
    def costo_total(self): return self.__costo_total

    @property
    def observaciones(self): return self.__observaciones

    def confirmar(self):
        # Solo se confirma una reserva que este PENDIENTE
        logger.info("[%s] Iniciando confirmacion.", self.__id_reserva)
        try:
            if self.__estado != Reserva.ESTADO_PENDIENTE:
                raise OperacionNoPermitidaError(
                    f"No se puede confirmar una reserva en estado '{self.__estado}'."
                )
        except OperacionNoPermitidaError as e:
            # Una transicion invalida NO cambia el estado actual de la reserva
            logger.error("[%s] Confirmacion rechazada: %s", self.__id_reserva, e)
            raise OperacionNoPermitidaError(
                f"Error al confirmar reserva {self.__id_reserva}: {e}"
            ) from e
        else:
            self.__estado = Reserva.ESTADO_CONFIRMADA
            self.__observaciones = (
                f"Reserva confirmada el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
            )
            logger.info("[%s] Reserva CONFIRMADA.", self.__id_reserva)
            return True
        finally:
            logger.info("[%s] Fin del proceso de confirmacion.", self.__id_reserva)

    def cancelar(self, motivo="Cancelacion solicitada por el cliente"):
        # No se cancela si ya fue procesada o ya esta cancelada
        logger.info("[%s] Iniciando cancelacion.", self.__id_reserva)
        try:
            if self.__estado == Reserva.ESTADO_PROCESADA:
                raise OperacionNoPermitidaError("No se puede cancelar una reserva ya procesada.")
            if self.__estado == Reserva.ESTADO_CANCELADA:
                raise OperacionNoPermitidaError("La reserva ya se encuentra cancelada.")
        except OperacionNoPermitidaError as e:
            logger.error("[%s] Cancelacion rechazada: %s", self.__id_reserva, e)
            raise OperacionNoPermitidaError(
                f"Error al cancelar reserva {self.__id_reserva}: {e}"
            ) from e
        else:
            self.__estado = Reserva.ESTADO_CANCELADA
            self.__observaciones = (
                f"Cancelada el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Motivo: {motivo}"
            )
            logger.info("[%s] Reserva CANCELADA.", self.__id_reserva)
            return True
        finally:
            logger.info("[%s] Fin del proceso de cancelacion.", self.__id_reserva)

    def procesar(self, impuesto=0.0, descuento=0.0):
        # Calcula el costo y deja la reserva como PROCESADA
        logger.info("[%s] Iniciando procesamiento.", self.__id_reserva)
        try:
            # Solo se procesa una reserva CONFIRMADA
            if self.__estado != Reserva.ESTADO_CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"Solo se procesan reservas CONFIRMADAS. Estado actual: {self.__estado}"
                )

            # Se verifica que el servicio este disponible
            if hasattr(self.__servicio, "esta_disponible") and not self.__servicio.esta_disponible():
                raise ServicioNoDisponibleError(
                    f"El servicio '{getattr(self.__servicio, 'nombre', 'N/A')}' no esta disponible."
                )

            # Se calcula el costo con el metodo del servicio (polimorfismo)
            try:
                costo = self.__servicio.calcular_costo(
                    self.__duracion_horas, impuesto, descuento
                )
            except Exception as e:
                raise CalculoInconsistenteError(
                    "Fallo al calcular el costo del servicio."
                ) from e

            # Se verifica que el costo sea valido
            if costo is None or not isinstance(costo, (int, float)) or costo < 0:
                raise CalculoInconsistenteError(f"Costo calculado invalido: {costo}")

        except OperacionNoPermitidaError as e:
            # Estado invalido: solo se avisa, el estado de la reserva no cambia
            logger.error("[%s] Procesamiento rechazado: %s", self.__id_reserva, e)
            raise ReservaError(
                f"No se pudo procesar la reserva {self.__id_reserva}: {e}"
            ) from e
        except (ServicioNoDisponibleError, CalculoInconsistenteError) as e:
            # Falla real del servicio o del calculo: la reserva queda FALLIDA
            self.__estado = Reserva.ESTADO_FALLIDA
            self.__observaciones = f"Fallo en procesamiento: {e}"
            logger.error("[%s] Procesamiento fallido: %s", self.__id_reserva, e)
            raise ReservaError(
                f"No se pudo procesar la reserva {self.__id_reserva}: {e}"
            ) from e
        else:
            self.__costo_total = round(float(costo), 2)
            self.__estado = Reserva.ESTADO_PROCESADA
            self.__observaciones = (
                f"Procesada el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
                f"Costo total: ${self.__costo_total:.2f}."
            )
            logger.info("[%s] Reserva PROCESADA. Costo: $%.2f", self.__id_reserva, self.__costo_total)
            return self.__costo_total
        finally:
            logger.info("[%s] Fin del proceso de reserva.", self.__id_reserva)

    def calcular_costo_total(self, *args, **kwargs):
        # Metodo sobrecargado: acepta 0, 1 o 2 parametros (impuesto, descuento)
        impuesto = args[0] if len(args) > 0 else kwargs.get("impuesto", 0.0)
        descuento = args[1] if len(args) > 1 else kwargs.get("descuento", 0.0)

        try:
            if not isinstance(impuesto, (int, float)) or not (0.0 <= impuesto <= 1.0):
                raise DatosInvalidosError(f"Impuesto fuera de rango: {impuesto}")
            if not isinstance(descuento, (int, float)) or not (0.0 <= descuento <= 1.0):
                raise DatosInvalidosError(f"Descuento fuera de rango: {descuento}")
        except DatosInvalidosError as e:
            logger.error("[%s] Parametros invalidos de costo: %s", self.__id_reserva, e)
            raise CalculoInconsistenteError(
                "Parametros invalidos para el calculo del costo."
            ) from e

        return self.__servicio.calcular_costo(
            self.__duracion_horas, impuesto, descuento
        )

    def to_dict(self):
        # Devuelve la reserva como diccionario (util para el log)
        return {
            "id_reserva": self.__id_reserva,
            "cliente": getattr(self.__cliente, "nombre", str(self.__cliente)),
            "servicio": getattr(self.__servicio, "nombre", str(self.__servicio)),
            "duracion_horas": self.__duracion_horas,
            "fecha_reserva": self.__fecha_reserva.strftime("%Y-%m-%d %H:%M:%S"),
            "estado": self.__estado,
            "costo_total": self.__costo_total,
            "observaciones": self.__observaciones,
        }

    def __str__(self):
        return (
            f"Reserva[{self.__id_reserva}] | "
            f"Cliente: {getattr(self.__cliente, 'nombre', 'N/A')} | "
            f"Servicio: {getattr(self.__servicio, 'nombre', 'N/A')} | "
            f"Duracion: {self.__duracion_horas}h | "
            f"Estado: {self.__estado} | Costo: ${self.__costo_total:.2f}"
        )

    def __repr__(self):
        return f"Reserva(id='{self.__id_reserva}', estado='{self.__estado}')"
