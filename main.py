from typing import List

from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import io
import PIL.Image as Image
from plantuml import PlantUML
from fastapi.staticfiles import StaticFiles

from os.path import abspath

from starlette.responses import RedirectResponse

from rules.rule_checker import ruleCheck, extract_class_names_and_parameters
import spacy
app = FastAPI()
IMAGEDIR = "Images/"
app.mount("/Images", StaticFiles(directory="Images"), name="Images")

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

class_names=[]
parameter_names=[]

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/processRule", response_class=HTMLResponse)
async def read_item(request: Request, input_text: str = Form(...)):
    global class_names, parameter_names
    t = input_text
    nlp = spacy.load("en_core_web_sm")
    # Example usage
    plantuml_representation = '''
    class Student {
    Name
    }
    Student "0..*" - "1..*" Course
    (Student, Course) .. Enrollment
    class Enrollment {
    drop()
    cancel()
    }
    '''
    '''class_names, parameter_names = extract_class_names_and_parameters(plantuml_representation)
    print("Class names:", class_names)
    print("Parameter names:", parameter_names)'''
    #global class_names, parameter_names
    #r = ruleCheck(t)

    #print("Result of rule: "+ t+ " => "+ r)
    r = ruleCheck(class_names, parameter_names, input_text)
    #print("Result of rule: " + input_text + " => " + r)
    result = "Result of rule: " + input_text + " => " + r
    def parse_sentence(sentence):
        # Process the sentence using spaCy
        doc = nlp(sentence)

        # Iterate through each token (word) in the sentence
        for token in doc:
            print(f"Word: {token.text}, Part of Speech: {token.pos_}")

    # Example sentence to parse
    #sentence = "The quick brown fox jumps over the lazy dog."
    #parse_sentence(t)
    
    #print(t.split(" "))
    return templates.TemplateResponse(
        "result.html", {"request": request, "input_text": input_text, "result":result}
    )

@app.post("/process_plantuml")
async def process_plantuml(request: Request, files: List[UploadFile] = File(...)):
    global class_names, parameter_names
    class_names=[]
    parameter_names=[]
    # Process the PlantUML files here


    # You can access each file using `files` list


    # Generate the output HTML

    output_html = "<h1>Processing Results</h1>"

    saved_images=[]
    for file in files:
        output_html += f"<p>Processed: {file.filename}</p>"
        server = PlantUML(url='http://www.plantuml.com/plantuml/img/',
                          basic_auth={},
                          form_auth={}, http_opts={}, request_opts={})
        #print(file.file.read().decode("utf-8"))

        file_string = file.file.read().decode("utf-8")
        class_names, parameter_names = extract_class_names_and_parameters(file_string)
        print("Class names:", class_names)
        print("Parameter names:", parameter_names)
        s = server.processes(file_string)
        image = Image.open(io.BytesIO(s))
        image.save(f"{IMAGEDIR}{file.filename}->.png")

        #saved_img=Image.open(file.filename+'->.png')
        saved_images.append(file.filename+'->.png')
    #print(saved_images)


    return templates.TemplateResponse("output.html", {"request": request, "output_html": output_html, "Images":saved_images})

@app.get("/back_button")
async def handle_back_button():
    return RedirectResponse(url="/")