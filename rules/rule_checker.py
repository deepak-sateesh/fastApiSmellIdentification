from .models.Rule1 import checkRule1
import re
def ruleCheck(Sentence):
    print("Before Check Rule 1")
    result = checkRule1(Sentence)

    print("After Check Rule 1")
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


    return class_names, parameter_names


