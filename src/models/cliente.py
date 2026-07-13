"""Modelo de Cliente para Hotel Maguana"""
import sqlite3
from datetime import datetime

class Cliente:
    """Clase para gestionar clientes/huéspedes del hotel"""
    
    def __init__(self, nombre='', apellido='', identificacion='', tipo_id='Cédula',
                 telefono='', email='', direccion='', nacionalidad='', 
                 fecha_nacimiento='', id_cliente=None):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.identificacion = identificacion  # Cédula, Pasaporte, etc.
        self.tipo_id = tipo_id  # Cédula, Pasaporte, Licencia
        self.telefono = telefono
        self.email = email
        self.direccion = direccion
        self.nacionalidad = nacionalidad
        self.fecha_nacimiento = fecha_nacimiento
    
    @staticmethod
    def crear_tabla(conn):
        """Crea la tabla de clientes si no existe"""
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                identificacion TEXT UNIQUE NOT NULL,
                tipo_id TEXT NOT NULL,
                telefono TEXT,
                email TEXT,
                direccion TEXT,
                nacionalidad TEXT,
                fecha_nacimiento TEXT,
                fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
    
    def guardar(self, conn):
        """Guarda un nuevo cliente en la base de datos"""
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO clientes (nombre, apellido, identificacion, tipo_id, 
                                    telefono, email, direccion, nacionalidad, fecha_nacimiento)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.nombre, self.apellido, self.identificacion, self.tipo_id,
                  self.telefono, self.email, self.direccion, self.nacionalidad, 
                  self.fecha_nacimiento))
            conn.commit()
            self.id_cliente = cursor.lastrowid
            return True, "Cliente guardado exitosamente"
        except sqlite3.IntegrityError:
            return False, "La identificación ya existe en el sistema"
        except Exception as e:
            return False, f"Error al guardar: {str(e)}"
    
    def actualizar(self, conn):
        """Actualiza los datos de un cliente existente"""
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE clientes 
                SET nombre=?, apellido=?, identificacion=?, tipo_id=?, telefono=?, 
                    email=?, direccion=?, nacionalidad=?, fecha_nacimiento=?
                WHERE id_cliente=?
            ''', (self.nombre, self.apellido, self.identificacion, self.tipo_id,
                  self.telefono, self.email, self.direccion, self.nacionalidad,
                  self.fecha_nacimiento, self.id_cliente))
            conn.commit()
            return True, "Cliente actualizado exitosamente"
        except sqlite3.IntegrityError:
            return False, "La identificación ya existe en el sistema"
        except Exception as e:
            return False, f"Error al actualizar: {str(e)}"
    
    def eliminar(self, conn):
        """Elimina un cliente de la base de datos"""
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM clientes WHERE id_cliente=?', (self.id_cliente,))
            conn.commit()
            return True, "Cliente eliminado exitosamente"
        except Exception as e:
            return False, f"Error al eliminar: {str(e)}"
    
    @staticmethod
    def obtener_todos(conn):
        """Obtiene todos los clientes de la base de datos"""
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clientes ORDER BY apellido, nombre')
        clientes = []
        for row in cursor.fetchall():
            cliente = Cliente(
                id_cliente=row[0],
                nombre=row[1],
                apellido=row[2],
                identificacion=row[3],
                tipo_id=row[4],
                telefono=row[5],
                email=row[6],
                direccion=row[7],
                nacionalidad=row[8],
                fecha_nacimiento=row[9]
            )
            clientes.append(cliente)
        return clientes
    
    @staticmethod
    def obtener_por_id(conn, id_cliente):
        """Obtiene un cliente por su ID"""
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clientes WHERE id_cliente=?', (id_cliente,))
        row = cursor.fetchone()
        if row:
            return Cliente(
                id_cliente=row[0],
                nombre=row[1],
                apellido=row[2],
                identificacion=row[3],
                tipo_id=row[4],
                telefono=row[5],
                email=row[6],
                direccion=row[7],
                nacionalidad=row[8],
                fecha_nacimiento=row[9]
            )
        return None
    
    @staticmethod
    def obtener_por_identificacion(conn, identificacion):
        """Obtiene un cliente por su número de identificación"""
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clientes WHERE identificacion=?', (identificacion,))
        row = cursor.fetchone()
        if row:
            return Cliente(
                id_cliente=row[0],
                nombre=row[1],
                apellido=row[2],
                identificacion=row[3],
                tipo_id=row[4],
                telefono=row[5],
                email=row[6],
                direccion=row[7],
                nacionalidad=row[8],
                fecha_nacimiento=row[9]
            )
        return None
    
    @staticmethod
    def buscar(conn, termino):
        """Busca clientes por nombre, apellido o identificación"""
        cursor = conn.cursor()
        termino = f"%{termino}%"
        cursor.execute('''
            SELECT * FROM clientes 
            WHERE nombre LIKE ? OR apellido LIKE ? OR identificacion LIKE ?
            ORDER BY apellido, nombre
        ''', (termino, termino, termino))
        clientes = []
        for row in cursor.fetchall():
            cliente = Cliente(
                id_cliente=row[0],
                nombre=row[1],
                apellido=row[2],
                identificacion=row[3],
                tipo_id=row[4],
                telefono=row[5],
                email=row[6],
                direccion=row[7],
                nacionalidad=row[8],
                fecha_nacimiento=row[9]
            )
            clientes.append(cliente)
        return clientes
    
    def nombre_completo(self):
        """Retorna el nombre completo del cliente"""
        return f"{self.nombre} {self.apellido}"
    
    def __str__(self):
        return f"{self.nombre_completo()} - {self.identificacion}"
