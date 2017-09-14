from abc import ABCMeta

class Element():
    __metaclass__ = ABCMeta # abstract class
    __slots__ = ['id', 'name', 'xml_node']  # allowed attributes

    def __init__(self, xml_node = None, id = None, name = None):
        self.id = id
        self.name = name
        self.xml_node = xml_node


    ############################################################


class DecisionElement(Element):
    __slots__ = ['description', 'question', 'allowed_answers', 'variable', 'authority_requirement_list', 'knowledge_requirement_list',
                 'information_requirement_list', 'invocation', 'decision_table']

    def __init__(self, xml_node = None, id = None, name = None, description = None, question = None, allowed_answers = None, variable = None, authority_requirement_list = [],
                 knowledge_requirement_list = [], information_requirement_list = [], invocation = None, decision_table = None):
        super().__init__(xml_node, id, name)
        self.description = description
        self.question = question
        self.allowed_answers = allowed_answers
        self.variable = variable
        self.authority_requirement_list = authority_requirement_list
        self.knowledge_requirement_list = knowledge_requirement_list
        self.information_requirement_list = information_requirement_list
        self.invocation = invocation
        self.decision_table = decision_table



class DecisionElementVariable():
    __slots__ = ['id', 'name', 'type_ref', 'xmlns']

    def __init__(self, id = None, name = None, type_ref = None, xmlns = None):
        self.id = id
        self.name = name
        self.type_ref = type_ref
        self.xmlns = xmlns


    ############################################################


class InputDataElement(Element):
    # information_item - the instance of InformationItem that stores the result of this InputData
    # type_ref - A pointer to a specification of the datatype of the possible values for this InputData, either an ItemDefinition, a base type
    #           in the specified expressionLanguage, or an imported type
    __slots__ = ['information_item', 'type_ref', 'variable']

    def __init__(self, xml_node = None, id = None, name = None, information_item = None, type_ref = None, variable = None):
        super().__init__(xml_node, id, name)
        self.information_item = information_item
        self.type_ref = type_ref
        self.variable = variable



class InputElementVariable():
    # type_ref - definition it referes to
    # type_ref_value - literal value of parameter 'typeRef'
    __slots__ = ['id', 'name', 'type_ref', 'type_ref_value']

    def __init__(self, id = None, name = None, type_ref = None, type_ref_value = None):
        self.id = id
        self.name = name
        self.type_ref = type_ref
        self.type_ref_value = type_ref_value


    ############################################################


class BusinessKnowledgeModelElement(Element):
    # A BusinessKnowledgeModel element may have zero or more knowledgeRequirement, which are instance of KnowledgeRequirement,
    # and zero or more authorityRequirement, which are instances of AuthorityRequirement.
    __slots__ = ['authority_requirement_list', 'knowledge_requirement_list', 'formal_parameter_list', '_decision_table', '_context']

    def __init__(self, xml_node = None, id = None, name = None, authority_requirement_list = [], knowledge_requirement_list = [], formal_parameter_list = [],
                 decision_table = None, context = None):
        super().__init__(xml_node, id, name)
        self.authority_requirement_list = authority_requirement_list
        self.knowledge_requirement_list = knowledge_requirement_list
        self.formal_parameter_list = formal_parameter_list
        self._decision_table = decision_table
        self._context = context

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

    def __init__(self, name = None, id = None, type_ref = None, xmlns = None):
        self.name = name
        self.id = id
        self.type_ref = type_ref
        self.xmlns = xmlns


    ############################################################


class KnowledgeSourceElement(Element):
    __slots__ = []

    def __init__(self, xml_node = None, id = None, name = None):
        super().__init__(xml_node, id, name)