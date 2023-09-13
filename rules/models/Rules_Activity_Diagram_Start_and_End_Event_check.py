def find_start_event(act_seq):
    if("start" in act_seq):
        return True
    return False


def find_end_event(act_seq):
    if ("stop" in act_seq):
        return True
    return False