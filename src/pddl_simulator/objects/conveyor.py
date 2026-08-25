from .box import Box
from .location import Location

#El objeto de tipo "transportador" tiene "capacidad" (un entero), "cajas dentro" (una lista de cajas)
# y "ubicación" (un string)

class Conveyor:
    def __init__(self, name, capacity = None, boxes_inside = None, location = None):

        self.name = name

        if capacity is None:
            self.capacity = 4 # Capacidad de cajas por defecto en caso de que el usuario no lo menciona
        elif isinstance(capacity, int) and capacity >= 1:
            self.capacity = capacity
        else:
            raise ValueError(f"the capacity of a conveyor must be a positive integer larger than 0")

        if location is not None and not isinstance(location, Location):
            raise TypeError(f"'location' must be a Location object, got {location!r}")

        self._location = location

        if boxes_inside is None:
            self.boxes_inside = []
            self.__initial_boxes_inside = []
        else:
            if len(boxes_inside) == len(set(boxes_inside)):
                if len(boxes_inside) > self.capacity:
                    raise ValueError(f"the conveyor {self.name} is initialized with {len(boxes_inside)} boxes inside, which exceeds its maximum capacity of {self.capacity}")
                else:
                    if all(isinstance(box, Box) for box in boxes_inside):
                        self.boxes_inside = boxes_inside[:]
                        for box in self.boxes_inside:
                            box.force_owner(self)
                            box.location = self._location

                        self.__initial_boxes_inside = boxes_inside[:]
                    else:
                        raise TypeError(f"'boxes_inside' must be a list containing only Box objects.")
            else:
                raise Exception("The boxes inside a conveyor must be unique, a specific box cannot appear more than once")


        self.__current_owner = None

        self.__initial_capacity = self.capacity
        self.__initial_location = self.location

    

    def number_of_boxes_inside(self):
        return len(self.boxes_inside)

    def add_box(self, box):
        if not isinstance(box, Box):
            raise ValueError(f"the conveyor {self.name} expected a Box object for 'box' but got {box!r}")
        if box not in self.boxes_inside and (self.number_of_boxes_inside() + 1) <= self.capacity:
            self.boxes_inside.append(box)
            return True
        else:
            return False
        
    def remove_box(self, box):
        if (box in self.boxes_inside):
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
        if new_location is not None and not isinstance(new_location, Location):
            raise TypeError(f"'location' must be a Location object, got {new_location!r}")

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
            box.force_owner(self)
            box.location = self._location