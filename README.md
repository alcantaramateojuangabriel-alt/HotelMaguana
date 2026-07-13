# 🏨 Hotel Maguana - Sistema de Gestión Hotelera

![Python](https://img.shields.io/badge/Python-3.7%2B-blue) ![SQLite](https://img.shields.io/badge/Database-SQLite3-green) ![Platform](https://img.shields.io/badge/Platform-Windows%207%2F10%2F11-orange) ![Version](https://img.shields.io/badge/Version-1.0.0-brown)

Sistema completo de gestión hotelera desarrollado en Python con interfaz gráfica Tkinter y base de datos SQLite3. Compatible con Windows 7, 10 y 11.

---

## Características Principales

- Gestión de Habitaciones (tipos, precios, disponibilidad)
- Sistema de Reservaciones con control de disponibilidad
- Registro y Gestión de Clientes/Huéspedes
- Facturación completa con cargos adicionales
- Reportes de ocupación e ingresos
- Gestión de Servicios adicionales
- Sistema de Usuarios con roles (Administrador / Recepción)
- Backup automático de base de datos
- Paleta de colores marrón/beige elegante
- 100% offline, sin servidor externo

---

## Requisitos del Sistema

| Componente | Mínimo |
|---|---|
| Sistema Operativo | Windows 7 SP1 / 10 / 11 |
| Python | 3.7 o superior |
| RAM | 2 GB |
| Disco | 500 MB libres |

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/alcantaramateojuangabriel-alt/HotelMaguana.git
cd HotelMaguana

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Inicializar la base de datos
python src/database/init_db.py

# 5. Ejecutar el sistema
python main.py
```

### Credenciales por Defecto
| Usuario | Contraseña | Rol |
|---|---|---|
| admin | admin123 | Administrador |
| recepcion | hotel2024 | Recepcionista |

---

## Estructura del Proyecto

```
HotelMaguana/
|-- main.py
|-- requirements.txt
|-- src/
|   |-- database/
|   |   |-- init_db.py
|   |   |-- connection.py
|   |   `-- backup.py
|   |-- models/
|   |   |-- habitacion.py
|   |   |-- cliente.py
|   |   |-- reservacion.py
|   |   |-- factura.py
|   |   `-- usuario.py
|   |-- views/
|   |   |-- login.py
|   |   |-- dashboard.py
|   |   |-- habitaciones.py
|   |   |-- reservaciones.py
|   |   |-- clientes.py
|   |   |-- facturacion.py
|   |   `-- reportes.py
|   |-- controllers/
|   |   |-- habitacion_ctrl.py
|   |   |-- cliente_ctrl.py
|   |   |-- reservacion_ctrl.py
|   |   `-- factura_ctrl.py
|   `-- utils/
|       |-- colores.py
|       |-- validaciones.py
|       `-- pdf_generator.py
|-- data/
|   `-- backups/
|-- assets/
|   `-- images/
`-- docs/
    |-- MANUAL_USUARIO.md
    |-- MANUAL_TECNICO.md
    `-- ESQUEMA_BD.md
```

---

## Base de Datos (SQLite3)

Tablas del sistema:
- `habitaciones` - Catálogo y estado de habitaciones
- `tipos_habitacion` - Tipos (simple, doble, suite, etc.)
- `clientes` - Registro de huéspedes
- `reservaciones` - Reservas activas e historial
- `facturas` - Facturas emitidas
- `detalle_factura` - Cargos por factura
- `servicios` - Catálogo de servicios adicionales
- `usuarios` - Usuarios del sistema
- `configuracion` - Parámetros del hotel

---

## Paleta de Colores

| Color | HEX | Uso |
|---|---|---|
| Marrón Oscuro | #3E2723 | Barra de título, encabezados |
| Marrón Medio | #5D4037 | Botones principales |
| Beige Oscuro | #D7CCC8 | Fondos de paneles |
| Beige Claro | #EFEBE9 | Fondo principal |
| Blanco Cálido | #FFF8F0 | Áreas de texto |

---

## Licencia

MIT License - Ver archivo LICENSE

---
*Desarrollado con amor para Hotel Maguana*
