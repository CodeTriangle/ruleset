from datetime import datetime as dt
import sys
from rulekeep import *
import yaml

if len(sys.argv) == 1:
    sys.exit("at least one argument needed (try 's' or 'f')")

# Argument handling
short = "s" in sys.argv[1]
full  = "f" in sys.argv[1]
regen = "r" in sys.argv[1]

slr = ""       # stores the SLR
flr = ""       # stores the FLR
toc = ""       # stores the Table of Contents
prop_list = {} # stores {id: sha1, power, title} of rules
rules = []

try:
    prop_list = string_tablist(get_contents("meta/proplist"))
    print("property list loaded")
except IOError:
    print("property list not found; continuing without")
    pass

smkdir("meta")
if short: smkdir("meta/short")
if full: smkdir("meta/full")

for section in yaml.load(get_contents("config/index"), Loader=yaml.FullLoader):
    if short: slr = slr + section_heading(section)
    if full:
        flr = flr + section_heading(section)
        toc = toc + section["name"] + "\n"

    for rule in section["rules"]:
        rules.append(rule)
        data = get_contents("rules/" + str(rule))

        if not regen:
            try:
                h = prop_list[str(rule)]
                if h[0] == get_hash(data):
                    if short: slr = slr + get_contents(f"meta/short/{rule}")
                    if full:
                        flr = flr + get_contents(f"meta/full/{rule}")
                        toc = toc + f"   * Rule {rule:>4}: {h[2]}\n"
                    print(f"{rule}\tunchanged")
                    continue
            except: print(f"{rule}\tchanged")
        else: print(f"{rule}\tprocessing")

        ldata = yaml.load(data, Loader=yaml.FullLoader)
        
        prop_list[str(rule)] = [
            get_hash(data),
            ldata["power"],
            ldata["name"]
        ]

        if short:
            gen = short_rule(ldata)
            
            print("\tprocessed short rule")
            write_file("meta/short/" + str(rule), gen)
            slr = slr + gen
        if full:
            gen = full_rule(ldata)
            toc = toc + f"   * Rule {rule:>4}: {ldata['name']}\n"
            
            print("\tprocessed full rule")
            write_file(f"meta/full/{rule}", gen)
            flr = flr + gen

header = get_contents("config/header").format(
    **get_stats(),
    her=max(rules),
    num=len(rules)
)

powers = {}

for rule in rules:
    power = str(prop_list[str(rule)][1])
    try: powers[power] = powers[power] + 1
    except KeyError: powers[power] = 1

power_string = "\n".join(
    [f"{powers[i]:<2} with Power={i}" for i in sorted(powers.keys())]
)

if short: write_file(
    "slr.txt", get_contents("config/slr_format").format(
        header=header, ruleset=slr
    )
)

if full:
    write_file(
    "flr.txt", get_contents("config/flr_format").format(
        header=header, line=line("-"), toc=toc, ruleset=flr, powers=power_string
    )
)

write_file("meta/proplist", tablist_string(prop_list))
