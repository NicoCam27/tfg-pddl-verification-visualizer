from .location import Location
from .box import Box


# -------------------------------------- LA MAYORIA DE LOS TRABAJOS NO TIENEN "NECESITA" Y SOLO TIENEN "POSEE"
#El objeto de tipo "persona" tiene "ubicacion" (un string), "necesidad" (un contenido como los que tienen las cajas) y "posee" (puede tener una caja, varias, o no tener nada)

# needs         -->   str   /   lista de str
# possesses     -->   Box   /   lista de Box

class Person:
    def __init__(self, name, location = None, needs = None, possesses = None):

        if location is not None and not isinstance(location, Location):
            raise TypeError(f"'location' must be a Location object, got {location!r}")

        self.name = name
        self.location = location

        self.__needs_is_a_list = False

        self.__possesses_is_a_list = False
        self.__possesses_at_least_one_object = False


        if (type(needs) == list):
            if all(isinstance(need, str) for need in needs):
                self.needs = needs[:]
                self.__initial_needs = needs[:]
                self.__needs_is_a_list = True
            else:
                raise TypeError(f"'needs' must be a list of strings.")
        else:
            self.needs = needs
            self.__initial_needs = needs


        if (type(possesses) == list):
            if all(isinstance(possess, Box) for possess in possesses):
                self.possesses = possesses[:]
                self.__initial_possesses = possesses[:]
                self.__possesses_is_a_list = True
                # Una persona que ya empieza con alguna caja posee al menos un objeto.
                # reset() aplica esta misma regla para no contradecir a la construcción.
                self.__possesses_at_least_one_object = len(possesses) > 0
            else:
                raise TypeError(f"'possesses' must be a list containing only Box objects.")
        else:
            self.possesses = possesses
            self.__initial_possesses = possesses
            self.__possesses_at_least_one_object = possesses is not None
        


    def convert_needs_to_list(self):
        self.__needs_is_a_list = True
        needs_list = [self.needs]
        self.needs = needs_list[:]

    def convert_possesses_to_list(self):
        self.__possesses_is_a_list = True
        possesses_list = [self.possesses]
        self.possesses = possesses_list[:]


    def add_needs(self, needs):
        if not isinstance(needs, str):
            raise ValueError(f"the person {self.name} expected a string for 'needs' but got {needs!r}")

        # Si se sabe que hay más de una necesidad para una persona, se agrega a la lista de needs
        if self.__needs_is_a_list:
            self.needs.append(needs)

        # Si se descubre que una persona tiene más de una necesidad, se crea una lista de necesidades y se agrega la necesidad
        # anteriormente almacenada y la necesidad adicional
        elif self.needs is not None:

            self.convert_needs_to_list()
            self.needs.append(needs)

        # En caso de que no es una lista de necesidade y no hay ningún need apuntado:
        else:
            self.needs = needs


    def add_possesses(self, box):
        if not isinstance(box, Box):
            raise ValueError(f"the person {self.name} can only possess one or more Box objects,  got {box!r}")

        if isinstance(self.needs, list):
            needs_content = box.content in self.needs
        else:
            needs_content = self.needs is not None and box.content == self.needs
        if not needs_content:
            raise ValueError(f"the person {self.name} does not need the content of the box {box.name} - it needs {self.needs} but the box has {box.content}")

        if self.__possesses_is_a_list:
            self.possesses.append(box)

        # Si la persona ya tiene un objeto, se convierte possesses en una lista y se añade el nuevo objeto
        elif self.possesses is not None:
            self.convert_possesses_to_list()
            self.possesses.append(box)

        # Si la persona no ha tenido ningún objeto anteriormente, se le asigna este objeto directamente
        else:
            self.possesses = box

        # Ahora la persona tiene al menos un objeto
        self.__possesses_at_least_one_object = True

        # Se satisface la necesidad de ese contenido y se elimina esa neceisdad
        if self.__needs_is_a_list:
            self.needs.remove(box.content)
        else:
            self.needs = None


    def __str__(self):
        return f"Person(name={self.name}, location={self.location}, needs={self.needs}, possesses={self.possesses})"
    
    def get_is_possesses_a_list(self):
        return self.__possesses_is_a_list

    def possesses_at_least_one_object(self):
        return self.__possesses_at_least_one_object

    #RESET
    def reset(self):
        if (type(self.__initial_needs) == list):
            self.needs = self.__initial_needs[:]
        else:
            self.__needs_is_a_list = False
            self.needs = self.__initial_needs

        # La asignación es incondicional (no un "if ... = True") para que el flag también
        # vuelva a False cuando el estado inicial no tenía ninguna caja.
        if (type(self.__initial_possesses) == list):
            self.possesses = self.__initial_possesses[:]
            self.__possesses_at_least_one_object = len(self.__initial_possesses) > 0
        else:
            self.__possesses_is_a_list = False
            self.possesses = self.__initial_possesses
            self.__possesses_at_least_one_object = self.__initial_possesses is not None