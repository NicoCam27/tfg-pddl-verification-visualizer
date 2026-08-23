#El objeto de tipo "transportador" tiene "capacidad" (un entero), "cajas dentro" (una lista de cajas)
# y "ubicación" (un string)

class Conveyor:
    def __init__(self, name, capacity = None, boxes_inside = None, location = None):

        self.name = name

        if capacity is None:
            self.capacity = 4 # Capacidad de cajas por defecto en caso de que el usuario no lo menciona
        else:
            self.capacity = capacity

        if boxes_inside is None:
            self.boxes_inside = []
            self.__initial_boxes_inside = []
        else:
            if len(boxes_inside) == len(set(boxes_inside)):
                self.boxes_inside = boxes_inside
                for box in self.boxes_inside:
                    box.try_pickup(self)

                self.__initial_boxes_inside = boxes_inside[:]
            else:
                raise Exception("Las cajas dentro de un transportador deben ser únicas, una caja específica no puede aparecer mas de una vez")
        
        self._location = location

        self.__current_owner = None

        self.__initial_capacity = capacity
        self.__initial_location = location

    

    def get_number_of_boxes_inside(self):
        return len(self.boxes_inside)

    def add_box(self, box):
        if(box not in self.boxes_inside):
            self.boxes_inside.append(box)
            return True
        else:
            return False
        
    def remove_box(self, box):
        if(box in self.boxes_inside):
            self.boxes_inside.remove(box)
            return True
        else:
            return False

    def try_move(self, drone):
        if self.__current_owner is not None:
            return False

        self.__current_owner = drone
        return True

    def release(self, drone):
        if self.__current_owner != drone:
            return False

        self.__current_owner = None
        return True

    def __str__(self):
        return f"Conveyor(name={self.name}, capacity={self.capacity}, boxes_inside={self.boxes_inside}, location={self._location})"
    
    def get_current_owner(self):
        return self.__current_owner

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, new_location):
        self._location = new_location
        for box in self.boxes_inside:
            box.location = new_location
    
    #RESET
    def reset(self):
        self.capacity = self.__initial_capacity
        self.boxes_inside = self.__initial_boxes_inside[:]
        self._location = self.__initial_location
        self.__current_owner = None

        for box in self.boxes_inside:
            box.try_pickup(self)
            box.location = self._location