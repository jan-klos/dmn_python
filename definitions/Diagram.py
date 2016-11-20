class Diagram:
    __slots__ = ['id', 'name', 'namespace', 'xmlns', 'xmlnsex', 'description', 'element_list', 'requirement_list', 'definition_list']

    def __init__(self):
        self.id = None
        self.name = None
        self.namespace = None
        self.xmlns = None
        self.xmlnsex = None
        self.description = None
        self.element_list = []
        self.requirement_list = []
        self.definition_list = []

    def add_element_list(self, list):
        self.element_list.extend(list)

    def add_element(self, element):
        self.element_list.append(element)

    def get_element_by_id(self, id):
        for element in self.element_list:
            if element.id == id:
                return element
        raise Exception("Element with given ID not found (ID: " + id + ")")

    def get_element_by_name(self, name):
        for element in self.element_list:
            if element.name == name:
                return element
        raise Exception("Element with given name not found (name: " + name + ")")

    def get_all_elements_of_type(self, type):
        result = []
        for element in self.element_list:
            if element.type == type:
                result.append(element)
        return result

    def remove_element(self, element):
        self.element_list.remove(element)
        requirements_to_remove = []
        for requirement in self.requirement_list:
            if requirement.fromElement == element or requirement.toElement == element:
                requirements_to_remove.append(requirement)
        self.remove_requirement_list(requirements_to_remove)

    def remove_element_by_id(self, id):
        self.remove_element(self.get_element_by_id(id))

    def print_elements(self):
        for element in self.element_list:
            print("Element type: " + element.type +  " - ID: " + str(element.id))




    def add_requirement_list(self, list):
        self.requirement_list.extend(list)

    def add_requirement(self, requirement):
        self.requirement_list.append(requirement)

    def get_requirement_by_id(self, id):
        for requirement in self.requirement_list:
            if requirement.id == id:
                return requirement
        raise Exception("Requirement with given ID not found   (ID: " + str(id) + ")")

    def remove_requirement(self, requirement):
        self.requirement_list.remove(requirement)

    def remove_requirement_by_id(self, id):
        self.requirement_list.remove(self.get_requirement_by_id(id))

    def remove_requirement_list(self, list):
        for requirement in list:
            self.requirement_list.remove(requirement)

    def print_requirements(self):
        for requirement in self.requirement_list:
            print("requirement type: " + requirement.type + " - from " + str(requirement.fromElement.id) + " - to "
                  + str(requirement.toElement.id) + " - ID: " + str(requirement.id))




    def add_definition(self, definition):
        self.definition_list.append(definition)

    def get_definition_by_name(self, name):
        for item in self.definition_list:
            if item.name == name:
                return item
        # raise Exception("Definition with given name not found (name: " + name + ")")