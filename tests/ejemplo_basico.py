from pddl_simulator import *

deposito = Location("deposito")
ubicacion1 = Location("ubicacion1")
ubicacion2 = Location("ubicacion2")

ubicaciones = [deposito, ubicacion1, ubicacion2]

izq = Arm("izq",)
der = Arm("der")

dron1 = Drone("dron1", deposito, [izq, der])

caja1 = Box("caja1", deposito, "comida")
caja2 = Box("caja2", deposito, "medicina")

persona1 = Person("persona1", ubicacion1, "comida")
persona2 = Person("persona2", ubicacion2, "medicina")

contenidos = ['comida', 'medicina']

actions = [
	create_action_load(dron1, izq, caja1, 0, 1, 1),
	create_action_load(dron1, der, caja2, 1, 1, 1),
	create_action_move(dron1, deposito, ubicacion1, 2, 1, 1),
	create_action_unload(dron1, izq, caja1, persona1, 3, 1, 1),
	create_action_move(dron1, ubicacion1, ubicacion2, 4, 1, 1),
	create_action_unload(dron1, der, caja2, persona2, 5, 1, 1),
	create_action_move(dron1, ubicacion2, deposito, 6, 1, 1)
]

drones=[dron1]
boxes=[caja1, caja2]
people=[persona1, persona2]

new_world = World(actions, ubicaciones, drones, boxes, people)