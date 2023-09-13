from .models.Rules_Cyclic_Dependency import find_cyclic_dependency
from .models.Rules_Prohibited_Words import   check_for_prohibited_words
import re

overall_rule_result = True
known_nouns = ["cyclic", "infinite_loop" ]
def ruleCheck(c_names, p_names,relations, Rule):
    global overall_rule_result
    if ("-->" in relations.keys()):
        lst = relations["-->"]
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
                    if(Noun1=="cyclic"):
                        overall_rule_result = overall_rule_result and find_cyclic_dependency(lst)
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

        #then part



    else:
        phrase = Rule
        print("Phrase:", phrase)
        print("before overall_rule_result: ",overall_rule_result)


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
        else:
            print("No match")
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


