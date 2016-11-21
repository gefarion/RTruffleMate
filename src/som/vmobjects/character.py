from som.vmobjects.abstract_object import AbstractObject


class Character(AbstractObject):
    _immutable_fields_ = ["_char"]
    
    def __init__(self, value):
        AbstractObject.__init__(self)
        self.char = value
    
    def get_embedded_character(self):
        return self.char
        
    def __str__(self):
        return "\"" + self.char + "\""

    def get_class(self, universe):
        return universe.characterClass
