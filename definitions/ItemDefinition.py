# An instance of ItemDefinition may contain zero or more itemComponent, which are themselves ItemDefinitions.
# Each itemComponent in turn may be defined by either a typeRef and allowedValues or a nested itemComponent.

class ItemDefinition:
    __slots__ = ['id', 'name', 'item_component_list', 'type_ref_xmlns', 'type_ref', 'allowed_values']  # allowed attributes

    def __init__(self, id = None, name = None, item_component_list = [], type_ref_xmlns = None, type_ref = None, allowed_values = None):
        self.id = id
        self.name = name
        self.item_component_list = item_component_list
        self.type_ref_xmlns = type_ref_xmlns
        self.type_ref = type_ref
        self.allowed_values = allowed_values