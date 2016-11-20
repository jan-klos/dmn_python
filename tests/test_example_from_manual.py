from DMNImport import DMNImport
from DMNVisualisation import DMNVisualisation
from DMNExport import DMNExport
import os

example_from_manual_path = 'examples/exampleFromManual.xml'

diagram = DMNImport.load_diagram_from_xml(os.path.abspath(example_from_manual_path))
DMNExport.export_to_xml(diagram)
DMNVisualisation.display_diagram(diagram)

for element in diagram.element_list:
    try:
        DMNVisualisation.print_decision_table(diagram.get_element_by_name(element.name))
    except AttributeError:
        pass