from .models.Rule1 import  find_cyclic_dependency, check_for_prohibited_words
import re

overall_rule_result = True
known_nouns = []
def ruleCheck(c_names, p_names,relations, Rule):
    global overall_rule_result
    # print("Before Check Rule 1")
    #Rule can be a phrase or if condition then rule
    r = Rule
    r = r.split(" ")
    s = [x for x in r if x]
    if (s[0].lower()  == "if" ):
        i = s.index("then")
        condition = s[1:i]
        next_rule = s[i+1:len(s)]
        print("Condition:", condition)
        #Condition: <there exist/doesn’t exist> | Noun | <in/between> | Noun/Nouns | <in> |  Diagrams
        c = condition
        if(c[0]=="there"):
            if(c[1]== "exist"):
                Noun1 = c[2]
                if(Noun1 in known_nouns):
                    #call that respective function
                    overall_rule_result = overall_rule_result and True
                else:
                    i = c.index("in")
                    if not i:
                        i = c.index("between")
                    rule_noun=c[2:i]
                    overall_rule_result = overall_rule_result and ruleCheck(c_names, p_names,relations," ".join(rule_noun))
            if(c[1]=="donot" or c[1]=="doesn\'t"):
                Noun1 = c[3]
                if (Noun1 in known_nouns):
                    # call that respective function
                    overall_rule_result =not( overall_rule_result and True)
                else:
                    i = c.index("in")
                    if not i:
                        i = c.index("between")
                    rule_noun = c[3:i]
                    overall_rule_result = not(overall_rule_result and ruleCheck(c_names, p_names,relations," ".join(rule_noun)))
            #in between nouns and diagram check is pending

        print("next_rule:", next_rule)
        next_rule_result = ruleCheck(c_names, p_names, relations, " ".join(next_rule))
        overall_rule_result = overall_rule_result and next_rule_result

    else:
        phrase = Rule
        print("Phrase:", phrase)
        print("before overall_rule_result: ",overall_rule_result)
        if ("-->" in relations.keys()):
            lst = relations["-->"]
        if ("cannot" in phrase and "\"" in phrase):
            print("cannot")
            overall_rule_result =  check_for_prohibited_words(c_names, p_names, phrase)
        elif ("\"" in phrase):
            print("can")
            overall_rule_result = not(check_for_prohibited_words(c_names, p_names, phrase))

        elif("not" in phrase and "cyclic" in phrase):
            print("not  cyclic")
            overall_rule_result = not(find_cyclic_dependency(lst))
        elif ("cyclic" in phrase):
            print("cyclic")
            overall_rule_result = find_cyclic_dependency(lst)
        print("After overall_rule_result: ", overall_rule_result)
    return overall_rule_result
    """result = checkRule1(c_names, p_names, Rule)
    if("-->" in relations.keys()):
        lst = relations["-->"]
    r = Rule
    r = r.split(" ")
    s = [x for x in r if x]
    if(s[0]=="if"):
        i = s.index("then")
        condition = s[1:i]
        next_rule = s[i:len(s)]

        print("s: ",s)
    if(False):
        result2 = find_cyclic_dependency(lst)
    # print("After Check Rule 1")
    return result"""


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
