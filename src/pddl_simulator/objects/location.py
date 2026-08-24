class Location:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name}"

    # En PDDL el nombre es el identificador único de un objeto, por lo que dos
    # Location con el mismo nombre deben considerarse la misma ubicación aunque
    # sean instancias distintas.
    def __eq__(self, other):
        return isinstance(other, Location) and self.name == other.name

    def __hash__(self):
        return hash(self.name)