"""Vista de Gestión de Habitaciones para Hotel Maguana"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.models.habitacion import Habitacion
from src.utils.colores import COLORES
from src.database.init_db import obtener_conexion

class HabitacionesView:
    """Ventana para gestionar habitaciones del hotel"""
    
    def __init__(self, parent):
        self.parent = parent
        self.conn = obtener_conexion()
        
        # Frame principal
        self.frame_principal = tk.Frame(parent, bg=COLORES['fondo'])
        self.frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        titulo = tk.Label(
            self.frame_principal,
            text="Gestión de Habitaciones",
            font=('Arial', 20, 'bold'),
            bg=COLORES['fondo'],
            fg=COLORES['texto_oscuro']
        )
        titulo.pack(pady=(0, 20))
        
        # Frame superior con botones y búsqueda
        frame_superior = tk.Frame(self.frame_principal, bg=COLORES['fondo'])
        frame_superior.pack(fill='x', pady=(0, 10))
        
        # Botones de acción
        btn_agregar = tk.Button(
            frame_superior,
            text="➕ Nueva Habitación",
            command=self.agregar_habitacion,
            bg=COLORES['secundario'],
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=15,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        btn_agregar.pack(side='left', padx=5)
        
        btn_editar = tk.Button(
            frame_superior,
            text="✏️ Editar",
            command=self.editar_habitacion,
            bg=COLORES['primario'],
            fg='white',
            font=('Arial', 11),
            padx=15,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        btn_editar.pack(side='left', padx=5)
        
        btn_eliminar = tk.Button(
            frame_superior,
            text="❌ Eliminar",
            command=self.eliminar_habitacion,
            bg='#d9534f',
            fg='white',
            font=('Arial', 11),
            padx=15,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        btn_eliminar.pack(side='left', padx=5)
        
        btn_actualizar = tk.Button(
            frame_superior,
            text="🔄 Actualizar",
            command=self.cargar_habitaciones,
            bg=COLORES['acento'],
            fg='white',
            font=('Arial', 11),
            padx=15,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        btn_actualizar.pack(side='left', padx=5)
        
        # Frame para tabla
        frame_tabla = tk.Frame(self.frame_principal, bg=COLORES['fondo'])
        frame_tabla.pack(fill='both', expand=True)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(frame_tabla)
        scroll_y.pack(side='right', fill='y')
        
        scroll_x = ttk.Scrollbar(frame_tabla, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')
        
        # Treeview para mostrar habitaciones
        columnas = ('ID', 'Número', 'Tipo', 'Precio', 'Capacidad', 'Estado', 'Descripción')
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show='headings',
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=15
        )
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Configurar columnas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Número', text='Número')
        self.tree.heading('Tipo', text='Tipo')
        self.tree.heading('Precio', text='Precio ($)')
        self.tree.heading('Capacidad', text='Capacidad')
        self.tree.heading('Estado', text='Estado')
        self.tree.heading('Descripción', text='Descripción')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Número', width=100, anchor='center')
        self.tree.column('Tipo', width=120, anchor='center')
        self.tree.column('Precio', width=100, anchor='center')
        self.tree.column('Capacidad', width=100, anchor='center')
        self.tree.column('Estado', width=120, anchor='center')
        self.tree.column('Descripción', width=250)
        
        self.tree.pack(fill='both', expand=True)
        
        # Estilos para filas según estado
        self.tree.tag_configure('disponible', background='#d4edda')
        self.tree.tag_configure('ocupada', background='#f8d7da')
        self.tree.tag_configure('mantenimiento', background='#fff3cd')
        self.tree.tag_configure('limpieza', background='#d1ecf1')
        
        # Cargar datos iniciales
        self.cargar_habitaciones()
    
    def cargar_habitaciones(self):
        """Carga todas las habitaciones en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener habitaciones de la base de datos
        habitaciones = Habitacion.obtener_todas(self.conn)
        
        for hab in habitaciones:
            # Determinar tag según estado
            tag = ''
            if hab.estado == 'Disponible':
                tag = 'disponible'
            elif hab.estado == 'Ocupada':
                tag = 'ocupada'
            elif hab.estado == 'Mantenimiento':
                tag = 'mantenimiento'
            elif hab.estado == 'Limpieza':
                tag = 'limpieza'
            
            self.tree.insert('', 'end', values=(
                hab.id_habitacion,
                hab.numero,
                hab.tipo,
                f"${hab.precio:.2f}",
                hab.capacidad,
                hab.estado,
                hab.descripcion
            ), tags=(tag,))
    
    def agregar_habitacion(self):
        """Abre ventana para agregar nueva habitación"""
        FormularioHabitacion(self.parent, self.conn, self.cargar_habitaciones)
    
    def editar_habitacion(self):
        """Edita la habitación seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una habitación para editar")
            return
        
        item = self.tree.item(seleccion[0])
        id_habitacion = item['values'][0]
        
        habitacion = Habitacion.obtener_por_id(self.conn, id_habitacion)
        if habitacion:
            FormularioHabitacion(self.parent, self.conn, self.cargar_habitaciones, habitacion)
    
    def eliminar_habitacion(self):
        """Elimina la habitación seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una habitación para eliminar")
            return
        
        item = self.tree.item(seleccion[0])
        numero = item['values'][1]
        
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro de eliminar la habitación {numero}?"
        )
        
        if respuesta:
            id_habitacion = item['values'][0]
            habitacion = Habitacion.obtener_por_id(self.conn, id_habitacion)
            if habitacion:
                exito, mensaje = habitacion.eliminar(self.conn)
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    self.cargar_habitaciones()
                else:
                    messagebox.showerror("Error", mensaje)

class FormularioHabitacion:
    """Formulario para agregar/editar habitaciones"""
    
    def __init__(self, parent, conn, callback, habitacion=None):
        self.conn = conn
        self.callback = callback
        self.habitacion = habitacion
        
        # Ventana modal
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Editar Habitación" if habitacion else "Nueva Habitación")
        self.ventana.geometry("500x600")
        self.ventana.configure(bg=COLORES['fondo'])
        self.ventana.resizable(False, False)
        self.ventana.transient(parent)
        self.ventana.grab_set()
        
        # Frame principal
        frame = tk.Frame(self.ventana, bg=COLORES['fondo'])
        frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Título
        titulo = tk.Label(
            frame,
            text="Editar Habitación" if habitacion else "Nueva Habitación",
            font=('Arial', 16, 'bold'),
            bg=COLORES['fondo'],
            fg=COLORES['texto_oscuro']
        )
        titulo.pack(pady=(0, 20))
        
        # Número de habitación
        tk.Label(frame, text="Número de Habitación:", bg=COLORES['fondo'], 
                fg=COLORES['texto_oscuro'], font=('Arial', 11)).pack(anchor='w', pady=(10, 5))
        self.entry_numero = tk.Entry(frame, font=('Arial', 11), relief='solid', bd=1)
        self.entry_numero.pack(fill='x', ipady=5)
        
        # Tipo
        tk.Label(frame, text="Tipo:", bg=COLORES['fondo'], 
                fg=COLORES['texto_oscuro'], font=('Arial', 11)).pack(anchor='w', pady=(10, 5))
        self.combo_tipo = ttk.Combobox(frame, font=('Arial', 11), state='readonly')
        self.combo_tipo['values'] = ('Simple', 'Doble', 'Suite', 'Presidencial')
        self.combo_tipo.pack(fill='x', ipady=5)
        
        # Precio
        tk.Label(frame, text="Precio por Noche ($):", bg=COLORES['fondo'], 
                fg=COLORES['texto_oscuro'], font=('Arial', 11)).pack(anchor='w', pady=(10, 5))
        self.entry_precio = tk.Entry(frame, font=('Arial', 11), relief='solid', bd=1)
        self.entry_precio.pack(fill='x', ipady=5)
        
        # Capacidad
        tk.Label(frame, text="Capacidad (personas):", bg=COLORES['fondo'], 
                fg=COLORES['texto_oscuro'], font=('Arial', 11)).pack(anchor='w', pady=(10, 5))
        self.spin_capacidad = tk.Spinbox(frame, from_=1, to=10, font=('Arial', 11))
        self.spin_capacidad.pack(fill='x', ipady=5)
        
        # Estado
        tk.Label(frame, text="Estado:", bg=COLORES['fondo'], 
                fg=COLORES['texto_oscuro'], font=('Arial', 11)).pack(anchor='w', pady=(10, 5))
        self.combo_estado = ttk.Combobox(frame, font=('Arial', 11), state='readonly')
        self.combo_estado['values'] = ('Disponible', 'Ocupada', 'Mantenimiento', 'Limpieza')
        self.combo_estado.pack(fill='x', ipady=5)
        
        # Descripción
        tk.Label(frame, text="Descripción:", bg=COLORES['fondo'], 
                fg=COLORES['texto_oscuro'], font=('Arial', 11)).pack(anchor='w', pady=(10, 5))
        self.text_descripcion = tk.Text(frame, height=4, font=('Arial', 10), relief='solid', bd=1)
        self.text_descripcion.pack(fill='x')
        
        # Botones
        frame_botones = tk.Frame(frame, bg=COLORES['fondo'])
        frame_botones.pack(pady=20)
        
        btn_guardar = tk.Button(
            frame_botones,
            text="Guardar",
            command=self.guardar,
            bg=COLORES['secundario'],
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=25,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        btn_guardar.pack(side='left', padx=5)
        
        btn_cancelar = tk.Button(
            frame_botones,
            text="Cancelar",
            command=self.ventana.destroy,
            bg='#6c757d',
            fg='white',
            font=('Arial', 11),
            padx=25,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        btn_cancelar.pack(side='left', padx=5)
        
        # Si es edición, cargar datos
        if habitacion:
            self.cargar_datos()
    
    def cargar_datos(self):
        """Carga los datos de la habitación en el formulario"""
        self.entry_numero.insert(0, self.habitacion.numero)
        self.combo_tipo.set(self.habitacion.tipo)
        self.entry_precio.insert(0, str(self.habitacion.precio))
        self.spin_capacidad.delete(0, 'end')
        self.spin_capacidad.insert(0, str(self.habitacion.capacidad))
        self.combo_estado.set(self.habitacion.estado)
        self.text_descripcion.insert('1.0', self.habitacion.descripcion)
    
    def validar_datos(self):
        """Valida los datos del formulario"""
        if not self.entry_numero.get().strip():
            messagebox.showerror("Error", "El número de habitación es obligatorio")
            return False
        
        if not self.combo_tipo.get():
            messagebox.showerror("Error", "Seleccione un tipo de habitación")
            return False
        
        try:
            precio = float(self.entry_precio.get())
            if precio <= 0:
                messagebox.showerror("Error", "El precio debe ser mayor a 0")
                return False
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido")
            return False
        
        if not self.combo_estado.get():
            messagebox.showerror("Error", "Seleccione un estado")
            return False
        
        return True
    
    def guardar(self):
        """Guarda la habitación"""
        if not self.validar_datos():
            return
        
        numero = self.entry_numero.get().strip()
        tipo = self.combo_tipo.get()
        precio = float(self.entry_precio.get())
        capacidad = int(self.spin_capacidad.get())
        estado = self.combo_estado.get()
        descripcion = self.text_descripcion.get('1.0', 'end-1c').strip()
        
        if self.habitacion:  # Editar
            self.habitacion.numero = numero
            self.habitacion.tipo = tipo
            self.habitacion.precio = precio
            self.habitacion.capacidad = capacidad
            self.habitacion.estado = estado
            self.habitacion.descripcion = descripcion
            exito, mensaje = self.habitacion.actualizar(self.conn)
        else:  # Nuevo
            habitacion = Habitacion(numero, tipo, precio, capacidad, estado, descripcion)
            exito, mensaje = habitacion.guardar(self.conn)
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.callback()
            self.ventana.destroy()
        else:
            messagebox.showerror("Error", mensaje)
