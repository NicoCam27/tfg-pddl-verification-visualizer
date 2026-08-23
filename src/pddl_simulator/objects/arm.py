#El objeto de brazo es un objeto que puede tener una caja o no tener nada, y se representa como un string (el nombre de la caja o "empty")
class Arm:

    def __init__(self, name, content = "empty"):

        self.name = name
        self.content = content

        self.__initial_content = content

    def __str__(self):
        return f"Arm(name={self.name}, content={self.content})"
    
    #RESET
    def reset(self):
        self.content = self.__initial_content
