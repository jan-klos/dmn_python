# An instance of ItemDefinition may contain zero or more itemComponent, which are themselves ItemDefinitions.
# Each itemComponent in turn may be defined by either a typeRef and allowedValues or a nested itemComponent.

class ItemDefinition:
    __slots__ = ['id', 'name', 'item_component_list', 'type_ref_xmlns', 'type_ref', 'allowed_values']  # allowed attributes

    def __init__(self):
        self.id = None
        self.name = None
        self.item_component_list = []
        self.type_ref_xmlns = None
        self.type_ref = None
        self.allowed_values = None