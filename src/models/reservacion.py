"""Modelo de Reservación para Hotel Maguana"""
import sqlite3
from datetime import datetime, timedelta

class Reservacion:
    """Clase para gestionar reservaciones del hotel"""
    
    def __init__(self, id_cliente=None, id_habitacion=None, fecha_entrada='', 
                 fecha_salida='', num_huespedes=1, estado='Pendiente', 
                 total=0.0, observaciones='', id_reservacion=None):
        self.id_reservacion = id_reservacion
        self.id_cliente = id_cliente
        self.id_habitacion = id_habitacion
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.num_huespedes = num_huespedes
        self.estado = estado  # Pendiente, Confirmada, Check-in, Check-out, Cancelada
        self.total = total
        self.observaciones = observaciones
    
    @staticmethod
    def crear_tabla(conn):
        """Crea la tabla de reservaciones si no existe"""
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservaciones (
                id_reservacion INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER NOT NULL,
                id_habitacion INTEGER NOT NULL,
                fecha_entrada TEXT NOT NULL,
                fecha_salida TEXT NOT NULL,
                num_huespedes INTEGER NOT NULL,
                estado TEXT NOT NULL DEFAULT 'Pendiente',
                total REAL NOT NULL,
                observaciones TEXT,
                fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
                FOREIGN KEY (id_habitacion) REFERENCES habitaciones(id_habitacion)
            )
        ''')
        conn.commit()
    
    def guardar(self, conn):
        """Guarda una nueva reservación en la base de datos"""
        cursor = conn.cursor()
        try:
            # Verificar disponibilidad de la habitación
            if not self.verificar_disponibilidad(conn):
                return False, "La habitación no está disponible para las fechas seleccionadas"
            
            cursor.execute('''
                INSERT INTO reservaciones (id_cliente, id_habitacion, fecha_entrada, 
                                          fecha_salida, num_huespedes, estado, total, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.id_cliente, self.id_habitacion, self.fecha_entrada, 
                  self.fecha_salida, self.num_huespedes, self.estado, self.total, self.observaciones))
            conn.commit()
            self.id_reservacion = cursor.lastrowid
            return True, "Reservación guardada exitosamente"
        except Exception as e:
            return False, f"Error al guardar: {str(e)}"
    
    def actualizar(self, conn):
        """Actualiza los datos de una reservación existente"""
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE reservaciones 
                SET id_cliente=?, id_habitacion=?, fecha_entrada=?, fecha_salida=?, 
                    num_huespedes=?, estado=?, total=?, observaciones=?
                WHERE id_reservacion=?
            ''', (self.id_cliente, self.id_habitacion, self.fecha_entrada, self.fecha_salida,
                  self.num_huespedes, self.estado, self.total, self.observaciones, self.id_reservacion))
            conn.commit()
            return True, "Reservación actualizada exitosamente"
        except Exception as e:
            return False, f"Error al actualizar: {str(e)}"
    
    def eliminar(self, conn):
        """Elimina una reservación de la base de datos"""
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM reservaciones WHERE id_reservacion=?', (self.id_reservacion,))
            conn.commit()
            return True, "Reservación eliminada exitosamente"
        except Exception as e:
            return False, f"Error al eliminar: {str(e)}"
    
    def verificar_disponibilidad(self, conn):
        """Verifica si la habitación está disponible para las fechas seleccionadas"""
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM reservaciones 
            WHERE id_habitacion=? AND estado IN ('Pendiente', 'Confirmada', 'Check-in')
            AND (
                (fecha_entrada <= ? AND fecha_salida > ?) OR
                (fecha_entrada < ? AND fecha_salida >= ?) OR
                (fecha_entrada >= ? AND fecha_salida <= ?)
            )
        ''', (self.id_habitacion, self.fecha_entrada, self.fecha_entrada,
              self.fecha_salida, self.fecha_salida, self.fecha_entrada, self.fecha_salida))
        count = cursor.fetchone()[0]
        return count == 0
    
    @staticmethod
    def obtener_todas(conn):
        """Obtiene todas las reservaciones de la base de datos"""
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM reservaciones 
            ORDER BY fecha_entrada DESC
        ''')
        reservaciones = []
        for row in cursor.fetchall():
            reserv = Reservacion(
                id_reservacion=row[0],
                id_cliente=row[1],
                id_habitacion=row[2],
                fecha_entrada=row[3],
                fecha_salida=row[4],
                num_huespedes=row[5],
                estado=row[6],
                total=row[7],
                observaciones=row[8]
            )
            reservaciones.append(reserv)
        return reservaciones
    
    @staticmethod
    def obtener_por_id(conn, id_reservacion):
        """Obtiene una reservación por su ID"""
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reservaciones WHERE id_reservacion=?', (id_reservacion,))
        row = cursor.fetchone()
        if row:
            return Reservacion(
                id_reservacion=row[0],
                id_cliente=row[1],
                id_habitacion=row[2],
                fecha_entrada=row[3],
                fecha_salida=row[4],
                num_huespedes=row[5],
                estado=row[6],
                total=row[7],
                observaciones=row[8]
            )
        return None
    
    @staticmethod
    def obtener_por_cliente(conn, id_cliente):
        """Obtiene todas las reservaciones de un cliente"""
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM reservaciones 
            WHERE id_cliente=?
            ORDER BY fecha_entrada DESC
        ''', (id_cliente,))
        reservaciones = []
        for row in cursor.fetchall():
            reserv = Reservacion(
                id_reservacion=row[0],
                id_cliente=row[1],
                id_habitacion=row[2],
                fecha_entrada=row[3],
                fecha_salida=row[4],
                num_huespedes=row[5],
                estado=row[6],
                total=row[7],
                observaciones=row[8]
            )
            reservaciones.append(reserv)
        return reservaciones
    
    @staticmethod
    def obtener_por_habitacion(conn, id_habitacion):
        """Obtiene todas las reservaciones de una habitación"""
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM reservaciones 
            WHERE id_habitacion=?
            ORDER BY fecha_entrada DESC
        ''', (id_habitacion,))
        reservaciones = []
        for row in cursor.fetchall():
            reserv = Reservacion(
                id_reservacion=row[0],
                id_cliente=row[1],
                id_habitacion=row[2],
                fecha_entrada=row[3],
                fecha_salida=row[4],
                num_huespedes=row[5],
                estado=row[6],
                total=row[7],
                observaciones=row[8]
            )
            reservaciones.append(reserv)
        return reservaciones
    
    @staticmethod
    def obtener_activas(conn):
        """Obtiene las reservaciones activas (Pendiente, Confirmada, Check-in)"""
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM reservaciones 
            WHERE estado IN ('Pendiente', 'Confirmada', 'Check-in')
            ORDER BY fecha_entrada
        ''')
        reservaciones = []
        for row in cursor.fetchall():
            reserv = Reservacion(
                id_reservacion=row[0],
                id_cliente=row[1],
                id_habitacion=row[2],
                fecha_entrada=row[3],
                fecha_salida=row[4],
                num_huespedes=row[5],
                estado=row[6],
                total=row[7],
                observaciones=row[8]
            )
            reservaciones.append(reserv)
        return reservaciones
    
    @staticmethod
    def obtener_por_estado(conn, estado):
        """Obtiene reservaciones por estado"""
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM reservaciones 
            WHERE estado=?
            ORDER BY fecha_entrada DESC
        ''', (estado,))
        reservaciones = []
        for row in cursor.fetchall():
            reserv = Reservacion(
                id_reservacion=row[0],
                id_cliente=row[1],
                id_habitacion=row[2],
                fecha_entrada=row[3],
                fecha_salida=row[4],
                num_huespedes=row[5],
                estado=row[6],
                total=row[7],
                observaciones=row[8]
            )
            reservaciones.append(reserv)
        return reservaciones
    
    def cambiar_estado(self, conn, nuevo_estado):
        """Cambia el estado de una reservación"""
        self.estado = nuevo_estado
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE reservaciones SET estado=? WHERE id_reservacion=?', 
                         (nuevo_estado, self.id_reservacion))
            conn.commit()
            return True, f"Estado cambiado a {nuevo_estado}"
        except Exception as e:
            return False, f"Error al cambiar estado: {str(e)}"
    
    def calcular_total(self, precio_noche):
        """Calcula el total de la reservación basado en el número de noches"""
        try:
            entrada = datetime.strptime(self.fecha_entrada, '%Y-%m-%d')
            salida = datetime.strptime(self.fecha_salida, '%Y-%m-%d')
            noches = (salida - entrada).days
            self.total = noches * precio_noche
            return self.total
        except:
            return 0.0
    
    def __str__(self):
        return f"Reservación #{self.id_reservacion} - {self.fecha_entrada} a {self.fecha_salida}"
