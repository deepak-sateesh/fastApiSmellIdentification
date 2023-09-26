import io, re
from typing import List

import PIL.Image as Image
import spacy
from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from plantuml import PlantUML
from starlette.responses import RedirectResponse

from map_file_and_rule_results import map_files_to_results
from rules.rule_checker import ruleCheck, missing_activities
from uml_diagram_information_extractor import class_diagram_extract_class_names_and_parameters_and_relations, \
    activity_diagram_extract_activity_sequence, sequence_diagram_extract_messages_information

app = FastAPI()
IPIMAGEDIR = "Input_Images/"
OPIMAGEDIR = "Output_Images/"
SMELLDEFDIR = "smell_definitions/"
app.mount("/Input_Images", StaticFiles(directory="Input_Images"), name="Input_Images")
app.mount("/Output_Images", StaticFiles(directory="Output_Images"), name="Output_Images")
app.mount("/smell_definitions", StaticFiles(directory="smell_definitions"), name="smell_definitions")

'''@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}



@app.get("/addRule")
async def add_rule(rule: str):
    return {"message": f"Hello {name}"}'''

templates = Jinja2Templates(directory="templates")
plant_uml_files = []
class_names = []
parameter_names = []
relations = {}
activity_sequence = []
messages = {}

uploaded_file_strings = []

@app.get("/", response_class = HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/processRule", response_class=HTMLResponse)
async def read_item(request: Request, input_text: str = Form(...)):
    global class_names, parameter_names, relations, activity_sequence, messages, plant_uml_files, uploaded_file_strings
    t = input_text
    nlp = spacy.load("en_core_web_sm")
    result_images=[]
    r = ruleCheck(class_names, parameter_names, relations, activity_sequence, messages, input_text)
    if r[0]:
        result = "Result of rule: " + input_text + " => " + "True"
    else:
        result = "Result of rule: " + input_text + " => " + "False"
    prohibited_words = r[1]
    cycles = r[2]
    missing_activities = r[3]
    # print("Result of rule: " + input_text + " => " + r)
    output_html = ""
    saved_images = []
    """for file in uploaded_file_strings:
        server = PlantUML(url='http://www.plantuml.com/plantuml/img/',
                          basic_auth={},
                          form_auth={}, http_opts={}, request_opts={})
        # print(file.file.read().decode("utf-8"))

        file_string = file[1]
        diagram_type = identify_diagram_type(file_string)

        s = server.processes(file_string)
        image = Image.open(io.BytesIO(s))
        image.save(f"{OPIMAGEDIR}{file[0]}->.png")

        # saved_img=Image.open(file.filename+'->.png')
        saved_images.append(file[0] + '->.png')"""
    result_images=map_files_to_results(uploaded_file_strings, prohibited_words, cycles, missing_activities)

    def parse_sentence(sentence):
        # Process the sentence using spaCy
        doc = nlp(sentence)

        # Iterate through each token (word) in the sentence
        for token in doc:
            print(f"Word: {token.text}, Part of Speech: {token.pos_}")

    # Example sentence to parse
    # sentence = "The quick brown fox jumps over the lazy dog."
    # parse_sentence(t)

    # print(t.split(" "))
    return templates.TemplateResponse(
        "result.html", {"request": request, "input_text": input_text, "result": result, "Output_Images": result_images}
    )

def read_file_lines(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            # Remove newline characters from each line and create a list
            lines = [line.strip() for line in lines]
            return lines
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []


@app.post("/checkSmells", response_class=HTMLResponse)
async def read_item(request: Request):
    result = ""
    result_images = []
    global class_names, parameter_names, relations, activity_sequence, messages, plant_uml_files, uploaded_file_strings
    # Provide the path to your text file
    file_path = f"{SMELLDEFDIR}smells.txt"  # Replace with the actual file path

    # Call the function to read the file
    lines = read_file_lines(file_path)
    for l in lines:
        input_text = l
        t = input_text
        nlp = spacy.load("en_core_web_sm")

        r = ruleCheck(class_names, parameter_names, relations, activity_sequence, messages, input_text)
        if r[0]:
            result += "Result of rule: " + input_text + " => " + "True\n <br/>"
        else:
            result += "Result of rule: " + input_text + " => " + "False <br/>"
        prohibited_words = r[1]
        cycles = r[2]
    # print("Result of rule: " + input_text + " => " + r)
    output_html = ""
    saved_images = []
    """for file in uploaded_file_strings:
        server = PlantUML(url='http://www.plantuml.com/plantuml/img/',
                          basic_auth={},
                          form_auth={}, http_opts={}, request_opts={})
        # print(file.file.read().decode("utf-8"))

        file_string = file[1]
        diagram_type = identify_diagram_type(file_string)

        s = server.processes(file_string)
        image = Image.open(io.BytesIO(s))
        image.save(f"{OPIMAGEDIR}{file[0]}->.png")

        # saved_img=Image.open(file.filename+'->.png')
        saved_images.append(file[0] + '->.png')"""
    result_images = map_files_to_results(uploaded_file_strings, prohibited_words, cycles, missing_activities)

    def parse_sentence(sentence):
        # Process the sentence using spaCy
        doc = nlp(sentence)

        # Iterate through each token (word) in the sentence
        for token in doc:
            print(f"Word: {token.text}, Part of Speech: {token.pos_}")

    # Example sentence to parse
    # sentence = "The quick brown fox jumps over the lazy dog."
    # parse_sentence(t)

    # print(t.split(" "))
    return templates.TemplateResponse(
        "smell_result.html", {"request": request, "input_text": input_text, "result": result, "Output_Images": result_images}
    )


def identify_diagram_type(plantuml_code):
    # Regular expression patterns
    sequence_diagram_start_pattern = re.compile(r'@startuml\s*')
    sequence_diagram_end_pattern = re.compile(r'@enduml\s*')
    sequence_message_pattern = re.compile(r'\w+\s*(->|--|<--)\s*\w+:.*')

    # Check for sequence diagram markers and messages
    contains_start_marker = sequence_diagram_start_pattern.search(plantuml_code)
    contains_end_marker = sequence_diagram_end_pattern.search(plantuml_code)
    contains_sequence_messages = sequence_message_pattern.search(plantuml_code)

    if contains_start_marker and contains_end_marker and contains_sequence_messages:
        return "Sequence Diagram"

    # Regular expression patterns
    activity_start_pattern = re.compile(r':.*[\s]*.*;')
    decision_pattern = re.compile(r'if\s*\(.+?\)\s*then\s*\(.+?\)')
    fork_join_pattern = re.compile(r'(fork|join)')
    flow_arrow_pattern = re.compile(r'->|--|<--')
    class_keyword_pattern = re.compile(r'.*class.*')


    # Check for activity diagram elements
    contains_activities = activity_start_pattern.search(plantuml_code)
    contains_decision = decision_pattern.search(plantuml_code)
    contains_fork_join = fork_join_pattern.search(plantuml_code)
    contains_flow_arrows = flow_arrow_pattern.search(plantuml_code)
    contains_class_keyword = class_keyword_pattern.search(plantuml_code)


    if not contains_class_keyword and (contains_activities or contains_decision or contains_fork_join or contains_flow_arrows):
        return "Activity Diagram"

    # Sample PlantUML class diagram code
    plantuml_code = """
    @startuml
    class Class1 {
      + attribute1: type
      - attribute2: type
      + method1(): returnType
      - method2(param: type): returnType
    }
    Class1 --|> Class2
    @enduml
    """

    # Regular expression patterns
    class_declaration_pattern = re.compile(r'class\s+\w+\s*\{')
    relationship_pattern = re.compile(r'--|<--|\.\.|<\|')
    attribute_method_pattern = re.compile(r'[-+]\s+\w+\(.*\):.*')

    # Check for class diagram elements
    contains_class_declaration = class_declaration_pattern.search(plantuml_code)
    contains_relationships = relationship_pattern.search(plantuml_code)
    contains_attributes_methods = attribute_method_pattern.search(plantuml_code)

    if contains_class_declaration or contains_relationships or contains_attributes_methods:
        return "Class Diagram"

    """ if "class" in plantuml_code:
        return "Class Diagram"
    elif "participant" in plantuml_code:
        return "Sequence Diagram"
    elif any(keyword in plantuml_code for keyword in ["start", "end", "if", "while"]):
        return "Activity Diagram"
    else:
        return "Unknown Diagram"""

    return "Unknown Diagram"""


@app.post("/process_plantuml")
async def process_plantuml(request: Request, files: List[UploadFile] = File(...)):
    global class_names, parameter_names, relations, activity_sequence, messages, plant_uml_files, uploaded_file_strings
    plant_uml_files = files
    class_names = []
    parameter_names = []
    # Process the PlantUML files here

    # You can access each file using `files` list

    # Generate the output HTML

    output_html = "<h1>Processing Results</h1>"

    saved_images = []
    for file in files:
        output_html += f"<p>Processed: {file.filename}</p>"
        server = PlantUML(url='http://www.plantuml.com/plantuml/img/',
                          basic_auth={},
                          form_auth={}, http_opts={}, request_opts={})
        # print(file.file.read().decode("utf-8"))

        file_string = file.file.read().decode("utf-8")
        uploaded_file_strings.append((file.filename,file_string))
        diagram_type = identify_diagram_type(file_string)
        if diagram_type == "Class Diagram":
            print("Class diagram")
            class_names, parameter_names, relations = class_diagram_extract_class_names_and_parameters_and_relations(
                file_string)
            print("Class names:", class_names)
            print("Parameter names:", parameter_names)
            print("Relations :", relations)

        elif diagram_type == "Sequence Diagram":
            # class_names, parameter_names, relations = sequence_diagram_extract_class_names_and_parameters_and_relations(file_string)
            print("Sequence diagram")
            messages = sequence_diagram_extract_messages_information(file_string)
            # Print the stored messages
            for message in messages:
                print(f"{message['sender']} -> {message['receiver']}: {message['message']}")

        elif diagram_type == "Activity Diagram":
            activity_sequence = activity_diagram_extract_activity_sequence(file_string)
            print("Activity diagram")
            print("Activity sequence: ", activity_sequence)

        s = server.processes(file_string)
        image = Image.open(io.BytesIO(s))
        image.save(f"{IPIMAGEDIR}{file.filename}->.png")

        # saved_img=Image.open(file.filename+'->.png')
        saved_images.append(file.filename + '->.png')
        #file.file.close()

    # print(saved_images)

    return templates.TemplateResponse("output.html",
                                      {"request": request, "output_html": output_html, "Input_Images": saved_images})


@app.get("/back_button")
async def handle_back_button():
    return RedirectResponse(url="/")
