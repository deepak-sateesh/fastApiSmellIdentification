from .models.Rule1 import checkRule1, find_cyclic_dependency
import re


def ruleCheck(c_names, p_names,relations, Rule):
    # print("Before Check Rule 1")
    result = checkRule1(c_names, p_names, Rule)
    lst=relations["-->"]
    result2 = find_cyclic_dependency(lst)
    # print("After Check Rule 1")
    return result2


def class_diagram_extract_class_names_and_parameters_and_relations(plantuml_representation):
    class_names = []
    parameter_names = []
    all_class_names = []
    relations2 = set()
    relations3 = set()
    relations4 = set()
    relation_dict = {}
    # Extract class names
    class_name_pattern = r"class\s+(\w+)\s+{*"
    class_matches = re.findall(class_name_pattern, plantuml_representation)
    class_names.extend(class_matches)

    # Extract parameter names

    parameter_name_pattern = r"\s+(\w+)"
    parameter_matches = re.findall(parameter_name_pattern, plantuml_representation)
    parameter_names.extend(parameter_matches)
    parameter_names = [i for i in parameter_names if i != 'class']
    for c in class_names:
        if c in parameter_names:
            parameter_names.remove(c)

    """for p in parameter_names:

        if p in class_names:
            class_names.remove(p)"""
    """
    < | -- Class02
    Class03 * -- Class04
    Class05
    o - - Class06
    Class07..Class08
    Class09 - - """
    relations = set()
    relation_lines = re.findall(r'(\w+) -\[*.*\]*-> (\w+)', plantuml_representation)
    relations.update(relation_lines)
    relation_dict["-->"] = relations

    relation_lines = re.findall(r'(\w+) <-\[*.*\]*- (\w+)', plantuml_representation)
    relations_rev = []
    relations_rev = [(x[1], x[0]) for x in relation_lines]
    relations.update(relations_rev)
    relation_dict["-->"] = relations
    for r in relations:
        all_class_names.append(r[0])
        all_class_names.append(r[1])


    relation_lines = re.findall(r'(\w+) \*-\[*.*\]*-  (\w+)', plantuml_representation)
    relations2.update(relation_lines)
    relation_dict["*--"] = relations2
    relation_lines = re.findall(r'(\w+) -\[*.*\]*-\* (\w+)', plantuml_representation)
    relations_rev = []
    relations_rev = [(x[1], x[0]) for x in relation_lines]
    relations2.update(relations_rev)
    relation_dict["*--"] = relations2
    for r in relations2:
        all_class_names.append(r[0])
        all_class_names.append(r[1])

    relation_lines = re.findall(r'(\w+) <\|-\[*.*\]*-  (\w+)', plantuml_representation)
    relations3.update(relation_lines)
    relation_dict["<|--"] = relations3
    relation_lines = re.findall(r'(\w+) -\[*.*\]*-\|> (\w+)', plantuml_representation)
    relations_rev = []
    relations_rev = [(x[1], x[0]) for x in relation_lines]
    relations3.update(relations_rev)
    relation_dict["<|--"] = relations3
    for r in relations3:
        all_class_names.append(r[0])
        all_class_names.append(r[1])

    relation_lines = re.findall(r'(\w+) o-\[*.*\]*-  (\w+)', plantuml_representation)
    relations4.update(relation_lines)
    relation_dict["o--"] = relations4
    relation_lines = re.findall(r'(\w+) -\[*.*\]*-o  (\w+)', plantuml_representation)
    relations_rev = []
    relations_rev = [(x[1], x[0]) for x in relation_lines]
    relations4.update(relations_rev)
    relation_dict["o--"] = relations4
    for r in relations4:
        all_class_names.append(r[0])
        all_class_names.append(r[1])

    class_names = list(set(class_names))

    parameter_names = list(set(parameter_names))
    class_names = set(class_names+(all_class_names))
    return class_names, parameter_names, relation_dict


def sequence_diagram_extract_class_names_and_parameters_and_relations(plantuml_representation):
    class_names = []
    parameter_names = []
    relations = set()
    relations2 = set()
    relation_dict = {}
    all_class_names = set()
    # Extract class names
    class_name_pattern = r"class\s+(\w+)\s+{*"
    class_matches = re.findall(class_name_pattern, plantuml_representation)
    class_names.extend(class_matches)

    # Extract parameter names

    parameter_name_pattern = r"\s+(\w+)"
    parameter_matches = re.findall(parameter_name_pattern, plantuml_representation)
    parameter_names.extend(parameter_matches)
    parameter_names = [i for i in parameter_names if i != 'class']
    for c in class_names:
        if c in parameter_names:
            parameter_names.remove(c)

    """for p in parameter_names:

        if p in class_names:
            class_names.remove(p)"""
    relation_lines = re.findall(r'(\w+) -\[.*\]-> (\w+)', plantuml_representation)
    relations.update(relation_lines)
    relation_dict["-->"] = relations
    #print("test", [rr for r in relations for rr in r])


    relation_lines = re.findall(r'(\w+) <\|--  (\w+)', plantuml_representation)
    relations2.update(relation_lines)
    relation_dict["<|--"] = relations2



    parameter_names = list(set(parameter_names))
    return class_names, parameter_names, relation_dict


def activity_diagram_extract_class_names_and_parameters_and_relations(plantuml_representation):
    class_names = []
    parameter_names = []
    relations = set()
    relations2 = set()
    relation_dict = {}
    # Extract class names
    class_name_pattern = r"class\s+(\w+)\s+{*"
    class_matches = re.findall(class_name_pattern, plantuml_representation)
    class_names.extend(class_matches)

    # Extract parameter names

    parameter_name_pattern = r"\s+(\w+)"
    parameter_matches = re.findall(parameter_name_pattern, plantuml_representation)
    parameter_names.extend(parameter_matches)
    parameter_names = [i for i in parameter_names if i != 'class']
    for c in class_names:
        if c in parameter_names:
            parameter_names.remove(c)

    """for p in parameter_names:

        if p in class_names:
            class_names.remove(p)"""
    relation_lines = re.findall(r'(\w+) -\[.*\]-> (\w+)', plantuml_representation)
    relations.update(relation_lines)
    relation_dict["-->"] = relations

    relation_lines = re.findall(r'(\w+) <\|--  (\w+)', plantuml_representation)
    relations2.update(relation_lines)
    relation_dict["<|--"] = relations2

    class_names = list(set(class_names))

    parameter_names = list(set(parameter_names))
    return class_names, parameter_names, relation_dict
