#El objeto de tipo "caja" tiene "ubicacion" (un string) y "contenido" (puede ser un string o vacío)
class Box:
    AVAILABLE = "available"
    CARRIED = "carried"
    DELIVERED = "delivered"

    def __init__(self, name, location = None, content = ""):
        self.name = name
        self.location = location
        self.content = content
        self.__state = self.AVAILABLE
        self.__current_owner = None

        self.__initial_location = location

    def try_pickup(self, obj):
        if self.__state != self.AVAILABLE and self.__state != self.DELIVERED:
            return False

        self.__state = self.CARRIED
        self.__current_owner = obj
        return True

    def release(self, obj):
        if self.__current_owner != obj:
            return False

        self.__state = self.AVAILABLE
        self.__current_owner = None
        return True
    
    def delivered_to(self, person):
        if self.__state != self.AVAILABLE and self.__state != self.DELIVERED:
            return False

        self.__state = self.DELIVERED
        self.__current_owner = person
        return True

    def __str__(self):
        return f"Box(name={self.name}, location={self.location}, content={self.content})"
    
    def get_state(self):
        return self.__state
    
    def get_current_owner(self):
        return self.__current_owner

    #RESET
    def reset(self):
        self.location = self.__initial_location
        self.__state = self.AVAILABLE
        self.__current_owner = None