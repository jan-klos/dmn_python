class DecisionTable():
    __slots__ = ['id', 'aggregation', 'input_list', 'output', 'rule_list', '_hit_policy', '_preferred_orientation']

    def __init__(self, id = None, hit_policy = None, preferred_orientation = None, aggregation = None, input_list = [], output = None, rule_list = []):
        self.id = id
        self._hit_policy = hit_policy
        self._preferred_orientation = preferred_orientation.upper()
        self.aggregation = aggregation
        self.input_list = input_list
        self.output = output
        self.rule_list = rule_list

    @property
    def hit_policy(self):
        return self._hit_policy

    @hit_policy.setter
    def hit_policy(self, hit_policy):
        if hit_policy == None:
            self._hit_policy = None
        elif hit_policy.upper() in ('UNIQUE', 'FIRST', 'PRIORITY', 'ANY', 'COLLECT', 'RULE ORDER', 'OUTPUT ORDER'):
            self._hit_policy = hit_policy.upper()
        else:
            raise Exception('The value of a hit_policy must be one of the following: UNIQUE, FIRST, PRIORITY, ANY, COLLECT, RULE ORDER, OUTPUT ORDER')

    @property
    def preferred_orientation(self):
        return self._preferred_orientation

    @preferred_orientation.setter
    def preferred_orientation(self, preferred_orientation):
        if preferred_orientation == None:
            self._preferred_orientation = None
        elif preferred_orientation.upper() in ('RULE-AS-ROW', 'RULE-AS-COLUMN', 'CROSSTABLE'):
            self._preferred_orientation = preferred_orientation.upper()
        else:
            raise ValueError('The value of preferred_orientation must be one of the following: RULE-AS-ROW, RULE-AS-COLUMN, CROSSTABLE')



class DecisionTableInput():
    __slots__ = ['label', 'expression', 'allowed_values']

    def __init__(self, label = None, expression = None, allowed_values = None):
        self.label = label
        self.expression = expression
        self.allowed_values = allowed_values



class DecisionTableOutput():
    __slots__ = ['name', 'allowed_values']

    def __init__(self, name = None, allowed_values = None):
        self.name = name
        self.allowed_values = allowed_values



class Rule():
    __slots__ = ['input_list', 'output']

    def __init__(self, input_list = [], output = None):
        self.input_list = input_list
        self.output = output


############################################################################


class Context:
    __slots__ = ['context_entry_list']

    def __init__(self, context_entry_list = None):
        self.context_entry_list = context_entry_list



class ContextEntry:
    # contextEntry - either literal expression or invocation
    __slots__ = ['name', '_literal_expression', '_invocation']

    def __init__(self):
        self.name = None
        self._literal_expression = None
        self._invocation = None

    @property
    def literal_expression(self):
        return self._literal_expression

    @literal_expression.setter
    def literal_expression(self, literal_expression):
        self._invocation = None
        self._literal_expression = literal_expression

    @property
    def invocation(self):
        return self._invocation

    @invocation.setter
    def invocation(self, invocation):
        self._literal_expression = None
        self._invocation = invocation


###############################################################################


class Invocation:
    # invocation is represented by a box containing the name of the business knowledge model to be invoked and a list of bindings
    __slots__ = ['busin_knowl_name', 'binding_list']

    def __init__(self, busin_knowl_name):
        self.busin_knowl_name = busin_knowl_name
        self.binding_list = []



class Binding:
    # binding is represented the name of a parameter and the binding expression
    __slots__ = ['name', 'expression']

    def __init__(self, name, expression):
        self.name = name
        self.expression = expression





