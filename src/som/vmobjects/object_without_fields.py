from som.vmobjects.abstract_object import AbstractObject


class ObjectWithoutFields(AbstractObject):

    _immutable_fields_ = ["_class"]

    def __init__(self, obj_class):
        self._class = obj_class

        # field to store meta object
        self._meta_object_environment = None

    def get_meta_object_environment(self):
        return self._meta_object_environment

    def set_meta_object_environment(self, environment):
        self._meta_object_environment = environment

    def get_class(self, universe):
        return self._class

    def set_class(self, value):
        self._class = value

    def get_number_of_fields(self):
        return 0
