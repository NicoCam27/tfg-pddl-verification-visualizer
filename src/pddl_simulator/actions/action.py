class Action:

    def __init__(
        self,
        start,
        duration,
        action_type=None,
        data=None,
        description="",
        on_finish=None 
    ):

        # Información temporal
        self.start = start
        self.duration = duration
        self.end_time = None

        # Tipo de accion y datos adicionales
        self.action_type = action_type
        
        if data is None:
            data = {}
        self.data = data
        

        # Callbacks
        self.on_finish = on_finish

        # Información para el usuario
        self.description = description

        # Estado interno
        self.started = False
        self.finished = False
        self.start_execution_time = None
        

    def reset(self):

        self.started = False
        self.finished = False

        self.start_execution_time = None
        self.end_time = None


    def start_execution(self, simulation_time):

            self.started = True

            self.start_execution_time = simulation_time

            self.end_time = simulation_time + self.duration

    def finish_execution(self):
        
        try:

            if self.on_finish is not None:
                self.on_finish()

            self.finished = True
            return None

        except ValueError as e:
            return str(e)
        
        except TypeError as e:
            return str(e)

        except Exception as e:
            return str(e)
        

    def is_running(self):

        return self.started and not self.finished

    def progress(self, simulation_time):

        if not self.started:
            return 0.0

        if self.finished:
            return 1.0
        
        return min(
            1.0,
            (simulation_time - self.start_execution_time)
            / self.duration
        )