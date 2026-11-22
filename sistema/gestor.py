"""Gestor central: listas internas y operaciones protegidas."""
from .cliente import Cliente
from .excepciones import SoftwareFJError
from .logger import obtener_logger
from .reserva import Reserva


class GestorSistema:
    def __init__(self):
        self.clientes, self.servicios, self.reservas = [], [], []
        self._log = obtener_logger()

    def _ejecutar(self, descripcion, funcion, *args, **kwargs):
        """Ejecuta una operación sin dejar que un error detenga el sistema."""
        try:
            resultado = funcion(*args, **kwargs)
        except SoftwareFJError as e:
            causa = f" | causa: {e.__cause__!r}" if e.__cause__ else ""
            self._log.error("%s falló: %s%s", descripcion, e, causa)
            print(f"  [ERROR CONTROLADO] {descripcion}: {e}{causa}")
            return None
        except Exception as e:  # error inesperado: se registra y se continúa
            self._log.exception("Error inesperado en %s", descripcion)
            print(f"  [ERROR INESPERADO] {descripcion}: {e!r}")
            return None
        else:
            self._log.info("%s completada correctamente.", descripcion)
            print(f"  [OK] {descripcion}")
            return resultado
        finally:
            self._log.info("Fin de operación: %s", descripcion)

    def registrar_cliente(self, **datos):
        c = self._ejecutar("Registro de cliente", lambda: Cliente(**datos))
        if c:
            self.clientes.append(c)
        return c

    def agregar_servicio(self, clase, *args, **kwargs):
        s = self._ejecutar(f"Creación de servicio {clase.__name__}", clase, *args, **kwargs)
        if s:
            self.servicios.append(s)
        return s

    def crear_reserva(self, cliente, servicio, horas, **parametros):
        r = self._ejecutar("Creación de reserva", Reserva, cliente, servicio, horas, **parametros)
        if r:
            self.reservas.append(r)
        return r

    def confirmar(self, reserva):
        return self._ejecutar("Confirmación de reserva", reserva.confirmar)

    def cancelar(self, reserva):
        return self._ejecutar("Cancelación de reserva", reserva.cancelar)

    def procesar(self, reserva, descuento=0.0):
        return self._ejecutar("Procesamiento de reserva", reserva.procesar, descuento)
