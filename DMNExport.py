from lxml.etree import *
import uuid, html, time

class DMNExport:
    class XMLNamespaces:
        xmlns = ''
        xmlnsex = ''
        ns2 = ''

    @staticmethod
    def export_to_xml(diagram, output_file = None):
        DMNExport.generate_header(diagram)
        DMNExport.generate_item_definition(DMNExport.root, diagram)
        DMNExport.generate_input_data(DMNExport.root, diagram)
        DMNExport.generate_knowledge_source(DMNExport.root, diagram)
        DMNExport.generate_business_knowledge_model(DMNExport.root, diagram)
        DMNExport.generate_decision(DMNExport.root, diagram)
        tree = ElementTree(DMNExport.root)
        if output_file == None:
            filename = 'diagram_' + time.strftime('%d-%m-%Y') + '_' + str(uuid.uuid4())[:8] + '.xml'
        else:
            filename = output_file
        tree.write(filename, pretty_print = True, xml_declaration = True, encoding = 'utf-8', standalone = 'yes')


    ##############################################################


    @staticmethod
    def generate_header(diagram):
        DMNExport.XMLNamespaces.xmlns = diagram.xmlns
        DMNExport.XMLNamespaces.xmlnsex = diagram.xmlnsex
        DMNExport.root = Element('definitions', xmlns=DMNExport.XMLNamespaces.xmlns,
                       nsmap={'ex': DMNExport.XMLNamespaces.xmlnsex},
                       namespace=diagram.namespace, name=diagram.name, id=diagram.id)
        if diagram.description != None:
            description = SubElement(DMNExport.root, 'description')
            description.text = diagram.description


    ##############################################################


    @staticmethod
    def generate_item_definition(parent, diagram):
        for item_def in diagram.definition_list:
            item_def_se = SubElement(parent, 'itemDefinition', name = item_def.name, id = item_def.id)
            DMNExport.generate_item_component(item_def_se, item_def)
        
    @staticmethod
    def generate_item_component(parent, item):
        if item.item_component_list != []:
            for item_comp in item.item_component_list:
                item_comp_se = SubElement(parent, 'itemComponent', name = item_comp.name, id = item_comp.id)
                DMNExport.generate_item_component(item_comp_se, item_comp)
        else:
            DMNExport.genereate_type_ref(parent, item)
            DMNExport.generate_allowed_values(parent, item)

    @staticmethod
    def genereate_type_ref(parent, item):
        DMNExport.XMLNamespaces.ns2 = item.type_ref_xmlns
        type_ref_se = SubElement(parent, 'typeRef', nsmap = {'ns2': DMNExport.XMLNamespaces.ns2})
        type_ref_se.text = item.type_ref

    @staticmethod
    def generate_allowed_values(parent, item):
        if item.allowed_values != None:
            allow_val_se = SubElement(parent, 'allowedValues')
            text_se = SubElement(allow_val_se, 'text')
            text_se.text = html.unescape(item.allowed_values)


    ##############################################################


    @staticmethod
    def generate_input_data(parent, diagram):
        for input_data in diagram.get_all_elements_of_type('input data element'):
            input_data_se = DMNExport.generate_subelement_name_id(parent, 'inputData', input_data.name, input_data.id)
            var = DMNExport.generate_subelement_name_id(input_data_se, 'variable', input_data.variable.name, input_data.variable.id)
            var.attrib['typeRef'] = input_data.variable.type_ref_value


    ##############################################################


    @staticmethod
    def generate_knowledge_source(parent, diagram):
        for know_sour in diagram.get_all_elements_of_type('knowledge source element'):
            DMNExport.generate_subelement_name_id(parent, 'knowledgeSource', know_sour.name, know_sour.id)


    ##############################################################


    @staticmethod
    def generate_business_knowledge_model(parent, diagram):
        for buss_know_model in diagram.get_all_elements_of_type('business knowledge model element'):
            buss_know_model_se = DMNExport.generate_subelement_name_id(parent, 'businessKnowledgeModel', buss_know_model.name, buss_know_model.id)
            encapsulated_logic_se = DMNExport.generate_subelement(buss_know_model_se, 'encapsulatedLogic')
            DMNExport.generate_formal_parameters(encapsulated_logic_se, buss_know_model)
            DMNExport.generate_requirements(buss_know_model_se, buss_know_model)
            DMNExport.generate_decision_table(encapsulated_logic_se, buss_know_model)
            DMNExport.generate_context(encapsulated_logic_se, buss_know_model)

    @staticmethod
    def generate_formal_parameters(parent, elem):
        for param in elem.formal_parameter_list:
            if param.xmlns != None:
                DMNExport.XMLNamespaces.ns2 = param.xmlns
                param_se = SubElement(parent, 'formalParameter',  nsmap = {'ns2': DMNExport.XMLNamespaces.ns2})
            else:
                param_se = SubElement(parent, 'formalParameter')
            if param.name != None:
                param_se.attrib['name'] = param.name
            if param.id != None:
                param_se.attrib['id'] = param.id
            if param.type_ref != None:
                param_se.attrib['typeRef'] = param.type_ref


    ##############################################################


    @staticmethod
    def generate_decision(parent, diagram):
        for decision in diagram.get_all_elements_of_type('decision element'):
            decision_se = DMNExport.generate_subelement_name_id(DMNExport.root, 'decision', decision.name, decision.id)
            if decision.description != None:
                DMNExport.generate_subelement_text(decision_se, 'description', decision.description)
            if decision.question != None:
                DMNExport.generate_subelement_text(decision_se, 'question', decision.question)
            if decision.allowed_answers != None:
                DMNExport.generate_subelement_text(decision_se, 'allowedAnswers', decision.allowed_answers)
            if decision.variable != None:
                if decision.variable.xmlns != None:
                    DMNExport.XMLNamespaces.ns2 = decision.variable.xmlns
                    variable_se = SubElement(decision_se, 'variable', nsmap={'ns2': DMNExport.XMLNamespaces.ns2})
                else:
                    variable_se = DMNExport.generate_subelement(decision_se, 'variable')
                if decision.variable.name != None:
                    variable_se.attrib['name'] = decision.variable.name
                if decision.variable.id != None:
                    variable_se.attrib['id'] = decision.variable.id
                if decision.variable.type_ref != None:
                    variable_se.attrib['typeRef'] = decision.variable.type_ref
            DMNExport.generate_requirements(decision_se, decision)
            DMNExport.generate_decision_table(decision_se, decision)
            DMNExport.generate_invocation(decision_se, decision)


    ##############################################################


    @staticmethod
    def generate_requirements(parent, elem):
        DMNExport.generate_authority_requirements(parent, elem)
        DMNExport.generate_information_requirements(parent, elem)
        DMNExport.generate_knowledge_requirements(parent, elem)

    @staticmethod
    def generate_authority_requirements(parent, elem):
        try:
            for requirement in elem.authority_requirement_list:
                DMNExport.generate_requirement(parent, requirement, 'authority', 'Authority')
        except AttributeError:
            pass

    @staticmethod
    def generate_information_requirements(parent, elem):
        try:
            for requirement in elem.information_requirement_list:
                if requirement.type == 'input data element':
                    DMNExport.generate_requirement(parent, requirement, 'information', 'Input')
                # required information is bkm or decision output
                else:
                    DMNExport.generate_requirement(parent, requirement, 'information', 'Decision')
        except AttributeError:
            pass

    @staticmethod
    def generate_knowledge_requirements(parent, elem):
        try:
            for requirement in elem.knowledge_requirement_list:
                DMNExport.generate_requirement(parent, requirement, 'knowledge', 'Knowledge')
        except AttributeError:
            pass

    @staticmethod
    def generate_requirement(parent, requirement, what_requirement, required_what):
        requirement_se = DMNExport.generate_subelement(parent, what_requirement + "Requirement")
        required_se = DMNExport.generate_subelement(requirement_se, "required" + required_what)
        required_se.attrib['href'] = requirement.id


    ##############################################################


    @staticmethod
    def generate_decision_table(parent, elem):
        if elem.decision_table != None:
            decision_table_se = DMNExport.generate_subelement(parent, 'decisionTable')
            decision_table = elem.decision_table
            if decision_table.id != None:
                decision_table_se.attrib['id'] = decision_table.id
            if decision_table.hit_policy != None:
                decision_table_se.attrib['hitPolicy'] = decision_table.hit_policy
            if decision_table.preferred_orientation != None:
                decision_table_se.attrib['preferredOrientation'] = decision_table.preferred_orientation
            if decision_table.aggregation != None:
                decision_table_se.attrib['aggregation'] = decision_table.aggregation
            for input in decision_table.input_list:
                input_se = DMNExport.generate_subelement(decision_table_se, 'input')
                if input.label != None:
                    input_se.attrib['label'] = input.label
                if input.expression != None:
                    DMNExport.generate_subelement_with_text_subelement(input_se, 'inputExpression', input.expression)
                if input.values != None:
                    DMNExport.generate_subelement_with_text_subelement(input_se, 'inputValues', html.unescape(input.values))
            try:
                output_se = DMNExport.generate_subelement_name(decision_table_se, 'output', decision_table.output.name)
                if decision_table.output.values != None:
                    DMNExport.generate_subelement_with_text_subelement(output_se, 'outputValues', html.unescape(decision_table.output.values))
            except KeyError:
                raise KeyError('Decision table must have an output')
            for rule in decision_table.rule_list:
                rule_se = DMNExport.generate_subelement(decision_table_se, 'rule')
                for rule_input in rule.input_list:
                    DMNExport.generate_subelement_with_text_subelement(rule_se, 'inputEntry', html.unescape(rule_input.value))
                try:
                    DMNExport.generate_subelement_with_text_subelement(rule_se, 'outputEntry', html.unescape(rule.output).replace('"', ''))
                except KeyError:
                    raise KeyError('Decision table rule must have an outputEntry')

    @staticmethod
    def generate_invocation(parent, elem):
        if elem.invocation != None:
            invocation_se = DMNExport.generate_subelement(parent, 'invocation')
            if elem.invocation.busin_knowl_name != None:
                DMNExport.generate_subelement_with_text_subelement(invocation_se, 'literalExpresssion', elem.invocation.busin_knowl_name)
            for binding in elem.invocation.binding_list:
                binding_se = DMNExport.generate_subelement(invocation_se, 'binding')
                if binding.name != None:
                    DMNExport.generate_subelement_name(binding_se, 'parameter', binding.name)
                if binding.expression != None:
                    DMNExport.generate_literal_expression(binding_se, binding.expression)

    @staticmethod
    def generate_context(parent, elem):
        if elem.context != None:
            context_se = DMNExport.generate_subelement(parent, 'context')
            for entry in elem.context.context_entry_list:
                entry_se = DMNExport.generate_subelement(context_se, 'contextEntry')
                if entry.name != None:
                    DMNExport.generate_subelement_name(entry_se, 'variable', entry.name)
                if entry.literal_expression != None:
                    DMNExport.generate_literal_expression(entry_se, entry.literal_expression)
                elif entry.invocation != None:
                    DMNExport.generate_invocation(entry_se, entry)
                else:
                    raise Error('EntryContext must consist of either literalExpression or invocation')

    @staticmethod
    def generate_literal_expression(parent, text):
        return DMNExport.generate_subelement_with_text_subelement(parent, 'literalExpresssion', html.unescape(text))


    ##############################################################


    @staticmethod
    def generate_subelement(parent, tag):
        return SubElement(parent, tag)

    @staticmethod
    def generate_subelement_name(parent, tag, name):
        return SubElement(parent, tag, name = name)

    @staticmethod
    def generate_subelement_name_id(parent, tag, name, id):
        return SubElement(parent, tag, name = name, id = id)

    @staticmethod
    def generate_subelement_text(parent, tag, text):
        se = DMNExport.generate_subelement(parent, tag)
        se.text = text
        return se

    @staticmethod
    def generate_subelement_with_text_subelement(parent, tag, text):
        se = DMNExport.generate_subelement(parent, tag)
        text_se = DMNExport.generate_subelement_text(se, 'text', text)