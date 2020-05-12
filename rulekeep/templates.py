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

from .utils import *
from .history import *

short_rule_format = get_contents("config/short_rule_format")
full_rule_format  = get_contents("config/full_rule_format")

def line(ch, w=72):
    return "".join([ch for i in range(0, w)])

def indent(tx, w=6):
    return "\n".join([line(" ", w) + i for i in tx.split("\n")])

def section_heading(section):
    return "{}\n{}\n{}\n{}\n".format(
        line("="), section["name"],
        indent(section["note"].strip(), 3), line("-")
    )

def rule_heading(rule):
    rev = 0
    for i in rule["history"]:
        if not try_get(i["change"], "uncounted"):
            if i["change"]["type"] in ["amendment",
                                       "reenactment",
                                       "infection-amendment"]:
                rev = rev + 1
    return f"Rule {rule['id']}/{rev} (Power={rule['power']})\n{rule['name']}"

def short_rule(rule):
    global short_rule_format
    
    return short_rule_format.format(
        heading=rule_heading(rule),
        text=indent(rule["text"].strip()),
        line=line("-")
    )

def history(hist):
    result = ""

    for change in hist:
        result = f"{result}\n{fixed_width(change_string(change))}"
    
    return result.format(*range(1, result.count("{}") + 1))

def annotation(anno):
    result = ""
    if try_get(anno, "cfjs"):
        cfj_list = []
        for cfj in anno["cfjs"]:
            cfj_list.append("CFJ " + str(cfj["id"]))
            if cfj["called"] != None:
                cfj_list[-1] = f"{cfj_list[-1]} (called {date_string(cfj['called'])})"
            result = result + ", ".join(cfj_list) + ": ";
    result = result + anno["text"]
    return fixed_width(result)

def annotation_list(annos):
    result = ""

    for anno in annos:
        result = result + annotation(anno)

    return result

def full_rule(rule):
    global full_rule_format

    annotations = ""
    try: annotations = annotation_list(rule["annotations"])
    except KeyError: pass

    return full_rule_format.format(
        heading=rule_heading(rule),
        text=indent(rule["text"].strip()),
        history=history(rule["history"]).strip(),
        annotations=annotations.strip() if annotations != "" else "(none)",
        line=line("-")
    )

def fixed_width(input_string, w=72):
    instr = input_string.split(" ")
    result = [instr.pop(0)]
    for word in instr:
        if len(result[-1]) + len(word) + 1 <= w:
            result[-1] = result[-1] + " " + word
        else:
            if len(result) == 1: w = w-3
            result.append(word)
    return "\n   ".join(result)
