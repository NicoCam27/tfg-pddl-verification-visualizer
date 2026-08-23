# -------------------------------------- LA MAYORIA DE LOS TRABAJOS NO TIENEN "NECESITA" Y SOLO TIENEN "POSEE"
#El objeto de tipo "persona" tiene "ubicacion" (un string), "necesidad" (un contenido como los que tienen las cajas) y "posee" (puede tener una caja, varias, o no tener nada)

# needs         -->   str   /   lista de str
# possesses     -->   Box   /   lista de Box

class Person:
    def __init__(self, name, location = "", needs = None, possesses = None):
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

        # Si se descubre que una persona tiene más de una necesidad, se crea una lista de necesidades y se agrega la necesidad
        # anteriormente almacenada y la necesidad adicional
        elif self.needs is not None:

            self.convert_needs_to_list()
            self.needs.append(needs)

        # En caso de que no es una lista de necesidade y no hay ningún need apuntado:
        else:
            self.needs = needs


    def add_possesses(self, object):
        # Ahora la persona tiene al menos un objeto
        self.__possesses_at_least_one_object = True

        if self.__possesses_is_a_list:
            self.possesses.append(object)

        # Si la persona ya tiene un objeto, se convierte possesses en una lista y se añade el nuevo objeto
        elif self.possesses is not None:
            self.convert_possesses_to_list()
            self.possesses.append(object)

        # Si la persona no ha tenido ningún objeto anteriormente, se le asigna este objeto directamente
        else:
            self.possesses = object


        # Se satisface la necesidad de ese contenido y se elimina esa neceisdad
        if self.__needs_is_a_list:
            self.needs.remove(object.content)
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

        if (type(self.__initial_possesses) == list):
            self.possesses = self.__initial_possesses[:]
        else:
            self.__possesses_is_a_list = False
            self.possesses = self.__initial_possesses