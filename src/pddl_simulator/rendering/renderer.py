import math
import pygame
from collections import defaultdict


class Renderer:
    def __init__(self, width=1500, height=800):
        pygame.init()

        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Simulación PDDL")

        self.font = pygame.font.SysFont(None, 24)
        self.small_font = pygame.font.SysFont(None, 20)

        self.location_positions = {}

    def compute_locations(self, locations):

        margin = 80

        n = len(locations)

        cols = math.ceil(math.sqrt(n))
        rows = math.ceil(n / cols)

        cell_w = (self.width - 2 * margin) / cols
        cell_h = (self.height - 2 * margin) / rows

        self.location_positions.clear()

        for i, location in enumerate(locations):
            row = i // cols
            col = i % cols

            x = margin + col * cell_w + cell_w / 2
            y = margin + row * cell_h + cell_h / 2

            self.location_positions[location] = (int(x), int(y))

    def is_box_carried(self, box, drones):

        if drones is None:
            return False

        for drone in drones:
            for arm in drone.arms:
                if arm.content == box.name:
                    return True

        return False
    
    def is_box_in_conveyor(self, box, conveyors):
        if conveyors is None:
            return False

        for conveyor in conveyors:
            if box in conveyor.boxes_inside:
                return True

        return False
    

    def draw(self, render_positions, drones = None, boxes = None, people = None, conveyors = None):

        self.screen.fill((240, 240, 240))


        # Dibujar Ubicaciones
        for location, (x, y) in self.location_positions.items():

            pygame.draw.circle(self.screen, (80,80,80), (x,y), 65)

            text = self.font.render(location, True, (255,255,255))
            rect = text.get_rect(center=(x,y))

            self.screen.blit(text, rect)

        
        # Dibujar Cajas
        if boxes is not None:
            for box in boxes:

                # -------------------------------------------------
                # No dibujar cajas que lleva un dron
                # -------------------------------------------------
                if self.is_box_carried(box, drones):
                    continue

                # -------------------------------------------------
                # No dibujar cajas que están dentro de un transportador
                # -------------------------------------------------
                if self.is_box_in_conveyor(box, conveyors):
                    continue

                # -------------------------------------------------
                # Dibujar cajas que están libres
                # -------------------------------------------------
                if box.location not in self.location_positions:
                    continue

                x, y = self.location_positions[box.location]

                pygame.draw.rect(
                    self.screen,
                    (180, 120, 0),
                    (x - 10, y + 40, 20, 20)
                )

        # Dibujar transportadores
        if conveyors is not None:
            for conveyor in conveyors:

                if conveyor not in render_positions:
                    continue

                x, y = render_positions[conveyor]

                # Rectangulo de Transportador
                conveyor_rect = pygame.Rect(
                    int(x) - 50,
                    int(y) + 10,
                    20,
                    20
                )

                pygame.draw.rect(
                    self.screen,
                    (240, 70, 70),
                    conveyor_rect
                )

                # -------------------------------------------------
                # Número de cajas dentro del transportador
                # -------------------------------------------------
                boxes_count = conveyor.get_number_of_boxes_inside()

                count_text = self.small_font.render(
                    str(boxes_count),
                    True,
                    (0, 0, 0)
                )

                count_rect = count_text.get_rect(
                    center=(
                        conveyor_rect.centerx,
                        conveyor_rect.top - 10
                    )
                )

                self.screen.blit(count_text, count_rect)

                # -------------------------------------------------
                # Tooltip
                # -------------------------------------------------
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if conveyor_rect.collidepoint(mouse_x, mouse_y):

                    boxes_inside = conveyor.boxes_inside

                    lines = []

                    if not boxes_inside:
                        lines.append(conveyor.name)
                    else:
                        lines.append(conveyor.name)

                        for box in boxes_inside:
                            lines.append(
                                f"{box.name} | {box.content}"
                            )

                    padding = 6
                    line_height = 20

                    width = max(
                        self.small_font.size(line)[0]
                        for line in lines
                    ) + padding * 2

                    height = (
                        len(lines) * line_height
                        + padding * 2
                    )

                    tooltip_x = conveyor_rect.right + 10
                    tooltip_y = conveyor_rect.top

                    if tooltip_x + width > self.width:
                        tooltip_x = (
                            conveyor_rect.left
                            - width
                            - 10
                        )

                    if tooltip_y + height > self.height:
                        tooltip_y = (
                            self.height
                            - height
                            - 10
                        )

                    pygame.draw.rect(
                        self.screen,
                        (255, 255, 220),
                        (tooltip_x, tooltip_y, width, height)
                    )

                    pygame.draw.rect(
                        self.screen,
                        (0, 0, 0),
                        (tooltip_x, tooltip_y, width, height),
                        1
                    )

                    for i, line in enumerate(lines):

                        text = self.small_font.render(
                            line,
                            True,
                            (0, 0, 0)
                        )

                        self.screen.blit(
                            text,
                            (
                                tooltip_x + padding,
                                tooltip_y
                                + padding
                                + i * line_height
                            )
                        )

        if people is not None:
            people_by_location = defaultdict(list)

            for person in people:
                people_by_location[person.location].append(person)
                
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Dibujar personas
            for location, people_in_location in people_by_location.items():

                if location not in self.location_positions:
                    continue

                x, y = self.location_positions[location]

                # Dibujar un circulo verde que representa a todas las personas en esa ubicación
                radius = 10
                person_x = x
                person_y = y - 45

                pygame.draw.circle(
                    self.screen,
                    (0, 180, 0),
                    (person_x, person_y),
                    radius
                )

                # Mostrar el número de personas
                count_text = self.small_font.render(
                    str(len(people_in_location)),
                    True,
                    (255, 255, 255)
                )

                count_rect = count_text.get_rect(center=(person_x, person_y))
                self.screen.blit(count_text, count_rect)

                # ----------------------------------------------------
                # Tooltip que se muestra cuando el cursor flota sobre el círculo verde
                # ----------------------------------------------------
                if (mouse_x - person_x) ** 2 + (mouse_y - person_y) ** 2 <= radius ** 2:

                    lines = []

                    for person in people_in_location:

                        if person.possesses == "nothing":
                            lines.append(person.name)

                        elif person.get_is_possesses_a_list():
                            box_found = False
                            if person.get_possesses_at_least_one_object():
                                for element in person.possesses:
                                    if element != "nothing":
                                        lines.append(
                                            f"{person.name} | {element.name} | {element.content}"
                                        )
                                        box_found = True

                            if not box_found:
                                lines.append(person.name)

                        else:
                            box = person.possesses
                            
                            lines.append(
                                f"{person.name} | {box.name} | {box.content}"
                            )


                    padding = 6
                    line_height = 20

                    width = max(
                        self.small_font.size(line)[0]
                        for line in lines
                    ) + padding * 2

                    height = len(lines) * line_height + padding * 2

                    tooltip_x = person_x + 20
                    tooltip_y = person_y - 10

                    # Evita que el tooltip salga de la pantalla
                    if tooltip_x + width > self.width:
                        tooltip_x = person_x - width - 20

                    if tooltip_y + height > self.height:
                        tooltip_y = self.height - height - 10

                    # Fondo
                    pygame.draw.rect(
                        self.screen,
                        (255, 255, 220),
                        (tooltip_x, tooltip_y, width, height)
                    )

                    # Bordes
                    pygame.draw.rect(
                        self.screen,
                        (0, 0, 0),
                        (tooltip_x, tooltip_y, width, height),
                        1
                    )

                    # Dibuja cada línea
                    for i, line in enumerate(lines):

                        text = self.small_font.render(
                            line,
                            True,
                            (0, 0, 0)
                        )

                        self.screen.blit(
                            text,
                            (
                                tooltip_x + padding,
                                tooltip_y + padding + i * line_height
                            )
                        )

        
        # Dibujar drones
        if drones is not None:
            for drone in drones:

                if drone.location not in self.location_positions:
                    continue

                x, y = render_positions[drone]

                # Dibujar el dron
                pygame.draw.rect(
                    self.screen,
                    (50, 120, 255),
                    (int(x) - 15, int(y) - 15, 30, 30)
                )

                # Nombre del dron
                text = self.font.render(
                    drone.name,
                    True,
                    (0, 0, 0)
                )
                self.screen.blit(text, (int(x) - 20, int(y) - 40))

                # Texto informativo
                text_offset = 25

                for arm in drone.arms:

                    if arm.content == "empty":
                        continue

                    box = arm.content

                    # Posición de la caja junto al dron
                    dx, dy = (10, 0)

                    box_x = int(x + dx)
                    box_y = int(y + dy)

                    # Dibujar la caja
                    pygame.draw.rect(
                        self.screen,
                        (180, 120, 0),
                        (box_x, box_y, 16, 16)
                    )

                    # Información de la caja
                    txt = self.small_font.render(
                        f"{arm.name} | {arm.content}",
                        True,
                        (150, 0, 0)
                    )

                    self.screen.blit(
                        txt,
                        (int(x) + 25, int(y) + text_offset)
                    )

                    text_offset += 18        
                

    def draw_error(self, error):
        if error is None:
            return

        error_font = pygame.font.SysFont(None, 26)

        text = error_font.render(
            f"Error: {error}",
            True,
            (220, 0, 0)
        )

        padding = 10

        rect = text.get_rect(
            centerx=self.width // 2,
            top=10
        )

        background = pygame.Rect(
            rect.left - padding,
            rect.top - padding,
            rect.width + padding * 2,
            rect.height + padding * 2
        )

        pygame.draw.rect(
            self.screen,
            (255, 230, 230),
            background
        )

        pygame.draw.rect(
            self.screen,
            (220, 0, 0),
            background,
            2
        )

        self.screen.blit(text, rect)