from abc import ABC, abstractmethod  # Herramientas para clases abstractas

class Entidad(ABC):
    """Clase abstracta que representa entidades generales del sistema."""

    def __init__(self, identificador):
        self._identificador = identificador  # Atributo protegido (encapsulación)

    @property
    def identificador(self):
        """Devuelve el identificador de la entidad."""
        return self._identificador

    @abstractmethod
    def describir(self):
        """Obliga a las clases hijas a describirse (polimorfismo)."""
        pass