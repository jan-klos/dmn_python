from tabulate import tabulate
import html, time, uuid, os
import graphviz as gv
from definitions.Elements import InputDataElement, BusinessKnowledgeModelElement, DecisionElement, KnowledgeSourceElement
from definitions.Requirements import InformationRequirement, KnowledgeRequirement, AuthorityRequirement

class DMNVisualisation:
    path_to_img = os.path.dirname(os.path.abspath(__file__)) + '/img/'

    @staticmethod
    # rankdir - orientation of the graph, can be either BT, TB, LR, or RL
    def display_diagram(model, output_file = None, rankdir = 'BT'):
        graph = gv.Digraph()
        graph.graph_attr['rankdir'] = rankdir

        for i in range(0, len(model.element_list)):
            name = model.element_list[i].name
            if name == None:
                raise TypeError('An element must have a name')
            if isinstance(model.element_list[i], DecisionElement):
                graph.node(name, label = DMNVisualisation.break_name(name), shape = 'none', image = DMNVisualisation.path_to_img + 'decision.png')
            elif isinstance(model.element_list[i], InputDataElement):
                graph.node(name, label = DMNVisualisation.break_name(name), shape = 'none', image = DMNVisualisation.path_to_img + 'inputData.png')
            elif isinstance(model.element_list[i], BusinessKnowledgeModelElement):
                graph.node(name, label = DMNVisualisation.break_name(name), shape = 'none', image = DMNVisualisation.path_to_img + 'bussKnowledgeModel.png')
            elif isinstance(model.element_list[i], KnowledgeSourceElement):
                graph.node(name, label = DMNVisualisation.break_name(name, 7), shape = 'none', image = DMNVisualisation.path_to_img + 'knowledgeSource.png')

        for requirement in model.requirement_list:
            if isinstance(requirement, AuthorityRequirement):
                graph.edge(requirement.from_elem.name, requirement.to_elem.name, style = 'dashed', arrowhead = 'dot')
            elif isinstance(requirement, KnowledgeRequirement):
                graph.edge(requirement.from_elem.name, requirement.to_elem.name, style = 'dashed', arrowhead = 'open')
            elif isinstance(requirement, InformationRequirement):
                graph.edge(requirement.from_elem.name, requirement.to_elem.name)

        if output_file == None:
            directory = os.getenv("HOME") + '/dmn_python_outputs/'
            if not os.path.exists(directory):
                os.makedirs(directory)
            filename = directory + 'diagram_' + time.strftime('%d-%m-%Y') + '_' + str(uuid.uuid4())[:4] + '.gv'
        else:
            filename = output_file
        graph.render(filename, view = True)

    @staticmethod
    def break_name(name, length = 9):
        n = 0
        result = name
        for i in range(0, len(name)):
            if name[i] != ' ':
                n += 1
            elif n > length:
                result = result[:i] + '\n' + result[i + 1:]
                n = 0
            else:
                n += 1
        return result


    ##############################################################################


    @staticmethod
    def print_decision_table(elem, output_file = None):
        if output_file == None:
            directory = os.getenv("HOME") + '/dmn_python_outputs/'
            if not os.path.exists(directory):
                os.makedirs(directory)
            filename = directory + 'decision_table_' + elem.id + '_' + time.strftime('%d-%m-%Y') + '_' + str(uuid.uuid4())[:4] + '.txt'
        else:
            filename = output_file
        output_file = open(filename, 'w')
        if elem.decision_table.preferred_orientation == 'RULE-AS-COLUMN':
            DMNVisualisation.print_decision_table_column(elem, output_file)
        # CROSSTAB not supported for now
        elif elem.decision_table.preferred_orientation == 'CROSSTAB':
            print('\n\n\n\nCROSSTAB orientation not supported for now, using RULE-AS-ROW')
            DMNVisualisation.print_decision_table_row(elem, output_file)
        # RULE-AS-ROW
        else:
            DMNVisualisation.print_decision_table_row(elem, output_file)
        output_file.close()

    @staticmethod
    def print_decision_table_column(elem, output_file):
        bottom_row = [elem.decision_table.hit_policy[0]]
        output_row = [elem.decision_table.output.name]
        table, table_row_empty = [], []
        for input in elem.decision_table.input_list:
            table_row = [input.label if input.label != None else input.expression]
            for rule in elem.decision_table.rule_list:
                table_row.append(html.unescape(rule.input_list[elem.decision_table.input_list.index(input)]))
            table.append(table_row)
        for rule in elem.decision_table.rule_list:
            bottom_row.append(elem.decision_table.rule_list.index(rule) + 1)
            table_row_empty.append('')
            output_row.append(html.unescape(rule.output))
        table.append(table_row_empty)
        table.append(output_row)
        table.append(bottom_row)

        print('\n\n ' + elem.name)
        print(tabulate(table, tablefmt='fancy_grid'))
        print(' ' + elem.name + '\n', end = '', file = output_file)
        print(tabulate(table, tablefmt='fancy_grid'), end = '', file = output_file)


    @staticmethod
    def print_decision_table_row(elem, output_file):
        headers = [elem.decision_table.hit_policy[0]]
        for input in elem.decision_table.input_list:
            inp = input.label if input.label != None else input.expression
            headers.append(inp)
        headers.append('')
        headers.append(elem.decision_table.output.name)

        table = []
        for rule in elem.decision_table.rule_list:
            table_row = [elem.decision_table.rule_list.index(rule) + 1]
            for input in rule.input_list:
                table_row.append(html.unescape(input))
            table_row.append('')
            table_row.append(html.unescape(rule.output))
            table.append(table_row)

        print('\n\n ' + elem.name)
        print(tabulate(table, headers, tablefmt='fancy_grid'))
        print(' ' + elem.name + '\n', end = '', file = output_file)
        print(tabulate(table, headers, tablefmt='fancy_grid'), end = '', file = output_file)