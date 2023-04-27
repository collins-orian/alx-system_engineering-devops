#!/usr/bin/python3
"""
Using https://jsonplaceholder.typicode.com
gathers data from API and exports it to JSON file
Implemented using recursion
"""
import re
import requests
import sys
import json


"""REST API url"""
API = "https://jsonplaceholder.typicode.com"


if __name__ == '__main__':
    if len(sys.argv) > 1:

        '''uses regular expressions to check if first command-line argument is an integer'''
        if re.fullmatch(r'\d+', sys.argv[1]):
            id = int(sys.argv[1])

            '''requests users from the API'''
            user_request = requests.get('{}/users/{}'.format(API, id)).json()

            '''requests the todos from the API'''
            todos_request = requests.get('{}/todos'.format(API)).json()

            '''gets the username, tasks from the information
            gotten from the api in json'''
            user_name = user_request.get('name')
            todos = list(filter(lambda x: x.get(
                'userId') == id, todos_request))

            '''create a json file and write content to the file'''
            with open("{}.json".format(id)) as json_file:
                user_data = list(map(
                    lambda x: {
                        "task": x.get("title"),
                        "completed": x.get("completed"),
                        "username": user_name
                    },
                    todos
                ))
                user_data = {
                    "{}".format(id): user_data
                }
                json.dump(user_data, json_file)
