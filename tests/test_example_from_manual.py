from dmn_python.DMNImport import DMNImport
from dmn_python.DMNVisualisation import DMNVisualisation
from dmn_python.DMNExport import DMNExport
import os

example_from_manual_path = 'examples/exampleFromManual.xml'

model = DMNImport.load_model_from_xml(os.path.abspath(example_from_manual_path))
DMNExport.export_model_to_xml(model)
DMNVisualisation.display_diagram(model)

# displaying all decision tables
for element in model.element_list:
    if hasattr(element, 'decision_table') and element.decision_table != None:
            DMNVisualisation.print_decision_table(model.get_element_by_name(element.name))
