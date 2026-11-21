# Archivo     : servicio.py
# Proyecto    : Software FJ
# Descripcion : Clase abstracta Servicio y tres servicios especializados
#               (ReservaSala, AlquilerEquipo y Asesoria) con polimorfismo.

import logging                                   # Para registrar eventos y errores en el log
from abc import abstractmethod                   # Para declarar metodos abstractos
from entidad import Entidad                      # Clase abstracta base del proyecto (parte 1)
from excepciones import (                        # Excepciones personalizadas del proyecto (parte 1)
    DatoInvalidoError,
    ParametroFaltanteError,
)

logger = logging.getLogger("SoftwareFJ")         # Mismo logger que usa el resto del proyecto


class Servicio(Entidad):
    """Clase abstracta que representa un servicio que ofrece Software FJ."""

    def __init__(self, identificador, nombre, tarifa_hora, disponible=True):
        super().__init__(identificador)          # Inicializa la clase padre (Entidad)
        self.nombre = nombre                     # Se asigna por el setter para validar
        self.tarifa_hora = tarifa_hora           # Se asigna por el setter para validar
        self.__disponible = bool(disponible)     # Atributo privado: estado de disponibilidad

    # ---------- Nombre ----------
    @property
    def nombre(self):
        return self.__nombre                     # Devuelve el nombre del servicio

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or valor.strip() == "":
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        if len(valor.strip()) < 3:
            raise DatoInvalidoError("El nombre del servicio debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()            # Se guarda sin espacios sobrantes

    # ---------- Tarifa por hora ----------
    @property
    def tarifa_hora(self):
        return self.__tarifa_hora                # Devuelve la tarifa por hora

    @tarifa_hora.setter
    def tarifa_hora(self, valor):
        if valor is None or isinstance(valor, bool):
            raise ParametroFaltanteError("La tarifa por hora es obligatoria.")
        try:
            tarifa = float(valor)                # Debe poder convertirse a numero
        except (ValueError, TypeError) as error:
            # Encadenamiento de excepciones: conserva la causa original
            raise DatoInvalidoError("La tarifa por hora debe ser numerica.") from error
        if tarifa <= 0:
            raise DatoInvalidoError("La tarifa por hora debe ser mayor a cero.")
        self.__tarifa_hora = tarifa              # Se guarda como numero decimal

    # ---------- Disponibilidad ----------
    def esta_disponible(self):
        """Indica si el servicio se puede reservar (lo usa Reserva.procesar)."""
        return self.__disponible

    def marcar_disponible(self):
        """Habilita el servicio para nuevas reservas."""
        self.__disponible = True
        logger.info("Servicio %s marcado como disponible.", self.nombre)

    def marcar_no_disponible(self):
        """Deshabilita el servicio (por ejemplo, por mantenimiento)."""
        self.__disponible = False
        logger.info("Servicio %s marcado como NO disponible.", self.nombre)

    # ---------- Validaciones comunes ----------
    def _validar_comunes(self, horas, impuesto, descuento):
        """Validaciones que comparten todos los servicios."""
        if isinstance(horas, bool) or not isinstance(horas, (int, float)):
            raise DatoInvalidoError("Las horas deben ser un valor numerico.")
        if horas <= 0:
            raise DatoInvalidoError("Las horas deben ser mayores a cero.")
        for etiqueta, valor in (("impuesto", impuesto), ("descuento", descuento)):
            if isinstance(valor, bool) or not isinstance(valor, (int, float)):
                raise DatoInvalidoError(f"El {etiqueta} debe ser numerico.")
            if not 0.0 <= valor <= 1.0:
                raise DatoInvalidoError(f"El {etiqueta} debe estar entre 0 y 1.")

    @staticmethod
    def _aplicar_ajustes(base, impuesto, descuento):
        """Aplica descuento y luego impuesto al costo base."""
        return round(base * (1 - descuento) * (1 + impuesto), 2)

    # ---------- Metodos abstractos (cada servicio los sobrescribe) ----------
    @abstractmethod
    def validar_parametros(self, horas, impuesto=0.0, descuento=0.0):
        """Valida los parametros segun las reglas propias de cada servicio."""

    @abstractmethod
    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        """Calcula el costo total (sobrescrito en cada servicio)."""

    # describir() tambien es abstracto: viene de Entidad y lo implementa cada servicio

    # ---------- Metodos sobrecargados (variantes del calculo) ----------
    def calcular_costo_con_impuesto(self, horas, impuesto):
        """Variante 1: solo con impuesto."""
        return self.calcular_costo(horas, impuesto, 0.0)

    def calcular_costo_con_descuento(self, horas, descuento):
        """Variante 2: solo con descuento."""
        return self.calcular_costo(horas, 0.0, descuento)

    def cotizar(self, horas, *args, **kwargs):
        """Variante 3: acepta 0, 1 o 2 parametros opcionales (impuesto, descuento)."""
        impuesto = args[0] if len(args) > 0 else kwargs.get("impuesto", 0.0)
        descuento = args[1] if len(args) > 1 else kwargs.get("descuento", 0.0)
        return self.calcular_costo(horas, impuesto, descuento)

    # ---------- Creacion segura (try/except/else/finally) ----------
    @classmethod
    def crear_seguro(cls, *args, **kwargs):
        """Intenta crear un servicio sin que el programa se caiga."""
        try:
            servicio = cls(*args, **kwargs)      # Intenta construir el servicio
        except (DatoInvalidoError, ParametroFaltanteError) as error:
            logger.error("Creacion de %s fallida: %s", cls.__name__, error)
            return None                          # El programa continua
        else:
            logger.info("Servicio creado: %s", servicio.nombre)
            return servicio
        finally:
            logger.info("Fin del intento de creacion de %s", cls.__name__)

    def __str__(self):
        return self.describir()                  # Al imprimir el objeto se muestra su descripcion


class ReservaSala(Servicio):
    """Servicio de reserva de salas (maximo 12 horas por reserva)."""

    def __init__(self, identificador, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0:
            raise DatoInvalidoError("La capacidad debe ser un entero mayor a cero.")
        self.__capacidad = capacidad             # Personas que caben en la sala

    @property
    def capacidad(self):
        return self.__capacidad

    def validar_parametros(self, horas, impuesto=0.0, descuento=0.0):
        self._validar_comunes(horas, impuesto, descuento)
        if horas > 12:                           # Regla propia de las salas
            raise DatoInvalidoError("Una sala no se puede reservar mas de 12 horas.")

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        self.validar_parametros(horas, impuesto, descuento)
        base = self.tarifa_hora * horas          # Costo = tarifa x horas
        return self._aplicar_ajustes(base, impuesto, descuento)

    def describir(self):
        return (f"Sala #{self.identificador}: {self.nombre} | Capacidad: {self.capacidad} personas "
                f"| ${self.tarifa_hora:,.0f}/hora")


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos (maximo 72 horas, con deposito opcional)."""

    def __init__(self, identificador, nombre, tarifa_hora, tipo_equipo, deposito=0.0, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(tipo_equipo, str) or tipo_equipo.strip() == "":
            raise ParametroFaltanteError("El tipo de equipo es obligatorio.")
        if isinstance(deposito, bool) or not isinstance(deposito, (int, float)) or deposito < 0:
            raise DatoInvalidoError("El deposito debe ser un numero mayor o igual a cero.")
        self.__tipo_equipo = tipo_equipo.strip() # Tipo de equipo (portatil, proyector...)
        self.__deposito = float(deposito)        # Cargo fijo que se suma al alquiler

    @property
    def tipo_equipo(self):
        return self.__tipo_equipo

    @property
    def deposito(self):
        return self.__deposito

    def validar_parametros(self, horas, impuesto=0.0, descuento=0.0):
        self._validar_comunes(horas, impuesto, descuento)
        if horas > 72:                           # Regla propia de los equipos
            raise DatoInvalidoError("Un equipo no se puede alquilar mas de 72 horas.")

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        self.validar_parametros(horas, impuesto, descuento)
        base = self.tarifa_hora * horas + self.deposito   # Costo = tarifa x horas + deposito
        return self._aplicar_ajustes(base, impuesto, descuento)

    def describir(self):
        return (f"Equipo #{self.identificador}: {self.nombre} ({self.tipo_equipo}) "
                f"| ${self.tarifa_hora:,.0f}/hora | Deposito: ${self.deposito:,.0f}")


class Asesoria(Servicio):
    """Servicio de asesoria especializada (de 0.5 a 8 horas, segun el nivel del asesor)."""

    NIVELES = {"basico": 1.0, "intermedio": 1.2, "experto": 1.5}   # Multiplicador por nivel

    def __init__(self, identificador, nombre, tarifa_hora, especialidad, nivel="basico", disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(especialidad, str) or especialidad.strip() == "":
            raise ParametroFaltanteError("La especialidad es obligatoria.")
        if not isinstance(nivel, str) or nivel.strip().lower() not in Asesoria.NIVELES:
            raise DatoInvalidoError("El nivel debe ser: basico, intermedio o experto.")
        self.__especialidad = especialidad.strip()
        self.__nivel = nivel.strip().lower()

    @property
    def especialidad(self):
        return self.__especialidad

    @property
    def nivel(self):
        return self.__nivel

    def validar_parametros(self, horas, impuesto=0.0, descuento=0.0):
        self._validar_comunes(horas, impuesto, descuento)
        if not 0.5 <= horas <= 8:                # Regla propia de las asesorias
            raise DatoInvalidoError("Una asesoria dura entre 0.5 y 8 horas.")

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        self.validar_parametros(horas, impuesto, descuento)
        base = self.tarifa_hora * horas * Asesoria.NIVELES[self.nivel]   # Segun el nivel
        return self._aplicar_ajustes(base, impuesto, descuento)

    def describir(self):
        return (f"Asesoria #{self.identificador}: {self.nombre} | {self.especialidad} "
                f"({self.nivel}) | ${self.tarifa_hora:,.0f}/hora")
