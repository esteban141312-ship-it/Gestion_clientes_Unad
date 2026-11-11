# Software FJ - Sistema Integral de Gestión

## Descripción del proyecto

Este proyecto consiste en el desarrollo de un **Sistema Integral de Gestión de Clientes, Servicios y Reservas** para la empresa Software FJ.

La aplicación permitirá gestionar clientes, diferentes tipos de servicios y reservas, incluyendo:

- Reservas de salas.
- Alquiler de equipos.
- Asesorías especializadas.

El sistema será desarrollado utilizando programación orientada a objetos en Python, aplicando principios como abstracción, herencia, polimorfismo y encapsulación.

También contará con un sistema de manejo avanzado de excepciones para controlar errores durante la ejecución y un archivo de logs para registrar eventos y errores.

La aplicación no utilizará bases de datos. La información se gestionará mediante objetos y listas internas.

## Participantes

| N.º | Nombre | Rol |
|---|---|---|
| 1 | Joan Esteban Buitrago | Desarrollador |

*Los demás integrantes se agregarán posteriormente.*

---

## Organización del repositorio

Para mantener un orden en el desarrollo del proyecto, se utilizará Git bash y GitHub para controlar los cambios realizados por cada integrante.

Se manejarán las siguientes ramas:

- **main:** rama principal del proyecto. No se deben realizar cambios directamente sobre ella.
- **dev:** rama de desarrollo donde se integrarán los avances de los integrantes.
- **Ramas individuales:** cada integrante deberá crear su propia rama para trabajar en sus cambios.

### Reglas de trabajo

1. No realizar modificaciones directamente en `main`.
2. Todos los cambios deben realizarse desde ramas individuales.
3. La rama `dev` será utilizada para integrar los avances.
4. Cada integrante debe subir sus cambios a su propia rama.
5. Antes de integrar cambios a `dev`, se deben revisar mediante un Pull Request.

---

## Configuración inicial de Git

### 1. Clonar el repositorio

Cada integrante debe descargar el proyecto en su equipo:

```bash
git clone https://github.com/esteban141312-ship-it/Gestion_clientes_Unad.git
```

Ingresar a la carpeta:

```bash
cd NOMBRE_DEL_PROYECTO
```

### 2. Obtener las ramas disponibles

Actualizar la información de las ramas del repositorio:

```bash
git fetch origin
```

### 3. Cambiar a la rama dev

Todos los integrantes deben trabajar tomando como referencia la rama `dev`:

```bash
git checkout dev
```

Actualizarla con los últimos cambios:

```bash
git pull origin dev
```

### 4. Crear una rama individual

Cada integrante debe crear su propia rama a partir de `dev`.

Ejemplo:

```bash
git checkout -b nombre-integrante
```

Se recomienda utilizar nombres descriptivos, por ejemplo:

- `joan`
- `integrante2`
- `integrante3`
- `integrante4`
- `integrante5`

### 5. Guardar los cambios

Después de realizar modificaciones en el proyecto, ejecutar:

```bash
git add .
```

Registrar los cambios:

```bash
git commit -m "Descripción de los cambios"
```

### 6. Subir la rama a GitHub

Enviar los cambios a la rama individual:

```bash
git push -u origin nombre-integrante
```

### 7. Actualizar la rama dev

Antes de comenzar nuevos trabajos, regresar a `dev` y actualizarla:

```bash
git checkout dev
git pull origin dev
```

Después, volver a crear una rama individual para el siguiente trabajo o actualizar la existente según corresponda.

---

## Flujo de trabajo

El flujo general de trabajo será el siguiente:

```text
             main
               |
               |
              dev
          /    |    \
         /     |     \
      joan  integrante2  integrante3 .....
```

Cada integrante trabajará en su propia rama y enviará sus cambios mediante Pull Requests para su revisión e integración en `dev`.

**Importante:** La rama `main` se mantendrá protegida y no se utilizará para el desarrollo cotidiano. Los cambios se realizarán en ramas individuales y se integrarán primero en `dev`.