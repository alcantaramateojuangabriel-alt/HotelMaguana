# -*- coding: utf-8 -*-
"""
Hotel Maguana - Inicializacion de Base de Datos
Crea todas las tablas necesarias del sistema hotelero
"""

import sqlite3
import os
import hashlib
from datetime import datetime

# Importar modelos
sys_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if sys_path not in sys.path:
    sys.path.insert(0, sys_path)

import sys
from src.models.habitacion import Habitacion
from src.models.cliente import Cliente  
from src.models.reservacion import Reservacion

# Ruta de la base de datos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'hotel_maguana.db')

def hash_password(password):
    """Genera hash SHA-256 de la contrasena."""
    return hashlib.sha256(password.encode()).hexdigest()

def get_connection():
    """Retorna una conexion a la base de datos."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    backups_dir = os.path.join(DATA_DIR, 'backups')
    if not os.path.exists(backups_dir):
        os.makedirs(backups_dir)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

SCHEMA_SQL = """
-- TABLA: Tipos de Habitacion
CREATE TABLE IF NOT EXISTS tipos_habitacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    capacidad INTEGER DEFAULT 2,
    precio_base REAL NOT NULL DEFAULT 0.0,
    activo INTEGER DEFAULT 1,
    creado_en TEXT DEFAULT CURRENT_TIMESTAMP
);

-- TABLA: Habitaciones
CREATE TABLE IF NOT EXISTS habitaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT NOT NULL UNIQUE,
    piso INTEGER DEFAULT 1,
    tipo_id INTEGER NOT NULL,
    precio_noche REAL NOT NULL,
    estado TEXT DEFAULT 'disponible',
    descripcion TEXT,
    amenidades TEXT,
    activo INTEGER DEFAULT 1,
    creado_en TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tipo_id) REFERENCES tipos_habitacion(id)
);

-- TABLA: Clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cedula_pasaporte TEXT UNIQUE,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    email TEXT,
    telefono TEXT,
    direccion TEXT,
    nacionalidad TEXT DEFAULT 'Dominicana',
    fecha_nacimiento TEXT,
    notas TEXT,
    activo INTEGER DEFAULT 1,
    creado_en TEXT DEFAULT CURRENT_TIMESTAMP
);

-- TABLA: Reservaciones
CREATE TABLE IF NOT EXISTS reservaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL,
    cliente_id INTEGER NOT NULL,
    habitacion_id INTEGER NOT NULL,
    fecha_entrada TEXT NOT NULL,
    fecha_salida TEXT NOT NULL,
    num_huespedes INTEGER DEFAULT 1,
    precio_noche REAL NOT NULL,
    total_estimado REAL NOT NULL,
    estado TEXT DEFAULT 'confirmada',
    notas TEXT,
    usuario_id INTEGER,
    creado_en TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (habitacion_id) REFERENCES habitaciones(id)
);

-- TABLA: Servicios adicionales
CREATE TABLE IF NOT EXISTS servicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    precio REAL NOT NULL DEFAULT 0.0,
    categoria TEXT DEFAULT 'general',
    activo INTEGER DEFAULT 1,
    creado_en TEXT DEFAULT CURRENT_TIMESTAMP
);

-- TABLA: Servicios consumidos por reservacion
CREATE TABLE IF NOT EXISTS servicios_consumidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reservacion_id INTEGER NOT NULL,
    servicio_id INTEGER NOT NULL,
    cantidad INTEGER DEFAULT 1,
    precio_unitario REAL NOT NULL,
    subtotal REAL NOT NULL,
    fecha TEXT DEFAULT CURRENT_TIMESTAMP,
    notas TEXT,
    FOREIGN KEY (reservacion_id) REFERENCES reservaciones(id),
    FOREIGN KEY (servicio_id) REFERENCES servicios(id)
);

-- TABLA: Facturas
CREATE TABLE IF NOT EXISTS facturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT UNIQUE NOT NULL,
    reservacion_id INTEGER NOT NULL,
    cliente_id INTEGER NOT NULL,
    subtotal REAL NOT NULL DEFAULT 0.0,
    descuento REAL DEFAULT 0.0,
    impuesto REAL DEFAULT 0.0,
    total REAL NOT NULL DEFAULT 0.0,
    estado TEXT DEFAULT 'pendiente',
    metodo_pago TEXT DEFAULT 'efectivo',
    notas TEXT,
    usuario_id INTEGER,
    creado_en TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reservacion_id) REFERENCES reservaciones(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- TABLA: Detalle de Facturas
CREATE TABLE IF NOT EXISTS detalle_factura (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    factura_id INTEGER NOT NULL,
    descripcion TEXT NOT NULL,
    cantidad INTEGER DEFAULT 1,
    precio_unitario REAL NOT NULL,
    subtotal REAL NOT NULL,
    tipo TEXT DEFAULT 'habitacion',
    FOREIGN KEY (factura_id) REFERENCES facturas(id)
);

-- TABLA: Usuarios del Sistema
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    email TEXT,
    rol TEXT DEFAULT 'recepcion',
    activo INTEGER DEFAULT 1,
    ultimo_login TEXT,
    creado_en TEXT DEFAULT CURRENT_TIMESTAMP
);

-- TABLA: Configuracion del Hotel
CREATE TABLE IF NOT EXISTS configuracion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clave TEXT NOT NULL UNIQUE,
    valor TEXT,
    descripcion TEXT
);

-- TABLA: Logs de Actividad
CREATE TABLE IF NOT EXISTS logs_actividad (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    accion TEXT NOT NULL,
    modulo TEXT,
    detalle TEXT,
    fecha TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

DATA_INICIAL = {
    'tipos_habitacion': [
        ('Habitacion Simple', 'Una cama individual', 1, 1500.00),
        ('Habitacion Doble', 'Dos camas individuales o una doble', 2, 2500.00),
        ('Suite Junior', 'Suite con sala de estar pequena', 2, 4500.00),
        ('Suite Presidencial', 'Suite de lujo con todas las comodidades', 4, 8000.00),
        ('Habitacion Familiar', 'Amplia habitacion para familias', 4, 3500.00),
    ],
    'servicios': [
        ('Desayuno Buffet', 'Desayuno buffet completo', 350.00, 'restaurante'),
        ('Almuerzo', 'Almuerzo completo en restaurante', 500.00, 'restaurante'),
        ('Cena', 'Cena completa en restaurante', 600.00, 'restaurante'),
        ('Lavanderia', 'Servicio de lavanderia por pieza', 150.00, 'lavanderia'),
        ('Planchado', 'Servicio de planchado por pieza', 100.00, 'lavanderia'),
        ('Transporte Aeropuerto', 'Traslado al aeropuerto', 1200.00, 'transporte'),
        ('Tour Ciudad', 'Tour por la ciudad', 2000.00, 'tours'),
        ('Spa - Masaje', 'Masaje relajante 60 minutos', 1800.00, 'spa'),
        ('Minibar', 'Consumo de minibar', 0.00, 'otros'),
        ('Parqueo', 'Parqueo por dia', 200.00, 'otros'),
    ],
    'configuracion': [
        ('nombre_hotel', 'Hotel Maguana', 'Nombre del hotel'),
        ('direccion', 'San Juan de la Maguana, Rep. Dominicana', 'Direccion del hotel'),
        ('telefono', '(809) 557-0000', 'Telefono principal'),
        ('email', 'info@hotelmaguana.com', 'Email de contacto'),
        ('rnc', '000-00000-0', 'RNC del hotel'),
        ('impuesto_itbis', '18', 'Porcentaje de ITBIS'),
        ('moneda', 'DOP', 'Moneda del sistema'),
        ('simbolo_moneda', 'RD$', 'Simbolo de moneda'),
        ('check_in_hora', '14:00', 'Hora de check-in'),
        ('check_out_hora', '12:00', 'Hora de check-out'),
        ('politica_cancelacion', '24 horas antes del check-in', 'Politica de cancelacion'),
        ('version_sistema', '1.0.0', 'Version del sistema'),
    ]
}

def insertar_habitaciones_ejemplo(cursor):
    """Inserta habitaciones de ejemplo."""
    habitaciones = [
        ('101', 1, 1, 1500.00, 'disponible', 'Vista al jardin'),
        ('102', 1, 1, 1500.00, 'disponible', 'Vista al jardin'),
        ('103', 1, 2, 2500.00, 'disponible', 'Vista al patio'),
        ('104', 1, 2, 2500.00, 'disponible', 'Vista al patio'),
        ('105', 1, 5, 3500.00, 'disponible', 'Familiar con dos camas dobles'),
        ('201', 2, 1, 1500.00, 'disponible', 'Vista a la calle'),
        ('202', 2, 1, 1500.00, 'disponible', 'Vista a la calle'),
        ('203', 2, 2, 2500.00, 'disponible', 'Vista a la piscina'),
        ('204', 2, 2, 2500.00, 'disponible', 'Vista a la piscina'),
        ('205', 2, 5, 3500.00, 'disponible', 'Familiar esquinera'),
        ('301', 3, 3, 4500.00, 'disponible', 'Suite Junior vista panoramica'),
        ('302', 3, 3, 4500.00, 'disponible', 'Suite Junior con jacuzzi'),
        ('401', 4, 4, 8000.00, 'disponible', 'Suite Presidencial piso 4'),
    ]
    cursor.executemany(
        'INSERT OR IGNORE INTO habitaciones (numero, piso, tipo_id, precio_noche, estado, descripcion) VALUES (?,?,?,?,?,?)',
        habitaciones
    )

def inicializar_db():
    """Inicializa la base de datos con el schema y datos iniciales."""
    print('Inicializando base de datos Hotel Maguana...')
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Crear tablas
        cursor.executescript(SCHEMA_SQL)
        
        # Crear tablas de modelos
        Habitacion.crear_tabla(conn)
        Cliente.crear_tabla(conn)
        Reservacion.crear_tabla(conn)

                # Insertar tipos de habitacion
        cursor.executemany(
            'INSERT OR IGNORE INTO tipos_habitacion (nombre, descripcion, capacidad, precio_base) VALUES (?,?,?,?)',
            DATA_INICIAL['tipos_habitacion']
        )
        # Insertar habitaciones de ejemplo
        insertar_habitaciones_ejemplo(cursor)
        # Insertar servicios
        cursor.executemany(
            'INSERT OR IGNORE INTO servicios (nombre, descripcion, precio, categoria) VALUES (?,?,?,?)',
            DATA_INICIAL['servicios']
        )
        # Insertar configuracion
        cursor.executemany(
            'INSERT OR IGNORE INTO configuracion (clave, valor, descripcion) VALUES (?,?,?)',
            DATA_INICIAL['configuracion']
        )
        # Crear usuario admin por defecto
        cursor.execute(
            'INSERT OR IGNORE INTO usuarios (username, password_hash, nombre, apellido, rol) VALUES (?,?,?,?,?)',
            ('admin', hash_password('admin123'), 'Administrador', 'Sistema', 'admin')
        )
        # Crear usuario recepcion por defecto
        cursor.execute(
            'INSERT OR IGNORE INTO usuarios (username, password_hash, nombre, apellido, rol) VALUES (?,?,?,?,?)',
            ('recepcion', hash_password('hotel2024'), 'Recepcionista', 'Hotel', 'recepcion')
        )
        conn.commit()
        print('Base de datos inicializada correctamente.')
        print(f'Ubicacion: {DB_PATH}')
    except Exception as e:
        conn.rollback()
        print(f'Error al inicializar la base de datos: {e}')
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    inicializar_db()
