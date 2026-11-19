# Excepciones personalizadas del sistema Software FJ

class ErrorSoftwareFJ(Exception):
    """Excepción base: todas las del sistema heredan de ella."""

class DatoInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando un dato no cumple las validaciones."""

class ParametroFaltanteError(ErrorSoftwareFJ):
    """Se lanza cuando falta un dato obligatorio."""

class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta una operación no válida."""

class ReservaError(ErrorSoftwareFJ):
    """Se lanza cuando una reserva no se puede procesar."""

class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando el servicio no está disponible."""

class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se lanza cuando el cálculo del costo es inválido."""

# Alias: así Reserva y Cliente usan la misma clase de error
DatosInvalidosError = DatoInvalidoError
