from som.interpreter.objectstorage.storage_location import \
    create_location_for_long, create_location_for_double, \
    create_location_for_object, create_location_for_unwritten_value, \
    NUMBER_OF_POINTER_FIELDS, NUMBER_OF_PRIMITIVE_FIELDS, \
    _AbstractStorageLocation
from som.vmobjects.double  import Double
from som.vmobjects.integer import Integer

class ObjectLayout(object):
    _cached_layouts = {}

    _immutable_fields_ = ["_for_class", "_prim_locations_used",
                          "_ptr_locations_used", "_total_locations",
                          "_storage_locations[*]", "_storage_types[*]", "_meta_object_environment"]

    def __init__(self, number_of_fields, for_class = None,
                 known_types = None, meta_object_environment = None):
        assert number_of_fields >= 0
        from som.vmobjects.object import Object

        self._for_class = for_class
        self._storage_types = known_types or [None] * number_of_fields
        self._total_locations = number_of_fields
        self._storage_locations = [None] * number_of_fields
        self._meta_object_environment = meta_object_environment

        next_free_prim_idx = 0
        next_free_ptr_idx  = 0

        for i in range(0, number_of_fields):
            storage_type = self._storage_types[i]

            if storage_type is Integer:
                storage = create_location_for_long(self, next_free_prim_idx)
                next_free_prim_idx += 1
            elif storage_type is Double:
                storage = create_location_for_double(self, next_free_prim_idx)
                next_free_prim_idx += 1
            elif storage_type is Object:
                storage = create_location_for_object(self, next_free_ptr_idx)
                next_free_ptr_idx += 1
            else:
                assert storage_type is None
                storage = create_location_for_unwritten_value(self)

            assert isinstance(storage, _AbstractStorageLocation)
            self._storage_locations[i] = storage

        self._prim_locations_used = next_free_prim_idx
        self._ptr_locations_used  = next_free_ptr_idx

    @staticmethod
    def get_or_create(number_of_fields, for_class = None,
                 known_types = None, meta_object_environment = None):

        cache_key = (number_of_fields, for_class, ObjectLayout._storage_types_hash(known_types), meta_object_environment)
        if cache_key in ObjectLayout._cached_layouts:
            return ObjectLayout._cached_layouts[cache_key]

        layout = ObjectLayout(number_of_fields, for_class, known_types, meta_object_environment)
        ObjectLayout._cached_layouts[cache_key] = layout

        return layout

    @staticmethod
    def _storage_types_hash(storage_types):

        if storage_types is None:
            return ""

        from som.vmobjects.object import Object
        h = "";
        for storage_type in storage_types:

            if storage_type is Integer:
                h = h + "I"
            elif storage_type is Double:
                h = h + "D"
            elif storage_type is Object:
                h = h + "O"
            else:
                h = h + "N"
        return h

    def clone_with_environment(self, environment):
        from som.vmobjects.object import Object
        assert environment is not None and isinstance(environment, Object)

        return ObjectLayout.get_or_create(self._total_locations, self._for_class, self._storage_types, environment)

    def has_meta_object_environment(self):
        return environment is not None

    def get_meta_object_environment(self):
        return self._meta_object_environment

    def is_for_same_class(self, other):
        return self._for_class is other

    def get_number_of_fields(self):
        return self._total_locations

    def with_generalized_field(self, field_idx):
        from som.vmobjects.object import Object
        if self._storage_types[field_idx] is Object:
            return self
        else:
            assert self._storage_types[field_idx] is not None
            with_generalized_field = self._storage_types[:]
            with_generalized_field[field_idx] = Object
            return ObjectLayout.get_or_create(self._total_locations, self._for_class,
                                with_generalized_field, self._meta_object_environment)

    def with_initialized_field(self, field_idx, spec_class):
        from som.vmobjects.object import Object
        # First we generalize to Integer, Double, or Object
        # don't need more precision
        if spec_class is Integer or spec_class is Double:
            spec_type = spec_class
        else:
            spec_type = Object

        if self._storage_types[field_idx] is spec_type:
            return self
        else:
            assert self._storage_types[field_idx] is None
            with_initialized_field = self._storage_types[:]
            with_initialized_field[field_idx] = spec_type
            return ObjectLayout.get_or_create(self._total_locations, self._for_class,
                                with_initialized_field, self._meta_object_environment)

    def get_storage_location(self, field_idx):
        return self._storage_locations[field_idx]

    def get_number_of_used_extended_ptr_locations(self):
        required_ext_fields = (self._ptr_locations_used
                               - NUMBER_OF_POINTER_FIELDS)
        if required_ext_fields < 0:
            return 0
        else:
            return required_ext_fields

    def get_number_of_used_extended_prim_locations(self):
        required_ext_field = (self._prim_locations_used
                              - NUMBER_OF_PRIMITIVE_FIELDS)
        if required_ext_field < 0:
            return 0
        else:
            return required_ext_field
