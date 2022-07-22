from argparse import ArgumentParser as AP
import sys
from collections import Counter
import csv


delimiter = '\t'
infile = "Plant Data Dump - data dump.tsv"

with open(infile) as ifp:
    header = next(ifp).strip().split(delimiter)
    print(header)
    reader = csv.reader(ifp, delimiter=delimiter)
    toklists = list(reader)

header_cli_fields = ["-".join(map(str.lower, x.split())) for x in header]
header_cli_ids = {x: i for i, x in enumerate(header_cli_fields)}

while 1:
    print("There are command modes: pull up satisfied plants ('filter') and pull up similar plants ('discover'). 'quit' to exit.")
    mode = input("Which mode do you want to activate?")
    ACCEPTED = ('filter', 'discover', 'quit')
    if mode not in ACCEPTED:
        print("Mode " + mode + " not in accepted")
        continue
    if mode == 'quit':
        break
    if mode == 'filter':
        filter_list = ":".join(header_cli_fields)
        print("You can filter a specific field with its name from this list: '%s'" % filter_list, file=sys.stderr)
        print("Or search for a term globally by leaving it empty or 'global'", file=sys.stderr)
        global_mode = input('Which field?')
        if not global_mode:
            global_mode = "global"
        filter_arg = input("What query?").lower()
        if global_mode == "global":
            permit_func = lambda x: any(filter_arg in y.lower() for y in x)
        else:
            permit_func = lambda x: filter_arg in x[header_cli_ids[global_mode].lower()]
        filtered_toklists = list(filter(permit_func, toklists))
        if filtered_toklists:
            print("\n".join(["\t".join(x[:2]) for x in filtered_toklists]))
            print("\n".join(map(lambda x: "\t".join(x), filtered_toklists)))
        else:
            print("No filtered toklists found")
