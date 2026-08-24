class Simulation:

    def __init__(self, actions, reset_callback=None):

        # Lista de objetos Action
        self.actions = actions

        # Función para restaurar el mundo al estado inicial
        self.reset_callback = reset_callback

        # Tiempo de simulación (segundos)
        self.simulation_time = 0.0

        # Multiplicador de velocidad
        self.speed = 1.0

        # Estado de la simulación
        self.playing = False

        # Acciones que están actualmente ejecutándose
        self.active_actions = []

        # Última acción iniciada (para mostrar en la UI)
        self.last_action_description = "Simulación preparada"

        # Estado de error
        self.error = None



    def update(self, dt):

        if not self.playing or self.has_error():
            return

        self.simulation_time += dt * self.speed

        for action in self.actions:
            if (
                not action.started
                and
                action.start <= self.simulation_time
            ):
                self.start_action(action)

                if self.has_error():
                    return

        for action in self.active_actions[:]:
            if self.simulation_time >= action.end_time:
                self.finish_action(action)

                if self.has_error():
                    return

        if self.finished():
            self.playing = False



    def start_action(self, action):

        action.start_execution(self.simulation_time)

        self.active_actions.append(action)

        self.last_action_description = action.description



    def finish_action(self, action):

        error = action.finish_execution()

        if error is not None:
            self.set_error(error)
            return

        self.active_actions.remove(action)



    def play(self):
        self.playing = True



    def pause(self):
        self.playing = False



    def reset(self):

        self.playing = False

        self.simulation_time = 0.0

        self.active_actions.clear()

        self.error = None

        self.last_action_description = "Simulación reiniciada"

        for action in self.actions:
            action.reset()

        if self.reset_callback:
            self.reset_callback()



    def set_speed(self, speed):
        self.speed = speed
        
    

    def finished(self):

        return all(
            action.finished
            for action in self.actions
        )

    
    def get_step_text(self):

        pending = sum(
            not action.started
            for action in self.actions
        )

        running = sum(
            action.is_running()
            for action in self.actions
        )

        finished = sum(
            action.finished
            for action in self.actions
        )

        return (
            f"Pendientes: {pending} | "
            f"En ejecución: {running} | "
            f"Finalizadas: {finished}/{len(self.actions)}"
        )


    def get_time_text(self):
        return f"Tiempo: {self.simulation_time:.2f} s"


    def get_last_action_description(self):
        return self.last_action_description

    def set_error(self, message):
        self.error = message
        self.playing = False
        self.active_actions.clear()

    def has_error(self):
        return self.error is not None

    def get_error(self):
        return self.error