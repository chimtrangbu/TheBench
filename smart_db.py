#!/usr/bin/env python3
import sys
import json
from people import ListPeople


if __name__ == '__main__':
    data = sys.stdin.readlines()  # get content of csv file

    # get filename of json file
    list_args = sys.argv
    filename = list_args[list_args.index('./smart_db.py') + 1]

    # read json file
    with open(filename) as json_file:
        list_query_dicts = json.load(json_file)

    # run base on classes in people.py
    for query_dict in list_query_dicts:
        print(ListPeople(data).query(query_dict))
        
