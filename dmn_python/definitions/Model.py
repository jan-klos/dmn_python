from dmn_python.definitions.Requirements import *

class Model:
    __slots__ = ['id', 'name', 'namespace', 'xmlns', 'xmlns_ex', 'description', 'element_list', 'requirement_list', 'definition_list']

    def __init__(self, id = None, name = None, namespace = None, xmlns = None, xmlns_ex = None, description = None, element_list = [], requirement_list = [], definition_list = []):
        self.id = id
        self.name = name
        self.namespace = namespace
        self.xmlns = xmlns
        self.xmlns_ex = xmlns_ex
        self.description = description
        self.element_list = element_list
        self.requirement_list = requirement_list
        self.definition_list = definition_list

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
            if isinstance(element, type):
                result.append(element)
        return result

    def remove_element(self, element):
        self.element_list.remove(element)
        requirements_to_remove = []
        for requirement in self.requirement_list:
            if requirement.from_elem == element or requirement.to_elem == element:
                requirements_to_remove.append(requirement)
        self.remove_requirement_list(requirements_to_remove)

    def remove_element_by_id(self, id):
        self.remove_element(self.get_element_by_id(id))

    def remove_element_by_name(self, name):
        self.remove_element(self.get_element_by_name(name))

    def print_elements(self):
        for element in self.element_list:
            print("Element type: " + element.__class__.__name__ +  " - ID: " + str(element.id))


##################################################


    def add_requirement_list(self, list):
        self.requirement_list.extend(list)

    def add_requirement(self, requirement):
        self.requirement_list.append(requirement)

    def create_requirement(self, requirement = None, from_elem_id = None, from_elem_name = None,
                        to_elem_id = None, to_elem_name = None, from_elem = None, to_elem = None, type = None):
        if type != 'authority' and type != 'information' and type != 'knowledge':
            raise ValueError('Requirement\'s type must be either authority, information, or knowledge')
        if requirement != None:
            pass
        else:
            if (from_elem_id == None and from_elem_name == None and from_elem == None) or (to_elem_id == None and to_elem_name == None and to_elem == None):
                raise ValueError('You must give id or name or reference of both elements connected by requirement')
            if type == 'authority':
                requirement = AuthorityRequirement()
            elif type == 'information':
                requirement = InformationRequirement()
            else:
                requirement = KnowledgeRequirement()
            if from_elem != None:
                requirement.from_elem = from_elem
            elif from_elem_id != None:
                requirement.from_elem = self.get_element_by_id(from_elem_id)
            elif from_elem_name != None:
                requirement.from_elem = self.get_element_by_name(from_elem_name)
            if to_elem != None:
                requirement.to_elem = to_elem
            elif to_elem_id != None:
                requirement.to_elem = self.get_element_by_id(to_elem_id)
            elif to_elem_name != None:
                requirement.to_elem = self.get_element_by_name(to_elem_name)
        self.requirement_list.append(requirement)
        for elem in self.element_list:
            if elem == requirement.to_elem:
                for elem_from in self.element_list:
                    if elem_from == requirement.from_elem:
                        try:
                            if type == 'authority':
                                elem.authority_requirement_list.append(elem_from)
                            elif type == 'information':
                                elem.information_requirement_list.append(elem_from)
                            else:
                                elem.knowledge_requirement_list.append(elem_from)
                        except AttributeError:
                            raise AttributeError('Wrong type of element')

    def get_requirement(self, from_elem_id = None, from_elem_name = None, to_elem_id = None, to_elem_name = None):
        if (from_elem_id == None and from_elem_name == None) or (to_elem_id == None and to_elem_name == None):
            raise ValueError('You must give id or name of both elements connected by requirement')
        list_from = []
        list_to = []
        if from_elem_id != None:
            for req in self.requirement_list:
                if req.from_elem.id == from_elem_id:
                    list_from.append(req)
        elif from_elem_name != None:
            for req in self.requirement_list:
                if req.from_elem.name == from_elem_name:
                    list_from.append(req)
        if to_elem_id != None:
            for req in self.requirement_list:
                if req.to_elem.id == to_elem_id:
                    list_to.append(req)
        elif to_elem_name != None:
            for req in self.requirement_list:
                if req.to_elem.name == to_elem_name:
                    list_to.append(req)
        try:
            return list(set(list_from).intersection(list_to))[0]
        except IndexError:
            raise Exception('Requirement not found')

    def remove_requirement(self, requirement):
        for elem in self.element_list:
            if hasattr(elem, 'authority_requirement_list'):
                for req in elem.authority_requirement_list:
                    if req == requirement.from_elem:
                        elem.authority_requirement_list.remove(req)
            if hasattr(elem, 'information_requirement_list'):
                for req in elem.information_requirement_list:
                    if req == requirement.from_elem:
                        elem.information_requirement_list.remove(req)
            if hasattr(elem, 'knowledge_requirement_list'):
                for req in elem.knowledge_requirement_list:
                    if req == requirement.from_elem:
                        elem.knowledge_requirement_list.remove(req)
        self.requirement_list.remove(requirement)

    def remove_requirement_list(self, list):
        for requirement in list:
            self.remove_requirement(requirement)

    def print_requirements(self):
        for requirement in self.requirement_list:
            print("requirement type: " + requirement.__class__.__name__ + " - from " + str(requirement.from_elem.name) + " to " + str(requirement.to_elem.name))




    def add_definition(self, definition):
        self.definition_list.append(definition)

    def get_definition_by_name(self, name):
        for item in self.definition_list:
            if item.name == name:
                return item
        raise NameError("Definition with given name not found (name: " + name + ")")