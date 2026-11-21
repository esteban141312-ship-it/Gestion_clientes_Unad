"""Prueba inicial: EntidadBase (clase abstracta) y logger."""
from sistema.entidad import EntidadBase
from sistema.logger import obtener_logger


class EntidadDePrueba(EntidadBase):
    """Clase concreta mínima para probar la clase abstracta."""

    def describir(self) -> str:
        return f"Entidad de prueba #{self.id}"


def main():
    log = obtener_logger()
    log.info("Inicio de la prueba de EntidadBase.")

    # 1) Una clase abstracta no se puede instanciar
    try:
        EntidadBase()
    except TypeError as e:
        log.error("Instanciación de clase abstracta rechazada: %s", e)
        print(f"[ERROR CONTROLADO] {e}")

    # 2) Una clase concreta sí, y recibe un id automático
    a, b = EntidadDePrueba(), EntidadDePrueba()
    print(a)
    print(b)
    log.info("Creadas %s y %s", a.describir(), b.describir())

    log.info("Fin de la prueba.")
    print("Prueba terminada. Revisa logs/software_fj.log")


if __name__ == "__main__":
    main()