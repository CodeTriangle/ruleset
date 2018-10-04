import datetime
from rulekeep.utils import get_contents
import yaml

cache = {}

def proposal_data(num):
    snum = str(num)
    try:
        cache[snum]
    except KeyError:
        cache[snum] = yaml.load(
            get_contents("proposals/{}".format(num))
        )
    return cache[snum]

def chtype_string(change):
    chtype = change["type"]
    if chtype == "enactment":
        return "Enacted"
    elif chtype == "initial":
        return "Initial {} rule {}".format(
            change["mutability"], change["id"]
        )
    elif chtype == "mutation":
        result =  "Mutated"

        try: result = result + " from MI=" + str(change["old-mi"])
        except KeyError: pass

        try: result = result + " to MI=" + str(change["new-mi"])
        except KeyError: pass

        return result
    elif chtype == "renumbering":
        return "Renumbered"
    elif chtype == "reenactment":
        return "Re-enacted and amended({})"
    elif chtype == "amendment":
        result = "Amended"
        try: change["uncounted"]
        except KeyError: result += "({})"
        return result
    elif chtype == "infection-amendment":
        return "Infected and amended({})"
    elif chtype == "infection":
        return "Infected"
    elif chtype == "retitling":
        return "Retitled"
    elif chtype == "repeal":
        return "Repealed"
    elif chtype == "power-change":
        result = "Power changed"
        try: result = result + " from " + str(change["old-power"])
        except KeyError: pass

        try: result = result + " to " + str(change["new-power"])
        except KeyError: pass

        return result
    elif chtype == "committee-assignment":
        return "Assigned to the " + change["committee"]
    elif chtype == "unknown":
        return "History unknown..."
    else:
        print("\tunrecognised type: " + chtype)
        return "Changed"

def agent_string(agent):
    try:
        proposal = agent["proposal"]
        result = "Proposal " + str(proposal)
        data = proposal_data(proposal)

        try: result = result + " \"%s\"" % data["title"]
        except KeyError: pass
        
        try:
            if proposal_data(proposal)["disinterested"]:
                result = result + " [disinterested]"
        except KeyError: pass
        
        try:
            data["author"]
            return result + " " + proposal_blame(proposal)
        except KeyError:
            return result
    except KeyError: pass

    try: return "Rule %d" % agent["rule"]
    except KeyError: pass

    try: return "a convergence caused by " + agent_string(agent["convergence"])
    except KeyError: pass

    try:
        agent["cleaning"]
        return "cleaning ({})".format(agent["cleaning"]["by"])
    except KeyError: pass

    try: return agent["ratification"]["document"] + " ratification"
    except KeyError: return "ratification"

    try: return "Decree given by " + agent["decree"]
    except KeyError: pass

def proposal_blame(num):
    proposal = proposal_data(num)
    result = "(" + proposal["author"]
    try:
        coauthors = proposal["coauthors"]
        if coauthors != []:
            result = result + "; with " + ", ".join(coauthors)
    except KeyError: pass
    except TypeError: pass
    return result + ")"

def date_string(date):
    if date == datetime.date(1993, 6, 30): return "Agora's birth"
    try: return date.isoformat()
    except KeyError: pass
    except AttributeError:
        return "around " + date["around"].isoformat()

def change_string(ch):
    result = chtype_string(ch["change"])

    try:
        result = result + " by " + agent_string(ch["agent"])
    except KeyError: pass

    try: result = result + ", " + date_string(ch["date"])
    except: pass

    return result