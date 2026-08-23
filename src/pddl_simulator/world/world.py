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

            render_positions = simulation.get_render_positions(
                renderer.location_positions, drones, conveyors
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
