from abc import ABCMeta

class Requirement():
    __metaclass__ = ABCMeta # abstract class
    __slots__ = ['from_elem', 'to_elem']  # allowed attributes

    def __init__(self, from_elem, to_elem):
        self.from_elem = from_elem
        self.to_elem = to_elem



class AuthorityRequirement(Requirement):
    def __init__(self, from_elem = None, to_elem = None):
        super().__init__(from_elem, to_elem)

class KnowledgeRequirement(Requirement):
    def __init__(self, from_elem = None, to_elem = None):
        super().__init__(from_elem, to_elem)

class InformationRequirement(Requirement):
    def __init__(self, from_elem = None, to_elem = None):
        super().__init__(from_elem, to_elem)
