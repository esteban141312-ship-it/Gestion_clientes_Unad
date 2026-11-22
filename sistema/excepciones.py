"""Excepciones personalizadas de Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base del sistema."""


class ClienteInvalidoError(SoftwareFJError):
    """Datos de cliente inválidos."""


class ServicioInvalidoError(SoftwareFJError):
    """Datos o parámetros de servicio inválidos."""


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio no está disponible."""


class ParametroFaltanteError(SoftwareFJError):
    """Falta un parámetro obligatorio."""


class CalculoInconsistenteError(SoftwareFJError):
    """El cálculo de costos produjo un resultado inconsistente."""


class ReservaInvalidaError(SoftwareFJError):
    """Intento de reserva incorrecto."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Operación no permitida para el estado actual."""
