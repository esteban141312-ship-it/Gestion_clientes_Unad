"""Clase Reserva: integra cliente, servicio, duración y estado."""
from .cliente import Cliente
from .entidad import EntidadBase
from .excepciones import (OperacionNoPermitidaError, ReservaInvalidaError,
                          ServicioNoDisponibleError, SoftwareFJError)
from .logger import obtener_logger
from .servicios import Servicio

PENDIENTE, CONFIRMADA, CANCELADA, PROCESADA = "PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA"


class Reserva(EntidadBase):
    def __init__(self, cliente, servicio, horas, **parametros):
        super().__init__()
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Cliente o servicio inválido para la reserva.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible.")
        try:
            servicio.validar_parametros(horas, **parametros)
        except SoftwareFJError as e:
            raise ReservaInvalidaError("Parámetros de reserva inválidos.") from e  # encadenamiento
        self._cliente, self._servicio = cliente, servicio
        self._horas, self._parametros = horas, parametros
        self._estado, self._costo = PENDIENTE, None

    @property
    def estado(self):
        return self._estado

    @property
    def costo(self):
        return self._costo

    def confirmar(self):
        if self._estado != PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self._estado}.")
        self._estado = CONFIRMADA
        obtener_logger().info("Reserva #%s confirmada.", self.id)

    def cancelar(self):
        if self._estado in (CANCELADA, PROCESADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva en estado {self._estado}.")
        self._estado = CANCELADA
        obtener_logger().info("Reserva #%s cancelada.", self.id)

    def procesar(self, descuento=0.0):
        """try/except/else/finally + encadenamiento de excepciones."""
        if self._estado != CONFIRMADA:
            raise OperacionNoPermitidaError("Solo se procesan reservas CONFIRMADAS.")
        try:
            costo = self._servicio.calcular_costo(
                self._horas, impuesto=Servicio.IVA, descuento=descuento, **self._parametros)
        except SoftwareFJError as e:
            raise ReservaInvalidaError(f"No se pudo procesar la reserva #{self.id}.") from e
        else:
            self._costo, self._estado = costo, PROCESADA
        finally:
            obtener_logger().info("Intento de procesamiento de reserva #%s (estado: %s).",
                                  self.id, self._estado)
        return self._costo

    def describir(self):
        costo = f"${self._costo:,.2f}" if self._costo is not None else "sin calcular"
        return (f"Reserva #{self.id} [{self._estado}] {self._cliente.nombre} -> "
                f"{self._servicio.nombre} x {self._horas}h, costo: {costo}")
