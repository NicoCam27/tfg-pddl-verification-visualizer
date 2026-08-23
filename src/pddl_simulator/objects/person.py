# -------------------------------------- LA MAYORIA DE LOS TRABAJOS NO TIENEN "NECESITA" Y SOLO TIENEN "POSEE"
#El objeto de tipo "persona" tiene "ubicacion" (un string), "necesidad" (un contenido como los que tienen las cajas) y "posee" (puede tener una caja o no tener nada)
class Person:
    def __init__(self, name, location = "", needs = "", possesses = "nothing"):
        self.name = name
        self.location = location

        self.__needs_is_a_list = False
        self.__possesses_is_a_list = False
        self.__possesses_at_least_one_object = False

        if (type(needs) == list):
            self.__initial_needs = needs[:]
            self.__needs_is_a_list = True
        else:
            self.__initial_needs = needs

        if (type(possesses) == list):
            self.__initial_possesses = possesses[:]
            self.__possesses_is_a_list = True
        else:
            self.__initial_possesses = possesses

        self.needs = needs
        self.possesses = possesses

        
        if (self.__needs_is_a_list and not self.__possesses_is_a_list):
            raise ValueError(f"the person {self.name} has more than one need and is a list, possesses has to be a list of the same length")
        elif (not self.__needs_is_a_list and self.__possesses_is_a_list):
            raise ValueError(f"the person {self.name} has only one need, possesses can't be a list")
        elif (self.__needs_is_a_list and self.__possesses_is_a_list) and (not (len(needs) == len(possesses))):
            raise ValueError(f"the length of the list of needs ({len(needs)}) isn't the same as the length of list of possesses ({len(possesses)}), they should be equal.")
        

    def convert_needs_to_list(self):
        self.__needs_is_a_list = True
        needs_list = [self.needs]
        self.needs = needs_list[:]

    def convert_possesses_to_list(self):
        self.__possesses_is_a_list = True
        possesses_list = [self.possesses]
        self.possesses = possesses_list[:]

    def add_needs(self, needs):
        # Si se sabe que hay más de una necesidad para una persona, se agrega a la lista de needs
        if self.__needs_is_a_list:

            self.needs.append(needs)
            self.possesses.append("nothing")

        # Si se descubre que una persona tiene más de una necesidad, se crea una lista de necesidades y se agrega la necesidad
        # anteriormente almacenada y la necesidad adicional
        elif self.needs != "":

            self.convert_needs_to_list()
            self.needs.append(needs)

            self.convert_possesses_to_list()
            self.possesses.append("nothing")

        # En caso de que no es una lista de necesidade y no hay ningún need apuntado:
        else:
            self.needs = needs

    def add_possesses(self, possession):

        self.__possesses_at_least_one_object = True

        # Si se sabe que hay más de una necesidad para una persona, se reemplaza el primer "nothing" que se encuentra en possesses
        if self.__possesses_is_a_list:
            for i, element in enumerate(self.possesses):
                if element == "nothing":
                    self.possesses[i] = possession
                    break
            for j, need in enumerate(self.needs):
                if possession.content == need:
                    self.needs[j] = "nothing"
                    break
        else:
            self.possesses = possession
            self.needs = "nothing"

    def __str__(self):
        return f"Person(name={self.name}, location={self.location}, needs={self.needs}, possesses={self.possesses})"
    
    def get_is_possesses_a_list(self):
        return self.__possesses_is_a_list

    def get_possesses_at_least_one_object(self):
        return self.__possesses_at_least_one_object

    #RESET
    def reset(self):
        if self.__needs_is_a_list:
            self.needs = self.__initial_needs[:]
        else:
            self.needs = self.__initial_needs

        if self.__possesses_is_a_list:
            self.possesses = self.__initial_possesses[:]
        else:
            self.possesses = self.__initial_possesses