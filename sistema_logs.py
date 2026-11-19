
import logging
import os


class SistemaLogs:
    """Clase encargada de administrar los registros del sistema."""

    def __init__(self, archivo="logs/sistema.log"):
        # Guardamos la ruta donde se almacenarán los registros
        self.archivo = archivo

        # Creamos la carpeta de logs si todavía no existe
        carpeta = os.path.dirname(archivo)

        if carpeta:
            os.makedirs(carpeta, exist_ok=True)

        # Utilizamos el mismo logger del integrante 1
        self.logger = logging.getLogger("SoftwareFJ")

        # Establecemos el nivel mínimo de registro
        self.logger.setLevel(logging.INFO)

        # Evitamos que los registros se dupliquen
        self.logger.propagate = False

        # Comprobamos que no existan manejadores repetidos
        if not self.logger.handlers:

            # Definimos el formato de los mensajes
            formato = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )

            # Creamos el manejador para guardar los registros
            manejador = logging.FileHandler(
                archivo, encoding="utf-8"
            )

            # Aplicamos el formato al manejador
            manejador.setFormatter(formato)

            # Conectamos el manejador con el logger
            self.logger.addHandler(manejador)

    # -------- Registro de información --------
    def info(self, mensaje):
        """Registra operaciones realizadas correctamente."""
        self.logger.info(mensaje)

    # -------- Registro de advertencias --------
    def advertencia(self, mensaje):
        """Registra situaciones que requieren atención."""
        self.logger.warning(mensaje)

    # -------- Registro de errores --------
    def error(self, mensaje):
        """Registra errores ocurridos en el sistema."""
        self.logger.error(mensaje)

    # -------- Registro de excepciones --------
    def excepcion(self, mensaje):
        """Registra una excepción dentro de un bloque except."""
        self.logger.exception(mensaje)
