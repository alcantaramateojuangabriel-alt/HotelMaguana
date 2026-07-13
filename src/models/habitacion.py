"""Modelo de Habitación para Hotel Maguana"""
import sqlite3
from datetime import datetime

class Habitacion:
    """Clase para gestionar habitaciones del hotel"""
    
    def __init__(self, numero=None, tipo=None, precio=0.0, capacidad=1, 
                 estado='Disponible', descripcion='', id_habitacion=None):
        self.id_habitacion = id_habitacion
        self.numero = numero
        self.tipo = tipo  # Simple, Doble, Suite, Presidencial
        self.precio = precio
        self.capacidad = capacidad
        self.estado = estado  # Disponible, Ocupada, Mantenimiento, Limpieza
        self.descripcion = descripcion
    
    @staticmethod
    def crear_tabla(conn):
        """Crea la tabla de habitaciones si no existe"""
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habitaciones (
                id_habitacion INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT UNIQUE NOT NULL,
                tipo TEXT NOT NULL,
                precio REAL NOT NULL,
                capacidad INTEGER NOT NULL,
                estado TEXT NOT NULL DEFAULT 'Disponible',
                descripcion TEXT,
                fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
    
    def guardar(self, conn):
        """Guarda una nueva habitación en la base de datos"""
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO habitaciones (numero, tipo, precio, capacidad, estado, descripcion)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.numero, self.tipo, self.precio, self.capacidad, self.estado, self.descripcion))
            conn.commit()
            self.id_habitacion = cursor.lastrowid
            return True, "Habitación guardada exitosamente"
        except sqlite3.IntegrityError:
            return False, "El número de habitación ya existe"
        except Exception as e:
            return False, f"Error al guardar: {str(e)}"
    
    def actualizar(self, conn):
        """Actualiza los datos de una habitación existente"""
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE habitaciones 
                SET numero=?, tipo=?, precio=?, capacidad=?, estado=?, descripcion=?
                WHERE id_habitacion=?
            ''', (self.numero, self.tipo, self.precio, self.capacidad, 
                  self.estado, self.descripcion, self.id_habitacion))
            conn.commit()
            return True, "Habitación actualizada exitosamente"
        except sqlite3.IntegrityError:
            return False, "El número de habitación ya existe"
        except Exception as e:
            return False, f"Error al actualizar: {str(e)}"
    
    def eliminar(self, conn):
        """Elimina una habitación de la base de datos"""
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM habitaciones WHERE id_habitacion=?', (self.id_habitacion,))
            conn.commit()
            return True, "Habitación eliminada exitosamente"
        except Exception as e:
            return False, f"Error al eliminar: {str(e)}"
    
    @staticmethod
    def obtener_todas(conn):
        """Obtiene todas las habitaciones de la base de datos"""
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM habitaciones ORDER BY numero')
        habitaciones = []
        for row in cursor.fetchall():
            hab = Habitacion(
                id_habitacion=row[0],
                numero=row[1],
                tipo=row[2],
                precio=row[3],
                capacidad=row[4],
                estado=row[5],
                descripcion=row[6]
            )
            habitaciones.append(hab)
        return habitaciones
    
    @staticmethod
    def obtener_por_id(conn, id_habitacion):
        """Obtiene una habitación por su ID"""
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM habitaciones WHERE id_habitacion=?', (id_habitacion,))
        row = cursor.fetchone()
        if row:
            return Habitacion(
                id_habitacion=row[0],
                numero=row[1],
                tipo=row[2],
                precio=row[3],
                capacidad=row[4],
                estado=row[5],
                descripcion=row[6]
            )
        return None
    
    @staticmethod
    def obtener_por_numero(conn, numero):
        """Obtiene una habitación por su número"""
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM habitaciones WHERE numero=?', (numero,))
        row = cursor.fetchone()
        if row:
            return Habitacion(
                id_habitacion=row[0],
                numero=row[1],
                tipo=row[2],
                precio=row[3],
                capacidad=row[4],
                estado=row[5],
                descripcion=row[6]
            )
        return None
    
    @staticmethod
    def obtener_disponibles(conn):
        """Obtiene todas las habitaciones disponibles"""
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM habitaciones WHERE estado="Disponible" ORDER BY numero')
        habitaciones = []
        for row in cursor.fetchall():
            hab = Habitacion(
                id_habitacion=row[0],
                numero=row[1],
                tipo=row[2],
                precio=row[3],
                capacidad=row[4],
                estado=row[5],
                descripcion=row[6]
            )
            habitaciones.append(hab)
        return habitaciones
    
    @staticmethod
    def obtener_por_tipo(conn, tipo):
        """Obtiene habitaciones por tipo"""
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM habitaciones WHERE tipo=? ORDER BY numero', (tipo,))
        habitaciones = []
        for row in cursor.fetchall():
            hab = Habitacion(
                id_habitacion=row[0],
                numero=row[1],
                tipo=row[2],
                precio=row[3],
                capacidad=row[4],
                estado=row[5],
                descripcion=row[6]
            )
            habitaciones.append(hab)
        return habitaciones
    
    def cambiar_estado(self, conn, nuevo_estado):
        """Cambia el estado de una habitación"""
        self.estado = nuevo_estado
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE habitaciones SET estado=? WHERE id_habitacion=?', 
                         (nuevo_estado, self.id_habitacion))
            conn.commit()
            return True, f"Estado cambiado a {nuevo_estado}"
        except Exception as e:
            return False, f"Error al cambiar estado: {str(e)}"
    
    def __str__(self):
        return f"Habitación {self.numero} - {self.tipo} - ${self.precio} - {self.estado}"
