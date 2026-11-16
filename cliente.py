import re                      # Para validar el correo con expresiones regulares
import logging                 # Para registrar errores en el archivo de logs
from entidad import Entidad
from excepciones import DatoInvalidoError, ParametroFaltanteError

logger = logging.getLogger("SoftwareFJ")  # Logger compartido con el resto del proyecto


class Cliente(Entidad):
    """Cliente con datos personales encapsulados y validaciones estrictas."""

    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)  # Inicializa la clase padre
        # Se asigna mediante los setters para que se validen los datos
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    # ---------- Nombre ----------
    @property
    def nombre(self):
        return self.__nombre  # Atributo privado

    @nombre.setter
    def nombre(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El nombre es obligatorio.")
        if len(valor.strip()) < 3:
            raise DatoInvalidoError("El nombre debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()

    # ---------- Correo ----------
    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not valor:
            raise ParametroFaltanteError("El correo es obligatorio.")
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"  # Formato básico de correo
        if not re.match(patron, valor):
            raise DatoInvalidoError(f"Correo inválido: {valor}")
        self.__correo = valor

    # ---------- Teléfono ----------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        try:
            int(valor)  # Debe contener solo números
        except (ValueError, TypeError) as error:
            # Encadenamiento de excepciones: conserva la causa original
            raise DatoInvalidoError("El teléfono debe ser numérico.") from error
        if not str(valor).isdigit():
            raise DatoInvalidoError("El telefono solo debe tener digitos")
        if len(str(valor)) != 10:
            raise DatoInvalidoError("El teléfono debe tener 10 dígitos.")
        self.__telefono = str(valor)

    # ---------- Polimorfismo ----------
    def describir(self):
        """Implementa el método abstracto de Entidad."""
        return f"Cliente #{self.identificador}: {self.nombre} | {self.correo} | {self.telefono}"

    # ---------- Creación segura (try/except/else/finally) ----------
    @staticmethod
    def crear_seguro(identificador, nombre, correo, telefono):
        """Intenta crear un cliente sin que el programa se caiga."""
        try:
            cliente = Cliente(identificador, nombre, correo, telefono)
        except (DatoInvalidoError, ParametroFaltanteError) as error:
            logger.error("Registro de cliente fallido: %s", error)  # Se guarda en logs
            return None  # El programa continúa
        else:
            # Solo se ejecuta si NO hubo error
            logger.info("Cliente registrado: %s", cliente.nombre)
            return cliente
        finally:
            # Se ejecuta siempre, haya o no error
            logger.info("Fin del intento de registro del cliente %s", identificador)