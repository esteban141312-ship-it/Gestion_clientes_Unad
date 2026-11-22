"""Clase abstracta Servicio y tres servicios especializados."""
from abc import ABC, abstractmethod

from .entidad import EntidadBase
from .excepciones import (CalculoInconsistenteError, ParametroFaltanteError,
                          ServicioInvalidoError)


def _numero_positivo(valor, campo):
    if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor <= 0:
        raise ServicioInvalidoError(f"{campo} debe ser un número positivo: {valor!r}")
    return valor


class Servicio(EntidadBase, ABC):
    IVA = 0.19

    def __init__(self, nombre, tarifa_hora, disponible=True):
        super().__init__()
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El nombre del servicio es obligatorio.")
        self._nombre = nombre.strip()
        self._tarifa_hora = _numero_positivo(tarifa_hora, "La tarifa")
        self._disponible = bool(disponible)

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        self._disponible = bool(valor)

    @abstractmethod
    def validar_parametros(self, horas, **kwargs):
        """Valida duración y parámetros propios del servicio."""

    @abstractmethod
    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0, **kwargs):
        """Calcula el costo. 'impuesto' y 'descuento' son opcionales (sobrecarga)."""

    # --- Variantes sobrecargadas del cálculo de costos ---
    def calcular_costo_con_iva(self, horas, **kwargs):
        return self.calcular_costo(horas, impuesto=self.IVA, **kwargs)

    def calcular_costo_con_descuento(self, horas, descuento, **kwargs):
        return self.calcular_costo(horas, impuesto=self.IVA, descuento=descuento, **kwargs)

    @staticmethod
    def _aplicar(subtotal, impuesto, descuento):
        if not (0 <= descuento < 1) or not (0 <= impuesto <= 1):
            raise CalculoInconsistenteError(
                f"Impuesto/descuento fuera de rango: {impuesto}, {descuento}")
        total = subtotal * (1 - descuento) * (1 + impuesto)
        if total <= 0:
            raise CalculoInconsistenteError("El costo total resultó no positivo.")
        return round(total, 2)

    @staticmethod
    def _validar_horas(horas, maximo):
        _numero_positivo(horas, "La duración")
        if horas > maximo:
            raise ServicioInvalidoError(f"Duración máxima permitida: {maximo} h.")

    def describir(self):
        estado = "disponible" if self._disponible else "NO disponible"
        return f"{self.nombre} (${self.tarifa_hora:,.0f}/h, {estado})"


class ReservaSala(Servicio):
    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}")
        self._capacidad = capacidad

    def validar_parametros(self, horas, **kwargs):
        self._validar_horas(horas, 12)
        asistentes = kwargs.get("asistentes")
        if asistentes is None:
            raise ParametroFaltanteError("Se requiere 'asistentes' para reservar una sala.")
        if not isinstance(asistentes, int) or not (0 < asistentes <= self._capacidad):
            raise ServicioInvalidoError(
                f"Asistentes inválidos ({asistentes}); capacidad: {self._capacidad}.")

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0, **kwargs):
        return self._aplicar(self.tarifa_hora * horas, impuesto, descuento)

    def describir(self):
        return f"Sala '{super().describir()}' - capacidad {self._capacidad}"


class AlquilerEquipo(Servicio):
    SEGURO = 0.05

    def __init__(self, nombre, tarifa_hora, tipo_equipo, deposito, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        self._tipo_equipo = tipo_equipo
        self._deposito = _numero_positivo(deposito, "El depósito")

    def validar_parametros(self, horas, **kwargs):
        self._validar_horas(horas, 72)

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0, **kwargs):
        subtotal = self.tarifa_hora * horas * (1 + self.SEGURO) + self._deposito
        return self._aplicar(subtotal, impuesto, descuento)

    def describir(self):
        return f"Equipo '{super().describir()}' - {self._tipo_equipo}, depósito ${self._deposito:,.0f}"


class AsesoriaEspecializada(Servicio):
    RECARGO_SENIOR = 0.30

    def __init__(self, nombre, tarifa_hora, especialidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ServicioInvalidoError("La especialidad es obligatoria.")
        self._especialidad = especialidad.strip()

    def validar_parametros(self, horas, **kwargs):
        self._validar_horas(horas, 8)
        if kwargs.get("nivel", "junior") not in ("junior", "senior"):
            raise ServicioInvalidoError("Nivel debe ser 'junior' o 'senior'.")

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0, **kwargs):
        factor = 1 + (self.RECARGO_SENIOR if kwargs.get("nivel") == "senior" else 0)
        return self._aplicar(self.tarifa_hora * horas * factor, impuesto, descuento)

    def describir(self):
        return f"Asesoría '{super().describir()}' - {self._especialidad}"
