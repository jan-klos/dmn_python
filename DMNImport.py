from xml.dom import minidom
from definitions.Elements import *
from definitions.Model import Model
from definitions.ItemDefinition import ItemDefinition
from definitions.Requirements import *
from definitions.Logic import *

class DMNImport:

    @staticmethod
    def load_model_from_xml(file_path):
        DMNImport.xml_doc = minidom.parse(file_path)
        DMNImport.model = Model()
        DMNImport.import_header()
        DMNImport.import_item_definition()
        DMNImport.import_input_data_elem()
        DMNImport.import_knowledge_source_elem()
        DMNImport.import_business_knowledge_model_elem()
        DMNImport.import_decision_elem()
        DMNImport.import_requirement()
        return DMNImport.model

    ##############################################################
    
    
    @staticmethod
    def import_header():
        header = DMNImport.get_first_element_by_tag(DMNImport.xml_doc, 'definitions')
        DMNImport.get_name_id(header, DMNImport.model)
        DMNImport.model.namespace = DMNImport.get_attribute_value(header, 'namespace')
        DMNImport.model.xmlns = DMNImport.get_attribute_value(header, 'xmlns')
        DMNImport.model.xmlns_ex = DMNImport.get_attribute_value(header, 'xmlns:ex')
        DMNImport.model.description = DMNImport.get_value_by_tag(DMNImport.xml_doc, 'description')


    ##############################################################


    @staticmethod
    def import_item_definition():
        for item in DMNImport.get_list_by_tag(DMNImport.xml_doc, 'itemDefinition'):
            item_def = DMNImport.get_name_id(item, ItemDefinition())
            if DMNImport.get_list_by_tag(item, 'itemComponent'):
                item_def.item_component_list = DMNImport.import_item_component(item)
            else:
                item_def = DMNImport.import_item_component_type_ref_allowed_values(item, item_def)
            DMNImport.model.add_definition(item_def)

    @staticmethod
    def import_item_component(xml_node):
        item_component_list = []
        for item in DMNImport.get_list_by_tag(xml_node, 'itemComponent'):
            if item.parentNode != xml_node:
                continue
            item_component = DMNImport.get_name_id(item, ItemDefinition())
            if not DMNImport.at_least_one_element_by_tag(item, 'itemComponent'):
                DMNImport.import_item_component_type_ref_allowed_values(item, item_component)
            else:
                item_component.item_component_list = DMNImport.import_item_component(item)
            item_component_list.append(item_component)
        return item_component_list

    @staticmethod
    def import_item_component_type_ref_allowed_values(xml_node, item_component):
        type_ref_item = DMNImport.get_first_element_by_tag(xml_node, 'typeRef')
        type_ref_xmlns = DMNImport.get_attribute_value(type_ref_item, 'xmlns:ns2')
        type_ref = type_ref_item.childNodes[0].toxml()
        try:
            allowed_values = DMNImport.get_value_by_two_tags(xml_node, 'allowedValues', 'text')
        except IndexError:
            allowed_values = None
        item_component.type_ref_xmlns = type_ref_xmlns
        item_component.type_ref = type_ref
        item_component.allowed_values = allowed_values
        return item_component


    ############################################################


    @staticmethod
    def import_input_data_elem():
        for item in DMNImport.get_list_by_tag(DMNImport.xml_doc, 'inputData'):
            input_data_elem = DMNImport.get_name_id(item, InputDataElement(item))
            input_data_elem.variable = DMNImport.import_input_element_variable(item)
            DMNImport.model.add_element(input_data_elem)

    @staticmethod
    def import_input_element_variable(xml_node):
        variable_item = DMNImport.get_first_element_by_tag(xml_node, 'variable')
        variable = DMNImport.get_name_id(variable_item, InputElementVariable())
        variable.type_ref_value = DMNImport.get_attribute_value(variable_item, 'typeRef')
        variable.type_ref = DMNImport.model.get_definition_by_name(variable.name)
        return variable



    ############################################################


    @staticmethod
    def import_knowledge_source_elem():
        for item in DMNImport.get_list_by_tag(DMNImport.xml_doc, 'knowledgeSource'):
            knowledge_source_elem = DMNImport.get_name_id(item, KnowledgeSourceElement(item))
            DMNImport.model.add_element(knowledge_source_elem)


    ############################################################


    @staticmethod
    def import_business_knowledge_model_elem():
        for item in DMNImport.get_list_by_tag(DMNImport.xml_doc, 'businessKnowledgeModel'):
            business_knowledge_elem = DMNImport.get_name_id(item, BusinessKnowledgeModelElement(item))
            business_knowledge_elem = DMNImport.import_logic(item, business_knowledge_elem)
            DMNImport.model.add_element(business_knowledge_elem)

    @staticmethod
    def import_logic(xml_node, business_knowledge_elem):
        business_knowledge_elem.formal_parameter_list = DMNImport.import_formal_parameter_list(xml_node, business_knowledge_elem)
        try:
            business_knowledge_elem.decision_table = DMNImport.import_decision_table(xml_node)
            return business_knowledge_elem
        except IndexError:
            business_knowledge_elem.context = DMNImport.import_context(DMNImport.get_first_element_by_tag(xml_node, 'context'))
            return business_knowledge_elem

    @staticmethod
    def import_formal_parameter_list(xml_node, business_knowledge_elem):
        formal_parameter_list = []
        for item in DMNImport.get_list_by_tag(xml_node, 'formalParameter'):
            formal_parameter_list.append(FormalParameter(DMNImport.get_attribute_value(item, 'name'), DMNImport.get_attribute_value(item, 'id'),
                    DMNImport.get_attribute_value(item, 'typeRef'), DMNImport.get_attribute_value(item, 'xmlns:ns2')))

        return formal_parameter_list

    @staticmethod
    def import_context(xml_node):
        context = Context()
        context.context_entry_list = DMNImport.import_context_entry_list(xml_node)
        return context

    @staticmethod
    def import_context_entry_list(xml_node):
        context_entry_list = []
        for item in DMNImport.get_list_by_tag(xml_node, 'contextEntry'):
            context_entry = ContextEntry()
            try:
                context_entry.name = DMNImport.get_attribute_value(DMNImport.get_first_element_by_tag(item, 'variable'), 'name')
            except IndexError:
                pass
            if len(DMNImport.get_list_by_tag(item, 'invocation')):
                context_entry.invocation = DMNImport.import_invocation(item)
            else:
                context_entry.literal_expression = DMNImport.get_literal_expression(item)
            context_entry_list.append(context_entry)
        return context_entry_list


    ############################################################


    @staticmethod
    def import_decision_elem():
        for item in DMNImport.get_list_by_tag(DMNImport.xml_doc, 'decision'):
            decision_elem = DMNImport.get_name_id(item, DecisionElement(item))
            decision_elem.variable = DMNImport.import_decision_element_variable(item)
            decision_elem = DMNImport.import_descr_quest_answ(item, decision_elem)
            try:
                decision_elem.invocation = DMNImport.import_invocation(item)
            except IndexError:
                pass
            try:
                decision_elem.decision_table = DMNImport.import_decision_table(item)
            except IndexError:
                pass
            DMNImport.model.add_element(decision_elem)

    @staticmethod
    def import_decision_element_variable(xml_node):
        try:
            variable_item = DMNImport.get_first_element_by_tag(xml_node, 'variable')
            variable = DMNImport.get_name_id(variable_item, DecisionElementVariable())
            variable.type_ref = DMNImport.get_attribute_value(variable_item, 'typeRef')
            variable.xmlns = DMNImport.get_attribute_value(variable_item, 'xmlns:ns2')
            return variable
        except IndexError:
            pass

    @staticmethod
    def import_descr_quest_answ(xml_node, decision_elem):
        try:
            decision_elem.description = DMNImport.get_value_by_tag(xml_node, 'description')
            decision_elem.question = DMNImport.get_value_by_tag(xml_node, 'question')
            decision_elem.allowed_answers = DMNImport.get_value_by_tag(xml_node, 'allowedAnswers')
        except IndexError:
            pass
        return decision_elem


    #############################################################


    @staticmethod
    def import_invocation(xml_node):
        xml_node = DMNImport.get_first_element_by_tag(xml_node, 'invocation')
        invocation = Invocation(DMNImport.get_literal_expression(xml_node))
        for item in DMNImport.get_list_by_tag(xml_node, 'binding'):
            invocation.binding_list.append(Binding(DMNImport.get_attribute_value(DMNImport.get_first_element_by_tag(item, 'parameter'), 'name'), DMNImport.get_literal_expression(item)))
        return invocation

    @staticmethod
    def import_decision_table(xml_node):
        xml_node = DMNImport.get_first_element_by_tag(xml_node, 'decisionTable')
        decision_table = DecisionTable(DMNImport.get_attribute_value(xml_node, 'id'), DMNImport.get_attribute_value(xml_node, 'hitPolicy'),
                DMNImport.get_attribute_value(xml_node, 'preferredOrientation'), DMNImport.get_attribute_value(xml_node, 'aggregation'))
        decision_table.input_list = DMNImport.import_decision_table_inputs(xml_node)
        output_item = DMNImport.get_first_element_by_tag(xml_node, 'output')
        decision_table.output = DecisionTableOutput(DMNImport.get_attribute_value(output_item, 'name'), DMNImport.get_value_by_tag(output_item, 'text'))
        decision_table.rule_list = DMNImport.import_rules(xml_node, decision_table.input_list)
        return decision_table

    @staticmethod
    def import_decision_table_inputs(xml_node):
        input_list = []
        for item in DMNImport.get_list_by_tag(xml_node, 'input'):
            input = DecisionTableInput(DMNImport.get_attribute_value(item, 'label'), DMNImport.get_value_by_tag(item, 'text'), DMNImport.get_second_value_by_tag(item, 'text'))
            input_list.append(input)
        return input_list

    @staticmethod
    def import_rules(xml_node, decision_table_input_list):
        rule_list = []
        for item in DMNImport.get_list_by_tag(xml_node, 'rule'):
            rule = Rule()
            rule_input_list = []
            for item1 in DMNImport.get_list_by_tag(item, 'inputEntry'):
                rule_input = DMNImport.get_value_by_tag(item1, 'text')
                rule_input_list.append(rule_input)
            rule.output = DMNImport.get_value_by_two_tags(item, 'outputEntry', 'text')
            rule.input_list = rule_input_list
            rule_list.append(rule)
        return rule_list



    #############################################################

    @staticmethod
    def import_requirement():
        for elem in DMNImport.model.element_list:
            DMNImport.import_requirement_of_elem(elem)


    @staticmethod
    def import_requirement_of_elem(elem):
        try:
            elem.authority_requirement_list = DMNImport.import_requirement_list(elem.xml_node, 'authority')
        except:
            pass
        try:
            elem.knowledge_requirement_list = DMNImport.import_requirement_list(elem.xml_node, 'knowledge')
        except:
            pass
        try:
            elem.information_requirement_list = DMNImport.import_requirement_list(elem.xml_node, 'information')
        except:
            pass
        DMNImport.add_requirements_to_model(elem)

    @staticmethod
    def import_requirement_list(xml_node, requirement_type):
        requirement_list = []
        for item in DMNImport.get_list_by_tag(xml_node, requirement_type + 'Requirement'):
            try:
                if DMNImport.at_least_one_element_by_tag(item, 'requiredDecision'):
                    requir = DMNImport.get_first_element_by_tag(item, 'requiredDecision')
                elif DMNImport.at_least_one_element_by_tag(item, 'requiredInput'):
                    requir = DMNImport.get_first_element_by_tag(item, 'requiredInput')
                elif DMNImport.at_least_one_element_by_tag(item, 'requiredKnowledge'):
                    requir = DMNImport.get_first_element_by_tag(item, 'requiredKnowledge')
                elif DMNImport.at_least_one_element_by_tag(item, 'requiredAuthority'):
                    requir = DMNImport.get_first_element_by_tag(item, 'requiredAuthority')
                requirement_list.append(DMNImport.model.get_element_by_id(requir.attributes['href'].value[1:]))
            except:
                raise Exception('Can\'t find needed ' + requirement_type + ' requirement')
        return requirement_list

    @staticmethod
    def add_requirements_to_model(elem):
        try:
            for requirement in elem.authority_requirement_list:
                DMNImport.model.add_requirement(AuthorityRequirement(requirement, elem))
        except:
            pass
        try:
            for requirement in elem.knowledge_requirement_list:
                DMNImport.model.add_requirement(KnowledgeRequirement(requirement, elem))
        except:
            pass
        try:
            for requirement in elem.information_requirement_list:
                DMNImport.model.add_requirement(InformationRequirement(requirement, elem))
        except:
            pass


    #################################################################################################

    @staticmethod
    def at_least_one_element_by_tag(xml_node, tag):
        return False if len(DMNImport.get_list_by_tag(xml_node, tag)) < 1 else True

    @staticmethod
    def get_value_by_two_tags(xml_node, tag1, tag2):
        return xml_node.getElementsByTagName(tag1)[0].getElementsByTagName(tag2)[0].childNodes[0].toxml()

    @staticmethod
    def get_value_by_tag(xml_node, tag):
        try:
            return xml_node.getElementsByTagName(tag)[0].childNodes[0].toxml()
        except IndexError:
            return None

    @staticmethod
    def get_second_value_by_tag(xml_node, tag):
        try:
            return xml_node.getElementsByTagName(tag)[1].childNodes[0].toxml()
        except IndexError:
            return None

    @staticmethod
    def get_list_by_tag(xml_node, tag):
        return xml_node.getElementsByTagName(tag)

    @staticmethod
    def get_first_element_by_tag(xml_node, tag):
        return xml_node.getElementsByTagName(tag)[0]


    @staticmethod
    def get_name_id(xml_node, object):
        object.id = DMNImport.get_attribute_value(xml_node, 'id')
        object.name = DMNImport.get_attribute_value(xml_node, 'name')
        return object

    @staticmethod
    def get_attribute_value(xml_node, value_name):
        try:
            return xml_node.attributes[value_name].value
        except KeyError:
            return None

    @staticmethod
    def get_literal_expression(xml_node):
        try:
            return DMNImport.get_value_by_two_tags(xml_node, 'literalExpression', 'text')
        except KeyError:
            return None



