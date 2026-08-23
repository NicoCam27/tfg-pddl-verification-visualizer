import pygame


# --------------------------------------------------
# Botón
# --------------------------------------------------
class Button:

    def __init__(self, x, y, width, height, text):

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

        self.font = pygame.font.SysFont(None, 24)

        self.enabled = True

    def draw(self, screen):

        color = (180, 180, 180)

        if not self.enabled:
            color = (120, 120, 120)

        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=8)

        text = self.font.render(self.text, True, (0, 0, 0))

        screen.blit(
            text,
            text.get_rect(center=self.rect.center)
        )

    def clicked(self, event):

        if not self.enabled:
            return False

        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


# --------------------------------------------------
# Slider
# --------------------------------------------------
class Slider:

    def __init__(self, x, y, width):

        self.x = x
        self.y = y
        self.width = width

        self.height = 4
        self.radius = 10

        self.dragging = False

        self.values = [
            0.25,
            0.5,
            1,
            2,
            4,
            8,
            16
        ]

        self.index = 2      # Empieza en 1x

        self.font = pygame.font.SysFont(None, 22)

    @property
    def value(self):
        return self.values[self.index]

    def draw(self, screen):

        pygame.draw.line(
            screen,
            (50, 50, 50),
            (self.x, self.y),
            (self.x + self.width, self.y),
            self.height
        )

        step = self.width / (len(self.values) - 1)

        knob_x = self.x + self.index * step

        pygame.draw.circle(
            screen,
            (70, 130, 255),
            (int(knob_x), self.y),
            self.radius
        )

        text = self.font.render(
            f"Velocidad: {self.value}x",
            True,
            (0, 0, 0)
        )

        screen.blit(text, (self.x, self.y + 20))

    def handle_event(self, event):

        step = self.width / (len(self.values) - 1)

        knob_x = self.x + self.index * step

        if event.type == pygame.MOUSEBUTTONDOWN:

            if (
                (event.pos[0] - knob_x) ** 2
                + (event.pos[1] - self.y) ** 2
                <= self.radius ** 2
            ):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:

            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:

            if self.dragging:

                x = min(max(event.pos[0], self.x), self.x + self.width)

                self.index = round((x - self.x) / step)


# --------------------------------------------------
# Panel de Control
# --------------------------------------------------
class ControlPanel:

    def __init__(self, screen_width, screen_height):

        y = screen_height - 70

        self.play_button = Button(200, y, 140, 40, "Reproducir")
        self.pause_button = Button(360, y, 120, 40, "Pausa")
        self.reset_button = Button(500, y, 140, 40, "Reiniciar")

        self.info_font = pygame.font.SysFont(None, 22)

        self.slider = Slider(700, y + 20, 300)

    def draw(self, screen, simulation):

        self.play_button.draw(screen)
        self.pause_button.draw(screen)
        self.reset_button.draw(screen)
        self.slider.draw(screen)

        step_text = self.info_font.render(
            simulation.get_step_text(),
            True,
            (0, 0, 0)
        )

        action_text = self.info_font.render(
            simulation.get_last_action_description(),
            True,
            (0, 0, 0)
        )

        screen.blit(step_text, (20, self.play_button.rect.y - 50))
        screen.blit(action_text, (20, self.play_button.rect.y - 25))

    def handle_event(self, event):

        self.slider.handle_event(event)

        if self.play_button.clicked(event):
            return "play"

        if self.pause_button.clicked(event):
            return "pause"

        if self.reset_button.clicked(event):
            return "reset"

        return None