"""Clase Cliente con encapsulación y validaciones estrictas."""
import re

from .entidad import EntidadBase
from .excepciones import ClienteInvalidoError, ParametroFaltanteError


class Cliente(EntidadBase):
    _EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")

    def __init__(self, nombre=None, documento=None, email=None, telefono=None):
        super().__init__()
        if None in (nombre, documento, email, telefono):
            raise ParametroFaltanteError("Faltan datos obligatorios del cliente.")
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3 or any(c.isdigit() for c in valor):
            raise ClienteInvalidoError(f"Nombre inválido: {valor!r}")
        self.__nombre = valor.strip().title()

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if not (isinstance(valor, str) and valor.isdigit() and 6 <= len(valor) <= 12):
            raise ClienteInvalidoError(f"Documento inválido: {valor!r}")
        self.__documento = valor

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        if not (isinstance(valor, str) and self._EMAIL.match(valor)):
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}")
        self.__email = valor.lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if not (isinstance(valor, str) and valor.isdigit() and 7 <= len(valor) <= 10):
            raise ClienteInvalidoError(f"Teléfono inválido: {valor!r}")
        self.__telefono = valor

    def describir(self) -> str:
        return f"Cliente #{self.id}: {self.nombre} (Doc: {self.documento}, {self.email})"
