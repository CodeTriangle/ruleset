# Copyright (C) 2019-2020, CodeTriangle
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#       
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#       
#     * Neither the name of CodeTriangle nor the names of other
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL CODETRIANGLE BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.

import datetime
from os import listdir
from .utils import *
import yaml

cache = {}

def proposal_data(num, log=False):
    global cache
    
    if try_get(cache, num):
        if log: print(f"\t{num}\talready scanned")
    else:
        if log: print(f"\t{num}\treading from file")
        cache[num] = yaml.load(
            get_contents("proposals/" + num),
            Loader=yaml.FullLoader
        )
        if log: print("\t\tread")
    return cache[num]

def chtype_string(change):
    chtype = change["type"]
    if chtype == "enactment":
        return "Enacted"
    elif chtype == "initial":
        return f"Initial {change['mutability']} rule {change['id']}"
    elif chtype == "mutation":
        return f"Mutated from MI={change['old-mi']} to {change['new-mi']}"
    elif chtype == "renumbering":
        return "Renumbered"
    elif chtype == "reenactment":
        return f"Re-enacted({{}}){' and amended' if try_get(change, 'unchanged') else ''}"
    elif chtype == "amendment":
        return f"Amended{'({})' if try_get(change, 'uncounted') else ''}"
    elif chtype == "infection-amendment":
        return "Infected and amended({})"
    elif chtype == "infection":
        return "Infected"
    elif chtype == "retitling":
        return "Retitled"
    elif chtype == "repeal":
        return "Repealed"
    elif chtype == "power-change":
        return f"Power changed from {change['old-power']} to {change['new-power']}"
    elif chtype == "committee-assignment":
        return "Assigned to the " + change["committee"]
    elif chtype == "unknown":
        return "History unknown..."
    else:
        print("\tunrecognised type: " + chtype)
        return "Changed"

def agent_string(agent):
    if try_get(agent, "proposal"):
        proposal = agent["proposal"]
        result = "P" + str(proposal)
        data = proposal_data(proposal)
        result = f"{result} '{try_get(data, 'title')}'"
        metadata = []

        if try_get(data, "chamber"):
            metadata.append(data["chamber"])
        if try_get(data, "disinterested"):
            metadata.append("disi.")
        if metadata:
            result = f"{result} [{', '.join(metadata)}]"
        
        if try_get(data, "author"):
            return result + " " + proposal_blame(proposal)
        else:
            return result

    if try_get(agent, "rule"):
        return f"R{agent['rule']}"
    if try_get(agent, "convergence"):
        return f"a convergence caused by {agent_string(agent['convergence'])}"
    if try_get(agent, "cleaning"):
        return f"cleaning ({agent['cleaning']['by']})"
    if try_get(agent, "ratification"):
        return f"ratification of {agent['ratification']['document']}"
    if try_get(agent, "decree"):
        return f"Decree given by {agent['decree']}"

def proposal_blame(num):
    proposal = proposal_data(num)
    result = "(" + proposal["author"]
    if try_get(proposal, 'coauthors'):
        result = ", ".join([result, *proposal['coauthors']])
    return result + ")"

def date_string(date):
    if date == datetime.date(1993, 6, 30): return "Agora's birth"
    try: return better_date(date)
    except AttributeError: pass

    try: return "around " + better_date(date["around"])
    except KeyError: pass
    except AttributeError: pass

    try: return "between {} and {}".format(
        better_date(date["between"]), better_date(date["and"])
    )

    except KeyError: pass
    except AttributeError: pass

def change_string(ch):
    result = chtype_string(ch["change"])

    if try_get(ch, "agent"):
        result = f"{result} by {agent_string(ch['agent'])}"
    if try_get(ch, "date"):
        result = f"{result}, {date_string(ch['date'])}"

    return result

def get_stats():
    return {
        "hp": max(to_int_list(listdir("proposals"))),
        "hr": max(to_int_list(listdir("rules")))
    }
