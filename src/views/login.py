# -*- coding: utf-8 -*-
"""
Hotel Maguana - Vista de Login
Pantalla de inicio de sesion del sistema
"""

import tkinter as tk
from tkinter import messagebox
import hashlib
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.colores import *

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.usuario_actual = None
        self.window = tk.Toplevel(root)
        self.window.title('Hotel Maguana - Inicio de Sesion')
        self.window.geometry('480x600')
        self.window.resizable(False, False)
        self.window.configure(bg=BEIGE_MEDIO)
        # Centrar ventana
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() - 480) // 2
        y = (self.window.winfo_screenheight() - 600) // 2
        self.window.geometry(f'480x600+{x}+{y}')
        self.window.protocol('WM_DELETE_WINDOW', self.on_close)
        self.window.grab_set()
        self._build_ui()

    def _build_ui(self):
        # Header
        frame_header = tk.Frame(self.window, bg=MARRON_OSCURO, height=140)
        frame_header.pack(fill='x')
        frame_header.pack_propagate(False)
        tk.Label(frame_header, text='HOTEL MAGUANA', bg=MARRON_OSCURO,
                 fg=TEXTO_BEIGE, font=('Arial', 22, 'bold')).pack(pady=(30, 5))
        tk.Label(frame_header, text='Sistema de Gestion Hotelera', bg=MARRON_OSCURO,
                 fg=BEIGE_OSCURO, font=('Arial', 11)).pack()

        # Linea decorativa
        tk.Frame(self.window, bg=DORADO, height=4).pack(fill='x')

        # Frame central
        frame_centro = tk.Frame(self.window, bg=BEIGE_MEDIO, padx=50, pady=30)
        frame_centro.pack(fill='both', expand=True)

        tk.Label(frame_centro, text='Iniciar Sesion', bg=BEIGE_MEDIO,
                 fg=MARRON_OSCURO, font=('Arial', 16, 'bold')).pack(pady=(10, 25))

        # Campo Usuario
        tk.Label(frame_centro, text='Usuario:', bg=BEIGE_MEDIO,
                 fg=MARRON_OSCURO, font=('Arial', 10, 'bold')).pack(anchor='w')
        self.entry_usuario = tk.Entry(frame_centro, font=('Arial', 12),
                                      bg=BLANCO_CALIDO, fg=TEXTO_OSCURO,
                                      relief='solid', bd=1,
                                      insertbackground=MARRON_OSCURO)
        self.entry_usuario.pack(fill='x', pady=(3, 15), ipady=6)

        # Campo Contrasena
        tk.Label(frame_centro, text='Contrasena:', bg=BEIGE_MEDIO,
                 fg=MARRON_OSCURO, font=('Arial', 10, 'bold')).pack(anchor='w')
        self.entry_password = tk.Entry(frame_centro, font=('Arial', 12),
                                        bg=BLANCO_CALIDO, fg=TEXTO_OSCURO,
                                        relief='solid', bd=1, show='*',
                                        insertbackground=MARRON_OSCURO)
        self.entry_password.pack(fill='x', pady=(3, 25), ipady=6)

        # Label de error
        self.label_error = tk.Label(frame_centro, text='', bg=BEIGE_MEDIO,
                                     fg=ROJO_ERROR, font=('Arial', 9))
        self.label_error.pack(pady=(0, 10))

        # Boton Ingresar
        self.btn_login = tk.Button(frame_centro, text='INGRESAR AL SISTEMA',
                                    command=self.login,
                                    bg=MARRON_MEDIO, fg=TEXTO_BEIGE,
                                    font=('Arial', 12, 'bold'),
                                    relief='flat', padx=20, pady=12,
                                    cursor='hand2',
                                    activebackground=MARRON_CLARO,
                                    activeforeground=TEXTO_BEIGE)
        self.btn_login.pack(fill='x', pady=5)
        aplicar_hover(self.btn_login, MARRON_MEDIO, MARRON_CLARO)

        # Footer
        frame_footer = tk.Frame(self.window, bg=BEIGE_OSCURO)
        frame_footer.pack(fill='x', side='bottom')
        tk.Label(frame_footer, text='Hotel Maguana v1.0.0 | San Juan de la Maguana, RD',
                 bg=BEIGE_OSCURO, fg=MARRON_CLARO,
                 font=('Arial', 8)).pack(pady=8)

        # Bindings
        self.entry_usuario.bind('<Return>', lambda e: self.entry_password.focus())
        self.entry_password.bind('<Return>', lambda e: self.login())
        self.entry_usuario.focus()

    def login(self):
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()

        if not usuario or not password:
            self.label_error.config(text='Por favor complete todos los campos.')
            return

        try:
            from database.init_db import get_connection
            conn = get_connection()
            cursor = conn.cursor()
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute(
                'SELECT * FROM usuarios WHERE username=? AND password_hash=? AND activo=1',
                (usuario, password_hash)
            )
            user = cursor.fetchone()

            if user:
                # Actualizar ultimo login
                from datetime import datetime
                cursor.execute(
                    'UPDATE usuarios SET ultimo_login=? WHERE id=?',
                    (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user['id'])
                )
                conn.commit()
                conn.close()

                self.usuario_actual = dict(user)
                self.window.destroy()
                self._abrir_dashboard()
            else:
                conn.close()
                self.label_error.config(text='Usuario o contrasena incorrectos.')
                self.entry_password.delete(0, 'end')
                self.entry_password.focus()
        except Exception as e:
            self.label_error.config(text=f'Error de conexion: {str(e)[:40]}')

    def _abrir_dashboard(self):
        try:
            from views.dashboard import DashboardWindow
            DashboardWindow(self.root, self.usuario_actual)
        except Exception as e:
            messagebox.showerror('Error', f'No se pudo abrir el sistema:\n{e}')
            self.root.quit()

    def on_close(self):
        if messagebox.askokcancel('Salir', 'Desea salir del sistema?'):
            self.root.quit()
