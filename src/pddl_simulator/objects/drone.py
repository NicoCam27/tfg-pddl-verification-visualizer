# POSIBLES MEJORAS O CAMBIOS:

# - Al recoger y dejar una caja, en vez de mencionar el brazo por su nombre, pasar directamente el objeto brazo, para evitar errores
#   de que el nombre del brazo no exista o esté mal escrito.
#   Esto también haría que el código sea más limpio, porque no habría que recorrer la lista de brazos para encontrar el brazo con ese nombre.

#El objeto de tipo "drone" tiene "ubicacion" (un string) y "brazos" (puede tener uno o varios brazos,
#                                                                   cada brazo puede tener una caja o no tener nada)
class Drone:
    def __init__(self, name, location = "", arms = None):

        if arms is None:
            arms = []

        self.name = name
        self.location = location
        if len(arms) == len(set(arms)):
            self.arms = arms
        else:
            raise Exception("Los brazos de un dron deben ser únicos, un brazo específico no puede aparecer mas de una vez")

        self.__initial_location = location

    def move(self, origin, destination, duration = 1, cost = 1):
        if self.location != origin:
            raise ValueError(f"the drone {self.name} is not in the location {origin}")
        print(f"The drone {self.name} is moving from {origin} to {destination}")
        self.location = destination
        return duration, cost

    def move_conveyor(self, conveyor, origin, destination, duration = 1, cost = 1):
        if self.location != origin:
            raise ValueError(f"the drone {self.name} is not in the location {origin}")
        elif self.location != conveyor.location:
            raise ValueError(f"the drone {self.name} is not in the same location ({self.location}) as the conveyor {conveyor.name} ({conveyor.location})")
        if not conveyor.try_move(self):
            owner = conveyor.get_current_owner()
            raise ValueError(f"the conveyor {conveyor.name} is already being moved by {owner.name}")
        print(f"The drone {self.name} is moving from {origin} to {destination} with conveyor {conveyor.name}")

        self.location = destination
        conveyor.location = destination

        conveyor.release(self)

        return duration, cost
    

    # Cuando se carga una caja, se verifica que tanto la caja como el
    # dron estén en la misma ubicación, y que el brazo esté vacío.
    #
    # box tiene que ser un objeto de tipo Box, no un string con el nombre de la caja,
    # porque se necesita acceder a su ubicación para verificar que esté en la misma ubicación que el dron
    def load(self, arm_name, box, duration = 1, cost = 1):
        arm = None
        arm_occupied = False
        for arm_observed in self.arms:
            if arm_observed.name == arm_name:
                if arm_observed.content != "empty":
                    arm_occupied = True
                    raise ValueError(f"the arm {arm_name} is already occupied - it has {arm_observed.content}")
                else:
                    arm = arm_observed
        if arm is None:
            raise ValueError(f"the drone {self.name} does not have an arm called {arm_name}")
        if self.location != box.location:
            raise ValueError(f"the drone {self.name} is in location {self.location} but the box {box.name} is in location {box.location}")
        # Se verifica que la caja no está siendo sujetada por algún otro dron o está en algún transportador
        if arm_occupied:
            raise ValueError(f"the arm {arm_name} is already occupied and can't pick up {box.name}")
        if not box.try_pickup(self):
            raise ValueError(f"the box {box.name} can't be picked up, it is in {box.get_current_owner().name}")
        else:
            arm.content = box.name
            print(f"The box {box.name} is now loaded in the arm {arm_name} of the drone {self.name}")
            return duration, cost
        

    # Cuando se descarga una caja y se entrega a una persona,
    # el brazo queda vacío y la caja queda en la ubicación del drone.
    #
    # Se verifica que el drone y la persona estén en la misma ubicación,
    # que el brazo tenga la caja que se quiere descargar, y que la persona tenga
    # la necesidad de esa caja (es decir, que el contenido de la caja sea igual a la necesidad de la persona)
    def unload(self, arm_name, box, person, duration = 1, cost = 1):
        if self.location != person.location:
            raise ValueError(f"the drone {self.name} is in location {self.location} but the person {person.name} is in location {person.location}")
        for arm in self.arms:
            if arm.name == arm_name:
                if arm.content != box.name:
                    raise ValueError(f"the arm {arm_name} isn't holding {box.name}. {box.get_current_owner().name} has the box")
                if not box.content in person.needs:
                    raise ValueError(f"the person {person.name} does not need the content of the box {box.name} - it needs {person.needs} but the box has {box.content}")
                if not box.release(self):
                    raise ValueError(f"the box {box.name} is not owned by the drone {self.name}")
                arm.content = "empty"
                box.location = self.location

                person.add_possesses(box)
                print(f"The box {box.name} has been unloaded from the arm {arm_name} of the drone {self.name} and given to the person {person.name}")
                return duration, cost
        raise ValueError(f"the drone {self.name} does not have an arm called {arm_name}")
        

    # Cuando se suelta una caja sin entregarla a una persona,
    # el brazo queda vacío y la caja queda en la ubicación del drone.
    def drop(self, arm_name, box, duration = 1, cost = 1):
        for arm in self.arms:
            if arm.name == arm_name:
                if arm.content != box.name:
                    raise ValueError(f"the arm {arm_name} isn't holding {box.name}. {box.get_current_owner().name} has the box")
                if not box.release(self):
                    raise ValueError(f"the box {box.name} is not owned by the drone {self.name}")

                arm.content = "empty"
                box.location = self.location
                print(f"The box {box.name} has been dropped from the arm {arm_name} of the drone {self.name} in the location {self.location}")
                return duration, cost
        raise ValueError(f"the drone {self.name} does not have an arm called {arm_name}")


    # Cuando se carga una caja en un transportador, se verifica que la caja,
    # el dron y el transportadorestén en la misma ubicación, y que el brazo esté vacío.
    #
    # box tiene que ser un objeto de tipo Box, no un string con el nombre
    # de la caja, porque se necesita acceder a su ubicación para verificar
    # que esté en la misma ubicación que el dron y el transportador.
    #
    # conveyor tiene que ser un objeto de tipo Conveyor, debido a que se accede
    # a información como la ubicación, cajas cargadas, y capacidad máxima
    def load_conveyor_with_box(self, arm_name, box, conveyor, duration = 1, cost = 1):
        if self.location != box.location:
            raise ValueError(f"the drone {self.name} is in location {self.location} but the box {box.name} is in location {box.location}")
        elif self.location != conveyor.location:
            raise ValueError(f"the drone {self.name} is not in the same location ({self.location}) the conveyor {conveyor.name} is in ({conveyor.location})")

        for arm in self.arms:
            if arm.name == arm_name:
                if arm.content != box.name:
                    raise ValueError(f"the arm {arm_name} isn't holding {box.name}. {box.get_current_owner().name} has the box")
                if conveyor.get_number_of_boxes_inside() == conveyor.capacity:
                    raise ValueError(f"the conveyor {conveyor.name} has reached its maximum capacity = {conveyor.capacity}")
                arm.content = "empty"

                # ---------------- es necesario hacer esto?
                #box.location = self.location
                # ----------------

                # Se verifica que se haya podido cargar correctamente la caja en el transportador y de que no se está intentando
                # meter una caja que ya está dentro del transportador.
                if (not box.release(self)):
                    raise ValueError(f"the box {box.name} is not owned by the drone {self.name}, it is owned by {box.get_current_owner().name}")
                if (not box.try_pickup(conveyor)):
                    raise ValueError(f"the box {box.name} can't be loaded into {conveyor.name}, it is owned by {box.get_current_owner().name}")
                if (conveyor.add_box(box)):
                    print(f"The box {box.name} has been loaded from the arm {arm_name} of the drone {self.name} into the conveyor {conveyor.name} which currently has {conveyor.get_number_of_boxes_inside()} boxes inside")
                    return duration, cost
                else:
                    raise ValueError(f"the box {box.name} is not in {arm_name} - it is in {box.get_current_owner().name}")
        raise ValueError(f"the drone {self.name} does not have an arm called {arm_name}")


    # Cuando se carga una caja de un transportador a un dron,
    # se verifica que la caja, el dron y el transportador
    # están en la misma ubicación, y que el brazo esté vacío.
    #
    # box tiene que ser un objeto de tipo Box, no un string con el nombre
    # de la caja, porque se necesita acceder a su ubicación para verificar
    # que esté en la misma ubicación que el dron y el transportador.
    #
    # conveyor tiene que ser un objeto de tipo Conveyor, debido a que se accede
    # a información como la ubicación, cajas cargadas, y capacidad máxima
    def unload_box_from_conveyor(self, arm_name, box, conveyor, duration = 1, cost = 1):
        if self.location != box.location:
            raise ValueError(f"the drone {self.name} is in location {self.location} but the box {box.name} is in location {box.location}")
        elif self.location != conveyor.location:
            raise ValueError(f"the drone {self.name} is not in the same location ({self.location}) the conveyor {conveyor.name} is in ({conveyor.location})")
        for arm in self.arms:
            if arm.name == arm_name:
                if arm.content != "empty":
                    raise ValueError(f"the arm {arm_name} is already occupied - it has {arm.content}")
                if (not box.release(conveyor)):
                    raise ValueError(f"the box {box.name} is not owned by the transporter {conveyor.name}, it is owned by {box.get_current_owner().name}")
                if (not box.try_pickup(self)):
                    raise ValueError(f"the box {box.name} can't be picked up by the drone {self.name}, it is owned by {box.get_current_owner().name}")
                if (conveyor.remove_box(box)):
                    arm.content = box.name
                    print(f"The box {box.name} is now loaded in the arm {arm_name} of the drone {self.name}, the conveyor {conveyor.name} currently has {conveyor.get_number_of_boxes_inside()} boxes inside")
                    return duration, cost
                else:
                    raise ValueError(f"The box {box.name} is not available to load")
        raise ValueError(f"the drone {self.name} does not have an arm called {arm_name}")


    def __str__(self):
        infoArms = ""
        for arm in self.arms:
            infoArms += f"  - {arm}\n"
        return f"Drone(name={self.name}, location={self.location}, arms=\n{infoArms})"
    
    def add_arm(self, arm):
        self.arms.append(arm)

    #RESET
    def reset(self):
        self.location = self.__initial_location
        for arm in self.arms:
            arm.reset()