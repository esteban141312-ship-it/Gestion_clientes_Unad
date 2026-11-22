"""Software FJ - Simulación completa del sistema (más de 10 operaciones)."""
from sistema.entidad import EntidadBase
from sistema.gestor import GestorSistema
from sistema.logger import obtener_logger
from sistema.servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


def probar_clase_abstracta():
    """EntidadBase es abstracta: no se puede instanciar directamente."""
    log = obtener_logger()
    try:
        EntidadBase()
    except TypeError as e:
        log.error("Instanciación de clase abstracta rechazada: %s", e)
        print(f"  [ERROR CONTROLADO] {e}")


def main():
    log = obtener_logger()
    log.info("===== INICIO DE LA SIMULACIÓN =====")
    g = GestorSistema()
    print("=== SOFTWARE FJ: simulación ===")

    print("\n0) Clase abstracta")
    probar_clase_abstracta()

    print("\n1-4) Clientes")
    ana = g.registrar_cliente(nombre="ana gómez", documento="1098765432",
                              email="ana@correo.com", telefono="3101234567")
    luis = g.registrar_cliente(nombre="Luis Pérez", documento="52345678",
                               email="luis@correo.com", telefono="3209876543")
    g.registrar_cliente(nombre="X1", documento="abc", email="malo", telefono="1")   # inválido
    g.registrar_cliente(nombre="Sin Datos")                                         # faltan parámetros

    print("\n5-9) Servicios")
    sala = g.agregar_servicio(ReservaSala, "Sala Ejecutiva", 80000, 10)
    equipo = g.agregar_servicio(AlquilerEquipo, "Proyector 4K", 15000, "Audiovisual", 100000)
    asesoria = g.agregar_servicio(AsesoriaEspecializada, "Asesoría Cloud", 120000, "Cloud")
    g.agregar_servicio(ReservaSala, "Sala Rota", -5, 0)                             # inválido
    equipo_off = g.agregar_servicio(AlquilerEquipo, "Portátil", 20000, "Cómputo",
                                    200000, disponible=False)

    print("\nPolimorfismo: describir() y costo de 2 h con IVA")
    for s in g.servicios:
        if s.disponible:
            print(f"  - {s.describir()} -> ${s.calcular_costo_con_iva(2):,.2f}")
    if sala:
        print(f"  Sala con 10% de descuento (2 h): ${sala.calcular_costo_con_descuento(2, 0.10):,.2f}")

    print("\n10-16) Reservas")
    r1 = g.crear_reserva(ana, sala, 3, asistentes=8)
    r2 = g.crear_reserva(luis, asesoria, 2, nivel="senior")
    r3 = g.crear_reserva(ana, equipo, 24)
    g.crear_reserva(luis, sala, 2, asistentes=50)           # excede capacidad
    g.crear_reserva(luis, sala, 2)                          # falta parámetro
    g.crear_reserva(luis, equipo_off, 5)                    # servicio no disponible
    g.crear_reserva("no-es-cliente", sala, 1, asistentes=2)  # cliente inválido

    print("\n17-24) Confirmar, procesar y cancelar")
    for r in (r1, r2, r3):
        if r:
            g.confirmar(r)
    if r1:
        g.procesar(r1)
    if r2:
        g.procesar(r2, descuento=0.10)
    if r3:
        g.procesar(r3, descuento=1.5)                       # descuento inconsistente
        g.cancelar(r1)                                      # ya procesada
        g.cancelar(r3)
        g.confirmar(r3)                                     # ya cancelada

    print("\n=== Estado final ===")
    for r in g.reservas:
        print(" ", r)
    log.info("===== FIN DE LA SIMULACIÓN =====")
    print("\nEl sistema terminó sin interrupciones. Revisa logs/software_fj.log")


if __name__ == "__main__":
    main()