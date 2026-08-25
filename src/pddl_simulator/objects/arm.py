from .box import Box

# El objeto de brazo es un objeto que puede tener una caja o no tener nada.
# Siempre empieza sin cajas.
class Arm:

    def __init__(self, name):

        self.name = name

        self._content = None

    def __str__(self):
        return f"Arm(name={self.name}, content={self.content})"

    
    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, new_content):
        if new_content is not None and not isinstance(new_content, Box):
                raise TypeError(f"'new_content' must be a Box object, got {new_content!r}")
        self._content = new_content

    #RESET
    def reset(self):
        self.content = None
