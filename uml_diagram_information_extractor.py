import re

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


def sequence_diagram_extract_messages_information(plantuml_representation):
    # Sample PlantUML Sequence Diagram code
    plantuml_code = """
    @startuml
    Participant A
    Participant B
    A -> B: Request 1
    B --> A: Response 1
    A -> B: Request 2
    B --> A: Response 2
    @enduml
    """

    # Split the code into lines
    lines = plantuml_code.split('\n')

    # Initialize a list to store messages
    messages = []

    # Iterate through the lines to extract messages
    for line in lines:
        # Check if the line represents a message
        if "->" in line:
            parts = line.split("->")
            sender = parts[0].strip()
            receiver_and_message = parts[1].strip().split(":")
            receiver = receiver_and_message[0].strip()
            message = receiver_and_message[1].strip() if len(receiver_and_message) > 1 else ""

            # Create a dictionary to represent the message and add it to the list
            message_info = {
                "sender": sender,
                "receiver": receiver,
                "message": message
            }
            messages.append(message_info)
    return messages


def activity_diagram_extract_activity_sequence(plantuml_representation):




    # Regular expression pattern to match activity labels

    # Regular expression pattern to match activity labels
    activity_label_pattern = re.compile(r'(?<=:).*[\s]*.*(?=;)')
   # r':(.*?)(?=;|@enduml)'
    #r'(?<=:)(.*?)(?=;|@enduml)'

    # Find all activity labels in the code
    activity_labels = activity_label_pattern.findall(plantuml_representation)

    start_node_pattern = re.compile(r'start')
    stop_node_pattern = re.compile(r'stop')

    # Find the start node in the code
    start_node_found = start_node_pattern.search(plantuml_representation)

    # Find the stop node in the code
    stop_node_found = stop_node_pattern.search(plantuml_representation)
    # Clean up whitespace and print the extracted activity labels

    cleaned_activity_labels = [activity.strip() for activity in activity_labels if activity.strip()]
    if(start_node_found):
       cleaned_activity_labels.insert(0,"start")
    if(stop_node_found):
        cleaned_activity_labels.append("stop")
    return cleaned_activity_labels

