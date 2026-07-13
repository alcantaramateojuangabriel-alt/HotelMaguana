# -*- coding: utf-8 -*-
"""
Hotel Maguana - Dashboard Principal
Panel de control principal del sistema hotelero
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.colores import *

class DashboardWindow:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        self.window = tk.Toplevel(root)
        self.window.title(f'Hotel Maguana - {usuario["nombre"]} {usuario["apellido"]}')
        self.window.geometry('1200x700')
        self.window.configure(bg=BEIGE_MEDIO)
        # Centrar
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() - 1200) // 2
        y = (self.window.winfo_screenheight() - 700) // 2
        self.window.geometry(f'1200x700+{x}+{y}')
        self.window.protocol('WM_DELETE_WINDOW', self.on_close)
        self._build_ui()

    def _build_ui(self):
        # Barra superior
        frame_top = tk.Frame(self.window, bg=MARRON_OSCURO, height=70)
        frame_top.pack(fill='x')
        frame_top.pack_propagate(False)
        tk.Label(frame_top, text='HOTEL MAGUANA - SISTEMA DE GESTION',
                 bg=MARRON_OSCURO, fg=TEXTO_BEIGE,
                 font=('Arial', 16, 'bold')).pack(side='left', padx=20, pady=20)
        tk.Label(frame_top, text=f'Usuario: {self.usuario["nombre"]} | Rol: {self.usuario["rol"].upper()}',
                 bg=MARRON_OSCURO, fg=BEIGE_OSCURO,
                 font=('Arial', 10)).pack(side='right', padx=20)

        # Menu lateral
        frame_menu = tk.Frame(self.window, bg=MARRON_MEDIO, width=220)
        frame_menu.pack(side='left', fill='y')
        frame_menu.pack_propagate(False)

        menu_items = [
            ('Dashboard', self.mostrar_dashboard),
            ('Habitaciones', self.modulo_habitaciones),
            ('Reservaciones', self.modulo_reservaciones),
            ('Check-In/Out', self.modulo_checkin),
            ('Clientes', self.modulo_clientes),
            ('Facturacion', self.modulo_facturacion),
            ('Servicios', self.modulo_servicios),
            ('Reportes', self.modulo_reportes),
            ('Configuracion', self.modulo_config),
        ]

        for texto, comando in menu_items:
            btn = tk.Button(frame_menu, text=texto, command=comando,
                           bg=MARRON_MEDIO, fg=TEXTO_BEIGE,
                           font=('Arial', 11), relief='flat',
                           padx=15, pady=12, cursor='hand2',
                           anchor='w', activebackground=MARRON_CLARO,
                           activeforeground=TEXTO_BEIGE)
            btn.pack(fill='x', padx=8, pady=3)
            aplicar_hover(btn, MARRON_MEDIO, MARRON_CLARO)

        tk.Frame(frame_menu, bg=MARRON_CLARO, height=2).pack(fill='x', pady=10)
        btn_salir = tk.Button(frame_menu, text='Cerrar Sesion',
                             command=self.on_close, bg=ROJO_ERROR,
                             fg=TEXTO_BLANCO, font=('Arial', 10, 'bold'),
                             relief='flat', padx=15, pady=10,
                             cursor='hand2', activebackground='#D32F2F',
                             activeforeground=TEXTO_BLANCO)
        btn_salir.pack(fill='x', side='bottom', padx=8, pady=8)

        # Area de contenido
        self.frame_contenido = tk.Frame(self.window, bg=BEIGE_MEDIO)
        self.frame_contenido.pack(side='right', fill='both', expand=True)

        self.mostrar_dashboard()

    def limpiar_contenido(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

    def mostrar_dashboard(self):
        self.limpiar_contenido()
        tk.Label(self.frame_contenido, text='Panel de Control',
                 **ESTILO_TITULO).pack(fill='x')

        frame_tarjetas = tk.Frame(self.frame_contenido, bg=BEIGE_MEDIO)
        frame_tarjetas.pack(fill='x', padx=20, pady=20)

        try:
            from database.init_db import get_connection
            conn = get_connection()
            cursor = conn.cursor()

            # Habitaciones disponibles
            cursor.execute("SELECT COUNT(*) FROM habitaciones WHERE estado='disponible'")
            disp = cursor.fetchone()[0]

            # Reservaciones activas
            cursor.execute("SELECT COUNT(*) FROM reservaciones WHERE estado='confirmada'")
            reservas = cursor.fetchone()[0]

            # Ocupacion actual
            cursor.execute("SELECT COUNT(*) FROM habitaciones WHERE estado='ocupada'")
            ocupadas = cursor.fetchone()[0]

            conn.close()

            self._crear_tarjeta(frame_tarjetas, 'Habitaciones\nDisponibles', str(disp), VERDE_EXITO, 0)
            self._crear_tarjeta(frame_tarjetas, 'Reservas\nActivas', str(reservas), AZUL_INFO, 1)
            self._crear_tarjeta(frame_tarjetas, 'Habitaciones\nOcupadas', str(ocupadas), DORADO, 2)
        except:
            pass

    def _crear_tarjeta(self, parent, titulo, valor, color, col):
        frame = tk.Frame(parent, bg=color, width=200, height=130)
        frame.grid(row=0, column=col, padx=15, pady=10)
        frame.grid_propagate(False)
        tk.Label(frame, text=valor, bg=color, fg=TEXTO_BLANCO,
                 font=('Arial', 32, 'bold')).pack(expand=True)
        tk.Label(frame, text=titulo, bg=color, fg=TEXTO_BLANCO,
                 font=('Arial', 10)).pack(pady=(0, 10))

    def modulo_habitaciones(self):
        self.limpiar_contenido()
        tk.Label(self.frame_contenido, text='Gestion de Habitaciones',
                 **ESTILO_TITULO).pack(fill='x')
        tk.Label(self.frame_contenido, text='Modulo en desarrollo',
                 bg=BEIGE_MEDIO, fg=MARRON_OSCURO,
                 font=('Arial', 14)).pack(pady=50)

    def modulo_reservaciones(self):
        self.limpiar_contenido()
        tk.Label(self.frame_contenido, text='Reservaciones',
                 **ESTILO_TITULO).pack(fill='x')
        tk.Label(self.frame_contenido, text='Modulo en desarrollo',
                 bg=BEIGE_MEDIO, fg=MARRON_OSCURO,
                 font=('Arial', 14)).pack(pady=50)

    def modulo_checkin(self):
        self.limpiar_contenido()
        tk.Label(self.frame_contenido, text='Check-In / Check-Out',
                 **ESTILO_TITULO).pack(fill='x')
        tk.Label(self.frame_contenido, text='Modulo en desarrollo',
                 bg=BEIGE_MEDIO, fg=MARRON_OSCURO,
                 font=('Arial', 14)).pack(pady=50)

    def modulo_clientes(self):
        self.limpiar_contenido()
        tk.Label(self.frame_contenido, text='Gestion de Clientes',
                 **ESTILO_TITULO).pack(fill='x')
        tk.Label(self.frame_contenido, text='Modulo en desarrollo',
                 bg=BEIGE_MEDIO, fg=MARRON_OSCURO,
                 font=('Arial', 14)).pack(pady=50)

    def modulo_facturacion(self):
        self.limpiar_contenido()
        tk.Label(self.frame_contenido, text='Facturacion',
                 **ESTILO_TITULO).pack(fill='x')
        tk.Label(self.frame_contenido, text='Modulo en desarrollo',
                 bg=BEIGE_MEDIO, fg=MARRON_OSCURO,
                 font=('Arial', 14)).pack(pady=50)

    def modulo_servicios(self):
        self.limpiar_contenido()
        tk.Label(self.frame_contenido, text='Servicios Adicionales',
                 **ESTILO_TITULO).pack(fill='x')
        tk.Label(self.frame_contenido, text='Modulo en desarrollo',
                 bg=BEIGE_MEDIO, fg=MARRON_OSCURO,
                 font=('Arial', 14)).pack(pady=50)

    def modulo_reportes(self):
        self.limpiar_contenido()
        tk.Label(self.frame_contenido, text='Reportes y Estadisticas',
                 **ESTILO_TITULO).pack(fill='x')
        tk.Label(self.frame_contenido, text='Modulo en desarrollo',
                 bg=BEIGE_MEDIO, fg=MARRON_OSCURO,
                 font=('Arial', 14)).pack(pady=50)

    def modulo_config(self):
        self.limpiar_contenido()
        tk.Label(self.frame_contenido, text='Configuracion del Sistema',
                 **ESTILO_TITULO).pack(fill='x')
        tk.Label(self.frame_contenido, text='Modulo en desarrollo',
                 bg=BEIGE_MEDIO, fg=MARRON_OSCURO,
                 font=('Arial', 14)).pack(pady=50)

    def on_close(self):
        if messagebox.askokcancel('Cerrar Sesion', 'Desea cerrar sesion?'):
            self.window.destroy()
            self.root.quit()
