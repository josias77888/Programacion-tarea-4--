import logging

# Se importa la clase Reserva del proyecto
from reserva import Reserva

# Se importan las excepciones personalizadas
from excepciones import (
    DatosInvalidosError,
    ReservaError,
    OperacionNoPermitidaError
)

# Se utiliza el logger compartido del proyecto
logger = logging.getLogger("SoftwareFJ")


class GestorGeneral:
    """Clase encargada de administrar el sistema Software FJ."""

    def __init__(self):
        # Listas que almacenan los objetos durante la ejecucion
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []

        # Se registra la inicializacion del gestor
        logger.info("GestorGeneral inicializado correctamente.")

    # --------------------------------------------------------
    # REGISTRO DE CLIENTES
    # --------------------------------------------------------

    def registrar_cliente(self, cliente):
        """Registra un cliente en el sistema."""

        try:
            # Se valida que el cliente no sea None
            if cliente is None:
                raise DatosInvalidosError(
                    "No se puede registrar un cliente vacio."
                )

            # Se verifica que el cliente no este registrado
            if cliente in self.__clientes:
                raise OperacionNoPermitidaError(
                    "El cliente ya se encuentra registrado."
                )

            # Se agrega el cliente a la lista
            self.__clientes.append(cliente)

            # Se registra la operacion
            logger.info("Cliente registrado correctamente.")

            return True

        except (DatosInvalidosError,
                OperacionNoPermitidaError) as e:

            # Se registra el error ocurrido
            logger.error("Error al registrar cliente: %s", e)

            # Se vuelve a lanzar la excepcion
            raise

    # --------------------------------------------------------
    # REGISTRO DE SERVICIOS
    # --------------------------------------------------------

    def registrar_servicio(self, servicio):
        """Registra un servicio en el sistema."""

        try:
            # Se valida que el servicio no sea None
            if servicio is None:
                raise DatosInvalidosError(
                    "No se puede registrar un servicio vacio."
                )

            # Se verifica que el servicio no este registrado
            if servicio in self.__servicios:
                raise OperacionNoPermitidaError(
                    "El servicio ya se encuentra registrado."
                )

            # Se agrega el servicio a la lista
            self.__servicios.append(servicio)

            # Se registra la operacion
            logger.info("Servicio registrado correctamente.")

            return True

        except (DatosInvalidosError,
                OperacionNoPermitidaError) as e:

            # Se registra el error
            logger.error("Error al registrar servicio: %s", e)

            # Se vuelve a lanzar la excepcion
            raise

    # --------------------------------------------------------
    # CREACION DE RESERVAS
    # --------------------------------------------------------

    def crear_reserva(self, cliente, servicio, duracion_horas):
        """Crea una reserva asociada a un cliente y servicio."""

        try:
            # Se verifica que el cliente este registrado
            if cliente not in self.__clientes:
                raise DatosInvalidosError(
                    "El cliente no esta registrado en el sistema."
                )

            # Se verifica que el servicio este registrado
            if servicio not in self.__servicios:
                raise DatosInvalidosError(
                    "El servicio no esta registrado en el sistema."
                )

            # Se crea el objeto Reserva
            nueva_reserva = Reserva(
                cliente,
                servicio,
                duracion_horas
            )

            # Se almacena la reserva
            self.__reservas.append(nueva_reserva)

            # Se registra la operacion
            logger.info(
                "Reserva %s creada correctamente.",
                nueva_reserva.id_reserva
            )

            # Se retorna la reserva creada
            return nueva_reserva

        except Exception as e:

            # Se registra el error ocurrido
            logger.error("Error al crear reserva: %s", e)

            # Se propaga la excepcion
            raise

    # --------------------------------------------------------
    # CONSULTA DE RESERVAS
    # --------------------------------------------------------

    def consultar_reservas(self):
        """Retorna todas las reservas registradas."""

        # Se registra la consulta
        logger.info("Consulta general de reservas.")

        # Se retorna una copia de la lista
        return list(self.__reservas)

    def buscar_reserva(self, id_reserva):
        """Busca una reserva por su identificador."""

        # Se recorre la lista de reservas
        for reserva in self.__reservas:

            # Se compara el identificador
            if reserva.id_reserva == id_reserva:

                # Se registra el resultado
                logger.info(
                    "Reserva %s encontrada.",
                    id_reserva
                )

                return reserva

        # Se registra que no fue encontrada
        logger.warning(
            "Reserva %s no encontrada.",
            id_reserva
        )

        return None

    # --------------------------------------------------------
    # CONFIRMACION DE RESERVAS
    # --------------------------------------------------------

    def confirmar_reserva(self, id_reserva):
        """Confirma una reserva existente."""

        # Se busca la reserva
        reserva = self.buscar_reserva(id_reserva)

        try:
            # Se verifica que exista
            if reserva is None:
                raise ReservaError(
                    f"No existe la reserva {id_reserva}."
                )

            # Se ejecuta el metodo confirmar de Reserva
            resultado = reserva.confirmar()

            # Se registra la operacion
            logger.info(
                "Reserva %s confirmada por el gestor.",
                id_reserva
            )

            return resultado

        except Exception as e:

            # Se registra el error
            logger.error(
                "Error al confirmar reserva %s: %s",
                id_reserva, e
            )

            # Se propaga la excepcion
            raise

    # --------------------------------------------------------
    # CANCELACION DE RESERVAS
    # --------------------------------------------------------

    def cancelar_reserva(self, id_reserva, motivo):
        """Cancela una reserva existente."""

        # Se busca la reserva
        reserva = self.buscar_reserva(id_reserva)

        try:
            # Se verifica que exista
            if reserva is None:
                raise ReservaError(
                    f"No existe la reserva {id_reserva}."
                )

            # Se ejecuta la cancelacion
            resultado = reserva.cancelar(motivo)

            # Se registra la operacion
            logger.info(
                "Reserva %s cancelada por el gestor.",
                id_reserva
            )

            return resultado

        except Exception as e:

            # Se registra el error
            logger.error(
                "Error al cancelar reserva %s: %s",
                id_reserva, e
            )

            # Se propaga la excepcion
            raise

    # --------------------------------------------------------
    # PROCESAMIENTO DE RESERVAS
    # --------------------------------------------------------

    def procesar_reserva(self, id_reserva,
                         impuesto=0.0, descuento=0.0):
        """Procesa una reserva y calcula su costo."""

        # Se busca la reserva
        reserva = self.buscar_reserva(id_reserva)

        try:
            # Se verifica que exista
            if reserva is None:
                raise ReservaError(
                    f"No existe la reserva {id_reserva}."
                )

            # Se procesa la reserva
            resultado = reserva.procesar(
                impuesto, descuento
            )

            # Se registra el resultado
            logger.info(
                "Reserva %s procesada. Costo: %.2f",
                id_reserva, resultado
            )

            return resultado

        except Exception as e:

            # Se registra el error
            logger.error(
                "Error al procesar reserva %s: %s",
                id_reserva, e
            )

            # Se propaga la excepcion
            raise

    # --------------------------------------------------------
    # LISTADOS GENERALES
    # --------------------------------------------------------

    def listar_clientes(self):
        """Retorna los clientes registrados."""

        # Se registra la consulta
        logger.info("Consulta de clientes registrados.")

        return list(self.__clientes)

    def listar_servicios(self):
        """Retorna los servicios registrados."""

        # Se registra la consulta
        logger.info("Consulta de servicios registrados.")

        return list(self.__servicios)

    # --------------------------------------------------------
    # RESUMEN DEL SISTEMA
    # --------------------------------------------------------

    def generar_resumen(self):
        """Genera un resumen de los elementos del sistema."""

        # Se construye el resumen
        resumen = {
            "total_clientes": len(self.__clientes),
            "total_servicios": len(self.__servicios),
            "total_reservas": len(self.__reservas)
        }

        # Se registra el resumen
        logger.info("Resumen general generado: %s", resumen)

        # Se retorna el diccionario
        return resumen

