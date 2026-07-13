#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hotel Maguana - Sistema de Gestion Hotelera
Archivo principal de entrada al sistema

Autor: Hotel Maguana Dev Team
Version: 1.0.0
Compatible con: Windows 7, 10, 11
Python: 3.7+
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def verificar_dependencias():
    """Verifica que todas las dependencias necesarias esten instaladas."""
    dependencias_faltantes = []
    
    try:
        import sqlite3
    except ImportError:
        dependencias_faltantes.append('sqlite3')
    
    try:
        import PIL
    except ImportError:
        pass  # Pillow es opcional para imagenes
    
    if dependencias_faltantes:
        print(f"ADVERTENCIA: Las siguientes dependencias no estan instaladas: {dependencias_faltantes}")
        print("Ejecute: pip install -r requirements.txt")

def inicializar_base_datos():
    """Inicializa la base de datos si no existe."""
    from database.init_db import inicializar_db
    try:
        inicializar_db()
        return True
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        return False

def main():
    """Funcion principal de entrada al sistema."""
    print("="*50)
    print("   HOTEL MAGUANA - Sistema de Gestion Hotelera")
    print("   Version 1.0.0")
    print("="*50)
    
    # Verificar dependencias
    verificar_dependencias()
    
    # Inicializar base de datos
    if not inicializar_base_datos():
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Error de Inicializacion",
            "No se pudo inicializar la base de datos.\n"
            "Por favor verifique los permisos del directorio."
        )
        sys.exit(1)
    
    # Iniciar la aplicacion
    try:
        from views.login import LoginWindow
        
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana raiz
        
        # Configuracion de la ventana raiz
        root.title("Hotel Maguana")
        
        # Iniciar pantalla de login
        app = LoginWindow(root)
        
        root.mainloop()
        
    except ImportError as e:
        print(f"Error al cargar modulos: {e}")
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Error de Carga",
            f"No se pudieron cargar los modulos del sistema:\n{e}\n\n"
            "Verifique la instalacion del programa."
        )
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
