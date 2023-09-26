from .models.Rules_Activity_Diagram_Start_and_End_Event_check import find_start_event, find_end_event
from .models.Rules_Cyclic_Dependency import find_cyclic_dependency
from .models.Rules_Prohibited_Words import   check_for_prohibited_words


overall_rule_result = True
known_nouns = ["cyclic", "infinite_loop", "start_activity", "end_activity" ]
prohibited_words = set()
cycles = []
missing_activities = set()
def ruleCheck(c_names, p_names,relations, activity_sequence, messages, Rule):
    global overall_rule_result, prohibited_words
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
                        cyclic_dependency_res = find_cyclic_dependency(lst)
                        overall_rule_result = overall_rule_result and cyclic_dependency_res[0]
                        cycles.append(cyclic_dependency_res[1])
                else:
                    i = c.index("in")
                    if not i:
                        i = c.index("between")
                    rule_noun=c[2:i]
                    overall_rule_result = overall_rule_result and ruleCheck(c_names, p_names,relations ,activity_sequence , messages," ".join(rule_noun))
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
                    overall_rule_result = not(overall_rule_result and ruleCheck(c_names, p_names,relations, activity_sequence, messages," ".join(rule_noun)))
            #in between nouns and diagram check is pending


        print("next_rule:", next_rule)
        next_rule_result = ruleCheck(c_names, p_names, relations, activity_sequence, messages, " ".join(next_rule))
        overall_rule_result = overall_rule_result and next_rule_result

        #then part



    else:
        phrase = Rule
        print("Phrase:", phrase)
        print("before overall_rule_result: ",overall_rule_result)


        if ("cannot" in phrase and ("\"" in phrase or '”' in phrase)):
            print("cannot")
            r = check_for_prohibited_words(c_names, p_names, phrase)
            overall_rule_result =r[0]
            prohibited_words.add(r[1])
        elif ("\"" in phrase or '”' in phrase):
            print("can")
            r = check_for_prohibited_words(c_names, p_names, phrase)
            overall_rule_result =not( r[0])
            prohibited_words.add(r[1])

        elif("not" in phrase and "cyclic" in phrase and lst):
            print("not  cyclic")
            cyclic_dependency_res = find_cyclic_dependency(lst)
            overall_rule_result = not(cyclic_dependency_res[0])
            cycles.append(cyclic_dependency_res[1])
        elif ("cyclic" in phrase and lst):
            print("cyclic")
            cyclic_dependency_res = find_cyclic_dependency(lst)
            overall_rule_result = cyclic_dependency_res[0]
            cycles.append(cyclic_dependency_res[1])




        elif ("start_event" in phrase and "Activity_diagram" in phrase and "should not" in phrase):
            overall_rule_result = not (find_start_event(activity_sequence))
            if not (find_start_event(activity_sequence)):
                missing_activities.add('start')
            if not (find_end_event(activity_sequence)):
                missing_activities.add('stop')
        elif ("start_event" in phrase and "Activity_diagram" in phrase and "should " in phrase):
            overall_rule_result = find_start_event(activity_sequence)
            if not (find_start_event(activity_sequence)):
                missing_activities.add('start')
            if not (find_end_event(activity_sequence)):
                missing_activities.add('stop')

        elif ("end_event" in phrase and "Activity_diagram" in phrase and "should not" in phrase):
            overall_rule_result = not(find_end_event(activity_sequence))
            if not (find_start_event(activity_sequence)):
                missing_activities.add('start')
            if not (find_end_event(activity_sequence)):
                missing_activities.add('stop')
        elif ("end_event" in phrase and "Activity_diagram" in phrase and "should" in phrase):
            overall_rule_result = find_end_event(activity_sequence)
            if not (find_start_event(activity_sequence)):
                missing_activities.add('start')
            if not (find_end_event(activity_sequence)):
                missing_activities.add('stop')

        else:
            print("No match")
        print("After overall_rule_result: ", overall_rule_result)


    return [overall_rule_result, prohibited_words, cycles, missing_activities]
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


