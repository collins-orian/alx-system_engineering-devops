#!/usr/bin/python3
"""
Using https://jsonplaceholder.typicode.com
gathers data from API and exports it in JSON 
format
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

            users_data = {}
            for user in user_request:
                id = user.get('id')
                user_name = user.get('username')
                todos = list(
                    filter(lambda x: x.get('userId') == id, todos_request))
                user_data = list(map(
                    lambda x: {
                        'username': user_name,
                        'task': x.get('title'),
                        'completed': x.get('completed')
                    },
                    todos
                ))
                users_data['{}'.format(id)] = user_data
            with open('todo_all_employees.json', 'w') as file:
                json.dump(users_data, file)
