import keyword
import re

from pathlib import Path

def limpiar_nombre_variable(nombre: str) -> str:
    # 1. Eliminar espacios en blanco al inicio y al final
    nombre_limpio = nombre.strip()

    # 2. Reemplazar espacios, guiones y puntuación común por un guion bajo
    # Convierte "mi-variable genial!" en "mi_variable_genial_"
    nombre_limpio = re.sub(
        r"[-\s\.\,\!\@\#\$\%\^\&\*\(\)\+=\{\}\[\]\|\\:\;\"\'\<_]+",
        "_",
        nombre_limpio,
    )

    # 3. Eliminar cualquier carácter que NO sea alfanumérico o guion bajo
    nombre_limpio = re.sub(r"[^a-zA-Z0-9_]", "", nombre_limpio)

    # 4. Si el nombre quedó vacío tras la limpieza, asignamos uno por defecto
    if not nombre_limpio:
        nombre_limpio = "variable"

    # 5. Si empieza con un número, le añadimos un guion bajo al principio
    if nombre_limpio[0].isdigit():
        nombre_limpio = f"_{nombre_limpio}"

    # 6. Comprobar si es una palabra reservada de Python (o constantes como True/False/None)
    if keyword.iskeyword(nombre_limpio) or nombre_limpio in [
        "True",
        "False",
        "None",
    ]:
        nombre_limpio = f"{nombre_limpio}_var"

    nombre_limpio = nombre_limpio.strip("_")

    # Si al limpiar los guiones quedó vacío o volvió a empezar con número, se corrige
    if not nombre_limpio:
        nombre_limpio = "variable"
    elif nombre.strip() and nombre.strip()[0].isdigit():
        nombre_limpio = f"_{nombre_limpio}"

    return nombre_limpio



def is_filename_valid(file_name: str) -> bool:
    # 1. Se comprueba que no esté vacío y no sea demasiado largo 
    # (El límite general en la mayoría de sistemas es de 255 caracteres)
    if not file_name or len(file_name) > 255:
        return False
    
    # 2. Caracteres prohibidos globalmente o que causan problemas
    # Se prohiben barras ( / \ ), caracteres de control, y reservados de Windows ( < > : " | ? * )
    forbidden_characters = r'[\/\\:\*\?"<>\|\x00-\x1f]'
    if re.search(forbidden_characters, file_name):
        return False
    
    # 3. Nombres reservados en Windows
    reserved_names = {
        "CON", "PRN", "AUX", "NUL",
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }
    # Se extrae la base del nombre sin la extensión (ej: de "CON.txt" saca "CON")
    name_base = Path(file_name).stem.upper()
    if name_base in reserved_names:
        return False
        
    # 4. No puede terminar en espacio o en punto (regla de Windows)
    if file_name.endswith(' ') or file_name.endswith('.'):
        return False

    # 5. La prueba de fuego con Pathlib
    # Se intenta "renderizar" la ruta de manera estricta para ver si el OS protesta
    try:
        # Path('.') / file_name crea una ruta relativa simulada
        # match() verifica si la sintaxis de la ruta es válida para el sistema actual
        Path(file_name).touch(exist_ok=True) # Opcional: Esto crearía el archivo vacío para asegurar
        return True
    except (ValueError, OSError):
        return False