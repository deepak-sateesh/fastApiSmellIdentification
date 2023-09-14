from plantuml import PlantUML
import re, io
import PIL.Image as Image

OPIMAGEDIR = "Output_Images/"


def map_files_to_results(uploaded_file_strings, prohibited_words, cycles):
    res = []
    #res.clear()
    local_cycles = cycles[0]
    for file in uploaded_file_strings:
            server = PlantUML(url='http://www.plantuml.com/plantuml/img/',
                              basic_auth={},
                              form_auth={}, http_opts={}, request_opts={})
            # print(file.file.read().decode("utf-8"))

            file_string = file[1]
            #diagram_type = identify_diagram_type(file_string)
            #marking prohibited words in class diagram
            for p in prohibited_words:
                if(p in file_string):
                    file_string = re.sub(f'({p})(?=.*:)', r'<font color="red">\1</font>', file_string) #attribute with type
                    file_string = re.sub(f'({p})(?=.*\s*.*}}|\s*}})', r'<font color="red">\1</font>', file_string) #attribute without type
                    file_string = re.sub(f'({p}.*\s*)(?=\s*{{)', r'\1 << (C,DarkRed) >> ', file_string) #class names

            # marking cycles  in class diagram

            for cycle in local_cycles:
                for i in range(len(cycle)):
                    source_class = cycle[i]
                    target_class = cycle[(i + 1) % len(cycle)]
                    #file_string = file_string.replace(f'{source_class} -.*-> {target_class}', f'{source_class} -[#blue]-> {target_class}')
                    file_string = re.sub(f'{source_class}\s*-.*->\s*{target_class}', f'{source_class} -[#blue]-> {target_class}', file_string)  # class names

            s = server.processes(file_string)
            image = Image.open(io.BytesIO(s))
            image.save(f"{OPIMAGEDIR}{file[0]}->.png")

            # saved_img=Image.open(file.filename+'->.png')
            res.append(file[0] + '->.png')
    return res