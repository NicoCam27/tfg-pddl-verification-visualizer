# TFG: Software para la verificación y visualización de resultados de Planificación Automática en dominios de logística de drones utilizando PDDL y Python.

## Autor

Iubal Nicolás Camjalli Spiegel

## Requisitos

- Python 3.11 o superior
- Pygame 2.6.1 o superior
  
## Instalación

La biblioteca se puede instalar de dos formas distintas

### Opción 1: Instalación directa desde GitHub

```bash
pip install git+https://github.com/NicoCam27/tfg-pddl-verification-visualizer.git
```

### Opción 2: Instalación desde una copia local del repositorio

Clona el repositorio:

```bash
git clone https://github.com/NicoCam27/tfg-pddl-verification-visualizer.git
cd tfg-pddl-verification-visualizer
```

Instala la biblioteca:

```bash
pip install .
```

## Uso

Una vez instalado el paquete, puede utilizarse directamente mediante:

```python
from pddl_simulator import *
```

Ejemplo básico:

```python
from pddl_simulator import *

izq = Arm("izq", "empty")
der = Arm("der", "empty")

dron1 = Drone("dron1", "deposito", [izq, der])

caja1 = Box("caja1", "deposito", "comida")
caja2 = Box("caja2", "deposito", "medicina")

persona1 = Person("persona1", "ubicacion1", "comida", "nothing")
persona2 = Person("persona2", "ubicacion2", "medicina", "nothing")

ubicaciones = ['deposito', 'ubicacion1', 'ubicacion2']

contenidos = ['comida', 'medicina']

actions = [
	create_action_load(dron1, "izq", caja1, 0, 1, 1),
	create_action_load(dron1, "der", caja2, 1, 1, 1),
	create_action_move(dron1, "deposito", "ubicacion1", 2, 1, 1),
	create_action_unload(dron1, "izq", caja1, persona1, 3, 1, 1),
	create_action_move(dron1, "ubicacion1", "ubicacion2", 4, 1, 1),
	create_action_unload(dron1, "der", caja2, persona2, 5, 1, 1),
	create_action_move(dron1, "ubicacion2", "deposito", 6, 1, 1)
]

drones=[dron1]
boxes=[caja1, caja2]
people=[persona1, persona2]

new_world = World(actions, ubicaciones, drones, boxes, people)
```

## Ejecución

Ejecuta cualquier programa Python que utilice la biblioteca:

```bash
python mi_programa.py
```

## Tecnologías utilizadas

- Python 3.11
- Pygame 2.6.1
- PDDL (Planning Domain Definition Language)
- Git
- GitHub

## Estructura del proyecto

```text
tfg-pddl-verification-visualizer/
├── src/
│   └── pddl_simulator/
│       ├── actions/
│       ├── objects/
│       ├── rendering/
│       ├── simulation/
│       ├── ui/
│       ├── utils/
│       ├── world/
│       └── __init__.py
├── tests/
├── examples/
├── docs/
├── README.md
├── requirements.txt
├── pyproject.toml
└── LICENSE
```

## Licencia

Este proyecto ha sido desarrollado como parte de un Trabajo Fin de Grado (TFG) en Ingeniería Informática.