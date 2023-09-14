import spacy
import re


# ElementsName  cannot have  “AND” in Class Diagram
#elements name : list of [Class1_Name, ClassAndName,...]
#Elements_name=["Class1_Name", "Class_And_Name","ClassNameANDName"]

ModalVerbs= ["Cannot","Can"]
nlp = spacy.load("en_core_web_sm")
'''Rule: 	Phrase
	        <If> | Condition | <Then> | Rule

Condition: <there exist/doesn’t exist> | Noun | <in/between> | Noun/Nouns | <in> |  Diagrams       

Noun: 	Known nouns
Rule   

Phrase: 	Noun | Modal verb | Verb | Noun | <in> | Diagram

Known nouns: <Number of edges/ threshold/ blacklisted names/ …>


Modal verb: <Shall/Shall not/ should/ should not/ must/ must not/ …>

Verb: 	<is/ are/ …>

Diagram: <Class diagram/ Sequence Diagram/ Activity Diagram>'''

#Phrase: 	Noun | Modal verb | Verb | Noun | <in> | Diagram
def parse_sentence(sentence):
    # Process the sentence using spaCy
    doc = nlp(sentence)

    # Iterate through each token (word) in the sentence
    for token in doc:
        print(f"Word: {token.text}, Part of Speech: {token.pos_}")





# print(t.split(" "))
def check_for_prohibited_words(class_names,parameter_names,sentence):
    Elements_names = list(class_names) + parameter_names
    s = sentence
    s = s.split(" ")
    s = [x for x in s if x]
    ss = [[x,"N"] for x in s]
    ss[0][1] = "Noun"
    ss[1][1] = "Modal Verb"
    ss[2][1] = "Verb"
    ss[3][1] = "Noun"
    ss[4][1] = "In"
    ss[5][1] = "Diagram"
    print(ss)
    #parse_sentence(sentence)
    if (ss[0][1] == "Noun"):
        #prohibitedWord = ((ss[3][0])[1:-1]).lower()
        prohibitedWord = ((ss[3][0])[1:-1]).lower()
        prohibitedWordAsItIs = (ss[3][0])[1:-1]
        print("prohibitedWord: "+prohibitedWordAsItIs)

        print(Elements_names)
        for e in Elements_names:
            e = e.lower()
            #print("efind")
            #print(e.find(prohibitedWord))
            if e.find(prohibitedWord) >= 0:
                return [False, prohibitedWordAsItIs]

        if (ss[1][1] == "Modal Verb"):
            if (ss[2][1] == "Verb"):
                if (ss[3][1] == "Noun"):
                    if (ss[4][1] == "In"):
                        if (ss[5][1] == "Diagram"):
                            return [True, prohibitedWord]
    return [False, prohibitedWordAsItIs]
    '''s=sentence
    parse_sentence(sentence)

    s=s.split(" ")
    s.pop(" ")
    s[0][1]="Noun"
    s[1][1] == "Modal Verb"
    s[2][1] == "Verb"
    s[3][1] == "Noun"
    s[4][1] == "In"
    s[5][1] == "Diagram"
    print(s)
    if(s[0][1]=="Noun"):
        if(s[0] in Elements_name):
            if(s[1][1]=="Modal Verb"):
                if(s[2][1]=="Verb"):
                    if (s[3][1] == "Noun"):
                        if (s[4][1] == "In"):
                            if (s[5][1] == "Diagram"):
                                return "True"
    return "False"'''


