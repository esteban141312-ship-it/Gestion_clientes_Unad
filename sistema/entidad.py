"""Clase abstracta que representa las entidades generales del sistema."""
import itertools
from abc import ABC, abstractmethod


class EntidadBase(ABC):
    _contador = itertools.count(1)

    def __init__(self):
        self._id = next(EntidadBase._contador)

    @property
    def id(self) -> int:
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción legible de la entidad."""

    def __str__(self) -> str:
        return self.describir()
