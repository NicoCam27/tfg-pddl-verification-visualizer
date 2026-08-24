import pygame
from pddl_simulator.objects.reset_world import *
from pddl_simulator.rendering.renderer import Renderer
from pddl_simulator.ui.ui import ControlPanel
from pddl_simulator.simulation import Simulation

class World:
    def __init__(self, actions, ubicaciones, drones = None, boxes = None, people = None, conveyors = None):
        renderer = Renderer()
        renderer.compute_locations(ubicaciones)
        control = ControlPanel(renderer.width, renderer.height)

        clock = pygame.time.Clock()


        simulation = Simulation(
            actions,
            reset_callback=lambda: reset_world(drones, boxes, people, conveyors)
        )


# HACER ESTO EN EL PROYECTO FINAL!!!!!!!

# ---------------- IMPLEMENTAR ESTO PERO CON EL NUEVO TIPO DE actions creados ----------------------------
# Por qué es importante implementar esto?
#
# Respuesta: Esta es una verificación para ver que todos los drones, transportadores y etc. que aparecen
#            acciones se pasaron como objetos y que no falta nada 
#
#        # Se verifica que todos los objetos mencionados en action se han pasado correctamente a world
#        for action in actions:
#            action_type = action.get_data().get("action_type")
#            if action_type == "move":
#                if drones is None:
#                    print("NO SE HAN PASADO DRONES")
#                else:
#                    if action.get_data().get("drone") in drones:
#                        print("Se confirma que el dron ", action.get_data().get("drone").name, " se ha pasado en las listas")
#                    else:
#                        print("el drone: ", action.get_data().get("drone").name, " no se ha pasado en la lista de objetos")
#            elif action_type == "move_conveyor":
#                if drones is None:
#                    print("NO SE HAN PASADO DRONES")
#                elif conveyors is None:
#                    print("NO SE HAN PASADO TRANSPORTADORES")
#                else:
#
#                    if (action.get_data().get("drone") not in drones):
#                        print("el drone: ", action.get_data().get("drone").name, " no se ha pasado en la lista de objetos")
#                    if (action.get_data().get("conveyor") not in conveyors):
#                        print("el transportador: ", action.get_data().get("conveyor").name, " no se ha pasado en la lista de objetos")
#                    else:
#                        print(
#                            "Se confirma que el dron ",
#                            action.get_data().get("drone").name,
#                            " se ha pasado en las listas correctamente, al igual que el transportador ",
#                            action.get_data().get("conveyor").name
#                            )
                        
            #if list is not None:
            #    print(action.get_data().get("drone"))

        running = True


        while running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                action = control.handle_event(event)
                
                if action == "play":
                    if not simulation.has_error():
                        simulation.play()

                elif action == "pause":
                    if not simulation.has_error():
                        simulation.pause()

                elif action == "reset":
                    simulation.reset()


            dt = clock.tick(60) / 250.0

            simulation.set_speed(control.slider.value)
            simulation.update(dt)

            render_positions = renderer.get_render_positions(
                simulation, drones, conveyors
            )

            renderer.draw(
                render_positions,
                drones,
                boxes,
                people,
                conveyors
            )

            control.draw(renderer.screen, simulation)

            if simulation.has_error():
                renderer.draw_error(simulation.get_error())

            pygame.display.flip()

            
        pygame.quit()
