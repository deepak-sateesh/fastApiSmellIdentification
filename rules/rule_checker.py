from .models.Rule1 import checkRule1
import re
def ruleCheck(c_names, p_names,Rule):
    #print("Before Check Rule 1")
    result = checkRule1(c_names, p_names,Rule)

    #print("After Check Rule 1")
    return result




def extract_class_names_and_parameters(plantuml_representation):
    class_names = []
    parameter_names = []


    # Extract class names
    class_name_pattern = r"class\s+(\w+)\s+{"
    class_matches = re.findall(class_name_pattern, plantuml_representation)
    class_names.extend(class_matches)

    # Extract parameter names

    parameter_name_pattern = r"\s+(\w+)"
    parameter_matches = re.findall(parameter_name_pattern, plantuml_representation)
    parameter_names.extend(parameter_matches)
    parameter_names=[i for i in parameter_names if i != 'class']
    for c in class_names:
        if c in parameter_names:
            parameter_names.remove(c)

    """for p in parameter_names:

        if p in class_names:
            class_names.remove(p)"""


    class_names=list(set(class_names))

    parameter_names=list(set(parameter_names))
    return class_names, parameter_names


