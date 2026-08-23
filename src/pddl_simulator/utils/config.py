from pathlib import Path

def cargar_configuracion(ruta_archivo: str) -> dict:
    config = {}

    # Verificar si el archivo realmente existe
    if not Path(ruta_archivo).exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_archivo}")

    # Leer el archivo con codificación UTF-8 para evitar problemas con tildes o eñes
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        for num_linea, linea in enumerate(f, 1):
            linea = linea.strip()

            # Ignorar líneas vacías o comentarios
            if not linea or linea.startswith("#"):
                continue

            # Validar que la línea tenga el formato correcto (Clave = Valor)
            if "=" not in linea:
                print(
                    f"[Aviso] Línea {num_linea} ignorada (falta '='): '{linea}'"
                )
                continue

            # Separar por el primer '=' que aparezca
            clave, valor = linea.split("=", 1)
            clave = clave.strip()
            valor = valor.strip()

            # GESTIÓN DE DUPLICADOS:
            # Si la clave ya existe (como recoger_caja), se agrupa en una lista
            if clave in config:
                if isinstance(config[clave], list):
                    config[clave].append(valor)
                else:
                    # Se convierte el valor existente en una lista y se añade el nuevo
                    config[clave] = [config[clave], valor]
            else:
                config[clave] = valor

    return config