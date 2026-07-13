# -*- coding: utf-8 -*-
"""
Hotel Maguana - Paleta de Colores
Define la paleta de colores marron/beige del sistema
"""

# ============================================================
# PALETA DE COLORES HOTEL MAGUANA - Marron y Beige
# ============================================================

# Marrones
MARRON_OSCURO = '#3E2723'       # Encabezados, barra titulo
MARRON_MEDIO = '#5D4037'        # Botones principales, menu
MARRON_CLARO = '#795548'        # Botones secundarios
MARRON_MUY_CLARO = '#A1887F'   # Bordes, separadores

# Beiges
BEIGE_OSCURO = '#D7CCC8'        # Fondos de paneles secundarios
BEIGE_MEDIO = '#EFEBE9'         # Fondo principal de ventanas
BEIGE_CLARO = '#F5F0EB'         # Fondo de formularios
BLANCO_CALIDO = '#FFF8F0'       # Areas de texto y listas

# Acentos
DORADO = '#FFC107'              # Alertas, badges, acentos
DORADO_OSCURO = '#FF8F00'       # Hover de dorado

# Estados
VERDE_EXITO = '#4CAF50'         # Disponible, exito
ROJO_ERROR = '#F44336'          # Error, cancelado, ocupado
AZUL_INFO = '#1976D2'           # Informacion, check-in
AMARANJADO = '#FF5722'          # Advertencia, mantenimiento

# Texto
TEXTO_OSCURO = '#1A0A00'        # Texto principal
TEXTO_MEDIO = '#3E2723'         # Texto secundario
TEXTO_CLARO = '#795548'         # Texto de placeholder
TEXTO_BLANCO = '#FFFFFF'        # Texto sobre fondos oscuros
TEXTO_BEIGE = '#FFF8F0'         # Texto sobre marron oscuro

# Colores de estado de habitaciones
ESTADO_DISPONIBLE = '#4CAF50'   # Verde - disponible
ESTADO_OCUPADA = '#F44336'      # Rojo - ocupada
ESTADO_RESERVADA = '#2196F3'    # Azul - reservada
ESTADO_LIMPIEZA = '#FF9800'     # Naranja - en limpieza
ESTADO_MANTENIMIENTO = '#9C27B0' # Morado - mantenimiento

# ============================================================
# ESTILOS PARA WIDGETS TKINTER
# ============================================================

ESTILO_TITULO = {
    'bg': MARRON_OSCURO,
    'fg': TEXTO_BEIGE,
    'font': ('Arial', 16, 'bold'),
    'pady': 15,
    'padx': 20,
}

ESTILO_SUBTITULO = {
    'bg': MARRON_MEDIO,
    'fg': TEXTO_BEIGE,
    'font': ('Arial', 12, 'bold'),
    'pady': 8,
    'padx': 15,
}

ESTILO_BOTON_PRIMARIO = {
    'bg': MARRON_MEDIO,
    'fg': TEXTO_BEIGE,
    'font': ('Arial', 10, 'bold'),
    'relief': 'flat',
    'padx': 15,
    'pady': 8,
    'cursor': 'hand2',
    'activebackground': MARRON_CLARO,
    'activeforeground': TEXTO_BEIGE,
    'bd': 0,
}

ESTILO_BOTON_SECUNDARIO = {
    'bg': BEIGE_OSCURO,
    'fg': MARRON_OSCURO,
    'font': ('Arial', 10),
    'relief': 'flat',
    'padx': 12,
    'pady': 6,
    'cursor': 'hand2',
    'activebackground': MARRON_MUY_CLARO,
    'activeforeground': MARRON_OSCURO,
    'bd': 0,
}

ESTILO_BOTON_PELIGRO = {
    'bg': ROJO_ERROR,
    'fg': TEXTO_BLANCO,
    'font': ('Arial', 10, 'bold'),
    'relief': 'flat',
    'padx': 12,
    'pady': 6,
    'cursor': 'hand2',
    'activebackground': '#D32F2F',
    'activeforeground': TEXTO_BLANCO,
    'bd': 0,
}

ESTILO_BOTON_EXITO = {
    'bg': VERDE_EXITO,
    'fg': TEXTO_BLANCO,
    'font': ('Arial', 10, 'bold'),
    'relief': 'flat',
    'padx': 12,
    'pady': 6,
    'cursor': 'hand2',
    'activebackground': '#388E3C',
    'activeforeground': TEXTO_BLANCO,
    'bd': 0,
}

ESTILO_LABEL = {
    'bg': BEIGE_MEDIO,
    'fg': TEXTO_OSCURO,
    'font': ('Arial', 10),
}

ESTILO_LABEL_TITULO = {
    'bg': BEIGE_MEDIO,
    'fg': MARRON_OSCURO,
    'font': ('Arial', 11, 'bold'),
}

ESTILO_ENTRY = {
    'bg': BLANCO_CALIDO,
    'fg': TEXTO_OSCURO,
    'font': ('Arial', 10),
    'relief': 'solid',
    'bd': 1,
    'insertbackground': MARRON_OSCURO,
}

ESTILO_FRAME = {
    'bg': BEIGE_MEDIO,
    'relief': 'flat',
}

ESTILO_FRAME_PANEL = {
    'bg': BLANCO_CALIDO,
    'relief': 'solid',
    'bd': 1,
}

ESTILO_TREEVIEW = {
    'background': BLANCO_CALIDO,
    'foreground': TEXTO_OSCURO,
    'fieldbackground': BLANCO_CALIDO,
    'font': ('Arial', 9),
}

def aplicar_hover(widget, color_normal, color_hover):
    """Aplica efecto hover a un widget button."""
    widget.bind('<Enter>', lambda e: widget.config(bg=color_hover))
    widget.bind('<Leave>', lambda e: widget.config(bg=color_normal))

def get_color_estado_habitacion(estado):
    """Retorna el color correspondiente al estado de una habitacion."""
    colores = {
        'disponible': ESTADO_DISPONIBLE,
        'ocupada': ESTADO_OCUPADA,
        'reservada': ESTADO_RESERVADA,
        'limpieza': ESTADO_LIMPIEZA,
        'mantenimiento': ESTADO_MANTENIMIENTO,
    }
    return colores.get(estado.lower(), MARRON_CLARO)
