from abc import ABCMeta

class Requirement():
    __metaclass__ = ABCMeta # abstract class
    __slots__ = ['from_elem', 'to_elem', 'type']  # allowed attributes

    def __init__(self, from_elem, to_elem, type):
        self.from_elem = from_elem
        self.to_elem = to_elem
        self.type = type



class AuthorityRequirement(Requirement):
    def __init__(self, from_elem, to_elem):
        super().__init__(from_elem, to_elem, 'authority requirement')

class KnowledgeRequirement(Requirement):
    def __init__(self, from_elem, to_elem):
        super().__init__(from_elem, to_elem, 'knowledge requirement')

class InformationRequirement(Requirement):
    def __init__(self, from_elem, to_elem):
        super().__init__(from_elem, to_elem, 'information requirement')
