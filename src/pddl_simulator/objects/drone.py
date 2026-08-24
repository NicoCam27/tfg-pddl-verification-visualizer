from .arm import Arm
from .box import Box
from .conveyor import Conveyor
from .location import Location
from .person import Person


#El objeto de tipo "drone" tiene "ubicacion" (un string) y "brazos" (puede tener uno o varios brazos,
#                                                                   cada brazo puede tener una caja o no tener nada)
class Drone:
    def __init__(self, name, location = None, arms = None):

        if arms is None:
            arms = []

        self.name = name
        if len(arms) == len(set(arms)):
            self.arms = arms
        else:
            raise Exception("Los brazos de un dron deben ser únicos, un brazo específico no puede aparecer mas de una vez")

        self.location = location

        self.__initial_location = location

    def move(self, origin, destination, duration = 1, cost = 1):
        if not isinstance(origin, Location):
            raise ValueError(f"the drone {self.name} expected a Location object for 'origin' but got {origin!r}")
        if not isinstance(destination, Location):
            raise ValueError(f"the drone {self.name} expected a Location object for 'destination' but got {destination!r}")
        
        if self.location != origin:
            raise ValueError(f"the drone {self.name} is not in the location {origin}")
        
        print(f"The drone {self.name} is moving from {origin} to {destination}")
        self.location = destination
        return duration, cost

    def move_conveyor(self, conveyor, arm, origin, destination, duration = 1, cost = 1):
        if not isinstance(conveyor, Conveyor):
            raise ValueError(f"the drone {self.name} expected a Conveyor object for 'conveyor' but got {conveyor!r}")
        if not isinstance(arm, Arm):
            raise ValueError(f"the drone {self.name} expected an Arm object for 'arm' but got {arm!r}")
        if not isinstance(origin, Location):
            raise ValueError(f"the drone {self.name} expected a Location object for 'origin' but got {origin!r}")
        if not isinstance(destination, Location):
            raise ValueError(f"the drone {self.name} expected a Location object for 'destination' but got {destination!r}")

        if self.location != origin:
            raise ValueError(f"the drone {self.name} is not in the location {origin}")
        elif self.location != conveyor.location:
            raise ValueError(f"the drone {self.name} is not in the same location ({self.location}) as the conveyor {conveyor.name} ({conveyor.location})")
        
        if arm in self.arms:
            if arm.content is not None:
                raise ValueError(f"the arm {arm.name} is already occupied - it has {arm.content}")
            else:
                # Se verifica que el transportador no está siendo sujetado por algún otro dron
                if not conveyor.try_move(self):
                    raise ValueError(f"the conveyor {conveyor.name} is already being moved by {conveyor.get_current_owner().name}")
                else:
                    print(f"The drone {self.name} is moving from {origin} to {destination} with conveyor {conveyor.name}")

                    self.location = destination
                    conveyor.location = destination

                    conveyor.release(self)

                    return duration, cost
        else:
            raise ValueError(f"the drone {self.name} does not have an arm called {arm.name}")
    

    # Cuando se carga una caja, se verifica que tanto la caja como el
    # dron estén en la misma ubicación, y que el brazo esté vacío.
    #
    # box tiene que ser un objeto de tipo Box porque se necesita acceder a su ubicación
    # para verificar que esté en la misma ubicación que el dron.
    def load(self, arm, box, duration = 1, cost = 1):
        if not isinstance(arm, Arm):
            raise ValueError(f"the drone {self.name} expected an Arm object for 'arm' but got {arm!r}")
        if not isinstance(box, Box):
            raise ValueError(f"the drone {self.name} expected a Box object for 'box' but got {box!r}")

        if self.location != box.location:
            raise ValueError(f"the drone {self.name} is in location {self.location} but the box {box.name} is in location {box.location}")

        if arm in self.arms:
            # Se verifica que la caja no está siendo sujetada por algún otro dron o está en algún transportador
            if arm.content is not None:
                raise ValueError(f"the arm {arm.name} is already occupied - it has {arm.content}")
            else:
                if not box.try_pickup(self):
                    raise ValueError(f"the box {box.name} can't be picked up, it is in {box.get_current_owner().name}")
                else:
                    arm.content = box
                    print(f"The box {box.name} is now loaded in the arm {arm.name} of the drone {self.name}")
                    return duration, cost
        else:
            raise ValueError(f"the drone {self.name} does not have an arm called {arm.name}")


    # Cuando se descarga una caja y se entrega a una persona,
    # el brazo queda vacío y la caja queda en la ubicación de la persona a la que se le ha entregado la caja.
    #
    # Se verifica que el drone y la persona estén en la misma ubicación,
    # que la persona necesite el contenido de esa caja (necesidad de la persona = contenido de la caja)
    # y que el brazo tenga la caja que se quiere descargar
    def unload(self, arm, box, person, duration = 1, cost = 1):
        if not isinstance(arm, Arm):
            raise ValueError(f"the drone {self.name} expected an Arm object for 'arm' but got {arm!r}")
        if not isinstance(box, Box):
            raise ValueError(f"the drone {self.name} expected a Box object for 'box' but got {box!r}")
        if not isinstance(person, Person):
            raise ValueError(f"the drone {self.name} expected a Person object for 'person' but got {person!r}")
        
        if self.location != person.location:
            raise ValueError(f"the drone {self.name} is in location {self.location} but the person {person.name} is in location {person.location}")
        # "needs" puede ser una lista de contenidos o un único contenido (str),
        if isinstance(person.needs, list):
            needs_content = box.content in person.needs
        else:
            needs_content = person.needs is not None and box.content == person.needs
        if not needs_content:
            raise ValueError(f"the person {person.name} does not need the content of the box {box.name} - it needs {person.needs} but the box has {box.content}")

        if arm in self.arms:
            if arm.content != box:
                raise ValueError(f"the arm {arm.name} isn't holding {box.name}. It is holding {arm.content}")
            if not box.release(self):
                raise ValueError(f"the box {box.name} is not owned by the drone {self.name}")
            box.delivered_to(person)
            arm.content = None
            box.location = person.location
            person.add_possesses(box)
            print(f"The box {box.name} has been unloaded from the arm {arm.name} of the drone {self.name} and given to the person {person.name}")
            return duration, cost
        else:
            raise ValueError(f"the drone {self.name} does not have an arm called {arm.name}")


    # Cuando se suelta una caja sin entregarla a una persona,
    # el brazo queda vacío y la caja queda en la ubicación del drone.
    def drop(self, arm, box, duration = 1, cost = 1):
        if not isinstance(arm, Arm):
            raise ValueError(f"the drone {self.name} expected an Arm object for 'arm' but got {arm!r}")
        if not isinstance(box, Box):
            raise ValueError(f"the drone {self.name} expected a Box object for 'box' but got {box!r}")

        if arm in self.arms:
            if arm.content != box:
                raise ValueError(f"the arm {arm.name} isn't holding {box.name}. It is holding {arm.content}")
            if not box.release(self):
                raise ValueError(f"the box {box.name} is not owned by the drone {self.name}")

            arm.content = None
            box.location = self.location
            print(f"The box {box.name} has been dropped from the arm {arm.name} of the drone {self.name} in the location {self.location}")
            return duration, cost
        else:
            raise ValueError(f"the drone {self.name} does not have an arm called {arm.name}")


    # Cuando se carga una caja en un transportador, se verifica que la caja,
    # el dron y el transportador estén en la misma ubicación, y que el brazo sujeta la caja.
    #
    # box tiene que ser un objeto de tipo Box porque se necesita acceder a su ubicación para verificar
    # que esté en la misma ubicación que el dron y el transportador.
    #
    # conveyor tiene que ser un objeto de tipo Conveyor, debido a que se accede
    # a información como la ubicación, cajas cargadas, y capacidad máxima
    def load_conveyor_with_box(self, arm, box, conveyor, duration = 1, cost = 1):
        if not isinstance(arm, Arm):
            raise ValueError(f"the drone {self.name} expected an Arm object for 'arm' but got {arm!r}")
        if not isinstance(box, Box):
            raise ValueError(f"the drone {self.name} expected a Box object for 'box' but got {box!r}")
        if not isinstance(conveyor, Conveyor):
            raise ValueError(f"the drone {self.name} expected a Conveyor object for 'conveyor' but got {conveyor!r}")

        if self.location != box.location:
            raise ValueError(f"the drone {self.name} is in location {self.location} but the box {box.name} is in location {box.location}")
        elif self.location != conveyor.location:
            raise ValueError(f"the drone {self.name} is not in the same location ({self.location}) the conveyor {conveyor.name} is in ({conveyor.location})")
        
        if arm in self.arms:
            if arm.content != box:
                raise ValueError(f"the arm {arm.name} isn't holding {box.name}. It is holding {arm.content}")
            if conveyor.number_of_boxes_inside() >= conveyor.capacity:
                raise ValueError(f"the conveyor {conveyor.name} has reached its maximum capacity = {conveyor.capacity}")
            # Se verifica que se haya podido cargar correctamente la caja en el transportador y de que 
            # no se está intentando meter una caja que ya está dentro del transportador.
            if (not box.release(self)):
                raise ValueError(f"the box {box.name} is not owned by the drone {self.name}, it is owned by {box.get_current_owner().name}")
            box.try_pickup(conveyor)
            if (not conveyor.add_box(box)):
                raise ValueError(f"the box {box.name} is already loaded in {conveyor.name}")
            else:
                arm.content = None
                print(f"The box {box.name} has been loaded from the arm {arm.name} of the drone {self.name} into the conveyor {conveyor.name} which currently has {conveyor.number_of_boxes_inside()} boxes inside")
                return duration, cost
        else:
            raise ValueError(f"the drone {self.name} does not have an arm called {arm.name}")
        

    # Cuando se descarga una caja de un transportador a un dron,
    # se verifica que la caja, el dron y el transportador
    # están en la misma ubicación, y que el brazo esté vacío.
    #
    # box tiene que ser un objeto de tipo Box porque se necesita acceder a su ubicación para verificar
    # que esté en la misma ubicación que el dron y el transportador.
    #
    # conveyor tiene que ser un objeto de tipo Conveyor, debido a que se accede
    # a información como la ubicación, cajas cargadas, y capacidad máxima
    def unload_box_from_conveyor(self, arm, box, conveyor, duration = 1, cost = 1):
        if not isinstance(arm, Arm):
            raise ValueError(f"the drone {self.name} expected an Arm object for 'arm' but got {arm!r}")
        if not isinstance(box, Box):
            raise ValueError(f"the drone {self.name} expected a Box object for 'box' but got {box!r}")
        if not isinstance(conveyor, Conveyor):
            raise ValueError(f"the drone {self.name} expected a Conveyor object for 'conveyor' but got {conveyor!r}")
        
        if self.location != box.location:
            raise ValueError(f"the drone {self.name} is in location {self.location} but the box {box.name} is in location {box.location}")
        elif self.location != conveyor.location:
            raise ValueError(f"the drone {self.name} is not in the same location ({self.location}) the conveyor {conveyor.name} is in ({conveyor.location})")

        if arm in self.arms:
            if arm.content is not None:
                raise ValueError(f"the arm {arm.name} is already occupied - it has {arm.content}")
            if (not box.release(conveyor)):
                raise ValueError(f"the box {box.name} is not owned by the transporter {conveyor.name}, it is owned by {box.get_current_owner().name}")
            box.try_pickup(self)
            if (not conveyor.remove_box(box)):
                raise ValueError(f"the box {box.name} is not in {conveyor.name}")
            else:
                arm.content = box
                print(f"The box {box.name} is now loaded in the arm {arm.name} of the drone {self.name}, the conveyor {conveyor.name} currently has {conveyor.number_of_boxes_inside()} boxes inside")
                return duration, cost
        else:
            raise ValueError(f"the drone {self.name} does not have an arm called {arm.name}")



    def __str__(self):
        infoArms = ""
        for arm in self.arms:
            infoArms += f"  - {arm}\n"
        return f"Drone(name={self.name}, location={self.location}, arms=\n{infoArms})"
    
    def add_arm(self, arm):
        self.arms.append(arm)

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, new_location):
        self._location = new_location
        for arm in self.arms:
            if arm.content is not None:
                arm.content.location = new_location

    #RESET
    def reset(self):
        self.location = self.__initial_location
        for arm in self.arms:
            arm.reset()