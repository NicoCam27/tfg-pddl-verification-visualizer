from .box import Box

#El objeto de brazo es un objeto que puede tener una caja, un transportador o None
class Arm:

    def __init__(self, name, content = None):

        self.name = name

        
        if content is not None and not isinstance(content, Box):
                raise TypeError(f"'content' must be a Box object, got {content!r}")
        
        self._content = content

        self.__initial_content = content

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
        self.content = self.__initial_content
