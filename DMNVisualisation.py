from tabulate import tabulate
import html, time, uuid, os
import graphviz as gv

class DMNVisualisation:
    path_to_img = os.path.dirname(os.path.abspath(__file__)) + '/img/'

    @staticmethod
    def display_diagram(diagram, output_file = None):
        graph = gv.Digraph()
        for i in range(0, len(diagram.element_list)):
            name = diagram.element_list[i].name
            if name == None:
                raise TypeError('An element must have a name')
            if diagram.element_list[i].type == 'decision element':
                graph.node(name, label = DMNVisualisation.break_name(name), shape = 'none', image = DMNVisualisation.path_to_img + 'decision.png')
            elif diagram.element_list[i].type == 'input data element':
                graph.node(name, label = DMNVisualisation.break_name(name), shape = 'none', image = DMNVisualisation.path_to_img + 'inputData.png')
            elif diagram.element_list[i].type == 'business knowledge model element':
                graph.node(name, label = DMNVisualisation.break_name(name), shape = 'none', image = DMNVisualisation.path_to_img + 'bussKnowledgeModel.png')
            #knowledge source
            else:
                graph.node(name, label = DMNVisualisation.break_name(name, 7), shape = 'none', image = DMNVisualisation.path_to_img + 'knowledgeSource.png')


        for requirement in diagram.requirement_list:
            if requirement.type == 'authority requirement':
                graph.edge(requirement.from_elem.name, requirement.to_elem.name, style = 'dashed', arrowhead = 'dot')
            elif requirement.type == 'knowledge requirement':
                graph.edge(requirement.from_elem.name, requirement.to_elem.name, style = 'dashed', arrowhead = 'open')
            # information requirement
            else:
                graph.edge(requirement.from_elem.name, requirement.to_elem.name)
        if output_file == None:
            filename = 'diagram_' + time.strftime('%d-%m-%Y') + '_' + str(uuid.uuid4())[:8] + '.gv'
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
    def print_decision_table(elem):
        if elem.decision_table.preferred_orientation == 'RULE-AS-COLUMN':
            DMNVisualisation.print_decision_table_column(elem)
        # CROSSTAB not supported for now
        elif elem.decision_table.preferred_orientation == 'CROSSTAB':
            print('\n\n\n\nCROSSTAB orientation not supported for now, using RULE-AS-ROW')
            DMNVisualisation.print_decision_table_row(elem)
        # RULE-AS-ROW
        else:
            DMNVisualisation.print_decision_table_row(elem)

    @staticmethod
    def print_decision_table_column(elem):
        bottom_row = [elem.decision_table.hit_policy[0]]
        output_row = [elem.decision_table.output]
        table, table_row_empty = [], []
        for input in elem.decision_table.input_list:
            table_row = [input.label if input.label != None else input.expression]
            for rule in elem.decision_table.rule_list:
                table_row.append(html.unescape(rule.input_list[elem.decision_table.input_list.index(input)].value))
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

    @staticmethod
    def print_decision_table_row(elem):
        headers = [elem.decision_table.hit_policy[0]]
        for input in elem.decision_table.input_list:
            inp = input.label if input.label != None else input.expression
            headers.append(inp)
        headers.append('')
        headers.append(elem.decision_table.output)

        table = []
        for rule in elem.decision_table.rule_list:
            table_row = [elem.decision_table.rule_list.index(rule) + 1]
            for input in rule.input_list:
                table_row.append(html.unescape(input.value))
            table_row.append('')
            table_row.append(html.unescape(rule.output))
            table.append(table_row)

        print('\n\n ' + elem.name)
        print(tabulate(table, headers, tablefmt='fancy_grid'))


#     table_row = [elem.decision_table.output]
#     table_row.append(elem.decision_table.output)
#     for rule in elem.decision_table.rule_list:
#         table_row.append(elem.decision_table.input_list[0])
#     table = [table_row]
#     table_row = [elem.decision_table.output]
#     table_row.append(elem.decision_table.output)
#     for rule in elem.decision_table.rule_list:
#         table_row.append(html.unescape(rule.input_list[0].value))
#     table.append(table_row)
#     for rule in elem.decision_table.rule_list:
#         table_row = [elem.decision_table.input_list[1]]
#         table_row.append(html.unescape(rule.input_list[1].value))
#         table_row.append()