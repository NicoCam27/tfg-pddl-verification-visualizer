from pddl_simulator import *

deposito = Location("deposito")
ubicacion1 = Location("ubicacion1")
ubicacion2 = Location("ubicacion2")

ubicaciones = [deposito, ubicacion1, ubicacion2]

izq = Arm("izq")
der = Arm("der")

dron1 = Drone("dron1", deposito, [izq, der])

caja1 = Box("caja1", deposito, "comida")
caja2 = Box("caja2", deposito, "medicina")

conveyor1 = Conveyor("conveyor1", 2, [], deposito)

persona1 = Person("persona1", ubicacion1, "comida")
persona2 = Person("persona2", ubicacion2, "medicina")

contenidos = ['comida', 'medicina']

actions = [
	create_action_load(dron1, izq, caja1, 0, 1, 1),
	create_action_load_conveyor_with_box(dron1, izq, caja1, conveyor1, 1, 1, 1),
	create_action_load(dron1, der, caja2, 2, 1, 1),
	create_action_load_conveyor_with_box(dron1, der, caja2, conveyor1, 3, 1, 1),
	create_action_move_conveyor(dron1, conveyor1, izq, deposito, ubicacion1, 4, 1, 1),
	create_action_unload_box_from_conveyor(dron1, izq, caja1, conveyor1, 5, 1, 1),
	create_action_unload(dron1, izq, caja1, persona1, 6, 1, 1),
	create_action_move_conveyor(dron1, conveyor1, izq, ubicacion1, ubicacion2, 7, 1, 1),
	create_action_unload_box_from_conveyor(dron1, izq, caja2, conveyor1, 8, 1, 1),
	create_action_unload(dron1, izq, caja2, persona2, 9, 1, 1),
	create_action_move(dron1, ubicacion2, deposito, 10, 1, 1)
]

drones=[dron1]
boxes=[caja1, caja2]
people=[persona1, persona2]
conveyors=[conveyor1]

new_world = World(actions, ubicaciones, drones, boxes, people, conveyors)
