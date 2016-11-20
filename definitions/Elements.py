from abc import ABCMeta

class Element():
    __metaclass__ = ABCMeta # abstract class
    __slots__ = ['id', 'name', 'type', 'xml_node']  # allowed attributes

    def __init__(self, type, xml_node):
        self.type = type
        self.id = None
        self.name = None
        self.xml_node = xml_node


    ############################################################


class DecisionElement(Element):
    __slots__ = ['description', 'question', 'allowed_answers', 'variable', 'authority_requirement_list', 'knowledge_requirement_list', 'information_requirement_list', 'invocation', 'decision_table']

    def __init__(self, xml_node):
        super().__init__('decision element', xml_node)
        self.description = None
        self.question = None
        self.allowed_answers = None
        self.variable = None
        self.authority_requirement_list = None
        self.knowledge_requirement_list = None
        self.information_requirement_list = None
        self.invocation = None
        self.decision_table = None



class DecisionElementVariable():
    __slots__ = ['id', 'name', 'type_ref', 'xmlns']

    def __init__(self):
        self.id = None
        self.name = None
        self.type_ref = None
        self.xmlns = None


    ############################################################


class InputDataElement(Element):
    # informationItem - the instance of InformationItem that stores the result of this InputData
    # type_ref - A pointer to a specification of the datatype of the possible values for this InputData, either an ItemDefinition, a base type
    #           in the specified expressionLanguage, or an imported type
    __slots__ = ['informationItem', 'type_ref', 'variable']                  # w xmlu było variable i dopiero w nim type_ref

    def __init__(self, xml_node):
        super().__init__('input data element', xml_node)
        self.informationItem = None
        self.type_ref = None



class InputElementVariable():
    # type_ref - definition it referes to
    # type_ref_value - literal value of parameter 'typeRef'
    __slots__ = ['id', 'name', 'type_ref', 'type_ref_value']

    def set_id(self, id):
        self.id = id
        self.name = None
        self.type_ref = None
        self.type_ref_value = None


    ############################################################


class BusinessKnowledgeModelElement(Element):
    # A BusinessKnowledgeModel element may have zero or more knowledgeRequirement, which are instance of KnowledgeRequirement,
    # and zero or more authorityRequirement, which are instances of AuthorityRequirement.
    __slots__ = ['authority_requirement_list', 'knowledge_requirement_list', 'formal_parameter_list', '_decision_table', '_context']

    def __init__(self, xml_node):
        super().__init__('business knowledge model element', xml_node)
        self.authority_requirement_list = None
        self.knowledge_requirement_list = None
        self.formal_parameter_list = []
        self._decision_table = None
        self._context = None

    @property
    def decision_table(self):
        return self._decision_table

    @decision_table.setter
    def decision_table(self, decision_table):
        self._context = None
        self._decision_table = decision_table

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context):
        self._decision_table = None
        self._context = context



class FormalParameter:
    __slots__ = ['name', 'id', 'type_ref', 'xmlns']

    def __init__(self, name, id, type_ref, xmlns):
        self.name = name
        self.id = id
        self.type_ref = type_ref
        self.xmlns = xmlns


    ############################################################


class KnowledgeSourceElement(Element):
    __slots__ = []

    def __init__(self, xml_node):
        super().__init__('knowledge source element', xml_node)