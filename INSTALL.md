# Guia de Instalacion - Hotel Maguana

## Requisitos Previos

- Python 3.7 o superior
- Windows 7 SP1, Windows 10 o Windows 11
- 2 GB de RAM minimo (4 GB recomendado)
- 500 MB de espacio en disco

## Instalacion Paso a Paso

### 1. Instalar Python

1. Descargar Python desde https://www.python.org/downloads/
2. Ejecutar el instalador
3. **IMPORTANTE**: Marcar la casilla "Add Python to PATH"
4. Click en "Install Now"
5. Verificar instalacion abriendo CMD y ejecutando:
   ```
   python --version
   ```

### 2. Descargar el Proyecto

**Opcion A: Con Git**
```bash
git clone https://github.com/alcantaramateojuangabriel-alt/HotelMaguana.git
cd HotelMaguana
```

**Opcion B: Descarga Directa**
1. Click en el boton verde "Code" en GitHub
2. Seleccionar "Download ZIP"
3. Extraer el archivo ZIP
4. Abrir CMD en la carpeta extraida

### 3. Crear Entorno Virtual (Opcional pero Recomendado)

```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Inicializar la Base de Datos

```bash
python src/database/init_db.py
```

Esto creara:
- La carpeta `data/` con la base de datos `hotel_maguana.db`
- Tablas del sistema
- Datos de prueba (habitaciones, servicios, etc.)
- Usuarios por defecto

### 6. Ejecutar el Sistema

```bash
python main.py
```

## Credenciales por Defecto

| Usuario | Contrasena | Rol |
|---------|------------|-----|
| admin | admin123 | Administrador |
| recepcion | hotel2024 | Recepcionista |

**IMPORTANTE**: Cambiar estas contrasenas despues del primer inicio de sesion.

## Solucion de Problemas

### Error: "python no se reconoce como comando"
- Python no esta en el PATH
- Reinstalar Python marcando "Add Python to PATH"

### Error al importar modulos
- Verificar que el entorno virtual este activo
- Reinstalar dependencias: `pip install -r requirements.txt`

### Error de base de datos
- Eliminar la carpeta `data/`
- Ejecutar nuevamente `python src/database/init_db.py`

### Problemas de permisos
- Ejecutar CMD como Administrador
- Verificar permisos de escritura en la carpeta del proyecto

## Desinstalacion

1. Cerrar la aplicacion
2. Desactivar entorno virtual: `deactivate`
3. Eliminar la carpeta del proyecto

## Soporte

Para reportar problemas o solicitar ayuda, abrir un Issue en GitHub:
https://github.com/alcantaramateojuangabriel-alt/HotelMaguana/issues
