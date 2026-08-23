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
        error = action.start_execution(self.simulation_time)

        if error is not None:
            self.set_error(error)
            return

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


    def get_render_positions(self, location_positions, drones, conveyors=None):
        positions = {}

        # ---------------------------------------------------------
        # Posición normal de los drones
        # ---------------------------------------------------------
        if drones is not None:
            for drone in drones:
                if drone is not None:
                    if drone.location in location_positions:
                        positions[drone] = location_positions[
                            drone.location
                        ]

        # ---------------------------------------------------------
        # Posición normal de los transportadores
        #
        # Cuando están en una ubicación y NO los transporta un dron,
        # aparecen un poco separados del centro de la ubicación.
        # ---------------------------------------------------------
        if conveyors is not None:
            for conveyor in conveyors:
                if conveyor is not None:
                    if conveyor.location in location_positions:
                        x, y = location_positions[
                            conveyor.location
                        ]

                        # Separación respecto al centro de la ubicación
                        positions[conveyor] = (
                            x - 50,
                            y + 20
                        )

        # ---------------------------------------------------------
        # Sobrescribir con posiciones interpoladas
        # ---------------------------------------------------------
        for action in self.active_actions:

            action_type = action.data.get("action_type")

            if action_type not in ("move", "move_conveyor"):
                continue

            drone = action.data["drone"]
            origin = action.data["origin"]
            destination = action.data["destination"]

            progress = action.progress(self.simulation_time)

            x0, y0 = location_positions[origin]
            x1, y1 = location_positions[destination]

            x = x0 + (x1 - x0) * progress
            y = y0 + (y1 - y0) * progress

            # El dron se mueve visualmente
            positions[drone] = (x, y)

            # -----------------------------------------------------
            # Si el dron está transportando un transportador,
            # el transportador va PEGADO al dron.
            # -----------------------------------------------------
            if action_type == "move_conveyor":
                conveyor = action.data["conveyor"]

                positions[conveyor] = (
                    x,
                    y
                )

        return positions

    
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